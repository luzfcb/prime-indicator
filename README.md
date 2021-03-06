PRIME Indicator
==============
Indicator applet for Ubuntu laptop users with NVIDIA/Intel switchable graphics
This indicator has only been tested on Ubuntu 14.04 but should be working just as well
on 12.04 with the newest hardware enablement stack.

This indicator applet allows owners of laptops with NVIDIA/Intel hybrid graphics to
quickly switch between the graphics cards and log out from within the Unity top panel in seconds.


Prerequisites
==============
You have to have a few packages installed on your Ubuntu box to take advantage of this indicator.
Make sure you have the NVIDIA driver >=331.20 installed and the additional package called "nvidia-prime".
In case the indicator doesn't start because it is missing the python module "appindicator",
again, make sure to install missing packages. If the indicator contains a glxinfo error message, you are missing the mesa-utils package. To install all needed dependencies:

sudo apt-get install nvidia-prime nvidia-331 nvidia-settings python-appindicator mesa-utils


How to install
==============

chmod a+x setup.sh

sudo ./setup.sh

How to remove
==============

chmod a+x remove.sh

sudo ./remove.sh
