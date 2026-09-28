Red Hat OpenShift Container Platform provides developers and IT organizations with a hybrid cloud application platform for deploying both new and existing applications on secure, scalable resources with minimal configuration and management. OpenShift Container Platform supports a wide selection of programming languages and frameworks, such as Java, JavaScript, Python, Ruby, and PHP.

Built on Red Hat Enterprise Linux (RHEL) and Kubernetes, OpenShift Container Platform provides a more secure and scalable multitenant operating system for today’s enterprise-class applications, while delivering integrated application runtimes and libraries. OpenShift Container Platform enables organizations to meet security, privacy, compliance, and governance requirements.

# About this release

OpenShift Container Platform ([RHBA-2026:449](https://access.redhat.com/errata/RHBA-2026:449)) is now available. This release uses [Kubernetes 1.35](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.35.md) with CRI-O runtime. New features, changes, and known issues that pertain to OpenShift Container Platform 4.17 are included in this topic.

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

## Authentication and authorization

## Autoscaling

## Cluster Version Operator

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

## Support

## Storage

## Web console

# Notable technical changes

This section includes several technical changes for OpenShift Container Platform 4.17.

# Deprecated and removed features

## Images deprecated and removed features

| Feature                  | 4.20       | 4.21       | 4.22 |
|--------------------------|------------|------------|------|
| Cluster Samples Operator | Deprecated | Deprecated |      |

Images deprecated and removed tracker

## Installation deprecated and removed features

| Feature                                                                                                                | 4.20                 | 4.21                 | 4.22       |
|------------------------------------------------------------------------------------------------------------------------|----------------------|----------------------|------------|
| `--cloud` parameter for `oc adm release extract`                                                                       | Deprecated           | Deprecated           | Deprecated |
| CoreDNS wildcard queries for the `cluster.local` domain                                                                | Deprecated           | Deprecated           | Deprecated |
| `compute.platform.openstack.rootVolume.type` for RHOSP                                                                 | Deprecated           | Deprecated           | Deprecated |
| `controlPlane.platform.openstack.rootVolume.type` for RHOSP                                                            | Deprecated           | Deprecated           | Deprecated |
| `ingressVIP` and `apiVIP` settings in the `install-config.yaml` file for installer-provisioned infrastructure clusters | Deprecated           | Deprecated           | Deprecated |
| `platform.aws.preserveBootstrapIgnition` parameter for Amazon Web Services (AWS)                                       | Deprecated           | Deprecated           | Deprecated |
| Installing a cluster on AWS with compute nodes in AWS Outposts                                                         | Deprecated           | Deprecated           | Deprecated |
| Adding kernel modules to nodes with kvc                                                                                | General Availability | General Availability | Deprecated |
| Installing a cluster using Fujitsu iRMC drivers on bare-metal machines                                                 | General Availability | Deprecated           | Deprecated |

Installation deprecated and removed tracker

## Machine Management deprecated and removed features

| Feature                                                                          | 4.20                 | 4.21       | 4.22       |
|----------------------------------------------------------------------------------|----------------------|------------|------------|
| Confidential Computing with AMD Secure Encrypted Virtualization for Google Cloud | Deprecated           | Deprecated | Deprecated |
| Managing bare-metal machines using Fujitsu iRMC drivers                          | General Availability | Deprecated | Deprecated |

Machine management deprecated and removed tracker

## Networking deprecated and removed features

| Feature  | 4.20       | 4.21       | 4.22 |
|----------|------------|------------|------|
| iptables | Deprecated | Deprecated |      |

Networking deprecated and removed tracker

## Node deprecated and removed features

| Feature                                                              | 4.20                 | 4.21                 | 4.22       |
|----------------------------------------------------------------------|----------------------|----------------------|------------|
| `ImageContentSourcePolicy` (ICSP) objects                            | Deprecated           | Deprecated           | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/zone`   | Deprecated           | Deprecated           | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/region` | Deprecated           | Deprecated           | Deprecated |
| Dynamic Accelerator Slicer (DAS) Operator                            | Technology Preview   | Technology Preview   | Removed    |
| runC container runtime                                               | General Availability | General Availability | Deprecated |

Node deprecated and removed tracker

## OpenShift CLI (oc) deprecated and removed features

| Feature                         | 4.20                 | 4.21                 | 4.22       |
|---------------------------------|----------------------|----------------------|------------|
| oc-mirror plugin v1             | Deprecated           | Deprecated           |            |
| Docker v2 registries            | Deprecated           | Deprecated           |            |
| `oc adm release mirror` command | General Availability | General Availability | Deprecated |

OpenShift CLI (oc) deprecated and removed tracker

## Operator lifecycle and development deprecated and removed features

| Feature                                      | 4.20       | 4.21       | 4.22       |
|----------------------------------------------|------------|------------|------------|
| Red Hat Marketplace                          | Deprecated | Deprecated | Removed    |
| SQLite database format for Operator catalogs | Deprecated | Deprecated | Deprecated |

Operator lifecycle and development deprecated and removed tracker

## Red Hat Enterprise Linux CoreOS (RHCOS) deprecated and removed features

| Feature                      | 4.20    | 4.21    | 4.22    |
|------------------------------|---------|---------|---------|
| WebAssembly (WASM) extension | Removed | Removed | Removed |

RHCOS deprecated and removed tracker

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

As an alternative, use the [oc-mirror plugin v2](../disconnected/oc_mirror_v2/about-installing-oc-mirror-v2.xml#about-installing-oc-mirror-v2).

Deprecation of adding kernel modules to nodes with KVC
As of OpenShift Container Platform 4.22, support for adding kernel modules to nodes with kmods-via-containers software (KVC) has been deprecated and will be removed in a future release.

Deprecation of the runC container runtime
As of OpenShift Container Platform 4.22, support for using the runC container runtime is deprecated and will be removed in a future release.

# Removed features

This section includes removed features for OpenShift Container Platform 4.17.

# Fixed issues

The following issues are fixed for this release:

## API Server and Authentication

## Bare Metal Hardware Provisioning

## Cloud Compute

## Cluster Autoscaler

## etcd

## Installer

## Kube API Server

## Kube Storage Version Migrator

## Machine Config Operator

## Management Console

## Monitoring

## Networking

## Node

## Observability

## oc

## oc-mirror

## OLM

## OpenShift API Server

## Storage

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

| Feature                                             | 4.20          | 4.21          | 4.22               |
|-----------------------------------------------------|---------------|---------------|--------------------|
| MCP server for Red Hat OpenShift Container Platform | Not Available | Not Available | Technology Preview |

AI applications Technology Preview tracker

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

| Feature                                                                 | 4.20               | 4.21                 | 4.22                 |
|-------------------------------------------------------------------------|--------------------|----------------------|----------------------|
| OLM v1 runtime validation of container images using sigstore signatures | Technology Preview | Technology Preview   | General Availability |
| OLM v1 permissions preflight check for cluster extensions               | Technology Preview | Technology Preview   | Technology Preview   |
| OLM v1 deploying a cluster extension in a specified namespace           | Technology Preview | Technology Preview   | Technology Preview   |
| OLM v1 deploying a cluster extension that uses webhooks                 | Technology Preview | General Availability | General Availability |
| OLM v1 software catalog                                                 | Not Available      | Technology Preview   | Technology Preview   |
| OLM v1 `deploymentConfig` API for cluster extension customization       | Not Available      | Not Available        | Technology Preview   |

Extensions Technology Preview tracker

## Installation Technology Preview features

| Feature                                                                                   | 4.20                 | 4.21                 | 4.22                                                         |
|-------------------------------------------------------------------------------------------|----------------------|----------------------|--------------------------------------------------------------|
| Installing a cluster on Alibaba Cloud by using Assisted Installer                         | Technology Preview   | Technology Preview   | Technology Preview                                           |
| Installing a cluster using Red Hat Enterprise Linux (RHEL) 10                             | Not Available        | Not Available        | Technology Preview                                           |
| Dedicated disk for etcd on Microsoft Azure                                                | Technology Preview   | Technology Preview   | Technology Preview                                           |
| Mount shared entitlements in BuildConfigs in RHEL                                         | Technology Preview   | Technology Preview   | General Availability (through Builds for OpenShift Operator) |
| OpenShift zones support for vSphere host groups                                           | Technology Preview   | Technology Preview   | General Availability                                         |
| Selectable Cluster Inventory                                                              |                      |                      |                                                              |
| Enabling a user-provisioned DNS on Google Cloud                                           | Technology Preview   | General Availability | General Availability                                         |
| Enabling a user-provisioned DNS on Microsoft Azure                                        | Not Available        | Technology Preview   | General Availability                                         |
| Enabling a user-provisioned DNS on Amazon Web Services (AWS)                              | Not Available        | Technology Preview   | Technology Preview                                           |
| Installing a cluster using Google Cloud private and restricted API endpoints              | Not Available        | General Availability | General Availability                                         |
| Installing a cluster on VMware vSphere with multiple network interface controllers        | General Availability | General Availability | General Availability                                         |
| Red Hat Bare Metal as a Service for OpenShift (formerly known as bare metal as a service) | Technology Preview   | Technology Preview   | General Availability                                         |
| Installing a cluster on Amazon Web Services (AWS) European Sovereign Cloud                | Not Available        | Not Available        | Technology Preview                                           |
| Installing a cluster on Amazon Web Services (AWS) with dual-stack networking              | Not Available        | Not Available        | Technology Preview                                           |
| Running firmware upgrades for hosts in deployed bare metal clusters                       | Technology Preview   | General Availability | General Availability                                         |
| Changing the CVO log level                                                                | Technology Preview   | Technology Preview   | Technology Preview                                           |
| Deploying virtualized control planes with KubeVirt Redfish                                | Not Available        | Not Available        | Technology Preview                                           |

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

| Feature                                                                                     | 4.20               | 4.21               | 4.22               |
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
| Bare-metal nodes on VMware vSphere clusters                                                 | Not Available      | Technology Preview | Technology Preview |
| Amazon Web Services Dedicated Host support                                                  | Not Available      | Not Available      | Technology Preview |

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

| Feature                                                                                                   | 4.20                 | 4.21                 | 4.22                 |
|-----------------------------------------------------------------------------------------------------------|----------------------|----------------------|----------------------|
| eBPF manager Operator                                                                                     | Technology Preview   | Technology Preview   |                      |
| Advertise using L2 mode the MetalLB service from a subset of nodes, using a specific pool of IP addresses | Technology Preview   | Technology Preview   |                      |
| Updating the interface-specific safe sysctls list                                                         | Technology Preview   | Technology Preview   |                      |
| Egress service custom resource                                                                            | Technology Preview   | Technology Preview   |                      |
| VRF specification in `BGPPeer` custom resource                                                            | Technology Preview   | Technology Preview   |                      |
| OVN-Kubernetes customized `br-ex` bridge on vSphere and RHOSP                                             | Technology Preview   | Technology Preview   | Technology Preview   |
| Live migration to OVN-Kubernetes from OpenShift Container Platform SDN                                    | Not Available        | Not Available        |                      |
| Dynamic configuration manager                                                                             | Technology Preview   | Technology Preview   |                      |
| SR-IOV Network Operator support for Intel C741 Emmitsburg Chipset                                         | Technology Preview   | Technology Preview   | General Availability |
| Dual-port NIC for PTP ordinary clock                                                                      | General Availability | General Availability |                      |
| DPU Operator                                                                                              | Technology Preview   | Technology Preview   |                      |
| Fast IPAM for the Whereabouts IPAM CNI plugin                                                             | Technology Preview   | Technology Preview   |                      |
| Unnumbered BGP peering                                                                                    | General Availability | General Availability |                      |
| Load balancing across the aggregated bonded interface with xmitHashPolicy                                 | Technology Preview   | Technology Preview   |                      |
| PF Status Relay Operator for high availability with SR-IOV networks                                       | Technology Preview   | Technology Preview   |                      |
| Preconfigured user-defined network end points using MTV                                                   | Technology Preview   | Technology Preview   |                      |
| Unassisted holdover for PTP devices                                                                       | Technology Preview   | General Availability |                      |
| No-overlay mode with BGP routing                                                                          | Not Available        | Not Available        | Technology Preview   |
| Configuring GNR-D T-BC holdover on a GNR-D platform                                                       | Not Available        | Not Available        | Technology Preview   |
| PTP Telecom Grandmaster (T-GM) on Intel Granite Rapids-D (GNR-D)                                          | Not Available        | Not Available        | Technology Preview   |

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

| Feature                                                         | 4.20          | 4.21          | 4.22               |
|-----------------------------------------------------------------|---------------|---------------|--------------------|
| Expanding a bare metal cluster using images from OCI registries | Not Available | Not Available | Technology Preview |

Postinstallation configuration Technology Preview tracker

## Red Hat OpenStack Platform (RHOSP) Technology Preview features

| Feature                                          | 4.20               | 4.21               | 4.22               |
|--------------------------------------------------|--------------------|--------------------|--------------------|
| RHOSP integration into the Cluster CAPI Operator | Technology Preview | Technology Preview | Technology Preview |
| Hosted control planes on RHOSP 17.1              | Technology Preview | Technology Preview | Technology Preview |

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

| Feature                                               | 4.20                 | 4.21                 | 4.22                 |
|-------------------------------------------------------|----------------------|----------------------|----------------------|
| AWS EFS One Zone volume                               | General Availability | General Availability | General Availability |
| Azure File CSI cloning support                        | Technology Preview   | General Availability | General Availability |
| Azure File CSI snapshot support                       | Technology Preview   | General Availability | General Availability |
| Azure Disk performance plus                           | General Availability | General Availability | General Availability |
| Configuring fsGroupChangePolicy per namespace         | General Availability | General Availability | General Availability |
| European Sovereign Cloud (EUSC) region                | Not Available        | Not Available        | Technology Preview   |
| Hyperdisk Balanced HA volumes                         | Not Available        | Not Available        | General Availability |
| LSO symlinks management                               | Not Available        | Not Available        | General Availability |
| Increasing max number of volumes per node for vSphere | Technology Preview   | Technology Preview   | Technology Preview   |
| RWX/RWO SELinux mount option                          | Technology Preview   | Technology Preview   | Technology Preview   |
| CSI volume group snapshots                            | Technology Preview   | Technology Preview   | Technology Preview   |
| Volume Attribute Classes                              | Technology Preview   | General Availability | General Availability |
| Volume populators                                     | General Availability | General Availability | General Availability |

Storage Technology Preview tracker

## Web console Technology Preview features

| Feature                                                                      | 4.20               | 4.21               | 4.22 |
|------------------------------------------------------------------------------|--------------------|--------------------|------|
| Red Hat OpenShift Lightspeed in the OpenShift Container Platform web console | Technology Preview | Technology Preview |      |

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
