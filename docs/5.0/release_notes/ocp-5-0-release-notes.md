Red Hat OpenShift Container Platform provides developers and IT organizations with a hybrid cloud application platform for deploying both new and existing applications on secure, scalable resources with minimal configuration and management. OpenShift Container Platform supports a wide selection of programming languages and frameworks, such as Java, JavaScript, Python, Ruby, and PHP.

Built on Red Hat Enterprise Linux (RHEL) and Kubernetes, OpenShift Container Platform provides a more secure and scalable multitenant operating system for today’s enterprise-class applications, while delivering integrated application runtimes and libraries. OpenShift Container Platform enables organizations to meet security, privacy, compliance, and governance requirements.

# About this release

OpenShift Container Platform ([RHEA-2026:4893](https://access.redhat.com/errata/RHEA-2026:4893)) is now available. This release uses [Kubernetes 1.36](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.36.md) with CRI-O runtime. New features, changes, and known issues that pertain to OpenShift Container Platform 4.17 are included in this topic.

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

This topic lists new features and enhancements in OpenShift Container Platform 4.17.

This release adds improvements related to the following components and concepts:

## AI applications

Troubleshooting NIDS issues with an AI agent
You can use the netedge toolset in the MCP server for OpenShift Container Platform to diagnose Network Ingress and DNS (NIDS) issues by describing symptoms to a connected LLM client in natural language.

For more information, see [Troubleshooting NIDS issues with an AI agent](../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-ingress-controller.xml#ai-driven-networking-troubleshooting_configuring-ingress-cluster-traffic-ingress-controller).

MCP server for Red Hat OpenShift Container Platform is generally available
When a problem occurs on your OpenShift Container Platform cluster, you want to determine exactly what is happening, so that you can fix the issue as soon as possible. The MCP server for Red Hat OpenShift Container Platform feature provides an AI tool for this purpose to quickly and easily diagnose your OpenShift Container Platform cluster.

New features include:

- Declarative lifecycle management through the MCP Lifecycle Operator using a single MCPServer custom resource, instead of managing multiple Kubernetes manifests or Helm charts.

- Safe, automated rollouts for MCP server version upgrades, with status and health reporting for each deployment.

- MCP gateway integration (Red Hat Connectivity Link), aggregating MCP servers behind a single endpoint with authentication and rate limiting.

- RBAC-enforced, read-only operation, restricting the server to non-mutating actions.

- Expanded toolsets, including `netedge` for Network Ingress and DNS (`NIDS`) troubleshooting, `ossm` for OpenShift Service Mesh (Kiali) mesh inspection, `tekton`, alongside the core and config toolsets.

- Support for latest (2026-07-28) MCP server specification.

  OpenShift Container Platform 4.22 introduced MCP server for Red Hat OpenShift Container Platform as a Technology Preview feature. For 5.0, this feature is generally available.

  For more information, see [Inspect clusters with MCP server for Red Hat OpenShift Container Platform](../ai_applications/mcp_server/mcp-server-overview.xml).

## Authentication and authorization

Advanced direct authentication fields are now generally available
Advanced direct authentication fields for OIDC-based authentication are now generally available for standalone and hosted control plane (HCP) clusters. These fields, which include custom OIDC discovery URLs, CEL-based claim mapping and validation rules, and user validation rules, no longer require the `TechPreviewNoUpgrade` feature set.

For more information, see [Advanced direct authentication fields](../authentication/structured-auth-config-fields.xml#structured-auth-config-fields).

External claims sourcing for external OIDC authentication (Technology Preview)
Clusters that use external OIDC authentication can now retrieve user identity information, such as group memberships, from sources beyond the identity provider’s JSON Web Token (JWT). Cluster administrators can configure external claims sources in the `Authentication` resource to fetch user attributes from endpoints such as UserInfo or Microsoft Graph APIs when JWT size limits prevent including all claim data. This feature requires the `TechPreviewNoUpgrade` feature set.

Component-scoped proxy for authentication is now available as a Technology Preview
You can configure a dedicated proxy for the authentication stack to reach external identity providers instead of the cluster-wide egress proxy. Setting the `spec.proxy` field on the `Authentication` Operator resource limits proxy-based egress to the Cluster Authentication Operator and the OAuth server. This feature requires the `AuthenticationComponentProxy` feature gate, enabled by the `TechPreviewNoUpgrade` feature set.

For more information, see [Configuring proxy settings for the authentication stack](../authentication/configuring-authentication-proxy.xml#configuring-authentication-proxy).

## Autoscaling

Cluster autoscaler enforcement of node group minimum size
You can configure the cluster autoscaler to keep each node group at or above the `minReplicas` value in the corresponding `MachineAutoscaler` resource, including when the cluster autoscaler considers the nodes unneeded, by setting the `enforceNodeGroupMinSize` parameter to `Enabled` in the `ClusterAutoscaler` custom resource.

The default value is `Disabled`. When `Disabled`, the cluster autoscaler can scale a node group below the `minReplicas` value if it considers the nodes unneeded.

For more information, see [Cluster autoscaler resource definition](../machine_management/applying-autoscaling.xml#cluster-autoscaler-cr_applying-autoscaling).

Per-project overcommit ratios for the Cluster Resource Override Operator
You can create a `ResourceOverride` object in a project to set CPU and memory override ratios that differ from the cluster-wide ratios. New pods in that project that have a specific label get these override ratios. New pods that do not have the label use the cluster-wide ratios. Existing pods keep their current requests and limits until you re-create them.

<!-- -->

Pause and restart the Verical Pod Autoscaler
You can pause Verical Pod Autoscaler (VPA) behavior without uninstalling the Operator or removing any vertical pod autoscalers by deleting the `VerticalPodAutoscalerController` CR. You can restart the VPA by re-creating the CR.

<!-- -->

etcd selectable database size
When large or high-churn workloads approach the default 8 GiB limit, you can increase the etcd backend database quota up to 16 GiB. After you increase the quota, you cannot decrease it.

For more information, see [Selectable etcd database size for large clusters](../etcd/etcd-performance.xml#etcd-selectable-db_etcd-performance).

## Extensions (OLM v1)

OLM v1 uses cluster administrator permissions to manage extensions
You no longer need to create a service account or configure service account permissions for each cluster extension.

Operator Lifecycle Manager (OLM) v1 uses the Operator Controller service account with cluster administrator permissions to install and manage extensions.

Use role-based access control (RBAC) and validating admission policies to control access to cluster extension resources.

Cluster extension installation and update deadlines (Technology Preview)
You can set installation and update deadlines for cluster extensions in Operator Lifecycle Manager (OLM) v1 as a Technology Preview feature.

Use the `spec.progressDeadlineMinutes` field in a `ClusterExtension` object to specify the deadline in minutes.

If an installation or update exceeds the deadline, OLM v1 reports `ProgressDeadlineExceeded` in the `Progressing` status condition. This message indicates that the installation or update needs manual intervention.

Default catalog images match the cluster version
Operator Lifecycle Manager (OLM) v1 selects image tags for default Operator catalogs based on the cluster version. On OpenShift Container Platform 5.0 clusters, the default catalogs use the `v5.0` image tag.

<!-- -->

The IBM Power® release on OpenShift Container Platform 4.17 adds improvements and new capabilities to OpenShift Container Platform components
New features on IBM Power® include:

- Custom Metrics Autoscaler Operator (KEDA) on IBM Power®

- Dual Operating Stream on IBM Power®

  - IBM Power®9 requires RHEL version 9 stream

  - IBM Power®10 and IBM Power®11 may use either RHEL version 9 or RHEL version 10 stream

<!-- -->

The IBM Z® and IBM® LinuxONE release on OpenShift Container Platform 4.17 adds improvements and new capabilities to OpenShift Container Platform components
New features on IBM Z® and IBM® LinuxONE include:

Self-service Technical Supportability Review
You can use the self-service Technical Supportability Review (TSR) on the Red Hat Customer Portal to validate your cluster configuration against Red Hat common practices. The self-service TSR uses AI to evaluate your cluster’s `must-gather` data and provides a prioritized executive summary that identifies your cluster’s top risks and recommends corrective actions. The TSR performs hundreds of checks across the OpenShift Container Platform platform, including OpenShift Virtualization, and coverage is continually expanding.

For more information, see [Technical Supportability Review with AI tool](https://access.redhat.com/support/cases/#/analyze) and [Red Hat Technical Supportability Review with AI: Proactive AI-Driven Cluster Assessments for OpenShift Container Platform](https://access.redhat.com/solutions/7141255). \* SR-IOV Network Operator support for IBM Z® and IBM® LinuxONE \* Custom Metrics Autoscaler Operator (KEDA) on IBM Z® \* Dual Operating Stream on IBM Z®

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

Google Cloud installations support global KMS keys for control plane and compute pool disk encryption
Google Cloud installations accept global-location Key Management Service (KMS) keys for control plane and compute machine pool disk encryption. When you specify KMS keys in the `defaultMachinePlatform` field in the `install-config.yaml` file, the installation program now uses these keys to encrypt the image registry and storage. These keys must be regional; global KMS keys are not supported for the default machine platform because they encrypt Google Cloud Storage (GCS) buckets, which require regional keys. However, when you specify KMS keys in the control plane or compute machine pool configurations, these keys can be either regional or global because they encrypt Compute Engine persistent disks, which support global KMS keys.

For more information, see [Installation configuration parameters for Google Cloud](../installing/installing_gcp/installation-config-parameters-gcp.xml#installation-config-parameters-gcp).

RHOSO token authentication
You can now use OpenStack Identity API v3 token authentication for clusters deployed on RHOSO.

For more information, see "Defining parameters for the installation program" in "Installing a cluster on OpenStack with customizations".

Dual-stack networking on Amazon Web Services (AWS) is generally available
With this release, dual-stack networking support for OpenShift Container Platform clusters on Amazon Web Services (AWS) is generally available. Dual-stack networking allows clusters to use both IPv4 and IPv6 addresses for network traffic.

Dual-stack networking on AWS was introduced in OpenShift Container Platform 4.22 with Technology Preview status. In OpenShift Container Platform 5.0, it is now generally available.

For more information, see [Installation configuration parameters for AWS](../installing/installing_aws/installation-config-parameters-aws.xml#installation-config-parameters-aws).

Updated support for Nutanix AOS and Prism Central versions
With this release, OpenShift Container Platform now supports version 7.6 for Nutanix AOS and Prism Central. No changes are required for existing deployments.

For more information, see [Nutanix version requirements](../installing/installing_nutanix/preparing-to-install-on-nutanix.xml#installation-nutanix-infrastructure_preparing-to-install-on-nutanix).

Installing a cluster using Red Hat Enterprise Linux (RHEL) 10 is generally available
With this update, you can install a cluster using RHEL version 10 as the base image for all machines in the cluster. To enable this feature, set the `osImageStream` parameter to `rhel-10` in your `install-config.yaml` file.

Installing a cluster using Red Hat Enterprise Linux (RHEL) 10 was introduced in OpenShift Container Platform 4.22 with Technology Preview status. In OpenShift Container Platform 5.0, it is now generally available.

For more information, see [Installation configuration parameters](../installing/install_config/installation-config-parameters-generic.xml#installation-config-parameters-generic).

VMware Cloud Foundation 9.1 support
You can install and run OpenShift Container Platform 4.17 on VMware Cloud Foundation (VCF) 9.1.

For more information, see [VMware vSphere infrastructure requirements](../installing/installing_vsphere/ipi/ipi-vsphere-installation-reqs.xml#installation-vsphere-infrastructure_ipi-vsphere-installation-reqs).

vCenter in-place upgrades on VMware vSphere clusters
OpenShift Container Platform clusters deployed on VMware vSphere now support vCenter in-place upgrades from vCenter 8 to vCenter 9 without requiring cluster redeployment. When you perform this upgrade, all cluster nodes remain in the `Ready` state, all cluster operators remain available, and the vSphere Container Storage Interface (CSI) driver continues to operate without interruption. No OpenShift Container Platform configuration changes are required.

This support applies to vCenter in-place upgrades only. vCenter server replacement scenarios are not covered by this feature.

For more information, see [VMware vSphere infrastructure requirements](../installing/installing_vsphere/ipi/ipi-vsphere-installation-reqs.xml#installation-vsphere-infrastructure_ipi-vsphere-installation-reqs).

Creating cluster update assessments with OpenShift Lightspeed
With this release, as a Technology Preview you can use the agentic OpenShift Lightspeed-driven **Cluster Update** page on the web console to check update availability, evaluate compatibility with your cluster, and produce an update assessment that you can review as you prepare for a cluster update.

For more information, see [Creating cluster update assessments with OpenShift Lightspeed](../updating/updating_a_cluster/update-ai.xml#updating-ai).

## Machine Config Operator

Overriding storage or partition setup is generally available
With this update, the overriding storage or partition setup feature is generally available. With this feature, you can change the installed disk partition schema, file systems, and RAID configurations for new nodes.

For more information, see [Overriding storage and partition setup](../machine_configuration/machine-configs-configure.xml#machine-config-install-time-configs_machine-configs-configure).

Updated boot images for AWS Marketplace now supported
Updated boot images are now supported for clusters that use AWS Marketplace boot images. With this feature, you can configure your cluster to update the node boot image whenever you update your cluster. By default, the boot image in your cluster is not updated along with your cluster.

For more information, see [Boot image management](../machine_configuration/mco-update-boot-images.xml#mco-update-boot-images).

Network policy support for the Machine Config Operator
The Machine Config Operator now has multiple network policies that control network traffic to and from the Operator and operand pods. These policies restrict traffic to only traffic that is explicitly allowed or required.

Paused machine config pools report on-cluster image build status
With this update, a paused machine config pool reports the progress of an on-cluster custom layered image build in the machine config pool status. You can confirm that the build succeeded before you unpause the pool and roll the image out to nodes. When the affected machine config pool is paused, if the build fails or is interrupted, the nodes keep their current operating system image.

For more information, see [Build an on-cluster custom layered image without rolling it out](../machine_configuration/mco-coreos-layering.xml#coreos-layering-configuring-on-build-paused_mco-coreos-layering).

Boot loader updates for Secure Boot clusters created on OpenShift Container Platform 4.15 or earlier
With this update, the Machine Config Operator updates the boot loader on `x86_64` and ARM nodes before it applies a new operating system image. The operator does this for clusters that were created on OpenShift Container Platform 4.15 or earlier and have Secure Boot enabled. The update covers existing nodes and nodes that start from an older boot image.

The automatic boot loader update in RHCOS does not update a boot loader that is already installed from an older boot image. Boot images used after OpenShift Container Platform 4.15.23 and 4.16 already include the current Secure Boot certificates.

Before this update, nodes in these clusters did not boot the new operating system image, because the installed boot loader did not trust the certificates used to sign that image.

As a result, those nodes can start and update to the new operating system image.

## Machine management

Virtual machine compute nodes without vSphere integration
With this release, support for adding platform-agnostic virtual machine (VM) compute nodes to an existing OpenShift Container Platform cluster on VMware vSphere is generally available. You can install Red Hat Enterprise Linux CoreOS (RHCOS) on the VMs and add them to the cluster without vSphere integration. This extends the existing support for adding bare-metal compute nodes.

You must provision and replace these compute nodes manually. Before you add the nodes, migrate workloads that use the native vSphere Container Storage Interface (CSI) driver to an alternative storage solution. Then disable the native CSI driver for the entire cluster.

For more information, see [Add compute machines without vSphere integration](../machine_management/user_infra/adding-bare-metal-compute-vsphere-user-infra.xml#adding-bare-metal-compute-vsphere-user-infra).

## Networking

Gateway API CRDs updated to version 1.5.1
With this release, OpenShift Container Platform updates the managed Gateway API custom resource definitions (CRDs) to version 1.5.1. The Gateway API controller is initially based on Red Hat OpenShift Service Mesh 3.4 and Istio 1.30.

This release adds support for the following Gateway API version 1.5.1 features:

- `TLSRoute` resources that route TLS traffic by matching the Server Name Indication (SNI) hostname, typically for passthrough scenarios where the backend, rather than the gateway, terminates TLS.

- A Cross-Origin Resource Sharing (CORS) filter on `HTTPRoute` resources that configures CORS headers by using a built-in filter.

- `ReferenceGrant` resources at the stable `gateway.networking.k8s.io/v1` API version.

For more information, see [Understand Gateway API](../networking/ingress_load_balancing/configuring_gateway_api/understand-gateway-api.xml#understand-gateway-api_understand-gateway-api).

<!-- -->

OVN-Kubernetes exposes user-defined network (UDN) scale metrics
With this release, OVN-Kubernetes exposes Prometheus scale metrics for user-defined network (UDN) `NetworkAttachmentDefinition` (NAD) sync, node annotation updates, and northbound database (NBDB) programming. Use the metrics to find bottlenecks when you create or scale user-defined networks. These metrics are available from the `ovnkube-cluster-manager` and `ovnkube-controller` metrics endpoints when you enable OVN-Kubernetes scale metrics. The following metrics are available:

- `ovnkube_clustermanager_udn_nad_sync_duration_seconds`

- `ovnkube_clustermanager_udn_update_node_annotation_duration_seconds`

- `ovnkube_controller_udn_nbdb_programmed_duration_seconds`

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

OVN-Kubernetes and CNI diagnostics toolsets for the MCP server for Red Hat OpenShift is generally available
With this release, you can troubleshoot OVN-Kubernetes networking issues in OpenShift Container Platform by using the `ovn-kubernetes` and `cni-diagnostics` toolsets in the Open MCP server for Red Hat OpenShift.

The `ovn-kubernetes` toolset provides tools to inspect OVN and Open vSwitch state, including logical flow listing, OVN database queries, and traffic tracing with `ovn-trace`. The `cni-diagnostics` toolset provides kernel-level networking diagnostics and packet capture, including conntrack inspection, iptables and nftables rule listing, `iproute2` queries, `tcpdump`, and eBPF-based packet tracing with `pwru`.

For more information, see [Troubleshooting OVN-Kubernetes with the MCP server](../networking/ovn_kubernetes_network_provider/troubleshooting-ovn-kubernetes-with-mcp-server.xml#troubleshooting-ovn-kubernetes-with-mcp-server).

High availability for PTP boundary clocks with dual time receiver ports on Intel E810 hardware
You can configure dual time receiver (TR) ports on a single Intel Westport Channel E810-XXVDA4T network interface controller (NIC) for Precision Time Protocol (PTP) Telecom Boundary Clock (T-BC) high availability. This configuration uses the Alternate Best Master Clock Algorithm (A-BMCA) to support automatic switchover between upstream paths if the active port fails or its quality degrades. As a result, downstream devices maintain continuous time synchronization without manual intervention during upstream path failures.

The `PtpConfig` custom resource (CR) uses a two-profile architecture with a time receiver profile and a time transmitter profile on separate PTP domains. Both TR ports share the same Physical Hardware Clock (PHC), so failover relies on A-BMCA reselection rather than switching between separate clock servos.

For more information, see [Configuring PTP boundary clock high availability with dual time receiver ports](../networking/advanced_networking/ptp/configuring-ptp.xml#ptp-configuring-linuxptp-services-dual-port-bc_configuring-ptp).

<!-- -->

High availability for PTP boundary clocks with dual time receiver ports on Intel Granite Rapids-D hardware (Technology Preview)
You can configure dual time receiver (TR) ports on Intel Granite Rapids-D (GNR-D) hardware, such as the Dell XR8720t with Intel E830 Carter Flat NICs, for Precision Time Protocol (PTP) Telecom Boundary Clock (T-BC) high availability. This configuration uses the Alternate Best Master Clock Algorithm (A-BMCA) to support automatic switchover between upstream paths if the active port fails or its quality degrades.

The GNR-D configuration uses a `PtpConfig` custom resource (CR) with two profiles and a `HardwareConfig` CR to define the Digital Phase-Locked Loop (DPLL) clock chain and holdover parameters.

For more information, see [Configuring linuxptp services as a boundary clock on Intel Granite Rapids-D hardware](../networking/advanced_networking/ptp/configuring-ptp.xml#ptp-configuring-linuxptp-services-as-boundary-clock-gnrd_configuring-ptp).

<!-- -->

Telecom Grandmaster on Intel Granite Rapids-D with field-tunable timing parameters (Technology Preview)
With this release, you can deploy a Precision Time Protocol (PTP) Telecom Grandmaster (T-GM) clock on Intel Granite Rapids-D (GNR-D) hardware, such as the Dell PowerEdge XR8720t platform. You can tune precision timing parameters in the field without upgrading the base kernel or firmware, which makes it easier to maintain timing performance in production telco environments. This feature is available as a Technology Preview.

To configure the deployment, you create a `HardwareConfig` custom resource (CR) alongside the `PtpConfig` CR. The `HardwareConfig` CR exposes field-tunable holdover thresholds, Global Navigation Satellite System (GNSS) source settings, and digital phase-locked loop (DPLL) parameters. You can also verify DPLL synchronization and Clock Class state transitions, monitor timing metrics, and troubleshoot GNSS connectivity and DPLL synchronization failures.

For more information, see [Configuring the HardwareConfig CR for a Telecom Grandmaster clock on Intel Granite Rapids-D hardware](../networking/advanced_networking/ptp/configuring-ptp.xml#nw-ptp-configuring-field-tunable-timing-parameters-gnrd_configuring-ptp).

<!-- -->

Updated IPv6 support policy
OpenShift Container Platform supports IPv6, including single-stack and dual-stack networking, wherever the underlying infrastructure platform provides IPv6. This model applies across OpenShift Container Platform deployment models.

IPv6 is fully supported on the following platforms, where the platform provides IPv6 connectivity:

- Bare-metal, user-provisioned, and platform-agnostic clusters, when the customer network provides IPv6

- VMware vSphere

- Red Hat OpenStack Platform (RHOSP)

- IBM Power® and IBM PowerVC

- IBM Z® and IBM® LinuxONE

- IBM Cloud® classic infrastructure

- Oracle® Cloud Infrastructure (OCI)

IPv6 is supported with platform-specific limitations on the following platforms:

- Amazon Web Services (AWS): Dual-stack cluster installation remains a Technology Preview feature. Dual-stack installation is not supported in AWS Wavelength Zones. Classic Load Balancers do not support IPv6. For service-level IPv6 support, see [Amazon Web Services (AWS) services that support IPv6](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ipv6-support.html).

- Microsoft Azure: Dual-stack virtual networks are supported. IPv6-only virtual machines are not supported. For additional Azure IPv6 limitations, see [Microsoft Azure IPv6 limitations](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/ipv6-overview#limitations).

- Google Cloud: Dual-stack and IPv6-only addressing are available for some services. For the service matrix, see [Google Cloud IPv6 support](https://docs.cloud.google.com/vpc/docs/ipv6-support).

- Alibaba Cloud: Dual-stack VPCs are supported. IPv6-only VPCs are not supported. See [Alibaba Cloud VPC FAQ](https://www.alibabacloud.com/help/en/vpc/frequently-asked-questions).

- Nutanix: Guest IPv6 is supported only on unmanaged (Network Controller) VLAN subnets when the physical fabric provides IPv6. Basic VLAN subnets do not support IPv6. See [Nutanix Prism VMs summary view](https://portal.nutanix.com/page/documents/details?targetId=Prism-Central-Guide-vpc_7_3:mul-explore-vm-view-pc-r.html).

- Oracle® Compute Cloud@Customer and Oracle® Edge Cloud: IPv6 is limited to SR-IOV virtual network interface cards (VNICs). See [Oracle® Compute Cloud@Customer October 2025 release notes](https://docs.oracle.com/iaas/releasenotes/compute-cloud-at-customer/release-note-m3-12-oct2025.htm).

- OpenShift Virtualization: Support for single-stack IPv6 clusters is limited to the OVN-Kubernetes `localnet` topology and the Linux bridge Container Network Interface (CNI) plugin.

IPv6 is not available on the following platforms because the vendor does not provide IPv6:

- Microsoft Azure Stack Hub. See [Azure Stack Hub networking](https://learn.microsoft.com/en-us/azure-stack/user/azure-stack-network-overview).

- IBM Cloud® VPC infrastructure. See [IBM Cloud® VPC limitations](https://cloud.ibm.com/docs/vpc?topic=vpc-limitations) and [Comparing classic and VPC infrastructure](https://cloud.ibm.com/docs/infrastructure-hub?topic=infrastructure-hub-compare-infrastructure).

- IBM Power® Virtual Server. Private subnets are documented as IPv4 CIDR only. See [Configuring a private network subnet](https://cloud.ibm.com/docs/power-iaas?topic=power-iaas-configuring-subnet).

- Oracle Database Appliance (ODA). See [Oracle Database Appliance Networks FAQ](https://docs.oracle.com/en/engineered-systems/oracle-database-appliance/19.22/cmtrx/faqs-oracle-database-appliance-networks.html).

For OVN-Kubernetes dual-stack configuration requirements that apply to all IPv6 clusters, see [OVN-Kubernetes IPv6 and dual-stack limitations](../networking/ovn_kubernetes_network_provider/about-ovn-kubernetes.xml#nw-ovn-kubernetes-limitations_about-ovn-kubernetes).

Virtual Machines tab on Network details pages
With this release, you can monitor secondary networks and manage Kubernetes services in the web console, removing the need for manual YAML authoring and disjointed navigation.

You can view all workloads associated with a specific network directly from the new **Virtual Machines** tab by navigating to any secondary network’s details page (including `NetworkAttachmentDefinition` \[NAD\], `UserDefinedNetwork` \[UDN\], or `ClusterUserDefinedNetwork` \[CUDN\]) by clicking its name under the Virtual Machine’s **Configuration** → **Network** tab.

[OCPNETUI-16](https://issues.redhat.com/browse/OCPNETUI-16)

Service and route management
You can build new services using an interactive form alongside a live, side-by-side YAML preview. You can monitor service and route status at a glance with backend health indicators now integrated directly into the **Services** and **Routes** list views.

[OCPNETUI-16](https://issues.redhat.com/browse/OCPNETUI-16)

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

Resilient Image Mirror Fallback for Connection and Registry Errors
Image pulls that use `ImageDigestMirrorSet` or `ImageTagMirrorSet` continue with the next configured mirror when a layer download fails because of a temporary registry error, rate limiting, or a missing layer. Authentication errors still stop the pull. No configuration change is required.

For more information, see [Understanding image registry repository mirroring](../openshift_images/image-configuration.xml#images-configuration-registry-mirror_image-configuration).

Container image signature verification with sigstore
For validated telco core Operators, you can use `ClusterImagePolicy` or `ImagePolicy` custom resources to verify signatures for container images using the sigstore framework.

For more information, see [Manage secure signatures with sigstore](../nodes/nodes-sigstore-using.xml#nodes-sigstore-using).

## OpenShift CLI (oc)

Removal of oc-mirror plugin v1 documentation
The Red Hat Customer Portal no longer includes documentation for the oc-mirror plugin v1 because the oc-mirror plugin v1 is deprecated. Use the oc-mirror plugin v2 to mirror images for a disconnected installation.

For more information, see [Mirroring images for a disconnected installation by using the oc-mirror plugin v2](../disconnected/oc_mirror_v2/about-installing-oc-mirror-v2.xml#about-installing-oc-mirror-v2).

oc-mirror plugin v2 documentation
In future oc-mirror plugin v2 releases, the oc-mirror plugin v2 documentation is planned for delivery outside OpenShift Container Platform general availability releases.

For more information, see [oc-mirror release notes](../disconnected/oc_mirror_v2/oc-mirror-v2-release-notes.xml#oc-mirror-v2-release-notes).

## Operator lifecycle

Operator Update Planner
The Operator Update Planner adds lifecycle and compatibility information to the **Installed Operators** page in the web console. This information covers Operators installed with Operator Lifecycle Manager (OLM) Classic. When catalog metadata is available, you can view the current support phase, its end date, and compatibility with the current OpenShift Container Platform version. Use this information to plan Operator updates.

This feature is not available for hosted control planes.

Default catalog images match the cluster version
Operator Lifecycle Manager (OLM) Classic selects image tags for default Operator catalogs based on the cluster version. On OpenShift Container Platform 5.0 clusters, the default catalogs use the `v5.0` image tag.

## Red Hat Enterprise Linux CoreOS (RHCOS)

RHCOS uses RHEL 10.2
RHCOS uses Red Hat Enterprise Linux (RHEL) 10.2 packages in OpenShift Container Platform4.17 . These packages ensure that your OpenShift Container Platform clusters receive the latest fixes, features, enhancements, hardware support, and driver updates.

New installations of OpenShift Container Platform 4.17 use RHCOS 10.2 by default.

You can upgrade your OpenShift Container Platform cluster from version 4.x to 5.0, then update your nodes to use RHCOS 10.2. If you update nodes to RHCOS 10.2, you must move all of your nodes to RHCOS 10.2. Running a cluster with a mixture of RHCOS 9.x and 10.2 nodes is not supported.

> [!NOTE]
> You cannot update the RHCOS version in a cluster that is using the runC container runtime, because runC is deprecated in OpenShift Container Platform 5.0. You must configure your cluster to use the crun container runtime. For more information, see [Configuring the container runtime](../machine_configuration/machine-configs-custom.xml#config-container-runtime_machine-configs-custom).

You can upgrade your cluster from 4.x to 5.0, but not update any node to RHCOS 10.2. Downgrading from RHCOS 10.2 to RHCOS 9.x is not supported.

For more information on updating RHCOS, see [Updating the cluster to RHCOS 10.x](../machine_configuration/mco-image-streams.xml#mco-image-streams).

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

Priority-based preemption for the NUMA Resources Operator scheduler
You can now enable priority-based preemption for the NUMA Resources Operator scheduler by using the `preemptionMode` field in the `NUMAResourcesScheduler` custom resource. When enabled, the scheduler can preempt lower-priority pods to make room for higher-priority pods on resource-constrained nodes. This improves scheduling for critical workloads on resource-constrained nodes.

For more information, see [Scheduling critical workloads with preemption](../scalability_and_performance/cnf-numa-aware-scheduling.xml#cnf-numa-scheduler-preemption_numa-aware).

<!-- -->

LLC-aware CPU pinning for low latency workloads
You can configure the CPU Manager to prefer CPU cores that share the same last-level cache (LLC) domain. This alignment is best effort. If the CPU Manager cannot keep the allocated CPUs in one LLC domain, and the node has enough CPUs, it still admits the workload. Preferring cores in the same LLC domain can improve performance for low latency workloads. To request this alignment, set the `prefer-align-cpus-by-uncorecache` CPU Manager policy option in the `PerformanceProfile` resource. This feature was previously available as a Technology Preview and is now generally available in OpenShift Container Platform 5.0.

For more information, see [Configuring LLC-aware CPU pinning for low latency workloads](../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#cnf-configuring-llc-aware-cpu-pinning_cnf-tuning-low-latency-nodes-with-perf-profile).

## Technical Supportability Review

Self-service Technical Supportability Review
You can use the self-service Technical Supportability Review (TSR) on the Red Hat Customer Portal to validate your cluster configuration against Red Hat common practices. The self-service TSR uses AI to evaluate your cluster’s `must-gather` data and provides a prioritized executive summary that identifies your cluster’s top risks and recommends corrective actions. The TSR performs hundreds of checks across the OpenShift Container Platform platform, including OpenShift Virtualization, and coverage is continually expanding.

For more information, see [Technical Supportability Review with AI tool](https://access.redhat.com/support/cases/#/analyze) and [Red Hat Technical Supportability Review with AI: Proactive AI-Driven Cluster Assessments for OpenShift Container Platform](https://access.redhat.com/solutions/7141255).

## Edge computing

Topology Aware Lifecycle Manager now emits Kubernetes events during ClusterGroupUpgrade reconciliation
You can use TALM events to automate operational workflows that respond to cluster lifecycle changes. Events are emitted for key remediation milestones including policy remediation start, success, timeout, and validation failures at global, batch, and cluster scope. By integrating these events with Event-Driven Ansible through the Multicluster Global Hub Operator, you can replace polling-based automation with event-driven workflows that scale efficiently across large cluster fleets.

For more information, see [Automating workflows with Topology Aware Lifecycle Manager events](../edge_computing/cnf-talm-for-cluster-upgrades.xml#cnf-talm-events-overview_cnf-topology-aware-lifecycle-manager).

Virtualized control planes with KubeVirt Redfish is generally available
With this update, deploying virtualized control planes with KubeVirt Redfish is generally available.

This update also adds `bcrypt` hashed passwords for more secure authentication to the KubeVirt Redfish API.

For more information about virtualized control planes, see [Understanding virtualized control planes](../vcp/vcp-overview.xml#vcp-overview).

Control plane node replacement with the ClusterInstance custom resource
You can replace a failed control plane node on a bare-metal multi-node cluster by editing the `ClusterInstance` custom resource (CR). You remove the failed node and then add a replacement node. The cluster must keep an `etcd` quorum of at least two healthy control plane nodes. You can replace only one control plane node at a time.

For more information, see [Advanced managed cluster configuration with ClusterInstance resources](../edge_computing/ztp-advanced-install-ztp.xml#ztp-advanced-install-ztp).

<!-- -->

The cnf-tests image supports `arm64` for platform verification latency tests
The `cnf-tests` image (`registry.redhat.io/openshift4/cnf-tests-rhel9`) is now a multi-architecture image that supports both `x86_64` (amd64) and `aarch64` (arm64) nodes. You can now run CNF latency tests for platform verification on `aarch64` RAN distributed unit (DU) systems, such as NVIDIA GH200 platforms. The image pull path remains unchanged for all architectures, because the container runtime automatically resolves the correct architecture manifest.

You can pull and use the updated multi-architecture image on existing OpenShift Container Platform 4.20 and later clusters.

For more information, see [Performing latency tests for platform verification](../scalability_and_performance/cnf-performing-platform-verification-latency-tests.xml#cnf-performing-platform-verification-latency-tests).

O-Cloud Manager for infrastructure and cluster lifecycle management (Technology Preview)
OpenShift Container Platform 5.0 introduces the O-Cloud Manager as a Technology Preview feature. Deploying and managing bare-metal clusters individually across hundreds of edge sites is time-consuming and error-prone. The O-Cloud Manager addresses this with reusable cluster blueprints, site-specific overrides, and automated hardware selection from resource pools. As a result, you can automate provisioning, scaling, configuration, and updates across your fleet from a single hub cluster by using a GitOps workflow or O-RAN Alliance O2 IMS-compatible REST APIs.

For more information, see [Infrastructure and cluster lifecycle management with the O-Cloud Manager](../infrastructure_lifecycle_management/ocloud-understanding-the-ocloud-manager.xml#ocloud-understanding-the-ocloud-manager).

## Security

Quantum-safe key encapsulation support with ML-KEM is now available
OpenShift Container Platform 4.17 adds support for quantum-safe key encapsulation across all Go-based TLS servers in the platform. This implementation uses the `X25519MLKEM768` hybrid key encapsulation mechanism (KEM), which combines the post-quantum ML-KEM algorithm with the classical X25519 elliptic curve. This combination provides protection against both classical and quantum computing attacks without requiring any cluster administrator action.

The `X25519MLKEM768` group is enabled by default in the `Old`, `Intermediate`, and `Modern` predefined TLS security profiles. When a client supports ML-KEM, the TLS handshake automatically negotiates quantum-safe key exchange.

> [!IMPORTANT]
> `X25519MLKEM768` is not FIPS-approved. Components running in FIPS mode automatically ignore this group.

For more information, see [Configuring TLS security profiles](../security/tls-security-profiles.xml#tls-security-profiles).

Configurable PKI for platform certificates (Technology Preview)
With this release, you can configure cryptographic parameters (key algorithms, key sizes, and elliptic curves) for internally generated platform certificates by using the `PKI` custom resource. Configuration applies at the cluster-wide or per-category (signer, serving, and client certificates) level and can be set at installation time or changed after installation. Operators automatically reissue non-conforming certificates when the configuration changes. This capability is a Technology Preview feature.

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

Configurable secret rotation for the Secrets Store CSI Driver
You can configure secret rotation intervals to control how often mounted secrets are refreshed from external stores, or disable rotation completely. By default, secret rotation is enabled with a 2-minute polling interval.

You can set the `minimumRefreshAge` field from 1 to 31,560,000 seconds. Shorter intervals provide quick updates for frequently changing secrets, while longer intervals reduce transaction costs and performance overhead for infrequently changing secrets. When rotation is disabled, secrets are fetched only at initial pod mount time.

For more information, see [Configuring secret rotation for the Secrets Store CSI Driver](../storage/container_storage_interface/persistent-storage-csi-secrets-store.xml#secrets-store-configuring-rotation_persistent-storage-csi-secrets-store).

Workload Identity Federation support for the Secrets Store CSI Driver
You can configure the Secrets Store CSI Driver to use Workload Identity Federation (WIF) for secure, credential-free authentication to external secret management systems. The driver uses short-lived service account tokens with a specified audience to authenticate to external secret stores such as AWS, Microsoft Azure, Google Cloud, or HashiCorp Vault.

This release is based on upstream v1.6.1. The driver does not have privileges to create a service account token on behalf of the pod. Any mounting functionality relying on this privilege should be re-configured appropriately, for example, by configuring the token requests.

For more information, see [Configuring token requests for Workload Identity Federation](../storage/container_storage_interface/persistent-storage-csi-secrets-store.xml#secrets-store-configuring-token-requests_persistent-storage-csi-secrets-store).

Upcoming SELinux mount option default for RWO/RWX volumes
For OpenShift Container Platform 5.0, ReadWriteOnce (RWO) and ReadWriteMany (RWX) volumes use recursive relabeling by default. However, OpenShift Container Platform 5.1 is targeted to have RWO and RWX volumes use mount option by default.

Some pods might not start when SELinux mount option behavior is applied.

To prepare for a future upgrade to 5.1, cluster administrators **must** do one of the following or the upgrade will be blocked:

- Fix your applications, so that the upgrade is safe.

  OpenShift Container Platform reports SELinux-related conflicts when creating pods, and on running pods, to make you aware of potential conflicts, and to help you resolve them. For more information about this reporting, see the Red Hat Knowledgebase article [OpenShift reports alert SELinuxMountGAReadinessWorkloadsDetected and the cluster is not upgradeable. (Red Hat Knowledgebase)](https://access.redhat.com/solutions/7146569).

- Opt-out from the new default behavior, per pod or namespace.

  If you are unable to resolve the SELinux-related conflicts, you can proactively opt-out of the future move to mount option as default for selected pods or namespaces. To opt out, see [Opting out of the SELinux mount option default](../storage/understanding-persistent-storage.xml#using_selinuxChangePolicy_pod-opt-out_understanding-persistent-storage).

For more information about SELinux mount option for RWO/RWX, see [RWO and RWX and SELinux mount option](../storage/understanding-persistent-storage.xml#using_selinuxChangePolicy_overview-mount-option-rwo-rwx_understanding-persistent-storage).

Updated release of the Secrets Store CSI Driver Operator
The Secrets Store CSI Driver Operator version v5.0 is now based on the upstream version v1.6.1 release of secrets-store-csi-driver.

## Web console

Web console uses the PatternFly Project Felt theme and supports high contrast mode
The OpenShift Container Platform web console uses the PatternFly Project Felt theme by default. Project Felt aligns the look of Red Hat product interfaces more closely with the Red Hat brand. As a result, the web console has an updated visual style, and its layout and navigation stay the same. You can also turn on high contrast mode, which makes text and controls easier to see, on every console page, including the login page.

[OCPSTRAT-2962](https://issues.redhat.com/browse/OCPSTRAT-2962)

Web console limits on-screen notifications
In OpenShift Container Platform 5.0, the web console displays up to three notifications on the screen at one time, and keeps the rest in the notification drawer. You can also minimize supported notifications to the drawer without canceling the operation in progress.

[CONSOLE-5361](https://issues.redhat.com/browse/CONSOLE-5361), [CONSOLE-5424](https://issues.redhat.com/browse/CONSOLE-5424)

Web console uses the Helm v4 SDK
In OpenShift Container Platform 5.0, the web console uses the Helm v4 software development kit (SDK), which matches the Helm v4 CLI, the current version of the Helm CLI for OpenShift Container Platform. Existing charts continue to work.

[OCPSTRAT-2913](https://issues.redhat.com/browse/OCPSTRAT-2913)

Install a Helm chart from a URL that requires authentication
In OpenShift Container Platform 5.0, you can use the web console to install or upgrade a Helm release from a chart URL that requires Basic HTTP authentication. Previously, you could install a Helm release from a chart URL only if the chart did not require authentication. As a result, you can now install charts from private registries and servers by selecting or creating a secret that contains your credentials.

For more information, see [Installing a Helm release from a URL](../applications/working_with_helm_charts/odc-working-with-helm-releases.xml#odc-creating-helm-release-from-url_working-with-helm-releases).

[OCPSTRAT-3238](https://issues.redhat.com/browse/OCPSTRAT-3238)

# Notable technical changes

This section includes several technical changes for OpenShift Container Platform 4.17.

The NUMA Resources Operator validates the secondary scheduler image
Before this update, the NUMA Resources Operator did not validate the image that you set in the `spec.imageSpec` field of the `NUMAResourcesScheduler` custom resource (CR). Because this CR is cluster-scoped and the scheduler runs with high privileges, a user with write access to the CR could run an arbitrary container image with scheduler privileges.

With this release, the NUMA Resources Operator validates the scheduler image by default. The Operator accepts only digest-based image references, such as `registry.redhat.io/openshift4/noderesourcetopology-scheduler-rhel9@sha256:<digest>`, and the digest must match one of the trusted scheduler images that are embedded in the Operator for the current or previous release stream. If you specify an image that does not meet these requirements, the `NUMAResourcesScheduler` resource enters a `Degraded` state with the reason `InvalidSchedulerImage`.

> [!IMPORTANT]
> If you set a custom image in the `spec.imageSpec` field of the `NUMAResourcesScheduler` CR, for example, a tag-based reference, the resource enters a `Degraded` state after you upgrade to this release. To restore the scheduler, perform one of the following actions:
>
> - Update the `spec.imageSpec` field to reference the scheduler image by its `sha256` digest instead of a tag, and make sure that the image you are using is in the current production stream.
>
> - Add the digest of your custom image to the trusted list by setting the `SCHEDULER_IMAGE_DIGESTS` environment variable in the Operator subscription.
>
> - Disable validation by setting the `SCHEDULER_IMAGE_VALIDATION` environment variable to `false` in the Operator subscription. Disabling validation removes this security protection, so avoid it unless necessary.

For more information about the NUMA Resources Operator and the `NUMAResourcesScheduler` CR, see [Scheduling NUMA-aware workloads](../scalability_and_performance/cnf-numa-aware-scheduling.xml#cnf-numa-aware-scheduling). ([OCPBUGS-94176](https://issues.redhat.com/browse/OCPBUGS-94176))

The NUMA Resources Operator validates the Resource Topology Exporter image
Before this update, the NUMA Resources Operator did not validate the Resource Topology Exporter (RTE) image that you set in the `spec.imageSpec` field of the `NUMAResourcesOperator` custom resource (CR). Because the RTE runs as a daemon set on worker nodes with elevated read privileges, a user with write access to the CR could run an arbitrary container image with those privileges.

With this release, the NUMA Resources Operator does not allow a custom RTE image by default. If you set the exporter image in the `spec.imageSpec` field of the `NUMAResourcesOperator` CR, the resource enters a `Degraded` state with the reason `CustomUserImage` and the Operator does not reconcile the resource. Leave the `spec.imageSpec` field unset so that the Operator uses the default RTE image for your OpenShift Container Platform release. In a disconnected environment, the image mirroring configuration for the Operator container redirects the default image to your internal registry.

> [!IMPORTANT]
> If you set a custom image in the `spec.imageSpec` field of the `NUMAResourcesOperator` CR, the resource enters a `Degraded` state after you upgrade to this release. To restore the deployment, perform one of the following actions:
>
> - Remove the `spec.imageSpec` field from the `NUMAResourcesOperator` CR so that the Operator uses the default RTE image.
>
> - Disable validation by setting the `EXPORTER_IMAGE_RESTRICTION` environment variable to `false` in the Operator subscription. Disabling validation removes this security protection, so avoid it unless necessary.

For more information about the NUMA Resources Operator and the `NUMAResourcesOperator` CR, see [Scheduling NUMA-aware workloads](../scalability_and_performance/cnf-numa-aware-scheduling.xml#cnf-numa-aware-scheduling). ([OCPBUGS-94176](https://issues.redhat.com/browse/OCPBUGS-94176))

<!-- -->

KMS v2 encryption updates (Technology Preview)
Kubernetes KMS v2 encryption for etcd now uses an OLM-managed architecture where KMS plugins run as sidecar containers alongside the API server, configured through a `VaultKMSConfig` custom resource. This release adds direct migration between KMS providers, per-node KMS plugin health reporting, and pre-flight validation of KMS configuration changes. HashiCorp Vault Enterprise is the only supported KMS provider.

For more information, see [Configuring KMS encryption](../etcd/KMS_v2/kms-configuring.xml#kms-configuring).

Increase in leader elections
In this release, a new feature completes a preemptive leader transfer before attempting to defragment the leader. The purpose of the transfer is to lower the risk of a timeout-triggered leader election while the leader is unavailable during defragmentation. While a timeout-based leader election usually indicates a problem, the leader election that is caused by the transfer is an expedited leader election. It does not indicate a problem.

This feature safely causes leader elections to increase by, at most during normal operations, once per the etcd Operator defragmentation reconciliation cycle. This increase should not affect the existing `too many leader election` alerts. Those alerts are still a reliable indicator for whether the cluster is suffering from excessive, unexpected leader elections, which can potentially cause disruptions.

# Deprecated and removed features

This topic lists features that are deprecated or removed in OpenShift Container Platform 4.17.

## Extensions deprecated and removed features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| OLM v1 `ClusterExtension.spec.serviceAccount` field | General Availability | General Availability | Deprecated |

Extensions deprecated and removed tracker

## Images deprecated and removed features

| Feature                  | 4.21       | 4.22       | 5.0        |
|--------------------------|------------|------------|------------|
| Cluster Samples Operator | Deprecated | Deprecated | Deprecated |

Images deprecated and removed tracker

## Installation deprecated and removed features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| `--cloud` parameter for `oc adm release extract` | Deprecated | Deprecated | Deprecated |
| CoreDNS wildcard queries for the `cluster.local` domain | Deprecated | Deprecated | Deprecated |
| `compute.platform.openstack.rootVolume.type` for RHOSP | Deprecated | Deprecated | Deprecated |
| `controlPlane.platform.openstack.rootVolume.type` for RHOSP | Deprecated | Deprecated | Deprecated |
| `ingressVIP` and `apiVIP` settings in the `install-config.yaml` file for installer-provisioned infrastructure clusters | Deprecated | Deprecated | Deprecated |
| `platform.aws.preserveBootstrapIgnition` parameter for Amazon Web Services (AWS) | Deprecated | Deprecated | Deprecated |
| Installing a cluster on AWS with compute nodes in AWS Outposts | Deprecated | Deprecated | Deprecated |
| Installing a cluster using Fujitsu iRMC drivers on bare-metal machines | Deprecated | Deprecated | Deprecated |

Installation deprecated and removed tracker

## Machine Management deprecated and removed features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Confidential Computing with AMD Secure Encrypted Virtualization for Google Cloud | Deprecated | Deprecated | Deprecated |
| Managing bare-metal machines using Fujitsu iRMC drivers | Deprecated | Deprecated | Deprecated |

Machine management deprecated and removed tracker

## Networking deprecated and removed features

| Feature  | 4.21       | 4.22       | 5.0        |
|----------|------------|------------|------------|
| iptables | Deprecated | Deprecated | Deprecated |

Networking deprecated and removed tracker

## Node deprecated and removed features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| `ImageContentSourcePolicy` (ICSP) objects | Deprecated | Deprecated | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/zone` | Deprecated | Deprecated | Deprecated |
| Kubernetes topology label `failure-domain.beta.kubernetes.io/region` | Deprecated | Deprecated | Deprecated |
| Dynamic Accelerator Slicer (DAS) Operator | Technology Preview | Removed | Removed |
| Node Observability Operator | Technology Preview | Technology Preview | Removed |
| runC container runtime | General Availability | Deprecated | Deprecated |

Node deprecated and removed tracker

## OpenShift CLI (oc) deprecated and removed features

| Feature                         | 4.21                 | 4.22       | 5.0        |
|---------------------------------|----------------------|------------|------------|
| oc-mirror plugin v1             | Deprecated           | Deprecated | Deprecated |
| Docker v2 registries            | Deprecated           | Deprecated | Deprecated |
| `oc adm release mirror` command | General Availability | Deprecated | Deprecated |

OpenShift CLI (oc) deprecated and removed tracker

## Operator lifecycle and development deprecated and removed features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Red Hat Marketplace | Deprecated | Removed | Removed |
| SQLite database format for Operator catalogs | Deprecated | Deprecated | Deprecated |

Operator lifecycle and development deprecated and removed tracker

## Red Hat Enterprise Linux CoreOS (RHCOS) deprecated and removed features

| Feature   | 4.21 | 4.22 | 5.0        |
|-----------|------|------|------------|
| RHCOS 9.x | GA   | GA   | Deprecated |

RHCOS 9.x deprecated and removed tracker

## Workloads deprecated and removed features

| Feature                    | 4.21       | 4.22       | 5.0        |
|----------------------------|------------|------------|------------|
| `DeploymentConfig` objects | Deprecated | Deprecated | Deprecated |

Workloads deprecated and removed tracker

## Edge computing deprecated and removed features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| `PolicyGenTemplate` CR for GitOps ZTP policy management | General Availability | General Availability | Deprecated |

Edge computing deprecated and removed tracker

# Deprecated features

This topic lists features that are deprecated in OpenShift Container Platform 4.17.

`ClusterExtension` service account field is deprecated
As of OpenShift Container Platform 5.0, the `spec.serviceAccount` field in a `ClusterExtension` object is optional and deprecated. Operator Lifecycle Manager (OLM) v1 uses the Operator Controller service account with cluster administrator permissions to manage extensions.

Existing objects that specify this field continue to function, but OLM v1 ignores the field. Omit this field from new cluster extension configurations.

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

Deprecation of Red Hat Enterprise Linux CoreOS (RHCOS) 9.x
As of OpenShift Container Platform 5.0, support for RHCOS 9.x is deprecated and will be removed in OpenShift Container Platform 5.3. RHCOS 10.2 is the default operating system starting in OpenShift Container Platform 5.0. You can update any nodes running RHCOS 9.x to 10.2.

For more information on updating RHCOS, see: [Setting the RHCOS version in a cluster](../machine_configuration/mco-image-streams.xml#mco-image-streams).

Deprecation of Helm v3 CLI
As of OpenShift Container Platform 5.0, the Helm v3 CLI is deprecated. You can still use the Helm v3 CLI alongside the Helm v4 CLI in OpenShift Container Platform 5.0, but the Helm v3 CLI is not available in OpenShift Container Platform 5.1 and later.

For information about moving from Helm v3 to Helm v4, see [Helm CLI for Red Hat OpenShift compatibility matrix](https://access.redhat.com/articles/7145580).

# Removed features

This section includes removed features for OpenShift Container Platform 4.17.

## The adding kernel modules to nodes with kvc feature is removed

The adding kernel modules to nodes with kvc feature was deprecated in OpenShift Container Platform 4.22, and is now removed from OpenShift Container Platform 5.0.

## The Node Observability Operator is removed

The Node Observability Operator was a Technology Preview feature and is now removed from OpenShift Container Platform 5.0.

# Fixed issues

The following issues are fixed for this release:

## API Server and Authentication

- Before this update, the OAuth server login page displayed OKD branding instead of OpenShift branding. As a consequence, users saw incorrect branding on the login page. With this update, the Operator binary is built with the correct branding configuration. As a result, the OAuth server login page displays OpenShift branding as expected. ([OCPBUGS-69977](https://redhat.atlassian.net/browse/OCPBUGS-69977))

- Before this update, LDAP group sync using the RFC 2307 schema failed with a "Filter Compile Error" when `groupUIDAttribute` was set to `dn`. As a consequence, users could not sync LDAP groups despite following the documented configuration. With this update, filter validation is skipped for group queries that use `dn` as the group UID attribute. As a result, LDAP group sync with the RFC 2307 schema completes successfully. ([OCPBUGS-78768](https://redhat.atlassian.net/browse/OCPBUGS-78768))

## Bare Metal Hardware Provisioning

- Before this update, the `baremetal` cluster Operator did not set its `Progressing` status condition to `True` during cluster upgrades. As a consequence, the Cluster Version Operator (CVO) waited for the Operator without receiving proper progress signals, and upgrade monitoring tests failed. With this release, the `baremetal` Operator correctly reports `Progressing=True` during version changes. As a result, cluster upgrades proceed with accurate Operator status reporting. ([OCPBUGS-66101](https://redhat.atlassian.net/browse/OCPBUGS-66101))

- Before this update, when the bare-metal host (BMH) `spec.online` parameter was set to `False`, the Bare Metal Operator (BMO) forced the `ironic` service to issue a power-off command to the node at the end of inspection, after the RAM disk was ejected. As a consequence, the node operating system lost access to the boot media during shutdown, and filesystem corruption errors were visible on the BMH console. With this release, the node is powered off after inspection, while cleaning up the RAM disk, before ejecting Redfish virtual media. As a result, the host does not lose access to the boot media. ([OCPBUGS-66156](https://redhat.atlassian.net/browse/OCPBUGS-66156))

- Before this update, the Bare Metal Operator (BMO) `getChecksum()` function accepted non-empty checksums for Oracle Cloud Infrastructure (OCI) images. As a consequence, OCI image provisioning failed. With this release, a check in the `getChecksum()` function rejects non-empty user-provided checksums for OCI images. As a result, OCI image provisioning does not fail. ([OCPBUGS-84305](https://redhat.atlassian.net/browse/OCPBUGS-84305))

- Before this update, when managing a high volume of `BareMetalHost` resources on a single multicluster engine instance, the Bare Metal Operator (BMO) issued excessive requests to the Provisioner API during reconciliation. As a consequence, VirtualMedia injection and node reconciliation were noticeably slower at this scale. With this release, the BMO reconciliation loop is optimized to issue fewer requests to the Provisioner API. As a result, responsiveness improves when managing large numbers of `BareMetalHost` resources. ([OCPBUGS-85527](https://redhat.atlassian.net/browse/OCPBUGS-85527))

- Before this update, when servicing a bare-metal host (BMH), the `service_disable_ramdisk` parameter remained set to `False` even if all servicing steps were performed out-of-band. As a result, the BMH underwent an unnecessary reboot. With this release, the `ironic` service code is modified to automatically set `service_disable_ramdisk` to `True` when all servicing steps are out-of-band. ([OCPBUGS-85528](https://redhat.atlassian.net/browse/OCPBUGS-85528))

- Before this update, the `ironic-agent` container image was missing the `iproute` package at runtime, which provides the `ip` command required for network configuration. As a consequence, the Ironic Python Agent (IPA) failed to heartbeat to the `ironic` service during bare-metal node cleaning, and node cleaning operations timed out. With this release, the `ironic-agent` container image build process is updated to retain required packages such as `iproute` and `psmisc`. As a result, IPA completes network configuration successfully and bare-metal node cleaning operations complete without timing out. ([OCPBUGS-94115](https://redhat.atlassian.net/browse/OCPBUGS-94115))

- Before this update, bare-metal nodes provisioned through virtual media failed to boot the inspection image because of incorrect kernel arguments in the provisioning ISO. As a consequence, soft lockups occurred on some hardware, for example, Fujitsu PRIMERGY M8, because the `{{console=ttyS0}}` parameter lacked baud rate and parity settings. The `{{ip=dhcp}}` parameter was missing, which prevented network acquisition during early boot. With this release, the provisioning ISO includes the `{{ip=dhcp}}` parameter and specifies the full serial console configuration. As a result, bare-metal Installer-provisioned installations complete without manual intervention. ([OCPBUGS-98696](https://redhat.atlassian.net/browse/OCPBUGS-98696))

- Before this update, the Bare Metal Operator (BMO) did not set the `IRONIC_INSECURE` function. As a consequence, bare-metal host (BMH) provisioning failed. With this release, the BMO correctly sets the `IRONIC_INSECURE` function. As a result, BMH provisioning succeeds. ([OCPBUGS-111889](https://redhat.atlassian.net/browse/OCPBUGS-111889))

## Cloud Compute

- Before this update, the `AWSMachine` controller was requeuing machine instances before confirming the presence of tags. As a consequence, duplicate Amazon Web Services (AWS) EC2 instances were created. With this release, the `AWSMachine` controller verifies tags before requeuing instances. As a result, duplicate EC2 instances are not created. ([OCPBUGS-62985](https://redhat.atlassian.net/browse/OCPBUGS-62985))

- Before this update, the `cloud-controller-manager` cluster Operator did not set its `Progressing` status condition to `True` during cluster upgrades. As a consequence, the Cluster Version Operator (CVO) waited for the Operator without receiving proper progress signals, and upgrade monitoring tests failed. With this release, the `cloud-controller-manager` Operator correctly reports `Progressing=True` during version changes. As a result, cluster upgrades proceed with accurate Operator status reporting. ([OCPBUGS-64852](https://redhat.atlassian.net/browse/OCPBUGS-64852))

- Before this update, if an OpenStack cloud provider lacked the optional Standard Attributes Tag extension, the Machine API Provider for OpenStack (MAPO) attempted to apply port tags during network port creation. As a consequence, provisioning failed. With this release, MAPO checks whether the `standard-attr-tag` extension is available before applying tags. If unsupported, MAPO skips tag assignment or returns an error prompting you to remove explicit configurations. As a result, machine provisioning completes successfully. ([OCPBUGS-77061](https://redhat.atlassian.net/browse/OCPBUGS-77061))

- Before this update, a programming error forced load balancers to always use control-plane instance groups rather than treating them as optional. As a consequence, load balancers included control plane nodes even when they had the `node.kubernetes.io/exclude-from-external-load-balancers` label. With this release, the logic for reusing the instance groups is corrected. As a result, nodes with the `node.kubernetes.io/exclude-from-external-load-balancers` label are correctly excluded from load balancers. ([OCPBUGS-84569](https://redhat.atlassian.net/browse/OCPBUGS-84569))

- Before this update, when you installed a cluster with `featureSet: TechPreviewNoUpgrade` and `baselineCapabilitySet: None`, the `openshift-cluster-api-vsphere` and `openshift-cluster-api-baremetal` `CredentialsRequest` custom resources (CRs) in the `0000_30_cluster-api_01_credentials-request.yaml` file did not have the `capability.openshift.io/name: CloudCredential` annotation. As a consequence, the Cluster Version Operator (CVO) attempted to apply these CRs even though the `CloudCredential` capability was not enabled, causing the installation to become unresponsive and result in an error indicating that the `CredentialsRequest` custom resource definition (CRD) was not available. With this release, the required capability annotation is added to the `CredentialsRequest` CRs. As a result, cluster installations with `TechPreviewNoUpgrade` and `baselineCapabilitySet: None` complete successfully. ([OCPBUGS-85063](https://redhat.atlassian.net/browse/OCPBUGS-85063))

- Before this update, when using vSphere Installer-provisioned infrastructure with static IP configuration, name server settings were lost when the Control Plane Machine Set (CPMS) was recreated. As a consequence, control plane nodes had incorrect DNS configuration after CPMS recreation. With this release, name server settings are preserved when recreating the CPMS. As a result, DNS configuration on control plane nodes remains correct after CPMS recreation. ([OCPBUGS-86860](https://redhat.atlassian.net/browse/OCPBUGS-86860))

- Before this update, the Cluster API Operator mounted only container images associated with the current release, not images referenced by existing revisions from previous releases. As a consequence, after upgrading a cluster with `featureSet: TechPreviewNoUpgrade`, the revision and installation program controllers failed when iterating over old revisions because the required images were not available. With this release, the Cluster API Operator mounts images for both the current release and any images referenced by existing revisions. As a result, cluster upgrades with Cluster API enabled complete successfully without rendering failures. ([OCPBUGS-87001](https://redhat.atlassian.net/browse/OCPBUGS-87001))

- Before this update, on Microsoft Azure, the `cloud-controller-manager` Operator transitioned to `Progressing=True` during `MachineSet` scaling operations when the cloud-controller-manager `daemonset` was rolling out to newly added nodes. As a consequence, tests that expected cluster Operators to remain non-progressing during node scaling failed. With this release, the Operator correctly reports `Progressing=False` during `MachineSet` scaling operations while `daemonset` pods are being scheduled to new nodes. As a result, the Operator status accurately reflects that scaling operations do not represent Operator version changes or configuration updates. ([OCPBUGS-98617](https://redhat.atlassian.net/browse/OCPBUGS-98617))

- Before this update, the Machine API Operator unconditionally emitted a `Status upgrade` event on every status reconciliation while its operands were rolling out during cluster upgrades. As a consequence, during single-node upgrades, the same event was emitted over 20 times, causing upgrades to fail the pathological-event invariant test that detects excessive event repetition. With this release, the Machine API Operator only emits `Status upgrade` events when transitioning into a new `Progressing` state or when the upgrade target or message changes. As a result, single-node cluster upgrades complete successfully without triggering pathological-event failures. ([OCPBUGS-100067](https://redhat.atlassian.net/browse/OCPBUGS-100067))

- Before this update, when Microsoft Azure Disk CSI found a disk already attached to a virtual machine (VM) whose provisioning state was `Failed`, `cloud-provider-azure` refreshed that VM by sending an empty `VirtualMachine` resource through a `CreateOrUpdate` element, producing a PUT request with an empty body. As a consequence, Azure rejected the refresh request with a `LocationRequired` error, which prevented recovery and obscured the earlier VM failure. With this release, the refresh operation uses the existing `BeginUpdate` operation with an empty VirtualMachineUpdate, preserving the intended no-op refresh as a PATCH request for both standard and flexible VM paths. As a result, failed VM refresh operations complete successfully and Azure no longer rejects the refresh with `LocationRequired` errors. ([OCPBUGS-100185](https://redhat.atlassian.net/browse/OCPBUGS-100185))

- Before this update, on hosted control planes, certificate signing requests (CSRs) for newly added machine pools required manual approval when using egress IP configurations. As a consequence, administrators had to manually approve all new CSRs, preventing automatic node onboarding. With this release, the cluster machine approver correctly handles CSR approval for hosted control plane machine pools with egress IP. As a result, CSRs are automatically approved and nodes can join the cluster without manual intervention. ([OCPBUGS-113529](https://redhat.atlassian.net/browse/OCPBUGS-113529))

## Cloud Credential Operator

- Before this update, when the Cloud Credential Operator (CCO) ran in manual mode on OpenShift Container Platform clusters configured to use Amazon Web Services (AWS) Security Token Service (STS), the Operator repeatedly attempted to reconcile `CredentialsRequest` resources for cluster Operators. As a consequence, unnecessary log messages were generated. With this release, the Operator recognizes externally managed secrets and skips unnecessary reconciliation. ([OCPBUGS-33994](https://redhat.atlassian.net/browse/OCPBUGS-33994))

## Cluster Autoscaler

## Cluster Version Operator

- Before this update, when a HostedCluster `spec.configuration.proxy` setting was scoped to data-plane components in 4.18, the Cluster Version Operator (CVO) was not updated to ignore that proxy configuration on hosted control planes. As a consequence, update advice retrieval was blocked when incompatible with the management cluster network. With this release, the CVO ignores hosted proxy configurations. As a result, egress to update services is successful. ([OCPBUGS-79358](https://redhat.atlassian.net/browse/OCPBUGS-79358))

## etcd

- Before this update, an upgrade with a control plane `MachineConfig` might have caused quorum loss. As a consequence, the upgrade caused prolonged API and etcd downtime, leading to service interruption. With this release, the `cluster-etcd-operator` keeps guard pods that prevent a `MachineConfig` object from draining the node. As a result, etcd maintains quorum during upgrades. ([OCPBUGS-66334](https://redhat.atlassian.net/browse/OCPBUGS-66334))

## Hosted Control Planes

- Before this update, KubeVirt-based `NodePool` resources incorrectly reported `ClusterNetworkCIDRConflict` errors because the controller flagged OVN-Kubernetes internal overlay IP addresses as conflicting with the cluster network. With this release, Classless Inter-Domain Routing (CIDR) conflict detection is triggered only when all the non-link local addresses for the machine fall within the cluster network. As a result, when external addresses exist, in-network addresses are correctly treated as expected container network interface (CNI) internal IP addresses, which prevents false positive conflict reports. ([OCPBUGS-84269](https://redhat.atlassian.net/browse/OCPBUGS-84269))

- Before this update, applying resource overrides to containers without pre-existing resource requests caused a nil map panic and crash loop. With this release, a nil guard is added to the `applyRequestsOverrides` function in the Control Plane Operator (CPO) before calling `maps.Copy` on the `Resources.Requests` parameter. As a result, resource request overrides are successfully applied regardless of pre-existing requests. ([OCPBUGS-93785](https://redhat.atlassian.net/browse/OCPBUGS-93785))

- Before this update, the Konnectivity proxy-server in the `kube-apiserver` deployment was not configured with the `--cluster-ca-cert` flag. As a consequence, a reachable client could establish a connection to the Konnectivity proxy-server without a valid client certificate signed by the hosted cluster Konnectivity certification authority (CA). With this release, the `--cluster-ca-cert` flag is added to the `konnectivity-server` container arguments in the `kube-apiserver` deployment manifest. As a result, unauthenticated connections are prevented because the proxy-server requires and validates client certificates signed by the hosted cluster Konnectivity CA. ([OCPBUGS-99014](https://redhat.atlassian.net/browse/OCPBUGS-99014))

## Installer

- Before this update, when you configured networking with the `agent-tui` parameter during an Assisted Installation Program workflow, the `NetworkManager` keyfiles were not automatically passed to the CoreOS installation program. As a consequence, network configurations did not persist into the installed operating system, causing nodes to have missing or incorrect network settings. With this release, the agent detects manually-created `NetworkManager` keyfiles by comparing their modification times against the agent-tui start time and automatically appends the `--copy-network` command to the CoreOS installation program arguments. As a result, network configurations persist to the installed system. ([OCPBUGS-63472](https://redhat.atlassian.net/browse/OCPBUGS-63472))

- Before this update, older versions of Software Development Kit (SDK) for Virtual Private Cloud (VPC) could not parse a VPC with new security group rule types, such as `any`, that were introduced by IBM Cloud. As a consequence, the installation program could not successfully set up a new VPC or use an existing VPC with such a protocol type. With this release, the SDK for VPC is updated to a version that supports parsing the new types. As a result, the installation process can create or use a VPC with the new security group rule types. ([OCPBUGS-78429](https://redhat.atlassian.net/browse/OCPBUGS-78429))

- Before this update, the installation program created inbound Amazon Web Services (AWS) security group rules for OVN database traffic that used inconsistent port numbers across OpenShift Container Platform versions (some versions used `6441-6442` instead of `6641-6642`). As a consequence, clusters exposed unnecessary security group rules that no longer reflected how OVN-Kubernetes communicates, as OVN databases run locally on each node and communicate over UNIX domain sockets rather than TCP. With this release, the installation program does not create security group rules for OVN database ports on AWS. As a result, newly installed AWS clusters no longer include these unused inbound security group rules. ([OCPBUGS-79536](https://redhat.atlassian.net/browse/OCPBUGS-79536))

- Before this update, during an appliance-based no-registry installation, the `watch-iri-tls-certs.path` and `reconfigure-local-registry-iri-tls.sh` files were only included in the installation ignition, not the bootstrap ignition. As a consequence, the appliance registry continued serving with self-signed certificates instead of the Internal Release Image (IRI) TLS certificate generated by Assisted Service, causing other nodes to fail pulling images over api-int and the installation to fail. With this release, the `watch-iri-tls-certs.path` unit and `reconfigure-local-registry-iri-tls.service` are included in the bootstrap ignition to reconfigure the registry with the correct IRI TLS certificate immediately. As a result, the installation completes successfully. ([OCPBUGS-81505](https://redhat.atlassian.net/browse/OCPBUGS-81505))

- Before this update, the Internal Release Image (IRI) registry, which serves the release image payload to cluster nodes, had its backing store mounted read-only but lacked enforcement at the application layer. As a consequence, any attempt to push an image to the IRI registry at `api-int.<baseDomain>:22625` returned an `HTTP 500 Internal Server Error`, with no indication that the registry was intentionally read-only. With this release, the `REGISTRY_STORAGE_MAINTENANCE_READONLY` environment variable is set on the IRI registry service. As result, an `HTTP 405 Method Not Allowed` message is returned on write attempts. ([OCPBUGS-82974](https://redhat.atlassian.net/browse/OCPBUGS-82974))

- Before this update, when destroying a cluster installed in the Amazon Web Services (AWS) China `cn-north-1` (Beijing) region, the installation program did not search the `cn-northwest-1` region for tagged Route 53 resources. As a consequence, Route 53 hosted zones and associated records were not deleted during cluster destruction. This issue resulted in leaked resources in the AWS China partition that required manual cleanup. With this release, the installation program correctly creates a tag client for the `cn-northwest-1` region when destroying a cluster from the `cn-north-1` region to discover all cluster-owned Route 53 resources. As a result, Route 53 hosted zones are properly discovered and deleted during cluster destruction in the AWS China `cn-north-1` region. ([OCPBUGS-85352](https://redhat.atlassian.net/browse/OCPBUGS-85352))

- Before this update, on Google Cloud clusters, values specified in `defaultMachinePlatform` were not applied to individual machine pools during cluster installation. As a consequence, settings such as `osDisk.diskType` were ignored, and control plane nodes used default values instead of the specified configuration. With this release, the installation program correctly applies `defaultMachinePlatform` settings to all machine pools. As a result, Google Cloud machine configurations use the specified platform defaults. ([OCPBUGS-88303](https://redhat.atlassian.net/browse/OCPBUGS-88303))

- Before this update, when removing a cluster, an error querying or deleting a Cloud Native Storage (CNS) volume prevented the installation program from processing remaining volumes. As a consequence, storage resources were not deleted. With this release, the installation program processes the remaining volumes across vCenters after individual errors and reports any cleanup failures. As a result, orphaned storage resources are prevented. ([OCPBUGS-92792](https://redhat.atlassian.net/browse/OCPBUGS-92792))

- Before this update, the installation program used a 30-second timeout when retrieving marketplace images. As a consequence, installation could fail with `context deadline exceeded` errors during `GetMarketplaceImage` operations. With this release, the installation program increases the timeout for retrieving marketplace images to five minutes. As a result, the installation program can successfully retrieve marketplace images. ([OCPBUGS-113641](https://redhat.atlassian.net/browse/OCPBUGS-113641))

## Kube API Server

- Before this update, the `kube-apiserver-check-endpoints` container generated a TLS certificate for the `check-endpoint` service on port `17697` with a validity of only one second. As a consequence, the certificate expired almost immediately after generation, which differed from earlier OpenShift Container Platform versions where the certificate was valid for one month. With this release, the `kube-apiserver-check-endpoints` container generates certificates with an appropriate validity period. As a result, the `check-endpoint` service certificate remains valid for the expected duration, consistent with earlier releases. ([OCPBUGS-62792](https://redhat.atlassian.net/browse/OCPBUGS-62792))

- Before this update, clusters installed with a custom service account issuer included both the custom issuer and the default issuer during the first 24 hours. As a consequence, service account tokens included two audiences, preventing some applications from deploying unless the audience was explicitly specified. With this release, only the custom issuer is present when configured during installation. As a result, service account tokens contain a single audience, and some applications can deploy immediately. ([OCPBUGS-76588](https://redhat.atlassian.net/browse/OCPBUGS-76588))

- Before this update, certificate files for the Kube API server were not flushed to disk immediately after being written, and data could remain in memory without being persisted to storage. As a consequence, on single-node OpenShift clusters, an ungraceful shutdown could cause all Kube API server certificates to be lost, leaving the cluster unable to start. With this release, certificate writes are flushed to disk before any earlier data is removed, ensuring crash durability. As a result, single-node OpenShift clusters that experience an unexpected shutdown no longer risk losing their Kube API server certificates. ([OCPBUGS-84258](https://redhat.atlassian.net/browse/OCPBUGS-84258))

- Before this update, when deploying STS clusters through Hive or ACM with manual credentials mode, the `kube-apiserver` Operator ignored the custom service account issuer from the Authentication CR during the first revision. As a consequence, the `kube-apiserver` used the default issuer at startup and then rolled out with the correct issuer after bootstrap, which raced against token expiry and caused installation timeouts. With this update, the Operator falls back to discovering the service account issuer from the rendered input manifests. As a result, STS cluster installations using Hive or ACM no longer experience timeouts caused by a service account issuer mismatch. ([OCPBUGS-86057](https://redhat.atlassian.net/browse/OCPBUGS-86057))

- Before this update, the `kube-apiserver-to-kubelet-signer` CA certificate refresh interval was incorrectly set to 30 days despite having a 365-day validity period. As a consequence, the CA was regenerated monthly, triggering unnecessary `kube-apiserver` rollouts. With this update, the refresh interval is set to 292 days, which is 80% of the validity period, consistent with other signers. As a result, the CA is no longer regenerated prematurely and unnecessary rollouts no longer occur. ([OCPBUGS-86699](https://redhat.atlassian.net/browse/OCPBUGS-86699))

- Before this update, the Go OpenSSL Federal Information Processing Standards (FIPS) provider could potentially overwhelm `libcrypto` library with concurrent requests. As a consequence, processes could hit the `maxThreads` limit of 10,000 and crash. With this release, the Go OpenSSL FIPS provider is updated to limit concurrent requests to the `libcrypto` library to four times the number of CPUs, buffering requests as lightweight Go routines. As a result, processes avoid the `maxThreads` limit and do not crash. ([OCPBUGS-99552](https://redhat.atlassian.net/browse/OCPBUGS-99552))

## Kube Scheduler

- Before this update, the `kube-scheduler` Cluster Operator briefly reported a `Degraded=True` status during cluster upgrades due to transient node not-ready events and static pod restarts. As a consequence, upgrade tests failed intermittently. With this update, a 10-minute stabilization period is applied to the `NodeControllerDegraded`, `StaticPodsDegraded`, and `GuardControllerDegraded` conditions. As a result, the `kube-scheduler` Cluster Operator no longer falsely reports a degraded status during upgrades. ([OCPBUGS-38663](https://redhat.atlassian.net/browse/OCPBUGS-38663))

## Kube Storage Version Migrator

## Machine Config Operator

- Before this update, when nodes used a locally stored RHEL CoreOS image and the image was garbage collected by Kubernetes, applying an extension to the node caused the machine config pool to become degraded. As a consequence, node updates failed with an error indicating that the image reference could not be resolved. With this release, the Machine Config Operator properly handles locally stored images that might be garbage collected. As a result, machine config pools no longer become degraded in this scenario. ([OCPBUGS-57473](https://redhat.atlassian.net/browse/OCPBUGS-57473))

- Before this update, when Image Mode was enabled in a machine config pool and the `MachineOSConfig` resource was deleted before the operating system image was fully applied to all nodes, the machine config pool became degraded. As a consequence, nodes failed to update with manifest unknown errors because the operating system image was garbage collected from the internal registry. With this release, the Machine Config Operator prevents premature garbage collection of operating system images during rollouts. As a result, machine config pools no longer become degraded when `MachineOSConfig` resources are deleted during image application. ([OCPBUGS-59197](https://redhat.atlassian.net/browse/OCPBUGS-59197))

- Before this update, the Machine Config Operator used inconsistent cryptographic implementations (`OpenPGP` versus `gpgme`) across different components. As a consequence, build environments without the `gpgme-devel` package experienced compilation failures. With this release, all Machine Config Operator components use the `gpgme` implementation consistently. As a result, builds complete successfully and align with industry-standard container tools. ([OCPBUGS-63750](https://redhat.atlassian.net/browse/OCPBUGS-63750))

- Before this update, the `machine-config` `ClusterOperator` did not reference cluster-scoped RBAC resources in its `relatedObjects` field. As a consequence, the `oc adm inspect clusteroperator/machine-config` command did not collect `ClusterRole` and `ClusterRoleBinding` resources needed for debugging. With this release, the `ClusterOperator` includes all relevant cluster-scoped resources in its `relatedObjects` field. As a result, must-gather and inspect commands collect complete debugging information. ([OCPBUGS-65504](https://redhat.atlassian.net/browse/OCPBUGS-65504))

- Before this update, when an extension package installation failed but did not return an error code, the machine config pool reported success even though the packages were not installed on the node. As a consequence, users believed the installation was successful when the expected packages were missing. With this release, the Machine Config Daemon verifies that expected packages are installed and degrades the machine config pool if verification fails. As a result, package installation failures are accurately reported to users. ([OCPBUGS-65645](https://redhat.atlassian.net/browse/OCPBUGS-65645))

- Before this update, when a `MachineOSBuild` image was deleted from the registry and a `MachineConfig` was reapplied, a new `MachineOSBuild` was triggered unnecessarily instead of reusing the existing build. As a consequence, unnecessary image rebuilds occurred, slowing down machine config updates. With this release, the Machine Config Operator correctly identifies and reuses existing builds when the configuration has not changed. As a result, machine config updates proceed directly without unnecessary image rebuilds. ([OCPBUGS-68350](https://redhat.atlassian.net/browse/OCPBUGS-68350))

- Before this update, when a `PinnedImageSet` resource specified a large number of container images to pin, the image synchronization process did not complete and appeared to get stuck. As a consequence, not all specified images were pinned to nodes as requested. With this release, the pinned image synchronization logic is improved to handle large image sets. As a result, all images in a `PinnedImageSet` are successfully synchronized to nodes. ([OCPBUGS-77140](https://redhat.atlassian.net/browse/OCPBUGS-77140))

- Before this update, when applying the DISA STIG compliance profile, the `usbguard` service was not properly enabled on nodes even after installing the extension. As a consequence, compliance scans failed for the `service-usbguard-enabled` rule. With this release, the Machine Config Operator correctly enables the `usbguard` service when the extension is installed. As a result, nodes pass DISA STIG compliance scans. ([OCPBUGS-78524](https://redhat.atlassian.net/browse/OCPBUGS-78524))

- Before this update, control plane nodes were labeled with `node-role.kubernetes.io/control-plane` but still had the legacy `node-role.kubernetes.io/master` taint. As a consequence, the node labeling and tainting were inconsistent. With this release, the Machine Config Operator applies the `node-role.kubernetes.io/control-plane` taint to align with the updated node labels. As a result, control plane node taints are consistent with their labels. ([OCPBUGS-82139](https://redhat.atlassian.net/browse/OCPBUGS-82139))

- Before this update, the Machine Config Operator updated Amazon Web Services (AWS) AMI allowlists through automated processes. As a consequence, new AWS regions and instance types were supported. With this release, the AMI allowlist is updated. As a result, additional Amazon Web Services (AWS) AMI IDs are recognized and supported. ([OCPBUGS-83539](https://redhat.atlassian.net/browse/OCPBUGS-83539))

- Before this update, during a cluster upgrade that changed the `baseOSExtensionsContainerImage` and `osImageURL` fields, two separate rendered `MachineConfig` resources were created sequentially instead of one. As a consequence, the upgrade process created unnecessary intermediate configurations. With this release, the Machine Config Controller creates a single rendered `MachineConfig` during upgrades. As a result, cluster upgrades proceed more efficiently without intermediate configuration steps. ([OCPBUGS-83619](https://redhat.atlassian.net/browse/OCPBUGS-83619))

- Before this update, when the Machine Config Daemon applied cgroup v2 kernel arguments on certain hardware configurations, the changes were staged but the node did not reboot automatically. As a consequence, nodes appeared to be stuck with mismatched `currentConfig` and `desiredConfig`, and the machine config pool became degraded after the configured timeout. With this release, the Machine Config Daemon correctly triggers node reboots after applying kernel argument changes. As a result, cgroup v2 kernel argument updates complete successfully. ([OCPBUGS-83830](https://redhat.atlassian.net/browse/OCPBUGS-83830))

- Before this update, when new nodes were provisioned during a cluster upgrade from OpenShift 4.18 to 4.20, the encapsulated Ignition configuration contained version 3.5.0 even though the node’s RHCOS 4.18 first-boot process only supported up to version 3.4.0. As a consequence, new node provisioning failed during upgrade rollouts with "unknown version" errors. With this release, the Machine Config Server generates encapsulated Ignition configurations that match the requesting node’s supported version. As a result, new nodes provision successfully during cluster upgrades. ([OCPBUGS-83859](https://redhat.atlassian.net/browse/OCPBUGS-83859))

- Before this update, when the `current-machine-os-build` annotation on a `MachineOSConfig` pointed to a build that no longer existed, the Machine Config Controller repeatedly logged errors and failed to update the machine config pool. As a consequence, machine config pools remained stuck at 0 machines configured when using Image Mode. With this release, the Machine Config Controller correctly handles missing build references and creates new builds as needed. As a result, machine config pools update successfully in Image Mode. ([OCPBUGS-84150](https://redhat.atlassian.net/browse/OCPBUGS-84150))

- Before this update, after upgrading to OpenShift 4.18.36, the Machine Config Daemon reported content mismatches on several nodes, blocking the upgrade from completing. As a consequence, cluster upgrades to 4.18.36 were blocked on affected nodes. With this release, the Machine Config Daemon correctly validates node content during upgrades. As a result, upgrades to 4.18.36 and later versions proceed without false content mismatch errors. ([OCPBUGS-84218](https://redhat.atlassian.net/browse/OCPBUGS-84218))

- Before this update, test automation for scaling `MachineSet` resources did not account for bare metal platforms that have no available hosts. As a consequence, automated tests for machine set scaling failed on bare metal platforms. With this release, the test automation correctly skips scenarios that are not applicable to bare metal platforms. As a result, machine set scaling tests pass on all supported platforms. ([OCPBUGS-84237](https://redhat.atlassian.net/browse/OCPBUGS-84237))

- Before this update, when the Machine Config Daemon performed a rollback after failing to apply a `MachineConfig`, SSH keys and user passwords were not properly restored. As a consequence, node access credentials were not correct after a rollback operation. With this release, the Machine Config Daemon correctly preserves and restores SSH keys and passwords during rollback operations. As a result, node access credentials remain valid after rollbacks. ([OCPBUGS-84332](https://redhat.atlassian.net/browse/OCPBUGS-84332))

- Before this update, when installing a cluster using the Agent-based Installer with `FEATURE_SET=TechPreviewNoUpgrade`, the installation did not complete because the operating system image stream certificate was missing. As a consequence, installations with Technology Preview features enabled timed out and failed. With this release, the required operating system image stream certificate is properly configured for Technology Preview installations. As a result, Agent-based Installer deployments with Technology Preview features complete successfully. ([OCPBUGS-84652](https://redhat.atlassian.net/browse/OCPBUGS-84652))

- Before this update, when the kubelet configuration was generated, an older Machine Config Controller version was used, causing the machine config pool to become degraded. As a consequence, the `generated-kubelet` configuration did not match the expected controller version, and the pool reported degraded status. With this release, the kubelet configuration is generated using the current controller version. As a result, machine config pools do not become degraded due to kubelet configuration version mismatches. ([OCPBUGS-84661](https://redhat.atlassian.net/browse/OCPBUGS-84661))

- Before this update, the `chrony-wait` service blocked node readiness for approximately 24 seconds on Azure and 11 seconds on other platforms while waiting for time synchronization. As a consequence, node startup times were unnecessarily delayed. With this release, the time synchronization waiting logic is optimized. As a result, nodes reach the Ready state faster during startup. ([OCPBUGS-84814](https://redhat.atlassian.net/browse/OCPBUGS-84814))

- Before this update, the Machine Config Daemon pulled and extracted the extensions container image during every operating system update, even when no extensions were installed or changed. As a consequence, unnecessary network bandwidth and time were consumed during operating system updates and node bootstrap. With this release, the Machine Config Daemon only pulls the extensions image when extensions are actually being installed or updated. As a result, operating system updates and node bootstrap complete faster and use less network bandwidth. ([OCPBUGS-84832](https://redhat.atlassian.net/browse/OCPBUGS-84832))

- Before this update, automated tests for Image Mode operations failed when the `current-machine-os-build` annotation was temporarily empty during normal reconciliation. As a consequence, test flakes occurred in continuous integration pipelines. With this release, the test helper correctly handles temporarily empty annotations. As a result, Image Mode tests run reliably without flakes. ([OCPBUGS-84867](https://redhat.atlassian.net/browse/OCPBUGS-84867))

- Before this update, multiple Machine Config Operator continuous integration jobs experienced complete failures across several OpenShift releases. As a consequence, automated testing was disrupted and development velocity was reduced. With this release, the continuous integration job failures are resolved. As a result, automated tests run successfully across all supported releases. ([OCPBUGS-84871](https://redhat.atlassian.net/browse/OCPBUGS-84871))

- Before this update, the Image Mode test suite contained several flaky tests that intermittently failed due to timing issues. As a consequence, continuous integration results were unreliable. With this release, the flaky tests are stabilized. As a result, the Image Mode test suite runs reliably. ([OCPBUGS-85117](https://redhat.atlassian.net/browse/OCPBUGS-85117))

- Before this update, when nodes were manually uncordoned by using `oc adm uncordon` during a machine config update, the Machine Config Daemon did not re-cordon them before proceeding with the update. As a consequence, workloads remained scheduled on nodes that were about to undergo disruptive updates. With this release, the Machine Config Daemon re-cordons manually uncordoned nodes before proceeding with updates. As a result, workloads are properly drained before disruptive node updates. ([OCPBUGS-85237](https://redhat.atlassian.net/browse/OCPBUGS-85237))

- Before this update, automated tests for Image Mode status reporting assumed multi-node topologies and failed on single-node OpenShift deployments. As a consequence, continuous integration tests for single-node OpenShift were unreliable. With this release, the tests correctly handle both single-node and multi-node topologies. As a result, Image Mode tests pass on all supported cluster configurations. ([OCPBUGS-86179](https://redhat.atlassian.net/browse/OCPBUGS-86179))

- Before this update, the Machine Config Operator test suite included tests that used base images older than OpenShift 4.13. As a consequence, outdated test coverage was maintained for unsupported versions. With this release, tests by using base images older than 4.13 are removed. As a result, the test suite focuses on currently supported OpenShift versions. ([OCPBUGS-86332](https://redhat.atlassian.net/browse/OCPBUGS-86332))

- Before this update, automated tests for real-time kernel functionality were limited to AWS and GCP platforms. As a consequence, real-time kernel features were not tested on other supported platforms. With this release, real-time kernel tests run on all platforms that support the feature. As a result, real-time kernel functionality is verified across all supported platforms. ([OCPBUGS-86474](https://redhat.atlassian.net/browse/OCPBUGS-86474))

- Before this update, a test regression occurred in the etcd Operator conditions test suite. As a consequence, component readiness metrics showed degraded status. With this release, the test regression is resolved. As a result, component readiness tests pass successfully. ([OCPBUGS-86554](https://redhat.atlassian.net/browse/OCPBUGS-86554))

- Before this update, when creating new vSphere templates, the operation was not atomic and could be interrupted, leaving incomplete templates. As a consequence, template creation failures could result in corrupted or incomplete templates. With this release, vSphere template creation is performed as an atomic operation. As a result, templates are created reliably without the risk of partial or corrupted templates. ([OCPBUGS-86826](https://redhat.atlassian.net/browse/OCPBUGS-86826))

- Before this update, end-to-end tests for Image Mode on GCP platform failed across OpenShift 4.22. As a consequence, continuous integration for 4.22 on GCP showed failures. With this release, the test failures are resolved. As a result, Image Mode tests pass successfully on GCP. ([OCPBUGS-86835](https://redhat.atlassian.net/browse/OCPBUGS-86835))

- Before this update, test case 69755 exhibited instability and intermittent failures. As a consequence, continuous integration results were inconsistent. With this release, the test is stabilized. As a result, test 69755 runs reliably without intermittent failures. ([OCPBUGS-86965](https://redhat.atlassian.net/browse/OCPBUGS-86965))

- Before this update, the `bootupd` workaround in the Machine Config Operator did not account for updates on existing nodes. As a consequence, `bootupd` updates failed on nodes that existed before the workaround was implemented. With this release, the `bootupd` workaround handles both new and existing nodes correctly. As a result, `bootupd` updates succeed on all nodes. ([OCPBUGS-88333](https://redhat.atlassian.net/browse/OCPBUGS-88333))

- Before this update, the Image Mode Day 1 installation continuous integration job failed consistently. As a consequence, automated testing for Image Mode installations was disrupted. With this release, the installation job failures are resolved. As a result, Image Mode Day 1 installation tests pass successfully. ([OCPBUGS-88686](https://redhat.atlassian.net/browse/OCPBUGS-88686))

- Before this update, the Machine Config Controller consumed significantly more memory in OpenShift 4.22 compared to earlier versions. As a consequence, the controller experienced memory pressure and potential performance degradation. With this release, memory usage in the Machine Config Controller is optimized. As a result, the controller operates efficiently without excessive memory consumption. ([OCPBUGS-92062](https://redhat.atlassian.net/browse/OCPBUGS-92062))

- Before this update, when adding a new vSphere failure domain, the Machine Config Operator boot image controller failed because it ignored the `providerSpec.Template` field and could not locate the template. As a consequence, the cluster Operator became degraded when new failure domains were added. With this release, the boot image controller correctly uses the `providerSpec.Template` field for template lookups. As a result, new vSphere failure domains are added successfully without degrading the cluster Operator. ([OCPBUGS-92182](https://redhat.atlassian.net/browse/OCPBUGS-92182))

- Before this update, the Machine Config Operator updated AWS AMI allowlists through automated processes. As a consequence, new AWS regions and instance types were supported. With this release, the AMI allowlist is updated. As a result, additional AWS AMI IDs are recognized and supported. ([OCPBUGS-95030](https://redhat.atlassian.net/browse/OCPBUGS-95030))

- Before this update, the Machine Config Controller `ClusterRole` was missing RBAC permissions for the `pkis` resource. As a consequence, operations involving `pkis` resources failed with permission denied errors. With this release, the required RBAC permissions are added to the `ClusterRole`. As a result, the Machine Config Controller can access `pkis` resources as needed. ([OCPBUGS-98745](https://redhat.atlassian.net/browse/OCPBUGS-98745))

- Before this update, when `MachineSet` resources were configured with a wrong vCenter server address, the Machine Config Controller silently ignored them when updating boot images. As a consequence, boot images were not updated for affected machine sets, leading to potential boot failures. With this release, the Machine Config Controller validates and processes all machine sets, logging warnings for configuration issues. As a result, administrators are notified of machine sets with wrong server configurations. ([OCPBUGS-99219](https://redhat.atlassian.net/browse/OCPBUGS-99219))

- Before this update, automated tests did not verify extension installation failures. As a consequence, regressions in extension verification error handling could go undetected. With this release, automated tests verify extension verification failure scenarios. As a result, extension error handling is properly tested. ([OCPBUGS-99696](https://redhat.atlassian.net/browse/OCPBUGS-99696))

- Before this update, the Machine Config Daemon first-boot process performed fsync operations that added 3-5 seconds to the rebase duration. As a consequence, node first-boot times were longer than necessary. With this release, fsync operations are disabled during first-boot rebase for improved performance. As a result, nodes complete first-boot rebase 3-5 seconds faster. ([OCPBUGS-100389](https://redhat.atlassian.net/browse/OCPBUGS-100389))

- Before this update, the Machine Config Operator updated AWS AMI allowlists through automated processes. As a consequence, new AWS regions and instance types were supported. With this release, the AMI allowlist is updated. As a result, additional AWS AMI IDs are recognized and supported. ([OCPBUGS-100433](https://redhat.atlassian.net/browse/OCPBUGS-100433))

- Before this update, automated tests for upgrade verification panicked on Amazon Web Services (AWS) Technology Preview clusters. As a consequence, continuous integration for Technology Preview features was disrupted. With this release, the test panics are resolved. As a result, upgrade verification tests run successfully on AWS Technology Preview clusters. ([OCPBUGS-100458](https://redhat.atlassian.net/browse/OCPBUGS-100458))

- Before this update, the Machine Config Daemon did not emit Kubernetes events when draining nodes during updates. As a consequence, cluster administrators had limited visibility into node drain operations. With this release, the Machine Config Daemon emits events during node drain operations. As a result, administrators can monitor node drain progress through Kubernetes events. ([OCPBUGS-114389](https://redhat.atlassian.net/browse/OCPBUGS-114389))

- Before this update, when a `MachineSet` resource specified a workspace that did not match any vSphere failure domain, the boot image controller reported the cluster Operator as degraded. As a consequence, valid machine sets with intentionally different workspace configurations caused unnecessary degradation. With this release, the boot image controller logs a warning and skips machine sets whose workspaces do not match any failure domain instead of degrading the Operator. As a result, the cluster Operator does not become degraded for machine sets with non-matching workspaces. ([OCPBUGS-116711](https://redhat.atlassian.net/browse/OCPBUGS-116711))

- Before this update, the Machine Config Operator boot image controller used `path.Join()` to combine an already-absolute failure domain network path with the compute cluster path, producing an invalid inventory path. As a consequence, boot image updates failed with "failed to find network" errors on vSphere. With this release, the controller correctly handles absolute network paths without concatenating them. As a result, boot image updates succeed on vSphere with absolute network paths. ([OCPBUGS-121850](https://redhat.atlassian.net/browse/OCPBUGS-121850))

## Management Console

- Before this update, CPU metrics were missing for Windows nodes on the OpenShift Container Platform Console node list page. As a consequence, users could not view CPU use for Windows nodes in the **Compute** → **Nodes** list view, although memory metrics were available. With this release, the console correctly displays CPU metrics for Windows nodes. As a result, users can view both CPU and memory metrics for Windows nodes in the console node list. ([OCPBUGS-12953](https://redhat.atlassian.net/browse/OCPBUGS-12953))

- Before this update, visiting the **Home** → **Overview** page and keeping the window open for an extended period could cause a JavaScript error due to undefined properties. As a consequence, an error page with "Cannot read properties of undefined (reading 'description')" was displayed. With this release, the **Overview** page properly handles undefined data during long-running sessions. As a result, the **Overview** page remains stable during extended use. ([OCPBUGS-14473](https://redhat.atlassian.net/browse/OCPBUGS-14473))

- Before this update, the console cluster Operator reported `Progressing=True` with various reasons during normal operations. As a consequence, CI upgrade tests failed due to unexpected Operator state transitions. With this release, the console Operator maintains stable status conditions during normal operations. As a result, cluster upgrades proceed without console Operator status blips. ([OCPBUGS-38676](https://redhat.atlassian.net/browse/OCPBUGS-38676))

- Before this update, the OpenShift console displayed the character "9" with wrong formatting in the Logs view at 100% browser scale. As a consequence, the character "9" appeared different from other characters in the logs. With this release, the PatternFly font rendering is corrected. As a result, all characters display consistently in the console Logs view. ([OCPBUGS-50016](https://redhat.atlassian.net/browse/OCPBUGS-50016))

- Before this update, when login with external OIDC provider encountered authentication issues, the console could enter an endless redirect loop. As a consequence, users were unable to access the console and saw repeated redirects to the callback URL. With this release, the console properly handles negative user login scenarios including authentication failures. As a result, users see appropriate error messages instead of experiencing endless redirect loops. ([OCPBUGS-59353](https://redhat.atlassian.net/browse/OCPBUGS-59353))

- Before this update, the console disabled the "Restore" option for `VolumeSnapshots` after the parent persistent volume claim (PVC) was deleted. As a consequence, users could not restore snapshots from the console after deleting the original PVC, although restoration worked by using CLI. With this release, the console allows restoring `VolumeSnapshots` regardless of parent PVC status. As a result, users can restore snapshots from the console even after the parent PVC is deleted. ([OCPBUGS-59404](https://redhat.atlassian.net/browse/OCPBUGS-59404))

- Before this update, the console cluster Operator reported `Progressing=True` during node reboots due to deployment generation changes. As a consequence, upgrade monitoring tests failed when node reboots occurred during the upgrade window. With this release, the console Operator correctly distinguishes between self-inflicted deployment changes and genuine progress events. As a result, the console Operator does not report false Progressing conditions during node reboots. ([OCPBUGS-64688](https://redhat.atlassian.net/browse/OCPBUGS-64688))

- Before this update, the console OperatorHub incorrectly displayed icons for Operators when multiple Operators with the same name existed. As a consequence, the Loki Operator from the community catalog and the Loki Operator from the Red Hat catalog sometimes displayed swapped or wrong icons. With this release, the console correctly renders Operator icons based on the Operator source. As a result, Operators display their correct icons in OperatorHub. ([OCPBUGS-67295](https://redhat.atlassian.net/browse/OCPBUGS-67295))

- Before this update, editing a Secret containing binary data through the console **Edit Secret** form corrupted the binary content. As a consequence, binary files such as `JAR` or `JCEKS` keystores became invalid and unusable after editing any field in the **Edit Secret** form. With this release, the console properly preserves binary data when editing Secret fields. As a result, binary files in Secrets remain intact when other Secret fields are modified. ([OCPBUGS-70273](https://redhat.atlassian.net/browse/OCPBUGS-70273))

- Before this update, users without projects saw permission errors on various resource pages. As a consequence, pages such as **Workloads** → **Pods** and **Networking** → **Services** displayed "Restricted access" errors for users with no project access. With this release, the console properly handles empty project lists for users. As a result, users without projects can access resource list pages without seeing permission errors. ([OCPBUGS-71878](https://redhat.atlassian.net/browse/OCPBUGS-71878))

- Before this update, the console Operator generated excessive DNS `NXDOMAIN` errors when DNS queries included ambiguous search paths. As a consequence, DNS traffic was not optimal, with several useless DNS queries sent before finding the correct resolution. With this release, the console Operator uses fully qualified domain names with trailing dots. As a result, DNS queries resolve correctly on the first attempt without generating `NXDOMAIN` errors. ([OCPBUGS-77026](https://redhat.atlassian.net/browse/OCPBUGS-77026))

- Before this update, importing the `golang` devfile from the developer catalog failed due to upstream changes. As a consequence, users could not create sample applications using the `golang` devfile from the **Add** page. With this release, the console handles updated `golang` devfile formats correctly. As a result, users can successfully import and use the `golang` devfile to create sample applications. ([OCPBUGS-77952](https://redhat.atlassian.net/browse/OCPBUGS-77952))

- Before this update, visual connectors between applications in the **Topology** view did not persist after dragging. As a consequence, connection arrows between applications disappeared when the mouse was released. With this release, the **Topology** view correctly persists visual connectors between applications. As a result, dragging connection arrows between applications creates persistent visual relationships. ([OCPBUGS-78365](https://redhat.atlassian.net/browse/OCPBUGS-78365))

- Before this update, the overflow action menu on the **Installed Operators** list page only showed "Delete ClusterServiceVersion". As a consequence, users could not access the expected "Edit Subscription" and "Uninstall Operator" actions. With this release, the console displays the correct overflow menu items for installed Operators. As a result, users can access "Edit Subscription" and "Uninstall Operator" actions from the Installed Operators list page. ([OCPBUGS-79520](https://redhat.atlassian.net/browse/OCPBUGS-79520))

- Before this update, the **Search by name** filter on the **Installed Operators** list page did not filter results. As a consequence, searching for Operators by name had no effect on the displayed list. With this release, the name search filter correctly filters the **Installed Operators** list. As a result, users can search and filter Operators by name on the Installed Operators page. ([OCPBUGS-79521](https://redhat.atlassian.net/browse/OCPBUGS-79521))

- Before this update, the console downloaded the complete `ClusterServiceVersion` list (over 600 MB on large clusters) every time users visited the **Cluster Settings** page. As a consequence, navigating to **Administration** → **Cluster Settings** caused significant network transfer and browser memory pressure on clusters with many installed Operators. With this release, the console only fetches `ClusterServiceVersion` data when needed and uses conditional rendering. As a result, the **Cluster Settings** page loads efficiently without downloading unnecessary CSV data. ([OCPBUGS-81511](https://redhat.atlassian.net/browse/OCPBUGS-81511))

- Before this update, the console fetched the full OpenAPI v2 schema (50+ MB on clusters with many CRDs) without using HTTP conditional request headers. As a consequence, the console re-downloaded the entire OpenAPI spec on startup, every 5 minutes, and after each API discovery cycle. With this release, the console uses conditional request headers to avoid re-downloading unchanged OpenAPI schemas. As a result, OpenAPI fetches use HTTP 304 responses when the schema has not changed, reducing network transfer. ([OCPBUGS-81512](https://redhat.atlassian.net/browse/OCPBUGS-81512))

- Before this update, the **Search** page resource dropdown used O(n²) filtering logic on clusters with 1000+ API resources. As a consequence, typing in the Resources field caused multi-second delays with 100% CPU usage. With this release, the resource dropdown uses optimized filtering and debouncing. As a result, the **Search** page resource dropdown performs efficiently on large clusters. ([OCPBUGS-81518](https://redhat.atlassian.net/browse/OCPBUGS-81518))

- Before this update, dashboard Prometheus queries polled every 15 seconds regardless of cluster size. As a consequence, large clusters experienced high query load from dashboard polling. With this release, the console adjusts dashboard polling intervals based on cluster size. As a result, dashboards use appropriate polling frequencies for the cluster scale. ([OCPBUGS-81521](https://redhat.atlassian.net/browse/OCPBUGS-81521))

- Before this update, dashboard components opened excessive independent Kubernetes WebSocket watches without memoization. As a consequence, dashboard cards re-rendered unnecessarily on unrelated watch updates, causing performance degradation. With this release, dashboard cards use proper memoization and consolidated watches. As a result, dashboard performance is improved with fewer unnecessary re-renders. ([OCPBUGS-81522](https://redhat.atlassian.net/browse/OCPBUGS-81522))

- Before this update, visiting the Node Terminal tab showed an unnecessary error message before the debug pod was created. As a consequence, users saw "Debug pod was not found or was deleted" during normal terminal loading. With this release, the console only shows error messages when terminal creation genuinely fails. As a result, users do not see misleading error messages during normal terminal loading. ([OCPBUGS-81630](https://redhat.atlassian.net/browse/OCPBUGS-81630))

- Before this update, Helm chart upgrades via the console did not use previous release values. As a consequence, upgrading Helm charts reset configuration to default values instead of preserving previous release settings. With this release, the console performs 3-way merge during Helm upgrades, matching Helm CLI behavior. As a result, Helm chart upgrades preserve previous release configuration values. ([OCPBUGS-83767](https://redhat.atlassian.net/browse/OCPBUGS-83767))

- Before this update, when the `DeploymentConfig` cluster capability was disabled, the **Workloads** sidebar menu displayed items in a different order. As a consequence, users saw inconsistent menu ordering between clusters with and without the `DeploymentConfig` capability. With this release, the **Workloads** sidebar menu maintains consistent ordering regardless of cluster capabilities. As a result, the **Workloads** menu order is consistent across clusters. ([OCPBUGS-83799](https://redhat.atlassian.net/browse/OCPBUGS-83799))

- Before this update, after selecting a plugin-registered perspective such as Fleet management, the perspective switcher became unresponsive. As a consequence, users could not switch away from plugin perspectives back to Administrator or Developer perspectives. With this release, the console properly manages perspective context state during perspective switches. As a result, users can freely switch between all perspectives including plugin-registered perspectives. ([OCPBUGS-84047](https://redhat.atlassian.net/browse/OCPBUGS-84047))

- Before this update, the **Shipwright builds** page crashed with a React hooks error. As a consequence, users could not view `ClusterBuildStrategy` details and saw "Rendered more hooks than during the previous render" errors. With this release, the console properly handles React hooks in **Shipwright build** pages. As a result, users can view `ClusterBuildStrategy` details without React errors. ([OCPBUGS-84214](https://redhat.atlassian.net/browse/OCPBUGS-84214))

- Before this update, after upgrading or rolling back a Helm release, the console redirected to a non-existent route. As a consequence, users saw 404 errors after Helm upgrade or rollback operations. With this release, the console redirects to the correct Helm list page after upgrade and rollback operations. As a result, Helm upgrade and rollback operations complete with proper navigation to the Helm releases list. ([OCPBUGS-84296](https://redhat.atlassian.net/browse/OCPBUGS-84296))

- Before this update, the pod terminal in the console did not show the shell prompt until the browser window was resized. As a consequence, the terminal appeared blank or non-functional until users manually resized the window or toggled fullscreen. With this release, the terminal correctly calculates dimensions and displays the prompt on initial load. As a result, the shell prompt is visible immediately when opening the pod terminal. ([OCPBUGS-84649](https://redhat.atlassian.net/browse/OCPBUGS-84649))

- Before this update, the API Explorer used a stale namespace when projects were changed via **Home** → **Projects**. As a consequence, the API Explorer displayed resources from a previously selected namespace instead of the current project. With this release, the console properly synchronizes namespace context across all navigation methods. As a result, the API Explorer reflects the correct namespace regardless of how projects are selected. ([OCPBUGS-84669](https://redhat.atlassian.net/browse/OCPBUGS-84669))

- Before this update, ESLint Testing Library configuration had inconsistencies identified during pull request review. As a consequence, test code used relative imports escaping package boundaries and included unnecessary act() wrappers. With this release, the ESLint configuration enforces proper Testing Library patterns. As a result, console tests use absolute imports and follow Testing Library best practices. ([OCPBUGS-84856](https://redhat.atlassian.net/browse/OCPBUGS-84856))

- Before this update, the `ConsoleDataView` component only included pagination controls in the top toolbar. As a consequence, pagination controls were unavailable on mobile viewports where the top pagination condenses to just an item count. With this release, the `ConsoleDataView` component includes both top and bottom pagination controls. As a result, full pagination controls remain accessible on mobile viewports. ([OCPBUGS-84876](https://redhat.atlassian.net/browse/OCPBUGS-84876))

- Before this update, the "Welcome to the new OpenShift experience" guided tour modal appeared briefly on every page reload. As a consequence, users who had already completed or skipped the tour saw the intro modal flash and disappear on each reload. With this release, the console properly synchronizes tour completion state before rendering the modal. As a result, the tour intro modal does not appear for users who have already completed or skipped the tour. ([OCPBUGS-85545](https://redhat.atlassian.net/browse/OCPBUGS-85545))

- Before this update, the `ColumnManagementModal` did not show the namespace column help text. As a consequence, users did not see the message explaining that the namespace column only appears when **All projects** is selected. With this release, the `ColumnManagementModal` correctly displays the namespace column help text. As a result, users see the explanatory message about namespace column visibility conditions. ([OCPBUGS-86182](https://redhat.atlassian.net/browse/OCPBUGS-86182))

- Before this update, the terminal opt key acted as a "meta" key on macOS instead of sending proper Alt sequences. As a consequence, macOS users could not use Alt+arrow shortcuts and other standard terminal key combinations. With this release, the terminal properly configures the opt key behavior on macOS. As a result, macOS users can use standard terminal keyboard shortcuts. ([OCPBUGS-86491](https://redhat.atlassian.net/browse/OCPBUGS-86491))

- Before this update, the console created new user-settings ConfigMaps on each user login instead of reusing existing ones. As a consequence, the openshift-console-user-settings namespace accumulated thousands of duplicate ConfigMaps over time. With this release, the console reuses existing user-settings ConfigMaps across sessions. As a result, one ConfigMap per user is created and reused for storing UI preferences. ([OCPBUGS-86564](https://redhat.atlassian.net/browse/OCPBUGS-86564))

- Before this update, several console Playwright tests had high failure rates in CI. As a consequence, the merge queue was frequently blocked by failing alertmanager, oauth, and update-modal end-to-end suites. With this release, the flaky tests are fixed and re-enabled. As a result, console Playwright tests run reliably in CI. ([OCPBUGS-88451](https://redhat.atlassian.net/browse/OCPBUGS-88451))

- Before this update, users could not filter projects by display name on the **Projects** list page. As a consequence, searching for projects by their display name annotation returned no results. With this release, the project filter searches both project names and display names. As a result, users can filter projects by either name or display name. ([OCPBUGS-88739](https://redhat.atlassian.net/browse/OCPBUGS-88739))

- Before this update, users were logged out of the console after exactly 5 minutes when certain console plugins encountered errors. As a consequence, users with pipeline or network observability plugins installed experienced frequent unexpected logouts. With this release, the console properly handles plugin errors without terminating user sessions. As a result, plugin errors do not cause premature user session termination. ([OCPBUGS-90370](https://redhat.atlassian.net/browse/OCPBUGS-90370))

- Before this update, the console cluster Operator reported `Progressing=True` during deployment specification updates in the upgrade window. As a consequence, upgrade monitoring tests failed due to brief Progressing conditions during legitimate Operator updates. With this release, the console Operator only reports `Progressing=True` for genuine deployment rollout delays. As a result, the console Operator does not report false Progressing conditions during upgrade specification updates. ([OCPBUGS-93982](https://redhat.atlassian.net/browse/OCPBUGS-93982))

- Before this update, Helm backend tests failed in CI with ChartMuseum connection errors. As a consequence, pull requests unrelated to Helm functionality failed CI checks. With this release, the Helm test suite properly handles ChartMuseum initialization. As a result, Helm backend tests run reliably in CI. ([OCPBUGS-94089](https://redhat.atlassian.net/browse/OCPBUGS-94089))

- Before this update, the console did not include a quick start for JBoss EAP 8.1. As a consequence, users could not access guided deployment instructions for JBoss EAP 8.1. With this release, the console includes an OpenShift quick start for JBoss EAP 8.1. As a result, users can access step-by-step deployment guidance for JBoss EAP 8.1. ([OCPBUGS-95602](https://redhat.atlassian.net/browse/OCPBUGS-95602))

- Before this update, Knative Cypress end-to-end tests were disabled due to high failure rates. As a consequence, Knative-related changes were not tested in CI. With this release, the Knative Cypress tests are fixed and re-enabled. As a result, Knative functionality is properly tested in CI. ([OCPBUGS-99292](https://redhat.atlassian.net/browse/OCPBUGS-99292))

- Before this update, upgrading react-virtualized to 9.22.6 broke `CellMeasurer` height measurement in virtualized tables. As a consequence, table rows overlapped each other as all rows rendered at 44px height regardless of content. With this release, the `TableRow` component supports ref forwarding for `CellMeasurer`. As a result, virtualized tables correctly measure and size rows based on content height. ([OCPBUGS-99475](https://redhat.atlassian.net/browse/OCPBUGS-99475))

- Before this update, the Installed Operators table row cells ignored column management selections. As a consequence, hiding columns by using "Manage columns" only affected headers while row data remained visible. With this release, the Installed Operators table rows respect column management selections. As a result, both column headers and row data reflect column management choices. ([OCPBUGS-99491](https://redhat.atlassian.net/browse/OCPBUGS-99491))

- Before this update, the terminal `ResizeObserver` could access uninitialized xterm render service dimensions. As a consequence, pod terminal pages crashed with "Cannot read properties of undefined" errors in end-to-end tests. With this release, the terminal `ResizeObserver` guards against uninitialized xterm internals. As a result, the pod terminal loads reliably without resize-related crashes. ([OCPBUGS-105314](https://redhat.atlassian.net/browse/OCPBUGS-105314))

- Before this update, the node-groups-filter end-to-end test used an incorrect data-test ID. As a consequence, the Playwright test failed to find the **Edit groups** button and failed on every CI run. With this release, the test uses the correct data-test ID matching the `PageHeading` component. As a result, the node-groups-filter end-to-end test passes reliably. ([OCPBUGS-105318](https://redhat.atlassian.net/browse/OCPBUGS-105318))

- Before this update, Helm chart installation by using an OCI URL with a version number failed. As a consequence, users could not install Helm charts by providing URLs such as OCI://registry-1.docker.io/bitnamicharts/nginx:22.6.12. With this release, the console correctly handles OCI URLs with version numbers in the **Chart URL** field. As a result, users can install Helm charts from OCI registries by specifying the complete URL with version. ([OCPBUGS-105603](https://redhat.atlassian.net/browse/OCPBUGS-105603))

- Before this update, the data view bulk selection column displayed unexpected gaps in the UI. As a consequence, the bulk selection column appeared misaligned or incomplete. With this release, the data view bulk selection column renders consistently. As a result, the bulk selection column displays correctly without visual gaps. ([OCPBUGS-106132](https://redhat.atlassian.net/browse/OCPBUGS-106132))

- Before this update, the console required cloud provider configuration during Operator installation on Workload Identity clusters. As a consequence, users could not install Operators such as External Secrets or cert-manager without immediately providing cloud-specific credentials. With this release, cloud provider configuration fields are optional during Operator installation. As a result, users can install Operators and configure cloud provider integration as a Day 2 operation. ([OCPBUGS-111921](https://redhat.atlassian.net/browse/OCPBUGS-111921))

- Before this update, the **Overview** page of **Control Plane Status** panel showed 0% for all components on healthy clusters. As a consequence, the console incorrectly indicated that API Servers, Controller Managers, and Schedulers were degraded. With this release, the **Control Plane Status** panel correctly queries and displays component health metrics. As a result, the **Control Plane Status** panel shows accurate response rates for all components. ([OCPBUGS-122258](https://redhat.atlassian.net/browse/OCPBUGS-122258))

- Before this update, the Namespace column was hidden on the **Node Pods** tab when a specific namespace was selected. As a consequence, users could not identify which namespace pods belonged to on the **Node Details** page, even though nodes are cluster-scoped and can display pods from multiple namespaces. With this release, the **Namespace** column displays on the **Node Pods** tab regardless of project selector state. As a result, users can identify the namespace for each pod on the **Node Details** page. ([OCPBUGS-123202](https://redhat.atlassian.net/browse/OCPBUGS-123202))

## Monitoring

- Before this update, when Prometheus compacted time series data, it attempted to enable direct I/O on files that were already open. Some file systems, such as IBM Storage Scale, do not support this operation. As a consequence, compaction failed with a `cannot enable Direct IO: invalid argument` error, Prometheus could not write chunks to disk, and memory usage in Prometheus pods increased until the pods hit their memory limits and restarted or affected other workloads on the node. With this release, Prometheus detects when a file system does not support direct I/O on open files and handles the condition gracefully. As a result, Prometheus writes chunks to disk and completes compaction successfully on these storage back ends. ([OCPBUGS-92191](https://redhat.atlassian.net/browse/OCPBUGS-92191))

- Before this update, the Cluster Monitoring Operator (CMO) checked only the `openshift-config/pull-secret` for the `cloud.openshift.com` authentication token used by the telemeter client. As a consequence, on platforms where this secret did not contain the token, such as the Microsoft Azure Red Hat OpenShift hosted control planes, the telemeter client was not deployed, which prevented cluster registration in Red Hat OpenShift Cluster Manager. With this release, the CMO falls back to `kube-system/global-pull-secret` if the token is not found in the primary secret. As a result, the telemeter client is deployed correctly. ([OCPBUGS-98450](https://redhat.atlassian.net/browse/OCPBUGS-98450))

- Before this update, Alertmanager crashed because the `tzdata` package was missing in the OpenShift Container Platform base images, This issue caused the absence of the `/usr/share/zoneinfo` directory. As a consequence, Alertmanager pods failed to start, which made time-based alerts inaccessible for the time zones. With this release, the `tzdata` package is reinstated in OpenShift Container Platform images. As a result, Alertmanager does not crash on startup when location fields are present in the `active_interval` or `mute_interval` entries. ([OCPBUGS-99435](https://redhat.atlassian.net/browse/OCPBUGS-99435))

- Before this update, containers in the `openshift-monitoring` namespace ran with writable root filesystems because `readOnlyRootFilesystem: true` was not enabled in their security contexts. As a consequence, customer compliance scans flagged these containers as security policy violations. With this release, monitoring components enable read-only root filesystems with dedicated `emptyDir` volumes for paths requiring write access. As a result, monitoring containers meet compliance requirements for read-only root filesystems. ([OCPBUGS-105389](https://redhat.atlassian.net/browse/OCPBUGS-105389))

- Before this update, Fibre Channel adapters reported incomplete data. As a consequence, the node_exporter failed to run. With this release, guards are added to ignore incomplete data. ([OCPBUGS-112719](https://redhat.atlassian.net/browse/OCPBUGS-112719))

## must-gather

- Before this update, `oc adm must-gather` collected the OpenShift console OAuth client secret in plain text within the `cluster-scoped-resources/oauth.openshift.io/oauthclients/console.yaml` file. As a consequence, sensitive OAuth `client_secret` values were exposed in must-gather archives, creating a security risk when sharing diagnostic data. With this release, `oc adm inspect` and `must-gather` redact `OAuthClient.secret` fields before writing YAML output, consistent with Secret, Route TLS, and Proxy credential handling. As a result, must-gather archives no longer contain plain text OAuth client secrets. ([OCPBUGS-99013](https://redhat.atlassian.net/browse/OCPBUGS-99013))

## Networking

- Before this update, the `CredentialsRequest` manifests for ingress on IBM Cloud and IBM Power Virtual Server were missing `include.release.openshift.io` annotations. As a consequence, the `oc adm release extract --credentials-requests --included` command excluded these manifests, and installations with manually managed credentials failed because the Ingress Operator could not create the `\*.apps` DNS record, resulting in a `DNSReady=False` status. With this release, the missing annotations are added to the `CredentialsRequest` manifests. As a result, installations using manually managed credentials succeed. ([OCPBUGS-36723](https://issues.redhat.com/browse/OCPBUGS-36723))

- Before this update, the `Wildcard` policy of an Ingress Controller prevented new routes from reusing earlier host names until an administrator restarted the router. As a consequence, affected routes reported a `HostAlreadyClaimed` error. With this release, the Ingress Controller allows new routes to reuse earlier host names immediately when the `Wildcard` policy is active. As a result, administrators can update host names seamlessly without restarting the router. ([OCPBUGS-49738](https://redhat.atlassian.net/browse/OCPBUGS-49738))

- Before this update, clicking **Create Ingress** on the web console **Search** page, after searching for Ingress resources, redirected users to a `404: Page Not Found` error instead of the Ingress creation form. As a consequence, users could not create an Ingress resource directly from the **Search** page and had to go to the creation form through another part of the console. With this release, the **Create Ingress** button on the **Search** page links to the correct URL. As a result, clicking **Create Ingress** from the **Search** page opens the Ingress creation form as expected. ([OCPBUGS-54248](https://issues.redhat.com/browse/OCPBUGS-54248))

- Before this update, the HAProxy tunnel timeout was longer than the AWS Network Load Balancer (NLB) idle timeout of `350` seconds when an Ingress Controller used an NLB. As a consequence, the NLB evicted idle connections without notification, causing TCP resets for clients. With this release, the Ingress Operator sets a shorter tunnel timeout that allows HAProxy to close idle connections before the NLB evicts them. As a result, clients receive a clean connection close instead of a TCP reset. ([OCPBUGS-54702](https://issues.redhat.com/browse/OCPBUGS-54702))

- Before this update, HAProxy assumed all client source addresses were IPv4 and did not enclose IPv6 addresses in brackets in the `Forwarded` header. As a consequence, IPv6 client requests produced noncompliant headers that could cause applications to fail to parse the client address. With this release, HAProxy checks the IP family of each source address and adds brackets around IPv6 addresses. As a result, the Ingress Controller produces correctly formatted `Forwarded` headers for both IPv4 and IPv6 client addresses. ([OCPBUGS-62267](https://issues.redhat.com/browse/OCPBUGS-62267))

- Before this update, AWS Network Load Balancers (NLBs) had native client IP preservation enabled by default. As a consequence, hairpin connection failures occurred when a pod connected to an internal NLB route that returned traffic to a router pod on the same node, causing connection timeouts. With this release, a protocol field is added to the `IngressController` API, and new NLB Ingress Controllers default to `PROXY` protocol version 2, which disables native client IP preservation. As a result, hairpin connections no longer fail, and an informational alert notifies administrators to configure the protocol field when upgrading. ([OCPBUGS-63219](https://issues.redhat.com/browse/OCPBUGS-63219))

- Before this update, `LLDP` settings from the underlying interface were not preserved on the `br-ex` bridge. As a consequence, enabling `LLDP` on `br-ex` required unsupported workarounds that could corrupt the network setup and cause nodes to lose connectivity on reboot. With this release, `LLDP` settings from the underlying interface are persisted on `br-ex`. As a result, `LLDP` can be enabled without disrupting network. ([OCPBUGS-63650](https://issues.redhat.com/browse/OCPBUGS-63650))

- Before this update, the OpenShift Router performed synchronous and sequential `SubjectAccessReview` (SAR) API calls to validate each externally-managed certificate for a route during startup. As a consequence for a cluster with a high amount of external certificate routes, the kubelet killed any router pod that exceeded the `120` second startup probe timeout value. With this release, an SAR caching mechanism, `sarCache`, and a semaphore throttles concurrent SAR API calls in the router. This process happens alongside any increasing route status that has a writer-lease concurrency. As a result, the initialization time of an OpenShift Router is dramatically reduced. This change allows thousands of routes with external certificates to load within the startup probe window and prevents router pods from entering a `CrashLoopBackOff` loop. ([OCPBUGS-77056](https://issues.redhat.com/browse/OCPBUGS-77056))

- Before this update, the NMState console plugin did not handle empty node selections when creating a `NodeNetworkConfigurationPolicy` (NNCP) resource. As a consequence, creating an NNCP without selecting nodes through the web console caused an error that prevented policy creation. With this release, the console plugin correctly processes empty node selections. As a result, you can create NNCP resources through the web console without errors. ([OCPBUGS-77435](https://issues.redhat.com/browse/OCPBUGS-77435))

- Before this update, the Cluster DNS Operator considered a node `schedulable` if any one of its taints was tolerated. As a consequence, nodes with many taints could be wrongly marked as `schedulable`. With this release, the Cluster DNS Operator checks that all taints are tolerated before marking a node `schedulable`. As a result, nodes with many taints are correctly marked `schedulable` only when every taint is tolerated. ([OCPBUGS-77532](https://issues.redhat.com/browse/OCPBUGS-77532))

- Before this update, the `nodeSelector` field description for the `NodeNetworkConfigurationPolicy` (NNCP) custom resource did not clarify that only simple key-value equality matching was supported. As a consequence, users expected that `matchLabels` and `matchExpressions` constructs would work in the `nodeSelector` field. However, the policy was rejected when they tried to use the constructs. With this release, the `nodeSelector` field description clarifies that only direct key-value pair matching is supported. As a result, `oc explain nncp.spec.nodeSelector` accurately describes the supported syntax. ([OCPBUGS-78801](https://issues.redhat.com/browse/OCPBUGS-78801))

- Before this update, OVN-Kubernetes used the `vm.kubevirt.io/name` label to identify `virt-launcher` pods during live migration status checks. As a consequence, when many virtual machines in the same namespace had the same `spec.template.spec.hostname` value, they shared the same label value on their `virt-launcher` pods. This caused the third and later VMs to fail to start with the error `Failed to discover live migration status: unexpected live migration state at pods`, as OVN-Kubernetes wrongly identified pods from other VMs. With this release, OVN-Kubernetes correctly identifies `virt-launcher` pods when many VMs share the same hostname. As a result, virtual machines start successfully regardless of whether other VMs in the namespace use the same hostname value. ([OCPBUGS-79408](https://issues.redhat.com/browse/OCPBUGS-79408))

- Before this update, the **Create UserDefinedNetwork** form in a web console did not trim whitespace from subnet CIDR values before submitting. As a consequence, copying a CIDR value with whitespace triggered a validation error. With this release, the form trims whitespace from CIDR input before validation. As a result, users can copy CIDR values with whitespace without errors. ([OCPBUGS-81271](https://issues.redhat.com/browse/OCPBUGS-81271))

- Before this update, when a virtual machine pod on a localnet OVN-Kubernetes secondary network was deleted, OVN-Kubernetes might not remove the logical switch port from the northbound database. As a consequence, an orphaned logical switch port with the same MAC address remained alongside the replacement pod port, causing network connectivity issues. With this release, OVN-Kubernetes correctly removes the logical switch port for deleted pods. As a result, virtual machine pods can be recreated on localnet secondary networks without connectivity issues. ([OCPBUGS-81326](https://issues.redhat.com/browse/OCPBUGS-81326))

- Before this update, in environments with high pod churn, learned Border Gateway Protocol (BGP) routes might get uninstalled from the cluster when using the FRR-K8s daemon. As a consequence, traffic that relied on those routes failed and affected BGP configurations managed by either the `RouteAdvertisements` feature or the MetalLB Operator. With this release, FRR is upgraded from version 8 to version 10. As a result, learned BGP routes remain properly installed in the routing table. ([OCPBUGS-84304](https://issues.redhat.com/browse/OCPBUGS-84304))

- Before this update, the `istio-proxy` and discovery containers in the `openshift-ingress` namespace did not set `terminationMessagePolicy` to `FallbackToLogsOnError`. As a consequence, less diagnostic information was available when containers terminated with errors. With this release, both containers set `terminationMessagePolicy=FallbackToLogsOnError`. As a result, container logs are used as the termination message when these containers exit with errors, improving diagnosis of Gateway API failures. ([OCPBUGS-84491](https://issues.redhat.com/browse/OCPBUGS-84491))

- Before this update, containers in the `openshift-ovn-kubernetes` namespace did not set `terminationMessagePolicy` to `FallbackToLogsOnError`. As a consequence, less diagnostic information was available when containers terminated with errors. With this release, the affected containers set `terminationMessagePolicy=FallbackToLogsOnError`. As a result, container logs are used as the termination message when these containers exit with errors, improving diagnosis of OVN-Kubernetes failures. ([OCPBUGS-84519](https://issues.redhat.com/browse/OCPBUGS-84519))

- Before this update, a race condition existed in the startup order of the grandmaster clock (T-GM) `ptp` process. As a consequence, at startup, the system time was occasionally offset by 37 seconds from the time advertised by the PTP grandmaster clock. This meant that the operating system could take several hours to synchronize with GNSS time. With this release, the process startup logic is reordered to eliminate the race condition. As a result, the system time synchronizes directly with the PTP grandmaster clock without the initial 37-second offset. ([OCPBUGS-85586](https://issues.redhat.com/browse/OCPBUGS-85586))

- Before this update, the DNS Operator treated a difference between desired and up-to-date pod counts as evidence of an ongoing rollout. As a consequence, cluster scale-up caused the Operator to report `Progressing=True` even though no DNS configuration change was underway. With this release, the DNS Operator verifies that a `DaemonSet` is actively rolling out by checking its observed generation and scheduled pod count. As a result, cluster scale-up no longer causes false `Progressing=True` reports. ([OCPBUGS-86009](https://issues.redhat.com/browse/OCPBUGS-86009))

- Before this update, attempting to edit the pod selector for certain system services in the web console caused the page to go blank. As a consequence, you could not change pod selectors for these services and had to refresh the browser. With this release, the web console properly handles the "Edit Pod selector" action for system services. As a result, you can edit pod selectors without encountering a blank page. ([OCPBUGS-86249](https://redhat.atlassian.net/browse/OCPBUGS-86249))

<!-- -->

- Before this update, the Precision Time Protocol (PTP) Operator relied on the digital phase-locked loop (DPLL) pin administrative state field to validate pin reports and determine clock synchronization status. As a consequence, when running on RHEL 9.6 and later kernels where the DPLL API separates administrative state (such as `selectable`) from operational state (such as `connected`), Telecom Grandmaster (T-GM) and Telecom Boundary Clock (T-BC) configurations failed to achieve lock and reported an `Unlocked` status. With this release, the PTP Operator supports the new DPLL pin operational state field introduced in RHEL 9.6. As a result, T-GM and T-BC configurations correctly achieve lock and report the proper synchronization status when running on RHEL 9.6 and later kernels. ([OCPBUGS-86565](https://issues.redhat.com/browse/OCPBUGS-86565))

- Before this update, when the Cluster Ingress Operator migrated Gateway API from OLM-managed to the Sail Library path, the Operator stopped managing the OLM subscription without notification. As a consequence, administrators had no way to know that the subscription was orphaned. With this release, an `OrphanedOSSMSubscription` Prometheus alert, metric, and `ClusterOperator` status condition were added to detect orphaned subscriptions and provide remediation guidance. As a result, administrators are notified when subscriptions are orphaned and receive clear guidance on next steps. ([OCPBUGS-86833](https://issues.redhat.com/browse/OCPBUGS-86833))

- Before this update, the Ingress Node Firewall Operator used exact label matching instead of Kubernetes label selector semantics. As a consequence, `IngressNodeFirewallNodeState` objects were not created for nodes added after startup. With this release, the Operator uses proper Kubernetes label selector matching. As a result, the Operator creates `IngressNodeFirewallNodeState` objects for dynamically added nodes or nodes with changed labels. ([OCPBUGS-86839](https://issues.redhat.com/browse/OCPBUGS-86839))

- Before this update, a HAProxy 2.8 issue was exposed when dynamically populating empty backends. As a consequence, the Dynamic Config Manager failed to register new backend servers, causing configuration errors. With this release, HAProxy is updated to include a patch that adds the backend server ID when dynamically adding servers to empty backends. As a result, the Dynamic Config Manager correctly registers new backend servers when routes are dynamically populated. ([OCPBUGS-87082](https://issues.redhat.com/browse/OCPBUGS-87082))

- Before this update, on dual-stack clusters, IPv6 egress IP addresses were not assigned to available nodes. As a consequence, traffic relying on IPv6 egress IPs did not egress with the expected source address. With this release, OVN-Kubernetes correctly assigns IPv6 egress IPs to available nodes. As a result, both IPv4 and IPv6 egress IP addresses are assigned as expected. ([OCPBUGS-87249](https://issues.redhat.com/browse/OCPBUGS-87249))

- Before this update, for Telecom Boundary Clock (T-BC) configurations, the cloud event proxy incorrectly derived the `CLOCK_REALTIME` synchronization state due to dual-publisher overrides and race conditions in `masterOffsetSource`. As a consequence, the `CLOCK_REALTIME` sync-state metric and cloud event oscillated between `LOCKED` and `FREERUN`, or became stuck in incorrect states. With this release, `phc2sys` acts as the sole publisher, and state is derived using `worst_of` (`phc2sys_state`, upstream PTP lock state) per O-RAN O-Cloud Notification API v04.00 Table 37. As a result, `CLOCK_REALTIME` accurately reflects both the `phc2sys` offset and upstream PTP lock state without spurious oscillation. ([OCPBUGS-88369](https://redhat.atlassian.net/browse/OCPBUGS-88369))

- Before this update, the `gatewayclass` controller set up watches on `Subscription` and `InstallPlan` OLM resources without checking whether the `OperatorLifecycleManager` capability was enabled. As a consequence, on clusters without OLM, the controller blocked indefinitely during startup, making Gateway API non-functional. With this release, the OLM resource watches are guarded with an `OperatorLifecycleManagerEnabled` check. As a result, the `gatewayclass` controller starts successfully on clusters without OLM. ([OCPBUGS-90505](https://issues.redhat.com/browse/OCPBUGS-90505))

- Before this update, the MetalLB Operator RBAC rules granted unnecessary permissions. As a consequence, the service account held broader privileges than required, increasing security exposure. With this release, the unneeded RBAC permissions are removed. As a result, the `ClusterRole` reflects only the permissions needed to operate. ([OCPBUGS-91651](https://issues.redhat.com/browse/OCPBUGS-91651))

- Before this update, the `ovn-ipsec` container startup script attempted to execute platform-python from a host mount point on s390x systems, but the executable was not available on the host. As a consequence, `IPsec` pods failed to start, preventing IPsec-enabled cluster installations from completing on s390x. With this release, the Cluster Network Operator no longer mounts `/usr/libexec` from the host, allowing the container to use its bundled executable. As a result, IPsec-enabled cluster installations complete successfully on s390x systems. ([OCPBUGS-98149](https://issues.redhat.com/browse/OCPBUGS-98149))

- Before this update, the Kubernetes NMState Operator applied status updates without taking ownership of the status field. As a consequence, status updates were rejected with field-ownership conflicts after upgrades, leaving the NMState CR status permanently frozen. With this release, the Kubernetes NMState Operator takes ownership of the status field when applying updates. As a result, the NMState CR status updates correctly after Operator upgrades. ([OCPBUGS-98155](https://issues.redhat.com/browse/OCPBUGS-98155))

- Before this update, after a fix for duplicate PTP events in NTP failover scenarios, the `openshift_ptp_clock_state` metric reported a `CLOCK_REALTIME` value for both the `phc2sys` and `chronyd` services at the same time. As a consequence, the reported clock state no longer matched the process that was actually active. A process that was not running could still show `CLOCK_REALTIME` as locked, making it unclear which time source the node was synchronized to. With this release, the stale `CLOCK_REALTIME` metric for the inactive process is removed when clock synchronization switches between `phc2sys` and `chronyd` services. As a result, only one `CLOCK_REALTIME` `openshift_ptp_clock_state` metric is present at a time, and the metric corresponds to the currently active process. ([OCPBUGS-98227](https://issues.redhat.com/browse/OCPBUGS-98227))

- Before this update, the Cluster Ingress Operator used the `sail-operator` library based on OpenShift Service Mesh (OSSM) 3.3, which deployed Istio version 1.28.5 for Gateway API integration. As a consequence, clusters by using the Gateway API with Istio integration ran an older Istio version with known fixed CVEs from the upstream Istio 1.28 release stream. With this release, the vendored `sail-operator` library is upgraded to OSSM 3.4.0, which deploys Istio 1.28.8. As a result, Gateway API deployments by using Istio integration include accumulated CVE fixes, bug fixes, and API improvements from the OSSM 3.4.0 release. ([OCPBUGS-98310](https://issues.redhat.com/browse/OCPBUGS-98310))

- Before this update, the `nmstate-configuration.sh` script used an invalid shell test expression when comparing the checksum of the applied NMState configuration to the current configuration to decide whether to skip reconfiguration. As a consequence, this comparison always failed silently, so the script always deleted the `br-ex` and `br0` Open vSwitch bridges on every run, even when the configuration was unchanged. Because `configure-ovs.sh` and `nmstatectl` then both skipped recreating the bridge, believing the configuration was already applied, the deleted `br-ex` bridge was never recreated. This caused a full network outage on any reboot of a node that used a NMState configuration from a cluster installation, such as a customized `br-ex` bridge. With this release, `nmstate-configuration.sh` uses valid shell syntax for the configuration comparison. As a result, the script correctly skips deleting and reapplying the OVS bridges when the NMState configuration is unchanged, and nodes with a NMState configuration from cluster installation retain network connectivity across reboots. ( [OCPBUGS-98316](https://issues.redhat.com/browse/OCPBUGS-98316))

- Before this update, the `FRRouting` (FRR) Bidirectional Forwarding Detection (BFD) daemon, `bfdd`, opened many User Datagram Protocol (UDP) sockets for each virtual routing and forwarding (VRF) plugin. This situation happens even when BFD is not explicitly enabled and the default file descriptor limit, `MAX_FDS`, was set to `1024`. As a consequence, for clusters with a large number of `ClusterUserDefinedNetworks` and `RouteAdvertisements` CRs, the `frr-k8s` pods enter `CrashLoopBackOff` because FRR exhausts its file descriptor limit. With this release, the FRR `MAX_FDS` value is changed from `1024` to `65536` to accommodate high-scale production networks with many VRFs. As a result, the `frr-k8s` pods can start and run successfully in clusters with a large number of `ClusterUserDefinedNetworks` and `RouteAdvertisements` CRs without hitting file descriptor exhaustion. ([OCPBUGS-98619](https://issues.redhat.com/browse/OCPBUGS-98619))

- Before this update, the network-check-source `ServiceMonitor` in the `openshift-network-diagnostics` namespace set `insecureSkipVerify: true` in its `tlsConfig`. As a consequence, Prometheus did not validate the TLS certificate presented by the network-check-source pod when scraping its metrics, leaving the scrape connection vulnerable to man-in-the-middle attacks. With this release, the network-check-source `ServiceMonitor` uses a `service-ca-signed` certificate and no longer disables TLS certificate validation. As a result, Prometheus validates the certificate when scraping network-check-source metrics. ([OCPBUGS-98918](https://issues.redhat.com/browse/OCPBUGS-98918))

- Before this update, the `ts2phc` process started before the upstream Precision Time Protocol (PTP) was stable on Telecom Boundary Clock (T-BC). As a consequence, the T-BC was slow to converge, causing `phc2sys` to adjust the system clock too early based on an irrelevant time offset before the hardware clock had stabilized. With this release, a delay is added to `ts2phc` on the T-BC until the time source is fully qualified and `phc2sys` is ready, while leaving T-GM behavior unchanged. As a result, the T-BC cannot attempt to synchronize against an unverified clock source. ([OCPBUGS-99070](https://issues.redhat.com/browse/OCPBUGS-99070))

- Before this update, on a cluster configured with many `clusterNetwork` Classless Inter-Domain Routing (CIDR), the priority 102 no-reroute logical router policies that OVN-Kubernetes creates for egress IP only matched pod traffic between nodes on the same cluster network CIDR. As a consequence, when a pod with an assigned egress IP tried to reach a pod on a node in a different cluster network CIDR, the traffic did not match a no-reroute policy and instead matched the lower-priority egress IP reroute policy, wrongly sending pod-to-pod traffic through the egress gateway router and breaking connectivity. With this release, the no-reroute logical router policies also match pod-to-pod traffic across different cluster network CIDRs. As a result, pods with an assigned egress IP can reach pods on nodes in a different cluster network CIDR. ([OCPBUGS-99636](https://issues.redhat.com/browse/OCPBUGS-99636))

- Before this update, when the Network Time Protocol (NTP) failover plugin was enabled, the `ts2phc` process deadlocked while writing to its standard output pipe. As a consequence, `ts2phc` failed to produce log output, and the Grandmaster (T-GM) clock never achieved a locked state. With this release, the `ts2phc` standard output deadlock is resolved. As a result, `ts2phc` logs correctly and the Grandmaster clock locks as expected when NTP failover is enabled. ([OCPBUGS-100049](https://issues.redhat.com/browse/OCPBUGS-100049))

- Before this update, when the `ptpSettings.logReduce` setting was changed and the `linuxptp` daemon reloaded its PTP profiles, a clock could briefly transition to `HOLDOVER` state and then not return to `LOCKED` state when the holdover period expired, even though the underlying PTP offsets remained healthy. As a consequence, the affected clock reported a `FREERUN` state indefinitely after the profile reload, instead of relocking. With this release, clocks relock correctly after a profile reload triggered by a `ptpSettings.logReduce` change. As a result, clocks return to a `LOCKED` state as expected after the reload. ([OCPBUGS-104533](https://issues.redhat.com/browse/OCPBUGS-104533))

- Before this update, the `IngressController` API in OpenShift Container Platform 4.22 lacked an `haproxyVersion` field. As a consequence, customers could not pin the HAProxy version before upgrading from 4.22 to 5.0, potentially resulting in unexpected HAProxy version changes after the upgrade. With this release, the `haproxyVersion` field is added to the `IngressController` API in OpenShift Container Platform 4.22.11. As a result, administrators can set `haproxyVersion: "2.8"` in their `IngressController` resources to ensure HAProxy remains at version 2.8 after upgrading to OpenShift Container Platform4.17. ([OCPBUGS-105261](https://issues.redhat.com/browse/OCPBUGS-105261))

- Before this update, on Boundary Clock (BC) and Telecom Boundary Clock (T-BC) nodes configured with `phc2sysOpts: -a -r`, the cloud-event-proxy sidecar determined the `os-clock-sync-state` (`CLOCK_REALTIME`) synchronization state only from `phc2sys` `CLOCK_REALTIME` offset log lines. As a consequence, when the upstream or remote time source was lost and `phc2sys` stopped selecting `CLOCK_REALTIME` as a sink after reconfiguring, no offset samples were produced, and cloud-event-proxy kept reporting the last known state as `LOCKED` indefinitely. Applications watching `/sync/sync-status/os-clock-sync-state` never saw `FREERUN` while the synchronization chain was actually broken, even though the interface-level lock-state correctly reported `FREERUN`. With this release, cloud-event-proxy detects when `phc2sys` stops selecting `CLOCK_REALTIME` as a sink after a reconfiguration and publishes `FREERUN` for `os-clock-sync-state`; normal offset and threshold handling resumes once `CLOCK_REALTIME` offset reporting resumes. As a result, applications monitoring `os-clock-sync-state` correctly observe `FREERUN` when `CLOCK_REALTIME` synchronization is lost on BC and T-BC nodes. ([OCPBUGS-105425](https://issues.redhat.com/browse/OCPBUGS-105425))

- Before this update, the Ingress Operator reverted fields with non-empty default values to empty when unrelated changes occurred, and ignored all changes in `init` containers except for image URLs. As a consequence, when these fields were filled with distinct values, the Ingress Operator entered an endless reconciliation loop, repeatedly reverting and reapplying the same changes. With this release, fields defaulted by the API server and managed by the Operator are included in the copy and hash calculation. As a result, unrelated changes are reported only once without triggering an endless reconciliation loop. ([OCPBUGS-114134](https://issues.redhat.com/browse/OCPBUGS-114134))

- Before this update, Multus performed pod-wide sorting of SR-IOV and PCI device IDs when assigning network interfaces to containers. As a consequence, in multi-container pods where each container requested the same device resource, pod restarts could cause the wrong network interface to be assigned to the wrong container. This resulted in network-status peripheral component interconnect (PCI) addresses disagreeing with `PCIDEVICE_*` environment variables, leaving containers using an wrong Virtual Function (VF). With this release, Multus preserves the kubelet’s device allocation order instead of sorting devices across the entire pod. As a result, each container receives the correct mapping between its allocated device and network attachment, ensuring SR-IOV network interfaces are assigned correctly in multi-container workloads. ([OCPBUGS-114773](https://issues.redhat.com/browse/OCPBUGS-114733))

## Node

- Before this update, the upstream pod in-place resize scheduler-focused test expected a second test pod to remain in `Pending` phase when the first pod consumed all available CPU resources, but the scheduler incorrectly allowed the second pod to enter `Running` phase. As a consequence, the test failed consistently with the error "Expected pod 'testpod2' to be in phase Pending, but got phase: Running". With this release, the scheduler correctly enforces resource constraints during in-place resize operations. As a result, the test passes reliably and pods are scheduled according to available node resources. ([OCPBUGS-63132](https://redhat.atlassian.net/browse/OCPBUGS-63132))

- Before this update, when the `config-operator` restarted or experienced temporary API server connectivity issues, the `config-drift-monitor` emitted `ConfigDriftMonitorStopped` and `RemoveSigtermProtection` events repeatedly for each Tuned resource during recovery. As a consequence, the pathological events test failed in serial-techpreview jobs, reporting that these events occurred more than 20 times. With this release, the `config-drift-monitor` reduces event noise during restart and recovery scenarios. As a result, pathological event tests pass reliably in serial-techpreview jobs. ([OCPBUGS-63307](https://redhat.atlassian.net/browse/OCPBUGS-63307))

- Before this update, when the kubelet calculated resource capacity during pod resize operations with the `InPlacePodVerticalScaling` feature gate enabled, it incorrectly computed the used CPU value as an extremely large number instead of the actual value. As a consequence, pod resize requests failed with "OutOfcpu" errors even when sufficient CPU capacity was available on the node. With this release, the kubelet correctly calculates used CPU during resize operations. As a result, in-place pod vertical scaling requests succeed when the node has sufficient CPU resources. ([OCPBUGS-64847](https://redhat.atlassian.net/browse/OCPBUGS-64847))

- Before this update, when `AutoSizingReserved` option was enabled by default for all topologies including hosted control planes, the feature dynamically increased system-reserved memory based on node size, which significantly reduced allocatable memory on the small instance types, for example, m5.large and m5.xlarge used in hosted control planes worker nodes. As a consequence, platform pods such as monitoring, DNS, networking, and registry could not be scheduled on hosted control planes worker nodes due to insufficient allocatable memory, causing cluster Operators to degrade and e2e tests to fail. With this release, `AutoSizingReserved` option is disabled for hosted control planes worker nodes (`ControlPlaneTopology=External`). As a result, hosted control planes e2e tests pass and hosted control planes worker nodes have sufficient allocatable memory for all platform pods to schedule successfully. ([OCPBUGS-79502](https://redhat.atlassian.net/browse/OCPBUGS-79502))

- Before this update, when scheduling pods that request PCI devices on systems with very large Non-uniform Memory Access (NUMA) topologies (for example, NVIDIA GB200 systems with 34 NUMA nodes), the kubelet TopologyManager never finished computing topology hints because of combinatorial explosion in hint generation. As a consequence, pods requesting GPU, InfiniBand, or Non-Volatile Memory Express (NVMe) devices remained indefinitely in `Pending` state, and KubeVirt VirtualMachineInstances using `hostDevices` never transitioned to Running. With this release, the TopologyManager hint generation algorithm is optimized to compute hints in bounded time even on systems with many NUMA nodes. As a result, pods and VMs requesting PCI host devices start successfully on large NUMA systems such as GB200-class hardware. ([OCPBUGS-83502](https://redhat.atlassian.net/browse/OCPBUGS-83502))

- Before this update, OpenShift Container Platform switched to RHEL 10 as the default base operating system, but the `runc` OCI runtime binary was not included in the RHCOS 10 image. As a consequence, all CI jobs configured to use `runc` as the OCI runtime failed during bootstrap because CRI-O could not find the `runc` executable in `$PATH`, preventing container runtime initialization. With this release, the CI infrastructure for runc-based jobs is updated to ensure the runc binary is available in RHCOS 10 environments. As a result, runc-based CI jobs bootstrap successfully and complete without runtime errors. ([OCPBUGS-89267](https://redhat.atlassian.net/browse/OCPBUGS-89267))

- Before this update, the kubelet LimitedSwap Drop-in Configuration test case (TC6) for Container-Native Virtualization (CNV) failed during kubelet restart via `oc debug node`, which degraded worker nodes and left system configuration artifacts (`system_compressible` and `reserved-cpu-test` remnants). As a consequence, subsequent tests in the `disruptive-longrunning` suite needed significantly more time to complete, and the entire test suite timed out. With this release, the test properly cleans up node configuration and ensures kubelet restarts successfully without degrading the node. As a result, `disruptive-longrunning` test suites complete within the expected time without timeout failures. ([OCPBUGS-90507](https://redhat.atlassian.net/browse/OCPBUGS-90507))

- Before this update, the `CRIOCredentialProviderConfig` custom resource definition (CRD) immediately set `v1` as the storage version when first introduced. As a consequence, clusters that upgraded to a version containing this CRD could not safely roll back to earlier versions because the storage version change was not gradual. With this release, the CRD follows the rollback-safe versioning pattern and does not immediately change the storage version upon introduction. As a result, cluster administrators can safely roll back upgrades without encountering CRD storage version incompatibilities. ([OCPBUGS-94869](https://redhat.atlassian.net/browse/OCPBUGS-94869))

- Before this update, the upstream Kubernetes test for Dynamic Resource Allocation (DRA) extended resources deployed a DRA driver and sample device plugin on separate nodes, and the test infrastructure exhibited flakiness when the driver setup interacted with the device plugin. As a consequence, the test failed approximately 53% of the time in the serial suite with errors such as "endpoint not found in cache for a registered resource: example.com/resource". With this release, the test is skipped in the general serial lane, matching the upstream approach of testing DRA in a dedicated lane where the driver setup is more reliable. As a result, the serial suite no longer experiences frequent failures from this flaky DRA test infrastructure. ([OCPBUGS-99058](https://redhat.atlassian.net/browse/OCPBUGS-99058))

- Before this update, the CPU Partitioning conformance test enumerated all `openshift-*` namespaces and expected them to have the `workload.openshift.io/allowed:management` annotation, but did not exclude ephemeral `openshift-debug-*` namespaces created by `oc debug node/` commands in parallel `SecurityPenetration` tests. As a consequence, when `SecurityPenetration` tests ran concurrently with the CPU Partitioning test, the CPU Partitioning test failed because debug namespaces lacked the management annotation. With this release, the test excludes `openshift-debug-*` namespaces from the annotation check. As a result, the CPU Partitioning test passes reliably even when `SecurityPenetration` tests run in parallel. ([OCPBUGS-100392](https://redhat.atlassian.net/browse/OCPBUGS-100392))

- Before this update, when creating approximately 100 pods concurrently on the same node with each pod mounting the same OCI image as an Image volume, CRI-O acquired a write lock for every mount operation through the containers/storage layer. As a consequence, even though the image layer was already present on the node, all mount operations serialized behind a single lock, causing pod startup time to increase by approximately 80% compared to using EmptyDir volumes. With this release, CRI-O optimizes the image volume mount path to avoid unnecessary lock contention when mounting already-present image layers. As a result, mounting the same image across many pods on a node no longer significantly degrades pod startup performance. ([OCPBUGS-108950](https://redhat.atlassian.net/browse/OCPBUGS-108950))

## Node Tuning Operator

- Before this update, a failure to update the `PerformanceProfile` status due to a temporarily unavailable API server during an upgrade or under network load could leave the profile in a `Degraded` condition. As a consequence, the degraded condition might stop and never resolve, even after the cluster returned to a healthy state, because the Operator did not retry until the next reconcile event. With this release, the Operator schedules a retry of the status update until it succeeds, retrying approximately every 30 seconds. As a result, the stopped degraded status is temporary and resolves automatically during the next retry. ([OCPBUGS-62277](https://redhat.atlassian.net/browse/OCPBUGS-62277))

- Before this update, the Node Tuning Operator (NTO) reconciliation used the rate-limited work queue for all event enqueues. As a consequence, node-tuning configuration was delayed for cluster notes greater than 100. With this release, the NTO reconciliation loop uses the rate-limited work queue only for failures instead of all event enqueues. As a result, node-tuning configuration for cluster nodes greater than 100 is not delayed. ([OCPBUGS-112279](https://redhat.atlassian.net/browse/OCPBUGS-112279))

- Before this update, the short description for the `info` command in the Performance Profile Creator (PPC) tool was not updated after the cluster inspection was moved. As a consequence, inconsistencies between the parent help and the information help occurred when you ran the PPC tool. With this release, the short description for the `info` command in the PPC tool is updated to match the current CLI. As a result, the help inconsistencies do not occur when you run the tool. ([OCPBUGS-114144](https://redhat.atlassian.net/browse/OCPBUGS-114144))

- Before this update, you were required to enable timer migration to prevent TCP and other leftover timers from interfering with latency-sensitive workloads. As a consequence, this migration increased latency for high-resolution timers and disrupted benchmarks such as the `cyclictest` tool. With this release, the improved timer wheel logic in Red Hat Enterprise Linux (RHEL) 10 allows you to disable timer migration. As a result, both polling and high-resolution timer latency-sensitive workloads run without interruption from leftover timers. ([OCPBUGS-114934](https://redhat.atlassian.net/browse/OCPBUGS-114934))

- Before this update, a race condition between the Red Hat Enterprise Linux CoreOS (RHCOS) CPU hotplug `udev` rule and the Node Tuning Operator service that offlines the CPUs defined in the performance profile brought some offlined CPUs back online. As a consequence, when you applied a `PerformanceProfile` that offlined CPUs from more than one NUMA node, only a subset of the specified CPUs remained offline after the node booted. With this release, the race condition is resolved. As a result, all CPUs listed in the `offlined` field of the performance profile remain offline after the node boots. ([OCPBUGS-128909](https://redhat.atlassian.net/browse/OCPBUGS-128909))

- Before this update, the NUMA Resources Operator did not validate the `spec.imageSpec` field in the `NUMAResourcesScheduler` custom resource (CR). As a consequence, users with write access to this cluster-scoped CR could run arbitrary container images with scheduler privileges. With this release, the Operator validates scheduler images and accepts only digest-based references (such as `registry.redhat.io/openshift4/noderesourcetopology-scheduler-rhel9@sha256:<digest>`) matching trusted images embedded in the Operator. As a result, images that do not meet these requirements cause the `NUMAResourcesScheduler` resource to enter a `Degraded` state with reason `InvalidSchedulerImage`. ([OCPBUGS-94176](https://redhat.atlassian.net/browse/OCPBUGS-94176))

  > [!IMPORTANT]
  > If you set a custom image in `spec.imageSpec` (for example, a tag-based reference), the resource enters a `Degraded` state after upgrading to this release.

  To restore the scheduler:

- Update `spec.imageSpec` to use a `sha256` digest reference from the current production stream.

- Add your custom image digest to the trusted list using the `SCHEDULER_IMAGE_DIGESTS` environment variable in the Operator subscription.

- Disable validation by setting `SCHEDULER_IMAGE_VALIDATION` to `false` in the Operator subscription. This removes security protection; use only when required.

For more information, see [Scheduling NUMA-aware workloads](../scalability_and_performance/cnf-numa-aware-scheduling.xml#cnf-numa-aware-scheduling).

## Observability

## oc

- Before this update, the `kubectl describe` conformance test contained a race condition that caused intermittent failures when checking if `kubectl describe` prints relevant information for replication controllers and pods. As a consequence, the test pass rate dropped from 100% to 86.36% in release 4.22. With this release, the race condition is resolved. As a result, the kubectl describe conformance test runs reliably and consistently passes. ([OCPBUGS-81740](https://redhat.atlassian.net/browse/OCPBUGS-81740))

- Before this update, the `oc adm upgrade recommend` test with an empty channel failed intermittently due to test re-ordering issues in the serial test suite. As a consequence, the test pass rate dropped from 100% to 97.48% in release 4.22. With this release, the test execution order is corrected. As a result, the `oc adm upgrade recommend` test with empty channel runs successfully and consistently. ([OCPBUGS-82304](https://redhat.atlassian.net/browse/OCPBUGS-82304))

- Before this update, some container-related `oc` commands failed intermittently after cluster upgrades. As a consequence, the workloads test checking container-related `oc` commands after upgrade experienced a pass rate drop from 100% to 50% in release 4.22. With this release, the underlying issues affecting container command execution post-upgrade are fixed. As a result, all container-related `oc` commands work reliably after cluster upgrades. ([OCPBUGS-84677](https://redhat.atlassian.net/browse/OCPBUGS-84677))

- Before this update, when using the `KUBECONFIG` environment variable with multiple configuration files, `oc login` incorrectly added all clusters and users from the secondary files to the main configuration file. As a consequence, entries in the main config file shadowed and overrode entries from other configuration files, causing unexpected context switching and authentication issues. With this release, `oc login` correctly writes authentication data only to the appropriate configuration file without merging all entries into the main config. As a result, users can maintain separate kubeconfig files using the `KUBECONFIG` environment variable without unintended modifications to their main configuration. ([OCPBUGS-85019](https://redhat.atlassian.net/browse/OCPBUGS-85019))

- Before this update, the `oc debug` command when used with image streams occasionally failed in the conformance test suite. As a consequence, the test exhibited flaky behavior that could cause CI pipeline failures. With this release, the underlying reliability issues with `oc debug` when using image streams are fixed. As a result, `oc debug` works consistently with image streams across all test runs. ([OCPBUGS-85531](https://redhat.atlassian.net/browse/OCPBUGS-85531))

- Before this update, the `oc` Windows RPM build failed during compilation with the error "unknown relocation type 7" because the `goversioninfo` tool generated 32-bit COFF objects without the `-64` flag. As a consequence, linking the Windows version information into the 64-bit binary caused relocation type incompatibilities and build failures. With this release, the `generate-versioninfo.sh` script passes the `-64` flag to `goversioninfo` to produce 64-bit compatible `.syso` files. As a result, the `oc` Windows binary builds successfully for 64-bit Windows platforms. ([OCPBUGS-87198](https://redhat.atlassian.net/browse/OCPBUGS-87198))

- Before this update, the `openshift-clients` RPM package had a hard dependency on `bash-completion`. As a consequence, users installing the package in minimal environments or systems without bash-completion faced installation failures or unnecessary package installations. With this release, the dependency on `bash-completion` is made optional. As a result, the `openshift-clients` RPM can be installed in minimal environments without requiring bash-completion. ([OCPBUGS-88342](https://redhat.atlassian.net/browse/OCPBUGS-88342))

- Before this update, the `oc adm storage-admin` conformance test used a brittle `HaveSuffix("no")` assertion that expected `oc auth can-i` output to end exactly with "no". As a consequence, when `oc auth can-i` began appending RBAC diagnostic information about missing ClusterRole references in version 5.0, the test failed because the output ended with "not found" instead of "no", causing the pass rate to drop from 100% to 76.9% on certain job configurations. With this release, the test assertion is updated to handle trailing RBAC diagnostic messages. As a result, the `oc adm storage-admin` test passes reliably even when RBAC diagnostics are included in the `oc auth can-i` output. ([OCPBUGS-99047](https://redhat.atlassian.net/browse/OCPBUGS-99047))

- Before this update, when using `oc login --exec-plugin oc-oidc` with Microsoft Entra ID (Azure AD), the OIDC token refresh failed after token expiration with the error "AADSTS900144: The request body must contain the following parameter: 'client_id'". As a consequence, users had to manually re-authenticate every time their ID token expired, typically after one hour. With this release, the `oc-oidc` exec credential plugin explicitly sets `AuthStyle: oauth2.AuthStyleInParams` to ensure `client_id` is always sent in the POST body when refreshing tokens. As a result, expired OIDC tokens are refreshed transparently against Microsoft Entra ID and other OIDC providers without requiring manual re-authentication. ([OCPBUGS-100310](https://redhat.atlassian.net/browse/OCPBUGS-100310))

- Before this update, the `OCP-42982 quota e2e` test called `oc new-project p42982-1` without the `--skip-config-write` flag, which caused the command to rewrite the shared `KUBECONFIG` file to set the current context to `p42982-1`. As a consequence, other test processes running concurrently with the same injected `KUBECONFIG` could load the kubeconfig mid-update and fail with "invalid configuration: context was not found for specified context: p42982-1" or "cluster has no server defined", resulting in intermittent CI failures. With this release, the test passes `--skip-config-write` to `oc new-project p42982-1` to prevent kubeconfig modification. As a result, concurrent e2e tests no longer experience kubeconfig corruption and context failures. ([OCPBUGS-101781](https://redhat.atlassian.net/browse/OCPBUGS-101781))

- Before this update, `oc rsh` occasionally failed on GCP platform with TechPreview feature set due to a WebSocket teardown race condition in the `kubelet exec` proxy. As a consequence, when the remote command completed under control plane CPU pressure, the kubelet could send a TCP RST instead of a graceful FIN during connection teardown, causing the client to receive "websocket: close 1006 (abnormal closure): unexpected EOF" errors, which dropped the test pass rate from 100% to 96.48% on GCP with TechPreview. With this release, the WebSocket exec protocol teardown handling is improved to prevent premature socket closure. As a result, `oc rsh` completes successfully and reliably on all platforms, including GCP with TechPreview feature set enabled. ([OCPBUGS-106190](https://redhat.atlassian.net/browse/OCPBUGS-106190))

## oc-mirror

## OLM

- Before this update, startup delays caused some health probes for Operator Lifecycle Manager (OLM) Classic catalog source pods to time out. As a consequence, this delay triggered pod restarts. With this release, Kubernetes gRPC probes avoid starting a process inside the container, which prevents these timeouts. ([OCPBUGS-74905](https://redhat.atlassian.net/browse/OCPBUGS-74905))

- Before this update, Operator Lifecycle Manager (OLM) v1 installations of Operators with webhooks sometimes stalled while waiting for serving certificates. With this release, certificate creation starts earlier, which reduces these installation delays. ([OCPBUGS-81452](https://redhat.atlassian.net/browse/OCPBUGS-81452))

- Before this update, the catalog endpoint provided by Operator Lifecycle Manager (OLM) v1 ignored TLS profile settings. With this release, the endpoint honors the configured minimum TLS version and cipher suites. ([OCPBUGS-86797](https://redhat.atlassian.net/browse/OCPBUGS-86797))

- Before this update, the metrics server in Operator Lifecycle Manager (OLM) v1 used default TLS settings instead of the TLS profile for the cluster. With this release, the metrics server follows the TLS profile and applies profile changes. ([OCPBUGS-88736](https://redhat.atlassian.net/browse/OCPBUGS-88736))

- Before this update, the package server in Operator Lifecycle Manager (OLM) Classic ignored the TLS profile for the cluster. With this release, the package server honors the configured minimum TLS version and cipher suites. ([OCPBUGS-88737](https://redhat.atlassian.net/browse/OCPBUGS-88737))

- Before this update, the Operator Lifecycle Manager (OLM) Classic package server on hosted control planes ignored the TLS profile for the hosted cluster. With this release, the package server follows the TLS settings for the hosted cluster. ([OCPBUGS-98575](https://redhat.atlassian.net/browse/OCPBUGS-98575))

## {ocp} API Server

- Before this update, the `openshift-apiserver` might have failed when many requests accessed project authorization data at the same time. This issue occurred more often on clusters with many namespaces and role-based access control (RBAC) rules. As a consequence, `openshift-apiserver` pods restarted unexpectedly with exit code `2`, which temporarily disrupted the API availability for project and namespace operations. With this release, the project authorization cache safely handles concurrent access. As a result, the `openshift-apiserver` namespace does not fail during concurrent project authorization lookups, and project listing operations remain responsive regardless of cluster size. ([OCPBUGS-84534](https://redhat.atlassian.net/browse/OCPBUGS-84534))

- Before this update, the NetworkPolicy for the `openshift-apiserver` namespace only allowed ingress on port 8443 and did not include the metrics port used by the `check-endpoints` container. As a consequence, Prometheus could not scrape metrics from the `check-endpoints` container, causing `TargetDown` alerts to fire continuously. With this update, the NetworkPolicy allows ingress on the metrics port. As a result, Prometheus scrapes succeed and the `TargetDown` alerts no longer fire. ([OCPBUGS-86583](https://redhat.atlassian.net/browse/OCPBUGS-86583))

## Pod Autoscaler

- Before this update, by default, the Vertical Pod Autoscaler (VPA) Operator required a control plane node for running workloads. As a consequence, it caused issues in single-node deployments. With this release, the Operator is updated to support deployment without control plane node requirements. As a result, the VPA Operator functions correctly in single-node configurations. ([OCPBUGS-42343](https://redhat.atlassian.net/browse/OCPBUGS-42343))

## Storage

- Before this update, when using zonal deployments of vSphere with OpenShift Container Platform, if a data center was missing from the vCenter section of the infrastructure configuration, the cluster became degraded without any warnings or errors logged by the vSphere platform detector. As a consequence, the CSI driver was unable to find virtual machines in the zone that was missed in the vCenter section. With this release, the vSphere platform detector validates that all data centers used in failure domains are also specified in the vCenter section. As a result, configuration errors are detected and reported, preventing cluster degradation. ([OCPBUGS-56274](https://redhat.atlassian.net/browse/OCPBUGS-56274))

- Before this update, when an UltraSSD_LRS Azure Disk volume snapshot was deleted in OpenShift Container Platform before the snapshot completed in Azure, and the delete operation failed in Azure, the `VolumeSnapshotContent` resource became stuck in a `Deleting` or `Terminating` state. As a consequence, the resource remained indefinitely in this state until the `openshift-cluster-csi-drivers/azure-disk-csi-driver-controller` pods were manually restarted. With this release, the Azure Disk CSI driver correctly reconciles with the Azure backend when deleting snapshots. As a result, terminating `VolumeSnapshotContent` objects are removed without requiring a restart of the CSI driver controller pods. ([OCPBUGS-77492](https://redhat.atlassian.net/browse/OCPBUGS-77492))

- Before this update, a regression in the Azure Disk CSI driver caused the `ManagedBy` field on Azure disks to remain set after a node was deleted, preventing disk detachment. As a consequence, when a disk was assigned to another node while waiting for `ControllerUnpublish` to finish, the operation became stuck indefinitely, and the disk could not be detached for several hours. With this release, the Azure Disk CSI driver correctly clears the `ManagedBy` field during the unpublish operation. As a result, disks detach properly when nodes are deleted or volumes are moved between nodes. ([OCPBUGS-78197](https://redhat.atlassian.net/browse/OCPBUGS-78197))

- Before this update, when the CSI driver `CreateVolumeGroupSnapshot` operation was called repeatedly, the host-path CSI driver did not return complete responses consistently. As a consequence, volume group snapshot creation operations could fail intermittently, particularly in test scenarios. With this release, the host-path CSI driver correctly returns complete responses for all `CreateVolumeGroupSnapshot` calls. As a result, volume group snapshot operations complete reliably. ([OCPBUGS-78576](https://redhat.atlassian.net/browse/OCPBUGS-78576))

- Before this update, the vSphere Problem Detector Operator incorrectly reported missing privileges for compute clusters on newly deployed OpenShift Container Platform clusters, even when vCenter permissions were configured identically to older clusters. As a consequence, warning events were logged indicating missing privileges such as `Resource.AssignVMToPool`, `VApp.AssignResourcePool`, `VApp.Import`, and `VirtualMachine.Config.AddNewDisk`, despite the service account having the required permissions. With this release, the vSphere Problem Detector Operator correctly validates vCenter permissions across all cluster deployments. As a result, false positive warnings are no longer generated on newly deployed clusters. ([OCPBUGS-79057](https://redhat.atlassian.net/browse/OCPBUGS-79057))

- With this release, end-to-end test automation has been added to validate that storage components no longer generate self-signed certificates. As a result, the feature is properly tested in automated test suites. ([OCPBUGS-84247](https://redhat.atlassian.net/browse/OCPBUGS-84247))

- Before this update, CSI driver configuration tests did not skip execution when the `ClusterCSIDriver` resource state was set to `Removed`. As a consequence, tests that attempted to configure CSI drivers timed out waiting for the storage Operator to become progressing, resulting in test failures with messages such as "Failed to wait for Operator Progressing=True". With this release, CSI driver configuration tests correctly detect when a `ClusterCSIDriver` is in the `Removed` state and skip execution. As a result, tests no longer fail when CSI drivers are intentionally removed. ([OCPBUGS-84809](https://redhat.atlassian.net/browse/OCPBUGS-84809))

- Before this update, the SELinux warning controller of the Kubernetes Controller Manager performed `O(V * P^2)` operations during every Prometheus metrics scrape, where V is the number of volumes and P is the number of pods per volume. As a consequence, on large clusters with hundreds of nodes and attached volumes, the KCM leader `/metrics` endpoint took over 12 seconds to respond, exceeding the 5-second Prometheus scrape timeout and causing `KubeControllerManagerDown` alerts to fire. With this release, the SELinux warning controller is optimized to reduce computational overhead during metrics collection. As a result, metrics scraping completes within the timeout period, and cluster monitoring operates correctly on large production clusters. ([OCPBUGS-85410](https://redhat.atlassian.net/browse/OCPBUGS-85410))

- Before this update, the Manila CSI driver node plugin crashed immediately on startup if the NFS CSI plugin socket was not available, with no retry logic for connection errors. As a consequence, after node disruptions, the Manila CSI driver accumulated excessive container restarts, causing CI invariant test failures. With this release, the Manila CSI driver retries connection attempts when the NFS plugin socket is temporarily unavailable, and the Operator deployment includes an init container to ensure proper startup ordering. As a result, the driver starts reliably after node reboots without excessive restarts. ([OCPBUGS-85457](https://redhat.atlassian.net/browse/OCPBUGS-85457))

- Before this update, the `smb-csi-driver-controller` pod had a total memory request of 230 MiB across its seven containers, but a hardcoded memory limit of only 200 MiB on the `csi-driver` container. As a consequence, the pod was deployed in an over-committed state where minimum requirements exceeded maximum allowed usage, triggering constant `KubePodMemoryUsageLimitHigh` alerts. With this release, the pod-level memory limit has been increased to accommodate all sidecar containers introduced in OpenShift Container Platform 4.20. As a result, monitoring alerts no longer fire for this pod. ([OCPBUGS-86023](https://redhat.atlassian.net/browse/OCPBUGS-86023))

- Before this update, when the `ClusterCSIDriver` management state of the AWS EBS CSI driver was set to `Unmanaged`, the static resources controller continued to reconcile and revert user-modified fields in the `CSIDriver` resource. As a consequence, manual changes to fields such as `nodeAllocatableUpdatePeriodSeconds` were immediately overwritten by the Operator. With this release, the static resources controller skips reconciliation when the management state is `Unmanaged`. As a result, administrators can modify CSI driver configuration without Operator interference when the driver is in unmanaged mode. ([OCPBUGS-86504](https://redhat.atlassian.net/browse/OCPBUGS-86504))

- Before this update, when failure domains were removed from the vSphere infrastructure specification, the vSphere Problem Detector logged warning messages indicating "failure domain labels missing from node" even though the nodes and failure domains were correctly configured. As a consequence, misleading warnings appeared in the logs during valid failure domain reconfiguration. With this release, the vSphere Problem Detector correctly handles failure domain removal without generating false warnings. As a result, no spurious warnings are logged when administrators remove failure domains from the platform specification. ([OCPBUGS-87906](https://redhat.atlassian.net/browse/OCPBUGS-87906))

- Before this update, all containers in the `gcp-pd-csi-driver-controller` deployment ran as the root user (UID 0). As a consequence, the deployment did not follow security best practices for running containers as non-root users. With this release, security constraints have been applied to run all CSI driver controller containers as non-root users with additional hardening including read-only root filesystems and dropped capabilities. As a result, the GCP Persistent Disk CSI driver controller adheres to OpenShift Container Platform security standards. ([OCPBUGS-88299](https://redhat.atlassian.net/browse/OCPBUGS-88299))

- Before this update, the CSI snapshot controller fired `SnapshotContentObjectDeleteError` warning events when it attempted to delete a `VolumeSnapshotContent` resource that had already been removed. As a consequence, misleading error events appeared during concurrent snapshot deletions or bulk deletion scenarios, even though the final deletion was successful. With this release, the snapshot controller suppresses error events when the resource is already deleted (NotFound error). As a result, no false-positive warnings are generated during normal snapshot cleanup operations. ([OCPBUGS-99009](https://redhat.atlassian.net/browse/OCPBUGS-99009))

- Before this update, the `ClusterServiceVersion (CSV)` component of the AWS EFS CSI driver Operator was missing required RBAC permissions for `networking.k8s.io/networkpolicies`. As a consequence, the Operator bundle failed the Konflux policy check `olm.required_network_policy_rbac_for_operands`, blocking Operator releases. With this release, the required RBAC permissions are added to the CSV. As a result, the Operator bundle passes policy validation and can be shipped in releases. ([OCPBUGS-99199](https://redhat.atlassian.net/browse/OCPBUGS-99199))

- Before this update, the `ClusterServiceVersion (CSV)` component of the SMB CSI driver Operator was missing required RBAC permissions for `networking.k8s.io/networkpolicies`. As a consequence, the Operator bundle failed the Konflux policy check `olm.required_network_policy_rbac_for_operands`, blocking Operator releases. With this release, the required RBAC permissions are added to the CSV. As a result, the Operator bundle passes policy validation and can be shipped in releases. ([OCPBUGS-99200](https://redhat.atlassian.net/browse/OCPBUGS-99200))

- Before this update, the `ClusterServiceVersion (CSV)` component of the GCP Filestore CSI driver Operator was missing required RBAC permissions for `networking.k8s.io/networkpolicies`. As a consequence, the Operator bundle failed the Konflux policy check `olm.required_network_policy_rbac_for_operands`, blocking Operator releases. With this release, the required RBAC permissions are added to the CSV. As a result, the Operator bundle passes policy validation and can be shipped in releases. ([OCPBUGS-99201](https://redhat.atlassian.net/browse/OCPBUGS-99201))

- Before this update, after RBAC restructuring in the CSI Operator, the GCP Persistent Disk CSI driver controller deployment failed Security Context Constraints (SCC) validation during cluster installation. As a consequence, pod creation failures occurred during install, causing the `[sig-auth][Feature:SCC][Early] should not have pod creation failures during install` conformance test to fail. With this release, the CSI Operator correctly configures RBAC and security contexts for the GCP PD CSI driver controller. As a result, pod creation succeeds during installation without SCC validation errors. ([OCPBUGS-99490](https://redhat.atlassian.net/browse/OCPBUGS-99490))

- Before this update, the `NetworkPolicy` resources `openshift-cluster-csi-drivers/allow-to-dns` and `openshift-cluster-storage-operator/allow-to-dns` used named ports (such as "https") instead of numeric port numbers. As a consequence, on CNIs such as OVN-Kubernetes that do not support named ports in `NetworkPolicies`, the rules were silently converted into allow-all rules, effectively bypassing the intended network restrictions. With this release, these NetworkPolicies use numeric port references (such as "443"). As a result, network policies function correctly on all supported CNI providers. ([OCPBUGS-99492](https://redhat.atlassian.net/browse/OCPBUGS-99492))

- Before this update, on Azure Red Hat OpenShift (ARO) clusters where the legacy `kube-system/azure-cloud-provider` secret existed, the Azure Disk CSI driver controller attempted to read this secret during startup despite being configured to use the credential file. As a consequence, the driver started with a nil Azure cloud provider and crashed with a panic on the first volume attach or detach operation, breaking all PVC operations cluster-wide. With this release, when cloud configuration secret arguments are empty, the driver correctly falls back to the `AZURE_CREDENTIAL_FILE` without attempting to read the legacy secret. As a result, volume attach and detach operations function correctly on ARO clusters. ([OCPBUGS-101779](https://redhat.atlassian.net/browse/OCPBUGS-101779))

- Before this update, in hosted control planes deployments where the management cluster required a proxy for external access, the CSI driver controller deployments did not receive `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables. As a consequence, CSI driver controller containers could not reach cloud provider APIs through the proxy, causing all volume provisioning operations to fail. With this release, the CSI Operator injects proxy environment variables into hosted control planes CSI driver controller deployments. As a result, volume provisioning operations complete successfully in proxy-enabled hosted control planes environments. ([OCPBUGS-111893](https://redhat.atlassian.net/browse/OCPBUGS-111893))

## Two node with Arbiter

- Before this update, the Machine Config Operator (MCO) sync logic operated independently per machine-config pool, which allowed the arbiter and control-plane machine-config pools to restart nodes simultaneously. As a consequence, it caused temporary quorum loss during MCO reboot and upgrade events in two-node clusters with arbiter configurations. With this release, MCO now handles arbiter nodes as a special case and prevents the arbiter and control-plane machine-config pools from restarting nodes at the same time. As a result, quorum is maintained during MCO reboot and upgrade events, avoiding temporary etcd quorum loss. ([OCPBUGS-64681](https://redhat.atlassian.net/browse/OCPBUGS-64681))

## Virtualization

- Before this update, the Hosted Cluster Config Operator (HCCO) machine controller included link-local addresses such as `169.254.0.2` and `fe80::*` in `EndpointSlice` endpoints. Kubernetes 1.33 rejects link-local addresses in `EndpointSlice` endpoints. As a consequence, the HCCO to fail when creating endpoints for `kubevirt` guest cluster `LoadBalancer` shadow services. `LoadBalancer` services in `kubevirt`-based hosted clusters failed with "Connection refused" errors. With this release, the HCCO filters out link-local addresses before creating `EndpointSlice` endpoints. `LoadBalancer` services in `kubevirt`-based hosted clusters are now accessible from the management cluster. ([OCPBUGS-83604](https://redhat.atlassian.net/browse/OCPBUGS-83604))

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

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| MCP server for Red Hat OpenShift Container Platform | Not Available | Technology Preview | General Availability <sup>\[1\]</sup> |

AI applications Technology Preview tracker

1.  The following toolsets are still Technology Preview status:

    - kubevirt

    - openshift/mustgather

    - cluster-diagnostics

    - cni-diagnostics

    - ovn-kubernetes

## Authentication and authorization Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Advanced direct authentication fields | Technology Preview | Technology Preview | General Availability |
| External claims sourcing for external OIDC authentication | Not Available | Not Available | Technology Preview |
| Component-scoped proxy for authentication | Not Available | Not Available | Technology Preview |
| Pod security admission restricted enforcement | Technology Preview | Technology Preview | Technology Preview |

Authentication and authorization Technology Preview tracker

## Edge computing Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Accelerated provisioning of GitOps ZTP | Technology Preview | Technology Preview | Technology Preview |
| Enabling disk encryption with TPM and PCR protection | Technology Preview | Technology Preview | Technology Preview |
| Configuring a local arbiter node | General Availability | General Availability | General Availability |
| Configuring a two-node OpenShift Container Platform cluster with fencing | Technology Preview | General Availability | General Availability |
| O-Cloud Manager | Not Available | Not Available | Technology Preview |

Edge computing Technology Preview tracker

## Extensions Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| OLM v1 runtime validation of container images using sigstore signatures | Technology Preview | General Availability | General Availability |
| OLM v1 permissions preflight check for cluster extensions | Technology Preview | Technology Preview | Removed |
| OLM v1 cluster extension installation and update deadlines | Not Available | Technology Preview | Technology Preview |
| OLM v1 deploying a cluster extension in a specified namespace | Technology Preview | Technology Preview | Technology Preview |
| OLM v1 deploying a cluster extension that uses webhooks | General Availability | General Availability | General Availability |
| OLM v1 software catalog | Technology Preview | Technology Preview | Technology Preview |
| OLM v1 `deploymentConfig` API for cluster extension customization | Not Available | Technology Preview | Technology Preview |

Extensions Technology Preview tracker

## Installation Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Installing a cluster on Alibaba Cloud by using Assisted Installer | Technology Preview | Technology Preview | Technology Preview |
| Installing a cluster using Red Hat Enterprise Linux (RHEL) 10 | Not Available | Technology Preview | General Availability |
| Dedicated disk for etcd on Microsoft Azure | Technology Preview | Technology Preview | Technology Preview |
| Mount shared entitlements in BuildConfigs in RHEL | Technology Preview | General Availability (through Builds for OpenShift Operator) | General Availability (through Builds for OpenShift Operator) |
| OpenShift zones support for vSphere host groups | Technology Preview | General Availability | General Availability |
| Selectable Cluster Inventory |  |  |  |
| Enabling a user-provisioned DNS on Google Cloud | General Availability | General Availability | General Availability |
| Enabling a user-provisioned DNS on Microsoft Azure | Technology Preview | General Availability | General Availability |
| Enabling a user-provisioned DNS on Amazon Web Services (AWS) | Technology Preview | Technology Preview | General Availability |
| Installing a cluster using Google Cloud private and restricted API endpoints | General Availability | General Availability | General Availability |
| Installing a cluster on VMware vSphere with multiple network interface controllers | General Availability | General Availability | General Availability |
| Red Hat Bare-Metal-as-a-Service for OpenShift (formerly known as bare metal as a service) | Technology Preview | General Availability | General Availability |
| Installing a cluster on Amazon Web Services (AWS) European Sovereign Cloud | Not Available | Technology Preview | Technology Preview |
| Installing a cluster on Amazon Web Services (AWS) with dual-stack networking | Not Available | Technology Preview | General Availability |
| Running firmware upgrades for hosts in deployed bare metal clusters | General Availability | General Availability | General Availability |
| Changing the CVO log level | Technology Preview | Technology Preview | Technology Preview |
| Deploying virtualized control planes with KubeVirt Redfish | Not Available | Technology Preview | General Availability |

Installation Technology Preview tracker

> [!NOTE]
> Fleet Management supersedes Selectable Cluster Inventory in OpenShift Container Platform 4.20 and later releases. For more information see, the Red Hat Advanced Cluster Management for Kubernetes documentation for [Fleet Management](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.15/html-single/release_notes/index#console-new-features).

## Machine Config Operator Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Boot image management for control plane nodes | Technology Preview | General Availability | General Availability |
| Image mode for OpenShift status reporting improvements | Technology Preview | Technology Preview | Technology Preview |
| Overriding storage or partition setup | Technology Preview | Technology Preview | General Availability |

Machine Config Operator Technology Preview tracker

## Machine management Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Managing machines with the Cluster API for Amazon Web Services | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for Google Cloud | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for IBM Power® Virtual Server | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for Microsoft Azure | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for RHOSP | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for VMware vSphere | Technology Preview | Technology Preview | Technology Preview |
| Managing machines with the Cluster API for bare metal | Technology Preview | Technology Preview | Technology Preview |
| Cloud controller manager for IBM Power® Virtual Server | Technology Preview | Technology Preview | Technology Preview |
| Adding multiple subnets to an existing VMware vSphere cluster by using compute machine sets | Technology Preview | Technology Preview | Technology Preview |
| Bare-metal nodes on VMware vSphere clusters | Technology Preview | Technology Preview | Technology Preview |
| Amazon Web Services Dedicated Host support | Not Available | Technology Preview | Technology Preview |

Machine management Technology Preview tracker

## Multi-Architecture Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| `kdump` on `arm64` architecture | General Availability | General Availability | General Availability |
| `kdump` on `s390x` architecture | General Availability | General Availability | General Availability |
| `kdump` on `ppc64le` architecture | General Availability | General Availability | General Availability |
| Support for configuring the image stream import mode behavior | Technology Preview | Technology Preview | Technology Preview |

Multi-Architecture Technology Preview tracker

## Networking Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| eBPF manager Operator | Technology Preview | Technology Preview | Technology Preview |
| Advertise using L2 mode the MetalLB service from a subset of nodes, using a specific pool of IP addresses | Technology Preview | Technology Preview | Technology Preview |
| Updating the interface-specific safe sysctls list | Technology Preview | Technology Preview | Technology Preview |
| Egress service custom resource | Technology Preview | Technology Preview | Technology Preview |
| VRF specification in `BGPPeer` custom resource | Technology Preview | Technology Preview | Technology Preview |
| OVN-Kubernetes customized `br-ex` bridge on vSphere and RHOSP | Technology Preview | Technology Preview | Technology Preview |
| OVN-Kubernetes and CNI diagnostics toolsets for the MCP server | Not Available | Not Available | General Availability |
| Dynamic Configuration Manager (DCM) | Technology Preview | General Availability | General Availability |
| SR-IOV Network Operator support for Intel C741 Emmitsburg Chipset | Technology Preview | General Availability | General Availability |
| SR-IOV Network Operator support for s390x | Not Available | Not Available | General Availability |
| Dual-port NIC for PTP ordinary clock | General Availability | General Availability | General Availability |
| DPU Operator | Technology Preview | Technology Preview | Technology Preview |
| Fast IPAM for the Whereabouts IPAM CNI plugin | Technology Preview | Technology Preview | Technology Preview |
| Unnumbered BGP peering | General Availability | General Availability | General Availability |
| Load balancing across the aggregated bonded interface with xmitHashPolicy | Technology Preview | Technology Preview | General Availability |
| PF Status Relay Operator for high availability with SR-IOV networks | Technology Preview | Technology Preview | Technology Preview |
| Preconfigured user-defined network end points using MTV | Technology Preview | Technology Preview | Technology Preview |
| Unassisted holdover for PTP devices | General Availability | General Availability | General Availability |
| No-overlay mode with BGP routing | Not Available | Technology Preview | Technology Preview |
| Configuring GNR-D T-BC holdover on a GNR-D platform | Not Available | Technology Preview | Technology Preview |
| PTP Telecom Boundary Clock (T-BC) high availability with dual time receiver ports on Intel Granite Rapids-D (GNR-D) | Not Available | Not Available | Technology Preview |
| PTP Telecom Grandmaster (T-GM) on Intel Granite Rapids-D (GNR-D) | Not Available | Technology Preview | Technology Preview |
| Telecom Grandmaster on Intel Granite Rapids-D with field-tunable timing parameters | Not Available | Not Available | Technology Preview |
| Network Observability Operator automatic installation | Not Available | Not Available | Technology Preview |

Networking Technology Preview tracker

## Node Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Additional CRI-O storage locations | Not Available | Technology Preview | General Availability |
| `MaxUnavailableStatefulSet` featureset | Technology Preview | Technology Preview | Technology Preview |
| Project-scoped image pull secrets for mirrored registries | Not Available | Technology Preview | General Availability |
| Partitionable device DRA support | Not Available | Technology Preview | General Availability |

Nodes Technology Preview tracker

## Postinstallation configuration Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Expanding a bare metal cluster using images from OCI registries | Not Available | Technology Preview | Technology Preview |

Postinstallation configuration Technology Preview tracker

## Red Hat Enterprise Linux CoreOS (RHCOS) Technology Preview features

| Feature    | 4.21          | 4.22               | 5.0                  |
|------------|---------------|--------------------|----------------------|
| RHCOS 10.2 | Not Available | Technology Preview | General Availability |

Red Hat Enterprise Linux CoreOS (RHCOS) 10.2 Technology Preview tracker

## Red Hat OpenStack Platform (RHOSP) Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| RHOSP integration into the Cluster CAPI Operator | Technology Preview | Technology Preview | Technology Preview |
| Hosted control planes on RHOSP 17.1 | Technology Preview | Technology Preview | Technology Preview |

RHOSP Technology Preview tracker

## Scalability and performance Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| factory-precaching-cli tool | Technology Preview | Technology Preview | Technology Preview |
| Hyperthreading-aware CPU manager policy | Technology Preview | Technology Preview | Technology Preview |
| LLC-aware CPU pinning | Technology Preview | Technology Preview | General Availability |
| Mount namespace encapsulation | Technology Preview | Technology Preview | Technology Preview |
| Node Observability Operator | Technology Preview | Technology Preview | Removed |
| Increasing the etcd database size | Technology Preview | Technology Preview | General Availability |
| Kubernetes KMS v2 encryption for etcd | Not Available | Technology Preview | Technology Preview |
| Managing etcd size by setting the `eventTTLMinutes` property | Technology Preview | General Availability | General Availability |
| Pinned Image Sets | Technology Preview | Technology Preview | Technology Preview |
| Configuring NUMA-aware scheduler replicas and high availability | General Availability | General Availability | General Availability |
| OVS-DPDK CPU reservation | Not Available | Not Available | Technology Preview |

Scalability and performance Technology Preview tracker

## Security Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Configurable PKI for platform certificates | Not Available | Not Available | Technology Preview |

Security Technology Preview tracker

## Storage Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Changed block tracking | Developer Preview | Developer Preview | Technology Preview |
| Azure File CSI cloning support | General Availability | General Availability | General Availability |
| Azure File CSI snapshot support | General Availability | General Availability | General Availability |
| European Sovereign Cloud (EUSC) region | Not Available | Technology Preview | Technology Preview |
| Hyperdisk Balanced HA volumes | Not Available | General Availability | General Availability |
| LSO symlinks management | Not Available | General Availability | General Availability |
| Increasing max number of volumes per node for vSphere | Technology Preview | Technology Preview | Technology Preview |
| RWX/RWO SELinux mount option | Technology Preview | Technology Preview | Technology Preview |
| CSI volume group snapshots | Technology Preview | Technology Preview | General Availability |
| CIFS/SMB CSI Driver Operator | General Availability | General Availability | General Availability |
| Volume Attribute Classes | General Availability | General Availability | General Availability |

Storage Technology Preview tracker

## Updates Technology Preview features

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Creating an AI-generated cluster update assessment | Not Available | Not Available | Technology Preview |

Updates Technology Preview tracker

# Known issues

Known issues in OpenShift Container Platform 4.17 can affect nodes, pods, and network devices. Review each issue for its impact and workaround.

- When you run Cloud-native Network Functions (CNF) latency tests on an OpenShift Container Platform cluster, the test might return results that exceed the latency threshold, such as 20 microseconds for cyclictest testing. This can result in intermittent test failures even when the cluster is correctly configured for low-latency workloads. As a workaround, revert the `stalld` backend to `sched_debug` to reduce the frequency and magnitude of latency spikes. ([OCPBUGS-86339](https://redhat.atlassian.net/browse/OCPBUGS-86339))

- Deleting and recreating test workloads with a BlueField-3 NIC causes clock jumps due to inconsistent PTP synchronization. This disrupts time synchronization in test workloads. The time synchronization stabilizes when the workloads are stable. ([RHEL-93579](https://redhat.atlassian.net/browse/RHEL-93579))

- When you use the Red Hat Enterprise Linux (RHEL) 10 stream, which is the default for new installations of 5.0 but not for upgrades from 4.22, throughput of messages less than 4KB in size is approximately 30-50% lower than RHEL 9. The regression is most pronounced at small message sizes, for example, 64 bytes and 1 KB, and diminishes at message sizes of 4 KB or larger. ([OCPBUGS-128611](https://redhat.atlassian.net/browse/OCPBUGS-128611))

- Worker nodes lock up after you apply a performance profile with strict CPU reservation and `isolated` or `reserved` CPUs.

  When you apply a performance profile that configures strict CPU reservation along with `isolated` and `reserved` CPUs, the worker node locks up and enters a `NotReady` state. This issue occurs because the CPU Manager state file does not match the available CPUs after the node reboots.

  To work around this problem, clear the CPU Manager state file and restart the kubelet service:

  1.  Start a debug session on the affected node:

      ``` terminal
      $ oc debug node/<node_name>
      ```

  2.  Change the root directory to `/host`:

      ``` terminal
      # chroot /host
      ```

  3.  Remove the CPU Manager state file:

      ``` terminal
      # rm /var/lib/kubelet/cpu_manager_state
      ```

  4.  Restart the kubelet service:

      ``` terminal
      # systemctl restart kubelet
      ```

      ([OCPBUGS-77659](https://redhat.atlassian.net/browse/OCPBUGS-77659))

- Currently, pods that use Single Root I/O Virtualization (SR-IOV) virtual functions (VFs) on Intel 710 network interface cards (NICs) might experience delays during deletion. A kernel regression that involves the `netdev` lock causes a deadlock during restoration of the original MAC address of a VF. As a consequence, deleting affected pods takes up to 90 seconds because of a Container Network Interface (CNI) timeout. ([OCPBUGS-97994](https://redhat.atlassian.net/browse/OCPBUGS-97994))

- Currently, pods that use the `guaranteed` Quality of Service (QoS) class and request whole CPUs might not restart automatically after a node reboot or kubelet restart. This issue can occur on nodes with a static CPU Manager policy and the `full-pcpus-only` specification. It occurs when most or all CPUs on the node are already allocated by such workloads. As a consequence, the affected pods remain in a pending or failed state. To work around this problem, manually delete and re-create the affected pods. ([OCPBUGS-43280](https://redhat.atlassian.net/browse/OCPBUGS-43280))

- The NUMA Resources Operator deploys a secondary scheduler for non-uniform memory access (NUMA) aware scheduling. When you enable preemption on this scheduler, a stale Node Resource Topology (NRT) cache can cause extra pod evictions.

  After a pod that requests exclusive resources terminates, the scheduler removes that pod from the list of running pods on the node. A topology updater runs asynchronously and can take a few seconds to record the termination. Until the updater refreshes the NRT cache, the scheduler still treats the resources of the terminated pod as reserved and uses this stale accounting for the next scheduling decision.

  The NUMA-aware scheduler uses this stale accounting when it cannot place a pod and then checks whether evicting lower-priority pods would free enough resources. If lower-priority pods are running, the scheduler can evict them even though the terminated pod has already released its resources. These evictions can continue until the topology updater refreshes the NRT cache with the released resources.

  To work around this problem, use a controller, such as a `Deployment`, `ReplicaSet`, or `DaemonSet`, for pods that run on the cluster. The controller re-creates an evicted pod. The scheduler might not place the re-created pod because placement depends on the position of the pod in the scheduling queue.

  ([OCPBUGS-123679](https://redhat.atlassian.net/browse/OCPBUGS-123679))

- A pod that the Node Resource Topology (NRT) plugin rejects because of stale NRT information can remain in a pending state after the scheduler refreshes the NRT cache.

  While a pod is in the unschedulable queue, the scheduler retries the pod only after a node event that changes resource availability or allocatable resources, or after the unschedulable timeout expires. The default timeout is 5 minutes. If the NRT plugin rejects the pod because of stale NRT information, refreshing the NRT cache does not generate one of those events. The pod stays in the unschedulable queue until one of those events occurs.

  To work around this problem, delete and re-create the pending pod after the scheduler refreshes the NRT cache. You can also schedule a pod on the target node that uses the `guaranteed` Quality of Service (QoS) class and requests a small amount of resources.

  ([OCPBUGS-123706](https://redhat.atlassian.net/browse/OCPBUGS-123706))

- While the NUMA-aware scheduler runs preemption attempts for a high-priority pod, an update to the Node Resource Topology (NRT) cache does not stop the scheduler from evicting lower-priority pods.

  During these attempts, the NRT cache can update and show enough free resources for the high-priority pod. No more resources need to be freed for that pod. The cache update does not stop the preemption flow or the scheduling cycle. As a consequence, the scheduler can still evict lower-priority pods. If the cache is updated before preemption starts and shows enough free resources, the scheduler does not make additional preemption attempts.

  To work around this problem, use a controller, such as a `Deployment`, `ReplicaSet`, or `DaemonSet`, for pods that run on the cluster. The controller re-creates an evicted pod. The scheduler might not place the re-created pod because placement depends on the position of the pod in the scheduling queue.

  ([OCPBUGS-123515](https://redhat.atlassian.net/browse/OCPBUGS-123515))

- Currently, you cannot use Single Root I/O Virtualization (SR-IOV) virtual functions (VFs) as ports in a bond device. The affected VFs are on Intel `i40e` (710 series) or `ice` (E810 series) network interface cards (NICs). A kernel regression causes the `set_mac_address` operation to fail when you add a second VF to the bond. The operation returns `Error -11 calling set_mac_address` (resource temporarily unavailable). As a consequence, the bond device does not become active, and you cannot add the affected VFs to the bond. To work around this problem, do not configure bond devices that use `i40e` or `ice` VFs as ports on affected nodes. ([RHEL-143410](https://redhat.atlassian.net/browse/RHEL-143410))

- Currently, the `ListenerSet` custom resource definition (CRD) is installed on the cluster, but the OpenShift Container Platform Gateway API implementation does not support `ListenerSet` resources. As a consequence, a `ListenerSet` that targets a OpenShift Container Platform-managed `Gateway` is not reconciled, and the listeners that it defines are not programmed onto the `Gateway` and do not route traffic. The `ListenerSet` reports an `Accepted=False` status condition with the `UnsupportedByController` reason, and the `ListenerSetOnManagedGateway` alert fires. As a workaround, define listeners directly on the `Gateway` resource instead of using a `ListenerSet`. ([OCPBUGS-100435](https://redhat.atlassian.net/browse/OCPBUGS-100435))

- Currently, Red Hat Enterprise Linux CoreOS (RHCOS) version 10 VMware vSphere installer-provisioned infrastructure nodes experience a `serial-getty@ttyS0` restart loop. This state occurs because there is no serial port present. The restart loop causes continuous `mount-table` churn that is visible on every node. In long-lived clusters, this might lead to `node-exporter` memory exhaustion, and control-plane degradation. ([OCPBUGS-133499](https://redhat.atlassian.net/browse/OCPBUGS-133499))

# Asynchronous errata updates

Security, bug fix, and enhancement updates for OpenShift Container Platform 4.17 are released as asynchronous errata through the Red Hat Network. All OpenShift Container Platform 4.17 errata is [available on the Red Hat Customer Portal](https://access.redhat.com/downloads/content/290/). See the [OpenShift Container Platform Life Cycle](https://access.redhat.com/support/policy/updates/openshift) for more information about asynchronous errata. Red Hat Customer Portal users can enable errata notifications in the account settings for Red Hat Subscription Management (RHSM). When errata notifications are enabled, users are notified through email whenever new errata relevant to their registered systems are released.

> [!NOTE]
> Red Hat Customer Portal user accounts must have systems registered and consuming OpenShift Container Platform entitlements for OpenShift Container Platform errata notification emails to generate.

This section will continue to be updated over time to provide notes on enhancements and bug fixes for future asynchronous errata releases of OpenShift Container Platform 4.17. Versioned asynchronous releases, for example with the form OpenShift Container Platform 4.17.z, will be detailed in subsections. In addition, releases in which the errata text cannot fit in the space provided by the advisory will be detailed in subsections that follow.

> [!IMPORTANT]
> For any OpenShift Container Platform release, always review the instructions on [updating your cluster](../updating/updating_a_cluster/updating-cluster-web-console.xml#updating-cluster-web-console) properly.
