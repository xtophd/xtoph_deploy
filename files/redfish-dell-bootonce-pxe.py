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
import re

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

url      = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1' % bmc_ip
response = requests.get(url, auth=(bmc_username, bmc_password), verify=False)

if response.status_code == 401:
    print("WARNING: check credentials")
    sys.exit(1)
else:
    pass



##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_mode   = data['Boot']['BootSourceOverrideMode']
override_target = data['Boot']['BootSourceOverrideTarget']

print("Current Override Mode: %s" % override_mode)
print("Current Override Target: %s" % override_target)

print("")

##
##   Get list of bootable devices
##

if override_mode == "UEFI":

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

    print("Looking for PXE capable devices:")

    pxe_id      = ""
    pxe_name    = ""
    pxe_display = ""
    pxe_uefi    = ""

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


        if ("PXE" in dev_display): 
            pxe_name    = dev_name
            pxe_id      = dev_id
            pxe_display = dev_display
            pxe_uefi    = dev_uefi

            print ( "* %s | %s | %s" % (pxe_id, pxe_display, pxe_uefi))

        else:

            print ( "  %s | %s | %s" % (dev_id, dev_display, dev_uefi))

    print("")



##
##    Clear BootOnce Override
##


url      = 'https://%s/redfish/v1/Systems/System.Embedded.1' % bmc_ip
headers  = {'content-type': 'application/json'}

if override_mode == "UEFI":
    payload  = {'Boot':{'BootSourceOverrideTarget':'None', 'UefiTargetBootSourceOverride': 'None', 'BootSourceOverrideEnabled':'Once'}}
else:
    payload  = {'Boot':{'BootSourceOverrideTarget':'None', 'BootSourceOverrideEnabled':'Once'}}

response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code != 200:
    print("FATAL: clear boot-once result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)
else:
    print("SUCCESS: boot-once cleared \"Pxe\"")
    pass



## 
##    Set PXE Device BootOnce
## 

url      = 'https://%s/redfish/v1/Systems/System.Embedded.1' % bmc_ip
headers  = {'content-type': 'application/json'}

if override_mode == "UEFI":
    print("Setting UEFI boot-once target")
    payload  = {'Boot':{'BootSourceOverrideTarget':'Pxe', 'UefiTargetBootSourceOverride': pxe_uefi}}
else:
    print("Setting BIOS boot-once target")
    payload  = {'Boot':{'BootSourceOverrideTarget':'Pxe'}}

response = requests.patch(url, data=json.dumps(payload), headers=headers, auth=(bmc_username, bmc_password), verify=False)

result_code = response.status_code

if result_code != 200:
    print("FATAL: set boot-once result code %s returned" % result_code)
    print(response.json())
    sys.exit(1)
else:
    print("SUCCESS: boot-once set to %s \"Pxe\"" % override_mode)



##
##    Print current boot-once override device
## 
#
#url      = 'https://%s/redfish/v1/Systems/System.Embedded.1/' % bmc_ip
#response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)
#
#data = response.json()
#
#print("Current boot-once target: %s" % data['Boot']['BootSourceOverrideTarget'])
#
#print("")

