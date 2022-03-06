#!/usr/bin/python3
#
# redfish-hp-virtualmedia-eject.py
#
#   The curl equivalent:
#
#      curl --insecure                          \
#           -s                                  \
#           -u <username>:<password>            \
#           -X POST                             \
#           -H "Content-Type: application/json" \
#           -d '{}'                             \
#           https://<bmc-ip>/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia 

#curl  -L 
#      -w  "%{http_code} %{url_effective}\\n"  
#      -ku $user:$password 
#      -H "Content-Type: application/json" 
#      -H "Accept: application/json" 
#      -d '{}'  
#      -X POST 
#      https://$bmc/redfish/v1/Managers/1/VirtualMedia/2/Actions/VirtualMedia.EjectMedia

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

parser = argparse.ArgumentParser(description="redfish utility for hp: eject virtual media")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Eject Media
## 

url      = 'https://%s/redfish/v1/Managers/1/VirtualMedia/2/Actions/Oem/Hp/HpiLOVirtualMedia.EjectVirtualMedia/' %bmc_ip
headers  = {'content-type': 'application/json'}

response = requests.post(url, data='{}', headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code == 200:
    print("SUCCESS: result code %s returned" % result_code)
else:
    print("FAIL: result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)

