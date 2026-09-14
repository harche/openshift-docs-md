To reduce application startup time, make your applications run more efficiently, and configure lazy pulling, you can configure additional storage locations for the CRI-O container engine to store OCI objects.

Fields in the `ContainerRuntimeConfig` custom resource (CR) let you specify where CRI-O stores and resolves container image layers, complete container images, and OCI artifacts.

# About additional CRI-O storage locations

To reduce application startup time and make your applications run more efficiently, you can configure additional storage locations for the CRI-O container engine.

By using storage locations for the CRI-O container engine other than the default you gain control over where CRI-O stores and retrieves OCI artifacts, complete container images, and container image layers. Using additional storage locations for these CRI-O objects can reduce application startup time and make your applications run more efficiently through dedicated solid-state drive (SSD) storage, shared image caches, or lazy pulling.

By default, CRI-O stores all container data under a single root directory, `/var/lib/containers/storage`. This works well for typical workloads, but can create problems in clusters that use large images or artifacts, such as artificial intelligence and machine learning (AI/ML) workloads.

For example, large OCI artifacts, such as machine learning models, are stored in the default location, consuming space and preventing the use of faster dedicated storage. By configuring the `additionalArtifactStores` field, you can store large AI/ML models on high-performance solid-state drives (SSD) separate from the root file system. As a result, your workloads can experience faster start times and your clusters can use storage more efficiently.

Also, you could use the `additionalImageStores` field to mount an NFS share with prepopulated images across all worker nodes. Nodes read from the shared cache instead of pulling from an external registry. This is useful in disconnected environments or when many nodes run the same workloads.

With the `additionalLayerStores` field, you could enable lazy pulling through a third-party storage plugin, such as stargz-store. With lazy pulling, containers start after downloading only the required file chunks. The remaining data is fetched during runtime.

After you configure any of these new storage locations, the Machine Config Operator (MCO) reboots the affected nodes with the new configuration. After the reboot, CRI-O begins resolving storage from the additional locations.

Additional storage for OCI artifacts
Use the `additionalArtifactStores` field in a container runtime config to specify read-only locations where CRI-O resolves OCI artifacts, such as machine learning models pulled as OCI volume images. CRI-O checks these locations in order before falling back to the default storage location. CRI-O requires an existing, prepopulated `artifacts/` subdirectory within each configured path. For example, if the path is `/mnt/ssd-artifacts`, place the artifacts in the `/mnt/ssd-artifacts/artifacts/` directory.

The following example container runtime config configures storage for OCI artifacts.

``` yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
  name: ssd-artifact-stores
spec:
  machineConfigPoolSelector:
    matchLabels:
      pools.operator.machineconfiguration.openshift.io/worker: ""
  containerRuntimeConfig:
    additionalArtifactStores:
      - path: /mnt/ssd-artifacts
      - path: /mnt/nfs-shared-artifacts
```

When you create the container runtime config, the Machine Config Operator (MCO) writes the configuration to the `/etc/crio/crio.conf.d/01-ctrcfg-additionalArtifactStores` file on the target nodes.

Additional storage for container images
Use the `additionalImageStores` field to specify read-only container image caches on shared or high-performance storage. When CRI-O needs an image, it checks the additional image stores first. If the image exists there, no registry pull happens.

The following example container runtime config configures storage for container images.

``` yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
  name: shared-image-cache
spec:
  machineConfigPoolSelector:
    matchLabels:
      pools.operator.machineconfiguration.openshift.io/worker: ""
  containerRuntimeConfig:
    additionalImageStores:
      - path: /mnt/nfs-image-cache
      - path: /mnt/ssd-images
```

When you create the container runtime config, the Machine Config Operator (MCO) writes the configuration to the `/etc/containers/storage.conf` file on the target nodes.

Additional container image layers for lazy pulling
Use the `additionalLayerStores` field to enable lazy pulling through a third-party Bring Your Own Storage (BYOS) plugin. With lazy pulling, you can start a container without waiting for the entire image to be downloaded. Instead, the necessary parts of the image are fetched on-demand during runtime using FUSE.

