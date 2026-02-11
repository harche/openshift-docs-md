Description
InternalReleaseImage is used to keep track and manage a set of release bundles (OCP and OLM operators images) that are stored into the control planes nodes.

Compatibility level 4: No compatibility is provided, the API can change at any point for any reason. These capabilities should not be used by applications needing long term support.

Type
`object`

Required
- `metadata`

- `spec`

# Specification

| Property | Type | Description |
|----|----|----|
| `apiVersion` | `string` | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources> |
| `kind` | `string` | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds> |
| `metadata` | [`ObjectMeta`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-ObjectMeta) | Standard object’s metadata. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata> |
| `spec` | `object` | spec describes the configuration of this internal release image. |
| `status` | `object` | status describes the last observed state of this internal release image. |

## .spec

Description
spec describes the configuration of this internal release image.

Type
`object`

Required
- `releases`

| Property | Type | Description |
|----|----|----|
| `releases` | `array` | releases is a list of release bundle identifiers that the user wants to add/remove to/from the control plane nodes. Entries must be unique, keyed on the name field. releases must contain at least one entry and must not exceed 16 entries. |
| `releases[]` | `object` | InternalReleaseImageRef is used to provide a simple reference for a release bundle. Currently it contains only the name field. |

## .spec.releases

Description
releases is a list of release bundle identifiers that the user wants to add/remove to/from the control plane nodes. Entries must be unique, keyed on the name field. releases must contain at least one entry and must not exceed 16 entries.

Type
`array`

## .spec.releases\[\]

Description
InternalReleaseImageRef is used to provide a simple reference for a release bundle. Currently it contains only the name field.

Type
`object`

Required
- `name`

| Property | Type | Description |
|----|----|----|
| `name` | `string` | name indicates the desired release bundle identifier. This field is required and must be between 1 and 64 characters long. The expected name format is ocp-release-bundle-\<version\>-\<arch\|stream\>. |

## .status

Description
status describes the last observed state of this internal release image.

Type
`object`

Required
- `releases`

| Property | Type | Description |
|----|----|----|
| `conditions` | `array` | conditions represent the observations of the InternalReleaseImage controller current state. Valid types are: Degraded. If Degraded is true, that means something has gone wrong in the controller. |
| `conditions[]` | `object` | Condition contains details for one aspect of the current state of this API Resource. |
| `releases` | `array` | releases is a list of the release bundles currently owned and managed by the cluster. A release bundle content could be safely pulled only when its Conditions field contains at least an Available entry set to "True" and Degraded to "False". Entries must be unique, keyed on the name field. releases must contain at least one entry and must not exceed 32 entries. |
| `releases[]` | `object` |  |

## .status.conditions

Description
conditions represent the observations of the InternalReleaseImage controller current state. Valid types are: Degraded. If Degraded is true, that means something has gone wrong in the controller.

Type
`array`

## .status.conditions\[\]

Description
Condition contains details for one aspect of the current state of this API Resource.

Type
`object`

Required
- `lastTransitionTime`

- `message`

- `reason`

- `status`

- `type`

| Property | Type | Description |
|----|----|----|
| `lastTransitionTime` | `string` | lastTransitionTime is the last time the condition transitioned from one status to another. This should be when the underlying condition changed. If that is not known, then using the time when the API field changed is acceptable. |
| `message` | `string` | message is a human readable message indicating details about the transition. This may be an empty string. |
| `observedGeneration` | `integer` | observedGeneration represents the .metadata.generation that the condition was set based upon. For instance, if .metadata.generation is currently 12, but the .status.conditions\[x\].observedGeneration is 9, the condition is out of date with respect to the current state of the instance. |
| `reason` | `string` | reason contains a programmatic identifier indicating the reason for the condition’s last transition. Producers of specific condition types may define expected values and meanings for this field, and whether the values are considered a guaranteed API. The value should be a CamelCase string. This field may not be empty. |
| `status` | `string` | status of the condition, one of True, False, Unknown. |
| `type` | `string` | type of condition in CamelCase or in foo.example.com/CamelCase. |

## .status.releases

Description
releases is a list of the release bundles currently owned and managed by the cluster. A release bundle content could be safely pulled only when its Conditions field contains at least an Available entry set to "True" and Degraded to "False". Entries must be unique, keyed on the name field. releases must contain at least one entry and must not exceed 32 entries.

Type
`array`

## .status.releases\[\]

Description

Type
`object`

