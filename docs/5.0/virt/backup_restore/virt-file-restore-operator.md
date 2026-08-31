Use the File Restore Operator to restore individual files and directories to running virtual machines from persistent volume claims or volume snapshots.

<div class="important">

The File Restore Operator is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# About the File Restore Operator

You can restore individual files and directories to running virtual machines (VMs) without restarting the VM by using the File Restore Operator, a Kubernetes operator that performs file-level restore operations.

The operator uses hot plug technology to attach a restore volume to a running VM, and uses SSH to copy files from the source VM to the target VM.

The File Restore Operator supports the following source types:

- **`PersistentVolumeClaims`** (PVCs): Restore from backup PVCs.

- **`VolumeSnapshots`**: Restore from Kubernetes volume snapshots.
