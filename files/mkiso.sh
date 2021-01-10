#!/bin/bash

##
##    This script is intended to be used with
##    the xtoph_deploy ansible role.  It generates
##    an iso images based on 2 input values.
##
##      $1 = ISO LABEL
##      $2 = ISO SOURCE PATH
##      $3 = ISO DESTINATION FILE
##



ISO_LABEL="$1"
ISO_SRC="$2"
ISO_FILE="$3"



##
##    Generate the ISO
##



genisoimage -U -r -v -T -J -joliet-long \
            -V      "${ISO_LABEL}" \
            -volset "${ISO_LABEL}" \
            -A      "${ISO_LABEL}" \
            -b      isolinux/isolinux.bin \
            -c      isolinux/boot.cat \
            -no-emul-boot \
            -boot-load-size 4 \
            -boot-info-table \
            -eltorito-alt-boot \
            -e images/efiboot.img \
            -no-emul-boot \
            -o "${ISO_FILE}" ${ISO_SRC}



##
##    NOTE: I have not made use of a hybrid
##          ISO for xtoph_deploy, but why not
##          allow hybrid booting as a CD-ROM or as a
##          hard disk with our generated image



isohybrid --uefi "${ISO_FILE}"





