#!/usr/bin/python3
#
# redfish-hp-virtualmedia-status.py
#
#   The curl equivalent:
#
#      curl --insecure -s -u $BMC_USER:$BMC_PASS https://$BMC_IP/redfish/v1/Managers/1/VirtualMedia/1/ | jq -r '.Inserted'
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

parser = argparse.ArgumentParser(description="redfish utility for hp: get virtualmedia state and return 'inserted' or 'ejected'")

parser.add_argument('-i', help='ilo ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Get virtualmedia status
##
##    NOTE: the value we want is a boolean, so simple evaluation works
##

url      = 'https://%s/redfish/v1/Managers/1/VirtualMedia/2/' % bmc_ip
response = requests.get(url, auth=(bmc_username, bmc_password), verify=False)

data = response.json()

if ( data['Inserted'] ):
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

