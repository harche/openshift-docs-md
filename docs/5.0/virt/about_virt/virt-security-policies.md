OpenShift Virtualization provides built-in security features and authorization policies to protect virtual machine workloads and ensure secure cluster operations across your environment.

**Key points**

- OpenShift Virtualization adheres to the `restricted` Kubernetes pod security standards profile, which aims to enforce the current best practices for pod security.

- Virtual machine (VM) workloads run as unprivileged pods.

- Security context constraints (SCCs) are defined for the `kubevirt-controller` service account. For more information about SCCs, see "Additional resources".

- TLS certificates for OpenShift Virtualization components are renewed and rotated automatically.

# Workload security

By default, virtual machine (VM) workloads do not run with root privileges in OpenShift Virtualization, and there are no supported OpenShift Virtualization features that require root privileges.

For each VM, a `virt-launcher` pod runs an instance of `libvirt` in *session mode* to manage the VM process. In session mode, the `libvirt` daemon runs as a non-root user account and only permits connections from clients that are running under the same user identifier (UID). Therefore, VMs run as unprivileged pods, adhering to the security principle of least privilege.

# TLS certificates

TLS certificates for OpenShift Virtualization components are renewed and rotated automatically. You are not required to refresh them manually.

## Automatic renewal schedules

TLS certificates are automatically deleted and replaced according to the following schedule:

- KubeVirt certificates are renewed daily.

- Containerized Data Importer controller (CDI) certificates are renewed every 15 days.

- MAC pool certificates are renewed every year. Automatic TLS certificate rotation does not disrupt any operations. For example, the following operations continue to function without any disruption:

- Migrations

- Image uploads

- VNC and console connections

# Authorization

OpenShift Virtualization uses role-based access control (RBAC) to define permissions for users and service accounts.

By default, OpenShift Virtualization aggregates virtualization permissions into standard OpenShift Container Platform cluster roles (`view`, `edit`, and `admin`). You can disable this role aggregation if you want to grant virtualization permissions manually to specific users or groups.

## Default cluster roles for OpenShift Virtualization

By using cluster role aggregation, OpenShift Virtualization extends the default OpenShift Container Platform cluster roles to include permissions for accessing virtualization objects. Roles unique to OpenShift Virtualization are not aggregated with OpenShift Container Platform roles.

| Default cluster role | OpenShift Virtualization cluster role | OpenShift Virtualization cluster role description |
|----|----|----|
| `view` | `kubevirt.io:view` | A user that can view all OpenShift Virtualization resources in the cluster but cannot create, delete, modify, or access them. For example, the user can see that a virtual machine (VM) is running but cannot shut it down or gain access to its console. |
| `edit` | `kubevirt.io:edit` | A user that can modify all OpenShift Virtualization resources in the cluster. For example, the user can create VMs, access VM consoles, and delete VMs. |
| `admin` | `kubevirt.io:admin` | A user that has full permissions to manage virtual machines and related resources, including the ability to delete collections of resources. The scope of permissions depends on whether the role is bound using a `ClusterRoleBinding` (cluster-wide) or `RoleBinding` (namespace-scoped). |
| `N/A` | `kubevirt.io:migrate` | A user that can create, delete, and update VM live migration requests, which are represented by namespaced `VirtualMachineInstanceMigration` (VMIM) objects. This role is specific to OpenShift Virtualization. |

OpenShift Virtualization cluster roles

## Role aggregation

Users with default `admin`, `edit`, or `view` roles automatically receive matching virtualization permissions. You can disable this behavior to control virtualization access explicitly.

> [!IMPORTANT]
> Disabling OpenShift Virtualization role aggregation is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

By default, OpenShift Virtualization uses Kubernetes aggregated cluster roles to extend the default `admin`, `edit`, and `view` cluster roles with permissions for virtualization resources. When a user has one of these default roles in a namespace, they can perform the corresponding virtualization operations. For example, a user with the `edit` role in a namespace can create and modify virtual machines (VMs) in that namespace.

The OpenShift Virtualization cluster roles are aggregated as follows:

| OpenShift Virtualization cluster role | Default cluster role |
|---------------------------------------|----------------------|
| `kubevirt.io:admin`                   | `admin`              |
| `kubevirt.io:edit`                    | `edit`               |
| `kubevirt.io:view`                    | `view`               |

OpenShift Virtualization cluster role aggregation

