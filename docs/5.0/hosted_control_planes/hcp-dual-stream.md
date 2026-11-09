In hosted control planes, Red Hat Enterprise Linux (RHEL) 9 and RHEL 10 compute nodes can run simultaneously within a single hosted cluster. By controlling the Red Hat Enterprise Linux CoreOS (RHCOS) major version for each `NodePool` object independently, you can incrementally migrate from RHEL 9 to RHEL 10 without replacing the entire cluster.

# Dual-stream RHCOS support for hosted control planes node pools

Hosted control planes supports running RHEL 9 and RHEL 10 boot images simultaneously within a single hosted cluster by assigning each `NodePool` resource to a specific Red Hat Enterprise Linux CoreOS (RHCOS) major version.

You control the operating system stream for each `NodePool` resource by using the `spec.osImageStream` API field, which accepts the `rhel-9` and `rhel-10` values. This capability is unique to hosted control planes and is not available in standalone OpenShift Container Platform, where all nodes in a cluster must share the same RHCOS version.

> [!IMPORTANT]
> In standalone OpenShift Container Platform, when you upgrade from a release of version 4 to version 5.0 without an explicit stream, existing nodes do not automatically migrate to RHEL 10. However, in the same scenario in hosted control planes, existing nodes do migrate to RHEL 10.

## How dual-stream differs from standalone OpenShift Container Platform

In standalone OpenShift Container Platform, all nodes in a cluster always run the same RHCOS major version. You cannot mix RHEL 9 and RHEL 10 nodes within a single cluster.

In hosted control planes, each `NodePool` resource has its own RHCOS boot image selection. Many `NodePool` resources within the same `HostedCluster` resource can run different RHCOS major versions simultaneously. With this architecture, you can complete the following tasks:

- Migrate workloads incrementally from RHEL 9 to RHEL 10 by running both versions in parallel.

- Pin workloads with RHEL 9 dependencies (such as `runc`) to RHEL 9 `NodePool` resources while moving other workloads to RHEL 10.

- Test RHEL 10 compatibility on a subset of nodes without replacing the entire cluster.

## Observing the active stream

The `status.osImageStream` field on a `NodePool` resource reports the RHCOS stream that is currently active across the pool’s nodes. The controller determines the observed stream from the operating system version reported by the nodes in the pool:

- RHCOS versions in the 4.xx series (for example, `4.22.x`) indicate `rhel-9`.

- RHCOS versions in the 5.xx series (for example, `5.0.x`) indicate `rhel-10`.

The `spec` value drives the controller’s boot image selection. The `status` value reflects what most nodes are actually running.

> [!NOTE]
> This version series mapping is enforced by the stream detection logic of the hosted control planes controller, not derived by users.

The majority-consensus rule means that `status.osImageStream` reflects the stream of the majority of nodes. During a rolling node replacement, the status field might temporarily show the old stream until most nodes have been replaced.

## Supported architectures for RHEL 10 NodePool resources

Red Hat Enterprise Linux (RHEL) 10 boot images for hosted control planes `NodePool` resources are available for a subset of architectures and platform combinations.

Before pinning a `NodePool` resource to `spec.osImageStream.name: rhel-10`, verify that RHEL 10 is available for your target architecture and platform. `NodePool` resources on architectures or platforms not listed in the RHEL 10 column must use `spec.osImageStream.name: rhel-9`.

| Architecture | RHEL 10 supported | Supported platforms for RHEL 10 |
|----|----|----|
| x86_64 | Yes | AWS, Azure, Google Cloud, bare metal, Red Hat OpenStack Platform (RHOSP), KubeVirt |
| aarch64 (ARM64) | Yes (limited) | AWS, Azure, Google Cloud, bare metal, RHOSP |
| ppc64le | Yes (limited) | Bare metal (Metal), RHOSP, IBM Power® Virtual Server |
| s390x | Yes (limited) | IBM Cloud®, KubeVirt, bare metal, RHOSP |

RHEL 10 platform support by architecture

> [!NOTE]
> RHEL 9 supports a broader set of platform and architecture combinations than RHEL 10 in this release. For any platform or architecture where RHEL 10 is not listed as supported, set `spec.osImageStream.name: rhel-9` on the `NodePool` resource.

### Platform availability gaps

The following table summarizes specific platform gaps for RHEL 10 boot images:

