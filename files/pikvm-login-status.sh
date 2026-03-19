#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It gets
##    power state of a host using pi-kvm API
##
##    https://docs.pikvm.org/api       
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -x                .. chomp ouptut (no CR/LF)
##
##    Prints string 'on' or 'off' to STDIO
##
##    curl --insecure -s -u "$bmc_uid:$bmc_pw" https://$bmc_ip/api/auth/check | jq -r '.ok'
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

RESPONSE=$( curl --insecure -s -u $bmc_username:$bmc_password https://$bmc_ip/api/auth/check | jq -r '.ok' | tr [:upper:] [:lower:] )

rc=$?

##
##    Chomp the output to purge CR/LF
##

RESPONSE=${RESPONSE//[$'\n\r']}



##
##    Output the results to stdout
##

if [[ "${RESPONSE}" == "true" ]]; then

    echo "SUCCESS: good credentials"
    exit 0

elif [[ "${RESPONSE}" != "true" ]]; then

    echo "FATAL: check credentials"
    exit 1
fi