In clusters that require stricter authorization boundaries, you can disable this automatic aggregation by setting `spec.virtualization.roleAggregationStrategy` to `Manual` in the `HyperConverged` custom resource (CR). The HyperConverged Operator (HCO) propagates the setting to KubeVirt at runtime and automatically enables the required `OptOutRoleAggregation` feature gate. Do not edit the KubeVirt CR or the feature gate directly.

> [!IMPORTANT]
> Setting the strategy to `Manual` immediately removes virtualization permissions from all users who rely on aggregated `admin`, `edit`, or `view` roles. The change takes effect at runtime with no grace period. Before disabling role aggregation, grant virtualization permissions explicitly to users and groups that require access.

The `roleAggregationStrategy` field supports the following values:

| Value | Behavior |
|----|----|
| `AggregateToDefault` (default) | Aggregates OpenShift Virtualization cluster roles to the default `admin`, `edit`, and `view` cluster roles. |
| `Manual` | Does not aggregate kubevirt cluster roles to the default cluster roles. Administrators must bind kubevirt cluster roles explicitly to users or groups. |

roleAggregationStrategy field values

If the field is not set, `AggregateToDefault` behavior is used.

When the strategy is `Manual`, the `aggregate-to-admin`, `aggregate-to-edit`, and `aggregate-to-view` labels on kubevirt cluster roles are set to `false`. Users with the standard `admin`, `edit`, or `view` roles do not automatically receive the corresponding kubevirt permissions. Existing RBAC bindings that grant kubevirt cluster roles directly continue to work.

You can change the strategy at any time. HCO and kubevirt apply the change at runtime, and reinstalling OpenShift Virtualization or restarting any pods is not required and not necessary.

## Control virtualization role assignment with the web console

Disable automatic virtualization permissions to enforce stricter authorization boundaries in your cluster.

> [!IMPORTANT]
> Disabling OpenShift Virtualization role aggregation is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with `cluster-admin` permissions.

- OpenShift Virtualization is installed.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Navigate to **Virtualization** → **Settings** in the web console.

2.  Click the **Preview features** tab.

3.  Toggle **Control default Virtualization permissions** to on to enable control over default virtualization role assignments.

4.  Click the **Cluster** tab.

5.  Under **General settings**, expand **Automatically grant Virtualization roles**.

6.  Select the required state:

    - To disable role aggregation, toggle **Automatically grant Virtualization roles** to off.

    - To enable role aggregation, toggle **Automatically grant Virtualization roles** to on.

</div>

<div class="formalpara">

<div class="title">

Verification

</div>

Navigate to **Virtualization** → **Settings** → **Cluster** and verify that **Automatically grant Virtualization roles** shows the intended state.

</div>

## Control virtualization role assignment with CLI

Disable automatic virtualization permissions to enforce stricter authorization boundaries in your cluster.

> [!IMPORTANT]
> Disabling OpenShift Virtualization role aggregation is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with `cluster-admin` permissions.

- OpenShift Virtualization is installed.

- The OpenShift CLI (`oc`) is installed.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Disable role aggregation by running the following command:

    ``` terminal
    $ oc patch hyperconverged kubevirt-hyperconverged \
        -n openshift-cnv \
        --type=merge \
        -p '{"spec":{"virtualization":{"roleAggregationStrategy":"Manual"}}}'
    ```

2.  Verify that the HyperConverged Operator (HCO) propagated the setting to KubeVirt:

    ``` terminal
    $ oc get kubevirt kubevirt-kubevirt-hyperconverged \
        -n openshift-cnv \
        -o jsonpath='{.spec.configuration.roleAggregationStrategy}'
    ```

    The output shows `Manual`.

3.  Verify that the `OptOutRoleAggregation` feature gate is enabled:

    ``` terminal
    $ oc get kubevirt kubevirt-kubevirt-hyperconverged \
        -n openshift-cnv \
        -o jsonpath='{.spec.configuration.developerConfiguration.featureGates}' | grep -o OptOutRoleAggregation
    ```

    The output shows `OptOutRoleAggregation`.

4.  Optional: Verify that a cluster role is no longer marked for aggregation. For example, verify that the `kubevirt.io:edit` cluster role has an `aggregate-to-edit` label value of `false`:

    ``` terminal
    $ oc get clusterrole kubevirt.io:edit \
        -o jsonpath='{.metadata.labels.rbac\.authorization\.k8s\.io/aggregate-to-edit}'
    ```

    The output shows `false`.

