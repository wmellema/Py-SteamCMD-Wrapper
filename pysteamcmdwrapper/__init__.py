#!/usr/bin/env python3

__author__ = "Wouter Mellema"
__copyright__ = "Copyright 2020"
__licence__ = "GNU GPLv3"
__version__ = "1.0.5"
__maintainer__ = "Wouter Mellema"
__status__ = "Development"

import os
import platform
import zipfile
import subprocess
import urllib.request

from getpass import getpass


package_links = {
    "Windows": {
        "url": "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip",
        "extention": ".exe",
        "d_extention": ".zip"
    },
    "Linux": {
        "url": "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz",
        "extention": ".sh",
        "d_extention": ".tar.gz"
    }
}


class SteamCMDException(Exception):
    """
    Base exception for steamcmdwrapper
    """
    def __init__(self, message=None, *args, **kwargs):
        self.message = message
        super(SteamCMDException, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return repr(self.message)

    def __str__(self):
        return repr(self.message)


class SteamCMDDownloadException(SteamCMDException):
    """
    Class for handeling download exceptions
    """
    def __init__(self, *args, **kwargs):
        super(SteamCMDDownloadException, self).__init__(*args, **kwargs)


class SteamCMDInstallException(SteamCMDException):
    """
    Class for handeling installation exceptions
    """
    def __init__(self, *args, **kwargs):
        super(SteamCMDInstallException, self).__init__(*args, **kwargs)


class SteamCMD():
    """
    Wrapper for SteamCMD
    Will install from source depending on OS.
    """

    _installation_path = ""
    _uname = "anonymous"
    _passw = ""

    def __init__(self, installation_path):
        self._installation_path = installation_path

        if not os.path.isdir(self._installation_path):
            raise SteamCMDInstallException("""
            No valid directory found at {}.
            Please make sure that the directory is correct.
            """.format(self._installation_path))

        self._prepare_installation()

    def _prepare_installation(self):
        """
        Sets internal configuration accoring to parameters and OS
        """

        self.platform = platform.system()
        if self.platform not in ["Windows", "Linux"]:
            raise SteamCMDException("""
            Non supported operatingsystem. Expected Windows or Linux, got {}
            """.format(self.platform))

        self.steamcmd_url = package_links[self.platform]["url"]
        self.zip = "steamcmd"+package_links[self.platform]["d_extention"]
        self.exe = os.path.join(
            self._installation_path,
            "steamcmd"+package_links[self.platform]["extention"]
            )

    def _download(self):
        """
        Internal method to download the SteamCMD Binaries from steams' servers.

        :return: downloaded data for debug purposes
        """
        try:
            resp = urllib.request.urlopen(self.steamcmd_url)
            data = resp.read()
            with open(self.zip, "wb") as f:
                f.write(data)
            return data
        except Exception as e:
            raise SteamCMDException(
                "An unknown exception occured during downloading. {}".format(e)
                )

    def _extract_steamcmd(self):
        """
        Internal method for extracting downloaded zip file. Works on both
        windows and linux.

        :return: location of extracted folder
        """
        ext = ""
        if self.platform == 'Windows':
            with zipfile.ZipFile(self.zip, 'r') as f:
                ext = f.extractall(self._installation_path)

        elif self.platform == 'Linux':
            import tarfile
            with tarfile.open(self.zip, 'r:gz') as f:
                ext = f.extractall(self._installation_path)

        else:
            # This should never happen, but let's just throw it just in case.
            raise SteamCMDException(
                'The operating system is not supported.'
                'Expected Linux or Windows, received: {}'.format(self.platform)
                )

        os.remove(self.zip)
        return ext

    def _print_log(self, *message):
        """
        Small helper function for printing log entries.
        Helps with output of subprocess.check_call not always having newlines

        :param *message: Accepts multiple messages, each will be printed on a
        new line
        """
        # TODO: Handle logs better
        print("")
        print("")
        for msg in message:
            print(msg)
        print("")

    def install(self, force=False):
        """
        Installs steamcmd if it is not already installed to self.install_path.

        :param force: forces steamcmd install regardless of its presence
        :return:
        """
        if not os.path.isfile(self.exe) or force:
            # Steamcmd isn't installed. Go ahead and install it.
            self._download()
            self._extract_steamcmd()

        else:
            raise SteamCMDException(
                'Steamcmd is already installed. Reinstall is not necessary.'
                'Use force=True to override.'
                )
        try:
            subprocess.check_call((self.exe, "+quit"))
        except subprocess.CalledProcessError as e:
            if e.returncode == 7:
                self._print_log(
                    "SteamCMD has returned error code 7 on fresh installation",
                    "",
                    "Not sure why this crashed,",
                    "long live steamcmd and it's non existent documentation..",
                    "It should be fine nevertheless")
                return
            else:
                raise SteamCMDInstallException(
                    "Failed to install, check error code {}".format(e.returncode))

        return

    def login(self, uname=None, passw=None):
        """
        Login function in order to do a persistent login on the steam servers.
        Prompts users for their credentials and spawns a child process.

        :param uname: Steam Username
        :param passw: Steam Password
        :return: status code of child process
        """
        self._uname = uname if uname else input("Please enter steam username: ")
        self._passw = passw if passw else getpass("Please enter steam password: ")

        params = (
            self.exe,
            "+login {} {}".format(self._uname, self._passw),
            "+quit",
        )

        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamCMDException("Steamcmd was unable to run.")

    def app_update(self, app_id, install_dir=None, validate=None, beta=None, betapassword=None):
        """
        Installer function for apps.

        :param app_id: The Steam ID for the app you want to install
        :param install_dir: Optional custom installation directory.
        :param validate: Optional parameter for validation. Turn this on
        when redownloading something
        :param beta: Optional parameter for running a beta branch.
        :param betapassword: Optional parameter for entering beta password.
        :return: Status code of child process
        """
        # TODO: Validate seems to be broken. Check why
        # TODO: Note: Non validated downloads will sometimes return error code 8. Just leave validate on?
        _validate = 'validate' if validate else ""
        _install_dir = '+force_install_dir "{}"'.format(install_dir) if install_dir else ""
        _beta = '-beta {}'.format(beta) if beta else ""
        _betapassword = '-betapassword {}'.format(betapassword) if betapassword else ""

        params = (
            self.exe,
            "+login {} {}".format(self._uname, self._passw),
            "{}".format(_install_dir),
            "+app_update {}".format(app_id),
            "{}".format(_beta),
            "{}".format(_betapassword),
            "{}".format(_validate),
            "+quit",
        )
        self._print_log("Parameters used:", " ".join(e for e in params if e))
        self._print_log(
            "Downloading item {}".format(app_id),
            "into {} with validate set to {}".format(_install_dir, validate))
        try:
            return subprocess.check_call(" ".join(e for e in params if e), shell=True)
        except subprocess.CalledProcessError as e:
            self._print_log(e)
            raise SteamCMDException("Steamcmd was unable to run.")

    def workshop_update(self, app_id, workshop_id, install_dir=None, validate=None, n_tries=5):
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
        # TODO: Validate seems to be broken. Check why
        # TODO: Note: Non validated downloads will sometimes return error code 8. Just leave validate on?
        if n_tries == 0:
            raise SteamCMDDownloadException(
                """Error downloading file, max number of timeout tries exceeded!
                Consider increasing the n_tries parameter if the download is
                particularly large"""
                )
        _validate = 'validate' if validate else ""
        _install_dir = '+force_install_dir "{}"'.format(install_dir) if install_dir else ""

        params = (
            self.exe,
            "+login {} {}".format(self._uname, self._passw),
            "{}".format(_install_dir),
            "+workshop_download_item {} {}".format(app_id, workshop_id),
            "{}".format(_validate),
            "+quit",
        )
        self._print_log("Parameters used:", " ".join(e for e in params if e))
        self._print_log(
            "Downloading {}".format(workshop_id),
            "On try {}".format(n_tries)
            )
        try:
            return subprocess.check_call(" ".join(e for e in params if e), shell=True)

        except subprocess.CalledProcessError as e:
            # SteamCMD has a habit of timing out large downloads, so if the
            # Validate flag is set, retry on timeout for the remainder of
            # n_tries.
            if e.returncode == 10:
                if _validate:
                    self._print_log("Download timeout! Retry due to validate flag")
                    return self.workshop_update(
                        app_id, workshop_id, install_dir, validate, n_tries-1
                    )
                else:
                    raise SteamCMDDownloadException(
                        """
                        SteamCMD was not able to complete this download due to a
                        download timeout. Please add the Validate flag in order to
                        keep retrying this download."""
                    )
            # SteamCMD sometimes crashes when timing out downloads, due to
            # an assert checking that the download actually finished.
            # If this happens, retry if the validate flag is set like above.
            elif e.returncode == 134:
                if _validate:
                    self._print_log("SteamCMD errored! Retry due to validate flag")
                    return self.workshop_update(
                        app_id, workshop_id, install_dir, validate, n_tries - 1
                    )
                else:
                    raise SteamCMDDownloadException(
                        """
                        SteamCMD was not able to complete this download due to a
                        SteamCMD error. Please add the Validate flag in order to
                        keep retrying this download."""
                    )
            raise SteamCMDException(
                """Steamcmd was unable to run. exit code was {}
                """.format(e.returncode)
            )
