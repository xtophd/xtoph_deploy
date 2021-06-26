# xtoph_deploy
Ansible role to automate deployment of virtual and physical machines.  Note that this project is designed to integrate and wrap other projects, not stand on it's own.  Please check out OCP4-Workshop or RHEL8-Workshop as examples.

The goal is to:
  * provide a simple tool to provision hosts
  * provision virtual machines on rhel+kvm using libvirt cli tools
  * provision virtual machines on ovirt or using the ovirt-api
  * provision baremetal machines using ipmi
  * operate with network services like dns/dhcp available by using common solutions like pxe, uefi-pxe and uefi-http, ipmi and redfish (coming soon)
  * operate without network services like dns/dhcp available by generating custom ISOs
  * focus on net new (green field)
  * focus on simplest implementation
  * focus on reusible solutions
  * support mixed platform deployments (ie: some vms in ovirt + a baremetal host)
  * once the host is built, job is done, leave no trace and no dependencies

The goal is NOT to:
  * manage ongoing services (dhcp, dns, etc...)
  * worry about prexisting configurations

User work-flow:
  * manual steps on deployhost
      * provision system with an @base install of RHEL 7 or 8
      * install ansible and git
      * install needed ISOs of RHEL (default location: /home/iso)
      * pull the workshop/project that uses xtoph_deploy
      * edit the configs to match environment
  * run xtoph_deploy setup
      * adds packages to support target platform
      * enables services required for the target platform (ie: libvirt services)
      * configures http
      * configures loopback mounts ISOs to serve as install repos
  * run xtoph_deploy deploy
      * builds media for system deployment
      * uses appropriate command-line or APIs to initiate system installs
      * done
  * Addtional capabilities once the configs are compete and working (systems provisioned) you can continue to use xtoph_deploy to
      *  undeploy : shutdown and delete the host(s)
      *  redeploy : shutdown and delete the host(s), and immediately start to deploy again

