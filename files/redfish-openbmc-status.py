#!/usr/bin/python3
#
# redfish-keytus-pxe-bootonce.py
#
#   Usage:
#
#      python3 redfish-keytus-bootonce-pxe.py -u "${bmc_id}" -p "${bmc_pw}" -i $"{bmc_ip}"
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/1/BootOptions?$expand=*($levels=1)" | jq
#
#      Show the current boot settings (includes override target)
#
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/1/"  | jq '.Boot.BootSourceOverrideEnabled'
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/1/"  | jq '.Boot.BootSourceOverrideTarget'
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

parser = argparse.ArgumentParser(description="redfish utility for dell: set boot-once to PXE")

parser.add_argument('-i', help='drac ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

##
## Info about the BMC
##

url      = 'https://%s/redfish/v1/Managers/1/' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

print("BMC Type: %s"      % data['ManagerType'])
print("BMC Model: %s"     % data['Model'])
print("BMC Name: %s"      % data['Name'])
print("BMC Firmware: %s"  % data['FirmwareVersion'])

##
##    Info about Redfish
## 

url      = 'https://%s/redfish/v1' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

print("Redfish Version: %s"      % data['RedfishVersion'])

##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/1/' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_mode   = data['Boot']['BootSourceOverrideMode']
override_target = data['Boot']['BootSourceOverrideTarget']

print("Current Override Mode: %s" % override_mode)
print("Current Override Target: %s" % override_target)

print ("Available Targets: %s" % data['Boot']['BootSourceOverrideTarget@Redfish.AllowableValues'])
print("")

