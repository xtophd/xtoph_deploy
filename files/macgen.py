#!/usr/bin/python
# macgen.py script to generate a MAC address for virtual machines
#
#  Another method using python-virtinst (if installed)
#      echo  'import virtinst.util ; print virtinst.util.randomMAC()' | python
#
#  Additional info for reference
#  Source: https://gitlab.com/wireshark/wireshark/raw/master/manuf
#
#    00:16:3E	Xensourc	Xensource, Inc.
#    00:1A:4A	Qumranet	Qumranet Inc.
#    00:1C:14	VMware	VMware, Inc.
#    00:50:56	VMware	VMware, Inc.
#    00:05:69	VMware	VMware, Inc.
#

import random
import sys

def randomMAC():
	mac = [ 0x00, 0x1A, 0x4A,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))

sys.stdout.write( randomMAC() )

