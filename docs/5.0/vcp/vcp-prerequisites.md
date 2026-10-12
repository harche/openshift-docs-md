Before deploying a virtualized control plane cluster, ensure your environment meets the following requirements.

# Hosting cluster requirements

The hosting cluster runs the virtualized control plane VMs and manages their lifecycle through KubeVirt Redfish.

The hosting cluster requires the following components:

- OpenShift Container Platform installed and operational.

- OpenShift Virtualization installed and configured.

- Sufficient compute resources to host control plane VMs.

- At least three physical nodes to enable anti-affinity placement, ensuring control plane VMs are spread across different physical hosts.

# Storage requirements

The hosting cluster must have a storage solution that supports VM disk images and meets the latency requirements of `etcd`.

Use Logical Volume Manager (LVM) Storage backed by NVMe drives for virtualized control plane storage. LVM Storage writes directly to local disks, providing the consistent low latency that `etcd` requires. Use dedicated NVMe drives for control plane VM disks to ensure predictable performance.

<div class="important">

Do not use Red Hat OpenShift Data Foundation (ODF) for control plane VM disk storage. ODF replicates data across multiple storage nodes, which can cause unpredictable latency spikes during synchronization that affect `etcd` performance.

</div>

During installation of the virtualized control plane, KubeVirt Redfish requires a shared storage location for the installation ISO. When the installer mounts boot media through the Redfish API, KubeVirt Redfish creates a data volume, downloads the installation ISO into that volume, and attaches the volume to the VM as virtual media. Because control plane VMs can be scheduled on any worker node in the hosting cluster, the storage location for the installation ISO must be accessible from all nodes. Do not use a node-local storage class such as LVM Storage for this volume.

# Network requirements

Virtualized control plane deployments require specific network connectivity between VMs, worker nodes, and external services.

Configure networking to meet the following requirements:

- L2 network connectivity between control plane VMs. The OpenShift Container Platform installation program requires all control plane nodes to share the same L2 network segment. The `apiVIPs` must reside on this L2 segment.

- A separate L2 network segment for worker nodes. The `ingressVIPs` must reside on the same L2 segment.

- L3 connectivity without network address translation (NAT) between the control plane VMs and worker nodes. Worker nodes must be able to route traffic directly to the control plane VMs. During installation, the bootstrap VM also requires L3 connectivity to the control plane.

- External access to the cluster API.

- Access to container image registries.

- DNS resolution for cluster components.

You can use either dynamic or static IP addressing for the control plane VMs:

- For deployments that use DHCP, configure static MAC addresses on the primary network interfaces of the VMs and create DHCP reservations for each MAC address. This ensures consistent IP assignment across VM restarts.

- For deployments that use static IP addressing, define the network configuration in your `install-config.yaml` or Agent-based installation manifests.

# Control plane VM requirements

Each control plane VM must meet minimum resource requirements to run the OpenShift Container Platform control plane components reliably.

Each control plane VM requires the following minimum resources:

- 8 vCPUs

- 16 GiB RAM

- 120 GiB storage

  <div class="note">

  Use Logical Volume Manager (LVM) Storage backed by NVMe drives for virtualized control plane storage.

  </div>

# KubeVirt Redfish requirements

KubeVirt Redfish exposes VMs through the Redfish API.

You need the following to use KubeVirt Redfish:

- Network access from the installation workstation to the KubeVirt Redfish route.

- Credentials configured in KubeVirt Redfish for API authentication.

- VMs labeled to be exposed through the Redfish API.

- A shared storage location for the installation ISO. During installation of the virtualized control plane, KubeVirt Redfish uses this location to create a data volume, download the installation ISO into that volume, and attach the volume to the VM as virtual media. Because VMs can be scheduled on any worker node in the hosting cluster, this storage location must be accessible from all nodes. Do not use a node-local storage class such as LVM Storage.

# Additional resources

- [Recommended resources for the agent-based installer](../installing/installing_with_agent_based_installer/preparing-to-install-with-agent-based-installer.xml#agent-based-installer-recommended-resources_preparing-to-install-with-agent-based-installer)

- [Effects of disk latency on etcd](../etcd/etcd-performance.xml#etcd-disk-latency_etcd-performance)
