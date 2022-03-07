#!/usr/bin/python3
#
# redfish-dell-bootonce-status.py
#
#   Usage:
#    
#      python3 redfish-dell-bootonce-status.py -u $BMC_USER -p $BMC_PASS -i $BMC_IP
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u $BMC_USER:$BMC_PASS 'https://$BMC_IP/redfish/v1/Systems/System.Embedded.1/BootOptions?$expand=*($levels=1)' | jq
#
#      Show the current boot settings (includes override target)
#
#          curl  --insecure -s -u $BMC_USER:$BMC_PASS 'https://$BMC_IP/redfish/v1/Systems/System.Embedded.1/' | jq '.Boot'
#
#
#
#

import argparse
import json
import requests
import sys
import warnings
import re

##
##    Disable warning messages
##

warnings.filterwarnings("ignore")

##
##    Load commandline arguments
##

parser = argparse.ArgumentParser(description="redfish utility for dell: report boot-once status")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')


args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_mode     = data['Boot']['BootSourceOverrideMode']
override_target   = data['Boot']['BootSourceOverrideTarget']
override_enabled  = data['Boot']['BootSourceOverrideEnabled']

print("Current Override Mode: %s" % override_mode)
print("Current Override Target: %s" % override_target)
print("Current Override Enabled: %s" % override_enabled)

print("")

##
##   Get list of bootable devices
##

if override_mode == "UEFI":

    url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/BootOptions?$expand=*($levels=1)' % bmc_ip

    response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

    if response.status_code != 200:
        print("FATAL: iDRAC version does not support feature")
        sys.exit()
    else:
        pass

    data = response.json()

    if data["Members"] == []:
        print("FATAL: no boot devices detected")
        sys.exit()

    print("Looking for UEFI PXE capable devices:")

    pxe_id      = ""
    pxe_name    = ""
    pxe_display = ""
    pxe_uefi    = ""

    for i in data["Members"]:

        dev_name    = ""
        dev_display = ""
        dev_id      = ""
        dev_uefi    = ""

        for j in i.items():
   
            if (j[0] == "Name")           : dev_name    = j[1]
            if (j[0] == "DisplayName")    : dev_display = j[1]
            if (j[0] == "UefiDevicePath") : dev_uefi    = j[1]
            if (j[0] == "Id")             : dev_id      = j[1]


        if ("PXE" in dev_display): 
            pxe_name    = dev_name
            pxe_id      = dev_id
            pxe_display = dev_display
            pxe_uefi    = dev_uefi

            print ( "* %s | %s | %s" % (pxe_id, pxe_display, pxe_uefi))

        else:

            print ( "  %s | %s | %s" % (dev_id, dev_display, dev_uefi))

    print("")



##
##    Ouput status of boot-once override device
## 

if ( override_target == "None" ):
    result = "unset"
else:
    result = "set"



##
##    Output varies if chomp is true
##

if args["chomp"]:
  print("%s" % result, end="")
else:
  print("%s" % result)

