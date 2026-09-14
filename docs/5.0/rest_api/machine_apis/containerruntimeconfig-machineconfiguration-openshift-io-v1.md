Description
ContainerRuntimeConfig describes a customized Container Runtime configuration.

Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).

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
| `spec`       | `object`                                                                             | spec contains the desired container runtime configuration.                                                                                                                                                                                                                                           |
| `status`     | `object`                                                                             | status contains observed information about the container runtime configuration.                                                                                                                                                                                                                      |

## .spec

Description
spec contains the desired container runtime configuration.

Type
`object`

Required
- `containerRuntimeConfig`

| Property                    | Type     | Description                                                                                                                                     |
|-----------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `containerRuntimeConfig`    | `object` | containerRuntimeConfig defines the tuneables of the container runtime.                                                                          |
| `machineConfigPoolSelector` | `object` | machineConfigPoolSelector selects which pools the ContainerRuntimeConfig shoud apply to. A nil selector will result in no pools being selected. |

## .spec.containerRuntimeConfig

Description
containerRuntimeConfig defines the tuneables of the container runtime.

Type
`object`

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Property</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>additionalArtifactStores</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>additionalArtifactStores configures additional read-only artifact storage locations for Open Container Initiative (OCI) artifacts.</p>
<p>Artifacts are checked in order: additional stores first, then the default location (/var/lib/containers/storage/artifacts). Stores are read-only. Maximum of 10 stores allowed. Each path must be unique.</p>
<p>When omitted, only the default artifact location is used. When specified, at least one store must be provided.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>additionalArtifactStores[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>AdditionalArtifactStore defines an additional read-only storage location for Open Container Initiative (OCI) artifacts.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>additionalImageStores</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>additionalImageStores configures additional read-only container image store locations for Open Container Initiative (OCI) images.</p>
<p>Images are checked in order: additional stores first, then the default location. Stores are read-only. Maximum of 10 stores allowed. Each path must be unique.</p>
<p>When omitted, only the default image location is used. When specified, at least one store must be provided.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>additionalImageStores[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>AdditionalImageStore defines an additional read-only storage location for Open Container Initiative (OCI) images.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>additionalLayerStores</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>additionalLayerStores configures additional read-only container image layer store locations for Open Container Initiative (OCI) images.</p>
<p>Layers are checked in order: additional stores first, then the default location. Stores are read-only. Maximum of 5 stores allowed. Each path must be unique.</p>
<p>When omitted, only the default layer location is used. When specified, at least one store must be provided.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>additionalLayerStores[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>AdditionalLayerStore defines a read-only storage location for Open Container Initiative (OCI) container image layers.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>defaultRuntime</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>defaultRuntime is the name of the OCI runtime to be used as the default for containers. Allowed values are <code>runc</code> and <code>crun</code>. When set to <code>runc</code>, OpenShift will use runc to execute the container When set to <code>crun</code>, OpenShift will use crun to execute the container When omitted, this means no opinion and the platform is left to choose a reasonable default, which is subject to change over time. Currently, the default is <code>crun</code>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>logLevel</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>logLevel specifies the verbosity of the logs based on the level it is set to. Options are fatal, panic, error, warn, info, and debug.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>logSizeMax</code></p></td>
<td style="text-align: left;"><p><code>integer-or-string</code></p></td>
<td style="text-align: left;"><p>logSizeMax specifies the Maximum size allowed for the container log file. Negative numbers indicate that no size limit is imposed. If it is positive, it must be &gt;= 8192 to match/exceed conmon’s read buffer.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>overlaySize</code></p></td>
<td style="text-align: left;"><p><code>integer-or-string</code></p></td>
<td style="text-align: left;"><p>overlaySize specifies the maximum size of a container image. This flag can be used to set quota on the size of container images. (default: 10GB)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>pidsLimit</code></p></td>
<td style="text-align: left;"><p><code>integer</code></p></td>
<td style="text-align: left;"><p>pidsLimit specifies the maximum number of processes allowed in a container</p></td>
</tr>
</tbody>
</table>

## .spec.containerRuntimeConfig.additionalArtifactStores

Description
additionalArtifactStores configures additional read-only artifact storage locations for Open Container Initiative (OCI) artifacts.

Artifacts are checked in order: additional stores first, then the default location (/var/lib/containers/storage/artifacts). Stores are read-only. Maximum of 10 stores allowed. Each path must be unique.

When omitted, only the default artifact location is used. When specified, at least one store must be provided.

Type
`array`

## .spec.containerRuntimeConfig.additionalArtifactStores\[\]

Description
AdditionalArtifactStore defines an additional read-only storage location for Open Container Initiative (OCI) artifacts.

Type
`object`

Required
- `path`

| Property | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`   | `string` | path specifies the absolute location of the additional artifact store. The path must exist on the node before configuration is applied. When an artifact is requested, artifacts found at this location will be used instead of retrieving from the registry. The path is required and must be between 1 and 256 characters long, begin with a forward slash, and only contain the characters a-z, A-Z, 0-9, '/', '.', '\_', and '-'. Consecutive forward slashes are not permitted. |

## .spec.containerRuntimeConfig.additionalImageStores

Description
additionalImageStores configures additional read-only container image store locations for Open Container Initiative (OCI) images.

Images are checked in order: additional stores first, then the default location. Stores are read-only. Maximum of 10 stores allowed. Each path must be unique.

When omitted, only the default image location is used. When specified, at least one store must be provided.

Type
`array`

## .spec.containerRuntimeConfig.additionalImageStores\[\]

Description
AdditionalImageStore defines an additional read-only storage location for Open Container Initiative (OCI) images.

Type
`object`

Required
- `path`

| Property | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`   | `string` | path specifies the absolute location of the additional image store. The path must exist on the node before configuration is applied. When a container image is requested, images found at this location will be used instead of retrieving from the registry. The path is required and must be between 1 and 256 characters long, begin with a forward slash, and only contain the characters a-z, A-Z, 0-9, '/', '.', '\_', and '-'. Consecutive forward slashes are not permitted. |

## .spec.containerRuntimeConfig.additionalLayerStores

Description
additionalLayerStores configures additional read-only container image layer store locations for Open Container Initiative (OCI) images.

Layers are checked in order: additional stores first, then the default location. Stores are read-only. Maximum of 5 stores allowed. Each path must be unique.

When omitted, only the default layer location is used. When specified, at least one store must be provided.

Type
`array`

## .spec.containerRuntimeConfig.additionalLayerStores\[\]

Description
AdditionalLayerStore defines a read-only storage location for Open Container Initiative (OCI) container image layers.

Type
`object`

Required
- `path`

| Property | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`   | `string` | path specifies the absolute location of the additional layer store. The path must exist on the node before configuration is applied. When a container image is requested, layers found at this location will be used instead of retrieving from the registry. The path is required and must be between 1 and 256 characters long, begin with a forward slash, and only contain the characters a-z, A-Z, 0-9, '/', '.', '\_', and '-'. Consecutive forward slashes are not permitted. |

## .spec.machineConfigPoolSelector

Description
machineConfigPoolSelector selects which pools the ContainerRuntimeConfig shoud apply to. A nil selector will result in no pools being selected.

Type
`object`

| Property             | Type              | Description                                                                                                                                                                                                                                                     |
|----------------------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `matchExpressions`   | `array`           | matchExpressions is a list of label selector requirements. The requirements are ANDed.                                                                                                                                                                          |
| `matchExpressions[]` | `object`          | A label selector requirement is a selector that contains values, a key, and an operator that relates the key and values.                                                                                                                                        |
| `matchLabels`        | `object (string)` | matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed. |

## .spec.machineConfigPoolSelector.matchExpressions

Description
matchExpressions is a list of label selector requirements. The requirements are ANDed.

Type
`array`

## .spec.machineConfigPoolSelector.matchExpressions\[\]

Description
A label selector requirement is a selector that contains values, a key, and an operator that relates the key and values.

Type
`object`

Required
- `key`

- `operator`

| Property   | Type             | Description                                                                                                                                                                                                                                |
|------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `key`      | `string`         | key is the label key that the selector applies to.                                                                                                                                                                                         |
| `operator` | `string`         | operator represents a key’s relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist.                                                                                                                       |
| `values`   | `array (string)` | values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch. |

## .status

Description
status contains observed information about the container runtime configuration.

Type
`object`

| Property             | Type      | Description                                                                     |
|----------------------|-----------|---------------------------------------------------------------------------------|
| `conditions`         | `array`   | conditions represents the latest available observations of current state.       |
| `conditions[]`       | `object`  | ContainerRuntimeConfigCondition defines the state of the ContainerRuntimeConfig |
| `observedGeneration` | `integer` | observedGeneration represents the generation observed by the controller.        |

## .status.conditions

Description
conditions represents the latest available observations of current state.

Type
`array`

## .status.conditions\[\]

Description
ContainerRuntimeConfigCondition defines the state of the ContainerRuntimeConfig

Type
`object`

| Property             | Type     | Description                                                                                                 |
|----------------------|----------|-------------------------------------------------------------------------------------------------------------|
| `lastTransitionTime` | \`\`     | lastTransitionTime is the time of the last update to the current status object.                             |
| `message`            | `string` | message provides additional information about the current condition. This is only to be consumed by humans. |
| `reason`             | `string` | reason is the reason for the condition’s last transition. Reasons are PascalCase                            |
| `status`             | `string` | status of the condition, one of True, False, Unknown.                                                       |
| `type`               | `string` | type specifies the state of the operator’s reconciliation functionality.                                    |

# API endpoints

The following API endpoints are available:

- `/apis/machineconfiguration.openshift.io/v1/containerruntimeconfigs`

  - `DELETE`: delete collection of ContainerRuntimeConfig

  - `GET`: list objects of kind ContainerRuntimeConfig

  - `POST`: create a ContainerRuntimeConfig

- `/apis/machineconfiguration.openshift.io/v1/containerruntimeconfigs/{name}`

  - `DELETE`: delete a ContainerRuntimeConfig

  - `GET`: read the specified ContainerRuntimeConfig

  - `PATCH`: partially update the specified ContainerRuntimeConfig

  - `PUT`: replace the specified ContainerRuntimeConfig

- `/apis/machineconfiguration.openshift.io/v1/containerruntimeconfigs/{name}/status`

  - `GET`: read status of the specified ContainerRuntimeConfig

  - `PATCH`: partially update status of the specified ContainerRuntimeConfig

  - `PUT`: replace status of the specified ContainerRuntimeConfig

## /apis/machineconfiguration.openshift.io/v1/containerruntimeconfigs

HTTP method
`DELETE`

Description
delete collection of ContainerRuntimeConfig

| HTTP code          | Reponse body                                                                        |
|--------------------|-------------------------------------------------------------------------------------|
| 200 - OK           | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty                                                                               |

HTTP responses

HTTP method
`GET`

Description
list objects of kind ContainerRuntimeConfig

| HTTP code          | Reponse body                                                                                                                |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfigList`](../objects/index.xml#io-openshift-machineconfiguration-v1-ContainerRuntimeConfigList) schema |
| 401 - Unauthorized | Empty                                                                                                                       |

HTTP responses

HTTP method
`POST`

Description
create a ContainerRuntimeConfig

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                                                                           | Description |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 201 - Created      | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 202 - Accepted     | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses

## /apis/machineconfiguration.openshift.io/v1/containerruntimeconfigs/{name}

| Parameter | Type     | Description                        |
|-----------|----------|------------------------------------|
| `name`    | `string` | name of the ContainerRuntimeConfig |

Global path parameters

HTTP method
`DELETE`

Description
delete a ContainerRuntimeConfig

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
read the specified ContainerRuntimeConfig

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified ContainerRuntimeConfig

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses

HTTP method
`PUT`

Description
replace the specified ContainerRuntimeConfig

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                                                                           | Description |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 201 - Created      | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses

## /apis/machineconfiguration.openshift.io/v1/containerruntimeconfigs/{name}/status

| Parameter | Type     | Description                        |
|-----------|----------|------------------------------------|
| `name`    | `string` | name of the ContainerRuntimeConfig |

Global path parameters

HTTP method
`GET`

Description
read status of the specified ContainerRuntimeConfig

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses

HTTP method
`PATCH`

Description
partially update status of the specified ContainerRuntimeConfig

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses

HTTP method
`PUT`

Description
replace status of the specified ContainerRuntimeConfig

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                                                                           | Description |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 201 - Created      | [`ContainerRuntimeConfig`](../machine_apis/containerruntimeconfig-machineconfiguration-openshift-io-v1.xml#containerruntimeconfig-machineconfiguration-openshift-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                                          |

HTTP responses
