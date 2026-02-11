Description
Backup provides configuration for performing backups of the openshift cluster.

Compatibility level 4: No compatibility is provided, the API can change at any point for any reason. These capabilities should not be used by applications needing long term support.

Type
`object`

Required
- `spec`

# Specification

| Property     | Type                                                                                 | Description                                                                                                                                                                                                                                                                                          |
|--------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apiVersion` | `string`                                                                             | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources>  |
| `kind`       | `string`                                                                             | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds> |
| `metadata`   | [`ObjectMeta`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-ObjectMeta) | Standard object’s metadata. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata>                                                                                                                                                                |
| `spec`       | `object`                                                                             | spec holds user settable values for configuration                                                                                                                                                                                                                                                    |
| `status`     | `object`                                                                             | status holds observed values from the cluster. They may not be overridden.                                                                                                                                                                                                                           |

## .spec

Description
spec holds user settable values for configuration

Type
`object`

Required
- `etcd`

| Property | Type     | Description                                                               |
|----------|----------|---------------------------------------------------------------------------|
| `etcd`   | `object` | etcd specifies the configuration for periodic backups of the etcd cluster |

## .spec.etcd

Description
etcd specifies the configuration for periodic backups of the etcd cluster

Type
`object`

| Property          | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `pvcName`         | `string` | pvcName specifies the name of the PersistentVolumeClaim (PVC) which binds a PersistentVolume where the etcd backup files would be saved The PVC itself must always be created in the "openshift-etcd" namespace If the PVC is left unspecified "" then the platform will choose a reasonable default location to save the backup. In the future this would be backups saved across the control-plane master nodes. |
| `retentionPolicy` | `object` | retentionPolicy defines the retention policy for retaining and deleting existing backups.                                                                                                                                                                                                                                                                                                                          |
| `schedule`        | `string` | schedule defines the recurring backup schedule in Cron format every 2 hours: 0 \*/2 \* \* \* every day at 3am: 0 3 \* \* \* Empty string means no opinion and the platform is left to choose a reasonable default which is subject to change without notice. The current default is "no backups", but will change in the future.                                                                                   |
| `timeZone`        | `string` | The time zone name for the given schedule, see <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>. If not specified, this will default to the time zone of the kube-controller-manager process. See <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#time-zones>                                                                                                                  |

## .spec.etcd.retentionPolicy

Description
retentionPolicy defines the retention policy for retaining and deleting existing backups.

Type
`object`

Required
- `retentionType`

| Property          | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `retentionNumber` | `object` | retentionNumber configures the retention policy based on the number of backups                                                                                                                                                                                                                                                                                                                                                     |
| `retentionSize`   | `object` | retentionSize configures the retention policy based on the size of backups                                                                                                                                                                                                                                                                                                                                                         |
| `retentionType`   | `string` | retentionType sets the type of retention policy. Currently, the only valid policies are retention by number of backups (RetentionNumber), by the size of backups (RetentionSize). More policies or types may be added in the future. Empty string means no opinion and the platform is left to choose a reasonable default which is subject to change without notice. The current default is RetentionNumber with 15 backups kept. |

## .spec.etcd.retentionPolicy.retentionNumber

Description
retentionNumber configures the retention policy based on the number of backups

Type
`object`

Required
- `maxNumberOfBackups`

| Property             | Type      | Description                                                                                                                                                                                                         |
|----------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `maxNumberOfBackups` | `integer` | maxNumberOfBackups defines the maximum number of backups to retain. If the existing number of backups saved is equal to MaxNumberOfBackups then the oldest backup will be removed before a new backup is initiated. |

## .spec.etcd.retentionPolicy.retentionSize

Description
retentionSize configures the retention policy based on the size of backups

Type
`object`

Required
- `maxSizeOfBackupsGb`

| Property             | Type      | Description                                                                                                                                                                                                 |
|----------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `maxSizeOfBackupsGb` | `integer` | maxSizeOfBackupsGb defines the total size in GB of backups to retain. If the current total size backups exceeds MaxSizeOfBackupsGb then the oldest backup will be removed before a new backup is initiated. |

## .status

Description
status holds observed values from the cluster. They may not be overridden.

Type
`object`

# API endpoints

The following API endpoints are available:

- `/apis/config.openshift.io/v1alpha1/backups`

  - `DELETE`: delete collection of Backup

  - `GET`: list objects of kind Backup

  - `POST`: create a Backup

- `/apis/config.openshift.io/v1alpha1/backups/{name}`

  - `DELETE`: delete a Backup

  - `GET`: read the specified Backup

  - `PATCH`: partially update the specified Backup

  - `PUT`: replace the specified Backup

- `/apis/config.openshift.io/v1alpha1/backups/{name}/status`

  - `GET`: read status of the specified Backup

  - `PATCH`: partially update status of the specified Backup

  - `PUT`: replace status of the specified Backup

## /apis/config.openshift.io/v1alpha1/backups

HTTP method
`DELETE`

Description
delete collection of Backup

| HTTP code          | Reponse body                                                                        |
|--------------------|-------------------------------------------------------------------------------------|
| 200 - OK           | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty                                                                               |

HTTP responses

HTTP method
`GET`

Description
list objects of kind Backup

| HTTP code          | Reponse body                                                                        |
|--------------------|-------------------------------------------------------------------------------------|
| 200 - OK           | [`BackupList`](../objects/index.xml#io-openshift-config-v1alpha1-BackupList) schema |
| 401 - Unauthorized | Empty                                                                               |

HTTP responses

HTTP method
`POST`

Description
create a Backup

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                          | Description |
|-----------|---------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 201 - Created      | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 202 - Accepted     | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses

## /apis/config.openshift.io/v1alpha1/backups/{name}

| Parameter | Type     | Description        |
|-----------|----------|--------------------|
| `name`    | `string` | name of the Backup |

Global path parameters

HTTP method
`DELETE`

Description
delete a Backup

| Parameter | Type     | Description                                                                                                                                                                                                                                              |
|-----------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`  | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |

Query parameters

| HTTP code          | Reponse body                                                                        |
|--------------------|-------------------------------------------------------------------------------------|
| 200 - OK           | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 202 - Accepted     | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty                                                                               |

HTTP responses

HTTP method
`GET`

Description
read the specified Backup

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified Backup

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses

HTTP method
`PUT`

Description
replace the specified Backup

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                          | Description |
|-----------|---------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 201 - Created      | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses

## /apis/config.openshift.io/v1alpha1/backups/{name}/status

| Parameter | Type     | Description        |
|-----------|----------|--------------------|
| `name`    | `string` | name of the Backup |

Global path parameters

HTTP method
`GET`

Description
read status of the specified Backup

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses

HTTP method
`PATCH`

Description
partially update status of the specified Backup

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses

HTTP method
`PUT`

Description
replace status of the specified Backup

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                          | Description |
|-----------|---------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 201 - Created      | [`Backup`](../config_apis/backup-config-openshift-io-v1alpha1.xml#backup-config-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                         |

HTTP responses
