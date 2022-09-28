from pysteamcmdwrapper import SteamCMD, SteamCMD_command

def testWorkshopDownloadCommand():
    sc = SteamCMD_command()
    sc.workshop_download_item(1,2)
    if sc.get_cmd() != '+workshop_download_item 1 2':
        raise AssertionError

def testWorkshopDownloadCommandValidate():
    sc = SteamCMD_command()
    sc.workshop_download_item(1,2, True)
    if sc.get_cmd() != '+workshop_download_item 1 2 validate':
        raise AssertionError

def testWorkshopDownloadCommandForceDir():
    sc = SteamCMD_command()
    sc.force_install_dir("a")
    sc.workshop_download_item(1,2)
    if sc.get_cmd() != '+force_install_dir "a" +workshop_download_item 1 2':
        raise AssertionError


def testAppUpdate():
    sc = SteamCMD_command()
    sc.app_update(1)
    if sc.get_cmd() != '+app_update 1':
        raise AssertionError

def testAppUpdateValidate():
    sc = SteamCMD_command()
    sc.app_update(1, validate=True)
    if sc.get_cmd() != '+app_update 1 validate':
        raise AssertionError

def testAppUpdateBeta():
    sc = SteamCMD_command()
    sc.app_update(1, beta='test')
    if sc.get_cmd() != '+app_update 1 -beta test':
        raise AssertionError

def testAppUpdateBetaValidate():
    sc = SteamCMD_command()
    sc.app_update(1, validate=True, beta='test')
    if sc.get_cmd() != '+app_update 1 validate -beta test':
        raise AssertionError

def testAppUpdateBetaPass():
    sc = SteamCMD_command()
    sc.app_update(1, beta_pass='mypass')
    if sc.get_cmd() != '+app_update 1 -betapassword mypass':
        raise AssertionError

def testForceInstallDir():
    sc = SteamCMD_command()
    sc.force_install_dir("mydir")
    if sc.get_cmd() != '+force_install_dir "mydir"':
        raise AssertionError

def testCustom():
    sc = SteamCMD_command()
    sc.custom("testcommand")
    if sc.get_cmd() != 'testcommand':
        raise AssertionError

def testChainCommand():
    sc = SteamCMD_command()
    sc.force_install_dir("mydir")
    sc.app_update(1, validate=True)
    sc.custom("mycustomcommand")
    if sc.get_cmd() != '+force_install_dir "mydir" +app_update 1 validate mycustomcommand':
        raise AssertionError

def testCommandRemove():
    sc = SteamCMD_command()
    sc.force_install_dir("mydir")
    sc.app_update(1, validate=True)
    sc.custom("mycustomcommand")
    if sc.get_cmd() != '+force_install_dir "mydir" +app_update 1 validate mycustomcommand':
        raise AssertionError
    if not sc.remove(1):
        raise AssertionError
    if sc.get_cmd() != '+force_install_dir "mydir" mycustomcommand':
        raise AssertionError
    if sc.remove(3):
        raise AssertionError
