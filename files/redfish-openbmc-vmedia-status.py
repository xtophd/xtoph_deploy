#!/usr/bin/python3
#
#
#   The curl equivalent:
#
#      curl --insecure -s -u "${bmc_id}:${bmc_pw}" https://${bmc_ip}/redfish/v1/Managers/1/VirtualMedia/CD | jq -r '.Inserted'
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

parser = argparse.ArgumentParser(description="redfish utility for openbmc: get virtualmedia state and return 'inserted' or 'ejected'")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

vmedia_image = ""
vmedia_state = ""
vmedia_type  = ""

##
##    Get virtualmedia status
##
##    NOTE: the value we want is a boolean, so simple evaluation works
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


print("Current Image: %s" % vmedia_image, file=sys.stderr)
print("Current Inserted State: %s" % vmedia_state, file=sys.stderr)
print("Current TransferProtocolType: %s" % vmedia_type, file=sys.stderr)

if ( vmedia_state == True ):
    result = "inserted"
else:
    result = "ejected"



##
##    Output varies if chomp is true
## 

if args["chomp"]: 
  print("%s" % result, end="")
else:
  print("%s" % result)

