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

## API server

## Authentication and authorization

Advanced direct authentication fields (Technology Preview)
You can configure advanced OIDC authentication scenarios using structured authentication fields and Common Expression Language (CEL) expressions. This feature exposes additional fields from the Kubernetes `AuthenticationConfiguration` API for flexible claim mapping and token validation. Use CEL expressions to define username and group claim fallback logic, add validation rules, and handle non-standard claim structures. This feature is available for both standalone clusters and hosted control planes.

For more information, see [About advanced direct authentication fields](../authentication/structured-auth-config-fields.xml#structured-auth-config-about).

## Autoscaling

## Cluster Version Operator

New `NetworkPolicy` parameter denies traffic for pods that are not host-networked
A new `NetworkPolicy` parameter for the `openshift-cluster-version` namespace denies all ingress and egress traffic for pods that are not host-networked.

## Edge computing

## etcd

## Extensions (OLM v1)

OLM v1 `deploymentConfig` API for cluster extension customization (Technology Preview)
The `deploymentConfig` API in the `ClusterExtension` resource enables declarative customization of Operator pod deployments, providing feature parity with `Subscription.spec.config` in OLM (Classic). Configure resource limits, node placement, environment variables, volumes, affinity rules, and pod annotations when installing cluster extensions. The format is compatible with OLM (Classic) configurations, simplifying migration.

For more information, see [Configuring cluster extensions](../extensions/ce/olmv1-configuring-extensions.xml#olmv1-deployment-config-api_olmv1-configuring-extensions).

## IBM Power

The IBM Power® release on OpenShift Container Platform 4.17 adds improvements and new capabilities to OpenShift Container Platform components
New features on IBM Power® include:

- Installer-provisioned infrastructure for IBM PowerVC is now generally available.

- Enforce RSA key format for Installer-provisioned infrastructure on IBM Power® Virtual Server.

- Harden the destroy logic for Installer-provisioned infrastructure on IBM Power® Virtual Server to simplify removing a cluster.

## IBM Z and IBM LinuxONE

The IBM Z® and IBM® LinuxONE release on OpenShift Container Platform 4.17 adds improvements and new capabilities to OpenShift Container Platform components
New features on IBM Z® and IBM® LinuxONE include:

- Enables Secrets Store CSI Driver on IBM Z®

- Hosted Control Plane support for OpenShift Container Platform clusters deployed on OpenShift Virtualization on IBM Z® and IBM® LinuxONE

## Installation and update

Installing a cluster on Microsoft Azure with a user-provisioned DNS is generally available
You can enable a user-provisioned domain name server (DNS) instead of the default cluster-provisioned DNS solution. For example, your organization’s security policies might not allow the use of public DNS services such as Microsoft Azure DNS. As a result, you can manage the API and Ingress DNS records in your own system rather than adding the records to the DNS of the cloud. If you use this feature, you must provision the cluster first and then provide your own DNS solution that includes records for `api.<cluster_name>.<base_domain>.` and `*.apps.<cluster_name>.<base_domain>.`.

Installing a cluster on Azure with a user-provisioned DNS was introduced in OpenShift Container Platform 4.21 with Technology Preview status. In OpenShift Container Platform 4.22, it is now generally available.

For more information, see [Enabling a user-managed DNS](../installing/installing_azure/ipi/installing-azure-customizations.xml#installation-azure-enabling-user-managed-DNS_installing-azure-customizations) and [Provisioning your own DNS records](../installing/installing_azure/ipi/installing-azure-customizations.xml#installation-azure-provisioning-own-dns-records_installing-azure-customizations).

OpenShift zones support for vSphere host groups is generally available
With this release, you can map OpenShift Container Platform failure domains to VMware vSphere host groups. This means that you can make use of the high availability offered by a vSphere stretched cluster configuration.

OpenShift zones support for vSphere host groups was introduced in OpenShift Container Platform 4.19 with Technology Preview status. In OpenShift Container Platform 4.17, it is now generally available.

For information on configuring host groups at installation, see [VMware vSphere host group enablement](../installing/installing_vsphere/ipi/installing-vsphere-installer-provisioned-customizations.xml#installation-vsphere-regions-zones-host-groups_installing-vsphere-installer-provisioned-customizations).

For information on configuring host groups for existing clusters, see [Specifying multiple host groups for your cluster on vSphere](../installing/installing_vsphere/post-install-vsphere-zones-regions-configuration.xml#specifying-host-groups-vsphere_post-install-vsphere-zones-regions-configuration).

Installing a cluster on AWS European Sovereign Cloud (Technology Preview)
You can now install OpenShift Container Platform on Amazon Web Services (AWS) in the European Sovereign Cloud (EUSC) region (`eusc-de-east-1`). The AWS EUSC region is separate and independent from other AWS regions, with all the infrastructure located within the European Union (EU). You must specify a custom Amazon Machine Image (AMI) in the `platform.aws.defaultMachinePlatform.amiID` field of your `install-config.yaml` file. Other limitations also apply. The AWS EUSC region is available as a Technology Preview feature.

For more information, see [AWS EUSC](../installing/installing_aws/installing-aws-account.xml#installation-aws-eusc_region_installing-aws-account).

Installing a cluster on Google Cloud with N4A machine types
With this update, you can install a OpenShift Container Platform cluster on Google Cloud with N4A machine types.

N4A Virtual Machines (VMs) use highly efficient Arm-based processors. N4A machines deliver exceptional performance compared to current-generation x86-based VMs, making them ideal for containerized applications and microservices on OpenShift Container Platform.

For more information, see [Tested instance types for Google Cloud](../installing/installing_gcp/installing-gcp-customizations.xml#installation-gcp-tested-machine-types_installing-gcp-customizations) and [N4A machine series (Google documentation)](https://docs.cloud.google.com/compute/docs/general-purpose-machines#n4a_series).

Installing a cluster using Red Hat Enterprise Linux (RHEL) 10
With this update, you can install a cluster using RHEL version 10 as the base image for all machines in the cluster. This feature is available as a Technology Preview. To enable this feature, enable the `TechPreviewNoUpgrade` feature set and set the `osImageStream` parameter to `rhel-10` in your `install-config.yaml` file.

For more information, see [Installation configuration parameters](../installing/install_config/installation-config-parameters-generic.xml#installation-config-parameters-generic).

Adding custom alerts to `oc adm upgrade recommend` command output
With this update, you can add the `openShiftUpdatePrecheck` label to alerts in a `PrometheusRule` custom resource (CR) so that, when you run the `oc adm upgrade recommend` command, any firing alerts with this label appear in the command output.

For more information, see [Adding custom alerts to `oc adm upgrade recommend` command output](../updating/preparing_for_updates/updating-cluster-prepare.xml#oc-adm-upgrade-recommend-custom-alert_updating-cluster-prepare).

Deploying virtualized control planes with KubeVirt Redfish (Technology Preview)
You can use KubeVirt Redfish to deploy OpenShift Container Platform clusters with control plane nodes running as virtual machines on a hosting cluster with OpenShift Virtualization. Running control plane nodes as VMs provides VM-level isolation for control plane components. KubeVirt Redfish exposes VMs through the standard Redfish API, enabling existing installation methods such as installer-provisioned infrastructure, Agent-based Installer, and GitOps Zero Touch Provisioning (ZTP) to manage VM power states and boot media. The feature is available as a Technology Preview.

For more information, see [Understanding virtualized control planes](../vcp/vcp-overview.xml#vcp-overview).

Bucketless workload identity for Google Cloud clusters
When installing or upgrading an OpenShift Container Platform cluster on Google Cloud with short-term credentials, you can now use the `--key-storage-method=pool-jwk-file` option with the `ccoctl gcp create-all` command to attach OIDC signing keys directly to the workload identity pool provider. This method eliminates the need to create a publicly accessible Google Cloud Storage (GCS) bucket for OIDC configuration, which reduces the public attack surface and can help meet security and network policies in restricted environments.

For more information, see [Creating GCP resources with the Cloud Credential Operator utility](../installing/installing_gcp/installing-gcp-customizations.xml#cco-ccoctl-creating-at-once_installing-gcp-customizations).

## Machine Config Operator

Boot nodes into a custom machine config pool
With this update, you can boot new nodes directly into a custom machine config pool. Before this update, you needed to create the node in the worker machine config pool, then move the node into the custom machine config pool, which requires a node reboot. By launching the node directly into the new pool, you save a node reboot cycle.

For information, see [Creating a custom machine config pool with a new node](../machine_configuration/machine-config-custom-mcp.xml#machine-config-custom-mcp-automatic_machine-config-creating-custom-mcp).

Boot image skew enforcement
With this update, the Machine Config Operator (MCO) examines the boot image version reported in the `MachineConfiguration` object to determine if that boot image is appropriate for the cluster. If the boot image version is too old, the Operator reports that boot image version skew is detected and blocks cluster updates until you manually update the boot image or disable boot image skew enforcement.

For more information, see [Boot image skew enforcement](../machine_configuration/mco-update-boot-skew-mgmt.xml#mco-update-boot-skew-mgmt).

Boot image management for control plane nodes is generally available
With this update, the boot image management feature for control plane nodes is generally available. With boot image management enabled, you can configure your cluster to update the node boot image whenever you update your cluster. Before this update, boot image management was supported for worker nodes only. Boot image management for control plane nodes was introduced in OpenShift Container Platform 4.21 for AWS, Google Cloud, and Azure clusters, and is now generally available for the platforms in 4.22. The boot image management feature for control plane nodes is not supported for VMware vSphere.

For more information, see [Boot image management](../machine_configuration/mco-update-boot-images.xml#machine-configs-configure).

Boot image management for worker nodes is now default for Azure and vSphere
With this update, the boot image management feature for worker nodes is default behavior in Azure and vSphere clusters. As such, after updating to OpenShift Container Platform 4.22, the boot images in your cluster are automatically updated to version 4.22. With subsequent updates, the Machine Config Operator (MCO) again updates the boot images in your cluster. Any new nodes you create after updating are based on the new version. Current nodes are not affected by this feature.

Before updating to 4.22, you must acknowledge this change or opt-out of this default behavior before proceeding. For information on opting out, see [Disabling boot image management](../machine_configuration/mco-update-boot-images.xml#mco-update-boot-images-disable_machine-configs-configure).

For more information on the boot image management feature, see [Boot image management](../machine_configuration/mco-update-boot-images.xml#mco-update-boot-images_machine-configs-configure).

Boot image update documentation
With this update, the Machine Config Operator documentation contains procedures to update the boot image on compute nodes for most supported OpenShift Container Platform platforms.

For OpenShift Container Platform platforms that do not support automatic boot image updating or for clusters configured with the boot image management feature disabled, you can manually update the boot image used by the compute nodes in your cluster.

For more information, see [Manually updating the boot image](../machine_configuration/mco-update-boot-images-manual.xml#mco-update-boot-images-manual).

`AppliedFilesAndOS` machine config node condition is now `AppliedFiles` and `AppliedOSImage` (Technology Preview)
With this update, the `AppliedFilesAndOS` condition reported by the machine config node has been split into the `AppliedFiles` and `AppliedOSImage` conditions as a Technology Preview feature. The machine config nodes custom resource monitors the progress of machine configuration updates to nodes. The `AppliedFiles` condition reports whether MCO has updated files on the node. The `AppliedOSImage` condition reports whether the MCO has updated the operating system.

For more information, see [About node status during updates](../machine_configuration/index.html#checking-mco-node-status_machine-config-overview).

## Machine management

## Monitoring

## Networking

Network policy enhancement
To reduce the cluster attack surface and ensure predictable network behavior, OpenShift Container Platform now enforces least-privilege network policies on critical networking components. Starting in 4.22, OpenShift Container Platform includes default `NetworkPolicy` objects in some of its own namespaces. Specifically, the operators that manage cluster DNS and cluster Ingress automatically install and maintain default deny-all `NetworkPolicy` objects in their respective namespaces.

<div class="important">

Because these namespaces now operate on a deny-by-default model, any unmanaged or custom pods running in these namespaces will have their network traffic blocked. Do not modify the default `NetworkPolicy` objects that OpenShift Container Platform includes in its own namespaces by default.

</div>

To check the namespaces that include the objects by default, you can run the following command:

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

Tune MetalLB advertisements for individual LoadBalancer services using service labels
With MetalLB, you can now set `spec.serviceSelectors` on `BGPAdvertisement` and `L2Advertisement` custom resources (CRs). This allows you to match LoadBalancer services by label so each advertisement applies its own BGP or Layer 2 settings to the services you choose, even when those services use the same IPAddressPool.

For more information, see [About advertising for the IP address pools](../networking/ingress_load_balancing/metallb/about-advertising-ipaddresspool.xml#about-advertise-for-ipaddress-pools).

Immutable AWS Network Load Balancer for a service
With this release, when deploying a service with the AWS Load Balancer the `service.beta.kubernetes.io/aws-load-balancer-type` annotation is immutable for existing services. To change the load balancer type, you must recreate the service.

BGP EVPN for cluster user-defined networks
With this release, Border Gateway Protocol Ethernet Virtual Private Network (BGP EVPN) is available for primary cluster user-defined networks. Enabling this feature on OpenShift Container Platform allows a `ClusterUserDefinedNetwork` overlay network to use the EVPN control plane for deeper integration with the data center network.

For more information, see [About BGP EVPN for primary cluster user-defined networks](../networking/advanced_networking/bgp_evpn_udn/about-bgp-evpn-user-defined-networks.xml#about-bgp-evpn-user-defined-networks).

NoOverlay mode with BGP routing
With this release, no-overlay mode with Border Gateway Protocol (BGP) routing is available as a Technology Preview feature on bare-metal clusters that use OVN-Kubernetes. No-overlay mode forwards layer 3 pod traffic on the underlay network using BGP-learned routes instead of Geneve encapsulation, which can improve east-west performance. You can enable no-overlay mode on the default layer 3cluster network and on primary `ClusterUserDefinedNetwork` resources.

For more information, see [Improve east-west performance by routing pods on the underlay with BGP](../networking/advanced_networking/bgp_routing/no-overlay-mode-bgp-routing.xml#no-overlay-mode-bgp-routing).

## Nodes

Image pull credential verification in multi-tenant clusters
With this update, administrators can use the `imagePullCredentialsVerificationPolicy` parameter in a `KubeletConfig` custom resource to enforce credential verification for cached images. This parameter forces the kubelet to re-authenticate with the container registry before it deploys a pod, ensuring that the requesting namespace has valid access rights to the image.

The underlying `KubeletEnsureSecretPulledImages` feature gate is enabled by default. Administrators can configure specific credential provider policies to balance security and stability:

- `AlwaysVerify`: Enforces credential checks for all image pull requests.

- `NeverVerifyAllowlistedImages`: Enforces credential checks for user workloads while exempting essential infrastructure images on an allowlist.

  Before this update, multi-tenant OpenShift Container Platform clusters had a security vulnerability where the kubelet did not re-verify credentials for cached images. If one tenant pulled a private image, another tenant could deploy a pod by using that same cache without providing image pull secrets. To mitigate this previously, administrators relied on unsupported configurations. However, these workarounds caused cluster instability, risked control plane failures during registry outages, and blocked crucial cluster upgrades.

  <div class="note">

  Do not use the `NeverVerifyPreloadedImages` policy when the default `KubeletEnsureSecretPulledImages` feature gate is active, as the policy might not function as expected. Use the `NeverVerifyAllowlistedImages` policy instead.

  </div>

  For more information, see [Creating a KubeletConfig CRD to edit kubelet parameters](../machine_configuration/machine-configs-custom.xml#create-a-kubeletconfig-crd-to-edit-kubelet-parameters_machine-configs-custom).

CPU resource enforcement is now enabled by default
With this update, the `system-reserved-compressible` parameter is enabled for all clusters that do not use the reserved CPU feature. This addresses previous issues where the system reserved CPU exceeded the desired limit. This default can be overridden by configuring the `systemReservedCPU: ""` parameter in a kubelet configuration.

For more information, see [How OpenShift Container Platform enforces system-reserved CPU](../nodes/nodes/nodes-nodes-resources-configuring.xml#system-reserved-compressible_nodes-nodes-resources-configuring).

Mount an OCI image into a pod
With this update, you can use an image volume to mount an Open Container Initiative (OCI)-compliant artifact directly into a pod. OCI artifacts enable users to store and distribute arbitrary files and metadata using OCI compliant container registries.

For more information, see [Mounting OCI images and artifacts into a pod](../nodes/pods/nodes-pods-image-volume.xml#nodes-pods-image-volume).

Configurable storage locations for CRI-O artifacts
With this update, you can create additional, non-default artifact storage locations in CRI-O that your pods can pull from. By using storage locations for the CRI-O container engine other than the default for OCI artifacts, complete container images, or container image layers, you can reduce application startup time and make your applications run more efficiently.

For more information, see [Additional CRI-O storage locations for faster container startup](../nodes/nodes/nodes-nodes-additional-crio-storage.xml#nodes-nodes-additional-crio-storage).

Project-scoped image pull secrets for mirrored registries (Technology Preview)
With this update, you can pull images from mirrored registries by using project-scoped pull secrets as a technology preview feature. Before this update, you needed to use node-level secrets when pulling from a mirrored registry because the kublet does not recognize the mirror configuration, which is configured at the container-runtime level.

For more information, see [Configuring project-scoped image pull secrets for mirrored registries](../openshift_images/image-configuration.xml#images-configuration-registry-mirror-project-secret_image-configuration).

Partitionable devices are now supported with dynamic resource allocation (Technology Preview)
With this update, the dynamic resource allocation feature supports partitioning physical hardware into smaller, logical instances, such as Multi-Instance GPUs, based on workload demands. With this technology preview feature, you can safely and efficiently share GPUs across multiple pods.

For more information, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

## OpenShift CLI (oc)

Digest-based image pinning for the oc-mirror v2 plugin
With this update, the oc-mirror v2 plugin pins Operator catalog images by their digest in your `ImageSetConfiguration` custom resource. Pinning by digest ensures that you always deploy the same Operator catalog image, regardless of any later changes to the upstream tags. For more information, see [Mirroring images for a disconnected installation by using the oc-mirror plugin v2](../disconnected/about-installing-oc-mirror-v2.xml#oc-mirror-workflows-partially-disconnected-v2_about-installing-oc-mirror-v2).

Configuration of custom target repositories and tags for additional images by using the oc-mirror v2 plugin
With this update, when using the oc-mirror v2 plugin, you can provide custom destination repository path and tag for specific images. By using the new `targetRepo` and `targetTag` fields within the `additionalImages` section of your `ImageSetConfiguration` custom resource, you can specify the target repository and tag for an image in your target mirror registry. For more information, see [ImageSet configuration parameters for oc-mirror plugin v2](../disconnected/about-installing-oc-mirror-v2.xml#oc-mirror-imageset-config-parameters-v2_about-installing-oc-mirror-v2).

Availability of the `oc mirror list` command in oc-mirror v2 plugin
With this update, you can use the list support feature with the oc-mirror v2 plugin. You can run the `oc mirror list` command to explore available platform and Operator content, including their specific versions, from remote and local registries. For more information, see [Creating the image set configuration](../disconnected/about-installing-oc-mirror-v2.xml#oc-mirror-building-image-set-config-v2_about-installing-oc-mirror-v2).

## Operator development

## Postinstallation configuration

Support for the PCI addresses of NICs in `BareMetalHost` hardware data
With this release, the Peripheral Component Interconnect (PCI) address for each network interface controller (NIC) is available in two separate custom resources (CRs). The PCI address is located in the `status.hardware.nics[]` section of the `BareMetalHost` CR and in the `spec.hardware.nics[]` section of the `HardwareData` CR. While these are separate resources, the values in the `pciAddress` fields, for example `0000:00:03.0`, are identical.

For more information, see [About the BareMetalHost resource](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#bmo-about-the-baremetalhost-resource_bare-metal-postinstallation-configuration) and [The BareMetalHost status](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#the-baremetalhost-status).

Red Hat Bare Metal as a Service for OpenShift is generally available
With this update, Red Hat Bare Metal as a Service for OpenShift, formerly known as Bare Metal as a Service (BMaaS), is generally available. You can provision and manage bare-metal hosts by using the Metal<sup>3</sup> API and the Bare Metal Operator (BMO). These hosts, external to the OpenShift Container Platform cluster, can run workloads that might not be suitable for containerization or virtualization, such as legacy applications or applications that require direct hardware access. For more information, see [Using Red Hat Bare Metal as a Service for OpenShift](../installing/installing_bare_metal/bare-metal-using-bare-metal-as-a-service.xml#bare-metal-using-bare-metal-as-a-service).

Expanding bare-metal clusters using OCI images and Red Hat Bare Metal as a Service for OpenShift (Technology Preview)
With this update, you can expand your bare-metal cluster using Red Hat Bare Metal as a Service for OpenShift with images from an OCI registry as a Technology Preview feature. You can use images from public OCI registries or from the built-in cluster registry. For more information, see [Using Red Hat Bare Metal as a Service for OpenShift](../installing/installing_bare_metal/bare-metal-using-bare-metal-as-a-service.xml).

Adding an ARM node to an x86 bare metal cluster
With this update, you can add ARM nodes to bare metal clusters with x86 control planes using PXE or virtual media. You can expand your cluster by creating a `BareMetalHost` object with the `aarch64` architecture, and then scaling the machine set to deploy the new machine.

For more information, see [Preparing the bare metal node](../installing/installing_bare_metal/bare-metal-expanding-the-cluster.xml#preparing-the-bare-metal-node_bare-metal-expanding).

## Red Hat Enterprise Linux CoreOS (RHCOS)

RHCOS uses RHEL 9.8
With this update, RHCOS uses Red Hat Enterprise Linux (RHEL) 9.8 packages in OpenShift Container Platform 4.22. These packages ensure that your OpenShift Container Platform instances receive the latest fixes, features, enhancements, hardware support, and driver updates.

RHCOS 10.2 support (Technology Preview)
With this update, you can configure your cluster to use RHCOS 10.2 as a Technology Preview feature. You can update the nodes in an existing non-production test cluster or install a new non-production test cluster. For more information, see [Setting the RHCOS version in a cluster](../machine_configuration/mco-image-streams.xml#mco-image-streams).

Ignition update to version 2.26.1
With this update, the Ignition utility is updated to version 2.26.1.

Butane update to version 0.26.0
With this update, the Butane utility is updated to version 0.26.0.

Afterburn update to version 5.10.0
With this update, the Afterburn utility is updated to version 5.10.0.

coreos-installer update to version 0.26.0
With this update, the coreos-installer utility is updated to version 0.26.0.

Support for the numad package
With this update, the numad package is supported. numad is an automatic NUMA affinity management daemon. It monitors NUMA topology and resource usage within a system that dynamically improves NUMA resource allocation, management, and system performance.

## Scalability and performance

NUMA-aware scheduler supports clusters with up to 500 nodes
With this release, you can scale the NUMA-aware secondary scheduler to support clusters with up to 500 nodes. The scheduler defaults to a `Burstable` quality of service (QoS) profile, which reduces baseline resource consumption while allowing the scheduler to scale up during peak loads.

For more information, see [Topology-aware scheduler scalability](../scalability_and_performance/cnf-numa-aware-scheduling.xml#cnf-topology-aware-scheduler-scalability_numa-aware).

<!-- -->

CRI-O ExecCPUAffinity protects low-latency workloads from exec process interruption
With this release, you can protect latency-sensitive workloads from performance degradation caused by `oc exec` and shell processes. When you apply a `PerformanceProfile`, the CRI-O `ExecCPUAffinity` feature automatically pins exec processes to a designated CPU within the container’s allocated set, preventing them from running on your workload CPUs. This feature is enabled by default for `Guaranteed` QoS pods with whole-integer CPU requests and requires no additional configuration. You can disable it per profile by adding the `performance.openshift.io/exec-cpu-affinity: "disable"` annotation to the `PerformanceProfile`.

For more information, see [How `ExecCPUAffinity` prevents latency spikes from exec operations](../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#cnf-exec-cpu-affinity_cnf-tuning-low-latency-nodes-with-perf-profile).

## Support

Custom image configuration for the Support Log Gather
With this update, you can collect diagnostic data by using custom images in the Support Log Gather. By pointing the `spec.imageStreamRef` field to an approved `ImageStream` tag, you can override the default image. The cluster administrators are responsible for creating and maintaining the list of allowed custom images by managing `ImageStream` resources in the Operator namespace. Each custom image requires its own `MustGather` custom resource and a service account with permissions to access the `ImageStream`. For more information, see [Configuring a Support Log Gather instance](../support/gathering-cluster-data.xml#support-log-gather-config-cli_gathering-cluster-data).

## Storage

### New VolumeSnapshotClass csi-gce-pd-vsc-images is generally available

By default, you cannot restore more than six volumes per snapshot per hour. So in Kubevirt environments, you normally cannot create more than six VMs per hour from a "golden image" (templates saved as snapshots).

For Google Cloud Platform (GCP) persistent disk (PD) storage Container Storage Interface (CSI), there is now a non-default `VolumeSnapshotClass`, named `csi-gce-pd-vsc-images`, that uses the `snapshot-type: images` parameter. When using KubeVirt, it allows you to overcome the six VMs per hour restriction, so that you can create VMs from "golden images".

This feature is generally available in OpenShift Container Platform 4.22.

For more information, see [Volume snapshots CRD: VolumeSnapshotClass](../storage/container_storage_interface/persistent-storage-csi-snapshots.xml#volume-snapshot-crds).

### Support for Hyperdisk Balanced High Availability volumes is generally available

OpenShift Container Platform 4.22 introduces support for Hyperdisk Balanced High Availability volumes as generally available.

Hyperdisk Balanced High Availability volumes are useful for:

- Protecting your applications from a zonal outage by synchronously replicating data across two zones in the same region

- When you require write access to the same volume in multiple zones

For more information, see [Hyperdisk-balanced high availability disks overview](../storage/container_storage_interface/persistent-storage-csi-gcp-pd.xml#persistent-storage-csi-gcp-hyperdisk-ha-overview_persistent-storage-csi-gcp-pd).

### Local Storage Operator symlinks management is generally available

To prevent storage breakage during OpenShift Container Platform upgrades, OpenShift Container Platform 4.22 provides a mechanism, the `LocalVolumeDeviceLink` Custom Resource Definition, to detect, alert, and remap broken symlinks without manual node-level intervention.

The Local Storage Operator (LSO) traditionally creates persistent volumes (PVs) based on `/dev/disk/by-id/` paths, following the assumption that they are stable. However, Linux kernel updates, firmware updates, or `udev` rule changes can cause these supposedly stable names to change or disappear.

Administrators have the following notification and correction options to deal with symlink disruptions:

- Monitoring: (default) If the current and preferred path do not match, an alert occurs, but no changes occur to the current path.

- Use existing path: Alerts are silenced and LSO uses the existing path.

- Recreate symlinks: Symlinks are recreated to point to the new, updated device path.

For more information, see [Local Storage Operator symlinks management](../storage/persistent_storage_local/persistent-storage-local.xml#local-storage-symlinks-top-level_persistent-storage-local).

### Mutable CSI node allocatable property is generally available

This feature allows for dynamically updating the maximum number of storage volumes a node can handle. Without this feature, volume limits are essentially immutable when a node first joins the cluster. If the environment changes—for example, if you attach a new network interface (ENI) that shares a hardware "slot" with your storage—OpenShift Container Platform does not recognize it has fewer slots available for disks, leading to pods becoming stuck.

This feature is only supported on AWS Elastic Block Storage (EBS).

Mutable CSI node allocatable property was introduced in OpenShift Container Platform 4.21 as a Technical Preview feature. In OpenShift Container Platform 4.22, it is supported as generally available.

### European Sovereign Cloud (EUSC) region (Technology Preview)

European Sovereign Cloud (EUSC) region acts as a "digital fortress" built within a specific country’s borders. Sovereign Clouds are specifically designed to meet strict legal, jurisdictional, and security requirements of a particular nation or entity.

In the context of storage, EUSC ensures that all data, including primary storage, backups, and the resulting metadata, resides physically within the specific nation’s borders and remains exclusively under its legal jurisdiction.

For OpenShift Container Platform 4.22, only AWS Elastic Block Storage supports EUSC. AWS Elastic File Storage (EFS) is not supported.

EUSC is supported as a Technology Preview feature.

For more information about EUSC, see [Support for European Sovereign Cloud (EUSC) region](../storage/container_storage_interface/persistent-storage-csi-ebs.xml#support-for-european-sovereign-cloud-eusc-region).

## Web console

Support for integrated OCI chart interaction
The OpenShift Container Platform web console now fully supports browsing, inspecting, and installing Open Container Initiative (OCI)-based Helm charts directly from configured repositories to provide functional parity with traditional HTTP(S) Helm charts. This enhancement removes the previous discovery-only limitation, enabling users to interact with and deploy OCI-based charts seamlessly within the console’s repository views.

For more information, see [Configuring custom Helm chart repositories](../applications/working_with_helm_charts/configuring-custom-helm-chart-repositories.xml#configuring-custom-helm-chart-repositories).

Azure Resource Group field for operator installations on Azure WIF clusters
The operator installation page now includes a **Resource Group** field for operators who have the `token-auth-azure` annotation enabled on Azure Workload Identity Federation (WIF) clusters. As a result, operators who require an Azure resource group value, such as `ODF` (NooBaa), can complete their setup without manual workarounds.

Install Helm charts from a direct URL
In the web console, you can now install a Helm chart directly from a URL, without first adding the chart to a Helm chart repository or the console catalog. Both `oci://` and `https://` URLs are supported.

<div class="warning">

Installing a Helm chart from a direct URL bypasses the validation checks provided by the developer catalog. Install charts only from URLs you trust, because unverified charts can introduce security risks to your cluster. When possible, use charts from the developer catalog or a configured Helm repository instead.

</div>

# Notable technical changes

This section includes several technical changes for OpenShift Container Platform 4.17.

Platform components and Operators now use dedicated service accounts
Most OpenShift Container Platform platform components and Operators have been updated to use dedicated service accounts instead of the `default` service account. This change follows the principle of least privilege, simplifies security audits, and reduces the risk of accidental permission elevation by ensuring that platform identities are isolated from user workloads.

The following dynamic tools continue to use the `default` service account to ensure operational efficiency:

- `oc debug`: Uses the `default` service account to avoid the performance overhead of creating and removing unique service accounts for short-lived troubleshooting sessions.

- `oc adm must-gather`: Uses the `default` service account to collect diagnostic data across the cluster without requiring extensive manual RBAC modifications.

For more information, see [Default project service accounts and roles](../authentication/using-service-accounts-in-applications.xml#default-service-accounts-and-roles_using-service-accounts).

Unused Cluster API Operator image removed from release image
With this update, the OpenShift Container Platform release image no longer includes the `cluster-api-operator` image. As a result, you can no longer pull this image from the release image manually. If you mirror the release image, you can delete this image from your mirror. ([OCPBUGS-61949](https://redhat.atlassian.net/browse/OCPBUGS-61949))

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

| Feature                                                              | 4.20               | 4.21               | 4.22       |
|----------------------------------------------------------------------|--------------------|--------------------|------------|
| `ImageContentSourcePolicy` (ICSP) objects                            | Deprecated         | Deprecated         | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/zone`   | Deprecated         | Deprecated         | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/region` | Deprecated         | Deprecated         | Deprecated |
| Dynamic Accelerator Slicer (DAS) Operator                            | Technology Preview | Technology Preview | Removed    |

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

As an alternative, use the [oc-mirror plugin v2](../disconnected/about-installing-oc-mirror-v2.xml#about-installing-oc-mirror-v2).

Deprecation of adding kernel modules to nodes with KVC
As of OpenShift Container Platform 4.22, support for adding kernel modules to nodes with kmods-via-containers software (KVC) has been deprecated and will be removed in a future release.

# Removed features

This section includes removed features for OpenShift Container Platform 4.17.

Deprecation and Removal of Dynamic Accelerator Slicer (DAS)
The Dynamic Accelerator Slicer (DAS) Operator was introduced to allow dynamic GPU partitioning in OpenShift Container Platform until the Dynamic Resource Allocation (DRA) partitionable device feature is available. With the DRA feature available as a technology preview feature in OpenShift Container Platform 4.17, the DAS Operator has been deprecated and removed.

For more information on DRA, see [Allocating GPUs to pods by using DRA](../nodes/pods/nodes-pods-allocate-dra.xml#nodes-pods-allocate-dra).

# Fixed issues

The following issues are fixed for this release:

## API Server and Authentication

- Before this update, the `oc explain authentication` command displayed incorrect descriptions for the OpenID Connect (OIDC) provider fields. With this release, all field descriptions are corrected. As a result, the multiline comments are combined into a single line for improved YAML generation which provides better `oc explain` output. ([OCPBUGS-56851](https://redhat.atlassian.net/browse/OCPBUGS-56851))

## Bare Metal Hardware Provisioning

- Before this update, when provisioning an NVIDIA DGX B200 bare-metal node using Advanced Cluster Management, the bare-metal host (BMH) could get stuck in a `Provisioning` state. With this release, the credential detection has been updated to detect missing credentials errors that were not being detected previously. ([OCPBUGS-62309](https://redhat.atlassian.net/browse/OCPBUGS-62309))

- Before this update, the cluster deletion got stuck during the inspection phase due to a power off stage transition. As a consequence, the cluster was not deleted. With this release, the bare-metal host (BMH) is prevented from getting stuck during deletion in a ZTP environment. ([OCPBUGS-65571](https://redhat.atlassian.net/browse/OCPBUGS-65571))

- Before this update, the resource ID for physical network interface controllers (NICs) on bare-metal machines using the HPE iLO6 system could change unpredictably when rebooting the machine. With this release, the resource ID stays the same after reboots. ([OCPBUGS-70226](https://redhat.atlassian.net/browse/OCPBUGS-70226))

- Before this update, when performing a firmware update on a bare-metal machine by updating the `HostFirmwareController` configuration, if the `HostUpdatePolicy` was set to `onReboot`, the Bare Metal Operator (BMO) would sometimes fail to initiate the reboot and firmware upgrade. With this release, the BMO initiates the reboot and performs the firmware upgrade. ([OCPBUGS-75006](https://redhat.atlassian.net/browse/OCPBUGS-75006))

- Before this update, when a physical network interface was enslaved to a bridge the interface and bridge shared the same MAC address. As a consequence, the provisioning interface detection would match both the interface and bridge and concatenate their names into an invalid multi-line value, which prevented the ironic service from starting. Because the ironic service could not start, workers could not PXE boot and agent-based installation failed with `SyncingFailed`. With this release, the bash text-parsing logic is replaced with a Python script using the `ip -json -d` command for structured output, which correctly selects a single interface when there are multiple matches for a MAC or IP address. As a result, agent-based installation on a bare-metal node completes successfully in bridged network configurations. ([OCPBUGS-77528](https://redhat.atlassian.net/browse/OCPBUGS-77528))

- Before this update, when provisioning a bare-metal machine, if you provided a network data Secret that was missing an `nmstate` key, the network data would be discarded silently, leading to unexpected errors. With this release, if the `nmstate` key is missing, the Image Customization Controller will generate an error informing you that the `nmstate` key is required to complete provisioning. ([OCPBUGS-77840](https://redhat.atlassian.net/browse/OCPBUGS-77840))

- Before this update, the bootstrap machine created during a bare-metal installation did not have a serial console log file. If the bootstrap machine failed and SSH access was not available, the logs were inaccessible. With this release, the bootstrap machine creates a serial console log file that is accessible to the must-gather diagnostic tool. ([OCPBUGS-78589](https://redhat.atlassian.net/browse/OCPBUGS-78589))

- Before this update, Baremetal Operator’s virtual media baseboard management controller (BMC) drivers required the `bootMACAddress` parameter for inspection, making it impossible to perform automatic MAC discovery. As a consequence, you were required to manually specify MAC addresses to inspect a bare-metal host (BMH) configured with virtual media based provisioning. With this release, the virtual media BMC drivers make the `bootMACAddress` parameter optional for hardware inspection. As a result, virtual media BMC BMHs can now be successfully created and inspected without requiring the `bootMACAddress` parameter, making it possible to discover MAC addresses automatically (for example, for use with O-Cloud Manager). Note that the `bootMACAddress` parameter is still required in install-config, installer-provisioned infrastructure (IPI) installations and assisted-installer installations. ([OCPBUGS-78785](https://redhat.atlassian.net/browse/OCPBUGS-78785))

- Before this update, metrics for the Cluster Baremetal Operator were exposed on all network interfaces on a bare-metal host. With this release, the metrics are only exposed to the `localhost` interface so that the `kube-rbac-proxy` sidecar can access the metrics. ([OCPBUGS-84924](https://redhat.atlassian.net/browse/OCPBUGS-84924))

## Cluster Autoscaler

- Before this update, the cluster autoscaler processed paused node groups as if they were active, which could lead to the wrong nodes being deleted. With this release, the cluster autoscaler identifies paused node groups and does not act upon them, preventing incorrect node deletion. ([OCPBUGS-78152](https://redhat.atlassian.net/browse/OCPBUGS-78152))

## etcd

- Before this update, the etcd Operator randomly removed control plane nodes, which caused duplication and potential cluster downtime. As a consequence, service disruptions might have caused the loss of control plane nodes in the etcd cluster. With this release, the etcd Operator prioritizes removing members in the same failure domain index, which reduces potential duplication and improves cluster stability. As a result, the etcd Operator ensures that the control plane remains stable with three nodes, which prevents potential service disruptions. ([OCPBUGS-73857](https://issues.redhat.com/browse/OCPBUGS-73857))

- Before this update, the etcd Operator allowed member deletion and removed pre-drain hooks during a revision rollout. As a consequence, cluster degradation occurred during simultaneous machine deletion, causing API unavailability. With this release, the Cluster Member Removal Controller logic is updated to prevent deletion during a revision rollout. As a result, cluster degradation during the `OnDelete` rollout is fixed, ensuring smooth vertical scaling. ([OCPBUGS-74151](https://issues.redhat.com/browse/OCPBUGS-74151))

## Installer

## Kube Controller Manager

## Kube Scheduler

## Kube Storage Version Migrator

- Before this update, the storage version migrator pod did not have a node selector configured, causing it to run on worker nodes instead of control plane nodes. As a consequence, this OpenShift Container Platform component did not follow the standard placement pattern for platform components. With this release, the migrator pod includes a node selector to schedule on control plane nodes. As a result, the storage version migrator pod runs on control plane nodes alongside other OpenShift Container Platform components. ([OCPBUGS-84312](https://redhat.atlassian.net/browse/OCPBUGS-84312))

## Networking

## Clock state metrics degrade correctly after upstream clock loss

## Node Tuning Operator

## OpenShift API Server

## Web console

Guided Tours respect a console capability setting
In previous releases, the web console displayed Guided Tours by default, even in environments where users already know OpenShift Container Platform, such as shared clusters. In OpenShift Container Platform 4.22, cluster administrators can enable or disable Guided Tours by configuring the console `GuidedTourFeature` capability.

[CONSOLE-4986](https://issues.redhat.com/browse/CONSOLE-4986)

## Storage

vSphere CSI driver operator metrics endpoint incorrectly returns 500 error
Previously, the vSphere container storage interface (CSI) driver operator’s metrics endpoint (port 8445) returned "HTTP 500" (Internal Server Error) when accessed without authentication, instead of the expected "HTTP 401" (Unauthorized/Forbidden).

This occurred because the service account lacked permission to create `subjectaccessreviews` resources, causing the authorization check itself to fail, rather than properly rejecting the unauthorized request. This issue has been resolved by adding the missing RBAC permissions to the vSphere CSI driver operator’s `ClusterRole`.

[OCPBUGS-60159](https://redhat.atlassian.net/browse/OCPBUGS-60159)

Azure CSI stray volume attachment prevents pod starts
Previously, after a node reboot, a pod may fail to start with "Multi-Attach" error, even though the volume is not attached to any node.

This was fixed by adding LUN verification to prevent race conditions during disk attachment.

Now, pods start successfully after a node reboot.

[OCPBUGS-74936](https://redhat.atlassian.net/browse/OCPBUGS-74936)

Azure CSI driver indefinite hang during volume detach after node deletion
Previously, a fix for dangling volumes (OCPBUGS-67165) introduced a regression where the `ControllerUnpublish` operation could continue indefinitely when waiting for a disk’s `ManagedBy` field to clear. This occurred if the disk was reassigned to another node during the detach operation, causing the wait loop to never exit since `ManagedBy` pointed to the new node instead of becoming NULL.

This issue has been resolved by checking whether the disk’s `ManagedBy` field points to a different node than the one being detached from. If so,the detach operation is considered complete, allowing volumes to properly clear the "detaching" state and be scheduled on new nodes.

[OCPBUGS-85193](https://redhat.atlassian.net/browse/OCPBUGS-85193)

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

| Feature                                                | 4.20               | 4.21                 | 4.22                 |
|--------------------------------------------------------|--------------------|----------------------|----------------------|
| Boot image management for Azure and vSphere            | Technology Preview | General Availability | General Availability |
| Boot image management for control plane nodes          | Not available      | Technology Preview   | General Availability |
| Image mode for OpenShift status reporting improvements | Not available      | Technology Preview   | Technology Preview   |
| Overriding storage or partition setup                  | Not available      | Technology Preview   | Technology Preview   |

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

Networking Technology Preview tracker

## Node Technology Preview features

| Feature                                                   | 4.20               | 4.21                 | 4.22                 |
|-----------------------------------------------------------|--------------------|----------------------|----------------------|
| `MaxUnavailableStatefulSet` featureset                    | Technology Preview | Technology Preview   | Technology Preview   |
| Default sigstore `openshift` cluster image policy         | Technology Preview | General Availability | General Availability |
| Attribute-Based GPU Allocation                            | Technology Preview | General Availability | General Availability |
| Project-scoped image pull secrets for mirrored registries | Not Available      | Not Available        | Technology Preview   |
| Partitionable device DRA support                          | Not Available      | Not Available        | Technology Preview   |

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

- Currently, the `topo-aware-scheduler` provided by the NUMA Resources Operator (NRO) does not support Kubernetes priority-based preemption. When all NUMA zones on available nodes are fully consumed by lower-priority pods, a high-priority pod with a `PreemptLowerPriority` policy remains in `Pending` state indefinitely instead of preempting the lower-priority pods. As a consequence, workloads that depend on priority-based preemption for scheduling recovery do not function correctly when using the `topo-aware-scheduler`. ([OCPBUGS-77930](https://issues.redhat.com/browse/OCPBUGS-77930))

- OpenShift Container Platform does not support restoring volume snapshots in a topology domain that does not have access to the datastore where the snapshot resides. You must manually schedule pods that use a persistent volume claim (PVC) that restore a snapshot to a region and zone with the snapshot. Using a shared datastore across all regions and zones meets this requirement. ([OCPBUGS-84702](https://issues.redhat.com/browse/OCPBUGS-84702))

# Asynchronous errata updates

Security, bug fix, and enhancement updates for OpenShift Container Platform 4.17 are released as asynchronous errata through the Red Hat Network. All OpenShift Container Platform 4.17 errata is [available on the Red Hat Customer Portal](https://access.redhat.com/downloads/content/290/). See the [OpenShift Container Platform Life Cycle](https://access.redhat.com/support/policy/updates/openshift) for more information about asynchronous errata. Red Hat Customer Portal users can enable errata notifications in the account settings for Red Hat Subscription Management (RHSM). When errata notifications are enabled, users are notified through email whenever new errata relevant to their registered systems are released.

<div class="note">

Red Hat Customer Portal user accounts must have systems registered and consuming OpenShift Container Platform entitlements for OpenShift Container Platform errata notification emails to generate.

</div>

This section will continue to be updated over time to provide notes on enhancements and bug fixes for future asynchronous errata releases of OpenShift Container Platform 4.17. Versioned asynchronous releases, for example with the form OpenShift Container Platform 4.17.z, will be detailed in subsections. In addition, releases in which the errata text cannot fit in the space provided by the advisory will be detailed in subsections that follow.

<div class="important">

For any OpenShift Container Platform release, always review the instructions on [updating your cluster](../updating/updating_a_cluster/updating-cluster-web-console.xml#updating-cluster-web-console) properly.

</div>
