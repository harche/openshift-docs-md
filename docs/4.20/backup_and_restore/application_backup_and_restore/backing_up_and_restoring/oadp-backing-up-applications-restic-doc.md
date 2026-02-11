You can use OADP to back up and restore Kubernetes volumes attached to pods from the file system of the volumes. This process is called File System Backup (FSB) or Pod Volume Backup (PVB). It is accomplished by using modules from the open source backup tools Restic or Kopia.

If your cloud provider does not support snapshots or if your applications are on NFS data volumes, you can create backups by using FSB.

> [!NOTE]
> [Restic](https://restic.net/) is installed by the OADP Operator by default. If you prefer, you can install [Kopia](https://kopia.io/) instead.

FSB integration with OADP provides a solution for backing up and restoring almost any type of Kubernetes volumes. This integration is an additional capability of OADP and is not a replacement for existing functionality.

You back up Kubernetes resources, internal images, and persistent volumes with Kopia or Restic by editing the `Backup` custom resource (CR).

You do not need to specify a snapshot location in the `DataProtectionApplication` CR.

> [!NOTE]
> In OADP version 1.3 and later, you can use either Kopia or Restic for backing up applications.
>
> For the Built-in DataMover, you must use Kopia.
>
> In OADP version 1.2 and earlier, you can only use Restic for backing up applications.

> [!IMPORTANT]
> FSB does not support backing up `hostPath` volumes. For more information, see [FSB limitations](https://velero.io/docs/v1.12/file-system-backup/#limitations).

> [!IMPORTANT]
> The `…​/.snapshot` directory is a snapshot copy directory, which is used by several NFS servers. This directory has read-only access by default, so Velero cannot restore to this directory.
>
> Do not give Velero write access to the `.snapshot` directory, and disable client access to this directory.
>
> <div>
>
> <div class="title">
>
> Additional resources
>
> </div>
>
> - [Enable or disable client access to Snapshot copy directory by editing a share](https://docs.netapp.com/us-en/ontap/enable-snapshot-dir-access-task.html#enable-or-disable-client-access-to-snapshot-copy-directory-by-editing-a-share)
>
> - [Prerequisites for backup and restore with FlashBlade](https://docs.portworx.com/portworx-backup-on-prem/reference/restore-with-fb#prerequisites-for-backup-and-restore-with-flashblade)
>
> </div>

# Backing up applications with File System Backup

<div>

<div class="title">

Prerequisites

</div>

- You must install the OpenShift API for Data Protection (OADP) Operator.

- You must not disable the default `nodeAgent` installation by setting `spec.configuration.nodeAgent.enable` to `false` in the `DataProtectionApplication` CR.

- You must select Kopia or Restic as the uploader by setting `spec.configuration.nodeAgent.uploaderType` to `kopia` or `restic` in the `DataProtectionApplication` CR.

- The `DataProtectionApplication` CR must be in a `Ready` state.

</div>

<div>

<div class="title">

Procedure

</div>

- Create the `Backup` CR, as in the following example:

  ``` yaml
  apiVersion: velero.io/v1
  kind: Backup
  metadata:
    name: <backup>
    labels:
      velero.io/storage-location: default
    namespace: openshift-adp
  spec:
    defaultVolumesToFsBackup: true
  ...
  ```

  - In OADP version 1.2 and later, add the `defaultVolumesToFsBackup: true` setting within the `spec` block. In OADP version 1.1, add `defaultVolumesToRestic: true`.

</div>