5.  Optional: To re-enable aggregation, set the field to `AggregateToDefault`:

    ``` terminal
    $ oc patch hyperconverged kubevirt-hyperconverged \
        -n openshift-cnv \
        --type=merge \
        -p '{"spec":{"virtualization":{"roleAggregationStrategy":"AggregateToDefault"}}}'
    ```

    Alternatively, remove the field entirely from the HyperConverged CR:

    ``` terminal
    $ oc patch hyperconverged kubevirt-hyperconverged \
        -n openshift-cnv \
        --type=json \
        -p '[{"op":"remove","path":"/spec/virtualization/roleAggregationStrategy"}]'
    ```

    When the field is set, including when it is set to `AggregateToDefault`, HCO keeps the `OptOutRoleAggregation` feature gate enabled. When the field is removed, HCO removes the feature gate and KubeVirt uses its default aggregation behavior.

</div>

## Bind virtualization roles to users

When role aggregation is disabled, bind OpenShift Virtualization cluster roles explicitly to users or groups. These roles supplement the default OpenShift Container Platform `admin`, `edit`, and `view` roles.

> [!IMPORTANT]
> Disabling OpenShift Virtualization role aggregation is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with `cluster-admin` permissions or with the `escalate` and `bind` permissions on the cluster role you want to assign.

- The target namespace exists, if you are creating a `RoleBinding`.

- The OpenShift CLI (`oc`) is installed.

</div>

> [!IMPORTANT]
> Users also need the base OpenShift Container Platform `edit` or `view` role to access core resources such as pods, persistent volume claims, and events. The OpenShift Virtualization cluster roles grant virtualization-specific permissions only.
>
> Regardless of the `roleAggregationStrategy` value, all authenticated users retain read access to the KubeVirt custom resource (CR) itself through the `kubevirt.io:default` cluster role.

<div>

<div class="title">

Procedure

</div>

1.  Use a `RoleBinding` to grant access in one namespace or a `ClusterRoleBinding` to grant access in all namespaces.

    - `RoleBinding` example that grants `kubevirt.io:edit` permissions to the `developers` group in the `dev-team` namespace:

      ``` yaml
      apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: virt-editors
        namespace: dev-team
      subjects:
        - kind: Group
          name: developers
          apiGroup: rbac.authorization.k8s.io
      roleRef:
        kind: ClusterRole
        name: kubevirt.io:edit
        apiGroup: rbac.authorization.k8s.io
      ```

    - `ClusterRoleBinding` example that grants `kubevirt.io:view` permissions to the `vm-viewers` group in all namespaces:

      ``` yaml
      apiVersion: rbac.authorization.k8s.io/v1
      kind: ClusterRoleBinding
      metadata:
        name: virt-viewers
      subjects:
        - kind: Group
          name: vm-viewers
          apiGroup: rbac.authorization.k8s.io
      roleRef:
        kind: ClusterRole
        name: kubevirt.io:view
        apiGroup: rbac.authorization.k8s.io
      ```

2.  Save the manifest to a file.

3.  Apply the manifest:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

- For a `RoleBinding`, verify that the binding was created and grants the expected permissions:

  ``` terminal
  $ oc get rolebinding virt-editors -n dev-team
  ```

  ``` terminal
  $ oc auth can-i create virtualmachines -n dev-team --as-group=developers
  ```

  The output shows `yes`.

- For a `ClusterRoleBinding`, verify that the binding grants permissions cluster-wide:

  ``` terminal
  $ oc get clusterrolebinding virt-viewers
  ```

  ``` terminal
  $ oc auth can-i list virtualmachines --all-namespaces --as-group=vm-viewers
  ```

  The output shows `yes`.

</div>

## RBAC roles for storage features in OpenShift Virtualization

Cluster-wide and namespaced RBAC roles enable the Containerized Data Importer (CDI) to manage storage resources, data volumes, and virtual machine disk operations.

### Cluster-wide RBAC roles

| CDI cluster role | Resources | Verbs |
|----|----|----|
| `cdi.kubevirt.io:admin` | `datavolumes`, `uploadtokenrequests` | `*` (all) |
| `datavolumes/source` | `create` |  |
| `cdi.kubevirt.io:edit` | `datavolumes`, `uploadtokenrequests` | `*` |
| `datavolumes/source` | `create` |  |
| `cdi.kubevirt.io:view` | `cdiconfigs`, `dataimportcrons`, `datasources`, `datavolumes`, `objecttransfers`, `storageprofiles`, `volumeimportsources`, `volumeuploadsources`, `volumeclonesources` | `get`, `list`, `watch` |
| `datavolumes/source` | `create` |  |
| `cdi.kubevirt.io:config-reader` | `cdiconfigs`, `storageprofiles` | `get`, `list`, `watch` |

