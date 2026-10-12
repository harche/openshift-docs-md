Container Storage Interface (CSI) changed block tracking (CBT) enables compatible backup applications to identify block ranges that changed between two snapshots of the same underlying CSI block-storage volume.

<div class="important">

Changed block tracking is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

Backup applications can use changed-block metadata to reduce the data read and transferred for incremental backups. The API can also identify allocated block ranges in a single snapshot, allowing backup applications to skip unallocated ranges when creating a full backup of that snapshot. These operations return metadata, not the snapshot data itself. The backup application reads and backs up the relevant data separately.

CBT requires support from both the CSI driver and the backup application.

For more information about CBT, see the Red Hat Knowledgebase solution "How to use Changed Block Tracking (Tech Preview) in OpenShift 5.0".

# Additional resources

- [How to use Changed Block Tracking (Tech Preview) in OpenShift 5.0](https://access.redhat.com/solutions/7146879)
