![](https://github.com/panda-official/TimeSwipe.py/workflows/Workflow/badge.svg) [![PyPI version](https://badge.fury.io/py/timeswipe.svg)](https://badge.fury.io/py/timeswipe)

## Install from binary wheels

### Raspbian armv7l
```
sudo apt-get update
sudo apt install python3-pip
sudo pip3 install timeswipe
```

### Arch linux aarch64 python 3.8
```
sudo pacman -S python-pip
sudo pip3 install wheel
sudo pip3 install `curl -s https://api.github.com/repos/panda-official/TimeSwipe.py/releases/latest | grep "browser_download_url.*timeswipe.*38.*aarch64.whl" | cut -d : -f 2,3 | tr -d \"`

```

### TimeSwipeOS python 3.8 (unsecure)
```
pip3 install wheel
pip3 install `curl -k -s https://api.github.com/repos/panda-official/TimeSwipe.py/releases/latest | grep "browser_download_url.*timeswipe.*38.*aarch64.whl" | cut -d : -f 2,3 | tr -d \"`
```

## Install from source wheel

### Raspbian

Install timeswipe driver deb packet from https://github.com/panda-official/TimeSwipe/releases

```
sudo apt-get update
sudo apt install python3-pip cmake g++ make libboost-python-dev
sudo pip3 install --upgrade pip
sudo pip3 install --no-binary :all: timeswipe
```

### Arch linux

Install timeswipe driver arch packet from https://github.com/panda-official/TimeSwipe/releases

```
sudo pacman -S python-pip cmake gcc make boost pkgconf
sudo pip3 install --upgrade pip
sudo pip3 install wheel
sudo pip3 install --no-binary :all: timeswipe
```
## Usage
Run Python script with Timeswipe dependency as root (sudo) because permission to access GPIO is needed.
 
## Develop

### Prepare on Raspbian

Install timeswipe deb packet from https://github.com/panda-official/TimeSwipe/releases

```
sudo apt install git cmake g++ make libboost-python-dev
sudo pip3 install wheel
```

### Prepare on Arch linux

Install timeswipe arch packet from https://github.com/panda-official/TimeSwipe/releases

```
sudo pacman -S python-pip cmake gcc make boost pkgconf git
sudo pip3 install wheel
```

### Build source wheel
```
git clone https://github.com/panda-official/TimeSwipe.py
cd TimeSwipe.py
python3 setup.py sdist
```

### Build binary wheel
```
git clone https://github.com/panda-official/TimeSwipe.py
cd TimeSwipe.py
python3 setup.py bdist_wheel
```

## Release new version on master branch

increment version in [setup.py](setup.py)
```
git tag v`python3 setup.py --version`
git push origin v`python3 setup.py --version`
```

