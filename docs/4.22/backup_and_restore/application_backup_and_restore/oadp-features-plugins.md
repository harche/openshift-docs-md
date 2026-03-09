OpenShift API for Data Protection (OADP) features provide options for backing up and restoring applications.

The default plugins enable Velero to integrate with certain cloud providers and to back up and restore OpenShift Container Platform resources.

# OADP features

OpenShift API for Data Protection (OADP) supports the following features:

Backup
You can use OADP to back up all applications on the OpenShift Platform, or you can filter the resources by type, namespace, or label.

OADP backs up Kubernetes objects and internal images by saving them as an archive file on object storage. OADP backs up persistent volumes (PVs) by creating snapshots with the native cloud snapshot API or with the Container Storage Interface (CSI). For cloud providers that do not support snapshots, OADP backs up resources and PV data with Restic.

<div class="note">

You must exclude Operators from the backup of an application for backup and restore to succeed.

</div>

Restore
You can restore resources and PVs from a backup. You can restore all objects in a backup or filter the objects by namespace, PV, or label.

<div class="note">

You must exclude Operators from the backup of an application for backup and restore to succeed.

</div>

Schedule
You can schedule backups at specified intervals.

Hooks
You can use hooks to run commands in a container on a pod, for example, `fsfreeze` to freeze a file system. You can configure a hook to run before or after a backup or restore. Restore hooks can run in an init container or in the application container.

# OADP plugins

