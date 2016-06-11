PRIME Indicator
===============
Indicator applet for Ubuntu 14.04 and higher laptop users with NVIDIA/Intel hybrid GPUs,
allowing quick switch between the GPUs in matter of seconds.
It has been tested on Ubuntu 14.04 and 16.04 only, but should be working just as well
on any Ubuntu distribution, more recent than 12.04, including Xubuntu, Kubuntu and Lubuntu flavours.
Ubuntu 12.04 users should also have no problems, as long if installing with the newest hardware enablement stack.


Prerequisites
=============
Make sure you have installed and enabled:

* NVIDIA driver, version 331.20 or higher
* NVIDIA's additional package, `nvidia-prime`
* `mesa-utils` package
* `python-appindicator` package

Or simply run the following, which will install all dependencies and the latest NVIDIA driver for your GPU.
```
sudo apt-get install nvidia-prime nvidia-settings python-appindicator mesa-utils
sudo apt-get install $(sudo ubuntu-drivers devices | grep -o nvidia-[[:digit:]]*)
```


Troubleshooting
===============

### `appindicator` module missing
Install the `python-appindicator` package.

### Couldn't find RGB GLX visual or fbconfig
Install the `mesa-utils` package.


Installation
============
```shell
chmod a+x setup.sh
sudo ./setup.sh
```