Aggregated cluster roles for the `cdi.kubevirt.io` API group

<table>
<caption>Cluster-wide roles for the <code>cdi-operator</code> service account</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">API group</th>
<th style="text-align: left;">Resources</th>
<th style="text-align: left;">Verbs</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p><code>rbac.authorization.k8s.io</code></p></td>
<td style="text-align: left;"><p><code>clusterrolebindings</code>, <code>clusterroles</code></p></td>
<td style="text-align: left;"><p><code>get</code>, <code>list</code>, <code>watch</code>, <code>create</code>, <code>update</code>, <code>delete</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>security.openshift.io</code></p></td>
<td style="text-align: left;"><p><code>securitycontextconstraints</code></p></td>
<td style="text-align: left;"><p><code>get</code>, <code>list</code>, <code>watch</code>, <code>update</code>, <code>create</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>apiextensions.k8s.io</code></p></td>
<td style="text-align: left;"><p><code>customresourcedefinitions</code>, <code>customresourcedefinitions/status</code></p></td>
<td style="text-align: left;"><p><code>get</code>, <code>list</code>, <code>watch</code>, <code>create</code>, <code>update</code>, <code>delete</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>cdi.kubevirt.io</code></p></td>
<td style="text-align: left;"><p><code>*</code></p></td>
<td style="text-align: left;"><p><code>*</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>upload.cdi.kubevirt.io</code></p></td>
<td style="text-align: left;"><p><code>*</code></p></td>
<td style="text-align: left;"><p><code>*</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>admissionregistration.k8s.io</code></p></td>
<td style="text-align: left;"><p><code>validatingwebhookconfigurations</code>, <code>mutatingwebhookconfigurations</code></p></td>
<td style="text-align: left;"><p><code>create</code>, <code>list</code>, <code>watch</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>admissionregistration.k8s.io</code></p></td>
<td style="text-align: left;"><p><code>validatingwebhookconfigurations</code></p>
<p>Allow list: <code>cdi-api-dataimportcron-validate, cdi-api-populator-validate, cdi-api-datavolume-validate, cdi-api-validate, objecttransfer-api-validate</code></p></td>
<td style="text-align: left;"><p><code>get</code>, <code>update</code>, <code>delete</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>admissionregistration.k8s.io</code></p></td>
<td style="text-align: left;"><p><code>mutatingwebhookconfigurations</code></p>
<p>Allow list: <code>cdi-api-datavolume-mutate</code></p></td>
<td style="text-align: left;"><p><code>get</code>, <code>update</code>, <code>delete</code></p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>apiregistration.k8s.io</code></p></td>
<td style="text-align: left;"><p><code>apiservices</code></p></td>
<td style="text-align: left;"><p><code>get</code>, <code>list</code>, <code>watch</code>, <code>create</code>, <code>update</code>, <code>delete</code></p></td>
</tr>
</tbody>
</table>

| API group | Resources | Verbs |
|----|----|----|
| `""` (core) | `events` | `create`, `patch` |
| `""` (core) | `persistentvolumeclaims` | `get`, `list`, `watch`, `create`, `update`, `delete`, `deletecollection`, `patch` |
| `""` (core) | `persistentvolumes` | `get`, `list`, `watch`, `update` |
| `""` (core) | `persistentvolumeclaims/finalizers`, `pods/finalizers` | `update` |
| `""` (core) | `pods`, `services` | `get`, `list`, `watch`, `create`, `delete` |
| `""` (core) | `configmaps` | `get`, `create` |
| `storage.k8s.io` | `storageclasses`, `csidrivers` | `get`, `list`, `watch` |
| `config.openshift.io` | `proxies` | `get`, `list`, `watch` |
| `cdi.kubevirt.io` | `*` | `*` |
| `snapshot.storage.k8s.io` | `volumesnapshots`, `volumesnapshotclasses`, `volumesnapshotcontents` | `get`, `list`, `watch`, `create`, `delete` |
| `snapshot.storage.k8s.io` | `volumesnapshots` | `update`, `deletecollection` |
| `apiextensions.k8s.io` | `customresourcedefinitions` | `get`, `list`, `watch` |
| `scheduling.k8s.io` | `priorityclasses` | `get`, `list`, `watch` |
| `image.openshift.io` | `imagestreams` | `get`, `list`, `watch` |
| `""` (core) | `secrets` | `create` |
| `kubevirt.io` | `virtualmachines/finalizers` | `update` |

