#!/usr/bin/python
#
# redfish-dell-pxe-bootonce.py
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u $uname:$password 'https://$bmc_ip/redfish/v1/Systems/System.Embedded.1/BootOptions?$expand=*($levels=1)' | jq
#
#      Show the current boot settings (includes override target)
#
#          curl  --insecure -s -u $uname:$password 'https://192.168.110.111/redfish/v1/Systems/System.Embedded.1/' | jq '.Boot'
#
#
#
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

parser = argparse.ArgumentParser(description="redfish utility for dell: eject virtual media")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Test login credentials
## 

response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1' % bmc_ip, auth=(bmc_username, bmc_password), verify=False)

if response.status_code == 401:
    print("WARNING: check credentials")
    sys.exit(1)
else:
    pass



## 
##  Set PXE Device BootOnce
## 

url      = 'https://%s/redfish/v1/Systems/System.Embedded.1' % bmc_ip
payload  = {'Boot':{'BootSourceOverrideTarget':'Pxe'}}
headers  = {'content-type': 'application/json'}

response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code != 200:
    print("FAIL: result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)
else:
    print("SUCCESS: bootonce set to \"Pxe\"")
    pass

