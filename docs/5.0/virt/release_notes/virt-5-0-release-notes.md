These release notes describe new features and enhancements, Technology Preview features, deprecated and removed features, fixed issues, and known issues for OpenShift Virtualization 4.22.

# Supported guest operating systems

To view the supported guest operating systems for OpenShift Virtualization, see [Certified Guest Operating Systems in Red Hat OpenStack Platform, Red Hat Virtualization, OpenShift Virtualization and Red Hat Enterprise Linux with KVM](https://access.redhat.com/articles/973163#ocpvirt).

# New features and enhancements

# Deprecated features

The `HotplugVolume` feature gate is deprecated
The `HotplugVolume` feature gate, which allows you to add storage without restarting your VM, is deprecated and will be removed in a future release. This feature gate will be replaced by `DeclarativeHotplugVolumes`.

<div class="note">

`DeclarativeHotplugVolumes` does not support hot plugging ephemeral volumes. Ephemeral volumes are hot plugged to a VMI and do not persist in the owner VM. Existing ephemeral volumes that are hot plugged are automatically detached after you switch to the `DeclarativeHotplugVolumes` feature gate.

</div>

[CNV-73301](https://issues.redhat.com/browse/CNV-73301)

# Removed features

Removed features are no longer supported in OpenShift Virtualization.

# Technology Preview features

Some features in this release are currently in Technology Preview. These experimental features are not intended for production use. Note the following scope of support on the Red Hat Customer Portal for these features:

[Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview)

Golden image support for heterogeneous clusters (Technology Preview)
Golden image support is available for heterogeneous clusters, which enables you to create and use golden images for virtual machines in environments with differing node configurations. This capability is a Technology Preview feature.

[CNV-62357](https://issues.redhat.com/browse/CNV-62357)

<!-- -->

Custom video device support in virtual machines (Technology Preview)
You can now configure a custom video device type when creating a virtual machine. Configuring a custom device type overrides the default video configuration, and allows you to specify different video devices, based on your guest operating system requirements and performance needs. This capability is a Technology Preview feature.

[CNV-71192](https://issues.redhat.com/browse/CNV-71192)

<!-- -->

Convert an existing VM to a template from the user interface (Technology Preview)
Virtual machine (VM) owners can create, filter, and delete a user-generated template. You can create a template from an existing VM in the same project as the running VM or a different project from the OpenShift Virtualization user interface. To make sure that the data is consistent, stop the VM before you create a template. This capability is a Technology Preview feature.

[CNV-81577](https://redhat.atlassian.net/browse/CNV-81577)

<!-- -->

Create virtual machines from in-cluster native templates (Technology Preview)
Virtual machine (VM) owners can create VMs from the OpenShift Virtualization cluster native template custom resource. The VM template tracks a golden image that is updated periodically, reducing errors and ensuring uniformity in the virtualized environment. You can host the template in all namespaces that you can control.

[CNV-73392](https://redhat.atlassian.net/browse/CNV-73392)

# Fixed issues

# Known issues

Some linked Jira tickets are accessible only with Red Hat credentials.

Non-versioned HyperConverged commands default to v1 API
In this release, the v1 API for the `HyperConverged` custom resource (CR) is introduced, in preparation for a future migration from v1beta1 to v1. Due to the way Kubernetes selects default API versions, non-versioned commands such as `oc get hco`, `oc edit hyperconverged`, and `oc patch hyperconverged` now default to the v1 API. As a consequence, these commands can behave unexpectedly or fail because the v1 API is not yet ready for production use.

To work around this problem, use the fully versioned type name `hyperconvergeds.v1beta1.hco.kubevirt.io` when running commands against the `HyperConverged` CR. For example, use `oc get hyperconvergeds.v1beta1.hco.kubevirt.io` instead of `oc get hco`. For the `oc explain` command, use the `--api-version` flag: `oc explain --api-version=hco.kubevirt.io/v1beta1 hco.spec`. As a result, commands target the v1beta1 API as intended.

[CNV-78892](https://redhat.atlassian.net/browse/CNV-78892)

<!-- -->

VMs using the cnv-bridge CNI fail to live migrate after updates from 4.12
When you update from OpenShift Container Platform 4.12 to a newer minor version, virtual machines that use the `cnv-bridge` Container Network Interface (CNI) fail to live migrate. As a consequence, live migration fails for affected VMs.

To work around this problem, change the `spec.config.type` field in your `NetworkAttachmentDefinition` manifest from `cnv-bridge` to `bridge` before you perform the update. As a result, live migration succeeds for VMs that use the updated network attachment definitions.

[Known issue when migrating VMs that use the cnv-bridge CNI](https://access.redhat.com/solutions/7069807)

<!-- -->

Red Hat OpenShift Service Mesh 3.1.1 and Istio 1.25 and later are incompatible with OpenShift Virtualization
Red Hat OpenShift Service Mesh 3.1.1 and Istio versions 1.25 and later are incompatible with OpenShift Virtualization 4.22 because the `traffic.sidecar.istio.io/kubevirtInterfaces` annotation is deprecated. As a consequence, service mesh integration with OpenShift Virtualization can fail when you use these versions.

To work around this problem, when you install Service Mesh for integration with OpenShift Virtualization, select Red Hat OpenShift Service Mesh version 3.0.4 and Istio 1.24.4 instead of the default versions that are displayed in the web console.

[OSSM-10883](https://issues.redhat.com/browse/OSSM-10883)

<!-- -->

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

Service account volume becomes invalid after VM migration
OpenShift Virtualization links a service account token in use by a pod to that specific pod by creating a disk image that contains the token. If you migrate a VM, the service account volume becomes invalid for the migrated VM. As a consequence, workloads that rely on that service account token can fail after migration.

To work around this problem, use user accounts instead of service accounts, because user account tokens are not bound to a specific pod.

[CNV-33835](https://issues.redhat.com/browse/CNV-33835)

Upgrading to OpenShift Virtualization 4.21 when using wasp-agent
If you are upgrading OpenShift Virtualization from version 4.20 to 4.21 and using `wasp-agent` to increase VM workload density, you must perform the following steps after you begin the upgrade:

1.  Wait for the Machine Configuration Pool (MCP) to complete the updating of the infra nodes.

2.  Edit the `KubeletConfig` file to remove the `failSwapOn: false` key-value pair.

3.  Wait for the MCP to finish updating the worker nodes.

[CNV-75837](https://issues.redhat.com/browse/CNV-75837)
