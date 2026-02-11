You can back up Red Hat 3scale API Management components by backing up the 3scale operator, and databases such as MySQL and Redis.

<div>

<div class="title">

Prerequisites

</div>

- You installed and configured Red Hat 3scale API Management. For more information, see [Installing 3scale API Management on OpenShift](https://docs.redhat.com/en/documentation/red_hat_3scale_api_management/2.15/html-single/installing_red_hat_3scale_api_management/index#install-threescale-on-openshift-guide) and [Red Hat 3scale API Management](https://docs.redhat.com/en/documentation/red_hat_3scale_api_management).

</div>

# Creating the Data Protection Application

You can create a Data Protection Application (DPA) custom resource (CR) for Red Hat 3scale API Management.

<div>

<div class="title">

Procedure

</div>

1.  Create a YAML file with the following configuration:

    <div class="formalpara">

    <div class="title">

    Example `dpa.yaml` file

    </div>

    ``` yaml
    apiVersion: oadp.openshift.io/v1alpha1
    kind: DataProtectionApplication
    metadata:
      name: dpa-sample
      namespace: openshift-adp
    spec:
      configuration:
        velero:
          defaultPlugins:
            - openshift
            - aws
            - csi
          resourceTimeout: 10m
        nodeAgent:
          enable: true
          uploaderType: kopia
      backupLocations:
        - name: default
          velero:
            provider: aws
            default: true
            objectStorage:
              bucket: <bucket_name>
              prefix: <prefix>
            config:
              region: <region>
              profile: "default"
              s3ForcePathStyle: "true"
              s3Url: <s3_url>
            credential:
              key: cloud
              name: cloud-credentials
    ```

    </div>

    - Specify a bucket as the backup storage location. If the bucket is not a dedicated bucket for Velero backups, you must specify a prefix.

    - Specify a prefix for Velero backups, for example, velero, if the bucket is used for multiple purposes.

    - Specify a region for backup storage location.

    - Specify the URL of the object store that you are using to store backups.

2.  Create the DPA CR by running the following command:

    ``` terminal
    $ oc create -f dpa.yaml
    ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [Installing the Data Protection Application](../../../backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.xml#oadp-installing-dpa_installing-oadp-aws)

</div>

# Backing up the 3scale API Management operator, secret, and APIManager

You can back up the Red Hat 3scale API Management operator resources, and both the `Secret` and APIManager custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- You created the Data Protection Application (DPA).

</div>

<div>

<div class="title">

Procedure

</div>

1.  Back up your 3scale operator CRs, such as `operatorgroup`, `namespaces`, and `subscriptions`, by creating a YAML file with the following configuration:

    <div class="formalpara">

    <div class="title">

    Example `backup.yaml` file

    </div>

    ``` yaml
    apiVersion: velero.io/v1
    kind: Backup
    metadata:
      name: operator-install-backup
      namespace: openshift-adp
    spec:
      csiSnapshotTimeout: 10m0s
      defaultVolumesToFsBackup: false
      includedNamespaces:
      - threescale
      includedResources:
      - operatorgroups
      - subscriptions
      - namespaces
      itemOperationTimeout: 1h0m0s
      snapshotMoveData: false
      ttl: 720h0m0s
    ```

    </div>

    - The value of the `metadata.name` parameter in the backup is the same value used in the `metadata.backupName` parameter used when restoring the 3scale operator.

    - Namespace where the 3scale operator is installed.

      > [!NOTE]
      > You can also back up and restore `ReplicationControllers`, `Deployment`, and `Pod` objects to ensure that all manually set environments are backed up and restored. This does not affect the flow of restoration.

2.  Create a backup CR by running the following command:

    ``` terminal
    $ oc create -f backup.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    backup.velero.io/operator-install-backup created
    ```

    </div>

3.  Back up the `Secret` CR by creating a YAML file with the following configuration:

    <div class="formalpara">

    <div class="title">

    Example `backup-secret.yaml` file

    </div>

    ``` yaml
    apiVersion: velero.io/v1
    kind: Backup
    metadata:
      name: operator-resources-secrets
      namespace: openshift-adp
    spec:
      csiSnapshotTimeout: 10m0s
      defaultVolumesToFsBackup: false
      includedNamespaces:
      - threescale
      includedResources:
      - secrets
      itemOperationTimeout: 1h0m0s
      labelSelector:
        matchLabels:
          app: 3scale-api-management
      snapshotMoveData: false
      snapshotVolumes: false
      ttl: 720h0m0s
    ```

    </div>

    - The value of the `metadata.name` parameter in the backup is the same value used in the `metadata.backupName` parameter used when restoring the `Secret`.

4.  Create the `Secret` backup CR by running the following command:

    ``` terminal
    $ oc create -f backup-secret.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    backup.velero.io/operator-resources-secrets created
    ```

    </div>

5.  Back up the APIManager CR by creating a YAML file with the following configuration:

    <div class="formalpara">

    <div class="title">

    Example backup-apimanager.yaml file

    </div>

    ``` yaml
    apiVersion: velero.io/v1
    kind: Backup
    metadata:
      name: operator-resources-apim
      namespace: openshift-adp
    spec:
      csiSnapshotTimeout: 10m0s
      defaultVolumesToFsBackup: false
      includedNamespaces:
      - threescale
      includedResources:
      - apimanagers
      itemOperationTimeout: 1h0m0s
      snapshotMoveData: false
      snapshotVolumes: false
      storageLocation: ts-dpa-1
      ttl: 720h0m0s
      volumeSnapshotLocations:
      - ts-dpa-1
    ```

    </div>

    - The value of the `metadata.name` parameter in the backup is the same value used in the `metadata.backupName` parameter used when restoring the APIManager.

6.  Create the APIManager CR by running the following command:

    ``` terminal
    $ oc create -f backup-apimanager.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    backup.velero.io/operator-resources-apim created
    ```

    </div>

</div>

<div>

<div class="title">

Additional resources

</div>

- [Creating a Backup CR](../../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-creating-backup-cr.xml#oadp-creating-backup-cr-doc)

</div>

# Backing up a MySQL database

You can back up a MySQL database by creating and attaching a persistent volume claim (PVC) to include the dumped data in the specified path.

<div>

<div class="title">

Prerequisites

</div>

- You have backed up the Red Hat 3scale API Management operator.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a YAML file with the following configuration for adding an additional PVC:

    <div class="formalpara">

    <div class="title">

    Example `ts_pvc.yaml` file

    </div>

    ``` yaml
    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: example-claim
      namespace: threescale
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi
      storageClassName: gp3-csi
      volumeMode: Filesystem
    ```

    </div>

2.  Create the additional PVC by running the following command:

    ``` terminal
    $ oc create -f ts_pvc.yml
    ```

3.  Attach the PVC to the system database pod by editing the `system-mysql` deployment to use the MySQL dump:

    ``` terminal
    $ oc edit deployment system-mysql -n threescale
    ```

    ``` yaml
      volumeMounts:
        - name: example-claim
          mountPath: /var/lib/mysqldump/data
        - name: mysql-storage
          mountPath: /var/lib/mysql/data
        - name: mysql-extra-conf
          mountPath: /etc/my-extra.d
        - name: mysql-main-conf
          mountPath: /etc/my-extra
        ...
          serviceAccount: amp
      volumes:
            - name: example-claim
              persistentVolumeClaim:
                claimName: example-claim
        ...
    ```

    - The PVC that contains the dumped data.

4.  Create a YAML file with following configuration to back up the MySQL database:

    <div class="formalpara">

    <div class="title">

    Example `mysql.yaml` file

    </div>

    ``` yaml
    apiVersion: velero.io/v1
    kind: Backup
    metadata:
      name: mysql-backup
      namespace: openshift-adp
    spec:
      csiSnapshotTimeout: 10m0s
      defaultVolumesToFsBackup: true
      hooks:
        resources:
        - name: dumpdb
          pre:
          - exec:
              command:
              - /bin/sh
              - -c
              - mysqldump -u $MYSQL_USER --password=$MYSQL_PASSWORD system --no-tablespaces
                > /var/lib/mysqldump/data/dump.sql
              container: system-mysql
              onError: Fail
              timeout: 5m
      includedNamespaces:
      - threescale
      includedResources:
      - deployment
      - pods
      - replicationControllers
      - persistentvolumeclaims
      - persistentvolumes
      itemOperationTimeout: 1h0m0s
      labelSelector:
        matchLabels:
          app: 3scale-api-management
          threescale_component_element: mysql
      snapshotMoveData: false
      ttl: 720h0m0s
    ```

    </div>

    - The value of the `metadata.name` parameter in the backup is the same value used in the `metadata.backupName` parameter used when restoring the MySQL database.

    - A directory where the data is backed up.

    - Resources to back up.

5.  Back up the MySQL database by running the following command:

    ``` terminal
    $ oc create -f mysql.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    backup.velero.io/mysql-backup created
    ```

    </div>

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the MySQL backup is completed by running the following command:

  ``` terminal
  $ oc get backups.velero.io mysql-backup -o yaml
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  status:
  completionTimestamp: "2025-04-17T13:25:19Z"
  errors: 1
  expiration: "2025-05-17T13:25:16Z"
  formatVersion: 1.1.0
  hookStatus: {}
  phase: Completed
  progress: {}
  startTimestamp: "2025-04-17T13:25:16Z"
  version: 1
  ```

  </div>

</div>

# Backing up the back-end Redis database

You can back up the Redis database by adding the required annotations and by listing which resources to back up using the `includedResources` parameter.

<div>

<div class="title">

Prerequisites

</div>

- You backed up the Red Hat 3scale API Management operator.

- You backed up your MySQL database.

- The Redis queues have been drained before performing the backup.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the annotations on the `backend-redis` deployment by running the following command:

    ``` terminal
    $ oc edit deployment backend-redis -n threescale
    ```

    ``` yaml
    annotations:
    post.hook.backup.velero.io/command: >-
             ["/bin/bash", "-c", "redis-cli CONFIG SET auto-aof-rewrite-percentage
             100"]
           pre.hook.backup.velero.io/command: >-
             ["/bin/bash", "-c", "redis-cli CONFIG SET auto-aof-rewrite-percentage
             0"]
    ```

2.  Create a YAML file with the following configuration to back up the Redis database:

    <div class="formalpara">

    <div class="title">

    Example `redis-backup.yaml` file

    </div>

    ``` yaml
    apiVersion: velero.io/v1
    kind: Backup
    metadata:
      name: redis-backup
      namespace: openshift-adp
    spec:
      csiSnapshotTimeout: 10m0s
      defaultVolumesToFsBackup: true
      includedNamespaces:
      - threescale
      includedResources:
      - deployment
      - pods
      - replicationcontrollers
      - persistentvolumes
      - persistentvolumeclaims
      itemOperationTimeout: 1h0m0s
      labelSelector:
        matchLabels:
          app: 3scale-api-management
          threescale_component: backend
          threescale_component_element: redis
      snapshotMoveData: false
      snapshotVolumes: false
      ttl: 720h0m0s
    ```

    </div>

    - The value of the `metadata.name` parameter in the backup is the same value used in the `metadata.backupName` parameter used when restoring the restoring the Redis database.

3.  Back up the Redis database by running the following command:

    ``` terminal
    $ oc create -f redis-backup.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    backup.velero.io/redis-backup created
    ```

    </div>

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the Redis backup is completed by running the following command:

  ``` terminal
  $ oc get backups.velero.io redis-backup -o yaml
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  status:
  completionTimestamp: "2025-04-17T13:25:19Z"
  errors: 1
  expiration: "2025-05-17T13:25:16Z"
  formatVersion: 1.1.0
  hookStatus: {}
  phase: Completed
  progress: {}
  startTimestamp: "2025-04-17T13:25:16Z"
  version: 1
  ```

  </div>

</div>
