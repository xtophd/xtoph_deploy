#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It gets
##    power state of a host using DELL racadm
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##      -m <http url>     .. URL to virtual media
##      -n <nfs path>     .. NFS to virtual media
##
##
##    Prints string 'on' or 'off' to STDIO
##
##



##
##    Parse the commandline options
##

options=$( getopt -o "u:p:i:m:n:" -l "chomp" -- "$@")

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
##    Use racadm to fetch or set state
##
##    NOTE: the 'sed' command only returns the portion after ':'
##

if [[ "$bmc_media" != "" ]]; then 
    bmc_cmd="remoteimage -c -l $bmc_media"
elif [[ "$bmc_nfsl" != "" ]]; then
    bmc_cmd="remoteimage -c -l $bmc_nfs"
else
    echo "FAIL: image location not specified"
    exit 1
fi

echo "racadm -u $bmc_username -p $bmc_password -r $bmc_ip $bmc_cmd"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`

##
##    Chomp the output to purge CR/LF
##

RESPONSE=${RESPONSE//[$'\n\r']}



##
##    Status message to stdout
##

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: result code ${rc} returned"
    exit $rc
else
    echo "FAIL: result code ${rc} returned"
    exit $rc
fi

