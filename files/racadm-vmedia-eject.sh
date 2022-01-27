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

options=$( getopt -o "u:p:i:m:" -l "chomp" -- "$@")

eval set -- "$options"

while true; do
    case $1 in
        '-u' ) bmc_username="$2" ; shift 2 ;;
        '-p' ) bmc_password="$2" ; shift 2 ;;
        '-i' ) bmc_ip="$2"       ; shift 2 ;;

        --)
            shift
            break;;

    esac
done



##
##    Disconnect the virtual media
##

bmc_cmd="vmdisconnect"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`

##
##    Status message to stdout
##

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: virtual media disconnected"
else

    if echo "$RESPONSE" |  grep -iq "No Virtual Media" ; then
        echo "WARNING: virtual media was not connected"
    else
        echo "FATAL: virtual media disconnect failed with result code ${rc}"
        exit $rc
    fi
fi



##
##    Disconnect the remote media
##

bmc_cmd="remoteimage -d"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`



##
##    Status message to stdout
##

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: remote image disconnected"
    exit 0
else
    echo "FATAL: remote image disconnect failed with result code ${rc}"
    exit $rc
fi

