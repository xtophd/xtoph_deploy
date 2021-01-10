#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It combines
##    all steps to create a libvirt network for
##    for use with VMs running in kvm.
##
##    The intent is to provide one command for
##    an ansible shell-task which can be throttled.
##    Thus all the steps from detection to creation,
##    need to be provided in one atomic command.
##



NETWORK_NAME="$1"



##
##    Test for libvirt network
##



if virsh net-info "${NETWORK_NAME}"; then
    echo "yes"
else
    echo "no"
fi




##
##    Exit with RC = 0
##



exit 0