The OpenShift API for Data Protection (OADP) provides default Velero plugins that are integrated with storage providers to support backup and snapshot operations. You can create [custom plugins](https://velero.io/docs/v1.16/custom-plugins/) based on the Velero plugins.

OADP also provides plugins for OpenShift Container Platform resource backups, OpenShift Virtualization resource backups, and Container Storage Interface (CSI) snapshots.

| OADP plugin                                   | Function                                                                       | Storage location                          |
|-----------------------------------------------|--------------------------------------------------------------------------------|-------------------------------------------|
| `aws`                                         | Backs up and restores Kubernetes objects.                                      | AWS S3                                    |
| Backs up and restores volumes with snapshots. | AWS EBS                                                                        |                                           |
| `azure`                                       | Backs up and restores Kubernetes objects.                                      | Microsoft Azure Blob storage              |
| Backs up and restores volumes with snapshots. | Microsoft Azure Managed Disks                                                  |                                           |
| `gcp`                                         | Backs up and restores Kubernetes objects.                                      | Google Cloud Storage                      |
| Backs up and restores volumes with snapshots. | Google Compute Engine Disks                                                    |                                           |
| `openshift`                                   | Backs up and restores OpenShift Container Platform resources. <sup>\[1\]</sup> | Object store                              |
| `kubevirt`                                    | Backs up and restores OpenShift Virtualization resources. <sup>\[2\]</sup>     | Object store                              |
| `csi`                                         | Backs up and restores volumes with CSI snapshots. <sup>\[3\]</sup>             | Cloud storage that supports CSI snapshots |
| `hypershift`                                  | Backs up and restores HyperShift hosted cluster resources. <sup>\[4\]</sup>    | Object store                              |

OADP plugins

1.  Mandatory.

2.  Virtual machine disks are backed up with CSI snapshots or Restic.

3.  The `csi` plugin uses the Kubernetes CSI snapshot API.

    - OADP 1.1 or later uses `snapshot.storage.k8s.io/v1`

    - OADP 1.0 uses `snapshot.storage.k8s.io/v1beta1`

4.  Do not add the `hypershift` plugin in the `DataProtectionApplication` custom resource if the cluster is not a HyperShift hosted cluster.

# About OADP Velero plugins

You can configure two types of plugins when you install Velero:

- Default cloud provider plugins

- Custom plugins

Both types of plugin are optional, but most users configure at least one cloud provider plugin.

## Default Velero cloud provider plugins

You can install any of the following default Velero cloud provider plugins when you configure the `oadp_v1alpha1_dpa.yaml` file during deployment:

- `aws` (Amazon Web Services)

- `gcp` (Google Cloud)

- `azure` (Microsoft Azure)

- `openshift` (OpenShift Velero plugin)

- `csi` (Container Storage Interface)

- `kubevirt` (KubeVirt)

You specify the desired default plugins in the `oadp_v1alpha1_dpa.yaml` file during deployment.

<div class="formalpara-title">

**Example file**

</div>

The following `.yaml` file installs the `openshift`, `aws`, `azure`, and `gcp` plugins:

``` yaml
 apiVersion: oadp.openshift.io/v1alpha1
 kind: DataProtectionApplication
 metadata:
   name: dpa-sample
 spec:
   configuration:
     velero:
       defaultPlugins:
       - openshift
       - aws
       - azure
       - gcp
```

## Custom Velero plugins

You can install a custom Velero plugin by specifying the plugin `image` and `name` when you configure the `oadp_v1alpha1_dpa.yaml` file during deployment.

You specify the desired custom plugins in the `oadp_v1alpha1_dpa.yaml` file during deployment.

<div class="formalpara-title">

**Example file**

</div>

The following `.yaml` file installs the default `openshift`, `azure`, and `gcp` plugins and a custom plugin that has the name `custom-plugin-example` and the image `quay.io/example-repo/custom-velero-plugin`:

``` yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
 name: dpa-sample
spec:
 configuration:
   velero:
     defaultPlugins:
     - openshift
     - azure
     - gcp
     customPlugins:
     - name: custom-plugin-example
       image: quay.io/example-repo/custom-velero-plugin
```

# Supported architectures for OADP

OpenShift API for Data Protection (OADP) supports the following architectures:

- AMD64

- ARM64

- PPC64le

- s390x

<div class="note">

OADP 1.2.0 and later versions support the ARM64 architecture.

</div>

# OADP support for IBM Power and IBM Z

OpenShift API for Data Protection (OADP) is platform neutral. The information that follows relates only to IBM Power® and to IBM Z®.

- OADP 1.3.6 was tested successfully against OpenShift Container Platform 4.12, 4.13, 4.14, and 4.15 for both IBM Power® and IBM Z®. The sections that follow give testing and support information for OADP 1.3.6 in terms of backup locations for these systems.

- OADP 1.4.6 was tested successfully against OpenShift Container Platform 4.14, 4.15, 4.16, and 4.17 for both IBM Power® and IBM Z®. The sections that follow give testing and support information for OADP 1.4.6 in terms of backup locations for these systems.

- OADP 1.5.4 was tested successfully against OpenShift Container Platform 4.19 for both IBM Power® and IBM Z®. The sections that follow give testing and support information for OADP 1.5.4 in terms of backup locations for these systems.

## OADP support for target backup locations using IBM Power

- IBM Power® running with OpenShift Container Platform 4.12, 4.13, 4.14, and 4.15, and OADP 1.3.6 was tested successfully against an AWS S3 backup location target. Although the test involved only an AWS S3 target, Red Hat supports running IBM Power® with OpenShift Container Platform 4.13, 4.14, and 4.15, and OADP 1.3.6 against all S3 backup location targets, which are not AWS, as well.

- IBM Power® running with OpenShift Container Platform 4.14, 4.15, 4.16, and 4.17, and OADP 1.4.6 was tested successfully against an AWS S3 backup location target. Although the test involved only an AWS S3 target, Red Hat supports running IBM Power® with OpenShift Container Platform 4.14, 4.15, 4.16, and 4.17, and OADP 1.4.6 against all S3 backup location targets, which are not AWS, as well.

- IBM Power® running with OpenShift Container Platform 4.19 and OADP 1.5.4 was tested successfully against an AWS S3 backup location target. Although the test involved only an AWS S3 target, Red Hat supports running IBM Power® with OpenShift Container Platform 4.19 and OADP 1.5.4 against all S3 backup location targets, which are not AWS, as well.

## OADP testing and support for target backup locations using IBM Z

- IBM Z® running with OpenShift Container Platform 4.12, 4.13, 4.14, and 4.15, and 1.3.6 was tested successfully against an AWS S3 backup location target. Although the test involved only an AWS S3 target, Red Hat supports running IBM Z® with OpenShift Container Platform 4.13 4.14, and 4.15, and 1.3.6 against all S3 backup location targets, which are not AWS, as well.

- IBM Z® running with OpenShift Container Platform 4.14, 4.15, 4.16, and 4.17, and 1.4.6 was tested successfully against an AWS S3 backup location target. Although the test involved only an AWS S3 target, Red Hat supports running IBM Z® with OpenShift Container Platform 4.14, 4.15, 4.16, and 4.17, and 1.4.6 against all S3 backup location targets, which are not AWS, as well.

- IBM Z® running with OpenShift Container Platform 4.19 and OADP 1.5.4 was tested successfully against an AWS S3 backup location target. Although the test involved only an AWS S3 target, Red Hat supports running IBM Z® with OpenShift Container Platform 4.19 and OADP 1.5.4 against all S3 backup location targets, which are not AWS, as well.

### Known issue of OADP using IBM Power® and IBM Z® platforms

- Currently, there are backup method restrictions for Single-node OpenShift clusters deployed on IBM Power® and IBM Z® platforms. Only NFS storage is currently compatible with Single-node OpenShift clusters on these platforms. In addition, only the File System Backup (FSB) methods such as Kopia and Restic are supported for backup and restore operations. There is currently no workaround for this issue.

# OADP and FIPS

Federal Information Processing Standards (FIPS) are a set of computer security standards developed by the United States federal government in line with the Federal Information Security Management Act (FISMA).

OpenShift API for Data Protection (OADP) has been tested and works on FIPS-enabled OpenShift Container Platform clusters.

# Avoiding the Velero plugin panic error

Label a custom Backup Storage Location (BSL) to resolve Velero plugin panic errors during `imagestream` backups. This action prompts the OADP controller to create the required registry secret when you manage the BSL outside the `DataProtectionApplication` (DPA) custom resource (CR).

A missing secret can cause a panic error for the Velero plugin during image stream backups. When the backup and the BSL are managed outside the scope of the DPA, the OADP controller does not create the relevant `oadp-<bsl_name>-<bsl_provider>-registry-secret` parameter.

During the backup operation, the OpenShift Velero plugin panics on the `imagestream` backup, with the following panic error:

``` text
024-02-27T10:46:50.028951744Z time="2024-02-27T10:46:50Z" level=error msg="Error backing up item"
backup=openshift-adp/<backup name> error="error executing custom action (groupResource=imagestreams.image.openshift.io,
namespace=<BSL Name>, name=postgres): rpc error: code = Aborted desc = plugin panicked:
runtime error: index out of range with length 1, stack trace: goroutine 94…
```

1.  Label the custom BSL with the relevant label by using the following command:

    ``` terminal
    $ oc label backupstoragelocations.velero.io <bsl_name> app.kubernetes.io/component=bsl
    ```

2.  After the BSL is labeled, wait until the DPA reconciles.

    <div class="note">

    You can force the reconciliation by making any minor change to the DPA itself.

    </div>

- After the DPA is reconciled, confirm that the parameter has been created and that the correct registry data has been populated into it by entering the following command:

  ``` terminal
  $ oc -n openshift-adp get secret/oadp-<bsl_name>-<bsl_provider>-registry-secret -o json | jq -r '.data'
  ```

# Workaround for OpenShift ADP Controller segmentation fault

Define either `velero` or `cloudstorage` in your Data Protection Application (DPA) configuration to prevent indefinite pod crashes. This configuration resolves a segmentation fault in the `openshift-adp-controller-manager` pod that occurs when both components are enabled.

Define either `velero` or `cloudstorage` when you configure a DPA. Otherwise, the `openshift-adp-controller-manager` pod fails with a crash loop segmentation fault due to the following settings:

- If you define both `velero` and `cloudstorage`, the `openshift-adp-controller-manager` fails.

- If you do not define both `velero` and `cloudstorage`, the `openshift-adp-controller-manager` fails.

For more information about this issue, see [OADP-1054](https://issues.redhat.com/browse/OADP-1054).
