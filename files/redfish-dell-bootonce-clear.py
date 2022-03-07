#!/usr/bin/python3
#
# redfish-dell-bootonce-clear.py
#
#   Usage:
#    
#      python3 redfish-dell-bootonce-clear.py -u $BMC_USER -p $BMC_PASS -i $BMC_IP
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

override_mode   = data['Boot']['BootSourceOverrideMode']
override_target = data['Boot']['BootSourceOverrideTarget']

print("Current Override Mode: %s" % override_mode)
print("Current Override Target: %s" % override_target)

print("")


url      = 'https://%s/redfish/v1/Systems/System.Embedded.1' % bmc_ip
headers  = {'content-type': 'application/json'}

if override_mode == "UEFI":
    payload  = {'Boot':{'BootSourceOverrideTarget':'None', 'UefiTargetBootSourceOverride': 'None', 'BootSourceOverrideEnabled':'Once'}}
else:
    payload  = {'Boot':{'BootSourceOverrideTarget':'None', 'BootSourceOverrideEnabled':'Once'}}

response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code != 200:
    print("FATAL: clear boot-once result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)
else:
    print("SUCCESS: boot-once cleared \"Pxe\"")

