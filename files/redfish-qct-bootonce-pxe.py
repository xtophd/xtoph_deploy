#!/usr/bin/python3
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/system/BootOptions?$expand=*($levels=1)" | jq
#
#      Show the current boot settings (includes override target)
#
#          curl --insecure -s -u "${bmc_uid}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/system" | jq '.Boot.BootSourceOverrideEnabled'
#          curl --insecure -s -u "${bmc_uid}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/system" | jq '.Boot.BootSourceOverrideTarget'
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

parser = argparse.ArgumentParser(description="redfish utility for qct: set bootonce operation to PXE")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/system' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_mode    = data['Boot']['BootSourceOverrideMode']
override_target  = data['Boot']['BootSourceOverrideTarget']
override_enabled = data['Boot']['BootSourceOverrideEnabled']
override_uefidev = data['Boot']['UefiTargetBootSourceOverride']

print("Current Override Mode: %s" % override_mode, file=sys.stderr)
print("Current Override Target: %s" % override_target, file=sys.stderr)
print("Current Override Enabled: %s" % override_enabled, file=sys.stderr)
print("Current Override UEFI Device: %s" % override_uefidev, file=sys.stderr)

##
##
##
##

if override_mode == "UEFI":

    url      = 'https://%s/redfish/v1/Systems/system/BootOptions' % bmc_ip
    response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

    if response.status_code != 200:
        print("FATAL: OpenBMC version does not support feature")
        sys.exit()
    else:
        pass

    data = response.json()

    if data["Members"] == []:
        print("FATAL: no boot devices detected")
        sys.exit()

    print("Looking for first IPv4 PXE capable device:", file=sys.stderr)

    done = False

    pxe_id      = ""
    pxe_name    = ""
    pxe_display = ""
    pxe_uefi    = ""

    for i in data["Members"]:

        member_url      = 'https://%s%s' % ( bmc_ip, i["@odata.id"] )
        member_response = requests.get(member_url,auth=(bmc_username, bmc_password), verify=False)
        member_data     = member_response.json()

        dev_name    = member_data['Name']
        dev_alias   = member_data['Alias']
        dev_display = member_data['DisplayName']
        dev_uefi    = member_data['UefiDevicePath']
        dev_id      = member_data['Id']

        if (("PXE" in dev_display) and ("IPv4" in dev_display) and not done):
            pxe_name    = dev_name
            pxe_alias   = dev_alias
            pxe_id      = dev_id
            pxe_display = dev_display
            pxe_uefi    = dev_uefi

            print ( "* %s" % pxe_id, file=sys.stderr)

            done = True

        else:

            print ( "  %s" % dev_id, file=sys.stderr)

        print ( "    %s" % (dev_alias), file=sys.stderr)
        print ( "    %s" % (dev_display), file=sys.stderr)
        print ( "    %s" % (dev_uefi), file=sys.stderr)
    print("")


##
##    BootOnce: 'Enabled' and set boot device to 'PXE'
##

if override_mode == "UEFI":

    
    url      = 'https://%s/redfish/v1/Systems/system' % bmc_ip
    headers  = {'content-type': 'application/json'}
    #payload  = {'Boot':{'BootSourceOverrideEnabled': 'Once', 'BootSourceOverrideMode': 'UEFI', 'BootSourceOverrideTarget': 'Pxe', 'UefiTargetBootSourceOverride': pxe_uefi }}

    ## Trying this next
    payload  = {'Boot':{'BootSourceOverrideTarget': 'Pxe', 'UefiTargetBootSourceOverride': pxe_uefi }}
    
    print ( "Attempting to set:", file=sys.stderr)
    print ( "  " + json.dumps(payload), file=sys.stderr)

    response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)
    
    result_code = response.status_code
    

    if result_code == 204:
        print("SUCCESS: result code %s returned" % result_code)
    else:
        print("FAIL: result code %s returned" % result_code)
        print(response)
        sys.exit(1)
    
else:
    print("FAIL: unexpected condition (Not UEFI)")
    sys.exit(1)
