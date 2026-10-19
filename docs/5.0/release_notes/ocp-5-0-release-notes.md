Red Hat OpenShift Container Platform provides developers and IT organizations with a hybrid cloud application platform for deploying both new and existing applications on secure, scalable resources with minimal configuration and management. OpenShift Container Platform supports a wide selection of programming languages and frameworks, such as Java, JavaScript, Python, Ruby, and PHP.

Built on Red Hat Enterprise Linux (RHEL) and Kubernetes, OpenShift Container Platform provides a more secure and scalable multitenant operating system for today’s enterprise-class applications, while delivering integrated application runtimes and libraries. OpenShift Container Platform enables organizations to meet security, privacy, compliance, and governance requirements.

# About this release

OpenShift Container Platform ([RHBA-2026:449](https://access.redhat.com/errata/RHBA-2026:449)) is now available. This release uses [Kubernetes 1.36](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.36.md) with CRI-O runtime. New features, changes, and known issues that pertain to OpenShift Container Platform 4.17 are included in this topic.

OpenShift Container Platform 4.17 clusters are available at <https://console.redhat.com/openshift>. From the Red Hat Hybrid Cloud Console, you can deploy OpenShift Container Platform clusters to either on-premises or cloud environments.

You must use RHCOS machines for the control plane and for the compute machines.

Starting from OpenShift Container Platform 4.14, the Extended Update Support (EUS) phase for even-numbered releases increases the total available lifecycle to 24 months on all supported architectures, including `x86_64`, 64-bit ARM (`aarch64`), IBM Power® (`ppc64le`), and IBM Z® (`s390x`) architectures. Beyond this, Red Hat also offers a 12-month additional EUS add-on, denoted as *Additional EUS Term 2*, that extends the total available lifecycle from 24 months to 36 months. The Additional EUS Term 2 is available on all architecture variants of OpenShift Container Platform. For more information about support for all versions, see the [Red Hat OpenShift Container Platform Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift).

## About FIPS compliance

OpenShift Container Platform is designed for FIPS. When running Red Hat Enterprise Linux (RHEL) or Red Hat Enterprise Linux CoreOS (RHCOS) booted in FIPS mode, OpenShift Container Platform core components use the RHEL cryptographic libraries that have been submitted to NIST for FIPS 140-2/140-3 Validation on only the `x86_64`, `ppc64le`, and `s390x` architectures.

For more information about the NIST validation program, see [Cryptographic Module Validation Program](https://csrc.nist.gov/Projects/cryptographic-module-validation-program/validated-modules). For the latest NIST status for the individual versions of RHEL cryptographic libraries that have been submitted for validation, see [Compliance Activities and Government Standards](https://access.redhat.com/articles/2918071#fips-140-2-and-fips-140-3-2).

## About PQC compliance

OpenShift Container Platform supports post-quantum cryptography (PQC) readiness for secure cluster communication. When running on Red Hat Enterprise Linux (RHEL) or Red Hat Enterprise Linux CoreOS (RHCOS), core OpenShift Container Platform components use the cryptographic capabilities provided by the platform operating system and TLS 1.3 security profiles, including hybrid Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM) key exchange where enabled by the configured TLS security profile and supported by the component.

For more information about NIST post-quantum cryptography standards, see [Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography). For the latest compliance information for OpenShift Container Platform, RHEL, and Red Hat Enterprise Linux CoreOS (RHCOS), see [Compliance Activities and Government Standards](https://access.redhat.com/articles/2918071).

# OpenShift Container Platform layered and dependent component support and compatibility

The scope of support for layered and dependent components of OpenShift Container Platform changes independently of the OpenShift Container Platform version. To determine the current support status and compatibility for an add-on, refer to its release notes. For more information, see the [Red Hat OpenShift Container Platform Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift).

# New features and enhancements

This release adds improvements related to the following components and concepts:

## AI applications

Troubleshooting NIDS issues with an AI agent
You can use the netedge toolset in the MCP server for OpenShift Container Platform to diagnose Network Ingress and DNS (NIDS) issues by describing symptoms to a connected LLM client in natural language.

For more information, see [Troubleshooting NIDS issues with an AI agent](../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-ingress-controller.xml#ai-driven-networking-troubleshooting_configuring-ingress-cluster-traffic-ingress-controller).

## Authentication and authorization

Advanced direct authentication fields are now generally available
Advanced direct authentication fields for OIDC-based authentication are now generally available for standalone and hosted control plane (HCP) clusters. These fields, which include custom OIDC discovery URLs, CEL-based claim mapping and validation rules, and user validation rules, no longer require the `TechPreviewNoUpgrade` feature set.

For more information, see [Advanced direct authentication fields](../authentication/structured-auth-config-fields.xml#structured-auth-config-fields).

## Autoscaling

## Cluster Version Operator

## etcd

etcd selectable database size
When large or high-churn workloads approach the default 8 GiB limit, you can increase the etcd backend database quota up to 16 GiB. After you increase the quota, you cannot decrease it.

For more information, see [Selectable etcd database size for large clusters](../etcd/etcd-performance.xml#etcd-selectable-db_etcd-performance).

## Extensions (OLM v1)

## IBM Power

The IBM Power® release on OpenShift Container Platform 4.17 adds improvements and new capabilities to OpenShift Container Platform components
New features on IBM Power® include:

- Custom Metrics Autoscaler Operator (KEDA) on IBM Power®

- Dual Operating Stream on IBM Power®

  - IBM Power®9 requires RHEL version 9 stream

  - IBM Power®10 and IBM Power®11 may use either RHEL version 9 or RHEL version 10 stream

## IBM Z and IBM LinuxONE

The IBM Z® and IBM® LinuxONE release on OpenShift Container Platform 4.17 adds improvements and new capabilities to OpenShift Container Platform components
New features on IBM Z® and IBM® LinuxONE include:

- SR-IOV Network Operator support for IBM Z® and IBM® LinuxONE

- Custom Metrics Autoscaler Operator (KEDA) on IBM Z®

- Dual Operating Stream on IBM Z®

## Insights Operator

## Installation and update

AI-powered update risk and status assessments
With this release, you can use the web console to generate AI-powered guidance specific to your cluster to assess the risk of an update path or the status of an in-progress update.

For more information, see [Analyzing update risk and status using AI](../updating/preparing_for_updates/updating-cluster-prepare.xml#update-assessment-ai_updating-cluster-prepare).

Installing a cluster on Amazon Web Services (AWS) with a user-provisioned DNS is generally available
You can enable a user-provisioned domain name server (DNS) instead of the default cluster-provisioned DNS solution. For example, your organization’s security policies might not allow the use of public DNS services such as Amazon Web Services (AWS) DNS. As a result, you can manage the API and Ingress DNS records in your own system rather than adding the records to the DNS of the cloud. If you use this feature, you must provision the cluster first and then provide your own DNS solution that includes records for `api.<cluster_name>.<base_domain>.` and `*.apps.<cluster_name>.<base_domain>.`.

Installing a cluster on AWS with a user-provisioned DNS was introduced in OpenShift Container Platform 4.21 with Technology Preview status. In OpenShift Container Platform 5.0, it is now generally available.

For more information, see [Enabling a user-managed DNS](../installing/installing_aws/ipi/installing-aws-vpc.xml#installation-aws-enabling-user-managed-DNS_installing-aws-vpc) and [Provisioning your own DNS records](../installing/installing_aws/ipi/installing-aws-vpc.xml#installation-aws-provisioning-own-dns-records_installing-aws-vpc).

Firewall requirements when interactively generating Amazon Web Services (AWS) install configurations
With this release, if you install a cluster on Amazon Web Services (AWS) and use the interactive installer to generate the `install-config.yaml` file, you must allow outbound access to `ec2.us-east-1.amazonaws.com` on port 443. This access is required to retrieve the list of available AWS regions during the interactive installation process.

For more information, see [Configuring your firewall](../installing/install_config/configuring-firewall.xml#configuring-firewall-module_configuring-firewall).

Installing OpenShift Container Platform in Google Cloud Dedicated regions
You can install OpenShift Container Platform in Google Cloud Dedicated (GCD) regions by using installer-provisioned infrastructure. GCD is a sovereign cloud platform that provides Google Cloud technology in a fully isolated environment with strict data and operational sovereignty guarantees. If you require strict data residency and operational control, you can deploy to sovereign cloud environments.

GCD is available from 4.22.16 and later.

For more information, see [Installing a cluster on Google Cloud Dedicated](../installing/installing_gcp/installing-gcp-dedicated.xml#installing-gcp-dedicated).

## Machine Config Operator

Overriding storage or partition setup is generally available
With this update, the overriding storage or partition setup feature is generally available. With this feature, you can change the installed disk partition schema, file systems, and RAID configurations for new nodes.

For more information, see [Overriding storage and partition setup](../machine_configuration/machine-configs-configure.xml#machine-config-install-time-configs_machine-configs-configure).

Updated boot images for AWS Marketplace now supported
Updated boot images are now supported for clusters that use AWS Marketplace boot images. With this feature, you can configure your cluster to update the node boot image whenever you update your cluster. By default, the boot image in your cluster is not updated along with your cluster.

For more information, see [Boot image management](../machine_configuration/mco-update-boot-images.xml#mco-update-boot-images).

Network policy support for the Machine Config Operator
The Machine Config Operator now has multiple network policies that control network traffic to and from the Operator and operand pods. These policies restrict traffic to only traffic that is explicitly allowed or required.

## Machine management

## Networking

Selectable HAProxy versions on Ingress Controllers
With this release, you can set `spec.haproxyVersion` on an `IngressController` custom resource to choose HAProxy 2.8 or HAProxy 3.2. Set `2.8` on OpenShift Container Platform 4.22 before you update if you need Ingress Controllers to keep HAProxy 2.8. Pin HAProxy 3.2 after you update when you want a later cluster update to keep the current default. If you set a version that a target release does not support, a preflight check blocks the cluster update until you unset the field or change it to a supported version. For more information, see [HAProxy version changes before a cluster update](../updating/preparing_for_updates/updating-cluster-prepare.xml#update-preparing-haproxy-version_updating-cluster-prepare) and [Selecting an HAProxy version](../networking/networking_operators/ingress-operator.xml#nw-selecting-haproxy-version_configuring-ingress).

HAProxy version update to 3.2.22
OpenShift Container Platform 4.17 uses HAProxy 3.2.22 as the default Ingress Controller version and includes HAProxy 2.8.27 for migration. OpenShift Container Platform 4.22 used HAProxy 2.8.18. Set `spec.haproxyVersion` to `2.8` if you need to defer HAProxy 3.2-specific behavior. HAProxy 2.8.27 still includes tighter request validation than HAProxy 2.8.18.

If Ingress Controllers use the default HAProxy 3.2.22, the following behavior changes can affect applications:

- Requests with a malformed target that does not start with `/` now receive HTTP `400` instead of being accepted.

- Requests with a comma or other disallowed characters in the `Host` header now receive HTTP `400` instead of HTTP `503` or `404`.

- Passthrough routes that use consistent-hash affinity remap backend pods one time after the update.

- Denied or redirected HTTP/1 requests no longer force `Connection: close`; keep-alive connections stay open.

- Requests that exceed header or URI size limits now return HTTP `414` or `431` instead of HTTP `400`.

- `OPTIONS` requests with an empty path keep that empty path instead of rewriting it to `/`. CORS handlers that match only `/` might stop matching.

If you pin HAProxy 2.8, Ingress Controllers run HAProxy 2.8.27. That version still rejects commas and additional disallowed characters in `Host` headers, preserves empty `OPTIONS` paths, and sanitizes inconsistent WebSocket `Upgrade` headers.

For the complete upstream change lists, see the [HAProxy 2.8 changelog](https://www.haproxy.org/download/2.8/src/CHANGELOG) and the [HAProxy 3.2 changelog](https://www.haproxy.org/download/3.2/src/CHANGELOG).

Dual stack enabled for OpenShift Container Platform clusters on Amazon Web Services (AWS)
With this update, OpenShift Container Platform clusters on Amazon Web Services (AWS) can be configured to use dual-stack networking. This allows for both IPv4 and IPv6 addresses to be used for network traffic. Currently, single stack IPv6 is not supported. For more information, see [Cluster Network Operator configuration object](../networking/networking_operators/cluster-network-operator.xml#nw-operator-cr_cluster-network-operator).

BYO security groups for AWS Network Load Balancers
The AWS Cloud Controller Manager (CCM) now supports attaching your Bring Your Own (BYO) security groups to Network Load Balancers (NLBs). The NLBs must have been created for Kubernetes `Service` resources of type `LoadBalancer`.

For more information, see [BYO security groups for AWS Network Load Balancers](../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-aws.xml#nw-ingress-aws-about-byo-security-groups_configuring-ingress-cluster-traffic-aws).

<!-- -->

High availability for PTP boundary clocks with dual time receiver ports on Intel E810 hardware
You can configure dual time receiver (TR) ports on a single Intel Westport Channel E810-XXVDA4T network interface controller (NIC) for Precision Time Protocol (PTP) Telecom Boundary Clock (T-BC) high availability. This configuration uses the Alternate Best Master Clock Algorithm (A-BMCA) to support automatic switchover between upstream paths if the active port fails or its quality degrades. As a result, downstream devices maintain continuous time synchronization without manual intervention during upstream path failures.

The `PtpConfig` custom resource (CR) uses a two-profile architecture with a time receiver profile and a time transmitter profile on separate PTP domains. Both TR ports share the same Physical Hardware Clock (PHC), so failover relies on A-BMCA reselection rather than switching between separate clock servos.

For more information, see [Configuring PTP boundary clock high availability with dual time receiver ports](../networking/advanced_networking/ptp/configuring-ptp.xml#ptp-configuring-linuxptp-services-dual-port-bc_configuring-ptp).

<!-- -->

High availability for PTP boundary clocks with dual time receiver ports on Intel Granite Rapids-D hardware (Technology Preview)
You can configure dual time receiver (TR) ports on Intel Granite Rapids-D (GNR-D) hardware, such as the Dell XR8720t with Intel E830 Carter Flat NICs, for Precision Time Protocol (PTP) Telecom Boundary Clock (T-BC) high availability. This configuration uses the Alternate Best Master Clock Algorithm (A-BMCA) to support automatic switchover between upstream paths if the active port fails or its quality degrades.

The GNR-D configuration uses a `PtpConfig` custom resource (CR) with two profiles and a `HardwareConfig` CR to define the Digital Phase-Locked Loop (DPLL) clock chain and holdover parameters.

For more information, see [Configuring linuxptp services as a boundary clock on Intel Granite Rapids-D hardware](../networking/advanced_networking/ptp/configuring-ptp.xml#ptp-configuring-linuxptp-services-as-boundary-clock-gnrd_configuring-ptp).

## Nodes

Additional CRI-O storage locations is generally available
With this update, the Additional CRI-O storage locations feature is generally available. With this feature, you can create additional, non-default artifact storage locations in CRI-O that your pods can pull from, which can reduce application startup time and make your applications run more efficiently.

For more information, see [Additional CRI-O storage locations for faster container startup](../nodes/nodes/nodes-nodes-additional-crio-storage.xml#nodes-nodes-additional-crio-storage).

Project-scoped image pull secrets for mirrored registries is generally available
With this update, the Project-scoped image pull secrets for mirrored registries feature is generally available. With this feature, you can pull images from mirrored registries by using project-scoped pull secrets rather than node-level secrets.

For more information, see [Configuring project-scoped image pull secrets for mirrored registries](../openshift_images/image-configuration.xml#images-configuration-registry-mirror-project-secret_image-configuration).

Dynamic resource allocation (DRA) improvements
With this update, the following improvements have been made to the DRA feature:

- Partitionable devices with DRA is generally available. With this update, manually partitioning physical hardware into smaller, logical instances, such as Multi-Instance GPUs, to use with dynamic resource allocation is generally available.

  For more information, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

- Consumable capacity for DRA. With this update, the consumable capacity method for DRA is available. You can share a single device, such as a GPU, among multiple independent resource claims without creating fixed partitions in advance. Each claim requests a quantity of device capacity, and the scheduler ensures that the total consumed capacity does not exceed the device’s capacity.

  As a result, workloads can use only the device capacity they need, which improves utilization of accelerators compared to exclusive allocation or predefined partitions.

  For more information, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

- Device taints and tolerations for DRA. With this update, device taints and tolerations for DRA are available. You can use your DRA driver in a resource slice to taint individual devices, such as GPUs, so that the scheduler does not place new pods on them and can remove pods that already use the devices. Cluster administrators can apply the same effect to matching devices by creating a `DeviceTaintRule` object. Workloads tolerate those taints in a resource claim, not in the pod specification.

  For more information, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

- Device binding conditions for DRA. With this update, device binding conditions for DRA are available. For devices that must be attached or prepared on a node before a pod starts, such as fabric-attached or network-attached accelerators, the scheduler waits until the device is ready instead of binding the pod immediately. DRA drivers declare the required readiness and failure conditions on the device. If the driver also requires the allocation to stay on the selected node, the scheduler records that node on the resource claim so that a controller can attach or prepare the device there.

  As a result, pods that need those devices start only after the hardware is actually available on the node, which avoids failed startups caused by devices that are still being attached.

  For more information, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

- Device health status in pod status. With this update, reporting the health of allocated DRA devices in the pod status is available. When your DRA driver reports that a device such as a GPU is unhealthy, the kubelet records that information on each container that uses the device. You can inspect the pod status to see whether an allocated device is `Healthy`, `Unhealthy`, or `Unknown`. If the driver provides extra detail, the status can also include a message that explains the health result.

  As a result, you can determine whether a failing pod is caused by the application or by the underlying device, without relying only on application logs.

  For more information, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

## OpenShift CLI (oc)

## Postinstallation configuration

## Red Hat Enterprise Linux CoreOS (RHCOS)

Red Hat Enterprise Linux CoreOS (RHCOS) now ships with the Toolbx tool for debugging
With this update, the underlying tool for debugging on Red Hat Enterprise Linux CoreOS (RHCOS) nodes is changing from the `rhcos-toolbox` script to the upstream Toolbx tool. This update simplifies the workflow for generating `sosreport` archives and other tasks. For example, you no longer need to invoke a toolbox container to generate an `sosreport` archive.

For more information, see [About Toolbx](../support/gathering-cluster-data.xml#about-toolbox_gathering-cluster-data) and [Generating a sosreport archive for an OpenShift Container Platform cluster node](../support/gathering-cluster-data.xml#support-generating-a-sosreport-archive_gathering-cluster-data).

Automatic boot loader updates on RHCOS
With this update, RHCOS automatically updates the boot loader on nodes when a node gets updated to a new operating system image. The automatic updates occur only on clusters that use the `x86_64` or ARM CPU architecture.

For UEFI systems, the `bootloader-update.service` updates the boot loader inside the EFI System Partition. For Legacy BIOS systems, the `bootloader-update.service` writes the boot loader directly to the boot sectors.

Before this change, during an operating system update the boot loader was not automatically updated. You needed to manually run the `bootupctl update` command or apply a machine config to update the boot loader.

As a result of this change, the boot loader stays in sync with the RHCOS version on the node.

For more information on manually updating the boot loader, see [Updating the boot loader on RHCOS nodes using bootupd](../updating/updating_a_cluster/updating-bootloader-rhcos.xml#updating-bootloader-rhcos).

## Scalability and performance

OVS-DPDK CPU reservation (Technology Preview)
With this release, you can reserve CPUs for Open vSwitch Data Plane Development Kit (OVS-DPDK) poll mode driver (PMD) threads by setting `spec.cpu.ovsDpdk` in a `PerformanceProfile` custom resource. The Node Tuning Operator applies multi-layer CPU isolation so that those host-side threads are protected from interference from the operating system, interrupts, and Kubernetes scheduling. This capability is a Technology Preview feature.

For more information, see [Reserving CPUs for OVS-DPDK](../scalability_and_performance/cnf-reserving-cpus-for-ovs-dpdk.xml#cnf-reserving-cpus-for-ovs-dpdk).

## Edge computing

Virtualized control planes with KubeVirt Redfish is generally available
With this update, deploying virtualized control planes with KubeVirt Redfish is generally available.

This update also adds `bcrypt` hashed passwords for more secure authentication to the KubeVirt Redfish API.

For more information about virtualized control planes, see [Understanding virtualized control planes](../vcp/vcp-overview.xml#vcp-overview).

## Support

## Storage

CSI volume group snapshots is generally available
Container Storage Interface (CSI) volume group snapshots use a label selector to group multiple persistent volume claims (PVCs) for snapshotting. A volume group snapshot represents copies from multiple volumes that are taken at the same point-in-time. This can be useful for applications that contain multiple volumes. This feature needs to be supported by the CSI driver.

OpenShift Data Foundation supports volume group snapshots.

OpenShift Container Platform 4.18 introduced CSI volume group snapshots as a Technology Preview feature. OpenShift Container Platform 5.0 supports this feature as generally available.

For more information about CSI volume group snapshots, see [CSI volume group snapshots](../storage/container_storage_interface/persistent-storage-csi-group-snapshots.xml#persistent-storage-csi-group-snapshots).

Changed block tracking (Technology Preview)
Container Storage Interface (CSI) Changed block tracking (CBT) enables compatible backup applications to identify block ranges that changed between two snapshots of the same underlying CSI block-storage volume.

Backup applications can use changed-block metadata to reduce the data read and transferred for incremental backups. The API can also identify allocated block ranges in a single snapshot, allowing backup applications to skip unallocated ranges when creating a full backup of that snapshot. These operations return metadata, not the snapshot data itself. The backup application reads and backs up the relevant data separately.

CBT was introduced in OpenShift Container Platform 4.20 as Developer Preview. For 5.0, it is supported as Technology Preview.

CBT requires support from both the CSI driver and the backup application.

For more information about CBT, see the Red Hat Knowledgebase solution [How to use Changed Block Tracking (Tech Preview) in OpenShift 5.0](https://access.redhat.com/solutions/7146879)

Upcoming SELinux mount option default for RWO/RWX volumes
For OpenShift Container Platform 5.0, ReadWriteOnce (RWO) and ReadWriteMany (RWX) volumes use recursive relabeling by default. However, OpenShift Container Platform 5.1 is targeted to have RWO and RWX volumes use mount option by default.

Some pods might not start when SELinux mount option behavior is applied.

To prepare for a future upgrade to 5.1, cluster administrators **must** do one of the following or the upgrade will be blocked:

- Fix your applications, so that the upgrade is safe.

  OpenShift Container Platform reports SELinux-related conflicts when creating pods, and on running pods, to make you aware of potential conflicts, and to help you resolve them. For more information about this reporting, see the Red Hat Knowledgebase article [OpenShift reports alert SELinuxMountGAReadinessWorkloadsDetected and the cluster is not upgradeable. (Red Hat Knowledgebase)](https://access.redhat.com/solutions/7146569).

- Opt-out from the new default behavior, per pod or namespace.

  If you are unable to resolve the SELinux-related conflicts, you can proactively opt-out of the future move to mount option as default for selected pods or namespaces. To opt out, see [Opting out of the SELinux mount option default](../storage/understanding-persistent-storage.xml#using_selinuxChangePolicy_pod-opt-out_understanding-persistent-storage).

For more information about SELinux mount option for RWO/RWX, see [RWO and RWX and SELinux mount option](../storage/understanding-persistent-storage.xml#using_selinuxChangePolicy_overview-mount-option-rwo-rwx_understanding-persistent-storage).

## Web console

# Notable technical changes

This section includes several technical changes for OpenShift Container Platform 4.17.

# Deprecated and removed features

## Images deprecated and removed features

| Feature                  | 4.21       | 4.22       | 5.0        |
|--------------------------|------------|------------|------------|
| Cluster Samples Operator | Deprecated | Deprecated | Deprecated |

Images deprecated and removed tracker

## Installation deprecated and removed features

| Feature                                                                                                                | 4.21       | 4.22       | 5.0        |
|------------------------------------------------------------------------------------------------------------------------|------------|------------|------------|
| `--cloud` parameter for `oc adm release extract`                                                                       | Deprecated | Deprecated | Deprecated |
| CoreDNS wildcard queries for the `cluster.local` domain                                                                | Deprecated | Deprecated | Deprecated |
| `compute.platform.openstack.rootVolume.type` for RHOSP                                                                 | Deprecated | Deprecated | Deprecated |
| `controlPlane.platform.openstack.rootVolume.type` for RHOSP                                                            | Deprecated | Deprecated | Deprecated |
| `ingressVIP` and `apiVIP` settings in the `install-config.yaml` file for installer-provisioned infrastructure clusters | Deprecated | Deprecated | Deprecated |
| `platform.aws.preserveBootstrapIgnition` parameter for Amazon Web Services (AWS)                                       | Deprecated | Deprecated | Deprecated |
| Installing a cluster on AWS with compute nodes in AWS Outposts                                                         | Deprecated | Deprecated | Deprecated |
| Installing a cluster using Fujitsu iRMC drivers on bare-metal machines                                                 | Deprecated | Deprecated | Deprecated |

Installation deprecated and removed tracker

## Machine Management deprecated and removed features

| Feature                                                                          | 4.21       | 4.22       | 5.0        |
|----------------------------------------------------------------------------------|------------|------------|------------|
| Confidential Computing with AMD Secure Encrypted Virtualization for Google Cloud | Deprecated | Deprecated | Deprecated |
| Managing bare-metal machines using Fujitsu iRMC drivers                          | Deprecated | Deprecated | Deprecated |

Machine management deprecated and removed tracker

## Networking deprecated and removed features

| Feature  | 4.21       | 4.22       | 5.0        |
|----------|------------|------------|------------|
| iptables | Deprecated | Deprecated | Deprecated |

Networking deprecated and removed tracker

## Node deprecated and removed features

| Feature                                                              | 4.21                 | 4.22       | 5.0        |
|----------------------------------------------------------------------|----------------------|------------|------------|
| `ImageContentSourcePolicy` (ICSP) objects                            | Deprecated           | Deprecated | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/zone`   | Deprecated           | Deprecated | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/region` | Deprecated           | Deprecated | Deprecated |
| Dynamic Accelerator Slicer (DAS) Operator                            | Technology Preview   | Removed    | Removed    |
| runC container runtime                                               | General Availability | Deprecated | Deprecated |

Node deprecated and removed tracker

## OpenShift CLI (oc) deprecated and removed features

| Feature                         | 4.21                 | 4.22       | 5.0        |
|---------------------------------|----------------------|------------|------------|
| oc-mirror plugin v1             | Deprecated           | Deprecated | Deprecated |
| Docker v2 registries            | Deprecated           | Deprecated | Deprecated |
| `oc adm release mirror` command | General Availability | Deprecated | Deprecated |

OpenShift CLI (oc) deprecated and removed tracker

## Operator lifecycle and development deprecated and removed features

| Feature                                      | 4.21       | 4.22       | 5.0        |
|----------------------------------------------|------------|------------|------------|
| Red Hat Marketplace                          | Deprecated | Removed    | Removed    |
| SQLite database format for Operator catalogs | Deprecated | Deprecated | Deprecated |

Operator lifecycle and development deprecated and removed tracker

## Web console deprecated and removed features

| Feature                                | 4.21       | 4.22       | 5.0        |
|----------------------------------------|------------|------------|------------|
| `useModal` hook for dynamic plugin SDK | Deprecated | Deprecated | Deprecated |

Web console deprecated and removed tracker

## Workloads deprecated and removed features

| Feature                    | 4.21       | 4.22       | 5.0        |
|----------------------------|------------|------------|------------|
| `DeploymentConfig` objects | Deprecated | Deprecated | Deprecated |

Workloads deprecated and removed tracker

## Edge computing deprecated and removed features

| Feature                                                 | 4.21                 | 4.22                 | 5.0        |
|---------------------------------------------------------|----------------------|----------------------|------------|
| `PolicyGenTemplate` CR for GitOps ZTP policy management | General Availability | General Availability | Deprecated |

Edge computing deprecated and removed tracker

# Deprecated features

Deprecation of Fujitsu Integrated Remote Management Controller (iRMC) driver for bare-metal machines
As of OpenShift Container Platform 4.21, support for the Fujitsu iRMC baseboard management controller (BMC) driver has been deprecated and will be removed in a future release. If a `BareMetalHost` resource contains a BMC address with `irmc://` as its URI scheme, the resource must be updated to use another BMC scheme, such as `redfish://` or `ipmi://`. Once support for this driver is removed, hosts that use `irmc://` URI schemes will become unmanageable.

For information about updating the `BareMetalHost` resource, see [Editing a BareMetalHost resource](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#bmo-editing-a-baremetalhost-resource_bare-metal-postinstallation-configuration).

Deprecation of the `oc adm release mirror` command
As of OpenShift Container Platform 4.22, using the `oc adm release mirror` command to mirror release images has been deprecated and will be removed in a future release.

As an alternative, use the [oc-mirror plugin v2](../disconnected/oc_mirror_v2/about-installing-oc-mirror-v2.xml#about-installing-oc-mirror-v2).

Deprecation of adding kernel modules to nodes with KVC
As of OpenShift Container Platform 4.22, support for adding kernel modules to nodes with kmods-via-containers software (KVC) has been deprecated and will be removed in a future release.

Deprecation of the runC container runtime
As of OpenShift Container Platform 4.22, support for using the runC container runtime is deprecated and will be removed in a future release.

`PolicyGenTemplate` CR for GitOps ZTP policy management is deprecated
As of OpenShift Container Platform 5.0, the `PolicyGenTemplate` custom resource (CR) and the corresponding Kustomize plugin are deprecated and will be removed in a future release. The `PolicyGenTemplate` CR and corresponding Kustomize plugin generate and deploy policies for managed clusters in GitOps Zero Touch Provisioning (ZTP) deployments. You can manage and deploy policies by using `PolicyGenerator` CRs instead.

For more information, see [Configuring managed cluster policies by using PolicyGenerator resources](../edge_computing/policygenerator_for_ztp/ztp-configuring-managed-clusters-policygenerator.xml#ztp-configuring-managed-clusters-policygenerator).

# Removed features

This section includes removed features for OpenShift Container Platform 4.17.

## The adding kernel modules to nodes with kvc feature is removed

The adding kernel modules to nodes with kvc feature was deprecated in OpenShift Container Platform 4.22, and is now removed from OpenShift Container Platform 5.0.

# Fixed issues

The following issues are fixed for this release:

## API Server and Authentication

## Bare Metal Hardware Provisioning

- Before this update, the `baremetal` cluster Operator did not set its `Progressing` status condition to `True` during cluster upgrades. As a consequence, the Cluster Version Operator (CVO) waited for the Operator without receiving proper progress signals, and upgrade monitoring tests failed. With this release, the `baremetal` Operator correctly reports `Progressing=True` during version changes. As a result, cluster upgrades proceed with accurate Operator status reporting. ([OCPBUGS-66101](https://redhat.atlassian.net/browse/OCPBUGS-66101))

- Before this update, when the bare-metal host (BMH) `spec.online` parameter was set to `False`, the Bare Metal Operator (BMO) forced the `ironic` service to issue a power-off command to the node at the end of inspection, after the ramdisk had been ejected. As a consequence, the node operating system lost access to the boot media during shutdown, and filesystem corruption errors were visible on the BMH console. With this release, the node is powered off after inspection, while cleaning up the ramdisk, before ejecting Redfish virtual media. As a result, the host does not lose access to the boot media. ([OCPBUGS-66156](https://redhat.atlassian.net/browse/OCPBUGS-66156))

- Before this update, the Bare Metal Operator (BMO) `getChecksum()` function accepted non-empty checksums for Oracle Cloud Infrastructure (OCI) images. As a consequence, OCI image provisioning failed. With this release, a check in the `getChecksum()` function rejects non-empty user-provided checksums for OCI images. As a result, OCI image provisioning does not fail. ([OCPBUGS-84305](https://redhat.atlassian.net/browse/OCPBUGS-84305))

- Before this update, when managing a high volume of `BareMetalHost` resources on a single multicluster engine instance, the Bare Metal Operator (BMO) issued excessive requests to the Provisioner API during reconciliation. As a consequence, VirtualMedia injection and node reconciliation were noticeably slower at this scale. With this release, the BMO reconciliation loop is optimized to issue fewer requests to the Provisioner API. As a result, responsiveness improves when managing large numbers of `BareMetalHost` resources. ([OCPBUGS-85527](https://redhat.atlassian.net/browse/OCPBUGS-85527))

- Before this update, when servicing a bare-metal host (BMH), the `service_disable_ramdisk` parameter remained set to `False` even if all servicing steps were performed out-of-band. As a result, the BMH underwent an unnecessary reboot. With this release, the `ironic` service code has been modified to automatically set `service_disable_ramdisk` to `True` when all servicing steps are out-of-band. ([OCPBUGS-85528](https://redhat.atlassian.net/browse/OCPBUGS-85528))

- Before this update, the `ironic-agent` container image was missing the `iproute` package at runtime, which provides the `ip` command required for network configuration. As a consequence, the Ironic Python Agent (IPA) failed to heartbeat to the `ironic` service during bare-metal node cleaning, and node cleaning operations timed out. With this release, the `ironic-agent` container image build process is updated to retain required packages such as `iproute` and `psmisc`. As a result, IPA completes network configuration successfully and bare-metal node cleaning operations complete without timing out. ([OCPBUGS-94115](https://redhat.atlassian.net/browse/OCPBUGS-94115))

- Before this update, bare-metal nodes provisioned through virtual media failed to boot the inspection image because of incorrect kernel arguments in the provisioning ISO. As a consequence, soft lockups occurred on some hardware, for example, Fujitsu PRIMERGY M8, because the `{{console=ttyS0}}` parameter lacked baud rate and parity settings. The `{{ip=dhcp}}` parameter was missing, which prevented network acquisition during early boot. With this release, the provisioning ISO includes the `{{ip=dhcp}}` parameter and specifies the full serial console configuration. As a result, bare-metal Installer-provisioned installations complete without manual intervention. ([OCPBUGS-98696](https://redhat.atlassian.net/browse/OCPBUGS-98696))

- Before this update, the Bare Metal Operator (BMO) did not set the `IRONIC_INSECURE` function. As a consequence, bare-metal host (BMH) provisioning failed. With this release, the BMO correctly sets the `IRONIC_INSECURE` function. As a result, BMH provisioning succeeds. ([OCPBUGS-111889](https://redhat.atlassian.net/browse/OCPBUGS-111889))

## Cloud Compute

- Before this update, the `AWSMachine` controller was requeuing machine instances before confirming the presence of tags. As a consequence, duplicate Amazon Web Services (AWS) EC2 instances were created. With this release, the `AWSMachine` controller verifies tags before requeuing instances. As a result, duplicate EC2 instances are not created. ([OCPBUGS-62985](https://redhat.atlassian.net/browse/OCPBUGS-62985))

- Before this update, if an OpenStack cloud provider lacked the optional Standard Attributes Tag extension, the Machine API Provider for OpenStack (MAPO) attempted to apply port tags during network port creation. As a consequence, provisioning failed. With this release, MAPO checks whether the `standard-attr-tag` extension is available before applying tags. If unsupported, MAPO skips tag assignment or returns an error prompting you to remove explicit configurations. As a result, machine provisioning completes successfully. ([OCPBUGS-77061](https://redhat.atlassian.net/browse/OCPBUGS-77061))

## Cloud Credential Operator

- Before this update, when the Cloud Credential Operator (CCO) ran in manual mode on OpenShift Container Platform clusters configured to use Amazon Web Services (AWS) Security Token Service (STS), the Operator repeatedly attempted to reconcile `CredentialsRequest` resources for cluster Operators. As a consequence, unnecessary log messages were generated. With this update, the Operator recognizes externally managed secrets and skips unnecessary reconciliation. ([OCPBUGS-33994](https://redhat.atlassian.net/browse/OCPBUGS-33994))

## Cluster Autoscaler

## Cluster Version Operator

- Before this update, when a HostedCluster `spec.configuration.proxy` setting was scoped to data-plane components in 4.18, the Cluster Version Operator (CVO) was not updated to ignore that proxy configuration on hosted control planes. As a consequence, update advice retrieval was blocked when incompatible with the management cluster network. With this release, the CVO ignores hosted proxy configurations. As a result, egress to update services is successful. ([OCPBUGS-79358](https://redhat.atlassian.net/browse/OCPBUGS-79358))

## etcd

- Before this update, an upgrade with a control plane `MachineConfig` might have caused quorum loss. As a consequence, the upgrade caused prolonged API and etcd downtime, leading to service interruption. With this release, the `cluster-etcd-operator` keeps guard pods that prevent a `MachineConfig` object from draining the node. As a result, etcd maintains quorum during upgrades. ([OCPBUGS-66334](https://redhat.atlassian.net/browse/OCPBUGS-66334))

## Helm

- Before this update, installing a Helm chart by using the Chart URL option in the OpenShift Container Platform web console with an Oracle® Cloud Infrastructure (OCI) URL that included a version number, for example, `oci://registry-1.docker.io/bitnamicharts/nginx:22.6.12` failed with an error indicating that the chart was not available or could not be found. As a consequence, users could not install Helm charts from OCI registries when specifying the version number directly in the URL. With this release, the Helm chart installation process correctly handles OCI URLs that include version numbers. As a result, users can now successfully install Helm charts from OCI registries by providing the complete URL with the version number in the web console Chart URL field.

## Hosted Control Planes

- Before this update, KubeVirt-based `NodePool` resources incorrectly reported `ClusterNetworkCIDRConflict` errors because the controller flagged OVN-Kubernetes internal overlay IP addresses as conflicting with the cluster network. With this release, Classless Inter-Domain Routing (CIDR) conflict detection is triggered only when all the non-link local addresses for the machine fall within the cluster network. As a result, when external addresses exist, in-network addresses are correctly treated as expected container network interface (CNI) internal IP addresses, which prevents false positive conflict reports. ([OCPBUGS-84269](https://redhat.atlassian.net/browse/OCPBUGS-84269))

- Before this update, applying resource overrides to containers without pre-existing resource requests caused a nil map panic and crash loop. With this release, a nil guard is added to the `applyRequestsOverrides` function in the Control Plane Operator (CPO) before calling `maps.Copy` on the `Resources.Requests` parameter. As a result, resource request overrides are successfully applied regardless of pre-existing requests. ([OCPBUGS-93785](https://redhat.atlassian.net/browse/OCPBUGS-93785))

- Before this update, the Konnectivity proxy-server in the `kube-apiserver` deployment was not configured with the `--cluster-ca-cert` flag. As a consequence, a reachable client could establish a connection to the Konnectivity proxy-server without a valid client certificate signed by the hosted cluster Konnectivity certification authority (CA). With this release, the `--cluster-ca-cert` flag is added to the `konnectivity-server` container arguments in the `kube-apiserver` deployment manifest. As a result, unauthenticated connections are prevented because the proxy-server requires and validates client certificates signed by the hosted cluster Konnectivity CA. ([OCPBUGS-99014](https://redhat.atlassian.net/browse/OCPBUGS-99014))

## Installer

## Kube API Server

## Kube Storage Version Migrator

## Machine Config Operator

## Management Console

## Monitoring

- Before this update, when Prometheus compacted time series data, it attempted to enable direct I/O on files that were already open. Some file systems, such as IBM Storage Scale, do not support this operation. As a consequence, compaction failed with a `cannot enable Direct IO: invalid argument` error, Prometheus could not write chunks to disk, and memory usage in Prometheus pods increased until the pods hit their memory limits and restarted or affected other workloads on the node. With this release, Prometheus detects when a file system does not support direct I/O on open files and handles the condition gracefully. As a result, Prometheus writes chunks to disk and completes compaction successfully on these storage back ends. ([OCPBUGS-92191](https://redhat.atlassian.net/browse/OCPBUGS-92191))

- Before this update, the Cluster Monitoring Operator (CMO) checked only the `openshift-config/pull-secret` for the `cloud.openshift.com` authentication token used by the telemeter client. As a consequence, on platforms where this secret did not contain the token, such as the Microsoft Azure Red Hat OpenShift hosted control planes, the telemeter client was not deployed, which prevented cluster registration in Red Hat OpenShift Cluster Manager. With this release, the CMO falls back to `kube-system/global-pull-secret` if the token is not found in the primary secret. As a result, the telemeter client is deployed correctly. ([OCPBUGS-98450](https://redhat.atlassian.net/browse/OCPBUGS-98450))

- Before this update, Alertmanager crashed because the `tzdata` package was missing in the OpenShift Container Platform base images, This issue caused the absence of the `/usr/share/zoneinfo` directory. As a consequence, Alertmanager pods failed to start, which made time-based alerts inaccessible for the time zones. With this release, the `tzdata` package has been reinstated in OpenShift Container Platform images. As a result, Alertmanager does not crash on startup when location fields are present in the `active_interval` or `mute_interval` entries. ([OCPBUGS-99435](https://redhat.atlassian.net/browse/OCPBUGS-99435))

- Before this update, containers in the `openshift-monitoring` namespace ran with writable root filesystems because `readOnlyRootFilesystem: true` was not enabled in their security contexts. As a consequence, customer compliance scans flagged these containers as security policy violations. With this release, monitoring components enable read-only root filesystems with dedicated `emptyDir` volumes for paths requiring write access. As a result, monitoring containers meet compliance requirements for read-only root filesystems. ([OCPBUGS-105389](https://redhat.atlassian.net/browse/OCPBUGS-105389))

- Before this update, Fibre Channel adapters reported incomplete data. As a consequence, the node_exporter failed to run. With this release, guards are added to ignore incomplete data. ([OCPBUGS-112719](https://redhat.atlassian.net/browse/OCPBUGS-112719))

## Networking

## Node

## Node Tuning Operator

- Before this update, a failure to update the `PerformanceProfile` status due to a temporarily unavailable API server during an upgrade or under network load could leave the profile in a `Degraded` condition. As a consequence, the degraded condition might stop and never resolve, even after the cluster returned to a healthy state, because the Operator did not retry until the next reconcile event. With this release, the Operator schedules a retry of the status update until it succeeds, retrying approximately every 30 seconds. As a result, the stopped degraded status is temporary and resolves automatically during the next retry. ([OCPBUGS-62277](https://issues.redhat.com/browse/OCPBUGS-62277))

- Before this update, the Node Tuning Operator (NTO) reconciliation used the rate-limited work queue for all event enqueues. As a consequence, node-tuning configuration was delayed for cluster notes greater than 100. With this release, the NTO reconciliation loop uses the rate-limited work queue only for failures instead of all event enqueues. As a result, node-tuning configuration for cluster nodes greater than 100 is not delayed. ([OCPBUGS-112279](https://issues.redhat.com/browse/OCPBUGS-112279))

- Before this update, the short description for the `info` command in the Performance Profile Creator (PPC) tool was not updated after the cluster inspection was moved. As a consequence, inconsistencies between the parent help and the information help occurred when you ran the PPC tool. With this release, the short description for the `info` command in the PPC tool is updated to match the current CLI. As a result, the help inconsistencies do not occur when you run the tool. ([OCPBUGS-114144](https://issues.redhat.com/browse/OCPBUGS-114144))

- Before this update, you were required to enable timer migration to prevent TCP and other leftover timers from interfering with latency-sensitive workloads. As a consequence, this migration increased latency for high-resolution timers and disrupted benchmarks such as the `cyclictest` tool. With this release, the improved timer wheel logic in Red Hat Enterprise Linux (RHEL) 10 allows you to disable timer migration. As a result, both polling and high-resolution timer latency-sensitive workloads run without interruption from leftover timers. ([OCPBUGS-114934](https://issues.redhat.com/browse/OCPBUGS-114934))

## Observability

## oc

## oc-mirror

## OLM

- Before this update, startup delays caused some health probes for Operator Lifecycle Manager (OLM) Classic catalog source pods to time out. As a consequence, this delay triggered pod restarts. With this release, Kubernetes gRPC probes avoid starting a process inside the container, which prevents these timeouts. ([OCPBUGS-74905](https://redhat.atlassian.net/browse/OCPBUGS-74905))

- Before this update, Operator Lifecycle Manager (OLM) v1 installations of Operators with webhooks sometimes stalled while waiting for serving certificates. With this release, certificate creation starts earlier, which reduces these installation delays. ([OCPBUGS-81452](https://redhat.atlassian.net/browse/OCPBUGS-81452))

- Before this update, the catalog endpoint provided by Operator Lifecycle Manager (OLM) v1 ignored TLS profile settings. With this release, the endpoint honors the configured minimum TLS version and cipher suites. ([OCPBUGS-86797](https://redhat.atlassian.net/browse/OCPBUGS-86797))

- Before this update, the metrics server in Operator Lifecycle Manager (OLM) v1 used default TLS settings instead of the TLS profile for the cluster. With this release, the metrics server follows the TLS profile and applies profile changes. ([OCPBUGS-88736](https://redhat.atlassian.net/browse/OCPBUGS-88736))

- Before this update, the package server in Operator Lifecycle Manager (OLM) Classic ignored the TLS profile for the cluster. With this release, the package server honors the configured minimum TLS version and cipher suites. ([OCPBUGS-88737](https://redhat.atlassian.net/browse/OCPBUGS-88737))

- Before this update, the Operator Lifecycle Manager (OLM) Classic package server on hosted control planes ignored the TLS profile for the hosted cluster. With this release, the package server follows the TLS settings for the hosted cluster. ([OCPBUGS-98575](https://redhat.atlassian.net/browse/OCPBUGS-98575))

## OpenShift API Server

- Before this update, the `openshift-apiserver` might have failed when multiple requests accessed project authorization data at the same time. This issue occurred more often on clusters with many namespaces and role-based access control (RBAC) rules. As a consequence, `openshift-apiserver` pods restarted unexpectedly with exit code `2`, which temporarily disrupted the API availability for project and namespace operations. With this release, the project authorization cache safely handles concurrent access. As a result, the `openshift-apiserver` namespace does not fail during concurrent project authorization lookups, and project listing operations remain responsive regardless of cluster size. ([OCPBUGS-84534](https://redhat.atlassian.net/browse/OCPBUGS-84534))

## Pod Autoscaler

- Before this update, by default, the Vertical Pod Autoscaler (VPA) Operator required a control plane node for running workloads. As a consequence, it caused issues in single-node deployments. With this release, the Operator is updated to support deployment without control plane node requirements. As a result, the VPA Operator functions correctly in single-node configurations. ([OCPBUGS-42343](https://redhat.atlassian.net/browse/OCPBUGS-42343))

## Storage

## Virtualization

- Before this update, the Hosted Cluster Config Operator (HCCO) machine controller included all CAPI machine internal IP addresses in EndpointSlice endpoints without filtering, including link-local addresses such as `169.254.0.2` and `fe80::*`. Because Kubernetes 1.33 added validation that rejects link-local addresses in EndpointSlice endpoints, the HCCO failed to create or update EndpointSlice endpoints for 'kubevirt\` guest cluster `LoadBalancer` shadow services on the management cluster. As a consequence, user-created `LoadBalancer` services in hosted clusters deployed with the `kubevirt` provider did not contain EndpointSlice endpoints or backends, which caused connection attempts from the management cluster to fail with "Connection refused" errors. With this release, the HCCO filters out link-local addresses from machine addresses before creating EndpointSlice endpoints. As a result, EndpointSlice endpoints are created successfully for all shadow services, and `LoadBalancer` services in `kubevirt`-based hosted clusters can be accessed from pods on the management cluster. ([OCPBUGS-83604](https://redhat.atlassian.net/browse/OCPBUGS-83604))

## Web console

# Technology Preview features status

Some features in this release are currently in Technology Preview. These experimental features are not intended for production use. Note the following scope of support on the Red Hat Customer Portal for these features:

[Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview)

In the following tables, features are marked with the following statuses:

- *Not Available*

- *Technology Preview*

- *General Availability*

- *Deprecated*

- *Removed*

## AI applications Technology Preview features

| Feature                                             | 4.21          | 4.22               | 5.0                |
|-----------------------------------------------------|---------------|--------------------|--------------------|
| MCP server for Red Hat OpenShift Container Platform | Not Available | Technology Preview | Technology Preview |

AI applications Technology Preview tracker

## Authentication and authorization Technology Preview features

| Feature                                       | 4.21               | 4.22               | 5.0                  |
|-----------------------------------------------|--------------------|--------------------|----------------------|
| Advanced direct authentication fields         | Technology Preview | Technology Preview | General Availability |
| Pod security admission restricted enforcement | Technology Preview | Technology Preview | Technology Preview   |

Authentication and authorization Technology Preview tracker

## Edge computing Technology Preview features

| Feature                                                                  | 4.21                 | 4.22                 | 5.0                  |
|--------------------------------------------------------------------------|----------------------|----------------------|----------------------|
| Accelerated provisioning of GitOps ZTP                                   | Technology Preview   | Technology Preview   | Technology Preview   |
| Enabling disk encryption with TPM and PCR protection                     | Technology Preview   | Technology Preview   | Technology Preview   |
| Configuring a local arbiter node                                         | General Availability | General Availability | General Availability |
| Configuring a two-node OpenShift Container Platform cluster with fencing | Technology Preview   | General Availability | General Availability |

Edge computing Technology Preview tracker

## Extensions Technology Preview features

| Feature                                                                 | 4.21                 | 4.22                 | 5.0                  |
|-------------------------------------------------------------------------|----------------------|----------------------|----------------------|
| OLM v1 runtime validation of container images using sigstore signatures | Technology Preview   | General Availability | General Availability |
| OLM v1 permissions preflight check for cluster extensions               | Technology Preview   | Technology Preview   | Technology Preview   |
| OLM v1 deploying a cluster extension in a specified namespace           | Technology Preview   | Technology Preview   | Technology Preview   |
| OLM v1 deploying a cluster extension that uses webhooks                 | General Availability | General Availability | General Availability |
| OLM v1 software catalog                                                 | Technology Preview   | Technology Preview   | Technology Preview   |
| OLM v1 `deploymentConfig` API for cluster extension customization       | Not Available        | Technology Preview   | Technology Preview   |

Extensions Technology Preview tracker

## Installation Technology Preview features

| Feature                                                                                   | 4.21                 | 4.22                                                         | 5.0                                                          |
|-------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| Installing a cluster on Alibaba Cloud by using Assisted Installer                         | Technology Preview   | Technology Preview                                           | Technology Preview                                           |
| Installing a cluster using Red Hat Enterprise Linux (RHEL) 10                             | Not Available        | Technology Preview                                           | Technology Preview                                           |
| Dedicated disk for etcd on Microsoft Azure                                                | Technology Preview   | Technology Preview                                           | Technology Preview                                           |
| Mount shared entitlements in BuildConfigs in RHEL                                         | Technology Preview   | General Availability (through Builds for OpenShift Operator) | General Availability (through Builds for OpenShift Operator) |
| OpenShift zones support for vSphere host groups                                           | Technology Preview   | General Availability                                         | General Availability                                         |
| Selectable Cluster Inventory                                                              |                      |                                                              |                                                              |
| Enabling a user-provisioned DNS on Google Cloud                                           | General Availability | General Availability                                         | General Availability                                         |
| Enabling a user-provisioned DNS on Microsoft Azure                                        | Technology Preview   | General Availability                                         | General Availability                                         |
| Enabling a user-provisioned DNS on Amazon Web Services (AWS)                              | Technology Preview   | Technology Preview                                           | General Availability                                         |
| Installing a cluster using Google Cloud private and restricted API endpoints              | General Availability | General Availability                                         | General Availability                                         |
| Installing a cluster on VMware vSphere with multiple network interface controllers        | General Availability | General Availability                                         | General Availability                                         |
| Red Hat Bare-Metal-as-a-Service for OpenShift (formerly known as bare metal as a service) | Technology Preview   | General Availability                                         | General Availability                                         |
| Installing a cluster on Amazon Web Services (AWS) European Sovereign Cloud                | Not Available        | Technology Preview                                           | Technology Preview                                           |
| Installing a cluster on Amazon Web Services (AWS) with dual-stack networking              | Not Available        | Technology Preview                                           | Technology Preview                                           |
| Running firmware upgrades for hosts in deployed bare metal clusters                       | General Availability | General Availability                                         | General Availability                                         |
| Changing the CVO log level                                                                | Technology Preview   | Technology Preview                                           | Technology Preview                                           |
| Deploying virtualized control planes with KubeVirt Redfish                                | Not Available        | Technology Preview                                           | General Availability                                         |

Installation Technology Preview tracker

<div class="note">

Fleet Management supersedes Selectable Cluster Inventory in OpenShift Container Platform 4.20 and later releases. For more information see, the Red Hat Advanced Cluster Management for Kubernetes documentation for [Fleet Management](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.15/html-single/release_notes/index#console-new-features).

</div>

## Machine Config Operator Technology Preview features

| Feature                                                | 4.21               | 4.22                 | 5.0                  |
|--------------------------------------------------------|--------------------|----------------------|----------------------|
| Boot image management for control plane nodes          | Technology Preview | General Availability | General Availability |
| Image mode for OpenShift status reporting improvements | Technology Preview | Technology Preview   | Technology Preview   |
| Overriding storage or partition setup                  | Technology Preview | Technology Preview   | General Availability |

Machine Config Operator Technology Preview tracker

## Machine management Technology Preview features

| Feature                                                                                     | 4.21               | 4.22               | 5.0                |
|---------------------------------------------------------------------------------------------|--------------------|--------------------|--------------------|
| Managing machines with the Cluster API for Amazon Web Services                              | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for Google Cloud                                     | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for IBM Power® Virtual Server                        | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for Microsoft Azure                                  | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for RHOSP                                            | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for VMware vSphere                                   | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for bare metal                                       | Technology Preview | Technology Preview | Technology Preview |
| Cloud controller manager for IBM Power® Virtual Server                                      | Technology Preview | Technology Preview | Technology Preview |
| Adding multiple subnets to an existing VMware vSphere cluster by using compute machine sets | Technology Preview | Technology Preview | Technology Preview |
| Bare-metal nodes on VMware vSphere clusters                                                 | Technology Preview | Technology Preview | Technology Preview |
| Amazon Web Services Dedicated Host support                                                  | Not Available      | Technology Preview | Technology Preview |

Machine management Technology Preview tracker

## Multi-Architecture Technology Preview features

| Feature                                                       | 4.21                 | 4.22                 | 5.0                  |
|---------------------------------------------------------------|----------------------|----------------------|----------------------|
| `kdump` on `arm64` architecture                               | General Availability | General Availability | General Availability |
| `kdump` on `s390x` architecture                               | General Availability | General Availability | General Availability |
| `kdump` on `ppc64le` architecture                             | General Availability | General Availability | General Availability |
| Support for configuring the image stream import mode behavior | Technology Preview   | Technology Preview   | Technology Preview   |

Multi-Architecture Technology Preview tracker

## Networking Technology Preview features

| Feature                                                                                                             | 4.21                 | 4.22                 | 5.0                  |
|---------------------------------------------------------------------------------------------------------------------|----------------------|----------------------|----------------------|
| eBPF manager Operator                                                                                               | Technology Preview   | Technology Preview   | Technology Preview   |
| Advertise using L2 mode the MetalLB service from a subset of nodes, using a specific pool of IP addresses           | Technology Preview   | Technology Preview   | Technology Preview   |
| Updating the interface-specific safe sysctls list                                                                   | Technology Preview   | Technology Preview   | Technology Preview   |
| Egress service custom resource                                                                                      | Technology Preview   | Technology Preview   | Technology Preview   |
| VRF specification in `BGPPeer` custom resource                                                                      | Technology Preview   | Technology Preview   | Technology Preview   |
| OVN-Kubernetes customized `br-ex` bridge on vSphere and RHOSP                                                       | Technology Preview   | Technology Preview   | Technology Preview   |
| Live migration to OVN-Kubernetes from OpenShift Container Platform SDN                                              | Not Available        | Not Available        | Not Available        |
| Dynamic configuration manager                                                                                       | Technology Preview   | Technology Preview   | Technology Preview   |
| SR-IOV Network Operator support for Intel C741 Emmitsburg Chipset                                                   | Technology Preview   | General Availability | General Availability |
| Dual-port NIC for PTP ordinary clock                                                                                | General Availability | General Availability | General Availability |
| DPU Operator                                                                                                        | Technology Preview   | Technology Preview   | Technology Preview   |
| Fast IPAM for the Whereabouts IPAM CNI plugin                                                                       | Technology Preview   | Technology Preview   | Technology Preview   |
| Unnumbered BGP peering                                                                                              | General Availability | General Availability | General Availability |
| Load balancing across the aggregated bonded interface with xmitHashPolicy                                           | Technology Preview   | Technology Preview   | General Availability |
| PF Status Relay Operator for high availability with SR-IOV networks                                                 | Technology Preview   | Technology Preview   | Technology Preview   |
| Preconfigured user-defined network end points using MTV                                                             | Technology Preview   | Technology Preview   | Technology Preview   |
| Unassisted holdover for PTP devices                                                                                 | General Availability | General Availability | General Availability |
| No-overlay mode with BGP routing                                                                                    | Not Available        | Technology Preview   | Technology Preview   |
| Configuring GNR-D T-BC holdover on a GNR-D platform                                                                 | Not Available        | Technology Preview   | Technology Preview   |
| PTP Telecom Boundary Clock (T-BC) high availability with dual time receiver ports on Intel Granite Rapids-D (GNR-D) | Not Available        | Not Available        | Technology Preview   |
| PTP Telecom Grandmaster (T-GM) on Intel Granite Rapids-D (GNR-D)                                                    | Not Available        | Technology Preview   | Technology Preview   |

Networking Technology Preview tracker

## Node Technology Preview features

| Feature                                                   | 4.21               | 4.22               | 5.0                  |
|-----------------------------------------------------------|--------------------|--------------------|----------------------|
| Additional CRI-O storage locations                        | Not Available      | Technology Preview | General Availability |
| `MaxUnavailableStatefulSet` featureset                    | Technology Preview | Technology Preview | Technology Preview   |
| Project-scoped image pull secrets for mirrored registries | Not Available      | Technology Preview | General Availability |
| Partitionable device DRA support                          | Not Available      | Technology Preview | General Availability |

Nodes Technology Preview tracker

## Postinstallation configuration Technology Preview features

| Feature                                                         | 4.21          | 4.22               | 5.0                |
|-----------------------------------------------------------------|---------------|--------------------|--------------------|
| Expanding a bare metal cluster using images from OCI registries | Not Available | Technology Preview | Technology Preview |

Postinstallation configuration Technology Preview tracker

## Red Hat OpenStack Platform (RHOSP) Technology Preview features

| Feature                                          | 4.21               | 4.22               | 5.0                |
|--------------------------------------------------|--------------------|--------------------|--------------------|
| RHOSP integration into the Cluster CAPI Operator | Technology Preview | Technology Preview | Technology Preview |
| Hosted control planes on RHOSP 17.1              | Technology Preview | Technology Preview | Technology Preview |

RHOSP Technology Preview tracker

## Scalability and performance Technology Preview features

| Feature                                                         | 4.21                 | 4.22                 | 5.0                  |
|-----------------------------------------------------------------|----------------------|----------------------|----------------------|
| factory-precaching-cli tool                                     | Technology Preview   | Technology Preview   | Technology Preview   |
| Hyperthreading-aware CPU manager policy                         | Technology Preview   | Technology Preview   | Technology Preview   |
| Mount namespace encapsulation                                   | Technology Preview   | Technology Preview   | Technology Preview   |
| Node Observability Operator                                     | Technology Preview   | Technology Preview   | Technology Preview   |
| Increasing the etcd database size                               | Technology Preview   | Technology Preview   | General Availability |
| Managing etcd size by setting the `eventTTLMinutes` property    | Technology Preview   | General Availability | General Availability |
| Pinned Image Sets                                               | Technology Preview   | Technology Preview   | Technology Preview   |
| Configuring NUMA-aware scheduler replicas and high availability | General Availability | General Availability | General Availability |
| OVS-DPDK CPU reservation                                        | Not Available        | Not Available        | Technology Preview   |

Scalability and performance Technology Preview tracker

## Storage Technology Preview features

| Feature                                               | 4.21                 | 4.22                 | 5.0                  |
|-------------------------------------------------------|----------------------|----------------------|----------------------|
| Changed block tracking                                | Developer Preview    | Developer Preview    | Technology Preview   |
| Azure File CSI cloning support                        | General Availability | General Availability | General Availability |
| Azure File CSI snapshot support                       | General Availability | General Availability | General Availability |
| European Sovereign Cloud (EUSC) region                | Not Available        | Technology Preview   | Technology Preview   |
| Hyperdisk Balanced HA volumes                         | Not Available        | General Availability | General Availability |
| LSO symlinks management                               | Not Available        | General Availability | General Availability |
| Increasing max number of volumes per node for vSphere | Technology Preview   | Technology Preview   | Technology Preview   |
| RWX/RWO SELinux mount option                          | Technology Preview   | Technology Preview   | Technology Preview   |
| CSI volume group snapshots                            | Technology Preview   | Technology Preview   | General Availability |
| Volume Attribute Classes                              | General Availability | General Availability | General Availability |

Storage Technology Preview tracker

## Web console Technology Preview features

| Feature                                                                      | 4.21               | 4.22               | 5.0                |
|------------------------------------------------------------------------------|--------------------|--------------------|--------------------|
| Red Hat OpenShift Lightspeed in the OpenShift Container Platform web console | Technology Preview | Technology Preview | Technology Preview |

Web console Technology Preview tracker

# Known issues

This section includes several known issues for OpenShift Container Platform 4.17.

# Asynchronous errata updates

Security, bug fix, and enhancement updates for OpenShift Container Platform 4.17 are released as asynchronous errata through the Red Hat Network. All OpenShift Container Platform 4.17 errata is [available on the Red Hat Customer Portal](https://access.redhat.com/downloads/content/290/). See the [OpenShift Container Platform Life Cycle](https://access.redhat.com/support/policy/updates/openshift) for more information about asynchronous errata. Red Hat Customer Portal users can enable errata notifications in the account settings for Red Hat Subscription Management (RHSM). When errata notifications are enabled, users are notified through email whenever new errata relevant to their registered systems are released.

<div class="note">

Red Hat Customer Portal user accounts must have systems registered and consuming OpenShift Container Platform entitlements for OpenShift Container Platform errata notification emails to generate.

</div>

This section will continue to be updated over time to provide notes on enhancements and bug fixes for future asynchronous errata releases of OpenShift Container Platform 4.17. Versioned asynchronous releases, for example with the form OpenShift Container Platform 4.17.z, will be detailed in subsections. In addition, releases in which the errata text cannot fit in the space provided by the advisory will be detailed in subsections that follow.

<div class="important">

For any OpenShift Container Platform release, always review the instructions on [updating your cluster](../updating/updating_a_cluster/updating-cluster-web-console.xml#updating-cluster-web-console) properly.

</div>
