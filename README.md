# Py-SteamCMD-Wrapper
![coverage](https://img.shields.io/badge/coverage-68%25-yellowgreen)
[![HitCount](http://hits.dwyl.com/wmellema/Py-SteamCMD-Wrapper.svg)](http://hits.dwyl.com/wmellema/Py-SteamCMD-Wrapper)


During the setup of game servers it can be infuriating to use SteamCMD due to some particularities within the SteamCMD Toolkit. This simple wrapper for python will handle everything from installation to downloading games.

## Getting Started

These instructions will get you a copy of the project up and running on your machine for development and testing purposes

### Prerequisites
When installing on linux, you'll need the 32-bit libraries specified on the [valvesoftware](https://developer.valvesoftware.com/wiki/SteamCMD#32-bit_libraries_on_64-bit_Linux_systems) website.

#### Ubuntu
```
sudo apt-get install lib32stdc++6
```
If you get an error for missing dependencies or broken packages, run the following
```
 dpkg --add-architecture i386
 apt-get update
 apt-get install lib32gcc1
 ```
 #### RHEL, Fedora, CentOS, etc.
 ```
 yum install glibc.i686 libstdc++.i686
```

#### Arch Linux
Enable the [multilib repository](https://wiki.archlinux.org/index.php/Multilib)
```
pacman -S lib32-gcc-libs
```

### Installing

Run the following command to install the package
```bash
pip install py-steamcmd-wrapper
```

In order to install steam using this wrapper you'll have to do the following:
``` python
from pysteamcmdwrapper import SteamCMD

steam = SteamCMD("MyInstallationDir")
steam.install()
```

### Usage
Curently there are 4 methods available in the wrapper. These are as follows:
- install
- login
- app_update
- workshop_update

You can use these methods to install steamcmd, login a user, download a game/gameserver or a workshop mod.
If your game needs a valid subscription (AKA you've bought the game) the login function needs to be called. When left empty, it will prompt for login information.

A small code snippet to install an Arma III dedicated server with CBA_A3 installed
```python
import os
from pysteamcmdwrapper import SteamCMD, SteamCMDException

SERVER_DIR = "armaserver"
WORKSHOP_DIR = os.path.join(os.getcwd(),"armamods","steamapps","workshop","content","107410")
MOD_DIR = os.path.join(os.getcwd(),SERVER_DIR)

s = SteamCMD("steamcmd")
try:
    s.install()
except SteamCMDException:
    print("Already installed, try to use the --force option to force installation")

s.login()
s.app_update(233780,os.path.join(os.getcwd(),SERVER_DIR),validate=True)

modname = "cba_a3"
id = "450814997"
s.workshop_update(107410,id,os.path.join(os.getcwd(),"armamods/"),validate=True)
try:
    os.symlink(os.path.join(WORKSHOP_DIR,id),os.path.join(MOD_DIR,"@"+modname))
except FileExistsError:
    print("Already linked")
keydir = os.path.join(MOD_DIR,"@"+modname,"keys")
if not os.path.isdir(keydir):
    keydir = os.path.join(MOD_DIR,"@"+modname,"key")
for key in os.listdir(keydir):
    print("Linking ",key)
    try:
        os.symlink(os.path.join(keydir,key),os.path.join(MOD_DIR,"keys",key))
    except FileExistsError:
        print("Already Linked")
```

> This snippet can be used with another project of mine. This will be coming soon!

The login function is only needed when a subscription to the game is needed. The wrapper uses the 'Anonymous' user by default

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/wmellema/39a671fa6c6ffda66b4bd689f53c57f1) for details on our code of conduct, and the process for submitting pull requests to me.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](#).

## Authors

* **Wouter Mellema** - *Initial work* - [wmellema](https://github.com/wmellema)

See also the list of [contributors](https://github.com/wmellema/Py-SteamCMD-Wrapper/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [f0rkz](https://github.com/f0rkz), whose original [pysteamcmd](https://github.com/f0rkz/pysteamcmd) project was abandoned, but still very usefull as a building block
