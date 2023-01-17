#!/usr/bin/python3
#
# redfish-dell-debug.py
#
#   Gathers some info and spits it to STDOUT
#
#   Usage:
#    
#      python3 redfish-dell-debug.py -u $BMC_USER -p $BMC_PASS -i $BMC_IP
#
#   SAMPLE:
#
#      while true ; do python redfish-dell-debug.py -i $BMC_IP -u $BMC_USER -p $BMC_PASS ; sleep 60 ; done | tee /var/tmp/redfish-debug.log 
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
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

##
##    Get power status
##

url       = 'https://%s/redfish/v1/Chassis/System.Embedded.1' % bmc_ip
response  = requests.get(url, auth=(bmc_username, bmc_password), verify=False)

data      = response.json()

print("Current Power Status: %s" % str.lower(data['PowerState']))

##
##    Get virtualmedia status
##
##    NOTE: the value we want is a boolean, so simple evaluation works
##

url      = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD' % bmc_ip
response = requests.get(url, auth=(bmc_username, bmc_password), verify=False)

data = response.json()

if ( data['Inserted'] ):
    print("Current vMedia Status: inserted")
else:
    print("Current vMedia Status: ejected")

##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

## DEBUG HELP
##print(json.dumps(data,indent=4,sort_keys=True))

override_mode     = data['Boot']['BootSourceOverrideMode']
override_target   = data['Boot']['BootSourceOverrideTarget']
override_enabled  = data['Boot']['BootSourceOverrideEnabled']
boot_order        = data['Boot']['BootOrder']

print("Current Override Mode: %s" % override_mode)
print("Current Override Target: %s" % override_target)
print("Current Override Enabled: %s" % override_enabled)
print("Current Boot Order: %s" % boot_order)



url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/BootOptions?$expand=*($levels=1)' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

if response.status_code != 200:
    print("FATAL: iDRAC version does not support feature")
    sys.exit()
else:
    pass

data = response.json()

if data["Members"] == []:
    print("FATAL: no boot devices detected")
    sys.exit()

print("Current Boot Devices:")

for i in data["Members"]:

    dev_name    = ""
    dev_display = ""
    dev_id      = ""
    dev_uefi    = ""

    for j in i.items():

        if (j[0] == "Name")           : dev_name    = j[1]
        if (j[0] == "DisplayName")    : dev_display = j[1]
        if (j[0] == "UefiDevicePath") : dev_uefi    = j[1]
        if (j[0] == "Id")             : dev_id      = j[1]


    print ( "  %s | %s | %s" % (dev_id, dev_display, dev_uefi))

print("")

