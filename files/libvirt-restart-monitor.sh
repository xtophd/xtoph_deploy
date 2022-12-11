#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It monitors
##    the state of a kvm virtual machine (domain)
##    and restarts it if found in a 'shut off' state
##
##      -d <domain>    .. virtual machine to monitor
##      -e <filename>  .. eject/remove iso image on restart
##      -t <timeout>   .. terminate after <timeout> seconds
##      -c <count>     .. terminate after <count> restarts
##      -f <filename>  .. terminate if <filename> exists
##
##    Prints string 'true' or 'false' to STDIO
##
##


##
##    Remember our start time 
##    and set some defaults
##

lrm_starttime=`date '+%s'`
lrm_currenttime=`date '+%s'`
lrm_count="1"
lrm_ejectimage=""
lrm_restarts="0"
lrm_runtime=""
lrm_domain=""
lrm_timeout="0"
lrm_filename=""


##
##    Parse the commandline options
##

options=$( getopt -o "d:t:c:f:e:" -- "$@")

eval set -- "$options"

while true; do
    case $1 in
        '-d' ) lrm_domain="$2"     ; shift 2 ;;
        '-t' ) lrm_timeout="$2"    ; shift 2 ;;
        '-c' ) lrm_count="$2"      ; shift 2 ;;
        '-f' ) lrm_filename="$2"   ; shift 2 ;;
        '-e' ) lrm_ejectimage="$2" ; shift 2 ;;

        --)
            shift
            break;;

    esac
done

##
##    Validations
##

if [[ ${lrm_domain}  == "" ]]; then echo "Missing VM Domain name (-d)"; fi
if [[ ${lrm_timeout} == "" ]]; then echo "Missing timeout value (-t)"; fi
if [[ ${lrm_count}   == "" ]]; then echo "Missing restart count (-c)"; fi

##
##    Simple infinite loop, exit on conditions
## 


while true; do

  lrm_currenttime=`date +%s`
 
  let "lrm_runtime = ${lrm_currenttime} - ${lrm_starttime}"

  if [[ ${lrm_runtime} -ge ${lrm_timeout} ]]; then
      echo "(${lrm_domain}) Time out reached... exiting"
      exit 0
  fi

  if [[ ${lrm_restarts} -ge ${lrm_count} ]]; then
      echo "(${lrm_domain}) Restart count limit reached... exiting"
      exit 0
  fi
  
  if [[ ${lrm_filename} != "" && -e ${lrm_filename} ]]; then
      echo "(${lrm_domain}) Filename detected... exiting"
      exit 0
  fi

  current_state=`virsh domstate ${lrm_domain}`

  if [[ ${current_state} == "shut off" ]]; then

      if [[ ${lrm_ejectimage} != "" && -e ${lrm_ejectimage} ]]; then

          ## Maybe in the future we should insert a 
          ## virsh eject operation, but for now just remove
          ## the file.

          rm -f ${lrm_ejectimage}
          echo "(${lrm_domain}) Media ejected/removed"
      fi

      virsh start ${lrm_domain}
      echo "(${lrm_domain}) Restarted"
      ((++lrm_restarts))
  fi

  sleep 5

done

