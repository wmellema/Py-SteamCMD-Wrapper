import os
import shutil
from pysteamcmdwrapper import SteamCMD
inst_dir = "tmp_installation"


def testCorrectDir():
    _inst_dir = inst_dir+"1"
    try:
        if not os.path.isdir(_inst_dir):
            os.mkdir(_inst_dir)
        s = SteamCMD(_inst_dir)
        assert s is not None
    except Exception as e:
        if os.path.isdir(_inst_dir):
            shutil.rmtree(_inst_dir, ignore_errors=True)
        raise e
    finally:
        shutil.rmtree(_inst_dir, ignore_errors=True)


def testSetup():
    _inst_dir = inst_dir+"2"
    try:
        if not os.path.isdir(_inst_dir):
            os.mkdir(_inst_dir)
        s = SteamCMD(_inst_dir)
        assert s is not None
        s.install()
        assert os.path.isdir(_inst_dir+'/package')
    except Exception as e:
        if os.path.isdir(_inst_dir):
            shutil.rmtree(_inst_dir, ignore_errors=True)
        raise e
    finally:
        shutil.rmtree(_inst_dir, ignore_errors=True)


def testGameDownload():
    _inst_dir = inst_dir+"3"
    try:
        if not os.path.isdir(_inst_dir):
            os.mkdir(_inst_dir)
        s = SteamCMD(_inst_dir)
        assert s is not None
        s.install()
        s.app_update(17575, os.path.join(os.getcwd(), "tmp_game"), validate=True)
        # return
        assert os.path.isdir(os.path.join(os.getcwd(), "tmp_game")+'/hl2')
    except Exception as e:
        if os.path.isdir(_inst_dir):
            shutil.rmtree(_inst_dir, ignore_errors=True)
            shutil.rmtree("tmp_game", ignore_errors=True)
        raise e
    finally:
        shutil.rmtree(_inst_dir, ignore_errors=True)
        shutil.rmtree("tmp_game", ignore_errors=True)


def test_workshop_download():
    _inst_dir = inst_dir+"4"
    try:
        if not os.path.isdir(_inst_dir):
            os.mkdir(_inst_dir)
        s = SteamCMD(_inst_dir)
        assert s is not None
        s.install()
        # s.app_update(1840, os.path.join(os.getcwd(), "tmp_csgo"), validate=True)
        # return
        s.workshop_update(107410, 450814997, os.path.join(os.getcwd(), "tmp_armamod/"), validate=True)
        assert os.path.isfile(os.path.join(
                os.getcwd(),
                "tmp_armamod",
                "steamapps",
                "workshop",
                "content",
                "107410",
                "450814997",
                "README.md"
                ))
    except AssertionError as e:
        print(os.system("tree "+os.getcwd()))
        raise e
    except Exception as e:
        if os.path.isdir(_inst_dir):
            shutil.rmtree(_inst_dir, ignore_errors=True)
            shutil.rmtree("tmp_csgo", ignore_errors=True)
        raise e
    finally:
        shutil.rmtree(_inst_dir, ignore_errors=True)
        shutil.rmtree("tmp_csgo", ignore_errors=True)


if __name__ == "__main__":
    test_workshop_download()
