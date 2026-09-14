Description
The TLSRoute resource is similar to TCPRoute, but can be configured to match against TLS-specific metadata. This allows more flexibility in matching streams for a given TLS listener.

If you need to forward traffic to a single target for a TLS listener, you could choose to use a TCPRoute with a TLS listener.

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
| `spec`       | `object`                                                                             | Spec defines the desired state of TLSRoute.                                                                                                                                                                                                                                                          |
| `status`     | `object`                                                                             | Status defines the current state of TLSRoute.                                                                                                                                                                                                                                                        |

## .spec

Description
Spec defines the desired state of TLSRoute.

Type
`object`

Required
- `hostnames`

- `rules`

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
<td style="text-align: left;"><p><code>hostnames</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>Hostnames defines a set of SNI hostnames that should match against the SNI attribute of TLS ClientHello message in TLS handshake. This matches the RFC 1123 definition of a hostname with 2 notable exceptions:</p>
<p>1. IPs are not allowed in SNI hostnames per RFC 6066. 2. A hostname may be prefixed with a wildcard label (<code>*.</code>). The wildcard label must appear by itself as the first label.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>parentRefs</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>ParentRefs references the resources (usually Gateways) that a Route wants to be attached to. Note that the referenced parent resource needs to allow this for the attachment to be complete. For Gateways, that means the Gateway needs to allow attachment from Routes of this kind and namespace. For Services, that means the Service must either be in the same namespace for a "producer" route, or the mesh implementation must support and allow "consumer" routes for the referenced Service. ReferenceGrant is not applicable for governing ParentRefs to Services - it is not possible to create a "producer" route for a Service in a different namespace from the Route.</p>
<p>There are two kinds of parent resources with "Core" support:</p>
<p>* Gateway (Gateway conformance profile) * Service (Mesh conformance profile, ClusterIP Services only)</p>
<p>This API may be extended in the future to support additional kinds of parent resources.</p>
<p>ParentRefs must be <em>distinct</em>. This means either that:</p>
<p>* They select different objects. If this is the case, then parentRef entries are distinct. In terms of fields, this means that the multi-part key defined by <code>group</code>, <code>kind</code>, <code>namespace</code>, and <code>name</code> must be unique across all parentRef entries in the Route. * They do not select different objects, but for each optional field used, each ParentRef that selects the same object must set the same set of optional fields to different values. If one ParentRef sets a combination of optional fields, all must set the same combination.</p>
<p>Some examples:</p>
<p>* If one ParentRef sets <code>sectionName</code>, all ParentRefs referencing the same object must also set <code>sectionName</code>. * If one ParentRef sets <code>port</code>, all ParentRefs referencing the same object must also set <code>port</code>. * If one ParentRef sets <code>sectionName</code> and <code>port</code>, all ParentRefs referencing the same object must also set <code>sectionName</code> and <code>port</code>.</p>
<p>It is possible to separately reference multiple distinct objects that may be collapsed by an implementation. For example, some implementations may choose to merge compatible Gateway Listeners together. If that is the case, the list of routes attached to those resources should also be merged.</p>
<p>Note that for ParentRefs that cross namespace boundaries, there are specific rules. Cross-namespace references are only valid if they are explicitly allowed by something in the namespace they are referring to. For example, Gateway has the AllowedRoutes field, and ReferenceGrant provides a generic way to enable other kinds of cross-namespace reference.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>parentRefs[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>ParentReference identifies an API object (usually a Gateway) that can be considered a parent of this resource (usually a route). There are two kinds of parent resources with "Core" support:</p>
<p>* Gateway (Gateway conformance profile) * Service (Mesh conformance profile, ClusterIP Services only)</p>
<p>This API may be extended in the future to support additional kinds of parent resources.</p>
<p>The API object must be valid in the cluster; the Group and Kind must be registered in the cluster for this reference to be valid.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>rules</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>Rules are a list of actions.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>rules[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>TLSRouteRule is the configuration for a given rule.</p></td>
</tr>
</tbody>
</table>

## .spec.parentRefs

Description
ParentRefs references the resources (usually Gateways) that a Route wants to be attached to. Note that the referenced parent resource needs to allow this for the attachment to be complete. For Gateways, that means the Gateway needs to allow attachment from Routes of this kind and namespace. For Services, that means the Service must either be in the same namespace for a "producer" route, or the mesh implementation must support and allow "consumer" routes for the referenced Service. ReferenceGrant is not applicable for governing ParentRefs to Services - it is not possible to create a "producer" route for a Service in a different namespace from the Route.

There are two kinds of parent resources with "Core" support:

- Gateway (Gateway conformance profile)

- Service (Mesh conformance profile, ClusterIP Services only)

This API may be extended in the future to support additional kinds of parent resources.

ParentRefs must be *distinct*. This means either that:

- They select different objects. If this is the case, then parentRef entries are distinct. In terms of fields, this means that the multi-part key defined by `group`, `kind`, `namespace`, and `name` must be unique across all parentRef entries in the Route.

- They do not select different objects, but for each optional field used, each ParentRef that selects the same object must set the same set of optional fields to different values. If one ParentRef sets a combination of optional fields, all must set the same combination.

Some examples:

- If one ParentRef sets `sectionName`, all ParentRefs referencing the same object must also set `sectionName`.

- If one ParentRef sets `port`, all ParentRefs referencing the same object must also set `port`.

- If one ParentRef sets `sectionName` and `port`, all ParentRefs referencing the same object must also set `sectionName` and `port`.

It is possible to separately reference multiple distinct objects that may be collapsed by an implementation. For example, some implementations may choose to merge compatible Gateway Listeners together. If that is the case, the list of routes attached to those resources should also be merged.

Note that for ParentRefs that cross namespace boundaries, there are specific rules. Cross-namespace references are only valid if they are explicitly allowed by something in the namespace they are referring to. For example, Gateway has the AllowedRoutes field, and ReferenceGrant provides a generic way to enable other kinds of cross-namespace reference.

Type
`array`

## .spec.parentRefs\[\]

Description
ParentReference identifies an API object (usually a Gateway) that can be considered a parent of this resource (usually a route). There are two kinds of parent resources with "Core" support:

- Gateway (Gateway conformance profile)

- Service (Mesh conformance profile, ClusterIP Services only)

This API may be extended in the future to support additional kinds of parent resources.

The API object must be valid in the cluster; the Group and Kind must be registered in the cluster for this reference to be valid.

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
<tr class="header">
<th style="text-align: left;">Property</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>group</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Group is the group of the referent. When unspecified, "gateway.networking.k8s.io" is inferred. To set the core API group (such as for a "Service" kind referent), Group must be explicitly set to "" (empty string).</p>
<p>Support: Core</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>kind</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Kind is kind of the referent.</p>
<p>There are two kinds of parent resources with "Core" support:</p>
<p>* Gateway (Gateway conformance profile) * Service (Mesh conformance profile, ClusterIP Services only)</p>
<p>Support for other resources is Implementation-Specific.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Name is the name of the referent.</p>
<p>Support: Core</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>namespace</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Namespace is the namespace of the referent. When unspecified, this refers to the local namespace of the Route.</p>
<p>Note that there are specific rules for ParentRefs which cross namespace boundaries. Cross-namespace references are only valid if they are explicitly allowed by something in the namespace they are referring to. For example: Gateway has the AllowedRoutes field, and ReferenceGrant provides a generic way to enable any other kind of cross-namespace reference.</p>
<p>Support: Core</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>port</code></p></td>
<td style="text-align: left;"><p><code>integer</code></p></td>
<td style="text-align: left;"><p>Port is the network port this Route targets. It can be interpreted differently based on the type of parent resource.</p>
<p>When the parent resource is a Gateway, this targets all listeners listening on the specified port that also support this kind of Route(and select this Route). It’s not recommended to set <code>Port</code> unless the networking behaviors specified in a Route must apply to a specific port as opposed to a listener(s) whose port(s) may be changed. When both Port and SectionName are specified, the name and port of the selected listener must match both specified values.</p>
<p>Implementations MAY choose to support other parent resources. Implementations supporting other types of parent resources MUST clearly document how/if Port is interpreted.</p>
<p>For the purpose of status, an attachment is considered successful as long as the parent resource accepts it partially. For example, Gateway listeners can restrict which Routes can attach to them by Route kind, namespace, or hostname. If 1 of 2 Gateway listeners accept attachment from the referencing Route, the Route MUST be considered successfully attached. If no Gateway listeners accept attachment from this Route, the Route MUST be considered detached from the Gateway.</p>
<p>Support: Extended</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>sectionName</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>SectionName is the name of a section within the target resource. In the following resources, SectionName is interpreted as the following:</p>
<p>* Gateway: Listener name. When both Port (experimental) and SectionName are specified, the name and port of the selected listener must match both specified values. * Service: Port name. When both Port (experimental) and SectionName are specified, the name and port of the selected listener must match both specified values.</p>
<p>Implementations MAY choose to support attaching Routes to other resources. If that is the case, they MUST clearly document how SectionName is interpreted.</p>
<p>When unspecified (empty string), this will reference the entire resource. For the purpose of status, an attachment is considered successful if at least one section in the parent resource accepts it. For example, Gateway listeners can restrict which Routes can attach to them by Route kind, namespace, or hostname. If 1 of 2 Gateway listeners accept attachment from the referencing Route, the Route MUST be considered successfully attached. If no Gateway listeners accept attachment from this Route, the Route MUST be considered detached from the Gateway.</p>
<p>Support: Core</p></td>
</tr>
</tbody>
</table>

## .spec.rules

Description
Rules are a list of actions.

Type
`array`

## .spec.rules\[\]

Description
TLSRouteRule is the configuration for a given rule.

Type
`object`

Required
- `backendRefs`

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
<td style="text-align: left;"><p><code>backendRefs</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>BackendRefs defines the backend(s) where matching requests should be sent. If unspecified or invalid (refers to a nonexistent resource or a Service with no endpoints), the rule performs no forwarding; if no filters are specified that would result in a response being sent, the underlying implementation must actively reject request attempts to this backend, by rejecting the connection. Request rejections must respect weight; if an invalid backend is requested to have 80% of requests, then 80% of requests must be rejected instead.</p>
<p>Support: Core for Kubernetes Service</p>
<p>Support: Extended for Kubernetes ServiceImport</p>
<p>Support: Implementation-specific for any other resource</p>
<p>Support for weight: Extended</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>backendRefs[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>BackendRef defines how a Route should forward a request to a Kubernetes resource.</p>
<p>Note that when a namespace different than the local namespace is specified, a ReferenceGrant object is required in the referent namespace to allow that namespace’s owner to accept the reference. See the ReferenceGrant documentation for details.</p>
<p>Note that when the BackendTLSPolicy object is enabled by the implementation, there are some extra rules about validity to consider here. See the fields where this struct is used for more information about the exact behavior.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Name is the name of the route rule. This name MUST be unique within a Route if it is set.</p></td>
</tr>
</tbody>
</table>

## .spec.rules\[\].backendRefs

Description
BackendRefs defines the backend(s) where matching requests should be sent. If unspecified or invalid (refers to a nonexistent resource or a Service with no endpoints), the rule performs no forwarding; if no filters are specified that would result in a response being sent, the underlying implementation must actively reject request attempts to this backend, by rejecting the connection. Request rejections must respect weight; if an invalid backend is requested to have 80% of requests, then 80% of requests must be rejected instead.

Support: Core for Kubernetes Service

Support: Extended for Kubernetes ServiceImport

Support: Implementation-specific for any other resource

Support for weight: Extended

Type
`array`

## .spec.rules\[\].backendRefs\[\]

Description
BackendRef defines how a Route should forward a request to a Kubernetes resource.

Note that when a namespace different than the local namespace is specified, a ReferenceGrant object is required in the referent namespace to allow that namespace’s owner to accept the reference. See the ReferenceGrant documentation for details.

Note that when the BackendTLSPolicy object is enabled by the implementation, there are some extra rules about validity to consider here. See the fields where this struct is used for more information about the exact behavior.

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
<tr class="header">
<th style="text-align: left;">Property</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>group</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Group is the group of the referent. For example, "gateway.networking.k8s.io". When unspecified or empty string, core API group is inferred.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>kind</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Kind is the Kubernetes resource kind of the referent. For example "Service".</p>
<p>Defaults to "Service" when not specified.</p>
<p>ExternalName services can refer to CNAME DNS records that may live outside of the cluster and as such are difficult to reason about in terms of conformance. They also may not be safe to forward to (see CVE-2021-25740 for more information). Implementations SHOULD NOT support ExternalName Services.</p>
<p>Support: Core (Services with a type other than ExternalName)</p>
<p>Support: Implementation-specific (Services with type ExternalName)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Name is the name of the referent.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>namespace</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Namespace is the namespace of the backend. When unspecified, the local namespace is inferred.</p>
<p>Note that when a namespace different than the local namespace is specified, a ReferenceGrant object is required in the referent namespace to allow that namespace’s owner to accept the reference. See the ReferenceGrant documentation for details.</p>
<p>Support: Core</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>port</code></p></td>
<td style="text-align: left;"><p><code>integer</code></p></td>
<td style="text-align: left;"><p>Port specifies the destination port number to use for this resource. Port is required when the referent is a Kubernetes Service. In this case, the port number is the service port number, not the target port. For other resources, destination port might be derived from the referent resource or this field.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>weight</code></p></td>
<td style="text-align: left;"><p><code>integer</code></p></td>
<td style="text-align: left;"><p>Weight specifies the proportion of requests forwarded to the referenced backend. This is computed as weight/(sum of all weights in this BackendRefs list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. Weight is not a percentage and the sum of weights does not need to equal 100.</p>
<p>If only one backend is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weight is set to 0, no traffic should be forwarded for this entry. If unspecified, weight defaults to 1.</p>
<p>Support for this field varies based on the context where used.</p></td>
</tr>
</tbody>
</table>

## .status

Description
Status defines the current state of TLSRoute.

Type
`object`

Required
- `parents`

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
<td style="text-align: left;"><p><code>parents</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>Parents is a list of parent resources (usually Gateways) that are associated with the route, and the status of the route with respect to each parent. When this route attaches to a parent, the controller that manages the parent must add an entry to this list when the controller first sees the route and should update the entry as appropriate when the route or gateway is modified.</p>
<p>Note that parent references that cannot be resolved by an implementation of this API will not be added to this list. Implementations of this API can only populate Route status for the Gateways/parent resources they are responsible for.</p>
<p>A maximum of 32 Gateways will be represented in this list. An empty list means the route has not been attached to any Gateway.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>parents[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>RouteParentStatus describes the status of a route with respect to an associated Parent.</p></td>
</tr>
</tbody>
</table>

## .status.parents

Description
Parents is a list of parent resources (usually Gateways) that are associated with the route, and the status of the route with respect to each parent. When this route attaches to a parent, the controller that manages the parent must add an entry to this list when the controller first sees the route and should update the entry as appropriate when the route or gateway is modified.

Note that parent references that cannot be resolved by an implementation of this API will not be added to this list. Implementations of this API can only populate Route status for the Gateways/parent resources they are responsible for.

A maximum of 32 Gateways will be represented in this list. An empty list means the route has not been attached to any Gateway.

Type
`array`

## .status.parents\[\]

Description
RouteParentStatus describes the status of a route with respect to an associated Parent.

Type
`object`

Required
- `conditions`

- `controllerName`

- `parentRef`

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
<td style="text-align: left;"><p><code>conditions</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>Conditions describes the status of the route with respect to the Gateway. Note that the route’s availability is also subject to the Gateway’s own status conditions and listener status.</p>
<p>If the Route’s ParentRef specifies an existing Gateway that supports Routes of this kind AND that Gateway’s controller has sufficient access, then that Gateway’s controller MUST set the "Accepted" condition on the Route, to indicate whether the route has been accepted or rejected by the Gateway, and why.</p>
<p>A Route MUST be considered "Accepted" if at least one of the Route’s rules is implemented by the Gateway.</p>
<p>There are a number of cases where the "Accepted" condition may not be set due to lack of controller visibility, that includes when:</p>
<p>* The Route refers to a nonexistent parent. * The Route is of a type that the controller does not support. * The Route is in a namespace to which the controller does not have access.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>conditions[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>Condition contains details for one aspect of the current state of this API Resource.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>controllerName</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>ControllerName is a domain/path string that indicates the name of the controller that wrote this status. This corresponds with the controllerName field on GatewayClass.</p>
<p>Example: "example.net/gateway-controller".</p>
<p>The format of this field is DOMAIN "/" PATH, where DOMAIN and PATH are valid Kubernetes names (<a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names">https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names</a>).</p>
<p>Controllers MUST populate this field when writing status. Controllers should ensure that entries to status populated with their ControllerName are cleaned up when they are no longer necessary.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>parentRef</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>ParentRef corresponds with a ParentRef in the spec that this RouteParentStatus struct describes the status of.</p></td>
</tr>
</tbody>
</table>

## .status.parents\[\].conditions

Description
Conditions describes the status of the route with respect to the Gateway. Note that the route’s availability is also subject to the Gateway’s own status conditions and listener status.

If the Route’s ParentRef specifies an existing Gateway that supports Routes of this kind AND that Gateway’s controller has sufficient access, then that Gateway’s controller MUST set the "Accepted" condition on the Route, to indicate whether the route has been accepted or rejected by the Gateway, and why.

A Route MUST be considered "Accepted" if at least one of the Route’s rules is implemented by the Gateway.

There are a number of cases where the "Accepted" condition may not be set due to lack of controller visibility, that includes when:

- The Route refers to a nonexistent parent.

- The Route is of a type that the controller does not support.

- The Route is in a namespace to which the controller does not have access.

Type
`array`

## .status.parents\[\].conditions\[\]

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

| Property             | Type      | Description                                                                                                                                                                                                                                                                                                                     |
|----------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `lastTransitionTime` | `string`  | lastTransitionTime is the last time the condition transitioned from one status to another. This should be when the underlying condition changed. If that is not known, then using the time when the API field changed is acceptable.                                                                                            |
| `message`            | `string`  | message is a human readable message indicating details about the transition. This may be an empty string.                                                                                                                                                                                                                       |
| `observedGeneration` | `integer` | observedGeneration represents the .metadata.generation that the condition was set based upon. For instance, if .metadata.generation is currently 12, but the .status.conditions\[x\].observedGeneration is 9, the condition is out of date with respect to the current state of the instance.                                   |
| `reason`             | `string`  | reason contains a programmatic identifier indicating the reason for the condition’s last transition. Producers of specific condition types may define expected values and meanings for this field, and whether the values are considered a guaranteed API. The value should be a CamelCase string. This field may not be empty. |
| `status`             | `string`  | status of the condition, one of True, False, Unknown.                                                                                                                                                                                                                                                                           |
| `type`               | `string`  | type of condition in CamelCase or in foo.example.com/CamelCase.                                                                                                                                                                                                                                                                 |

## .status.parents\[\].parentRef

Description
ParentRef corresponds with a ParentRef in the spec that this RouteParentStatus struct describes the status of.

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
<tr class="header">
<th style="text-align: left;">Property</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>group</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Group is the group of the referent. When unspecified, "gateway.networking.k8s.io" is inferred. To set the core API group (such as for a "Service" kind referent), Group must be explicitly set to "" (empty string).</p>
<p>Support: Core</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>kind</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Kind is kind of the referent.</p>
<p>There are two kinds of parent resources with "Core" support:</p>
<p>* Gateway (Gateway conformance profile) * Service (Mesh conformance profile, ClusterIP Services only)</p>
<p>Support for other resources is Implementation-Specific.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Name is the name of the referent.</p>
<p>Support: Core</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>namespace</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>Namespace is the namespace of the referent. When unspecified, this refers to the local namespace of the Route.</p>
<p>Note that there are specific rules for ParentRefs which cross namespace boundaries. Cross-namespace references are only valid if they are explicitly allowed by something in the namespace they are referring to. For example: Gateway has the AllowedRoutes field, and ReferenceGrant provides a generic way to enable any other kind of cross-namespace reference.</p>
<p>Support: Core</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>port</code></p></td>
<td style="text-align: left;"><p><code>integer</code></p></td>
<td style="text-align: left;"><p>Port is the network port this Route targets. It can be interpreted differently based on the type of parent resource.</p>
<p>When the parent resource is a Gateway, this targets all listeners listening on the specified port that also support this kind of Route(and select this Route). It’s not recommended to set <code>Port</code> unless the networking behaviors specified in a Route must apply to a specific port as opposed to a listener(s) whose port(s) may be changed. When both Port and SectionName are specified, the name and port of the selected listener must match both specified values.</p>
<p>Implementations MAY choose to support other parent resources. Implementations supporting other types of parent resources MUST clearly document how/if Port is interpreted.</p>
<p>For the purpose of status, an attachment is considered successful as long as the parent resource accepts it partially. For example, Gateway listeners can restrict which Routes can attach to them by Route kind, namespace, or hostname. If 1 of 2 Gateway listeners accept attachment from the referencing Route, the Route MUST be considered successfully attached. If no Gateway listeners accept attachment from this Route, the Route MUST be considered detached from the Gateway.</p>
<p>Support: Extended</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>sectionName</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>SectionName is the name of a section within the target resource. In the following resources, SectionName is interpreted as the following:</p>
<p>* Gateway: Listener name. When both Port (experimental) and SectionName are specified, the name and port of the selected listener must match both specified values. * Service: Port name. When both Port (experimental) and SectionName are specified, the name and port of the selected listener must match both specified values.</p>
<p>Implementations MAY choose to support attaching Routes to other resources. If that is the case, they MUST clearly document how SectionName is interpreted.</p>
<p>When unspecified (empty string), this will reference the entire resource. For the purpose of status, an attachment is considered successful if at least one section in the parent resource accepts it. For example, Gateway listeners can restrict which Routes can attach to them by Route kind, namespace, or hostname. If 1 of 2 Gateway listeners accept attachment from the referencing Route, the Route MUST be considered successfully attached. If no Gateway listeners accept attachment from this Route, the Route MUST be considered detached from the Gateway.</p>
<p>Support: Core</p></td>
</tr>
</tbody>
</table>

# API endpoints

The following API endpoints are available:

- `/apis/gateway.networking.k8s.io/v1/tlsroutes`

  - `GET`: list objects of kind TLSRoute

- `/apis/gateway.networking.k8s.io/v1/namespaces/{namespace}/tlsroutes`

  - `DELETE`: delete collection of TLSRoute

  - `GET`: list objects of kind TLSRoute

  - `POST`: create a TLSRoute

- `/apis/gateway.networking.k8s.io/v1/namespaces/{namespace}/tlsroutes/{name}`

  - `DELETE`: delete a TLSRoute

  - `GET`: read the specified TLSRoute

  - `PATCH`: partially update the specified TLSRoute

  - `PUT`: replace the specified TLSRoute

- `/apis/gateway.networking.k8s.io/v1/namespaces/{namespace}/tlsroutes/{name}/status`

  - `GET`: read status of the specified TLSRoute

  - `PATCH`: partially update status of the specified TLSRoute

  - `PUT`: replace status of the specified TLSRoute

## /apis/gateway.networking.k8s.io/v1/tlsroutes

HTTP method
`GET`

Description
list objects of kind TLSRoute

| HTTP code          | Reponse body                                                                            |
|--------------------|-----------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRouteList`](../objects/index.xml#io-k8s-networking-gateway-v1-TLSRouteList) schema |
| 401 - Unauthorized | Empty                                                                                   |

HTTP responses

## /apis/gateway.networking.k8s.io/v1/namespaces/{namespace}/tlsroutes

HTTP method
`DELETE`

Description
delete collection of TLSRoute

| HTTP code          | Reponse body                                                                        |
|--------------------|-------------------------------------------------------------------------------------|
| 200 - OK           | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty                                                                               |

HTTP responses

HTTP method
`GET`

Description
list objects of kind TLSRoute

| HTTP code          | Reponse body                                                                            |
|--------------------|-----------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRouteList`](../objects/index.xml#io-k8s-networking-gateway-v1-TLSRouteList) schema |
| 401 - Unauthorized | Empty                                                                                   |

HTTP responses

HTTP method
`POST`

Description
create a TLSRoute

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                 | Description |
|-----------|----------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 201 - Created      | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 202 - Accepted     | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses

## /apis/gateway.networking.k8s.io/v1/namespaces/{namespace}/tlsroutes/{name}

| Parameter | Type     | Description          |
|-----------|----------|----------------------|
| `name`    | `string` | name of the TLSRoute |

Global path parameters

HTTP method
`DELETE`

Description
delete a TLSRoute

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
read the specified TLSRoute

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified TLSRoute

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses

HTTP method
`PUT`

Description
replace the specified TLSRoute

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                 | Description |
|-----------|----------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 201 - Created      | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses

## /apis/gateway.networking.k8s.io/v1/namespaces/{namespace}/tlsroutes/{name}/status

| Parameter | Type     | Description          |
|-----------|----------|----------------------|
| `name`    | `string` | name of the TLSRoute |

Global path parameters

HTTP method
`GET`

Description
read status of the specified TLSRoute

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses

HTTP method
`PATCH`

Description
partially update status of the specified TLSRoute

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses

HTTP method
`PUT`

Description
replace status of the specified TLSRoute

| Parameter         | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dryRun`          | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type                                                                                                                 | Description |
|-----------|----------------------------------------------------------------------------------------------------------------------|-------------|
| `body`    | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |             |

Body parameters

| HTTP code          | Reponse body                                                                                                         |
|--------------------|----------------------------------------------------------------------------------------------------------------------|
| 200 - OK           | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 201 - Created      | [`TLSRoute`](../network_apis/tlsroute-gateway-networking-k8s-io-v1.xml#tlsroute-gateway-networking-k8s-io-v1) schema |
| 401 - Unauthorized | Empty                                                                                                                |

HTTP responses
