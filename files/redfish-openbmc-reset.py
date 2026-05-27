#!/usr/bin/python3
#
# redfish-keytus-reset.py
#
#   Usage:
#
#      python3 redfish-openbmc-reset.py -u "${bmc_id}" -p "${bmc_pw}" -i $"{bmc_ip}"
#
#   The curl equivalent:
#
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Managers/1/Actions/Manager.Reset" | jq
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

parser = argparse.ArgumentParser(description="OpenBMC redfish utility: reset BMC")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

##
## Request reset of the BMC
##

url      = 'https://%s/redfish/v1/Managers/1/Actions/Manager.Reset' % bmc_ip

headers  = {'content-type': 'application/json'}
payload  = {'ResetType': 'ForceRestart','Oem': {'Public': {'CurrentPassword': bmc_password, 'EncryptFlag': 'false'}}}

print(json.dumps(payload))

response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code
    
if result_code == 200:
    print("SUCCESS: OpenBMC reset returned code %s" % result_code)
    sys.exit(0)
else:
    print("FAIL: OpenBMC reset returned code %s" % result_code)
    print(response)
    sys.exit(1)

