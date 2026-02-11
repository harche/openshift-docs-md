Before you install OpenShift Virtualization, review this section to ensure that your cluster meets the requirements.

# Compatible platforms

You can use the following platforms with OpenShift Virtualization:

- On-premise bare metal servers. See [Planning a bare metal cluster for OpenShift Virtualization](../../installing/installing_bare_metal/preparing-to-install-on-bare-metal.xml#virt-planning-bare-metal-cluster-for-ocp-virt_preparing-to-install-on-bare-metal).

- Bare metal clusters installed on ARM64-based (`arm64`, also known as `aarch64`) systems.

<!-- -->

- IBM Z® or IBM® LinuxONE (s390x architecture) systems where an OpenShift Container Platform cluster is installed in logical partitions (LPARs). See [Preparing to install on IBM Z and IBM LinuxONE](../../installing/installing_ibm_z/preparing-to-install-on-ibm-z.xml#preparing-to-install-on-ibm-z_preparing-to-install-on-ibm-z).

Cloud platforms
OpenShift Virtualization is also compatible with a variety of public cloud platforms. Each cloud platform has specific storage provider options available. The following table outlines which platforms are fully supported (GA) and which are currently offered as Technology Preview features.

<div class="important">

Installing OpenShift Virtualization on certain cloud platforms is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

<table>
<colgroup>
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Vendor</th>
<th style="text-align: left;">Status</th>
<th style="text-align: left;">Storage</th>
<th style="text-align: left;">Related links</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Amazon Web Services (AWS)</p></td>
<td style="text-align: left;"><p>GA</p></td>
<td style="text-align: left;"><p>Elastic Block Store (EBS), Red Hat OpenShift Data Foundation (ODF), Portworx, FSx (NetApp)</p></td>
<td style="text-align: left;"><ul>
<li><p><a href="../../installing/installing_aws/ipi/installing-aws-customizations.xml#installing-aws-customizations">Installing a cluster on AWS with customizations</a></p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Red Hat OpenShift Service on AWS (ROSA)</p></td>
<td style="text-align: left;"><p>GA</p></td>
<td style="text-align: left;"><p>EBS, Portworx, FSx (Q3), ODF</p></td>
<td style="text-align: left;"><ul>
<li><p><a href="https://docs.redhat.com/en/documentation/red_hat_openshift_service_on_aws/4/html/virtualization/index">OpenShift Virtualization</a> in the Red Hat OpenShift Service on AWS documentation</p></li>
<li><p><a href="https://docs.aws.amazon.com/rosa/latest/userguide/what-is-rosa.html">What is Red Hat OpenShift Service on AWS?</a> in the AWS documentation</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Oracle Cloud Infrastructure (OCI)</p></td>
<td style="text-align: left;"><p>GA</p></td>
<td style="text-align: left;"><p>OCI native storage</p></td>
<td style="text-align: left;"><ul>
<li><p><a href="https://access.redhat.com/articles/7118050">OpenShift Virtualization and Oracle Cloud Infrastructure known issues and limitations</a> in the Red Hat Knowledgebase</p></li>
<li><p><a href="https://github.com/oracle-quickstart/oci-openshift/blob/main/docs/openshift-virtualization.md">Installing OpenShift Virtualization on OCI</a> in the <code>oracle-quickstart/oci-openshift</code> GitHub repository</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Azure Red Hat OpenShift (ARO)</p></td>
<td style="text-align: left;"><p>GA</p></td>
<td style="text-align: left;"><p>ODF</p></td>
<td style="text-align: left;"><ul>
<li><p><a href="https://learn.microsoft.com/en-us/azure/openshift/howto-create-openshift-virtualization">OpenShift Virtualization for Azure Red Hat OpenShift (preview)</a> in the Microsoft documentation</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Google Cloud</p></td>
<td style="text-align: left;"><p>Technology Preview</p></td>
<td style="text-align: left;"><p>Google Cloud native storage</p></td>
<td style="text-align: left;"><ul>
<li><p><a href="https://access.redhat.com/articles/7120382">OpenShift Virtualization and Google Cloud known storage issues and limitations</a> in the Red Hat Knowledgebase</p></li>
</ul></td>
</tr>
</tbody>
</table>

<div class="tip">

For platform-specific networking information, see the [networking overview](../../virt/vm_networking/virt-networking-overview.xml#virt-networking).

</div>

Bare metal instances or servers offered by other cloud providers are not supported.

## OpenShift Virtualization on AWS bare metal

You can run OpenShift Virtualization on an Amazon Web Services (AWS) bare metal OpenShift Container Platform cluster.

<div class="note">

OpenShift Virtualization is also supported on Red Hat OpenShift Service on AWS (ROSA) Classic clusters, which have the same configuration requirements as AWS bare-metal clusters.

</div>

Before you set up your cluster, review the following summary of supported features and limitations:

Installing

- You can install the cluster by using installer-provisioned infrastructure, ensuring that you specify bare-metal instance types for the worker nodes. For example, you can use the `c5n.metal` type value for a machine based on x86_64 architecture. You specify bare-metal instance types by editing the `install-config.yaml` file.

  For more information, see the OpenShift Container Platform documentation about installing on AWS.

Accessing virtual machines (VMs)

- There is no change to how you access VMs by using the `virtctl` CLI tool or the OpenShift Container Platform web console.

- You can expose VMs by using a `NodePort` or `LoadBalancer` service.

  <div class="note">

  The load balancer approach is preferable because OpenShift Container Platform automatically creates the load balancer in AWS and manages its lifecycle. A security group is also created for the load balancer, and you can use annotations to attach existing security groups. When you remove the service, OpenShift Container Platform removes the load balancer and its associated resources.

  </div>

Networking

- You cannot use Single Root I/O Virtualization (SR-IOV) or bridge Container Network Interface (CNI) networks, including virtual LAN (VLAN). If your application requires a flat layer 2 network or control over the IP pool, consider using OVN-Kubernetes secondary overlay networks.

Storage

- You can use any storage solution that is certified by the storage vendor to work with the underlying platform.

  <div class="important">

  AWS bare metal, Red Hat OpenShift Service on AWS, and Red Hat OpenShift Service on AWS classic architecture clusters might have different supported storage solutions. Ensure that you confirm support with your storage vendor.

  </div>

- Using Amazon Elastic File System (EFS) or Amazon Elastic Block Store (EBS) with OpenShift Virtualization might cause performance and functionality limitations as shown in the following table:

  | Feature                                  | EBS volume    |               |           | EFS volume    | Shared storage solutions |
  |------------------------------------------|---------------|---------------|-----------|---------------|--------------------------|
  |                                          | **gp2**       | **gp3**       | **io2**   |               |                          |
  | VM live migration                        | Not available | Not available | Available | Available     | Available                |
  | Fast VM creation by using cloning        | Available     |               |           | Not available | Available                |
  | VM backup and restore by using snapshots | Available     |               |           | Not available | Available                |

  EFS and EBS performance and functionality limitations

  Consider using CSI storage, which supports ReadWriteMany (RWX), cloning, and snapshots to enable live migration, fast VM creation, and VM snapshots capabilities.

Hosted control planes (HCPs)

- HCPs for OpenShift Virtualization are not currently supported on AWS infrastructure.

<!-- -->

- [Connecting a virtual machine to an OVN-Kubernetes secondary network](../../virt/vm_networking/virt-connecting-vm-to-ovn-secondary-network.xml#virt-connecting-vm-to-ovn-secondary-network)

- [Exposing a virtual machine by using a service](../../virt/vm_networking/virt-exposing-vm-with-service.xml#virt-exposing-vm-with-service)

## ARM64 compatibility

Using OpenShift Virtualization on an OpenShift Container Platform cluster installed on an ARM64 system is generally available (GA).

Before using OpenShift Virtualization on an ARM64-based system, consider the following limitations:

Operating system
- Only Linux-based guest operating systems are supported.

- All virtualization limitations for RHEL also apply to OpenShift Virtualization. For more information, see [How virtualization on ARM64 differs from AMD64 and Intel 64](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_virtualization/assembly_feature-support-and-limitations-in-rhel-9-virtualization_configuring-and-managing-virtualization#how-virtualization-on-arm-64-differs-from-amd64-and-intel64_feature-support-and-limitations-in-rhel-9-virtualization) in the RHEL documentation.

Live migration
- Live migration is **not supported** on ARM64-based OpenShift Container Platform clusters.

- Hotplug is not supported on ARM64-based clusters because it depends on live migration.

VM creation
- RHEL 10 supports instance types and preferences, but not templates.

- RHEL 9 supports templates, instance types, and preferences.

## IBM Z and IBM LinuxONE compatibility

You can use OpenShift Virtualization in an OpenShift Container Platform cluster that is installed in logical partitions (LPARs) on an IBM Z® or IBM® LinuxONE (`s390x` architecture) system.

Some features are not currently available on `s390x` architecture, while others require workarounds or procedural changes. These lists are subject to change.

**Currently unavailable features**

The following features are currently not available on `s390x` architecture:

- Memory hot plugging and hot unplugging

- Node Health Check Operator

- SR-IOV Operator

- PCI passthrough

- OpenShift Virtualization cluster checkup framework

- OpenShift Virtualization on a cluster installed in FIPS mode

- IPv6

- IBM® Storage scale

- Hosted control planes for OpenShift Virtualization

- VM pages using HugePages

The following features are not applicable on `s390x` architecture:

- virtual Trusted Platform Module (vTPM) devices

- UEFI mode for VMs

- USB host passthrough

- Configuring virtual GPUs

- Creating and managing Windows VMs

- Hyper-V

**Functionality differences**

The following features are available for use on s390x architecture but function differently or require procedural changes:

- When [deleting a virtual machine by using the web console](../../virt/managing_vms/virt-delete-vms.xml#virt-delete-vm-web_virt-delete-vms), the **grace period** option is ignored.

- When [configuring the default CPU model](../../virt/managing_vms/advanced_vm_management/virt-configuring-default-cpu-model.xml#virt-configuring-default-cpu-model_virt-configuring-default-cpu-model), the `spec.defaultCPUModel` value is `"gen15b"` for an IBM Z cluster.

- When [configuring a downward metrics device](../../virt/monitoring/virt-exposing-downward-metrics.xml#virt-configuring-downward-metrics_virt-exposing-downward-metrics), if you use a VM preference, the `spec.preference.name` value must be set to `rhel.9.s390x` or another available preference with the format `*.s390x`.

- When [creating virtual machines from instance types](../../virt/creating_vm/virt-creating-vms-from-instance-types.xml#virt-creating-vms-from-instance-types), you are not allowed to set `spec.domain.memory.maxGuest` because memory hot plugging is not supported on IBM Z®.

- Prometheus queries for VM guests could have inconsistent outcome in comparison to `x86`.

# Important considerations for any platform

Before you install OpenShift Virtualization on any platform, note the following caveats and considerations.

Installation method considerations
You can use any installation method, including user-provisioned, installer-provisioned, or Assisted Installer, to deploy OpenShift Container Platform. However, the installation method and the cluster topology might affect OpenShift Virtualization functionality, such as snapshots or [live migration](../../virt/install/preparing-cluster-for-virt.xml#live-migration_preparing-cluster-for-virt).

Red Hat OpenShift Data Foundation
If you deploy OpenShift Virtualization with Red Hat OpenShift Data Foundation, you must create a dedicated storage class for Windows virtual machine disks. See [Optimizing ODF PersistentVolumes for Windows VMs](https://access.redhat.com/articles/6978371) for details.

IPv6
OpenShift Virtualization support for single-stack IPv6 clusters is limited to the OVN-Kubernetes localnet and Linux bridge Container Network Interface (CNI) plugins.

<div class="important">

Deploying OpenShift Virtualization on a single-stack IPv6 cluster is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

<!-- -->

FIPS mode
If you install your cluster in [FIPS mode](../../installing/overview/installing-fips.xml#installing-fips-mode_installing-fips), no additional setup is required for OpenShift Virtualization.

# Hardware and operating system requirements

Review the following hardware and operating system requirements for OpenShift Virtualization.

## CPU requirements

- Supported by Red Hat Enterprise Linux (RHEL) 9.

  See [Red Hat Ecosystem Catalog](https://catalog.redhat.com) for supported CPUs.

  <div class="note">

  If your worker nodes have different CPUs, live migration failures might occur because different CPUs have different capabilities. You can mitigate this issue by ensuring that your worker nodes have CPUs with the appropriate capacity and by configuring node affinity rules for your virtual machines.

  See [Configuring a required node affinity rule](../../nodes/scheduling/nodes-scheduler-node-affinity.xml#nodes-scheduler-node-affinity-configuring-required_nodes-scheduler-node-affinity) for details.

  </div>

- Supports AMD64, Intel 64-bit (x86-64-v2), IBM Z® (`s390x`), or ARM64-based (`arm64` or `aarch64`) architectures and their respective CPU extensions.

- Intel VT-x, AMD-V, or ARM virtualization extensions are enabled, or `s390x` virtualization support is enabled.

- NX (no execute) flag is enabled.

- If you use `s390x` architecture, the [default CPU model](../../virt/managing_vms/advanced_vm_management/virt-configuring-default-cpu-model.xml#virt-configuring-default-cpu-model) is set to `gen15b`.

## Operating system requirements

- Red Hat Enterprise Linux CoreOS (RHCOS) installed on worker nodes.

  See [About RHCOS](../../architecture/architecture-rhcos.xml#rhcos-about_architecture-rhcos) for details.

  <div class="note">

  RHEL worker nodes are not supported.

  </div>

## Storage requirements

- Supported by OpenShift Container Platform. See [Optimizing storage](../../scalability_and_performance/optimization/optimizing-storage.xml#_optimizing-storage).

- You must create a default OpenShift Virtualization or OpenShift Container Platform storage class. The purpose of this is to address the unique storage needs of VM workloads and offer optimized performance, reliability, and user experience. If both OpenShift Virtualization and OpenShift Container Platform default storage classes exist, the OpenShift Virtualization class takes precedence when creating VM disks.

<div class="note">

To mark a storage class as the default for virtualization workloads, set the annotation `storageclass.kubevirt.io/is-default-virt-class` to `"true"`.

</div>

- If the storage provisioner supports snapshots, you must associate a `VolumeSnapshotClass` object with the default storage class.

### About volume and access modes for virtual machine disks

If you use the storage API with known storage providers, the volume and access modes are selected automatically. However, if you use a storage class that does not have a storage profile, you must configure the volume and access mode.

For a list of known storage providers for OpenShift Virtualization, see [the Red Hat Ecosystem Catalog](https://catalog.redhat.com/search?searchType=software&badges_and_features=OpenShift+Virtualization&subcategories=Storage).

For best results, use the `ReadWriteMany` (RWX) access mode and the `Block` volume mode. This is important for the following reasons:

- `ReadWriteMany` (RWX) access mode is required for live migration.

- The `Block` volume mode performs significantly better than the `Filesystem` volume mode. This is because the `Filesystem` volume mode uses more storage layers, including a file system layer and a disk image file. These layers are not necessary for VM disk storage.

  For example, if you use Red Hat OpenShift Data Foundation, Ceph RBD volumes are preferable to CephFS volumes.

<div class="important">

You cannot live migrate virtual machines with the following configurations:

- Storage volume with `ReadWriteOnce` (RWO) access mode

- Passthrough features such as GPUs

Set the `evictionStrategy` field to `None` for these virtual machines. The `None` strategy powers down VMs during node reboots.

</div>

# Live migration requirements

- Shared storage with `ReadWriteMany` (RWX) access mode.

- Sufficient RAM and network bandwidth.

  <div class="note">

  You must ensure that there is enough memory request capacity in the cluster to support node drains that result in live migrations. You can determine the approximate required spare memory by using the following calculation:

      Product of (Maximum number of nodes that can drain in parallel) and (Highest total VM memory request allocations across nodes)

  The default [number of migrations that can run in parallel](../../virt/live_migration/virt-configuring-live-migration.xml#virt-configuring-live-migration) in the cluster is 5.

  </div>

- If the virtual machine uses a host model CPU, the nodes must support the virtual machine’s host model CPU.

<div class="note">

A [dedicated Multus network](../../virt/vm_networking/virt-dedicated-network-live-migration.xml#virt-dedicated-network-live-migration) for live migration is highly recommended. A dedicated network minimizes the effects of network saturation on tenant workloads during migration.

</div>

# Physical resource overhead requirements

OpenShift Virtualization is an add-on to OpenShift Container Platform and imposes additional overhead that you must account for when planning a cluster.

Each cluster machine must accommodate the following overhead requirements in addition to the OpenShift Container Platform requirements. Oversubscribing the physical resources in a cluster can affect performance.

<div class="important">

The numbers noted in this documentation are based on Red Hat’s test methodology and setup. These numbers can vary based on your own individual setup and environments.

</div>

## Memory overhead

Calculate the memory overhead values for OpenShift Virtualization by using the equations below.

Cluster memory overhead
    Memory overhead per infrastructure node ≈ 150 MiB

    Memory overhead per worker node ≈ 360 MiB

Additionally, OpenShift Virtualization environment resources require a total of 2179 MiB of RAM that is spread across all infrastructure nodes.

Virtual machine memory overhead
    Memory overhead per virtual machine ≈ (0.002 × requested memory) \
                  + 218 MiB \
                  + 8 MiB × (number of vCPUs) \
                  + 16 MiB × (number of graphics devices) \
                  + (additional memory overhead)

- Required for the processes that run in the `virt-launcher` pod.

- Number of virtual CPUs requested by the virtual machine.

- Number of virtual graphics cards requested by the virtual machine.

- Additional memory overhead:

  - If your environment includes a Single Root I/O Virtualization (SR-IOV) network device or a Graphics Processing Unit (GPU), allocate 1 GiB additional memory overhead for each device.

  - If Secure Encrypted Virtualization (SEV) is enabled, add 256 MiB.

  - If Trusted Platform Module (TPM) is enabled, add 53 MiB.

## CPU overhead

Calculate the cluster processor overhead requirements for OpenShift Virtualization by using the equation below. The CPU overhead per virtual machine depends on your individual setup.

Cluster CPU overhead
    CPU overhead for infrastructure nodes ≈ 4 cores

OpenShift Virtualization increases the overall utilization of cluster level services such as logging, routing, and monitoring. To account for this workload, ensure that nodes that host infrastructure components have capacity allocated for 4 additional cores (4000 millicores) distributed across those nodes.

    CPU overhead for worker nodes ≈ 2 cores + CPU overhead per virtual machine

Each worker node that hosts virtual machines must have capacity for 2 additional cores (2000 millicores) for OpenShift Virtualization management workloads in addition to the CPUs required for virtual machine workloads.

Virtual machine CPU overhead
If dedicated CPUs are requested, there is a 1:1 impact on the cluster CPU overhead requirement. Otherwise, there are no specific rules about how many CPUs a virtual machine requires.

## Storage overhead

Use the guidelines below to estimate storage overhead requirements for your OpenShift Virtualization environment.

Cluster storage overhead
    Aggregated storage overhead per node ≈ 10 GiB

10 GiB is the estimated on-disk storage impact for each node in the cluster when you install OpenShift Virtualization.

Virtual machine storage overhead
Storage overhead per virtual machine depends on specific requests for resource allocation within the virtual machine. The request could be for ephemeral storage on the node or storage resources hosted elsewhere in the cluster. OpenShift Virtualization does not currently allocate any additional ephemeral storage for the running container itself.

Example
As a cluster administrator, if you plan to host 10 virtual machines in the cluster, each with 1 GiB of RAM and 2 vCPUs, the memory impact across the cluster is 11.68 GiB. The estimated on-disk storage impact for each node in the cluster is 10 GiB and the CPU impact for worker nodes that host virtual machine workloads is a minimum of 2 cores.

# Single-node OpenShift differences

You can install OpenShift Virtualization on single-node OpenShift.

However, you should be aware that Single-node OpenShift does not support the following features:

- High availability

- Pod disruption

- Live migration

- Virtual machines or templates that have an eviction strategy configured

<!-- -->

- [Glossary of common terms for OpenShift Container Platform storage](../../storage/index.xml#openshift-storage-common-terms_storage-overview)

# Object maximums

You must consider the following tested object maximums when planning your cluster:

- [OpenShift Container Platform object maximums](../../scalability_and_performance/planning-your-environment-according-to-object-maximums.xml#planning-your-environment-according-to-object-maximums)

- [OpenShift Virtualization supported limits](../../virt/about_virt/virt-supported-limits.xml#virt-supported-limits)

# Cluster high-availability options

You can configure one of the following high-availability (HA) options for your cluster:

- Automatic high availability for [installer-provisioned infrastructure](../../installing/installing_bare_metal/ipi/ipi-install-overview.xml#ipi-install-overview) (IPI) is available by deploying [machine health checks](../../machine_management/deploying-machine-health-checks.xml#machine-health-checks-about_deploying-machine-health-checks).

  <div class="note">

  In OpenShift Container Platform clusters installed using installer-provisioned infrastructure and with a properly configured `MachineHealthCheck` resource, if a node fails the machine health check and becomes unavailable to the cluster, it is recycled. What happens next with VMs that ran on the failed node depends on a series of conditions. See [Run strategies](../../virt/nodes/virt-node-maintenance.xml#run-strategies) for more detailed information about the potential outcomes and how run strategies affect those outcomes.

  Currently, IPI is not supported on IBM Z®.

  </div>

- Automatic high availability for both IPI and non-IPI is available by using the **Node Health Check Operator** on the OpenShift Container Platform cluster to deploy the `NodeHealthCheck` controller. The controller identifies unhealthy nodes and uses a remediation provider, such as the Self Node Remediation Operator or Fence Agents Remediation Operator, to remediate the unhealthy nodes. For more information on remediation, fencing, and maintaining nodes, see the [Workload Availability for Red Hat OpenShift](https://access.redhat.com/documentation/en-us/workload_availability_for_red_hat_openshift) documentation.

  <div class="note">

  Fence Agents Remediation uses supported fencing agents to reset failed nodes faster than the Self Node Remediation Operator. This improves overall virtual machine high availability. For more information, see the [OpenShift Virtualization - Fencing and VM High Availability Guide](https://access.redhat.com/articles/7057929) knowledgebase article.

  </div>

- High availability for any platform is available by using either a monitoring system or a qualified human to monitor node availability. When a node is lost, shut it down and run `oc delete node <lost_node>`.

  <div class="note">

  Without an external monitoring system or a qualified human monitoring node health, virtual machines lose high availability.

  </div>
