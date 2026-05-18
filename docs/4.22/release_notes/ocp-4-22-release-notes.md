Red Hat OpenShift Container Platform provides developers and IT organizations with a hybrid cloud application platform for deploying both new and existing applications on secure, scalable resources with minimal configuration and management. OpenShift Container Platform supports a wide selection of programming languages and frameworks, such as Java, JavaScript, Python, Ruby, and PHP.

Built on Red Hat Enterprise Linux (RHEL) and Kubernetes, OpenShift Container Platform provides a more secure and scalable multitenant operating system for today’s enterprise-class applications, while delivering integrated application runtimes and libraries. OpenShift Container Platform enables organizations to meet security, privacy, compliance, and governance requirements.

# About this release

OpenShift Container Platform ([RHBA-2026:1481](https://access.redhat.com/errata/RHBA-2026:1481)) is now available. This release uses [Kubernetes 1.35](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.35.md) with CRI-O runtime. New features, changes, and known issues that pertain to OpenShift Container Platform 4.17 are included in this topic.

OpenShift Container Platform 4.17 clusters are available at <https://console.redhat.com/openshift>. From the Red Hat Hybrid Cloud Console, you can deploy OpenShift Container Platform clusters to either on-premises or cloud environments.

You must use RHCOS machines for the control plane and for the compute machines.

Starting from OpenShift Container Platform 4.14, the Extended Update Support (EUS) phase for even-numbered releases increases the total available lifecycle to 24 months on all supported architectures, including `x86_64`, 64-bit ARM (`aarch64`), IBM Power® (`ppc64le`), and IBM Z® (`s390x`) architectures. Beyond this, Red Hat also offers a 12-month additional EUS add-on, denoted as *Additional EUS Term 2*, that extends the total available lifecycle from 24 months to 36 months. The Additional EUS Term 2 is available on all architecture variants of OpenShift Container Platform. For more information about support for all versions, see the [Red Hat OpenShift Container Platform Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift).

OpenShift Container Platform is designed for FIPS. When running Red Hat Enterprise Linux (RHEL) or Red Hat Enterprise Linux CoreOS (RHCOS) booted in FIPS mode, OpenShift Container Platform core components use the RHEL cryptographic libraries that have been submitted to NIST for FIPS 140-2/140-3 Validation on only the `x86_64`, `ppc64le`, and `s390x` architectures.

For more information about the NIST validation program, see [Cryptographic Module Validation Program](https://csrc.nist.gov/Projects/cryptographic-module-validation-program/validated-modules). For the latest NIST status for the individual versions of RHEL cryptographic libraries that have been submitted for validation, see [Compliance Activities and Government Standards](https://access.redhat.com/articles/2918071#fips-140-2-and-fips-140-3-2).

# OpenShift Container Platform layered and dependent component support and compatibility

The scope of support for layered and dependent components of OpenShift Container Platform changes independently of the OpenShift Container Platform version. To determine the current support status and compatibility for an add-on, refer to its release notes. For more information, see the [Red Hat OpenShift Container Platform Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift).

# New features and enhancements

This release adds improvements related to the following components and concepts:

## API server

## Authentication and authorization

## Autoscaling

## Edge computing

## etcd

## Extensions (OLM v1)

## IBM Power

## IBM Z and IBM LinuxONE

## Installation and update

Installing a cluster on Microsoft Azure with a user-provisioned DNS is generally available
You can enable a user-provisioned domain name server (DNS) instead of the default cluster-provisioned DNS solution. For example, your organization’s security policies might not allow the use of public DNS services such as Microsoft Azure DNS. As a result, you can manage the API and Ingress DNS records in your own system rather than adding the records to the DNS of the cloud. If you use this feature, you must provision the cluster first and then provide your own DNS solution that includes records for `api.<cluster_name>.<base_domain>.` and `*.apps.<cluster_name>.<base_domain>.`.

Installing a cluster on Azure with a user-provisioned DNS was introduced in OpenShift Container Platform 4.21 with Technology Preview status. In OpenShift Container Platform 4.22, it is now generally available.

For more information, see [Enabling a user-managed DNS](../installing/installing_azure/ipi/installing-azure-customizations.xml#installation-azure-enabling-user-managed-DNS_installing-azure-customizations) and [Provisioning your own DNS records](../installing/installing_azure/ipi/installing-azure-customizations.xml#installation-azure-provisioning-own-dns-records_installing-azure-customizations).

Installing a cluster on AWS European Sovereign Cloud (Technology Preview)
You can now install OpenShift Container Platform on Amazon Web Services (AWS) in the European Sovereign Cloud (EUSC) region (`eusc-de-east-1`). The AWS EUSC region is separate and independent from other AWS regions, with all the infrastructure located within the European Union (EU). You must specify a custom Amazon Machine Image (AMI) in the `platform.aws.defaultMachinePlatform.amiID` field of your `install-config.yaml` file. Other limitations also apply. The AWS EUSC region is available as a Technology Preview feature.

For more information, see [AWS EUSC](../installing/installing_aws/installing-aws-account.xml#installation-aws-eusc_region_installing-aws-account).

Installing a cluster on Google Cloud with N4A machine types
With this update, you can install a OpenShift Container Platform cluster on Google Cloud with N4A machine types.

N4A Virtual Machines (VMs) use highly efficient Arm-based processors. N4A machines deliver exceptional performance compared to current-generation x86-based VMs, making them ideal for containerized applications and microservices on OpenShift Container Platform.

For more information, see [Tested instance types for Google Cloud](../installing/installing_gcp/installing-gcp-customizations.xml#installation-gcp-tested-machine-types_installing-gcp-customizations) and [N4A machine series (Google documentation)](https://docs.cloud.google.com/compute/docs/general-purpose-machines#n4a_series).

## Machine Config Operator

## Machine management

## Monitoring

## Networking

Network policy enhancement
OpenShift Container Platform now includes `NetworkPolicy` objects in some of its own namespaces by default. This inclusion improves overall security and better protects control plane components.

Do not modify the `NetworkPolicy` objects that OpenShift Container Platform includes in its own namespaces by default. To check the namespaces that include the objects by default, you can run the following command:

``` terminal
$ oc get networkpolicies --all-namespaces
```

The OpenShift Container Platform 4.17 release did not include these objects in all OpenShift Container Platform namespaces; later OpenShift Container Platform releases might include the objects in additional namespaces.

IPv4 forwarding for specific network interfaces
You can enable IPv4 forwarding on specific network interfaces by using the Kubernetes NMState Operator. By setting the `forwarding: true` field in a `NodeNetworkConfigurationPolicy` custom resource, you can configure individual interfaces to forward IP packets without enabling global IP forwarding on the cluster. This approach improves security by keeping global forwarding disabled while allowing forwarding only on the interfaces that require it, such as secondary interfaces used by MetalLB load balancers.

For more information, see [Enable IP forwarding on specific interfaces](../networking/k8s_nmstate/k8s-nmstate-updating-node-network-config.xml#nw-nmstate-enable-per-interface-ip-forwarding_k8s-nmstate-updating-node-network-config).

Kubernetes NMState Operator extends metrics support
The Kubernetes NMState Operator can now collect metrics from the following Kubernetes components:

- `kubernetes_nmstate_policies_status`, which tracks the active status of `NodeNetworkConfigurationPolicy` (NNCP) resources across the cluster.

- `kubernetes_nmstate_enactments_status`, which tracks the active status of `NodeNetworkConfigurationEnactment` (NNCE) resources on a per-node basis.

  For more information, see [Viewing metrics collected by the Kubernetes NMState Operator](../networking/networking_operators/k8s-nmstate-about-the-k8s-nmstate-operator.xml#viewing-stats-collected-kubernetes-nmstate-op_k8s-nmstate-about-the-k8s-nmstate-operator).

Alternative interface names for network interfaces with the Kubernetes NMState Operator
Assign alternative names to network interfaces by using the Kubernetes NMState Operator. Alternative names provide consistent, descriptive labels for interfaces across cluster nodes, simplifying automation in environments where interface names vary across nodes.

For more information, see [Configure alternative network interface names](../networking/k8s_nmstate/k8s-nmstate-updating-node-network-config.xml#k8s-nmstate-alternative-interface-names_k8s-nmstate-updating-node-network-config).

Ingress firewall configuration with the `commatrix` plugin
The `commatrix` plugin generates `nftables` firewall rules in Butane format for deployment to cluster nodes. These rules restrict ingress traffic to only the flows required by deployed services, promoting a zero-trust security posture. The plugin also generates a `NodeDisruptionPolicy` patch to apply rule updates without node reboots.

For more information, see [Generate nftables firewall rules in Butane format](../installing/install_config/configuring-firewall.xml#commatrix-generate-butane_configuring-firewall).

<!-- -->

MetalLB ConfigurationState resource reports controller and speaker configuration health
You can now use the new `ConfigurationState` custom resource to verify that MetalLB has successfully applied your settings across the cluster. This feature provides a single, consistent location to identify configuration errors that were previously only visible by searching through individual node logs or FRR status reports

MetalLB creates a `ConfigurationState` resource for the controller and for each speaker node. Each resource reports whether your configuration is valid and surfaces specific error details if validation fails, such as issues with `IPAddressPool`, `BGPPeer`, or `BFDProfile` objects. This centralized reporting helps you monitor system integrity and resolve networking conflicts more quickly.

For more information, see [Checking MetalLB configuration status](../networking/ingress_load_balancing/metallb/monitoring-metallb-status.xml#nw-metallb-checking-configuration-status_monitor-metallb-config-status).

<!-- -->

Multi-network policy backend uses nftables
With this release, the multi-network policy backend uses `nftables` instead of `iptables`. The `iptables` backend has been removed and there is no option to revert to it. The `MultiNetworkPolicy` API and user-facing configuration are unchanged, so your existing multi-network policies continue to work without modification.

For more information, see [Configuring multi-network policy](../networking/multiple_networks/secondary_networks/configuring-multi-network-policy.xml#configuring-multi-network-policy).

## Nodes

## Operator development

## Postinstallation configuration

Support for the PCI addresses of NICs in `BareMetalHost` hardware data
With this release, the Peripheral Component Interconnect (PCI) address for each network interface controller (NIC) is available in two separate custom resources (CRs). The PCI address is located in the `status.hardware.nics[]` section of the `BareMetalHost` CR and in the `spec.hardware.nics[]` section of the `HardwareData` CR. While these are separate resources, the values in the `pciAddress` fields, for example `0000:00:03.0`, are identical.

For more information, see [About the BareMetalHost resource](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#bmo-about-the-baremetalhost-resource_bare-metal-postinstallation-configuration) and [The BareMetalHost status](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#the-baremetalhost-status).

## Scalability and performance

NUMA-aware scheduler supports clusters with up to 500 nodes
With this release, you can scale the NUMA-aware secondary scheduler to support clusters with up to 500 nodes. The scheduler defaults to a `Burstable` quality of service (QoS) profile, which reduces baseline resource consumption while allowing the scheduler to scale up during peak loads.

For more information, see [Topology-aware scheduler scalability](../scalability_and_performance/cnf-numa-aware-scheduling.xml#cnf-topology-aware-scheduler-scalability_numa-aware).

<!-- -->

CRI-O ExecCPUAffinity protects low-latency workloads from exec process interruption
With this release, you can protect latency-sensitive workloads from performance degradation caused by `oc exec` and shell processes. When you apply a `PerformanceProfile`, the CRI-O `ExecCPUAffinity` feature automatically pins exec processes to a designated CPU within the container’s allocated set, preventing them from running on your workload CPUs. This feature is enabled by default for `Guaranteed` QoS pods with whole-integer CPU requests and requires no additional configuration. You can disable it per profile by adding the `performance.openshift.io/exec-cpu-affinity: "disable"` annotation to the `PerformanceProfile`.

For more information, see [How `ExecCPUAffinity` prevents latency spikes from exec operations](../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#cnf-exec-cpu-affinity_cnf-tuning-low-latency-nodes-with-perf-profile).

## Web console

Support for integrated OCI chart interaction
The OpenShift Container Platform web console now fully supports browsing, inspecting, and installing Open Container Initiative (OCI)-based Helm charts directly from configured repositories to provide functional parity with traditional HTTP(S) Helm charts. This enhancement removes the previous discovery-only limitation, enabling users to interact with and deploy OCI-based charts seamlessly within the console’s repository views.

For more information, see [Configuring custom Helm chart repositories](../applications/working_with_helm_charts/configuring-custom-helm-chart-repositories.xml#configuring-custom-helm-chart-repositories).

# Notable technical changes

This section includes several technical changes for OpenShift Container Platform 4.17.

Platform components and Operators now use dedicated service accounts
Most OpenShift Container Platform platform components and Operators have been updated to use dedicated service accounts instead of the `default` service account. This change follows the principle of least privilege, simplifies security audits, and reduces the risk of accidental permission elevation by ensuring that platform identities are isolated from user workloads.

The following dynamic tools continue to use the `default` service account to ensure operational efficiency:

- `oc debug`: Uses the `default` service account to avoid the performance overhead of creating and removing unique service accounts for short-lived troubleshooting sessions.

- `oc adm must-gather`: Uses the `default` service account to collect diagnostic data across the cluster without requiring extensive manual RBAC modifications.

For more information, see [Default project service accounts and roles](../authentication/using-service-accounts-in-applications.xml#default-service-accounts-and-roles_using-service-accounts).

# Deprecated and removed features

## Images deprecated and removed features

| Feature                  | 4.20       | 4.21       | 4.22 |
|--------------------------|------------|------------|------|
| Cluster Samples Operator | Deprecated | Deprecated |      |

Images deprecated and removed tracker

## Installation deprecated and removed features

| Feature                                                                                                                | 4.20                 | 4.21       | 4.22 |
|------------------------------------------------------------------------------------------------------------------------|----------------------|------------|------|
| `--cloud` parameter for `oc adm release extract`                                                                       | Deprecated           | Deprecated |      |
| CoreDNS wildcard queries for the `cluster.local` domain                                                                | Deprecated           | Deprecated |      |
| `compute.platform.openstack.rootVolume.type` for RHOSP                                                                 | Deprecated           | Deprecated |      |
| `controlPlane.platform.openstack.rootVolume.type` for RHOSP                                                            | Deprecated           | Deprecated |      |
| `ingressVIP` and `apiVIP` settings in the `install-config.yaml` file for installer-provisioned infrastructure clusters | Deprecated           | Deprecated |      |
| `platform.aws.preserveBootstrapIgnition` parameter for Amazon Web Services (AWS)                                       | Deprecated           | Deprecated |      |
| Installing a cluster on AWS with compute nodes in AWS Outposts                                                         | Deprecated           | Deprecated |      |
| Deploying managed clusters using `SiteConfig` and the GitOps ZTP workflow                                              | Deprecated           | Removed    |      |
| Installing a cluster using Fujitsu iRMC drivers on bare-metal machines                                                 | General Availability | Deprecated |      |

Installation deprecated and removed tracker

## Machine Management deprecated and removed features

| Feature                                                                          | 4.20                 | 4.21       | 4.22 |
|----------------------------------------------------------------------------------|----------------------|------------|------|
| Confidential Computing with AMD Secure Encrypted Virtualization for Google Cloud | Deprecated           | Deprecated |      |
| Managing bare-metal machines using Fujitsu iRMC drivers                          | General Availability | Deprecated |      |

Machine management deprecated and removed tracker

## Networking deprecated and removed features

| Feature  | 4.20       | 4.21       | 4.22 |
|----------|------------|------------|------|
| iptables | Deprecated | Deprecated |      |

Networking deprecated and removed tracker

## Node deprecated and removed features

| Feature                                                              | 4.20       | 4.21       | 4.22 |
|----------------------------------------------------------------------|------------|------------|------|
| `ImageContentSourcePolicy` (ICSP) objects                            | Deprecated | Deprecated |      |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/zone`   | Deprecated | Deprecated |      |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/region` | Deprecated | Deprecated |      |

Node deprecated and removed tracker

## OpenShift CLI (oc) deprecated and removed features

| Feature                         | 4.20                 | 4.21                 | 4.22       |
|---------------------------------|----------------------|----------------------|------------|
| oc-mirror plugin v1             | Deprecated           | Deprecated           |            |
| Docker v2 registries            | Deprecated           | Deprecated           |            |
| `oc adm release mirror` command | General Availability | General Availability | Deprecated |

OpenShift CLI (oc) deprecated and removed tracker

## Operator lifecycle and development deprecated and removed features

| Feature                                      | 4.20       | 4.21       | 4.22 |
|----------------------------------------------|------------|------------|------|
| SQLite database format for Operator catalogs | Deprecated | Deprecated |      |

Operator lifecycle and development deprecated and removed tracker

## Web console deprecated and removed features

| Feature                                | 4.20       | 4.21       | 4.22 |
|----------------------------------------|------------|------------|------|
| `useModal` hook for dynamic plugin SDK | Deprecated | Deprecated |      |

Web console deprecated and removed tracker

## Workloads deprecated and removed features

| Feature                    | 4.20       | 4.21       | 4.22       |
|----------------------------|------------|------------|------------|
| `DeploymentConfig` objects | Deprecated | Deprecated | Deprecated |

Workloads deprecated and removed tracker

# Deprecated features

Deprecation of Fujitsu Integrated Remote Management Controller (iRMC) driver for bare-metal machines
As of OpenShift Container Platform 4.21, support for the Fujitsu iRMC baseboard management controller (BMC) driver has been deprecated and will be removed in a future release. If a `BareMetalHost` resource contains a BMC address with `irmc://` as its URI scheme, the resource must be updated to use another BMC scheme, such as `redfish://` or `ipmi://`. Once support for this driver is removed, hosts that use `irmc://` URI schemes will become unmanageable.

For information about updating the `BareMetalHost` resource, see [Editing a BareMetalHost resource](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#bmo-editing-a-baremetalhost-resource_bare-metal-postinstallation-configuration).

Deprecation of the `oc adm release mirror` command
As of OpenShift Container Platform 4.22, using the `oc adm release mirror` command to mirror release images has been deprecated and will be removed in a future release.

As an alternative, use the [oc-mirror plugin v2](../disconnected/about-installing-oc-mirror-v2.xml#about-installing-oc-mirror-v2).

# Removed features

This section includes removed features for OpenShift Container Platform 4.17.

# Fixed issues

The following issues are fixed for this release:

## Installer

## Kube Controller Manager

## Kube Scheduler

## Networking

## Clock state metrics degrade correctly after upstream clock loss

## Node Tuning Operator

## OpenShift API Server

## Web console

Guided Tours respect a console capability setting
In previous releases, the web console displayed Guided Tours by default, even in environments where users already know OpenShift Container Platform, such as shared clusters. In OpenShift Container Platform 4.22, cluster administrators can enable or disable Guided Tours by configuring the console `GuidedTourFeature` capability.

[CONSOLE-4986](https://issues.redhat.com/browse/CONSOLE-4986)

# Technology Preview features status

Some features in this release are currently in Technology Preview. These experimental features are not intended for production use. Note the following scope of support on the Red Hat Customer Portal for these features:

[Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview)

In the following tables, features are marked with the following statuses:

- *Not Available*

- *Technology Preview*

- *General Availability*

- *Deprecated*

- *Removed*

## Authentication and authorization Technology Preview features

| Feature                                       | 4.20               | 4.21               | 4.22               |
|-----------------------------------------------|--------------------|--------------------|--------------------|
| Pod security admission restricted enforcement | Technology Preview | Technology Preview | Technology Preview |

Authentication and authorization Technology Preview tracker

## Edge computing Technology Preview features

| Feature                                                                  | 4.20                 | 4.21                 | 4.22                 |
|--------------------------------------------------------------------------|----------------------|----------------------|----------------------|
| Accelerated provisioning of GitOps ZTP                                   | Technology Preview   | Technology Preview   | Technology Preview   |
| Enabling disk encryption with TPM and PCR protection                     | Technology Preview   | Technology Preview   | Technology Preview   |
| Configuring a local arbiter node                                         | General Availability | General Availability | General Availability |
| Configuring a two-node OpenShift Container Platform cluster with fencing | Technology Preview   | Technology Preview   | General Availability |

Edge computing Technology Preview tracker

## Extensions Technology Preview features

| Feature                                                                 | 4.20               | 4.21                 | 4.22 |
|-------------------------------------------------------------------------|--------------------|----------------------|------|
| OLM v1 runtime validation of container images using sigstore signatures | Technology Preview | Technology Preview   |      |
| OLM v1 permissions preflight check for cluster extensions               | Technology Preview | Technology Preview   |      |
| OLM v1 deploying a cluster extension in a specified namespace           | Technology Preview | Technology Preview   |      |
| OLM v1 deploying a cluster extension that uses webhooks                 | Technology Preview | General Availability |      |
| OLM v1 software catalog                                                 | Not Available      | Technology Preview   |      |

Extensions Technology Preview tracker

## Installation Technology Preview features

| Feature                                                                            | 4.20                 | 4.21                 | 4.22 |
|------------------------------------------------------------------------------------|----------------------|----------------------|------|
| Adding kernel modules to nodes with kvc                                            | Technology Preview   | Technology Preview   |      |
| Installing a cluster on Alibaba Cloud by using Assisted Installer                  | Technology Preview   | Technology Preview   |      |
| Dedicated disk for etcd on Microsoft Azure                                         | Technology Preview   | Technology Preview   |      |
| Mount shared entitlements in BuildConfigs in RHEL                                  | Technology Preview   | Technology Preview   |      |
| OpenShift zones support for vSphere host groups                                    | Technology Preview   | Technology Preview   |      |
| Selectable Cluster Inventory                                                       | Technology Preview   | Technology Preview   |      |
| Enabling a user-provisioned DNS on Google Cloud                                    | Technology Preview   | General Availability |      |
| Enabling a user-provisioned DNS on Microsoft Azure                                 | Not Available        | Technology Preview   |      |
| Enabling a user-provisioned DNS on Amazon Web Services (AWS)                       | Not Available        | Technology Preview   |      |
| Installing a cluster using Google Cloud private and restricted API endpoints       | Not Available        | General Availability |      |
| Installing a cluster on VMware vSphere with multiple network interface controllers | General Availability | General Availability |      |
| Using bare metal as a service                                                      | Technology Preview   | Technology Preview   |      |
| Running firmware upgrades for hosts in deployed bare metal clusters                | Technology Preview   | General Availability |      |
| Changing the CVO log level                                                         | Technology Preview   | Technology Preview   |      |

Installation Technology Preview tracker

## Machine Config Operator Technology Preview features

| Feature                                                | 4.20               | 4.21                 | 4.22 |
|--------------------------------------------------------|--------------------|----------------------|------|
| Boot image management for Azure and vSphere            | Technology Preview | General Availability |      |
| Boot image management for control plane nodes          | Not available      | Technology Preview   |      |
| image mode for OpenShift status reporting improvements | Not available      | Technology Preview   |      |
| Overriding storage or partition setup                  | Not available      | Technology Preview   |      |

Machine Config Operator Technology Preview tracker

## Machine management Technology Preview features

| Feature                                                                                     | 4.20               | 4.21               | 4.22 |
|---------------------------------------------------------------------------------------------|--------------------|--------------------|------|
| Managing machines with the Cluster API for Amazon Web Services                              | Technology Preview | Technology Preview |      |
| Managing machines with the Cluster API for Google Cloud                                     | Technology Preview | Technology Preview |      |
| Managing machines with the Cluster API for IBM Power® Virtual Server                        | Technology Preview | Technology Preview |      |
| Managing machines with the Cluster API for Microsoft Azure                                  | Technology Preview | Technology Preview |      |
| Managing machines with the Cluster API for RHOSP                                            | Technology Preview | Technology Preview |      |
| Managing machines with the Cluster API for VMware vSphere                                   | Technology Preview | Technology Preview |      |
| Managing machines with the Cluster API for bare metal                                       | Technology Preview | Technology Preview |      |
| Cloud controller manager for IBM Power® Virtual Server                                      | Technology Preview | Technology Preview |      |
| Adding multiple subnets to an existing VMware vSphere cluster by using compute machine sets | Technology Preview | Technology Preview |      |
| Bare-metal nodes on VMware vSphere clusters                                                 | Not Available      | Technology Preview |      |

Machine management Technology Preview tracker

## Multi-Architecture Technology Preview features

| Feature                                                       | 4.20                 | 4.21                 | 4.22 |
|---------------------------------------------------------------|----------------------|----------------------|------|
| `kdump` on `arm64` architecture                               | General Availability | General Availability |      |
| `kdump` on `s390x` architecture                               | General Availability | General Availability |      |
| `kdump` on `ppc64le` architecture                             | General Availability | General Availability |      |
| Support for configuring the image stream import mode behavior | Technology Preview   | Technology Preview   |      |

Multi-Architecture Technology Preview tracker

## Networking Technology Preview features

| Feature                                                                                                   | 4.20                 | 4.21                 | 4.22 |
|-----------------------------------------------------------------------------------------------------------|----------------------|----------------------|------|
| eBPF manager Operator                                                                                     | Technology Preview   | Technology Preview   |      |
| Advertise using L2 mode the MetalLB service from a subset of nodes, using a specific pool of IP addresses | Technology Preview   | Technology Preview   |      |
| Updating the interface-specific safe sysctls list                                                         | Technology Preview   | Technology Preview   |      |
| Egress service custom resource                                                                            | Technology Preview   | Technology Preview   |      |
| VRF specification in `BGPPeer` custom resource                                                            | Technology Preview   | Technology Preview   |      |
| OVN-Kubernetes customized `br-ex` bridge on vSphere and RHOSP                                             | Technology Preview   | Technology Preview   |      |
| Live migration to OVN-Kubernetes from OpenShift Container Platform SDN                                    | Not Available        | Not Available        |      |
| Dynamic configuration manager                                                                             | Technology Preview   | Technology Preview   |      |
| SR-IOV Network Operator support for Intel C741 Emmitsburg Chipset                                         | Technology Preview   | Technology Preview   |      |
| Dual-port NIC for PTP ordinary clock                                                                      | General Availability | General Availability |      |
| DPU Operator                                                                                              | Technology Preview   | Technology Preview   |      |
| Fast IPAM for the Whereabouts IPAM CNI plugin                                                             | Technology Preview   | Technology Preview   |      |
| Unnumbered BGP peering                                                                                    | General Availability | General Availability |      |
| Load balancing across the aggregated bonded interface with xmitHashPolicy                                 | Technology Preview   | Technology Preview   |      |
| PF Status Relay Operator for high availability with SR-IOV networks                                       | Technology Preview   | Technology Preview   |      |
| Preconfigured user-defined network end points using MTV                                                   | Technology Preview   | Technology Preview   |      |
| Unassisted holdover for PTP devices                                                                       | Technology Preview   | General Availability |      |

Networking Technology Preview tracker

## Node Technology Preview features

| Feature                                           | 4.20                 | 4.21                 | 4.22 |
|---------------------------------------------------|----------------------|----------------------|------|
| `MaxUnavailableStatefulSet` featureset            | Technology Preview   | Technology Preview   |      |
| sigstore support                                  | General Availability | General Availability |      |
| Default sigstore `openshift` cluster image policy | Technology Preview   | General Availability |      |
| Linux user namespace support                      | General Availability | General Availability |      |
| Attribute-Based GPU Allocation                    | Technology Preview   | General Availability |      |

Nodes Technology Preview tracker

## Red Hat OpenStack Platform (RHOSP) Technology Preview features

| Feature                                          | 4.20               | 4.21               | 4.22 |
|--------------------------------------------------|--------------------|--------------------|------|
| RHOSP integration into the Cluster CAPI Operator | Technology Preview | Technology Preview |      |
| Hosted control planes on RHOSP 17.1              | Technology Preview | Technology Preview |      |

RHOSP Technology Preview tracker

## Scalability and performance Technology Preview features

| Feature                                                         | 4.20               | 4.21               | 4.22 |
|-----------------------------------------------------------------|--------------------|--------------------|------|
| factory-precaching-cli tool                                     | Technology Preview | Technology Preview |      |
| Hyperthreading-aware CPU manager policy                         | Technology Preview | Technology Preview |      |
| Mount namespace encapsulation                                   | Technology Preview | Technology Preview |      |
| Node Observability Operator                                     | Technology Preview | Technology Preview |      |
| Increasing the etcd database size                               | Technology Preview | Technology Preview |      |
| Managing etcd size by setting the `eventTTLMinutes` property    | Not available      | Technology Preview |      |
| Pinned Image Sets                                               | Technology Preview | Technology Preview |      |
| Configuring NUMA-aware scheduler replicas and high availability | Technology Preview | Technology Preview |      |

Scalability and performance Technology Preview tracker

## Storage Technology Preview features

| Feature                                                                 | 4.20                 | 4.21                 | 4.22 |
|-------------------------------------------------------------------------|----------------------|----------------------|------|
| AWS EFS One Zone volume                                                 | General Availability | General Availability |      |
| Automatic device discovery and provisioning with Local Storage Operator | Technology Preview   | Technology Preview   |      |
| Azure File CSI cloning support                                          | Technology Preview   | General Availability |      |
| Azure File CSI snapshot support                                         | Technology Preview   | General Availability |      |
| Azure Disk performance plus                                             | General Availability | General Availability |      |
| Configuring fsGroupChangePolicy per namespace                           | General Availability | General Availability |      |
| Shared Resources CSI Driver in OpenShift Builds                         | Technology Preview   | Technology Preview   |      |
| Increasing max number of volumes per node for vSphere                   | Technology Preview   | Technology Preview   |      |
| RWX/RWO SELinux mount option                                            | Technology Preview   | Technology Preview   |      |
| CSI volume group snapshots                                              | Technology Preview   | Technology Preview   |      |
| Volume Attribute Classes                                                | Technology Preview   | General Availability |      |
| Volume populators                                                       | General Availability | General Availability |      |

Storage Technology Preview tracker

## Web console Technology Preview features

| Feature                                                                      | 4.20               | 4.21               | 4.22 |
|------------------------------------------------------------------------------|--------------------|--------------------|------|
| Red Hat OpenShift Lightspeed in the OpenShift Container Platform web console | Technology Preview | Technology Preview |      |

Web console Technology Preview tracker

# Known issues

This section includes several known issues for OpenShift Container Platform 4.17.

- Currently, the `topo-aware-scheduler` provided by the NUMA Resources Operator (NRO) does not support Kubernetes priority-based preemption. When all NUMA zones on available nodes are fully consumed by lower-priority pods, a high-priority pod with a `PreemptLowerPriority` policy remains in `Pending` state indefinitely instead of preempting the lower-priority pods. As a consequence, workloads that depend on priority-based preemption for scheduling recovery do not function correctly when using the `topo-aware-scheduler`. ([OCPBUGS-77930](https://issues.redhat.com/browse/OCPBUGS-77930))

# Asynchronous errata updates

Security, bug fix, and enhancement updates for OpenShift Container Platform 4.17 are released as asynchronous errata through the Red Hat Network. All OpenShift Container Platform 4.17 errata is [available on the Red Hat Customer Portal](https://access.redhat.com/downloads/content/290/). See the [OpenShift Container Platform Life Cycle](https://access.redhat.com/support/policy/updates/openshift) for more information about asynchronous errata. Red Hat Customer Portal users can enable errata notifications in the account settings for Red Hat Subscription Management (RHSM). When errata notifications are enabled, users are notified through email whenever new errata relevant to their registered systems are released.

<div class="note">

Red Hat Customer Portal user accounts must have systems registered and consuming OpenShift Container Platform entitlements for OpenShift Container Platform errata notification emails to generate.

</div>

This section will continue to be updated over time to provide notes on enhancements and bug fixes for future asynchronous errata releases of OpenShift Container Platform 4.17. Versioned asynchronous releases, for example with the form OpenShift Container Platform 4.17.z, will be detailed in subsections. In addition, releases in which the errata text cannot fit in the space provided by the advisory will be detailed in subsections that follow.

<div class="important">

For any OpenShift Container Platform release, always review the instructions on [updating your cluster](../updating/updating_a_cluster/updating-cluster-web-console.xml#updating-cluster-web-console) properly.

</div>