| Platform     | Architecture | Status                                   |
|--------------|--------------|------------------------------------------|
| KubeVirt     | aarch64      | RHEL 10 images not available; use RHEL 9 |
| KubeVirt     | ppc64le      | RHEL 10 images not available; use RHEL 9 |
| AWS          | ppc64le      | RHEL 10 images not available; use RHEL 9 |
| AWS          | s390x        | RHEL 10 images not available; use RHEL 9 |
| Azure        | ppc64le      | RHEL 10 images not available; use RHEL 9 |
| Azure        | s390x        | RHEL 10 images not available; use RHEL 9 |
| Google Cloud | ppc64le      | RHEL 10 images not available; use RHEL 9 |
| Google Cloud | s390x        | RHEL 10 images not available; use RHEL 9 |

RHEL 10 platform availability gaps

## Container runtime compatibility for RHEL 10 node pools

Before you migrate workloads to a RHEL 10 `NodePool` resource, verify that no `ContainerRuntimeConfig` resources in the cluster specify `defaultRuntime: runc` for the workloads you intend to migrate.

Workloads that depend on `runc` must remain on RHEL 9 `NodePool` resources and cannot be migrated to RHEL 10.

> [!NOTE]
> In standalone OpenShift Container Platform, when you upgrade from a release of version 4 to version 5.0 without an explicit stream, existing nodes do not automatically migrate to RHEL 10. However, in the same scenario in hosted control planes, existing nodes do migrate to RHEL 10.

| Container runtime | RHEL 9 `NodePool` resources | RHEL 10 `NodePool` resources |
|-------------------|-----------------------------|------------------------------|
| `crun`            | Yes                         | Yes                          |
| `runc`            | Yes                         | No                           |

Container runtime availability by RHCOS stream

If a `NodePool` resource uses a `ContainerRuntimeConfig` resource with `defaultRuntime: runc`, the controller behavior depends on the `spec.osImageStream` setting:

- On OpenShift Container Platform 5.0 and later, when the `spec.osImageStream` field is not set, the default stream is `rhel-10`. However, if the controller detects a `ContainerRuntimeConfig` custom resource with `defaultRuntime: runc` set, it selects `rhel-9` instead. On releases earlier than 5.0, such as 4.22, `rhel-9` is always the default regardless of runtime configuration.

- When a stream has no boot image for a given combination of a platform and an architecture, such as RHEL 10 on KubeVirt, the controller sets the `ValidPlatformImage=False` condition on the `NodePool` resource.

- When `spec.osImageStream.name` is set to `rhel-10`, the controller cannot satisfy the `runc` requirement on an RHEL 10 `NodePool` resource. The controller sets the `ValidMachineConfig=False` condition on the `NodePool` resource. The node configuration is not applied until the conflict is resolved.

On a `NodePool` resource that has `spec.osImageStream.name: rhel-10` set, if you see `ValidMachineConfig=False`, take the following steps:

1.  Identify the `ContainerRuntimeConfig` resources in the cluster by entering the following command:

    ``` terminal
    $ oc get containerruntimeconfig
    ```

2.  Review each `ContainerRuntimeConfig` for `defaultRuntime: runc` settings by entering the following command:

    ``` terminal
    $ oc get containerruntimeconfig <config_name> -o yaml
    ```

3.  Either remove the `ContainerRuntimeConfig` that specifies `runc`, or move the workloads that require `runc` to a RHEL 9 `NodePool` resource.

# Creating a NodePool with a specific RHCOS major version

Pinning the RHCOS stream at creation time gives you control over the operating system version running on your compute nodes and prevents unexpected stream transitions during future OpenShift Container Platform upgrades.

You can create a `NodePool` resource that runs RHEL 9 or RHEL 10 worker nodes by setting the `spec.osImageStream` field in the `NodePool` manifest.

If you do not set `spec.osImageStream` field, the `NodePool` resource uses the version-derived default: `rhel-9` on OpenShift Container Platform releases before 5.0, and `rhel-10` on OpenShift Container Platform 5.0 and later.

> [!IMPORTANT]
> If you change the `spec.osImageStream.name` field on an existing `NodePool`, you trigger a rolling node replacement. All nodes in the pool are reprovisioned by using the new RHCOS boot image. This results in temporary capacity reduction during the rollout.
>
> Changing `spec.osImageStream.name` from `rhel-10` to `rhel-9` on an existing `NodePool` is not supported. The API rejects the change with the following error:
>
>     OS stream downgrade from rhel-10 to rhel-9 is not allowed; create a new NodePool instead
>
> Instead, create a `NodePool` resource with `spec.osImageStream.name: rhel-9` and migrate workloads to the new pool.

