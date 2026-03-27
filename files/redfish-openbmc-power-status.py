#!/usr/bin/python3
#
# redfish-dell-power-status.py
#
#   The curl equivalent:
#
#      curl --insecure -s -u %{bmc_id}:${bmc_pw}  \
#           https://${bmc_ip}/redfish/v1/Chassis/1 | jq -r ".PowerState" | tr [:upper:] [:lower:]
#

import argparse
import json
import requests
import sys
import warnings
from time import sleep



##
##    Disable warning messages
##

warnings.filterwarnings("ignore")



##
##    Load commandline arguments
##

parser = argparse.ArgumentParser(description="redfish utility for dell: get power state and return 'on' or 'off'")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Get power status - need 3 consecutive consistenct results
## 

url         = 'https://%s/redfish/v1/Chassis/1' % bmc_ip
last_result = ""
i           = 1

while i < 4:

    response  = requests.get(url, auth=(bmc_username, bmc_password), verify=False)
    data      = response.json()

    if last_result != "" and last_result != data['PowerState']:
        print("Restarting the confirmation count...",file=sys.stderr)
        last_result=""
        i = 1
        next

    print("Confirmation %s/3" % i,file=sys.stderr)
    last_result = data['PowerState']
    i += 1
    sleep(3)


##
##    Output varies if chomp is true
## 

if args["chomp"]: 
  print("%s" % str.lower(data['PowerState']), end="")
else:
  print("%s" % str.lower(data['PowerState']))