External BYOS plugins, such as stargz-snapshotter and nydus-storage-plugin, serve container image layers on-demand through a FUSE file system. The `additionalLayerStores` field configures the FUSE mount paths for CRI-O.

When CRI-O needs an image, it accesses the plugin’s FUSE file system, triggering metadata download and lazy pulling. The container starts after downloading only the required chunks.

<div class="note">

If you are using the Linux native zstd:chunked format for partial pulling, you do not need to configure the `additionalLayerStores` field. With partial pulling, CRI-O retrieves the chunk metadata, determines which chunks are needed, and fetches only those chunks by using HTTP range requests rather than downloading the entire compressed layer.

</div>

To use lazy pulling, you must install a BYOS plugin on your nodes. Then, create a container runtime config to configure the FUSE mount paths.

The following example container runtime config configures container image layers for lazy pulling.

``` yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
  name: lazy-pulling
spec:
  machineConfigPoolSelector:
    matchLabels:
      pools.operator.machineconfiguration.openshift.io/worker: ""
  containerRuntimeConfig:
    additionalLayerStores:
      - path: /var/lib/stargz-store
```

When you create the container runtime config, the Machine Config Operator (MCO) writes the configuration to the `/etc/containers/storage.conf` file on the target nodes.

## Limitations and known issues with additional CRI-O storage locations

When working with additional CRI-O storage locations, make note of the limitations and known issues that could affect your cluster.

The following limitations and known issues have been identified for additional CRI-O storage:

- Lazy pulling and partial pulling rely on HTTP range requests. As such, your registry must support HTTP range requests. If not supported, CRI-O falls back to standard image pulls.

- When using an additional layer store for Bring Your Own Storage (BYOS) lazy pulling, you must convert the pulled container images from the standard OCI format to a compatible format, such as the eStargz or Nydus formats.

- The zstd:chunked format performs *partial pulling*, where CRI-O fetches only the missing chunks before the container starts, skipping content already present from prior pulls. Partial pulling does not use the `additionalLayerStores` field.

- After you configure additional CRI-O storage, the Machine Config Operator (MCO) reboots the affected nodes with the new configuration.

- Container creation can be impacted if your storage plugin crashes or hangs. For more information, see "Troubleshoot additional CRI-O storage locations".

- The additional layer store API is experimental in the upstream containers/storage project. Breaking changes are possible.

- Multiple `ContainerRuntimeConfig` resources affecting the same configuration file might result in only a subset of the changes taking effect.

- This feature is not supported for Red Hat build of MicroShift (MicroShift), which does not use the MCO.

- If you need to downgrade your cluster to OpenShift Container Platform version 4.21 or earlier, before you downgrade, delete any `ContainerRuntimeConfig` resource that includes the `additionalArtifactStores`, `additionalImageStores`, or `additionalLayerStores` fields.

<!-- -->

