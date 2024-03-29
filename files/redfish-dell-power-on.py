#!/usr/bin/python3
#
# redfish-dell-setpower-on.py
#
#   The curl equivalent:
#
#      curl --insecure                          \
#           -s                                  \
#           -u $bmc_uid:$bmc_pw                 \
#           -X POST                             \
#           -H "Content-Type: application/json" \
#           -d '{"ResetType": "On"}'            \
#           https://$bmc_ip/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset
#

import argparse
import json
import requests
import sys
import warnings



##
##    Disable warning messages
##

warnings.filterwarnings("ignore")



##
##    Load commandline arguments
##

parser = argparse.ArgumentParser(description="redfish utility for dell: set power state 'on'")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Set power state
## 


url     = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset' % bmc_ip
payload = {'ResetType': 'On'}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code == 204:
    print("SUCCESS: result code %s returned" % result_code)
else:
    print("FAIL: result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)