<div>

<div class="title">

Prerequisites

</div>

- An OpenShift Container Platform 5.0 or later cluster running hosted control planes is available.

- The `oc` CLI is installed and configured to access the `HostedCluster` namespace.

- You have reviewed the [supported architectures and platform boot images](../hosted_control_planes/hcp-dual-stream.xml#hcp-dual-stream-arch_hcp-dual-stream) to confirm that RHEL 10 is available for your target platform and architecture.

- No `ContainerRuntimeConfig` resources in the cluster set `defaultRuntime: runc` for workloads that you intend to run on RHEL 10 nodes. For more information, see "Container runtime compatibility for RHEL 10 node pools".

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a `NodePool` manifest file, for example `nodepool.yaml`, with `spec.osImageStream.name` field set to the target RHCOS stream.

    - For RHEL 10, create a manifest file as shown in the following example:

      ``` yaml
      apiVersion: hypershift.openshift.io/v1beta1
      kind: NodePool
      metadata:
        name: <nodepool_name>
        namespace: <namespace_name>
      spec:
        clusterName: <cluster_name>
        replicas: <replica_count>
        osImageStream:
          name: rhel-10
        platform:
          type: AWS
          aws:
            instanceType: m5.xlarge
      ```

      - Replace `<nodepool_name>` with the name for the `NodePool` resource.

      - Replace `<cluster_name>` with the name of the `HostedCluster` resource that this `NodePool` resource belongs to.

      - Replace `<replica_count>` with the number of compute nodes to provision.

      - Replace `<namespace_name>` with the namespace for the `NodePool` resource. The conventional namespace for `NodePool` resources in hosted control planes is `clusters`, but `NodePool` resources can reside in other namespaces.

    - For RHEL 9, create a manifest file as shown in the following example:

      ``` yaml
      apiVersion: hypershift.openshift.io/v1beta1
      kind: NodePool
      metadata:
        name: <nodepool_name>
        namespace: <namespace_name>
      spec:
        clusterName: <cluster_name>
        replicas: <replica_count>
        osImageStream:
          name: rhel-9
        platform:
          type: AWS
          aws:
            instanceType: m5.xlarge
      ```

      - Replace `<nodepool_name>` with the name for the `NodePool` resource.

      - Replace `<cluster_name>` with the name of the `HostedCluster` resource that this `NodePool` resource belongs to.

      - Replace `<replica_count>` with the number of compute nodes to provision.

      - Replace `<namespace_name>` with the namespace for the `NodePool` resource. The conventional namespace for `NodePool` resources in hosted control planes is `clusters`, but `NodePool` resources can reside in other namespaces.

2.  Apply the `NodePool` manifest by entering the following command:

    ``` terminal
    $ oc apply -f nodepool.yaml
    ```

3.  Monitor the `NodePool` resource until the nodes reach `Ready` status by entering the following command:

    ``` terminal
    $ oc get nodepool <nodepool_name> -n <namespace> -w
    ```

    Node provisioning typically takes 5–15 minutes depending on platform. If the `NodePool` resource does not reach a ready state within 30 minutes, check events by entering `oc describe nodepool <nodepool_name> -n <namespace>`.

4.  Verify that `status.osImageStream` reflects the intended stream by entering the following command:

    ``` terminal
    $ oc get nodepool <nodepool_name> -n <namespace> -o jsonpath='{.status.osImageStream}'
    ```

    The following example shows expected output for RHEL 10:

    ``` terminal
    rhel-10
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Confirm that the `NodePool` nodes are running and that the status shows the correct RHCOS stream by entering the following command:

  ``` terminal
  $ oc get nodepool <nodepool_name> -n <namespace>
  ```

  The `READY` column shows `True` when all nodes in the pool are available.

  > [!NOTE]
  > The `spec.osImageStream` field cannot be removed from a `NodePool` spec after it has been set. If you need to use a different stream, you must create a new `NodePool` resource.

</div>

# Prerequisites to migrate workloads between RHCOS major versions

Before you migrate workloads from a RHEL 9 `NodePool` resource to a RHEL 10 `NodePool` resource in hosted control planes, verify that your environment meets the requirements. Failing to complete these checks before migration can result in workload failures, blocked drains, or compatibility issues on the new RHEL 10 nodes.

Environment requirements
- Your `HostedCluster` resource is running OpenShift Container Platform 5.0 or later.

- The `oc` CLI is installed and configured with access to the `HostedCluster` resource and its `NodePool` resources.

- You have cluster-admin or equivalent permissions on the `HostedCluster` resource.

Container runtime check
Verify that no `ContainerRuntimeConfig` resources in the cluster set `defaultRuntime: runc` for workloads targeted for RHEL 10 nodes by entering the following command:

``` terminal
$ oc get containerruntimeconfigs -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containerRuntimeConfig.defaultRuntime}{"\n"}{end}'
```

If any `ContainerRuntimeConfig` specifies `runc`, those workloads must remain on RHEL 9 `NodePool` resources. RHEL 10 does not ship `runc`. For more information, see "Container runtime compatibility for RHEL 10 node pools".

Capacity check
Confirm that the cluster has sufficient capacity to run both the existing RHEL 9 `NodePool` resource and the new RHEL 10 `NodePool` resource simultaneously during migration. The side-by-side migration strategy requires both `NodePool` resources to be active at the same time. Plan for the additional resource usage before starting the migration.

PodDisruptionBudget review
Review `PodDisruptionBudget` (PDB) resources in the namespaces that contain workloads running on the RHEL 9 `NodePool` resource by entering the following command:

``` terminal
$ oc get poddisruptionbudget -A
```

PDBs that set `maxUnavailable: 0` or `minAvailable` equal to the total number of pod replicas block the drain operation. Either temporarily adjust the PDB during the migration window, or scale up the workload replica count before draining so that the PDB constraints can be satisfied.

Architecture and platform check
Confirm that RHEL 10 boot images are available for the target platform and architecture. For more information, see the "Platform availability gaps" section in "Supported architectures for RHEL 10 NodePool resources".

FIPS check
If FIPS mode is enabled on the `HostedCluster` resource, verify that your architecture supports FIPS on RHEL 10. FIPS is supported on RHEL 10 for x86_64, ppc64le, and s390x architectures only.

If your `NodePool` resource uses aarch64, you must keep it on RHEL 9 if FIPS compliance is required.

# Migrating workloads between RHCOS major versions in hosted control planes

You can migrate workloads from a RHEL 9 `NodePool` resource to a RHEL 10 `NodePool` resource within the same `HostedCluster` resource by using the side-by-side `NodePool` resource strategy.

This approach runs both `NodePool` resources simultaneously, drains the old `NodePool` resource to move workloads, and then removes the old `NodePool` resource.

This procedure covers the `Replace` upgrade strategy, which is the default for cloud-based `NodePool` resources. For `NodePool` resources that use the `InPlace` upgrade strategy, typically on bare metal or on-premise deployments, draining is managed by an in-place upgrade tool that applies drain-and-reboot to each node.

In-place rollback from RHEL 10 to RHEL 9 on a `NodePool` resource is not supported and is permanently blocked by API validation. If you need to return workloads to RHEL 9 after they are running on RHEL 10 nodes, create a `NodePool` resource with `spec.osImageStream.name: rhel-9` and follow the same side-by-side migration procedure.

> [!IMPORTANT]
> Workloads that require the `runc` container runtime must remain on RHEL 9 `NodePool` resources and cannot be migrated to RHEL 10 `NodePool` resources. RHEL 10 does not include `runc`. Migrating workloads that depend on `runc` to a RHEL 10 `NodePool` resource causes the `ValidMachineConfig=False` condition to be set on the NodePool.

<div>

<div class="title">

Prerequisites

</div>

- Your `HostedCluster` resource is running OpenShift Container Platform 5.0 or later.

- No `ContainerRuntimeConfig` resources set `defaultRuntime: runc` for workloads you intend to migrate.

- The cluster has enough capacity to run both the existing RHEL 9 `NodePool` resource and the new RHEL 10 `NodePool` resource simultaneously.

- You have reviewed `PodDisruptionBudget` (PDB) resources in affected namespaces and confirmed that PDB constraints will not permanently block the drain.

- The target platform and architecture support RHEL 10 boot images. For more information, see "Supported architectures for RHEL 10 `NodePool` resources".

</div>

For a full pre-migration checklist, see "Prerequisites for migrating workloads between RHCOS major versions".

<div>

<div class="title">

Procedure

</div>

1.  Complete the following steps on the management cluster:

    1.  Identify the name of the existing RHEL 9 `NodePool` resource and note the namespace by entering the following command:

        ``` terminal
        $ oc get nodepool -n clusters
        ```

    2.  Create a `NodePool` resource manifest file, for example `rhel10-nodepool.yaml`, with `spec.osImageStream.name` set to `rhel-10`, as shown in the following example:

        ``` yaml
        apiVersion: hypershift.openshift.io/v1beta1
        kind: NodePool
        metadata:
          name: <new_nodepool_name>
          namespace: clusters
        spec:
          clusterName: <cluster_name>
          replicas: <replica_count>
          osImageStream:
            name: rhel-10
          platform:
            type: AWS
            aws:
              instanceType: m5.xlarge
        ```

        - Replace `<new_nodepool_name>` with the name for the new RHEL 10 `NodePool` resource.

        - Replace `<cluster_name>` with the name of the `HostedCluster` resource.

        - Replace `<replica_count>` with the number of compute nodes. Match or exceed the replica count of the old `NodePool` resource to maintain workload capacity during migration.

    3.  Apply the new `NodePool` manifest by entering the following command:

        ``` terminal
        $ oc apply -f rhel10-nodepool.yaml
        ```

    4.  Wait for all nodes in the new RHEL 10 `NodePool` resource to reach `Ready` status before proceeding by entering the following command:

        ``` terminal
        $ oc get nodepool <new_nodepool_name> -n clusters -w
        ```

        Node provisioning typically takes 5–15 minutes depending on platform. If the `NodePool` resource does not reach a ready state within 30 minutes, check events by entering `oc describe nodepool <new_nodepool_name> -n clusters`.

    5.  Verify that `status.osImageStream` on the new `NodePool` resource shows `rhel-10` by entering the following command:

        ``` terminal
        $ oc get nodepool <new_nodepool_name> -n clusters -o jsonpath='{.status.osImageStream}'
        ```

        The expected output is as follows:

        ``` terminal
        rhel-10
        ```

2.  Complete the following steps on the hosted cluster:

    1.  Cordon all nodes in the old RHEL 9 `NodePool` resource to prevent new workloads from being scheduled on them. List the nodes associated with the old `NodePool` resource by entering the following command:

        ``` terminal
        $ oc get nodes -l hypershift.openshift.io/nodePool=<old_nodepool_name>
        ```

        Cordon all nodes at once by entering the following command:

        ``` terminal
        $ for node in $(oc get nodes -l hypershift.openshift.io/nodePool=<old_nodepool_name> -o name); do oc adm cordon "$node"; done
        ```

    2.  Drain all nodes in the old RHEL 9 `NodePool` resource to evict workloads by entering the following command:

        ``` terminal
        $ for node in $(oc get nodes -l hypershift.openshift.io/nodePool=<old_nodepool_name> -o name); do oc adm drain "$node" --ignore-daemonsets --delete-emptydir-data; done
        ```

        > [!NOTE]
        > If a PDB blocks the drain, the command pauses and reports which pods cannot be evicted. Resolve the PDB constraint before continuing. You might need to temporarily scale up the affected workload or adjust the PDB during the migration window.

    3.  Verify that the workloads have moved to nodes in the new RHEL 10 `NodePool` resource.

        1.  List the nodes in the new `NodePool` resource by entering the following command:

            ``` terminal
            $ oc get nodes -l hypershift.openshift.io/nodePool=<new_nodepool_name>
            ```

        2.  List all pods and confirm they are running on the new RHEL 10 nodes by entering the following command:

            ``` terminal
            $ oc get pods -A -o wide
            ```

            Confirm that pods formerly running on RHEL 9 nodes now show RHEL 10 node names in the `NODE` column and are in `Running` status.

3.  On the management cluster, delete the old RHEL 9 `NodePool` resource after confirming that all workloads are running successfully on RHEL 10 nodes by entering the following command:

    ``` terminal
    $ oc delete nodepool <old_nodepool_name> -n clusters
    ```

</div>

<div>

<div class="title">

Verification

</div>

1.  On the management cluster, confirm that the old `NodePool` resource no longer exists by entering the following command:

    ``` terminal
    $ oc get nodepool -n clusters
    ```

    Ensure the old `NodePool` resource name is not in the output.

2.  On the hosted cluster, confirm that all workloads are running on RHEL 10 nodes by entering the following command:

    ``` terminal
    $ oc get nodes -l hypershift.openshift.io/nodePool=<new_nodepool_name>
    ```

    Ensure all nodes show `Ready` status with no taints from the drain operation.

</div>
