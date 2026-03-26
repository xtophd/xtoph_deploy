#!/usr/bin/python3
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/1/BootOptions?$expand=*($levels=1)" | jq
#
#      Show the current boot settings (includes override target)
#
#          curl --insecure -s -u "${bmc_uid}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/1" | jq '.Boot.BootSourceOverrideEnabled'
#          curl --insecure -s -u "${bmc_uid}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/1" | jq '.Boot.BootSourceOverrideTarget'
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

url      = 'https://%s/redfish/v1/Systems/1' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_etag    = response.headers.get('ETag')
override_mode    = data['Boot']['BootSourceOverrideMode']
override_target  = data['Boot']['BootSourceOverrideTarget']
override_enabled = data['Boot']['BootSourceOverrideEnabled']

#print("Current Override Mode: %s" % override_mode, file=sys.stderr)
#print("Current Override Target: %s" % override_target, file=sys.stderr)
#print("Current Override Enabled: %s" % override_enabled, file=sys.stderr)

##
##    BootOnce: 'Enabled' and set boot device to 'PXE'
##

if override_mode == "UEFI":
    
    url      = 'https://%s/redfish/v1/Systems/1' % bmc_ip
    headers  = {'content-type': 'application/json', 'If-Match': override_etag}
    payload  = {'Boot':{'BootSourceOverrideEnabled': 'Once','BootSourceOverrideTarget': 'Pxe'}}
    
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