- [Troubleshoot additional CRI-O storage locations](../../nodes/nodes/nodes-nodes-additional-crio-storage.xml#nodes-nodes-additional-crio-storage-troubleshooting_nodes-nodes-additional-crio-storage)

# Configuring additional CRI-O storage locations

To reduce application startup time and make your applications run more efficiently, you can configure additional storage locations for the CRI-O container engine by using the `ContainerRuntimeConfig` custom resource (CR).

Use the `additionalArtifactStores`, `additionalImageStores`, and `additionalLayerStores` fields in a `ContainerRuntimeConfig` to specify read-only locations where CRI-O stores and resolves OCI artifacts, container images, or container image layers. CRI-O checks these locations in order before falling back to the default storage location.

<div class="important">

When using multiple `ContainerRuntimeConfig` resources, merge all additional storage configurations into a single `ContainerRuntimeConfig` for each machine config pool. Multiple `ContainerRuntimeConfig` resources affecting the same configuration file might result in only a subset of the changes taking effect.

</div>

- If you are configuring the `additionalImageStores` or `additionalLayerStores` field, the target storage paths must exist and be accessible on the nodes and the container image or layers must be present in the directory. For network storage, ensure the paths are mounted before applying the configuration.

- If you are configuring the `additionalLayerStores` field, you must meet the following additional prerequisites:

  - You must install a supported storage plugin binary on each node, such as Stargz Store or Nydus Storage Plugin. You must install the plugin by using one of the following methods:

    - Use a daemon set to run the plugin as a privileged container.

    - Use a machine config to install the binary and configure it as a systemd service.

    - Use Image mode for OpenShift to install the plugin in a custom RHCOS image.

  - You converted the container images to a lazy-pull-compatible format, such as eStargz or Nydus. See "eStargz format" or "Nydus format" for more information.

  - Your container registry must support HTTP range requests.

1.  Create a YAML file for the `ContainerRuntimeConfig` CR similar to the following example:

    ``` yaml
    apiVersion: machineconfiguration.openshift.io/v1
    kind: ContainerRuntimeConfig
    metadata:
      name: crio-additional-stores
    spec:
      machineConfigPoolSelector:
        matchLabels:
          pools.operator.machineconfiguration.openshift.io/worker: ""
      containerRuntimeConfig:
        additionalArtifactStores:
          - path: /mnt/ssd-artifacts
          - path: /mnt/nfs-shared-artifacts
        additionalImageStores:
          - path: /mnt/nfs-image-cache
          - path: /mnt/ssd-images
        additionalLayerStores:
          - path: /var/lib/stargz-store
    ```

    where:

    `spec.machineConfigPoolSelector.matchLabels`
    Specifies a label associated with the nodes that you want to update.

    `spec.containerRuntimeConfig.additionalArtifactStores.path`
    Optional: Specifies the path to the directory that contains OCI artifacts. CRI-O searches for content in an `artifacts/` subdirectory within this path. You can specify up to 10 directories.

    `spec.containerRuntimeConfig.additionalImageStores.path`
    Optional: Specifies the path to an NFS share or other location that contains pre-populated container images. You can specify up to 10 directories.

    `spec.containerRuntimeConfig.additionalLayerStores.path`
    Optional: Specifies the path to the directory that contains lazy-pull-compatible-formatted container image layers. You can specify up to 5 directories.

    The specified path must meet the following criteria:

    - Contains between 1 and 256 characters

    - Is an absolute path, starting with the `/` character

    - Contains only alphanumeric characters: `a-z`, `A-Z`, `0-9`, `/`, `.`, `_`, and `-`

    - Cannot contain consecutive forward slashes

    You can configure any combination of these three additional CRI-O storage locations.

    For a layer store, the MCO automatically appends the `:ref` suffix to the path when writing to the `storage.conf` file. This suffix switches the container storage library from storing actual image layers (blobs) to storing references (pointers) to where those layers can be found, which is required for the lazy-pulling plugins. You do not need to include the suffix in the `ContainerRuntimeConfig` path.

    <div class="note">

    If a path does not exist or is inaccessible at runtime, CRI-O generates a warning and continues with the remaining stores. The default storage location is always used as a fallback.

    </div>

2.  Create the `ContainerRuntimeConfig` CR by running the following command:

    ``` terminal
    $ oc create -f <container_runtime_config>.yaml
    ```

    Replace `<container_runtime_config>` with the name of the YAML file.

    After you configure any of these new storage locations, the Machine Config Operator (MCO) reboots the affected nodes with the new configuration.

<!-- -->

1.  After the nodes have returned to the `Ready` status, check that the new stores have been added to the node configuration:

    1.  Start a debug pod by running the following command:

        ``` terminal
        $ oc debug node/<node_name>
        ```

        where `<node_name>` specifies the name of one of the nodes in the affected machine config pool.

    2.  Set `/host` as the root directory within the debug shell by running the following command:

        ``` terminal
        sh-5.1# chroot /host
        ```

        - For an artifact store, review the contents of the `/etc/crio/crio.conf.d/01-ctrcfg-additionalArtifactStores` file by running the following command:

          ``` terminal
          sh-5.1# cat /etc/crio/crio.conf.d/01-ctrcfg-additionalArtifactStores
          ```

          <div class="formalpara-title">

          **Example output**

          </div>

          ``` terminal
          [crio]
            [crio.runtime]
              additional_artifact_stores = ["/mnt/ssd-artifacts", "/mnt/nfs-shared-artifacts"]
          ```

        - For an image store, review the contents of the `/etc/containers/storage.conf` file by running the following command:

          ``` terminal
          sh-5.1# cat /etc/containers/storage.conf
          ```

          <div class="formalpara-title">

          **Example output**

          </div>

          ``` terminal
          [storage]
            [storage.options]
             additionalimagestores = ["/mnt/nfs-image-cache", "/mnt/ssd-images"]
          ```

        - For a layer store, review the contents of the `/etc/containers/storage.conf` file by running the following command:

          ``` terminal
          sh-5.1# cat /etc/containers/storage.conf
          ```

          <div class="formalpara-title">

          **Example output**

          </div>

          ``` terminal
          [storage]
            [storage.options]
             additionallayerstores = ["/var/lib/stargz-store:ref"]
          ```

# Troubleshoot additional CRI-O storage locations

You can troubleshoot some known issues with the additional CRI-O storage.

FUSE plugin crash or hang impact and recovery
If a FUSE-backed additional layer store plugin crashes, containers using layers from that store get fast-fail ENOTCONN errors. Other containers are unaffected. If a plugin hangs, CRI-O can stall node-wide due to lock contention. No timeout or circuit-breaker exists.

To recover from this condition, restart the `DaemonSet` plugin. If CRI-O is stalled, also drain and reboot the node.

You can avoid this condition by setting a non-zero `PullProgressTimeout` value in CRI-O when additional layer stores are configured. You can set the `pull_progress_timeout` value by using a `MachineConfig` object under `/etc/crio/crio.conf.d/`. You cannot set the `pull_progress_timeout` value by using a `ContainerRuntimeConfig` object. For more information, see the "Failed to pull image due to `pull_progress_timeout` value is too small" Red Hat Knowledgebase article.

Trust model for additional layer store content
For pre-populated additional layer stores, content integrity relies entirely on the FUSE plugin.

Pre-populated additional layer stores are trusted without content verification. No digest or checksum is checked on the info, blob, or diff files. A compromised FUSE plugin can serve arbitrary file content to containers. This is inherent to the trust model, because the plugin runs with full node access.

To ensure verification, use zstd:chunked format image pulls, which verifies individual chunks by using SHA-256.

It can be additionally helpful to run the Linux fs-verity utility on the additional layer store content where supported.

composefs silent integrity degradation
The composefs code path does not report ENOTSUP or ENOTTY errors from the `EnableVerity` command. As a result, you can use composefs blobs without integrity verification, and you will receive no warning. This is an inherent composefs behavior that you cannot work around.

fsverity enforcement is conditional
To ensure image verification, note that zstd:chunked image pulls enforce the Linux fs-verity integrity checks only when the `DifferFsVerityRequired` mode is set in the Linux fs-verity tool. If not set, the enforcement of fs-verity operates on a best-effort basis. Full integrity verification requires an fs-verity-capable file system and explicit `DifferFsVerityRequired` configuration.

# Additional resources

- [Stargz Store plugin](https://github.com/containerd/stargz-snapshotter)

- [Install Stargz Snapshotter and Stargz Store](https://github.com/containerd/stargz-snapshotter/blob/main/docs/INSTALL.md)

- [Nydus Storage Plugin](https://github.com/containers/nydus-storage-plugin)

- [eStargz format](https://github.com/containerd/stargz-snapshotter/blob/main/docs/estargz.md)

- [Nydus format](https://nydus.dev/)

- [Troubleshoot additional CRI-O storage locations](../../nodes/nodes/nodes-nodes-additional-crio-storage.xml#nodes-nodes-additional-crio-storage-troubleshooting_nodes-nodes-additional-crio-storage)

- [Running background tasks on nodes automatically with daemon sets](../../nodes/jobs/nodes-pods-daemonsets.xml#nodes-pods-daemonsets)

- [Using machine config objects to configure nodes](../../machine_configuration/machine-configs-configure.xml#machine-configs-configure)

- [Image mode for OpenShift](../../machine_configuration/mco-coreos-layering.xml#mco-coreos-layering)

- [Failed to pull image due to `pull_progress_timeout` value is too small (Red Hat Knowledgebase article)](https://access.redhat.com/solutions/7127369)
