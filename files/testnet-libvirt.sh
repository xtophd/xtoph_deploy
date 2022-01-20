#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It checks
##    if a libvirt network exists.
##
##    Prints string 'yes' or 'no' to STDIO
##
##    Always returns RC = 0
##



NETWORK_NAME="$1"



##
##    Test for libvirt network
##



if virsh net-info "${NETWORK_NAME}" >/dev/null; then
    echo "yes"
else
    echo "no"
fi



##
##    Exit with RC = 0
##



exit 0
