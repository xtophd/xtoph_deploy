#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It is meant
##    as a template for custom host setup commands.
##    Copy this to your ./files directory, rename it
##    and then reference in the machine profile.
##
##      -i <ip|host fqdn> .. ip address or fqdn
##      -u <username>     .. username
##      -p <password>     .. password
##
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

        --)
            shift
            break;;

    esac
done



##
##    Run a command
##

bmc_cmd=" lclog worknote add -m 'xtoph_deploy: system provisioned'"

RESPONSE=`racadm -u $bmc_username \
                 -p $bmc_password \
                 -r $bmc_ip       \
                    $bmc_cmd`



##
##    Check the output
##

rc=$?

if [[ ${rc} == 0 ]] ; then
    echo "SUCCESS: boot-once enabled"
else
    echo "FATAL: set boot-once result code ${rc}"
    echo "$RESPONSE"
    exit $rc
fi


