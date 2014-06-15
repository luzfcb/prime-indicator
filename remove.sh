#!/bin/bash
function removePrime    {
    #Kill running prime-indicator
    ps aux | grep /usr/bin/prime-indicator | grep -v grep | awk '{print $2}' | xargs kill
    rm /usr/bin/prime-indicator
    rm -r /usr/lib/primeindicator/
    rm /etc/sudoers.d/prime-indicator-sudoers

}
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run using sudo" 2>&1
    exit 1
else
    read -n1 -p "Remove PRIME Indicator? (y/N) "
    echo
    if [[ $REPLY = [yY] ]]; then
       removePrime
    fi
fi
