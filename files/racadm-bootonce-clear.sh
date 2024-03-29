#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It gets
##    power state of a host using DELL racadm
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -x                .. chomp ouptut (no CR/LF)
##
##    Prints string 'on' or 'off' to STDIO
##
##



##
##    Parse the commandline options
##

options=$( getopt -o "u:p:i:m:" -l "chomp" -- "$@")

eval set -- "$options"

while true; do
    case $1 in
        '-u' ) bmc_username="$2" ; shift 2 ;;
        '-p' ) bmc_password="$2" ; shift 2 ;;
        '-i' ) bmc_ip="$2"       ; shift 2 ;;

        --)
            shift
            break;;

    esac
done



##
##    Clear the serverboot.bootonce flag
##
##      NOTE: ServerBoot.BootOnce and VirtualMedia.BootOnce are
##            two different things
##

bmc_cmd="set iDRAC.ServerBoot.BootOnce Disabled"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`

##    Status message to stdout

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: cleared serverboot.bootonce flag"
else
    echo "FAIL: clear bootonce returned {$rc}"
    echo "$RESPONSE"
    exit $rc
fi



##
##    Clear the virtualmedia.bootonce flag
##
##      NOTE: ServerBoot.BootOnce and VirtualMedia.BootOnce are
##            two different things
##

bmc_cmd="set iDRAC.VirtualMedia.BootOnce Disabled"


RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`

##    Status message to stdout

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: cleared virtualmedia.bootonce flag"
else
    echo "FATAL: clear virtualmedia.bootonce returned {$rc}"
    echo "$RESPONSE"
    exit $rc
fi