Cluster-wide roles for the `cdi-controller` service account

### Namespaced RBAC roles

| API group | Resources | Verbs |
|----|----|----|
| `rbac.authorization.k8s.io` | `rolebindings`, `roles` | `get`, `list`, `watch`, `create`, `update`, `delete` |
| `""` (core) | `serviceaccounts`, `configmaps`, `events`, `secrets`, `services` | `get`, `list`, `watch`, `create`, `update`, `patch`, `delete` |
| `apps` | `deployments`, `deployments/finalizers` | `get`, `list`, `watch`, `create`, `update`, `delete` |
| `route.openshift.io` | `routes`, `routes/custom-host` | `get`, `list`, `watch`, `create`, `update` |
| `config.openshift.io` | `proxies` | `get`, `list`, `watch` |
| `monitoring.coreos.com` | `servicemonitors`, `prometheusrules` | `get`, `list`, `watch`, `create`, `delete`, `update`, `patch` |
| `coordination.k8s.io` | `leases` | `get`, `create`, `update` |

Namespaced roles for the `cdi-operator` service account

| API group | Resources | Verbs |
|----|----|----|
| `""` (core) | `configmaps` | `get`, `list`, `watch`, `create`, `update`, `delete` |
| `""` (core) | `secrets` | `get`, `list`, `watch` |
| `batch` | `cronjobs` | `get`, `list`, `watch`, `create`, `update`, `delete` |
| `batch` | `jobs` | `create`, `delete`, `list`, `watch` |
| `coordination.k8s.io` | `leases` | `get`, `create`, `update` |
| `networking.k8s.io` | `ingresses` | `get`, `list`, `watch` |
| `route.openshift.io` | `routes` | `get`, `list`, `watch` |

Namespaced roles for the `cdi-controller` service account

## Additional SCCs and permissions for the kubevirt-controller service account

Security context constraints (SCCs) control permissions for pods. These permissions include actions that a pod, a collection of containers, can perform and what resources it can access. You can use SCCs to define a set of conditions that a pod must run with to be accepted into the system.

The `virt-controller` is a cluster controller that creates the `virt-launcher` pods for virtual machines in the cluster.

> [!NOTE]
> By default, `virt-launcher` pods run with the `default` service account in the namespace. If your compliance controls require a unique service account, assign one to the VM. The setting applies to the `VirtualMachineInstance` object and the `virt-launcher` pod.

The `kubevirt-controller` service account is granted additional SCCs and Linux capabilities so that it can create `virt-launcher` pods with the appropriate permissions. These extended permissions allow virtual machines to use OpenShift Virtualization features that are beyond the scope of typical pods.

The `kubevirt-controller` service account is granted the following SCCs:

`scc.AllowHostDirVolumePlugin = true`
This allows virtual machines to use the hostpath volume plugin.

`scc.AllowPrivilegedContainer = false`
This ensures the `virt-launcher` pod is not run as a privileged container.

`scc.AllowedCapabilities = []corev1.Capability{"SYS_NICE", "NET_BIND_SERVICE"}`
- `SYS_NICE` allows setting the CPU affinity.

- `NET_BIND_SERVICE` allows DHCP and Slirp operations.

### Viewing the SCC and RBAC definitions for the kubevirt-controller

You can view the `SecurityContextConstraints` definition for the `kubevirt-controller` by using the `oc` tool:

``` terminal
$ oc get scc kubevirt-controller -o yaml
```

You can view the RBAC definition for the `kubevirt-controller` clusterrole by using the `oc` tool:

``` terminal
$ oc get clusterrole kubevirt-controller -o yaml
```

# Additional resources

- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/#restricted)

- [About Security context constraints](../../authentication/managing-security-context-constraints.xml#security-context-constraints-about_configuring-internal-oauth)

- [Using RBAC to define and apply permissions](../../authentication/using-rbac.xml#using-rbac)

- [Managing security context constraints](../../authentication/managing-security-context-constraints.xml#security-context-constraints-about_configuring-internal-oauth)

- [Creating a cluster role](../../authentication/using-rbac.xml#creating-cluster-role_using-rbac)

- [Cluster role binding commands](../../authentication/using-rbac.xml#cluster-role-binding-commands_using-rbac)

- [Enabling user permissions to clone data volumes across namespaces](../../virt/storage/virt-enabling-user-permissions-to-clone-datavolumes.xml#virt-enabling-user-permissions-to-clone-datavolumes)
