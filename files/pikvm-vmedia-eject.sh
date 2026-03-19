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
        '-m' ) bmc_media="$2"    ; shift 2 ;;

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

if [[ "${RESULT}" == "true" ]]; then

    echo "STATUS: disconnecting"
    RESPONSE=$( curl --insecure -s -X POST -k -u "$bmc_username:$bmc_password" "https://$bmc_ip/api/msd/set_connected?connected=0" )

elif [[ "${RESULT}" == "false" ]]; then

    echo "STATUS: already disconnected"
fi



##
##    Delete the image
##

IMAGE_NAME=$( basename "${bmc_media}" )
RESPONSE=$( curl --insecure -s -u "$bmc_username:$bmc_password" https://$bmc_ip/api/msd )
RESULT=$( echo "${RESPONSE}" | jq -r ".result.storage.images.\"$IMAGE_NAME\"" )

if [[ "${RESULT}" != "null" ]]; then
    ## Image exists, proceed to remove

    echo "STATUS: removing"

    RESPONSE=$( curl --insecure -s -X POST -k -u "$bmc_username:$bmc_password" https://$bmc_ip/api/msd/remove?image=${IMAGE_NAME} )

    RESULT=$( echo "${RESPONSE}" | jq -r '.ok' | tr [:upper:] [:lower:] )

    if [[ "${RESULT}" == "true" ]]; then
        echo "SUCCESS: result ${RESULT} returned"
        exit 0
    fi 

else

    echo "STATUS: already removed"
    echo "SUCCESS: result ${RESULT} returned"
    exit 0

fi



##
##    Something went wrong, exit with error code
##

echo "FATAL: eject vmedia failed"
echo "${REPONSE}"
exit 1

