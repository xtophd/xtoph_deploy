#!/usr/bin/python3
#
# redfish-hp-virtualmedia-bootonce.py
#
#   The curl equivalent:
#



import argparse
import json
import requests
import sys
import warnings
import textwrap



##
##    Disable warning messages
##

warnings.filterwarnings("ignore")



##
##    Load commandline arguments
##

parser = argparse.ArgumentParser(description="redfish utility for hp: set boot-once to virtual media")

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
override_target   = data['Boot']['BootSourceOverrideTarget']

try:
  override_mode    = data['Boot']['BootSourceOverrideMode']
except:
  override_mode    = ''

print("Current Override Enabled: %s" % override_enabled)
print("Current Override Target: %s" % override_target)
print("Current Override Mode: %s" % override_mode)

print("")




## 
##    Set Virtual Media Boot-Once
## 

url      = 'https://%s/redfish/v1/Systems/1/' % bmc_ip
headers  = {'content-type': 'application/json'}

if override_mode == "UEFI":
    print("WHOOPS: I don't do UEFI yet!!!")
    sys.exit(2)

else:

    payload  = {"Boot": {"BootSourceOverrideTarget": "Pxe", "BootSourceOverrideEnabled": "Once"}}

response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code == 200:
    print("SUCCESS: result code %s returned" % result_code)
else:
    print("FAIL: result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)

