#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It inserts
##    vmedia to a host using pi-kvm API
##
##    https://docs.pikvm.org/api       
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -x                .. chomp ouptut (no CR/LF)
##
##    curl --insecure -s -X POST -k -u "$bmc_id:$bmc_pw" https://$bmc_ip/api/msd/reset | jq -r '.ok'
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

        '--chomp' ) chomp_output="yes" ; shift ;;

        --)
            shift
            break;;

    esac
done



##
##    Use curl to fetch or set state
##

RESPONSE=$( curl --insecure -s -u "$bmc_username:$bmc_password" "https://$bmc_ip/api/msd" )

RESULT=$( echo "${RESPONSE}" | jq -r '.result.drive.connected' | tr [:upper:] [:lower:] )

##
##    We are going to need the image name for later
##

IMAGE_NAME=$( echo "${RESPONSE}" | jq -r '.result.drive.image.name' )

##
##    Time to disconnect the image
##

if [[ "${RESULT}" == "true" ]]; then

    echo "STATUS: disconnecting" >&2
    RESPONSE=$( curl --insecure -s -X POST -k -u "$bmc_username:$bmc_password" "https://$bmc_ip/api/msd/set_connected?connected=0" )

    ## Remove image from MSD

    echo "STATUS: removing" >&2
    RESPONSE=$( curl --insecure -s -X POST -k -u "$bmc_username:$bmc_password" https://$bmc_ip/api/msd/remove?image=${IMAGE_NAME} )

    RESULT=$( echo "${RESPONSE}" | jq -r '.ok' | tr [:upper:] [:lower:] )

    if [[ "${RESULT}" == "true" ]]; then
        echo "SUCCESS: vmedia ejected"
        exit 0
    fi 

elif [[ "${RESULT}" == "false" ]]; then

    echo "STATUS: already disconnected" >&2
    echo "SUCCESS: vmedia ejected"
    exit 0
fi

##
##    Something went wrong, exit with error code
##

echo "FATAL: vmedia eject failed"
echo "${REPONSE}"
exit 1

