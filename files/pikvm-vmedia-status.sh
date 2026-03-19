#!/bin/bash 

##
##    OUTPUT: inserted | ejected
##
##    USAGE:
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -m <image url>    .. url
##      -x                .. chomp ouptut (no CR/LF)
##
##    SUMMARY:
##      reports status of media
##
##          ejected  == not connected && not stored on msd
##          inserted == saved on msd  && connected
##
##    CURL SAMPLE:
##
##      curl --insecure -s -u "$bmc_id:$bmc_pw" https://$bmc_ip/api/msd | jq -r '.result.drive.connected'
##
##    DOCS: https://docs.pikvm.org/api       
##

##    Initialize vars

bmc_username=""
bmc_password=""
bmc_ip=""
bmc_image=""
chomp_output="no"

##    Parse the commandline options

options=$( getopt -o "u:p:i:m:" -l "chomp" -- "$@")

eval set -- "$options"

while true; do
    case $1 in
        '-u' ) bmc_username="$2" ; shift 2 ;;
        '-p' ) bmc_password="$2" ; shift 2 ;;
        '-i' ) bmc_ip="$2"       ; shift 2 ;;
        '-m' ) bmc_image="$2"    ; shift 2 ;;

        '--chomp' ) chomp_output="yes" ; shift ;;

        --)
            shift
            break;;

    esac
done



##
##    Is media in a connected state
##

RESPONSE=$( curl --insecure -s -u $bmc_username:$bmc_password https://$bmc_ip/api/msd )
RESULT=$( echo "${RESPONSE}" | jq -r '.result.drive.connected' | tr [:upper:] [:lower:] )

RESULT=${RESULT//[$'\n\r']}

if [[ "${RESULT}" == "true" ]]; then

    ( [[ "${chomp_output}" == "yes" ]] && echo -n "inserted" ) || echo "inserted"

    exit 0
fi



##
##    Is media present on the msd
##

if [[ $bmc_image != "" ]]; then

    IMAGE_NAME=$( basename "${bmc_image}" )

    RESPONSE=$( curl --insecure -s -u "${bmc_username}:${bmc_password}" "https://$bmc_ip/api/msd" )
    RESULT=$( echo "${RESPONSE}" | jq -r ".result.storage.images.\"$IMAGE_NAME\"" )

    RESULT=${RESULT//[$'\n\r']}

    if [[ "${RESULT}" != "null" ]]; then

        ( [[ "${chomp_output}" == "yes" ]] && echo -n "inserted" ) || echo "inserted"

        exit 0
    fi
fi


##
##    media is both disconnected and removed from the msd    
##

( [[ "${chomp_output}" == "yes" ]] && echo -n "ejected" ) || echo "ejected"

