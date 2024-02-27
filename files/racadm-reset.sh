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

options=$( getopt -o "u:p:i:" -l "chomp" -- "$@")

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
##    Reset iDRAC
##

bmc_cmd="racreset"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`



##
##    Status message to stdout
##

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: drac reset"
else
    echo "FAIL: attempt to reset drac resulted in error ${rc}"
    echo "$RESPONSE"
    exit $rc
fi

