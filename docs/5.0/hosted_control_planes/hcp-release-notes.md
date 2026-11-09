With this release, hosted control planes for OpenShift Container Platform 4.17 is available. Hosted control planes for OpenShift Container Platform 4.17 supports multicluster engine for Kubernetes Operator version 4.17.

# New features and enhancements

This release adds improvements related to self-managed hosted control planes for OpenShift Container Platform.

Comprehensive etcd encryption key rotation monitoring in hosted clusters
With this update, comprehensive status reporting and monitoring is implemented for etcd encryption key rotation in hosted clusters. Platform administrators can now programmatically determine the success of key rotation and have visibility into data re-encryption progress. This ensures that key rotation processes do not significantly impact cluster performance, maintaining cluster availability during the process. This enhancement meets Microsoft S360 security requirements and ensures reliable key rotation.

Core data re-encryption with new keys implemented in hosted clusters
With this update, the core data re-encryption functionality is implemented in hosted control planes to ensure all existing etcd data is re-encrypted with new keys during rotation operations. This feature guarantees a higher level of security for hosted control planes users as their etcd data is protected with the latest keys, reducing potential security and compliance issues, and maintaining cluster availability and performance.

Manage RHCOS version streams within a hosted cluster
In hosted control planes, Red Hat Enterprise Linux (RHEL) 9 and RHEL 10 compute nodes can run simultaneously within a single hosted cluster. By controlling the Red Hat Enterprise Linux CoreOS (RHCOS) major version for each NodePool object independently, you can incrementally migrate from RHEL 9 to RHEL 10 without replacing the entire cluster. For more information, see [Managing RHCOS version streams within a hosted cluster](../hosted_control_planes/hcp-dual-stream.xml#hcp-dual-stream).

# Notable technical changes

Review the following notable technical changes introduced in this release.

Hosted control planes on Microsoft Azure is a General Availability feature
As of OpenShift Container Platform 5.0, self-managed hosted control planes on Azure is supported as a General Availability feature. For more information, see [Deploying hosted control planes on Azure](../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-deploy-azure).

# Fixed issues

This section lists the fixed issues in this release of hosted control planes for OpenShift Container Platform.

- Before this update, the wrong restoration of `kubeadmin` password hashes caused new passwords not to work in a restored cluster. As a consequence, the restored cluster used the old `kubeadmin` password instead of the new one, resulting in login failure. With this release, the `kubeadmin` password hash mismatch in restored clusters has been addressed, and reconciliation logic has been updated. As a result, new `kubeadmin` passwords in restored clusters now match, allowing successful login. ([OCPBUGS-38898](https://redhat.atlassian.net/browse/OCPBUGS-38898))

- Before this update, the `control-plane-pki-operator` reported incorrect `certificate revoked` conditions without waiting for CA bundle reloads on Kubernetes API Server. As a consequence, intermittent invalid certificates were issued, causing temporary unauthorized access. This release ensures that the `control-plane-pki-operator` waits for the CA bundle reload, preventing intermittent certificate use. As a result, the `control-plane-pki-operator` correctly reports certificate revocation, ensuring immediate invalidation across all Kubernetes API Server instances. ([OCPBUGS-62177](https://redhat.atlassian.net/browse/OCPBUGS-62177))

- Before this update, AWS ISO domains were omitted from the `IsCloudAPI` list of the `Konnectivity` service. As a consequence, AWS ISO domain communication was proxied instead of direct, causing necessary endpoints to fail. With this release, AWS ISO domains have been added to the `IsCloudAPI` list for OpenShift Container Platform 4.21 and later versions. As a result, the `Konnectivity` service now adds AWS ISO domains to the `NO_PROXY` list of the Ingress Operator, enabling direct communication with endpoints in those namespaces. ([OCPBUGS-77040](https://redhat.atlassian.net/browse/OCPBUGS-77040))

- Before this update, the Hosted Cluster Config Operator would crash loop on an un-customized Kubernetes cluster because the Operator was unconditionally attempting to watch the OpenShift Container Platform Route resource. With this release, the Operator attempts to watch the resource only when it exists on the management cluster. As a result, the Operator is no longer crash looping on an un-customized Kubernetes cluster. ([OCPBUGS-87364](https://issues.redhat.com/browse/OCPBUGS-87364))

- Before this update, the `Konnectivity` component of hosted control planes failed to add specific AWS ISO regions to the `NO_PROXY` list. As a consequence, the proxy routed cluster communication with these AWS domains instead of sending it directly, causing connectivity issues. With this release, `Konnectivity` component automatically adds AWS ISO domains to the `NO_PROXY` list of the Ingress Operator. As a result, this update resolves AWS ISO domain connectivity issues, enabling direct communication for the required endpoints. ([OCPBUGS-85781](https://redhat.atlassian.net/browse/OCPBUGS-85781))

- Before this update, the `IsCloudAPI` method for the `Konnectivity` proxy did not include Amazon Web Services (AWS) ISO region domain suffixes, such as `.c2s.ic.gov`, `.hci.ic.gov`, or `.sc2s.sgov.gov` in its cloud API detection lists. As a consequence, the Ingress Operator could not add AWS ISO domains to the `NO_PROXY` list, blocking direct communication with endpoints. With this release, the AWS ISO suffixes are added to the `IsCloudAPI` detection list. As a result, the `Konnectivity` proxy correctly identifies the AWS ISO region endpoints as cloud APIs, so that the Ingress Operator can route traffic to those domains directly. ([OCPBUGS-85779](https://redhat.atlassian.net/browse/OCPBUGS-85779))

- Before this update, the wrong restoration of `kubeadmin` password hashes caused new passwords not to work in a restored cluster. As a consequence, the restored cluster used the old `kubeadmin` password instead of the new one, resulting in login failure. With this release, the `kubeadmin` password hash mismatch in restored clusters has been addressed, and reconciliation logic has been updated. As a result, new `kubeadmin` passwords in restored clusters now match, allowing successful login. ([OCPBUGS-38898](https://redhat.atlassian.net/browse/OCPBUGS-38898))

- Before this update, the Hosted Cluster Config Operator failed to start on non-OpenShift management clusters due to an unconditional watch for `route.openshift.io` routes. As a consequence, hosted control planes deployment was prevented. With this release, the Hosted Cluster Config Operator now ignores route watches on non-OpenShift management clusters, preventing failure during startup. As a result, the Hosted Cluster Config Operator now starts cleanly on non-OpenShift management clusters, improving deployment on un-customized Kubernetes. ([OCPBUGS-86008](https://redhat.atlassian.net/browse/OCPBUGS-86008))

- Before this update, when a KubeVirt hosted cluster and its management cluster both used OVN-Kubernetes with dual-stack networking, they each defaulted to `fd98::/64` for the IPv6 join switch subnet. As a consequence, external IPv6 `LoadBalancer` traffic targeting VM pods was moved to join IP of the management cluster; for example, `fd98::2`. Inside the VM, the OVN of the hosted cluster intercepts the response because it also owns `fd98::/64`, black-holing the packet and breaking IPv6 connectivity. With this release, the reconciler now automatically sets `IPv6.InternalJoinSubnet` to `fd99::/64`, avoiding the collision with the `fd98::/64` of the management cluster. A new `OVNIPv6Config` API field also allows explicit user configuration of the IPv6 join subnet on any platform. As a result, IPv6 `LoadBalancer` traffic flows correctly in dual-stack KubeVirt hosted clusters without routing collisions between the management and hosted OVN networks. ([OCPBUGS-84303](https://redhat.atlassian.net/browse/OCPBUGS-84303))

- Before this update, the `HostedCluster` controller set the `AWSDefaultSecurityGroupDeleted` condition on all `HostedCluster` resources during deletion, regardless of platform type. The `AWSDefaultSecurityGroupCreated` condition was correctly gated behind an AWS platform check, but the deletion counterpart had no such gate. As a consequence, non-AWS `HostedCluster` resources, such as Azure and KubeVirt, displayed an AWS-specific `AWSDefaultSecurityGroupDeleted` condition with `Status: Unknown` during deletion, producing misleading status information. With this release, a platform-type check gates the `AWSDefaultSecurityGroupDeleted` condition to AWS-only `HostedCluster` resources, matching the existing pattern used for `AWSDefaultSecurityGroupCreated`.As a result, non-AWS `HostedCluster` resources no longer display the `AWSDefaultSecurityGroupDeleted` condition during deletion. The condition is set for only AWS platform clusters. ([OCPBUGS-84971](https://redhat.atlassian.net/browse/OCPBUGS-84971))

- Before this update, the `CertificateRevocationController` verified certificate revocation through the Kubernetes API Server service load balancer, which routes to a single pod. In high availability (HA) deployments with three Kubernetes API Server replicas, the check could hit a pod that had loaded the updated trust bundle while others did not, causing premature state transitions in the revocation flow. With this release, the controller has been updated to verify certificate trust and revocation against every individual Kubernetes API Server pod by IP, rather than through the service. Certificate revocation now completes reliably in HA deployments by confirming all Kubernetes API Server pods have propagated the change. ([OCPBUGS-86039](https://issues.redhat.com/browse/OCPBUGS-86039))

- Before this update, when the `hypershift.openshift.io/restart-date` annotation was set on a `HostedCluster` resource, the `cleanupClusterNetworkOperatorResources` function in the Control Plane Operator restarted several Cluster Network Operator-managed operands, but omitted the `cloud-network-config-controller` deployment. As a consequence, the `cloud-network-config-controller` pod was not restarted when the `restart-date` annotation was applied. Stale cloud API credentials or `kubeconfig` references could persist after rotation, causing cloud networking operations to fail on AWS, Azure, and OpenStack platforms with OVN networking. With this release, the `restart-date` annotation propagation is moved from the Control Plane Operator into the Cluster Network Operator. The Cluster Network Operator reads the `hypershift.openshift.io/restart-date` annotation from the `HostedControlPlane` custom resource and injects it into pod template annotations of all rendered `Deployments`, `DaemonSets`, and `StatefulSets` within the hosted control planes namespace. The redundant Control Plane Operator-side restart logic was removed. As a result, when the `restart-date` annotation is set on a `HostedCluster` resource, all Cluster Network Operator-managed operands are now restarted correctly. ([OCPBUGS-88531](https://redhat.atlassian.net/browse/OCPBUGS-88531))

- Before this update, on dual-stack hosted clusters, Kubernetes API Server certificates churned due to improper IP Subject Alternative Name (SAN) normalization. As a consequence, hosted control planes installations with IPv6 public networks repeatedly failed, causing continuous restarts of `kube-apiserver` pods. With this release, IP SANs in certificates have been normalized to stop dual-stack Kubernetes API Server certificate churn. As a result, hosted control planes installation no longer fails with IPv6 public networks in `ClusterNetwork` and `ServiceNetwork`, ensuring smooth dual-stack cluster setup. ([OCPBUGS-112730](https://redhat.atlassian.net/browse/OCPBUGS-112730))

- Before this update, KubeVirt hosted clusters that used Multus as the primary network received `nmstate` IPv6 configuration that was intended for the default OVN network. As a consequence, affected compute nodes could not obtain an IPv6 address through Stateless Address AutoConfiguration (SLAAC), and could not become Ready. With this release, hosted control planes conditionally overrides the configuration for IPv6-enabled Multus-primary node pools. As a result, compute nodes can obtain their IPv6 addresses through SLAAC and become Ready. ([OCPBUGS-121866](https://redhat.atlassian.net/browse/OCPBUGS-121866))

- Before this update, an invalid tagged registry entry in the `blockedRegistries` field of a `HostedCluster` resource caused an error. As a consequence, nodes failed to join the cluster. With this release, a fix validates registry entries. As a result, invalid registry config errors are now caught earlier and reported in node pool condition and ignition logs, making it easier to debug and join the cluster. ([OCPBUGS-43353](https://redhat.atlassian.net/browse/OCPBUGS-43353))

- Before this update, the Private Link controller retrieved the `DNSZoneID` from AWS instead of the status, causing health checks to enter a continuous reconciliation loop and potential AWS rate limit hits. As a consequence, AWS a Distributed denial-of-service (DDoS) attack was possible. With this release, the controller now uses `Status.DNSZoneID` before it queries AWS Route53, reducing AWS rate limit hits. As a result, AWS rate limits are no longer exceeded due to continuous reconciliation loops in health checks, improving the overall system stability. ([OCPBUGS-57453](https://redhat.atlassian.net/browse/OCPBUGS-57453))

- Before this update, the error message for installing an unsupported OpenShift Container Platform patch version was misleading. As a consequence, users encountered difficulties installing unsupported OpenShift Container Platform release versions. With this release, the error message in the unsupported OpenShift Container Platform release version selection now shows the correct minor version. As a result, the `HostedCluster` resource no longer enters a degraded state when installing unsupported OpenShift Container Platform versions beyond 4.18.0. ([OCPBUGS-59142](https://redhat.atlassian.net/browse/OCPBUGS-59142))

- Before this update, the `oauth-apiserver` resource in hosted control planes was started without the `--tls-cipher-suites` argument. With this fix, the `oauth-apiserver` resource now includes the appropriate TLS cipher suites based on the configured TLS security profile. ([OCPBUGS-65730](https://redhat.atlassian.net/browse/OCPBUGS-65730))

- Before this update, an in-place upgrade error occurred due to an unnamed degraded node during disk validation, causing the upgrade to stall. As a consequence, the degraded node was not identified in logs, resulting in silent upgrade failures. With this release, the upgrade error message now includes the degraded node name. As a result, the degraded node is identified in Hosted Cluster Config Operator logs, and the `NodePool` resource status reflects stalled upgrades, enabling clearer troubleshooting for users. ([OCPBUGS-75887](https://redhat.atlassian.net/browse/OCPBUGS-75887))

- Before this update, the headless `etcd-client` service caused intermittent peer TLS rejections due to duplicate PTR records, because its IP address was not covered in the DNS SANs of the certificate. As a consequence, intermittent etcd peer connection rejections occurred due to duplicate DNS records in the headless service. With this release, the missing DNS name for the `etcd-client` service has been added to prevent intermittent peer connection rejections. As a result, this bug fix resolves intermittent rejections of etcd peer connections due to duplicate PTR records, improving etcd reliability in bare metal deployments. ([OCPBUGS-76530](https://redhat.atlassian.net/browse/OCPBUGS-76530))

- Before this update, the validation rule for the API Server `LoadBalancer` hostname in the `servingCerts` section lacked `has()` guards. As a consequence, validation failures occurred during upgrades of multicluster engine Operator, preventing the patching of `HostedCluster` CRDs. With this release, the missing `has()` guards have been fixed in the `servingCerts` validation rule. As a result, validation failures during `HostedCluster` CRD patching are resolved, enabling successful multicluster engine Operator upgrades. ([OCPBUGS-77827](https://redhat.atlassian.net/browse/OCPBUGS-77827))

- Before this update, non-AWS platforms triggered repetitive vCPU log messages due to unsupported platform usage in metrics collection. As a consequence, repetitive `info` logs created rapid log growth in complex environments. With this release, repetitive vCPU logs for non-AWS platforms are removed from the metrics collector. As a result, repetitive vCPU log messages are suppressed, reducing log noise for non-AWS users. ([OCPBUGS-81631](https://redhat.atlassian.net/browse/OCPBUGS-81631))

- Before this update, when multiple node pools in a hosted cluster on AWS referenced subnets in the same availability zone (AZ), VPC endpoint reconciliation failed with an AWS `DuplicateSubnetsInSameZone` error. The AWS API requires at most one subnet per AZ per VPC endpoint, so affected clusters experienced indefinite endpoint unavailability. With this update, the Control Plane Operator deduplicates subnets by AZ before calling the AWS endpoint API, selecting one subnet per AZ deterministically. VPC endpoint reconciliation no longer fails due to multiple subnets in the same AZ. ([OCPBUGS-82443](https://redhat.atlassian.net/browse/OCPBUGS-82443))

- Before this update, in hosted clusters on OpenShift Virtualization, users could not change the default storage class. With this release, users can set a different default storage class other than `kubevirt-csi-infra-default` on hosted clusters on OpenShift Virtualization. ([OCPBUGS-43444](https://redhat.atlassian.net/browse/OCPBUGS-43444))

- Before this update, a substring matching approach for skipping HTTP proxy in the `noProxy` list caused the Node-local API to always tunnel via the proxy. As a consequence, TLS handshake timeouts and workload failures occurred. With this release, standard `NO_PROXY` matching is used for `skipProxyForKAS`. As a result, the API server no longer tunnels via the proxy for excluded hostnames in `NO_PROXY`, improving the stability of workloads and Operator experience. ([OCPBUGS-83328](https://redhat.atlassian.net/browse/OCPBUGS-83328))

- Before this update, during hosted cluster creation on Azure, the private DNS zone creation for the base domain shadowed `*.apps` DNS resolution. As a consequence, hosted clusters on Azure failed to provision due to DNS resolution errors. With this release, the fix prevents Azure private DNS zone shadowing of the apps domain when `externalDNSDomain` equals `name.baseDomain`. As a result, creating hosted clusters on Azure no longer results in console and ingress failures due to DNS resolution errors. ([OCPBUGS-85351](https://redhat.atlassian.net/browse/OCPBUGS-85351))

- Before this update, during a KubeVirt `NodePool` rolling update, the HyperShift Operator deleted the old `userdata` Secret as soon as a new configuration version was computed, while existing worker VMs still referenced it. As a consequence, the worker VMs failed to mount the `cloudinitvolume-udata` volume, blocking live migration and potentially stalling infrastructure and hub cluster upgrades. This release extended the existing `userdata` Secret retention logic to also cover the KubeVirt platform, deferring Secret cleanup until the rollout is complete and all old-generation VMs are gone. As a result, KubeVirt worker VMs continue to operate and live-migrate normally during `NodePool` rolling updates. ([OCPBUGS-86494](https://redhat.atlassian.net/browse/OCPBUGS-86494))

- Before this update, the Control Plane Operator attempted to delete the AWS default security group during `HostedCluster` resource deletion, but skipped the health check due to an early return, causing an infinite re-queue loop when the OIDC provider was deleted before the `HostedCluster` resource. As a consequence, the `HostedCluster` resource leaked on the management cluster, causing test failures and resource waste. With this release, the health check controller now evaluates AWS credentials during deletion, preventing the infinite re-queue loop when the OIDC provider is deleted. As a result, the `HostedCluster` resource deletion process no longer gets stuck in a loop, preventing permanent resource leaks when the OIDC provider is removed before the `HostedCluster` resource. ([OCPBUGS-91511](https://redhat.atlassian.net/browse/OCPBUGS-91511))

# Technology Preview features status

Some features in this release are currently in Technology Preview. These experimental features are not intended for production use.

Note the following scope of support on the Red Hat Customer Portal for these features:

[Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview)

In the following table, features are marked with the following statuses:

- *Not Available*

- *Technology Preview*

- *General Availability*

- *Deprecated*

- *Removed*

> [!IMPORTANT]
> For IBM Power and IBM Z, the following exceptions apply:
>
> - For version 4.20 and later, you must run the control plane on machine types that are based on 64-bit x86 architecture or s390x architecture, and node pools on IBM Power or IBM Z.
>
> - For version 4.19 and earlier, you must run the control plane on machine types that are based on 64-bit x86 architecture, and node pools on IBM Power or IBM Z.

| Feature | 4.21 | 4.22 | 5.0 |
|----|----|----|----|
| Hosted control planes for OpenShift Container Platform using non-bare-metal agent machines | Technology Preview | Technology Preview | Technology Preview |
| Hosted control planes for OpenShift Container Platform on RHOSP | Technology Preview | Technology Preview | Technology Preview |
| Custom taints and tolerations | Technology Preview | Technology Preview | Technology Preview |
| NVIDIA GPU devices on hosted control planes for OpenShift Virtualization | Technology Preview | Technology Preview | Technology Preview |
| Hosted control planes for OpenShift Virtualization on IBM Z | Technology Preview | General Availability | General Availability |
| Hosted control planes for OpenShift Container Platform on Microsoft Azure | Not Available | Technology Preview | General Availability |
| Backup and restore with the etcd snapshot method | Not Available | Technology Preview | Technology Preview |
| Restoring a hosted cluster to a new management cluster by using OADP | Technology Preview | Technology Preview | Technology Preview |

Hosted control planes GA and TP tracker

> [!NOTE]
> Hosted control planes for OpenShift Virtualization on IBM Z is supported as Technology Preview starting with OpenShift Container Platform 4.21, multicluster engine for Kubernetes Operator 2.11, and Red Hat Advanced Cluster Management (RHACM) 2.16. Creating hosted control planes with external infrastructure is not supported.

# Known issues

This section includes several known issues for hosted control planes for OpenShift Container Platform 4.17.

- If the annotation and the `ManagedCluster` resource name do not match, the multicluster engine for Kubernetes Operator console displays the cluster as `Pending import`. The cluster cannot be used by the multicluster engine Operator. The same issue happens when there is no annotation and the `ManagedCluster` name does not match the `Infra-ID` value of the `HostedCluster` resource.

- When you use the multicluster engine for Kubernetes Operator console to add a new node pool to an existing hosted cluster, the same version of OpenShift Container Platform might appear more than once in the list of options. You can select any instance in the list for the version that you want.

- When a node pool is scaled down to 0 workers, the list of hosts in the console still shows nodes in a `Ready` state. You can verify the number of nodes in two ways:

  - In the console, go to the node pool and verify that it has 0 nodes.

  - On the command-line interface, run the following commands:

    - Verify that 0 nodes are in the node pool by running the following command:

      ``` terminal
      $ oc get nodepool -A
      ```

    - Verify that 0 nodes are in the cluster by running the following command:

      ``` terminal
      $ oc get nodes --kubeconfig
      ```

    - Verify that 0 agents are reported as bound to the cluster by running the following command:

      ``` terminal
      $ oc get agents -A
      ```

- When you create a hosted cluster in an environment that uses the dual-stack network, you might encounter pods stuck in the `ContainerCreating` state. This issue occurs because the `openshift-service-ca-operator` resource cannot generate the `metrics-tls` secret that the DNS pods need for DNS resolution. As a result, the pods cannot resolve the Kubernetes API server. To resolve this issue, configure the DNS server settings for a dual stack network.

- If you created a hosted cluster in the same namespace as its managed cluster, detaching the managed hosted cluster deletes everything in the managed cluster namespace including the hosted cluster. The following situations can create a hosted cluster in the same namespace as its managed cluster:

  - You created a hosted cluster on the Agent platform through the multicluster engine for Kubernetes Operator console by using the default hosted cluster cluster namespace.

  - You created a hosted cluster through the command-line interface or API by specifying the hosted cluster namespace to be the same as the hosted cluster name.

- When you use the console or API to specify an IPv6 address for the `spec.services.servicePublishingStrategy.nodePort.address` field of a hosted cluster, a full IPv6 address with 8 hextets is required. For example, instead of specifying `2620:52:0:1306::30`, you need to specify `2620:52:0:1306:0:0:0:30`.

- In hosted control planes on OpenShift Virtualization, if you store all hosted cluster information in a shared namespace and then back up and restore a hosted cluster, you might unintentionally change other hosted clusters. To avoid this issue, back up and restore only hosted clusters that use labels, or avoid storing all hosted cluster information in a shared namespace.

- For version 4.21, hosted control planes pins all Cluster API images to the `4.20.10-multi` release image for compatibility reasons. Hosted control planes pins the images when Cluster API deployments are generated. The `4.20.10-multi` image must always be mirrored and available in order for the Cluster API to work with hosted control planes version 4.21.

- Intermittent egress IP outages occur when a hosted cluster uses the following combined settings:

  - The service publishing strategy for the `Konnectivity` service is set to `Route`.

  - The management cluster uses Virtual Router Redundancy Protocol (VRRP) VIP for ingress.
