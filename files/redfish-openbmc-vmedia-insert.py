#!/usr/bin/python3
#
#   The curl equivalent:
#
#      curl --insecure                          \
#           -s                                  \
#           -u <username>:<password>            \
#           -X POST                             \
#           -H "Content-Type: application/json" \
#           -d "{\"Image\":\"<image_url>"       \
#           https://${bmc_ip}/redfish/v1/Managers/1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia
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

parser = argparse.ArgumentParser(description="redfish utility for openbmc: insert virtual media")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('-m', help='media image url', required=True)
parser.add_argument('-n', help='media image nfs path', required=True)

args = vars(parser.parse_args())

##
##    NOTE: OpenBMC does not want the colon in the NFS path
##

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]
image_url    = args["m"]
image_nfs    = args["n"].replace(':','')

vmedia_image = ""
vmedia_state = ""
vmedia_type  = ""



##
##    Get virtualmedia status
##

url      = 'https://%s/redfish/v1/Managers/1/VirtualMedia/CD' % bmc_ip
response = requests.get(url, auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_etag    = response.headers.get('ETag')

if 'Image' in data:
    vmedia_image     = data['Image']
if 'Inserted' in data:
    vmedia_state     = data['Inserted']
if 'TransferProtocolType' in data:
    vmedia_type      = data['TransferProtocolType']

print("BMC IP: %s" % bmc_ip, file=sys.stderr)
print("BMC UID: %s" % bmc_username, file=sys.stderr)
print("Current Image: %s" % vmedia_image, file=sys.stderr)
print("Current Inserted State: %s" % vmedia_state, file=sys.stderr)
print("Current TransferProtocolType: %s" % vmedia_type, file=sys.stderr)



## 
##    Insert Virtual Media
## 

if vmedia_state != True:

    url      = 'https://%s/redfish/v1/Managers/1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia' % bmc_ip
    headers  = {'content-type': 'application/json'}
    payload  = {'Image': image_nfs,
                'TransferProtocolType': 'NFS' }

    print("Attempting Insertion", file=sys.stderr)

    print("New Image: %s" % image_nfs, file=sys.stderr)
    print("New TransferProtocolType: NFS", file=sys.stderr)

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)
    
    result_code = response.status_code
    
    if result_code == 200:
        print("SUCCESS: vmedia image insert returned code %s" % result_code)
        sys.exit(0)
    else:
        print("FAIL: vmedia image insert returned code %s" % result_code)
        print(response)
        sys.exit(1)

else:
    
    print("FAIL: vmedia image already inserted")
    print(response)
    sys.exit(1)