Required
- `name`

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Property</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p><code>conditions</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>conditions represent the observations of an internal release image current state. Valid types are: Mounted, Installing, Available, Removing and Degraded.</p>
<p>If Mounted is true, that means that a valid ISO has been discovered and mounted on one of the cluster nodes. If Installing is true, that means that a new release bundle is currently being copied on one (or more) cluster nodes, and not yet completed. If Available is true, it means that the release has been previously installed on all the cluster nodes, and it can be used. If Removing is true, it means that a release deletion is in progress on one (or more) cluster nodes, and not yet completed. If Degraded is true, that means something has gone wrong (possibly on one or more cluster nodes).</p>
<p>In general, after installing a new release bundle, it is required to wait for the Conditions "Available" to become "True" (and all the other conditions to be equal to "False") before being able to pull its content.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>conditions[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>Condition contains details for one aspect of the current state of this API Resource.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>image</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>image is an OCP release image referenced by digest. The format of the image pull spec is: host[:port][/namespace]/name@sha256:&lt;digest&gt;, where the digest must be 64 characters long, and consist only of lowercase hexadecimal characters, a-f and 0-9. The length of the whole spec must be between 1 to 447 characters. The field is optional, and it will be provided after a release will be successfully installed.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>name indicates the desired release bundle identifier. This field is required and must be between 1 and 64 characters long. The expected name format is ocp-release-bundle-&lt;version&gt;-&lt;arch|stream&gt;.</p></td>
</tr>
</tbody>
</table>

## .status.releases\[\].conditions

Description
conditions represent the observations of an internal release image current state. Valid types are: Mounted, Installing, Available, Removing and Degraded.

If Mounted is true, that means that a valid ISO has been discovered and mounted on one of the cluster nodes. If Installing is true, that means that a new release bundle is currently being copied on one (or more) cluster nodes, and not yet completed. If Available is true, it means that the release has been previously installed on all the cluster nodes, and it can be used. If Removing is true, it means that a release deletion is in progress on one (or more) cluster nodes, and not yet completed. If Degraded is true, that means something has gone wrong (possibly on one or more cluster nodes).

In general, after installing a new release bundle, it is required to wait for the Conditions "Available" to become "True" (and all the other conditions to be equal to "False") before being able to pull its content.

Type
`array`

## .status.releases\[\].conditions\[\]

Description
Condition contains details for one aspect of the current state of this API Resource.

Type
`object`

Required
- `lastTransitionTime`

- `message`

- `reason`

- `status`

- `type`

| Property | Type | Description |
|----|----|----|
| `lastTransitionTime` | `string` | lastTransitionTime is the last time the condition transitioned from one status to another. This should be when the underlying condition changed. If that is not known, then using the time when the API field changed is acceptable. |
| `message` | `string` | message is a human readable message indicating details about the transition. This may be an empty string. |
| `observedGeneration` | `integer` | observedGeneration represents the .metadata.generation that the condition was set based upon. For instance, if .metadata.generation is currently 12, but the .status.conditions\[x\].observedGeneration is 9, the condition is out of date with respect to the current state of the instance. |
| `reason` | `string` | reason contains a programmatic identifier indicating the reason for the condition’s last transition. Producers of specific condition types may define expected values and meanings for this field, and whether the values are considered a guaranteed API. The value should be a CamelCase string. This field may not be empty. |
| `status` | `string` | status of the condition, one of True, False, Unknown. |
| `type` | `string` | type of condition in CamelCase or in foo.example.com/CamelCase. |

# API endpoints

The following API endpoints are available:

- `/apis/machineconfiguration.openshift.io/v1alpha1/internalreleaseimages`

  - `DELETE`: delete collection of InternalReleaseImage

  - `GET`: list objects of kind InternalReleaseImage

  - `POST`: create an InternalReleaseImage

- `/apis/machineconfiguration.openshift.io/v1alpha1/internalreleaseimages/{name}`

  - `DELETE`: delete an InternalReleaseImage

  - `GET`: read the specified InternalReleaseImage

  - `PATCH`: partially update the specified InternalReleaseImage

  - `PUT`: replace the specified InternalReleaseImage

- `/apis/machineconfiguration.openshift.io/v1alpha1/internalreleaseimages/{name}/status`

  - `GET`: read status of the specified InternalReleaseImage

  - `PATCH`: partially update status of the specified InternalReleaseImage

  - `PUT`: replace status of the specified InternalReleaseImage

## /apis/machineconfiguration.openshift.io/v1alpha1/internalreleaseimages

HTTP method
`DELETE`

Description
delete collection of InternalReleaseImage

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`GET`

Description
list objects of kind InternalReleaseImage

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImageList`](../objects/index.xml#io-openshift-machineconfiguration-v1alpha1-InternalReleaseImageList) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`POST`

Description
create an InternalReleaseImage

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 201 - Created | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 202 - Accepted | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/machineconfiguration.openshift.io/v1alpha1/internalreleaseimages/{name}

| Parameter | Type     | Description                      |
|-----------|----------|----------------------------------|
| `name`    | `string` | name of the InternalReleaseImage |

Global path parameters

HTTP method
`DELETE`

Description
delete an InternalReleaseImage

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 202 - Accepted | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`GET`

Description
read the specified InternalReleaseImage

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified InternalReleaseImage

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PUT`

Description
replace the specified InternalReleaseImage

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 201 - Created | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/machineconfiguration.openshift.io/v1alpha1/internalreleaseimages/{name}/status

| Parameter | Type     | Description                      |
|-----------|----------|----------------------------------|
| `name`    | `string` | name of the InternalReleaseImage |

Global path parameters

HTTP method
`GET`

Description
read status of the specified InternalReleaseImage

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PATCH`

Description
partially update status of the specified InternalReleaseImage

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PUT`

Description
replace status of the specified InternalReleaseImage

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 201 - Created | [`InternalReleaseImage`](../machine_apis/internalreleaseimage-machineconfiguration-openshift-io-v1alpha1.xml#internalreleaseimage-machineconfiguration-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses
