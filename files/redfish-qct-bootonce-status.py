#!/usr/bin/python3
#
#   The curl equivalent:
#
#      Discover one time bootable devices
#
#          curl --insecure -s -u "${bmc_id}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/system/BootOptions?$expand=*($levels=1)" | jq
#
#      Show the current boot settings (includes override target)
#
#          curl --insecure -s -u "${bmc_uid}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/system" | jq '.Boot.BootSourceOverrideEnabled'
#          curl --insecure -s -u "${bmc_uid}:${bmc_pw}" "https://${bmc_ip}/redfish/v1/Systems/system" | jq '.Boot.BootSourceOverrideTarget'
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

parser = argparse.ArgumentParser(description="redfish utility for qct: report boot-once status")

parser.add_argument('-i', help='bmc ip or hostname', required=True)
parser.add_argument('-u', help='username', required=True)
parser.add_argument('-p', help='password', required=True)
parser.add_argument('--chomp', help='chomp linefeed from output', dest="chomp", default=False, action='store_true')

args = vars(parser.parse_args())

bmc_ip       = args["i"]
bmc_username = args["u"]
bmc_password = args["p"]

##
##    Determine what mode we're in (UEFI vs Legacy/BIOS)
## 

url      = 'https://%s/redfish/v1/Systems/system' % bmc_ip
response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

data = response.json()

override_mode    = data['Boot']['BootSourceOverrideMode']
override_target  = data['Boot']['BootSourceOverrideTarget']
override_enabled = data['Boot']['BootSourceOverrideEnabled']

print("\nRESPONSE:\n%s\n\n" % json.dumps(response.json(),indent=4), file=sys.stderr)

print("Current Override Mode: %s" % override_mode, file=sys.stderr)
print("Current Override Target: %s" % override_target, file=sys.stderr)
print("Current Override Enabled: %s" % override_enabled, file=sys.stderr)

##
##   
##

if override_mode == "UEFI":

    url      = 'https://%s/redfish/v1/Systems/system/BootOptions' % bmc_ip
    response = requests.get(url,auth=(bmc_username, bmc_password), verify=False)

    if response.status_code != 200:
        print("FATAL: OpenBMC version does not support feature")
        sys.exit()
    else:
        pass

    data = response.json()

    if data["Members"] == []:
        print("FATAL: no boot devices detected")
        sys.exit()

    print("Listing available BootOptions:", file=sys.stderr)

    done = False

    pxe_id      = ""
    pxe_name    = ""
    pxe_display = ""
    pxe_uefi    = ""

    for i in data["Members"]:

        member_url      = 'https://%s%s' % ( bmc_ip, i["@odata.id"] )
        member_response = requests.get(member_url,auth=(bmc_username, bmc_password), verify=False)
        member_data     = member_response.json()

        dev_name    = member_data['Name']
        dev_alias   = member_data['Alias']
        dev_display = member_data['DisplayName']
        dev_uefi    = member_data['UefiDevicePath']
        dev_id      = member_data['Id']

        print ( "  %s" % dev_id, file=sys.stderr)
        print ( "    %s" % (dev_alias), file=sys.stderr)
        print ( "    %s" % (dev_display), file=sys.stderr)
        print ( "    %s" % (dev_uefi), file=sys.stderr)

    print("")

##
##   
##

if override_mode == "UEFI":
    if override_target != "None" and override_enabled != "Disabled" :
        result = "set"
    else:
        result = "unset"

else:
    print("FAIL: unexpected condition (Not UEFI)")
    sys.exit(1)


   
##
##    Output varies if chomp is true
##

if args["chomp"]:
  print("%s" % result, end="")
else:
  print("%s" % result)
