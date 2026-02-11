The schedule operation allows you to create a backup of your data at a particular time, specified by a Cron expression.

You schedule backups by creating a `Schedule` custom resource (CR) instead of a `Backup` CR.

> [!WARNING]
> Leave enough time in your backup schedule for a backup to finish before another backup is created.
>
> For example, if a backup of a namespace typically takes 10 minutes, do not schedule backups more frequently than every 15 minutes.

<div>

<div class="title">

Prerequisites

</div>

- You must install the OpenShift API for Data Protection (OADP) Operator.

- The `DataProtectionApplication` CR must be in a `Ready` state.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Retrieve the `backupStorageLocations` CRs:

    ``` terminal
    $ oc get backupStorageLocations -n openshift-adp
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAMESPACE       NAME              PHASE       LAST VALIDATED   AGE   DEFAULT
    openshift-adp   velero-sample-1   Available   11s              31m
    ```

    </div>

2.  Create a `Schedule` CR, as in the following example:

    ``` yaml
    $ cat << EOF | oc apply -f -
    apiVersion: velero.io/v1
    kind: Schedule
    metadata:
      name: <schedule>
      namespace: openshift-adp
    spec:
      schedule: 0 7 * * *
      template:
        hooks: {}
        includedNamespaces:
        - <namespace>
        storageLocation: <velero-sample-1>
        defaultVolumesToFsBackup: true
        ttl: 720h0m0s
    EOF
    ```

</div>

- `cron` expression to schedule the backup, for example, `0 7 * * *` to perform a backup every day at 7:00.

  > [!NOTE]
  > To schedule a backup at specific intervals, enter the `<duration_in_minutes>` in the following format:
  >
  > ``` terminal
  >   schedule: "*/10 * * * *"
  > ```
  >
  > Enter the minutes value between quotation marks (`" "`).

- Array of namespaces to back up.

- Name of the `backupStorageLocations` CR.

- Optional: In OADP version 1.2 and later, add the `defaultVolumesToFsBackup: true` key-value pair to your configuration when performing backups of volumes with Restic. In OADP version 1.1, add the `defaultVolumesToRestic: true` key-value pair when you back up volumes with Restic.

<div>

<div class="title">

Verification

</div>

- Verify that the status of the `Schedule` CR is `Completed` after the scheduled backup runs:

  ``` terminal
  $ oc get schedule -n openshift-adp <schedule> -o jsonpath='{.status.phase}'
  ```

</div>
