Cross-cluster live migration enables users to move a virtual machine (VM) workload from one OpenShift Container Platform cluster to another cluster without disruption.

- OpenShift Virtualization 4.20 or later must be installed.

- The OpenShift Container Platform and OpenShift Virtualization minor release versions must match. For example, if the OpenShift Container Platform version is 4.20.0, the OpenShift Virtualization must also be 4.20.0.

- Two OpenShift Container Platform clusters are required, and the migration network for both clusters must be connected to the same L2 network segment.

- You must have cluster administration privileges and appropriate RBAC privileges to manage VMs on both clusters.
