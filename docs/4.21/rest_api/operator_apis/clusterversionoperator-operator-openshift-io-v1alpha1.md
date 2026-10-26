Description
ClusterVersionOperator holds cluster-wide information about the Cluster Version Operator.

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
| `spec` | `object` | spec is the specification of the desired behavior of the Cluster Version Operator. |
| `status` | `object` | status is the most recently observed status of the Cluster Version Operator. |

## .spec

Description
spec is the specification of the desired behavior of the Cluster Version Operator.

Type
`object`

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
<td style="text-align: left;"><p><code>operatorLogLevel</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>operatorLogLevel is an intent based logging for the operator itself. It does not give fine grained control, but it is a simple way to manage coarse grained logging choices that operators have to interpret for themselves.</p>
<p>Valid values are: "Normal", "Debug", "Trace", "TraceAll". Defaults to "Normal".</p></td>
</tr>
</tbody>
</table>

## .status

Description
status is the most recently observed status of the Cluster Version Operator.

Type
`object`

| Property | Type | Description |
|----|----|----|
| `observedGeneration` | `integer` | observedGeneration represents the most recent generation observed by the operator and specifies the version of the spec field currently being synced. |

# API endpoints

The following API endpoints are available:

- `/apis/operator.openshift.io/v1alpha1/clusterversionoperators`

  - `DELETE`: delete collection of ClusterVersionOperator

  - `GET`: list objects of kind ClusterVersionOperator

  - `POST`: create a ClusterVersionOperator

- `/apis/operator.openshift.io/v1alpha1/clusterversionoperators/{name}`

  - `DELETE`: delete a ClusterVersionOperator

  - `GET`: read the specified ClusterVersionOperator

  - `PATCH`: partially update the specified ClusterVersionOperator

  - `PUT`: replace the specified ClusterVersionOperator

- `/apis/operator.openshift.io/v1alpha1/clusterversionoperators/{name}/status`

  - `GET`: read status of the specified ClusterVersionOperator

  - `PATCH`: partially update status of the specified ClusterVersionOperator

  - `PUT`: replace status of the specified ClusterVersionOperator

## /apis/operator.openshift.io/v1alpha1/clusterversionoperators

HTTP method
`DELETE`

Description
delete collection of ClusterVersionOperator

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`GET`

Description
list objects of kind ClusterVersionOperator

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperatorList`](../objects/index.xml#io-openshift-operator-v1alpha1-ClusterVersionOperatorList) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`POST`

Description
create a ClusterVersionOperator

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 201 - Created | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 202 - Accepted | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/operator.openshift.io/v1alpha1/clusterversionoperators/{name}

| Parameter | Type     | Description                        |
|-----------|----------|------------------------------------|
| `name`    | `string` | name of the ClusterVersionOperator |

Global path parameters

HTTP method
`DELETE`

Description
delete a ClusterVersionOperator

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
read the specified ClusterVersionOperator

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified ClusterVersionOperator

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PUT`

Description
replace the specified ClusterVersionOperator

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 201 - Created | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/operator.openshift.io/v1alpha1/clusterversionoperators/{name}/status

| Parameter | Type     | Description                        |
|-----------|----------|------------------------------------|
| `name`    | `string` | name of the ClusterVersionOperator |

Global path parameters

HTTP method
`GET`

Description
read status of the specified ClusterVersionOperator

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PATCH`

Description
partially update status of the specified ClusterVersionOperator

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PUT`

Description
replace status of the specified ClusterVersionOperator

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 201 - Created | [`ClusterVersionOperator`](../operator_apis/clusterversionoperator-operator-openshift-io-v1alpha1.xml#clusterversionoperator-operator-openshift-io-v1alpha1) schema |
| 401 - Unauthorized | Empty |

HTTP responses
