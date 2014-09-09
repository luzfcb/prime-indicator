#!/bin/bash
function removePrimeIndicator    {
    #Kill running prime-indicator
    ps aux | grep /usr/bin/prime-indicator | grep -v grep | awk '{print $2}' | xargs kill
    rm -f /usr/bin/prime-indicator
    rm -rf /usr/lib/primeindicator/
    rm -f /etc/sudoers.d/prime-indicator-sudoers
    rm -f $HOME/.config/autostart/prime-indicator.desktop

}
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run using sudo" 2>&1
    exit 1
else
    read -n1 -p "Remove PRIME Indicator? (y/N) "
    echo
    if [[ $REPLY = [yY] ]]; then
       removePrimeIndicator
    fi
fi
