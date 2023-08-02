#!/usr/bin/python3
#
# redfish-hp-setpower-on.py
#
#   The curl equivalent:
#
#      curl --insecure -s -u $BMC_USER:$BMC_PASS -X POST -H "Content-Type: application/json" -d '{"ResetType": "On"}' https://$BMC_IP/redfish/v1/Systems/1/Actions/ComputerSystem.Reset
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

parser = argparse.ArgumentParser(description="redfish utility for hp: set power state 'on'")

parser.add_argument('-i', help='ilo ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Set power state
## 

url     = 'https://%s/redfish/v1/Systems/1/Actions/ComputerSystem.Reset/' % bmc_ip
payload = {'ResetType': 'On'}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code == 200:
    print("SUCCESS: result code %s returned" % result_code)
else:
    print("FAIL: result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)

