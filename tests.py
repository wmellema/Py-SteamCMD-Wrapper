import unittest, os, shutil,platform
from pysteamcmdwrapper import *

inst_dir = "tmp_installation"

class TestInstallation(unittest.TestCase):
    def testCorrectDir(self):
        try:
            if not os.path.isdir(inst_dir):
                os.mkdir(inst_dir)
            s = SteamCMD(inst_dir)
            assert s is not None
        except Exception as e:
            if os.path.isdir(inst_dir):
                shutil.rmtree(inst_dir,ignore_errors=True)
            raise e
        finally:
            shutil.rmtree(inst_dir,ignore_errors=True)
    def testIncorrectDir(self):
        self.assertRaises(SteamCMDInstallException,SteamCMD,installation_path="dir1")

    def testSetup(self):
        try:
            if not os.path.isdir(inst_dir):
                os.mkdir(inst_dir)
            s = SteamCMD(inst_dir)
            assert s is not None
            s.install()
            assert os.path.isdir(inst_dir+'/package')
        except Exception as e:
            if os.path.isdir(inst_dir):
                shutil.rmtree(inst_dir,ignore_errors=True)
            raise e
        finally:
            shutil.rmtree(inst_dir,ignore_errors=True)

    def testGameDownload(self):
        try:
            if not os.path.isdir(inst_dir):
                os.mkdir(inst_dir)
            s = SteamCMD(inst_dir)
            assert s is not None
            s.install()
            s.app_update(17575,validate=True)
            # return
            assert os.path.isdir(inst_dir+'/steamapps/common/Pirates, Vikings, and Knights II Dedicated Server/hl2')
        except Exception as e:
            if os.path.isdir(inst_dir):
                shutil.rmtree(inst_dir,ignore_errors=True)
            raise e
        finally:
            shutil.rmtree(inst_dir,ignore_errors=True)

if __name__ == '__main__':
    unittest.main()
