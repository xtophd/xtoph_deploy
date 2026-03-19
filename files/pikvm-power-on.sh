#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It sets the
##    power state of a host to 'on' using pi-kvm API
##
##    https://docs.pikvm.org/api       
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -x                .. chomp ouptut (no CR/LF)
##
##
##    curl --insecure -s -u "$bmc_uid:$bmc_pw" https://$bmc_ip/api/atx/power?action=on
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
##    Use curl to fetch or set state
##

RESPONSE=$( curl --insecure -s -k -X POST -u $bmc_username:$bmc_password https://$bmc_ip/api/atx/click?button=power | jq '.ok' | tr [:upper:] [:lower:])

rc=$?

##
##    Chomp the output to purge CR/LF
##

RESPONSE=${RESPONSE//[$'\n\r']}

##
##    Output the results to stdout
##

if [[ "${RESPONSE}" == "true" ]]; then

    echo "SUCCESS: result code ${rc} returned"
    exit $rc

    exit 0

elif [[ "${RESPONSE}" != "true" ]]; then

    echo "FAIL: result code ${rc} returned"
    exit $rc

    exit 0
fi
