Troubleshoot OpenShift API for Data Protection (OADP) issues by using diagnostic tools such as the OADP CLI, webhooks, `must-gather` custom resource, and other methods. This helps you identify and resolve problems with backup and restore operations.

You can troubleshoot OADP issues by using the following methods:

- Debug Velero custom resources (CRs) by using the OpenShift CLI tool.

- Debug Velero or Restic pod crashes, which are caused due to a lack of memory or CPU.

- Debug issues with Velero and admission webhooks.

- Check OADP installation issues, OADP Operator issues, backup and restore CR issues, and Restic issues.

- Use the available OADP timeouts to reduce errors, retries, or failures.

- Run the `DataProtectionTest` (DPT) custom resource to verify your backup storage bucket configuration and check the CSI snapshot readiness for persistent volume claims.

- Collect logs and CR information by using the `must-gather` tool.

- Monitor and analyze the workload performance with the help of OADP monitoring.

# Additional resources

- [Debugging with the OpenShift CLI tool](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-cli-tool.xml#oadp-debugging-oc-cli_oadp-cli-tool)

- [Debugging backups and restores using the OADP CLI](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-cli-tool.xml#migration-debugging-velero-resources_oadp-cli-tool)

- [Pods crash or restart due to lack of memory or CPU](../../../backup_and_restore/application_backup_and_restore/troubleshooting/pods-crash-or-restart-due-to-lack-of-memory-or-cpu.xml#pods-crash-or-restart-due-to-lack-of-memory-or-cpu)

- [Restoring workarounds for Velero backups that use admission webhooks](../../../backup_and_restore/application_backup_and_restore/troubleshooting/restoring-workarounds-for-velero-backups-that-use-admission-webhooks.xml#restoring-workarounds-for-velero-backups-that-use-admission-webhooks)

- [OADP installation issues](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-installation-issues.xml#oadp-installation-issues)

- [OADP Operator issues](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-operator-issues.xml#oadp-operator-issues)

- [Backup and restore CR issues](../../../backup_and_restore/application_backup_and_restore/troubleshooting/backup-and-restore-cr-issues.xml#backup-and-restore-cr-issues)

- [Restic issues](../../../backup_and_restore/application_backup_and_restore/troubleshooting/restic-issues.xml#restic-issues)

- [OADP timeouts](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-timeouts.xml#oadp-timeouts)

- [DataProtectionTest custom resource](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-data-protection-test.xml#oadp-data-protection-test)

- [Using the must-gather tool](../../../backup_and_restore/application_backup_and_restore/troubleshooting/using-the-must-gather-tool.xml#using-the-must-gather-tool)

- [OADP monitoring](../../../backup_and_restore/application_backup_and_restore/troubleshooting/oadp-monitoring.xml#oadp-monitoring)
