These release notes describe new features and enhancements, Technology Preview features, deprecated and removed features, fixed issues, and known issues for OpenShift Virtualization 5.0.

# Supported guest operating systems

To view the supported guest operating systems for OpenShift Virtualization, see [Certified Guest Operating Systems in Red Hat OpenStack Platform, Red Hat Virtualization, OpenShift Virtualization and Red Hat Enterprise Linux with KVM](https://access.redhat.com/articles/973163#ocpvirt).

# New features and enhancements

Dual stream support for OpenShift Virtualization clusters
You can provision OpenShift Virtualization clusters that run Red Hat Enterprise Linux CoreOS (RHCOS) version 9.8 and version 10.2. RHCOS 10.2 is the default operating system. RHCOS 9.8 is also supported. Live migration of virtual machines (VMs) between RHCOS 9.x and RHCOS 10.x worker nodes is supported.

[CNV-84749](https://issues.redhat.com/browse/CNV-84749)

<!-- -->

The v1 version of the `HyperConverged` API is the default
The `v1` API version of the `HyperConverged` custom resource (CR) is the default version. The `v1beta1` version is deprecated and will be removed in a future release. OpenShift Virtualization adds new API fields only to the `v1` version. Updates from earlier versions require no manual action.

[CNV-79504](https://issues.redhat.com/browse/CNV-79504)

<!-- -->

Boot source image support for heterogeneous clusters is generally available
After you enable the `enableMultiArchBootImageImport` feature gate, OpenShift Virtualization creates architecture-specific boot sources for each supported architecture, such as `rhel9-amd64` and `rhel9-arm64`. You can also specify the architecture for standalone data volumes and virtual machines. For more information, see [Heterogeneous cluster support](../../virt/storage/virt-boot-source-image-heterogeneous-clusters.xml#virt-boot-source-image-heterogeneous-clusters).

[CNV-67900](https://issues.redhat.com/browse/CNV-67900)

<!-- -->

The `virt-platform-autopilot` controller is generally available
The `virt-platform-autopilot` controller lowers deployment complexity by automatically enforcing configuration best practices across OpenShift Virtualization and adjacent Operators, such as the Kube Descheduler Operator and Cluster Observability Operator. It simplifies initial setup and maintains safe, optimal settings for swap readiness, load-aware balancing, and enhanced cluster observability to help ensure long-term stability across version upgrades.

[CNV-81291](https://issues.redhat.com/browse/CNV-81291)

<!-- -->

Load-aware rebalancing is enabled by default on clusters
On clusters where the Kube Descheduler Operator is installed, OpenShift Virtualization automatically configures the descheduler to run in load-aware balancing mode, which accounts for both CPU and memory usage when it rebalances virtual machine (VM) workloads across nodes. The descheduler is an optional component that OpenShift Virtualization does not install for you. If the Kube Descheduler Operator is not installed, no rebalancing occurs. You can disable load-aware rebalancing in the OpenShift Container Platform web console. For more information, see [How automated postinstallation configuration works](../../virt/post_installation_configuration/virt-platform-autopilot.xml#virt-about-platform-autopilot_virt-platform-autopilot).

[CNV-80073](https://issues.redhat.com/browse/CNV-80073)

<!-- -->

Self-service Technical Supportability Review
You can use the self-service Technical Supportability Review (TSR) on the Red Hat Customer Portal to validate your cluster configuration against Red Hat common practices. The self-service TSR uses AI to evaluate your cluster’s `must-gather` data and provides a prioritized executive summary that identifies your cluster’s top risks and recommends corrective actions. The TSR performs hundreds of checks across the OpenShift Container Platform platform, including OpenShift Virtualization, and coverage is continually expanding.

For more information, see [Technical Supportability Review with AI tool](https://access.redhat.com/support/cases/#/analyze) and [Red Hat Technical Supportability Review with AI: Proactive AI-Driven Cluster Assessments for OpenShift Container Platform](https://access.redhat.com/solutions/7141255).

<!-- -->

Support for IBM Z Fusion Access for SAN on IBM Z and IBM LinuxONE is generally available
On IBM Z® and IBM® LinuxONE, you can deploy IBM® Fusion Access for SAN. IBM® Fusion Access for SAN is a cloud-native solution that helps you manage existing Storage Area Network (SAN) infrastructure for workloads on OpenShift Virtualization. For more information, see [Fusion Access for SAN](https://www.ibm.com/docs/en/fusion-software/2.14.0?topic=fusion-access-san).

[CNV-98210](https://issues.redhat.com/browse/CNV-98210)

<!-- -->

`VirtualMachineTemplate` custom resource definitions are generally available
The `template.kubevirt.io/v1beta1` API group and the `VirtualMachineTemplate` custom resource definition (CRD) are generally available. You can define a virtual machine (VM) blueprint as a cluster-native `VirtualMachineTemplate` object and then create VMs from that object. You can use the `VirtualMachineTemplateRequest` CRD to create a `VirtualMachineTemplate` from an existing `VirtualMachine`. This release updates the API group from `v1alpha1` to `v1beta1`.

<div class="note">

You cannot create a `VirtualMachineTemplate` from a `VirtualMachine` that you have never started.

</div>

[CNV-84116](https://issues.redhat.com/browse/CNV-84116)

<!-- -->

Custom video device types are generally available
You can configure a custom video device type when you create a virtual machine (VM). Configuring a custom device type overrides the default video configuration. You can specify different video devices, based on your guest operating system requirements and performance needs.

[CNV-71195](https://issues.redhat.com/browse/CNV-71195)

<!-- -->

The `virt-platform-autopilot` controller replaces the `wasp-agent` component
The `virt-platform-autopilot` controller replaces the `wasp-agent` component for configuring higher VM workload density. When you enable memory overcommitment in the `HyperConverged` custom resource, the controller automatically deploys the necessary node-level configurations, which simplifies the setup process. You must manually provision swap storage on worker nodes by creating a `MachineConfig` object. For more information, see [Configuring higher VM workload density](../../virt/post_installation_configuration/virt-configuring-higher-vm-workload-density.xml#virt-configuring-higher-vm-workload-density).

[CNV-83420](https://issues.redhat.com/browse/CNV-83420)

<!-- -->

KubeVirt Redfish for VM management is generally available
With this release, KubeVirt Redfish is generally available. KubeVirt Redfish exposes OpenShift Virtualization virtual machines through the standard Redfish API. Using KubeVirt Redfish, administrators can manage VM power states, boot configuration, and virtual media attachments. This update also adds `bcrypt` hashed passwords for more secure authentication to the KubeVirt Redfish API.

For more information, see [Configuring KubeVirt Redfish for VM management](../post_installation_configuration/virt-kubevirt-redfish.xml#virt-kubevirt-redfish).

<!-- -->

Configuring PCI passthrough for the RoCE and ISM devices on IBM Z and IBM LinuxONE is generally available
On IBM Z® and IBM® LinuxONE, you can configure PCI passthrough for Network Express RoCE adapters and IBM® Internal Shared Memory (ISM) virtual PCI devices.

For more information, see [PCI passthrough on IBM Z](https://docs.redhat.com/en/documentation/openshift_container_platform/5.0/html/virtualization/managing_vms/advanced_vm_management/virt-configuring-pci-passthrough.html#virt-configuring-pci-passthrough-ibm-z_virt-configuring-pci-passthrough).

[CNV-96643](https://issues.redhat.com/browse/CNV-96643)

<!-- -->

Confidential computing with CCRV on IBM Z and IBM LinuxONE
You can deploy confidential computing workloads by using IBM® Confidential Computing Container Runtime for Red Hat Virtualization Solutions (CCRV). This integration enables CCRV workloads to use OpenShift Virtualization functionalities while maintaining confidential computing capabilities.

[CNV-96593](https://issues.redhat.com/browse/CNV-96593)

<!-- -->

Configure VM node placement on IBM Z mixed-node clusters
On IBM Z® and IBM® LinuxONE clusters, OpenShift Virtualization only supports VMs on bare metal LPAR nodes. You can restrict both OpenShift Virtualization infrastructure components and VM workloads to bare metal LPAR nodes by applying a node placement rule.

For more information, see [Configuring node placement for OpenShift Virtualization components on IBM Z](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html-single/virtualization/index#virt-configuring-node-placement-ibm-z_virt-node-placement-virt-components).

[CNV-95482](https://issues.redhat.com/browse/CNV-95482)

<!-- -->

Simplified IBM Secure Execution deployment by using a bootable image
You can upload an IBM® Secure Execution bootable image and associate it with a predefined preference. Virtual machines (VMs) that you create from the image automatically enable the `launchSecurity` setting.

For more information, see [Upload and use an IBM Secure Execution bootable image on IBM Z and IBM LinuxONE](../../virt/creating_vm/virt-configuring-ibm-secure-execution-vms-ibm-z.xml#virt-upload-ibm-secure-execution-bootable-image-ibm-z_virt-configuring-ibm-secure-execution-vms-ibm-z).

[CNV-97316](https://issues.redhat.com/browse/CNV-97316)

<!-- -->

Default network for new virtual machines in a project
If you have cluster administrator permissions, you can configure a default network for a project so that new virtual machines (VMs) in that project use it automatically. The default can be the pod network or a network attachment definition (NAD) that is available in the project. This setting applies only to VMs that you create after you configure it, and it does not change existing VMs.

For more information, see [Configuring project-level default networks](../../virt/creating_vm/virt-creating-vms-web.xml#virt-vm-configuring-default-network-per-project_virt-creating-vms-web).

[CNV-92410](https://issues.redhat.com/browse/CNV-92410)

<!-- -->

Network hot swap for running virtual machines
You can change the network that a running virtual machine (VM) interface uses. In the OpenShift Container Platform web console, open the **Configuration** \> **Network** tab, edit the existing interface, and select a different network.

[CNV-82742](https://issues.redhat.com/browse/CNV-82742)

<!-- -->

Declarative hot plug volumes and CD-ROM media changes are enabled by default
The `DeclarativeHotplugVolumes` feature gate is enabled by default in the `HyperConverged` custom resource (CR). You can insert and eject CD-ROM storage in a running virtual machine (VM) without restarting the VM and without changing the default configuration. In earlier releases, you enabled the feature gate manually because it was incompatible with ephemeral hot plug volumes.

[CNV-81481](https://issues.redhat.com/browse/CNV-81481)

<!-- -->

Bulk storage class migration for offline VMs
Administrators can bulk migrate storage classes of stopped virtual machines (VMs) in the OpenShift Container Platform web console. This functionality supports storage class migration for VMs in any state. You can select both running and stopped VMs in a single migration plan.

[CNV-73500](https://redhat.atlassian.net/browse/CNV-73500)

<!-- -->

Automatic cleanup of source PVCs after storage migration
You can clear the option to keep source persistent volume claims (PVCs) after a storage migration. If you clear this option in the web console, OpenShift Virtualization cleans up the original PVCs after the storage migration completes. By default, OpenShift Virtualization retains the source PVCs after a storage migration, and you clean up the PVCs manually.

[CNV-73509](https://issues.redhat.com/browse/CNV-73509)

<!-- -->

Categories for virtual machine templates
You can assign a category to a virtual machine (VM) template and then filter the template catalog by category. You set the category when you create a template from an existing VM, and you can change it later. A category is optional, and a template can have only one category.

[CNV-92485](https://issues.redhat.com/browse/CNV-92485)

<!-- -->

Network names on the virtual machine Network tab link to their resources
On the **Configuration** \> **Network** tab of a virtual machine (VM), each network name is a link. The link opens the detail page of the underlying network attachment definition (NAD), user-defined network (UDN), or cluster user-defined network (CUDN). Entries for **Pod networking** and for deleted networks remain plain text.

[CNV-89211](https://issues.redhat.com/browse/CNV-89211)

<!-- -->

New search language for building complex virtual machine queries
You can build and save complex virtual machine (VM) queries directly in the search field, without opening the **Advanced search** dialog. You can combine multiple parameters and their multiple values in the search.

For more information, see [Searching for virtual machines by using the web console](../../virt/managing_vms/virt-list-vms.xml#virt-searching-vms-web_virt-list-vms).

[CNV-74170](https://issues.redhat.com/browse/CNV-74170)

<!-- -->

CSV export for OpenShift Virtualization list tables
You can download table data in CSV format from OpenShift Virtualization list views in the OpenShift Container Platform web console, including **Virtual Machines**, **Templates**, **DataSources**, **Bootable volumes**, **Migration policies**, and **Storage migrations**. The downloaded CSV file has the filtered and sorted rows exactly as shown in the table and excludes hidden content and non-data columns.

[CNV-89012](https://issues.redhat.com/browse/CNV-89012)

<!-- -->

Virtual machine filtering by group
You can filter virtual machines by group in the OpenShift Container Platform web console. The **Group** filter is available in the advanced search dialog and as a drop-down filter in the main virtual machine list view.

[CNV-94093](https://issues.redhat.com/browse/CNV-94093)

<!-- -->

Auto-hidden navigation menu on virtualization pages
The left navigation menu now collapses when you go to OpenShift Virtualization pages, such as the virtual machine (VM) list and VM detail pages. This gives you more space to view and manage your VMs. If you expand the navigation menu, it stays open while you remain on virtualization pages. To turn off this behavior, go to **Settings** \> **User** \> **General** and clear the **Auto-hide navigation menu** toggle.

[CNV-86441](https://issues.redhat.com/browse/CNV-86441)

<!-- -->

Metrics for GPUs attached to virtual machines
OpenShift Virtualization exposes metrics that identify the GPUs attached to a virtual machine instance (VMI). You can correlate these metrics with the GPU metrics that the NVIDIA Data Center GPU Manager (DCGM) exporter provides to track GPU allocation and usage. Recording rules simplify the use of these metrics in OpenShift Virtualization dashboards.

[CNV-51516](https://issues.redhat.com/browse/CNV-51516)

<!-- -->

Perses-based virtualization dashboards
OpenShift Virtualization provides Perses-based dashboards that show virtual machine (VM) inventory, resource usage, service levels, time in status, top resource consumers, and node memory. OpenShift Virtualization deploys the dashboards automatically as `PersesDashboard` custom resources in the `openshift-cnv` namespace. To view the dashboards, click **Observe** \> **Dashboards(Perses)** in the OpenShift Container Platform web console. The dashboards require Cluster Observability Operator (COO) with the monitoring stack enabled. For more information, see [Virtualization dashboards overview](../../virt/monitoring/virt-prometheus-queries.xml#virt-about-virtualization-dashboards_virt-prometheus-queries).

[CNV-42730](https://issues.redhat.com/browse/CNV-42730)

<!-- -->

New virtual machine panic alerts in the OpenShift Virtualization runbooks
The following alerts for the OpenShift Virtualization Operator are included in the OpenShift Virtualization runbooks:

- `ClusterVMPanicDetected`

- `VMNonRecoverableOSPanic`

  [CNV-81546](https://issues.redhat.com/browse/CNV-81546)

# Deprecated features

The `HotplugVolume` feature gate is deprecated
The `HotplugVolume` feature gate, which allows you to add storage without restarting your VM, is deprecated and will be removed in a future release. This feature gate will be replaced by `DeclarativeHotplugVolumes`.

<div class="note">

`DeclarativeHotplugVolumes` does not support hot plugging ephemeral volumes. Ephemeral volumes are hot plugged to a VMI and do not persist in the owner VM. Existing ephemeral volumes that are hot plugged are automatically detached after you switch to the `DeclarativeHotplugVolumes` feature gate.

</div>

[CNV-73301](https://issues.redhat.com/browse/CNV-73301)

<!-- -->

The `pc-q35-rhel7.x.0` and `pc-q35-rhel8.x.0` machine types are deprecated
These machine types have been deprecated since OpenShift Virtualization 4.13 and will be removed in a future release as part of the move to Red Hat Enterprise Linux (RHEL) 10 user space. Update the machine type of your virtual machines (VMs) to `pc-q35-rhel9.8.0`. Updating the machine type requires a VM restart, so plan for downtime. For more information about updating multiple VMs at the same time, see [Updating multiple virtual machines](../../virt/managing_vms/virt-edit-vms.xml#virt-updating-multiple-vms_virt-edit-vms).

[CNV-98500](https://issues.redhat.com/browse/CNV-98500)

# Removed features

Removed features are no longer supported in OpenShift Virtualization.

The `wasp-agent` component is removed
The `wasp-agent` component, which configured higher VM workload density, is removed and is no longer supported. You configure higher VM workload density by using the `virt-platform-autopilot` controller. For more information, see [Configuring higher VM workload density](../../virt/post_installation_configuration/virt-configuring-higher-vm-workload-density.xml#virt-configuring-higher-vm-workload-density).

[CNV-83420](https://issues.redhat.com/browse/CNV-83420)

<!-- -->

Ephemeral hot plug telemetry is removed
Telemetry for ephemeral hot plug volumes is removed and is no longer supported. The `DeclarativeHotplugVolumes` feature gate replaces the deprecated `HotplugVolume` feature gate.

[CNV-81481](https://issues.redhat.com/browse/CNV-81481)

# Technology Preview features

Some features in this release are currently in Technology Preview. These experimental features are not intended for production use. Note the following scope of support on the Red Hat Customer Portal for these features:

[Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview)

Convert an existing VM to a template from the user interface (Technology Preview)
Virtual machine (VM) owners can create, filter, and delete a user-generated template. You can create a template from an existing VM in the same project as the running VM or a different project from the OpenShift Virtualization user interface. To make sure that the data is consistent, stop the VM before you create a template. This capability is a Technology Preview feature.

[CNV-81577](https://redhat.atlassian.net/browse/CNV-81577)

<!-- -->

Create virtual machines from in-cluster native templates (Technology Preview)
Virtual machine (VM) owners can create VMs from the OpenShift Virtualization cluster native template custom resource. The VM template tracks a golden image that is updated periodically, reducing errors and ensuring uniformity in the virtualized environment. You can host the template in all namespaces that you can control.

[CNV-73392](https://redhat.atlassian.net/browse/CNV-73392)

<!-- -->

Groups label for organizing virtual machines (Technology Preview)
The label for organizing and grouping virtual machines (VMs) in the web console is **Groups**, which more accurately reflects the functionality. This capability is a Technology Preview feature. For more information, see [Organize virtual machines by using the web console](../../virt/managing_vms/virt-list-vms.xml#virt-organize-vms-web_virt-list-vms).

[CNV-91926](https://redhat.atlassian.net/browse/CNV-91926)

<!-- -->

Model Context Protocol server tools for storage and virtual machine templates (Technology Preview)
You can use the Model Context Protocol (MCP) server to manage OpenShift Virtualization resources through high-level workflows. This release adds tools for persistent storage, virtual machine (VM) templates, and HyperConverged Operator status and configuration. The kubevirt toolset is not enabled by default. To use these tools, add kubevirt to the toolsets setting in the OpenShift Container Platform MCP server configuration file. This capability is a Technology Preview feature.

[CNV-77676](https://issues.redhat.com/browse/CNV-77676)

<!-- -->

Opt out of virtualization role aggregation for users (Technology Preview)
Cluster administrators can set the `.spec.roleAggregationStrategy` field in the `HyperConverged` custom resource (CR) to `Manual` to stop aggregating the virtualization cluster roles `admin`, `edit`, and `view` to users. After an administrator selects `Manual`, regular users cannot interact with virtualization resources such as virtual machines (VMs) in their projects, either from the command-line interface (CLI) or the web console. To grant a user these permissions, the administrator creates a `RoleBinding` object. This capability is a Technology Preview feature.

[CNV-87048](https://issues.redhat.com/browse/CNV-87048)

# Fixed issues

Detached disks are no longer deleted together with the original virtual machine
Before this update, when you detached a disk from a virtual machine (VM), the `DataVolume` object retained a stale owner reference to the original VM. As a consequence, if you deleted the original VM, garbage collection deleted the `DataVolume` object and its underlying persistent volume claim (PVC). This caused data loss even when the disk was attached to a different VM. With this release, OpenShift Virtualization updates the owner reference when you detach a disk, so the `DataVolume` object no longer references the original VM. As a result, a detached disk and its PVC are preserved when you delete the VM that the disk was originally attached to.

[CNV-71659](https://redhat.atlassian.net/browse/CNV-71659)

# Known issues

Some linked Jira tickets are accessible only with Red Hat credentials.

Node labels remain after uninstalling OpenShift Virtualization
Uninstalling OpenShift Virtualization does not remove the `feature.node.kubevirt.io` node labels that OpenShift Virtualization creates. As a consequence, nodes can still appear as if they are configured for virtualization workloads.

To work around this problem, manually remove the `feature.node.kubevirt.io` labels from affected nodes after you uninstall OpenShift Virtualization.

[CNV-38543](https://issues.redhat.com/browse/CNV-38543)

<!-- -->

Live migration fails when VM names exceed 47 characters
Live migration fails if a virtual machine name exceeds 47 characters. As a consequence, you cannot live migrate VMs with longer names.

To work around this problem, use VM names that are 47 characters or fewer when you create VMs that you plan to live migrate.

[CNV-61066](https://issues.redhat.com/browse/CNV-61066)

<!-- -->

Duplicate boot sources remain after you enable multi-architecture boot image import
If you enable the `spec.featureGates.enableMultiArchBootImageImport` feature gate after boot sources are imported, OpenShift Virtualization recreates the boot source import resources by using architecture-suffixed names. The names depend on the architectures that the cluster supports, for example `fedora-amd64`, `fedora-arm64`, and `fedora-s390x`. The earlier resources, which have no architecture suffix, remain in the `openshift-virtualization-os-images` namespace. As a consequence, duplicate boot sources are displayed in the web console and in the CLI. Storage usage can also increase, because the extra persistent volume claims (PVCs) and volume snapshots are still present.

To work around this problem, delete the leftover boot source resources. First, identify the active `DataSource` objects, which are the objects that resolve to the PVC or volume snapshot that you want to keep. Then, delete the stale `DataSource` objects and the PVCs and volume snapshots that they reference. As a result, only the architecture-suffixed boot sources remain.

[CNV-68996](https://issues.redhat.com/browse/CNV-68996)
