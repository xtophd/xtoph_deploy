#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  Sets
##    power state of a host using IPMI
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##

##
##    Parse the commandline options
##

options=$( getopt -o "u:p:i:" -- "$@")

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
##    Use ipmi to fetch or set state
##
##    NOTE: the 'sed' command only returns the portion after ':'
##

bmc_cmd="chassis power on"

RESPONSE=`ipmitool -I lanplus \
                   -U $bmc_username \
                   -P $bmc_password \
                   -H $bmc_ip       \
                      $bmc_cmd`



##
##    Status message to stdout
##

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: result code ${rc} returned"
    exit $rc
else
    echo "FAIL: result code ${rc} returned"
    exit $rc
fi

