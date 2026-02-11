You back up persistent volumes with Container Storage Interface (CSI) snapshots by editing the `VolumeSnapshotClass` custom resource (CR) of the cloud storage before you create the `Backup` CR, see [CSI volume snapshots](../../../storage/container_storage_interface/persistent-storage-csi-snapshots.xml#persistent-storage-csi-snapshots-overview_persistent-storage-csi-snapshots).

For more information, see [Creating a Backup CR](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-creating-backup-cr.xml#oadp-creating-backup-cr-doc).

# Backing up persistent volumes with CSI snapshots

<div>

<div class="title">

Prerequisites

</div>

- The cloud provider must support CSI snapshots.

- You must enable CSI in the `DataProtectionApplication` CR.

</div>

<div>

<div class="title">

Procedure

</div>

- Add the `metadata.labels.velero.io/csi-volumesnapshot-class: "true"` key-value pair to the `VolumeSnapshotClass` CR:

  <div class="formalpara">

  <div class="title">

  Example configuration file

  </div>

  ``` yaml
  apiVersion: snapshot.storage.k8s.io/v1
  kind: VolumeSnapshotClass
  metadata:
    name: <volume_snapshot_class_name>
    labels:
      velero.io/csi-volumesnapshot-class: "true"
    annotations:
      snapshot.storage.kubernetes.io/is-default-class: true
  driver: <csi_driver>
  deletionPolicy: <deletion_policy_type>
  ```

  </div>

  - Must be set to `true`.

  - If you are restoring this volume in another cluster with the same driver, make sure that you set the `snapshot.storage.kubernetes.io/is-default-class` parameter to `false` instead of setting it to `true`. Otherwise, the restore will partially fail.

  - OADP supports the `Retain` and `Delete` deletion policy types for CSI and Data Mover backup and restore.

</div>

<div>

<div class="title">

Next steps

</div>

- You can now create a `Backup` CR.

</div>
