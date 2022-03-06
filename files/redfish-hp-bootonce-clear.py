#!/usr/bin/python3
#
# redfish-hp-bootonce-clear.py
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u $uname:$password 'https://$bmc_ip/redfish/v1/Systems/System.Embedded.1/BootOptions?$expand=*($levels=1)' | jq
#
#      Show the current boot settings (includes override target)
#
#          curl --insecure -s -u $BMC_USER:$BMC_PASS https://$BMC_IP/redfish/v1/Systems/1/  | jq '.Boot.BootSourceOverrideEnabled'
#          curl --insecure -s -u $BMC_USER:$BMC_PASS https://$BMC_IP/redfish/v1/Systems/1/  | jq '.Boot.BootSourceOverrideTarget'
#
#    NOTE: ILO 5 implements BootSourceOverrideMode which reports hardware configured in UEFI or BIOS mode.  My lab is currently 
#          limited with ILO4 (gen 8) and for now this shim is BIOS mode only.
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

parser = argparse.ArgumentParser(description="redfish utility for hp: set boot-once to PXE")

parser.add_argument('-i', help='ilo ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/1/' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_enabled  = data['Boot']['BootSourceOverrideEnabled']
override_target  = data['Boot']['BootSourceOverrideTarget']

try:
  override_mode    = data['Boot']['BootSourceOverrideMode']
except:
  override_mode    = ''

print("Current Override Enabled: %s" % override_enabled)
print("Current Override Target: %s" % override_target)
print("Current Override Mode: %s" % override_mode)

print("")

##
##   Get list of bootable devices
##

if override_mode == "UEFI":


    ##
    ## THE FOLLOWING HAS NOT BEEN VETTED ON ILO5 (THIS IS DELL BASE LOGIC)
    ##

    url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/BootOptions?$expand=*($levels=1)' % bmc_ip

    response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

    if response.status_code != 200:
        print("FATAL: iLO version does not support feature")
        sys.exit()
    else:
        pass

    data = response.json()

    if data["Members"] == []:
        print("FATAL: no boot devices detected")
        sys.exit()

    print("Looking for PXE capable devices:")

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
##    Clear BootOnce Override
##


url      = 'https://%s/redfish/v1/Systems/1/' % bmc_ip
headers  = {'content-type': 'application/json'}

if override_mode == "UEFI":
    payload  = {'Boot':{'BootSourceOverrideTarget':'None', 'UefiTargetBootSourceOverride': 'None', 'BootSourceOverrideEnabled':'Once'}}
else:
    payload  = {'Boot':{'BootSourceOverrideTarget':'None'}}

response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code != 200:
    print("FATAL: clear boot-once result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)
else:
    print("SUCCESS: boot-once cleared")
    pass

