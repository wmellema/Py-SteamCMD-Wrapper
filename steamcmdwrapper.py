#!/usr/bin/env python3

__author__      = "Wouter Mellema"
__copyright__   = "Copyright 2020"
__licence__     = "GNU GPLv3"
__version__     = "1.0.0"
__maintainer__  = "Wouter Mellema"
__status__      = "Development"

import os
import platform
import zipfile
import subprocess
import urllib.request

from getpass import getpass


package_links = {"Windows":{"url":"https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip","extention":".exe","d_extention":".zip"},
                 "Linux":{"url":"https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz","extention":".sh","d_extention":".tar.gz"}}

class SteamCMDException(Exception):
    """
    Base exception for steamcmdwrapper
    """
    def __init__(self,message=None,*args,**kwargs):
        self.message = message
        super(SteamCMDException,self).__init__(*args,**kwargs)

    def __unicode__(self):
        return repr(self.message)

    def __str__(self):
        return repr(self.message)

class SteamCMD():
    installation_path = ""
    uname = "anonymous"
    passw = None
    
    def __init__(self,installation_path):
        self.installation_path = installation_path

        if not os.path.isdir(self.installation_path):
            raise SteamCMDException("No valid directory found at {}. Please make sure that the directory is correct.".format(self.installation_path))

        self._check_install_requirements()

    def _check_install_requirements(self):
        """
        Checks if everything is in order and sets the required parameters
        """
        self.platform = platform.system()
        if not self.platform in ["Windows","Linux"]:
            raise SteamCMDException("Non supported operatingsystem. Expected Windows or Linux, got {}".format(self.platform))
        self.steamcmd_url = package_links[self.platform]["url"]
        self.zip = "steamcmd"+package_links[self.platform]["d_extention"]
        self.exe = os.path.join(self.installation_path,"steamcmd"+package_links[self.platform]["extention"])

    def _download(self):
        """
        Internal method to download the SteamCMD Binaries from steams' servers.
        :return: downloaded data for debug purposes
        """
        try:
            resp = urllib.request.urlopen(self.steamcmd_url)
            data = resp.read()
            with open(self.zip,"wb") as f:
                f.write(data)
            return data
        except Exception as e:
            raise SteamCMDException("An unknown exception occured during downloading. {}".format(e))

    def _extract_steamcmd(self):
        """
        Internal method for extracting downloaded zip file. Works on both windows and linux.
        :return: location of extracted folder
        """
        if self.platform == 'Windows':
            with zipfile.ZipFile(self.zip, 'r') as f:
                return f.extractall(self.installation_path)

        elif self.platform == 'Linux':
            with tarfile.open(self.zip, 'r:gz') as f:
                return f.extractall(self.installation_path)

        else:
            # This should never happen, but let's just throw it just in case.
            raise SteamCMDException('The operating system is not supported.'
                                      'Expected Linux or Windows, received: {}'.format(self.platform))
    def install(self, force=False):
        """
        Installs steamcmd if it is not already installed to self.install_path.
        :param force: forces steamcmd install regardless of its presence
        :return:
        """
        if not os.path.isfile(self.exe) or force == True:
            # Steamcmd isn't installed. Go ahead and install it.
            self._download()
            self._extract_steamcmd()

        else:
            raise SteamCMDException('Steamcmd is already installed. Reinstall is not necessary.'
                                    'Use force=True to override.')
        subprocess.check_call((self.exe,"+quit"))
        return

    def login(self,uname=None,passw=None):
        """
        Login function in order to do a persistent login on the steam servers.
        Prompts users for their credentials and spawns a child process.
        :param uname: Steam Username
        :param passw: Steam Password
        :return: status code of child process
        """
        self.uname = uname if uname else input("Please enter steam username: ")
        self.passw = passw if passw else getpass("Please enter steam password: ")

        params = (
            self.exe,
            "+login {} {}".format(self.uname,self.passw),
            "+quit",
        )

        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamCMDException("Steamcmd was unable to run.")

    def app_update(self, app_id, install_dir = None, validate = False):
        """
        Installer function for apps.
        :param app_id: The Steam ID for the app you want to install
        :param install_dir: Optional custom installation directory.
        :param validate: Optional parameter for validation. Turn this on when redownloading something
        :return: Status code of child process
        """

        validate = 'validate' if validate else None
        install_dir = '+force_install_dir "{}"'.format(install_dir) if install_dir else None

        params = (
            self.exe,
            "+login {} {}".format(self.uname,self.passw),
            "{}".format(install_dir),
            "+app_update {}".format(app_id),
            "{}".format(validate),
            "+quit",
        )

        try:

            return subprocess.check_call(params)
        except subprocess.CalledProcessError as e:
            print(e)
            raise SteamCMDException("Steamcmd was unable to run.")


    def workshop_update(self, app_id, workshop_id, install_dir = None, validate = None, n_tries = 5):
        """
        Installer function for workshop content. Retries multiple times on timeout due to valves'
        stupid timeout on large downloads.
        :param app_id: The parent application ID
        :param workshop_id: The ID for workshop content. Can be found in the url.
        :param install_dir: Optional custom installation directory.
        :param validate: Optional parameter for validation. Turn this on when redownloading something
        :param n_tries: Counter for how many redownloads it can make before officially timing out.
        :return: Status code of child process
        """

        if n_tries == 0:
            raise SteamCMDException("Max number of tries exceeded!")
        _validate = 'validate' if validate else None
        _install_dir = '+force_install_dir "{}"'.format(install_dir) if install_dir else None

        params = (
            self.exe,
            "+login {} {}".format(self.uname,self.passw),
            "{}".format(_install_dir),
            "+workshop_download_item {} {}".format(app_id,workshop_id),
            "{}".format(_validate),
            "+quit",
        )

        try:

            return subprocess.check_call(params)
        except subprocess.CalledProcessError as e:
            print(e.returncode)
            if e.returncode == 10:
                print("")
                print("Download timeout, trying again...")
                return self.workshop_update(app_id,workshop_id,install_dir,validate,n_tries-1)
            raise SteamCMDException("Steamcmd was unable to run. exit code was {}".format(e.returncode))
