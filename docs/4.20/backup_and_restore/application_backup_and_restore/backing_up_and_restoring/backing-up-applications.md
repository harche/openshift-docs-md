Frequent backups might consume storage on the backup storage location. Check the frequency of backups, retention time, and the amount of data of the persistent volumes (PVs) if using non-local backups, for example, S3 buckets. Because all taken backup remains until expired, also check the time to live (TTL) setting of the schedule.

You can back up applications by creating a `Backup` custom resource (CR). For more information, see [Creating a Backup CR](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-creating-backup-cr.xml#oadp-creating-backup-cr-doc). The following are the different backup types for a `Backup` CR:

- The `Backup` CR creates backup files for Kubernetes resources and internal images on S3 object storage.

- If you use Velero’s snapshot feature to back up data stored on the persistent volume, only snapshot related information is stored in the S3 bucket along with the Openshift object data.

- If your cloud provider has a native snapshot API or supports CSI snapshots, the `Backup` CR backs up persistent volumes (PVs) by creating snapshots. For more information about working with CSI snapshots, see [Backing up persistent volumes with CSI snapshots](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-backing-up-pvs-csi-doc.xml#oadp-backing-up-pvs-csi-doc).

If the underlying storage or the backup bucket are part of the same cluster, then the data might be lost in case of disaster.

For more information about CSI volume snapshots, see [CSI volume snapshots](../../../storage/container_storage_interface/persistent-storage-csi-snapshots.xml#persistent-storage-csi-snapshots).

- If your cloud provider does not support snapshots or if your applications are on NFS data volumes, you can create backups by using Kopia or Restic. See [Backing up applications with File System Backup: Kopia or Restic](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-backing-up-applications-restic-doc.xml#oadp-backing-up-applications-restic-doc).

<div class="important">

<div class="title">

PodVolumeRestore fails with a `…​/.snapshot: read-only file system` error

</div>

The `…​/.snapshot` directory is a snapshot copy directory, which is used by several NFS servers. This directory has read-only access by default, so Velero cannot restore to this directory.

Do not give Velero write access to the `.snapshot` directory, and disable client access to this directory.

- [Enable or disable client access to Snapshot copy directory by editing a share](https://docs.netapp.com/us-en/ontap/enable-snapshot-dir-access-task.html#enable-or-disable-client-access-to-snapshot-copy-directory-by-editing-a-share)

- [Prerequisites for backup and restore with FlashBlade](https://docs.portworx.com/portworx-backup-on-prem/reference/restore-with-fb#prerequisites-for-backup-and-restore-with-flashblade)

</div>

<div class="important">

The OpenShift API for Data Protection (OADP) does not support backing up volume snapshots that were created by other software.

</div>

# Previewing resources before running backup and restore

OADP backs up application resources based on the type, namespace, or label. This means that you can view the resources after the backup is complete. Similarly, you can view the restored objects based on the namespace, persistent volume (PV), or label after a restore operation is complete. To preview the resources in advance, you can do a dry run of the backup and restore operations.

- You have installed the OADP Operator.

1.  To preview the resources included in the backup before running the actual backup, run the following command:

    ``` terminal
    $ velero backup create <backup-name> --snapshot-volumes false
    ```

    - Specify the value of `--snapshot-volumes` parameter as `false`.

2.  To know more details about the backup resources, run the following command:

    ``` terminal
    $ velero describe backup <backup_name> --details
    ```

    - Specify the name of the backup.

3.  To preview the resources included in the restore before running the actual restore, run the following command:

    ``` terminal
    $ velero restore create --from-backup <backup-name>
    ```

    - Specify the name of the backup created to review the backup resources.

      <div class="important">

      The `velero restore create` command creates restore resources in the cluster. You must delete the resources created as part of the restore, after you review the resources.

      </div>

4.  To know more details about the restore resources, run the following command:

    ``` terminal
    $ velero describe restore <restore_name> --details
    ```

    - Specify the name of the restore.

You can create backup hooks to run commands before or after the backup operation. See [Creating backup hooks](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-creating-backup-hooks-doc.xml#oadp-creating-backup-hooks-doc).

You can schedule backups by creating a `Schedule` CR instead of a `Backup` CR. See [Scheduling backups using Schedule CR](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-scheduling-backups-doc.xml#oadp-scheduling-backups-doc).

# Known issues

OpenShift Container Platform 4.17 enforces a pod security admission (PSA) policy that can hinder the readiness of pods during a Restic restore process.

This issue has been resolved in the OADP 1.1.6 and OADP 1.2.2 releases, therefore it is recommended that users upgrade to these releases.

For more information, see [Restic restore partially failing on OCP 4.15 due to changed PSA policy](../../../backup_and_restore/application_backup_and_restore/troubleshooting/restic-issues.xml#oadp-restic-restore-failing-psa-policy_restic-issues).

- [Installing Operators on clusters for administrators](../../../operators/admin/olm-adding-operators-to-cluster.xml#olm-installing-operators-from-software-catalog_olm-adding-operators-to-a-cluster)

- [Installing Operators in namespaces for non-administrators](../../../operators/user/olm-installing-operators-in-namespace.xml#olm-installing-operators-in-namespace)
