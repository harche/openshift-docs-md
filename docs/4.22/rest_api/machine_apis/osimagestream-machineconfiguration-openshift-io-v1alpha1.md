Description
OSImageStream describes a set of streams and associated images available for the MachineConfigPools to be used as base OS images.

The resource is a singleton named "cluster".

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
| `spec`       | `object`                                                                             | spec contains the desired OSImageStream config configuration.                                                                                                                                                                                                                                        |
| `status`     | `object`                                                                             | status describes the last observed state of this OSImageStream. Populated by the MachineConfigOperator after reading release metadata. When not present, the controller has not yet reconciled this resource.                                                                                        |

## .spec

Description
spec contains the desired OSImageStream config configuration.

Type
`object`

## .status

Description
status describes the last observed state of this OSImageStream. Populated by the MachineConfigOperator after reading release metadata. When not present, the controller has not yet reconciled this resource.

Type
`object`

Required
- `availableStreams`

- `defaultStream`

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
<td style="text-align: left;"><p><code>availableStreams</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>availableStreams is a list of the available OS Image Streams that can be used as the base image for MachineConfigPools. availableStreams is required, must have at least one item, must not exceed 100 items, and must have unique entries keyed on the name field.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>availableStreams[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>defaultStream</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>defaultStream is the name of the stream that should be used as the default when no specific stream is requested by a MachineConfigPool.</p>
<p>It must be a valid RFC 1123 subdomain between 1 and 253 characters in length, consisting of lowercase alphanumeric characters, hyphens ('-'), and periods ('.'), and must reference the name of one of the streams in availableStreams.</p></td>
</tr>
</tbody>
</table>

## .status.availableStreams

Description
availableStreams is a list of the available OS Image Streams that can be used as the base image for MachineConfigPools. availableStreams is required, must have at least one item, must not exceed 100 items, and must have unique entries keyed on the name field.

Type
`array`

## .status.availableStreams\[\]

Description

Type
`object`

Required
- `name`

- `osExtensionsImage`

- `osImage`

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
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>name is the required identifier of the stream.</p>
<p>name is determined by the operator based on the OCI label of the discovered OS or Extension Image.</p>
<p>Must be a valid RFC 1123 subdomain between 1 and 253 characters in length, consisting of lowercase alphanumeric characters, hyphens ('-'), and periods ('.').</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>osExtensionsImage</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>osExtensionsImage is a required OS Extensions Image referenced by digest.</p>
<p>osExtensionsImage bundles the extra repositories used to enable extensions, augmenting the base operating system without modifying the underlying immutable osImage.</p>
<p>The format of the image pull spec is: host[:port][/namespace]/name@sha256:&lt;digest&gt;, where the digest must be 64 characters long, and consist only of lowercase hexadecimal characters, a-f and 0-9. The length of the whole spec must be between 1 to 447 characters.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>osImage</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>osImage is a required OS Image referenced by digest.</p>
<p>osImage contains the immutable, fundamental operating system components, including the kernel and base utilities, that define the core environment for the node’s host operating system.</p>
<p>The format of the image pull spec is: host[:port][/namespace]/name@sha256:&lt;digest&gt;, where the digest must be 64 characters long, and consist only of lowercase hexadecimal characters, a-f and 0-9. The length of the whole spec must be between 1 to 447 characters.</p></td>
</tr>
</tbody>
</table>

# API endpoints

The following API endpoints are available:

- `/apis/machineconfiguration.openshift.io/v1alpha1/osimagestreams`

  - `DELETE`: delete collection of OSImageStream

  - `GET`: list objects of kind OSImageStream

  - `POST`: create an OSImageStream

- `/apis/machineconfiguration.openshift.io/v1alpha1/osimagestreams/{name}`

  - `DELETE`: delete an OSImageStream

  - `GET`: read the specified OSImageStream

  - `PATCH`: partially update the specified OSImageStream

  - `PUT`: replace the specified OSImageStream

- `/apis/machineconfiguration.openshift.io/v1alpha1/osimagestreams/{name}/status`

  - `GET`: read status of the specified OSImageStream

  - `PATCH`: partially update status of the specified OSImageStream

  - `PUT`: replace status of the specified OSImageStream

## /apis/machineconfiguration.openshift.io/v1alpha1/osimagestreams

HTTP method
`DELETE`

Description
delete collection of OSImageStream

| HTTP code          | Reponse body                                                                        |
|--------------------|-------------------------------------------------------------------------------------|
| 200 - OK           | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty                                                                               |

HTTP responses

HTTP method
`GET`

Description
list objects of kind OSImageStream

| HTTP code          | Reponse body                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStreamList`](../objects/index.xml#io-openshift-machineconfiguration-v1alpha1-OSImageStreamList) schema |
| 401 - Unauthorized | Empty                                                                                                           |

HTTP responses

HTTP method
`POST`

Description
create an OSImageStream

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                                                            | Description |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 201 - Created      | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 202 - Accepted     | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses

## /apis/machineconfiguration.openshift.io/v1alpha1/osimagestreams/{name}

| Parameter | Type     | Description               |
|-----------|----------|---------------------------|
| `name`    | `string` | name of the OSImageStream |

Global path parameters

HTTP method
`DELETE`

Description
delete an OSImageStream

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
read the specified OSImageStream

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified OSImageStream

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses

HTTP method
`PUT`

Description
replace the specified OSImageStream

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                                                            | Description |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 201 - Created      | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses

## /apis/machineconfiguration.openshift.io/v1alpha1/osimagestreams/{name}/status

| Parameter | Type     | Description               |
|-----------|----------|---------------------------|
| `name`    | `string` | name of the OSImageStream |

Global path parameters

HTTP method
`GET`

Description
read status of the specified OSImageStream

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses

HTTP method
`PATCH`

Description
partially update status of the specified OSImageStream

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses

HTTP method
`PUT`

Description
replace status of the specified OSImageStream

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                                                            | Description |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                                                                    |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 201 - Created      | [`OSImageStream`](../machine_apis/osimagestream-machineconfiguration-openshift-io-v1alpha1.xml#osimagestream-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty                                                                                                                                                           |

HTTP responses
