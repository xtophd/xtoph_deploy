#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It combines
##    all steps to create a network bridge suitable 
##    for use with 'mknet-libvirt.sh' which comes
##    next.
##
##    The intent is to provide one command for
##    an ansible shell-task which can be throttled.
##    Thus all the steps from detection to creation,
##    need to be provided in one atomic command.
##



BRIDGE_NAME="$1"
BRIDGE_INTERFACE_NAME="$2"
BRIDGE_IP4="$3"
BRIDGE_GW4="$4"
BRIDGE_PREFIX="$5"
BRIDGE_DNS="$6"



##
##    Test for bridge
##



if ! nmcli dev show "${BRIDGE_NAME}" ; then
   

 
    ##
    ##    Create the bridge
    ##
    
    
    
    nmcli con add type bridge \
          con-name "{{ kvm_cfg.network.bridge }}" \
          ifname   "{{ kvm_cfg.network.bridge }}" \
          ip4      "{{ kvm_cfg.network.ipv4.addr }}" \
          gw4      "{{ kvm_cfg.network.ipv4.gw }}" \
          ipv4.dns "{{ g_pubDNS }}" \
          autoconnect yes bridge.stp no ipv6.method ignore
    
    
    
    ##
    ##    Add device to bridge 
    ##
    
    
    
    nmcli con add type ethernet \
          con-name {{ kvm_cfg.network.dev }} \
          ifname {{ kvm_cfg.network.dev }} \
          master {{ kvm_cfg.network.bridge }}
    
    nmcli con modify {{ kvm_cfg.network.bridge }} connection.autoconnect-slaves yes
    
    
    
    ##
    ##    Bring up the bridge
    ##
    
    
    
    ifdown "{{ kvm_cfg.network.dev }}"
    ifdown "{{ kvm_cfg.network.bridge }}"
    ifup   "{{ kvm_cfg.network.bridge }}"

fi
