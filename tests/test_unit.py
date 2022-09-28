from pysteamcmdwrapper import SteamCMD, SteamCMD_command

def testWorkshopDownloadCommand():
    sc = SteamCMD_command()
    sc.workshop_download_item(1,2)
    assert sc.get_cmd() == '+workshop_download_item 1 2'

def testWorkshopDownloadCommandValidate():
    sc = SteamCMD_command()
    sc.workshop_download_item(1,2, True)
    assert sc.get_cmd() == '+workshop_download_item 1 2 validate'

def testWorkshopDownloadCommandForceDir():
    sc = SteamCMD_command()
    sc.force_install_dir("a")
    sc.workshop_download_item(1,2)
    assert sc.get_cmd() == '+force_install_dir "a" +workshop_download_item 1 2'

def testAppUpdate():
    sc = SteamCMD_command()
    sc.app_update(1)
    assert sc.get_cmd() == '+app_update 1'

def testAppUpdateValidate():
    sc = SteamCMD_command()
    sc.app_update(1, validate=True)
    assert sc.get_cmd() == '+app_update 1 validate'

def testAppUpdateBeta():
    sc = SteamCMD_command()
    sc.app_update(1, beta='test')
    assert sc.get_cmd() == '+app_update 1 -beta test'

def testAppUpdateBetaValidate():
    sc = SteamCMD_command()
    sc.app_update(1, validate=True, beta='test')
    assert sc.get_cmd() == '+app_update 1 validate -beta test'

def testAppUpdateBetaPass():
    sc = SteamCMD_command()
    sc.app_update(1, beta_pass='mypass')
    assert sc.get_cmd() == '+app_update 1 -betapassword mypass'

def testForceInstallDir():
    sc = SteamCMD_command()
    sc.force_install_dir("mydir")
    assert sc.get_cmd() == '+force_install_dir "mydir"'

def testCustom():
    sc = SteamCMD_command()
    sc.custom("testcommand")
    assert sc.get_cmd() == 'testcommand'

def testChainCommand():
    sc = SteamCMD_command()
    sc.force_install_dir("mydir")
    sc.app_update(1, validate=True)
    sc.custom("mycustomcommand")
    assert sc.get_cmd() == '+force_install_dir "mydir" +app_update 1 validate mycustomcommand'

def testCommandRemove():
    sc = SteamCMD_command()
    sc.force_install_dir("mydir")
    sc.app_update(1, validate=True)
    sc.custom("mycustomcommand")
    assert sc.get_cmd() == '+force_install_dir "mydir" +app_update 1 validate mycustomcommand'
    assert sc.remove(1)
    assert sc.get_cmd() == '+force_install_dir "mydir" mycustomcommand'
    assert not sc.remove(3)
