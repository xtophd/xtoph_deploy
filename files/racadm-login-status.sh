#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It gets
##    the system version info as means to test
##    the login credentials
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -x                .. chomp ouptut (no CR/LF)
##
##    Prints string 'true' or 'false' to STDIO
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
##    Use racadm to fetch or set state
##
##    NOTE: the 'sed' command only returns the portion after ':'
##

bmc_cmd="getversion"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`



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

