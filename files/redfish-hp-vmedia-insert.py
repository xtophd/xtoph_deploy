#!/usr/bin/python
#
# redfish-hp-virtualmedia-insert.py
#
#   The curl equivalent:
#
#      #D#curl --insecure                          \
#      #E#     -s                                  \
#      #L#     -u <username>:<password>            \
#      #L#     -X POST                             \
#      # #     -H "Content-Type: application/json" \
#      # #     -d "{\"Image\":\"<image_url>"       \
#      # #     https://<bmc-ip>/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia


#      curl -L 
#           -w "%{http_code} %{url_effective}\\n"  
#           -ku $user:$password 
#           -H "Content-Type: application/json" 
#           -H "Accept: application/json" 
#           -d '{"Image": "http://10.49.30.20:8000/sjdmc-sjcontrol3.iso"}'  
#           -X POST 
#           https://$bmc/redfish/v1/Managers/1/VirtualMedia/2/Actions/VirtualMedia.InsertMedia
#



#
# THIS SCRIPT IS UNTESTED/UNCONFIRMED
# THIS SCRIPT IS UNTESTED/UNCONFIRMED
# THIS SCRIPT IS UNTESTED/UNCONFIRMED
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

parser = argparse.ArgumentParser(description="redfish utility for dell: insert virtual media")

parser.add_argument('-i', help='ilo ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('-m', help='media image url', required=True)
parser.add_argument('-n', help='media image nfs path', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]
image_url    = args["m"]
image_nfs    = args["n"]



## 
##    Insert Virtual Media
## 


url      = 'https://%s/redfish/v1/Managers/1/VirtualMedia/2/Actions/VirtualMedia.InsertMedia' % bmc_ip
headers  = {'content-type': 'application/json'}
payload  = {'Image': image_url }

response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code == 204:
    print("SUCCESS: result code %s returned" % result_code)
else:
    print("FAIL: result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)

