
This document in intended to provide some overview of major release changes/updates/gotchas.



== (xtoph_deploy Dropping RHEL 7 (Python2) as a deployhost platform (2022/03/05)

Due to the expanding capabilities of the redfish shim scripts and the lack of support
in python2 to print without a linefeed (chomp), I'm being forced to dump python2 which
means RHEL 7 / CentOS 7 are no longer being tested as a xtoph_deploy platform.

You can still deploy RHEL 7, just not host the xtoph_deploy on it.

I may revert to using shell + curl as the redfish shim solution, but for now I'm sticking
with python3.



== (xtoph_deploy) Multi KVM/Libvirt Platfrom Support (2021/09/23)

Recent updates to xtoph_deploy allow of the specification of multiple libvirt/kvm platform nodes.  Thus, you can deploy openshift across multiple hypervisors without needing to implement ovirt or redhat-virtualization (rhv).  This only works with bridged networking, if you want NAT based network then you are locked in to an all-in-one (single host) deployment.



== (xtoph_deploy) Multi Platfrom Support (2021/09/07)

It is now required that the platform type be specificed as part of the node configuration.  In the context of OCP4-Workshop, this is done in master-config.yml with h_plPROF and should be set to 'ovirt','libvirt' or 'baremetal' which are the 3 currently supported platforms.

This now allows for the speficiation of multiple (different) platforms for deployment.  Meaning, if you have 2 RHV clusters for example, you can deploy a node to one cluster and different node to another cluster.  Testing to follow, but it should work.

There's some work to do in order to support multiple libvirt platforms, but that is the next step.



== (xtoph_deploy) Config File Format Changes (2021/09/07)

All of the custom configs and default configs were stripped of their top-level variable names.  When the variables are loaded, the import_vars task now sets the top-level.

Also, of the configs were stripped of the repetitive nested node/variable names were existed only becuase I had not figured out how to properly prune and graft a sub-element of one hash to a sub-element and another hash.  Now the variable files are simple and they can be safely copied from the role/vars directory in configs and modified.
