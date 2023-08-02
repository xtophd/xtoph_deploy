#!/usr/bin/python3
#
# redfish-noop.py
#
#   Use this as a safe no-operation routine for a redfish
#   call that may not be implemented, or does not work
#   on a specific platform.
#
#   Usage:
#    
#      python3 redfish-noop.py -u $BMC_USER -p $BMC_PASS -i $BMC_IP
#
# 
#

import argparse
import json
import requests
import sys
import warnings
import re

##
##    Disable warning messages
##

warnings.filterwarnings("ignore")

##
##    Load commandline arguments
##

parser = argparse.ArgumentParser(description="redfish utility for dell: report boot-once status")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

print("SUCCESS: noop performed")
