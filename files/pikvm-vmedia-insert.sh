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
##    curl --insecure -s -X POST -k -u "$bmc_id:$bmc_pw" https://$bmc_ip/api/msd/write_remote?url=$bmc_isourl
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
        '-n' ) bmc_nfs="$2"      ; shift 2 ;;

        '--chomp' ) chomp_output="yes" ; shift ;;

        --)
            shift
            break;;

    esac
done



##
##    Use curl to insert/load the media 
##

echo "STATUS: starting vmedia insert"

RESPONSE=$( curl --insecure -s -X POST -u "$bmc_username:$bmc_password" "https://$bmc_ip/api/msd/write_remote?url=$bmc_media" )

RESULT=$( echo "${RESPONSE}" | tail -1 | jq -r '.ok' | tr [:upper:] [:lower:] )

if [[ "${RESULT}" == "true" ]]; then

    echo "STATUS: vmedia inserted"

elif [[ "${RESULT}" == "false" ]]; then

    echo "FAIL: vmedia insert returned ${RESULT}"
    exit 1;

else

    echo "FAIL: unexpected vmedia insert error"
    echo "$RESPONSE"
    exit 1;

fi


##
##    Use curl to configure the image as cdrom
##

IMAGE_NAME=$( basename ${bmc_media} )

RESPONSE=$( curl --insecure -s -X POST -u "$bmc_username:$bmc_password" "https://$bmc_ip/api/msd/set_params?image=${IMAGE_NAME}&cdrom=1" )

RESULT=$( echo "${RESPONSE}" | jq -r '.ok' | tr [:upper:] [:lower:] )

if [[ "${RESULT}" == "true" ]]; then

    echo "STATUS: vmedia configured"

elif [[ "${RESULT}" == "false" ]]; then

    echo "FAIL: vmedia configure returned ${RESULT}"
    exit 1;

else

    echo "FAIL: unexpected media configure error"
    echo "$RESPONSE"
    exit 1;

fi



##
##    Final Step: Use curl to connect the media to host
##

RESPONSE=$( curl --insecure -s -v -X POST -u "$bmc_username:$bmc_password" "https://$bmc_ip/api/msd/set_connected?connected=1" )

RESULT=$( echo "${RESPONSE}" | jq -r '.ok' | tr [:upper:] [:lower:] )

if [[ "${RESULT}" == "true" ]]; then

    echo "STATUS: vmedia connect returned ${RESULT}"

elif [[ "${RESULT}" == "false" ]]; then

    echo "FAIL: vmedia connect returned ${RESULT}"
    exit 1;

else

    echo "FAIL: unexpected vmedia connect error"
    echo "$RESPONSE"
    exit 1;

fi



##
##    Chomp the output to purge CR/LF
##

RESULT=${RESULT//[$'\n\r']}



##
##    Output the results to stdout
##

if [[ "${RESULT}" == "true" ]]; then

    echo "SUCCESS: result ${RESULT} returned"
    exit 0

elif [[ "${RESULT}" == "false" ]]; then

    echo "FAIL: result ${RESULT} returned"
    echo "${RESPONSE}"
    exit 1
fi



##
##    Something went wrong, exit with error code
##

echo "FATAL: insert vmedia failed"
echo "${REPONSE}"
exit 1

