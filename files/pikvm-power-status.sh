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
##    curl --insecure -s -u "$bmc_uid:$bmc_pw" https://$bmc_ip/api/atx | jq -r '.result.power'
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

RESPONSE=$( curl --insecure -s -u $bmc_username:$bmc_password https://$bmc_ip/api/atx | jq -r '.result.power' | tr [:upper:] [:lower:] )

##
##    Chomp the output to purge CR/LF
##

RESPONSE=${RESPONSE//[$'\n\r']}

##
##    Output the results to stdout
##

if [[ "${RESPONSE}" == "off" ]]; then

    ( [[ "${chomp_output}" == "yes" ]] && echo -n "off" ) || echo "off" 

    exit 0

elif [[ "${RESPONSE}" == "on" ]]; then

    ( [[ "${chomp_output}" == "yes" ]] && echo -n "on" ) || echo "on" 

    exit 0
fi



##
##    Something went wrong, exit with error code
##

echo "FATAL: get power status returned ${rc}"
echo "$REPONSE"
exit 1

