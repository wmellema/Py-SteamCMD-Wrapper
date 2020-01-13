import unittest, os, shutil,platform
from pysteamcmdwrapper import *


class TestInstallation(unittest.TestCase):
    def testCorrectDir(self):
        try:
            os.mkdir('dir')
            s = SteamCMD("dir")
            assert s is not None
        except Exception as e:
            if os.path.isdir('dir'):
                shutil.rmtree('dir',ignore_errors=True)
            raise e
        shutil.rmtree('dir',ignore_errors=True)
    def testIncorrectDir(self):
        self.assertRaises(SteamCMDInstallException,SteamCMD,installation_path="dir1")

    def testSetup(self):
        pass
    def testGameDownload(self):
        try:
            os.mkdir('dir')
            s = SteamCMD("dir")
            assert s is not None
            s.install()
            s.app_update(233780,validate=True)
            assert os.path.isfile('dir/steamapps/common/Arma 3 Server/mpmissions/readme.txt')
        except Exception as e:
            if os.path.isdir('dir'):
                pass
                shutil.rmtree('dir',ignore_errors=True)
            raise e
        shutil.rmtree('dir',ignore_errors=True)

if __name__ == '__main__':
    unittest.main()
