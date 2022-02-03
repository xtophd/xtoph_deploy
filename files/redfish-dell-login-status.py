#!/usr/bin/python
#
# redfish-dell-login-status.py
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

parser = argparse.ArgumentParser(description="redfish utility for dell: test login credentials and output 'true' or 'false'")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]



## 
##    Test login credentials
## 

url      = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1' % bmc_ip
response = requests.get(url, auth=(bmc_username, bmc_password), verify=False)

if response.status_code == 401:
    print("FATAL: check credentials")
    result="false"
else:
    print("SUCCESS: credentials good")
    result="true"



##
##    Output varies if chomp is true
## 

if args["chomp"]: 
  print("%s" % result, end="")
else:
  print("%s" % result)

