#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It checks
##    is a firewalld zone exists.
##
##    Prints string 'yes' or 'no' to STDIO
##   
##    Always returns RC = 0



ZONE_NAME="$1"



##
##    Test for libvirt network
##



if firewall-cmd --info-zone="${ZONE_NAME}" >/dev/null ; then
    echo -n "yes"
else
    echo -n "no"
fi



##
##    Exit with RC = 0
##



exit 0
