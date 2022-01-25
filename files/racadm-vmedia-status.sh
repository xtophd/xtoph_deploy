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

bmc_cmd="remoteimage -s"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd | grep -i sharename | sed -e 's/\w*\s*//' | wc -w`



##
##    Chomp the output to purge CR/LF
##

RESPONSE=${RESPONSE//[$'\n\r']}



##
##    Output the results to stdout
##

if [[ ${RESPONSE} -eq 0 ]]; then

    ( [[ "${chomp_output}" == "yes" ]] && echo -n "ejected" ) || echo "ejected" 

    exit 0

elif [[ ${RESPONSE} -gt 0 ]]; then

    ( [[ "${chomp_output}" == "yes" ]] && echo -n "inserted" ) || echo "inserted" 

    exit 0
fi



##
##    Something went wrong, exit with error code
##

if [[ ${rc} != 0 ]] ; then
    echo "FAIL: result code ${rc} returned"
    exit $rc
fi

