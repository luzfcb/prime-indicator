#!/bin/bash
# This file is part of PRIME Indicator - indicator applet for NVIDIA Optimus laptops.
# Copyright (C) 2016 André Brait Carneiro Fabotti
#
# This work is based on the works of Alfred Neumayer and Clement Lefebvre.
#
# PRIME Indicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PRIME Indicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PRIME Indicator.  If not, see <http://www.gnu.org/licenses/>.

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root." 2>&1
    exit 1
fi

LIB_DIR="/usr/lib/prime-indicator"
SUDOERS_FILE="/etc/sudoers.d/99-prime-indicator-sudoers"
AUTOSTART_FILE="/etc/xdg/autostart/prime-indicator.desktop"

rm -f ${SUDOERS_FILE}
rm -f ${AUTOSTART_FILE}
rm -rf ${LIB_DIR}
rm -rf ${HOME}/.config/prime-indicator

echo "Uninstall complete."
exit 0
