PRIME Indicator
===============
Indicator applet for Ubuntu 14.04 and higher laptop users with NVIDIA/Intel hybrid GPUs,
allowing quick switch between the GPUs in matter of seconds.
It has been tested on Ubuntu 16.04 only, but should be working just as well
on any Ubuntu distribution more recent than 12.04, including Xubuntu, Kubuntu and Lubuntu flavours.
Ubuntu 12.04 users should also have no problems, as long if installing with the newest hardware enablement stack.

It should also work on any Linux distribution that includes the minimum dependencies listed in the Prerequisites section and a package that provides the same functionality Ubuntu's `nvidia-prime` does.

This version features full power saving by completely disabling the NVIDIA GPU when it's not being used. 
NVIDIA PRIME won't do it by default, leaving NVIDIA GPU powered on even when it's using the Intel GPU only.
While this saves some power (because the NVIDIA GPU is idle), it still consumes about 4~5W more than with it 
completely off. Since this is not ideal, this version is extended to use bbswitch to power the NVIDIA GPU off. 
Still, should the need for it to be on arrise, this version provides an option to force it to stay powered on
when using integrated graphics only, so it can be used for GPGPU and other tasks other than rendering.

In Ubuntu-based distros, the power management is implemented using the gpumanager service. If you're running an Ubuntu-based distro, it's likely you won't see much battery-life related benefits when running this version. However, if for any reason gpumanager is not working for you, this version is worth trying as it's able to overcome some situations where gpumanager might fail to turn the dGPU off (such as when using the latest NVIDIA drivers from the Proprietary Graphics Drivers PPA, https://bugs.launchpad.net/ubuntu/+source/ubuntu-drivers-common/+bug/1619306).

There's currently support for the following Desktop Environments:

* Budgie
* Cinnamon
* GNOME
* KDE
* LXDE
* LXQt
* MATE
* Unity
* XFCE

Prerequisites
=============
Make sure you have installed and enabled:

* NVIDIA driver, version 331.20 or higher
* NVIDIA's additional package, `nvidia-prime`
* `mesa-utils` package
* `python3` package
* `gir1.2-appindicator3` package
* `bbswitch-dkms` package

Or simply run the following, which will install all dependencies and the latest NVIDIA driver for your GPU (if it's supported by NVIDIA's latest drivers).
```
sudo apt-get install python3 mesa-utils nvidia-prime nvidia-settings bbswitch-dkms gir1.2-appindicator3
sudo apt-get install $(sudo ubuntu-drivers devices | grep -o nvidia-[[:digit:]]*)
```

Troubleshooting
===============

### `appindicator` module missing
Install the `gir1.2-appindicator3` package.

### Couldn't find RGB GLX visual or fbconfig
Install the `mesa-utils` package.

### PRIME Indicator only shows a question mark icon
If you're using `UEFI`, try disabling `Secure Boot` as NVIDIA's proprietary driver does NOT work with `Secure Boot` enabled and it might result in neither GPU being recognized.

### The icons look awful!
I've added some icon options! Edit the config file which resides in `$HOME/.config/prime-indicator/prime-indicator.cfg` and change the option `iconset` in the `Appearance` section to one of the following options:
* `theme-default`: uses icons provided by the icon theme you're using. Falls back to the color option if none is provided (default)
* `symbolic`: attempts to color the icons based on the GTK theme the system is using (depends on the theme's configuration, might not work at all)
* `color`: full color icons (blue Intel logo and green NVIDIA logo)
* `custom(<RGB Hex Color Code>)` [Not implemented yet]: allows you to determine the color the icons should have using hexadecimal RGB values in the #`RR``GG``BB` format. You can select the color you want using many different utilities such as this [HTML Color Picker](http://www.w3schools.com/colors/colors_picker.asp). Example: `custom(#bebebe)` colors the icons gray.


Installation
============
```shell
chmod a+x setup.sh
sudo ./setup.sh
```
