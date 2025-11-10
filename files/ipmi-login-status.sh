#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It gets
##    power state of a host using IPMI
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      --chomp           .. strip linefeed from output
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

        '--chomp' ) chomp_output="yes" ; shift ;;

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

bmc_cmd="mc info"

RESPONSE=`ipmitool -I lanplus \
                   -U $bmc_username \
                   -P $bmc_password \
                   -H $bmc_ip       \
                      $bmc_cmd  | sed -e 's/^.* is \(.*\)$/\1/' | tr [:upper:] [:lower:]`

##
##    Simple pass or fail based on $(rc)
##

if [[ $? == 0 ]] ; then
    echo "SUCCESS: good credentials"
    ( [[ "${chomp_output}" == "yes" ]] && echo -n "true" ) || echo "true"
else
    echo "FATAL: check credentials"
    ( [[ "${chomp_output}" == "yes" ]] && echo -n "false" ) || echo "false"
    exit 1
fi

