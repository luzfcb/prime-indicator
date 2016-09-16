#!/bin/bash
# PRIME Indicator - indicator applet for NVIDIA Optimus laptops
# Copyright (C) 2013 Alfred Neumayer
# Copyright (C) 2016 André Brait
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root." 2>&1
    exit 1
fi

mkdir -p /usr/lib/primeindicator
cp src/primeindicator.py /usr/bin/
chown root:root /usr/bin/primeindicator.py
chmod 755 /usr/bin/primeindicator.py
cp src/gpuswitcher /usr/lib/primeindicator/
cp resource/*.svg /usr/lib/primeindicator/
chmod a+r /usr/lib/primeindicator/*.svg
chown root:root /usr/lib/primeindicator/gpuswitcher
chmod a+x /usr/lib/primeindicator/gpuswitcher
cp src/primeindicator-sudoers /etc/sudoers.d/
chmod 644 /etc/sudoers.d/primeindicator-sudoers
mkdir -p $HOME/.config/primeindicator
cp src/primeindicator.cfg $HOME/.config/primeindicator/
chown -R $SUDO_USER:$SUDO_USER $HOME/.config/primeindicator

echo "Autostart PRIME Indicator?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) 	mkdir -p $HOME/.config/autostart
        		cp src/primeindicator.desktop $HOME/.config/autostart
        		chown $SUDO_USER:$SUDO_USER $HOME/.config/autostart
    			chown $SUDO_USER:$SUDO_USER $HOME/.config/autostart/primeindicator.desktop
    			chmod +x $HOME/.config/autostart/primeindicator.desktop
    			break;;
        No ) 	rm -f $HOME/.config/autostart/primeindicator.desktop
        		break;;
    esac
done

echo -e "\nTo start PRIME Indicator now, use the command\n"
echo -e "\t/usr/bin/primeindicator.py & disown"

echo -e "\nSetup complete."
exit 0
