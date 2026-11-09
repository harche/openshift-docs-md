Description
MutatingAdmissionPolicy describes the definition of an admission mutation policy that mutates the object coming into admission chain.

Type
`object`

# Specification

| Property | Type | Description |
|----|----|----|
| `apiVersion` | `string` | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources> |
| `kind` | `string` | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds> |
| `metadata` | [`ObjectMeta`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-ObjectMeta) | metadata is the standard object metadata; More info: <https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata>. |
| `spec` | `object` | MutatingAdmissionPolicySpec defines the desired behavior of the admission policy. |

## .spec

Description
MutatingAdmissionPolicySpec defines the desired behavior of the admission policy.

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
<td style="text-align: left;"><p><code>failurePolicy</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>failurePolicy defines how to handle failures for the admission policy. Failures can occur from CEL expression parse errors, type check errors, runtime errors and invalid or mis-configured policy definitions or bindings.</p>
<p>A policy is invalid if paramKind refers to a non-existent Kind. A binding is invalid if paramRef.name refers to a non-existent resource.</p>
<p>failurePolicy does not define how validations that evaluate to false are handled.</p>
<p>Allowed values are Ignore or Fail. Defaults to Fail.</p>
<p>Possible enum values: - <code>"Fail"</code> means that an error calling the webhook causes the admission to fail. - <code>"Ignore"</code> means that an error calling the webhook is ignored.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>matchConditions</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>matchConditions is a list of conditions that must be met for a request to be validated. Match conditions filter requests that have already been matched by the matchConstraints. An empty list of matchConditions matches all requests. There are a maximum of 64 match conditions allowed.</p>
<p>If a parameter object is provided, it can be accessed via the <code>params</code> handle in the same manner as validation expressions.</p>
<p>The exact matching logic is (in order): 1. If ANY matchCondition evaluates to FALSE, the policy is skipped. 2. If ALL matchConditions evaluate to TRUE, the policy is evaluated. 3. If any matchCondition evaluates to an error (but none are FALSE): - If failurePolicy=Fail, reject the request - If failurePolicy=Ignore, the policy is skipped</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>matchConditions[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>MatchCondition represents a condition which must by fulfilled for a request to be sent to a webhook.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>matchConstraints</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>MatchResources decides whether to run the admission control policy on an object based on whether it meets the match criteria. The exclude rules take precedence over include rules (if a resource matches both, it is excluded)</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>mutations</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>mutations contain operations to perform on matching objects. mutations may not be empty; a minimum of one mutation is required. mutations are evaluated in order, and are reinvoked according to the reinvocationPolicy. The mutations of a policy are invoked for each binding of this policy and reinvocation of mutations occurs on a per binding basis.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>mutations[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>Mutation specifies the CEL expression which is used to apply the Mutation.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>paramKind</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>ParamKind is a tuple of Group Kind and Version.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>reinvocationPolicy</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>reinvocationPolicy indicates whether mutations may be called multiple times per MutatingAdmissionPolicyBinding as part of a single admission evaluation. Allowed values are "Never" and "IfNeeded".</p>
<p>Never: These mutations will not be called more than once per binding in a single admission evaluation.</p>
<p>IfNeeded: These mutations may be invoked more than once per binding for a single admission request and there is no guarantee of order with respect to other admission plugins, admission webhooks, bindings of this policy and admission policies. Mutations are only reinvoked when mutations change the object after this mutation is invoked. Required.</p>
<p>Possible enum values: - <code>"IfNeeded"</code> indicates that the mutation may be called at least one additional time as part of the admission evaluation if the object being admitted is modified by other admission plugins after the initial mutation call. - <code>"Never"</code> indicates that the mutation must not be called more than once in a single admission evaluation.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>variables</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>variables contain definitions of variables that can be used in composition of other expressions. Each variable is defined as a named CEL expression. The variables defined here will be available under <code>variables</code> in other expressions of the policy except matchConditions because matchConditions are evaluated before the rest of the policy.</p>
<p>The expression of a variable can refer to other variables defined earlier in the list but not those after. Thus, variables must be sorted by the order of first appearance and acyclic.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>variables[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>Variable is the definition of a variable that is used for composition. A variable is defined as a named expression.</p></td>
</tr>
</tbody>
</table>

## .spec.matchConditions

Description
matchConditions is a list of conditions that must be met for a request to be validated. Match conditions filter requests that have already been matched by the matchConstraints. An empty list of matchConditions matches all requests. There are a maximum of 64 match conditions allowed.

If a parameter object is provided, it can be accessed via the `params` handle in the same manner as validation expressions.

The exact matching logic is (in order): 1. If ANY matchCondition evaluates to FALSE, the policy is skipped. 2. If ALL matchConditions evaluate to TRUE, the policy is evaluated. 3. If any matchCondition evaluates to an error (but none are FALSE): - If failurePolicy=Fail, reject the request - If failurePolicy=Ignore, the policy is skipped

Type
`array`

## .spec.matchConditions\[\]

Description
MatchCondition represents a condition which must by fulfilled for a request to be sent to a webhook.

Type
`object`

Required
- `name`

- `expression`

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
<td style="text-align: left;"><p><code>expression</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>expression represents the expression which will be evaluated by CEL. Must evaluate to bool. CEL expressions have access to the contents of the AdmissionRequest and Authorizer, organized into CEL variables:</p>
<p>'object' - The object from the incoming request. The value is null for DELETE requests. 'oldObject' - The existing object. The value is null for CREATE requests. 'request' - Attributes of the admission request(/pkg/apis/admission/types.go#AdmissionRequest). 'authorizer' - A CEL Authorizer. May be used to perform authorization checks for the principal (user or service account) of the request. See <a href="https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz">https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz</a> 'authorizer.requestResource' - A CEL ResourceCheck constructed from the 'authorizer' and configured with the request resource. Documentation on CEL: <a href="https://kubernetes.io/docs/reference/using-api/cel/">https://kubernetes.io/docs/reference/using-api/cel/</a></p>
<p>Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>name</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>name is an identifier for this match condition, used for strategic merging of MatchConditions, as well as providing an identifier for logging purposes. A good name should be descriptive of the associated expression. Name must be a qualified name consisting of alphanumeric characters, '-', '<em>' or '.', and must start and end with an alphanumeric character (e.g. 'MyName', or 'my.name', or '123-abc', regex used for validation is '([A-Za-z0-9][-A-Za-z0-9</em>.]*)?[A-Za-z0-9]') with an optional DNS subdomain prefix and '/' (e.g. 'example.com/MyName')</p>
<p>Required.</p></td>
</tr>
</tbody>
</table>

## .spec.matchConstraints

Description
MatchResources decides whether to run the admission control policy on an object based on whether it meets the match criteria. The exclude rules take precedence over include rules (if a resource matches both, it is excluded)

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
<td style="text-align: left;"><p><code>excludeResourceRules</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>excludeResourceRules describes what operations on what resources/subresources the ValidatingAdmissionPolicy should not care about. The exclude rules take precedence over include rules (if a resource matches both, it is excluded)</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>excludeResourceRules[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>NamedRuleWithOperations is a tuple of Operations and Resources with ResourceNames.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>matchPolicy</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>matchPolicy defines how the "MatchResources" list is used to match incoming requests. Allowed values are "Exact" or "Equivalent".</p>
<p>- Exact: match a request only if it exactly matches a specified rule. For example, if deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, but "rules" only included <code>apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]</code>, a request to apps/v1beta1 or extensions/v1beta1 would not be sent to the ValidatingAdmissionPolicy.</p>
<p>- Equivalent: match a request if modifies a resource listed in rules, even via another API group or version. For example, if deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, and "rules" only included <code>apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]</code>, a request to apps/v1beta1 or extensions/v1beta1 would be converted to apps/v1 and sent to the ValidatingAdmissionPolicy.</p>
<p>Defaults to "Equivalent"</p>
<p>Possible enum values: - <code>"Equivalent"</code> means requests should be sent to the webhook if they modify a resource listed in rules via another API group or version. - <code>"Exact"</code> means requests should only be sent to the webhook if they exactly match a given rule.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>namespaceSelector</code></p></td>
<td style="text-align: left;"><p><a href="../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-LabelSelector"><code>LabelSelector</code></a></p></td>
<td style="text-align: left;"><p>namespaceSelector decides whether to run the admission control policy on an object based on whether the namespace for that object matches the selector. If the object itself is a namespace, the matching is performed on object.metadata.labels. If the object is another cluster scoped resource, it never skips the policy.</p>
<p>For example, to run the webhook on any objects whose namespace is not associated with "runlevel" of "0" or "1"; you will set the selector as follows: "namespaceSelector": { "matchExpressions": [ { "key": "runlevel", "operator": "NotIn", "values": [ "0", "1" ] } ] }</p>
<p>If instead you want to only run the policy on any objects whose namespace is associated with the "environment" of "prod" or "staging"; you will set the selector as follows: "namespaceSelector": { "matchExpressions": [ { "key": "environment", "operator": "In", "values": [ "prod", "staging" ] } ] }</p>
<p>See <a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/">https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/</a> for more examples of label selectors.</p>
<p>Default to the empty LabelSelector, which matches everything.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>objectSelector</code></p></td>
<td style="text-align: left;"><p><a href="../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-LabelSelector"><code>LabelSelector</code></a></p></td>
<td style="text-align: left;"><p>objectSelector decides whether to run the validation based on if the object has matching labels. objectSelector is evaluated against both the oldObject and newObject that would be sent to the cel validation, and is considered to match if either object matches the selector. A null object (oldObject in the case of create, or newObject in the case of delete) or an object that cannot have labels (like a DeploymentRollback or a PodProxyOptions object) is not considered to match. Use the object selector only if the webhook is opt-in, because end users may skip the admission webhook by setting the labels. Default to the empty LabelSelector, which matches everything.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>resourceRules</code></p></td>
<td style="text-align: left;"><p><code>array</code></p></td>
<td style="text-align: left;"><p>resourceRules describes what operations on what resources/subresources the ValidatingAdmissionPolicy matches. The policy cares about an operation if it matches <em>any</em> Rule.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>resourceRules[]</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>NamedRuleWithOperations is a tuple of Operations and Resources with ResourceNames.</p></td>
</tr>
</tbody>
</table>

## .spec.matchConstraints.excludeResourceRules

Description
excludeResourceRules describes what operations on what resources/subresources the ValidatingAdmissionPolicy should not care about. The exclude rules take precedence over include rules (if a resource matches both, it is excluded)

Type
`array`

## .spec.matchConstraints.excludeResourceRules\[\]

Description
NamedRuleWithOperations is a tuple of Operations and Resources with ResourceNames.

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
<td style="text-align: left;"><p><code>apiGroups</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>apiGroups is the API groups the resources belong to. '<strong>' is all groups. If '</strong>' is present, the length of the slice must be one. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>apiVersions</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>apiVersions is the API versions the resources belong to. '<strong>' is all versions. If '</strong>' is present, the length of the slice must be one. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>operations</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>operations is the operations the admission hook cares about - CREATE, UPDATE, DELETE, CONNECT or * for all of those operations and any future admission operations that are added. If '*' is present, the length of the slice must be one. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>resourceNames</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>resourceNames is an optional white list of names that the rule applies to. An empty set means that everything is allowed.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>resources</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>resources is a list of resources this rule applies to.</p>
<p>For example: 'pods' means pods. 'pods/log' means the log subresource of pods. '*' means all resources, but not subresources. 'pods/*' means all subresources of pods. '*/scale' means all scale subresources. '*/*' means all resources and their subresources.</p>
<p>If wildcard is present, the validation rule will ensure resources do not overlap with each other.</p>
<p>Depending on the enclosing object, subresources might not be allowed. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>scope</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>scope specifies the scope of this rule. Valid values are "Cluster", "Namespaced", and "*" "Cluster" means that only cluster-scoped resources will match this rule. Namespace API objects are cluster-scoped. "Namespaced" means that only namespaced resources will match this rule. "*" means that there are no scope restrictions. Subresources match the scope of their parent resource. Default is "*".</p>
<p>Possible enum values: - <code>"*"</code> means that all scopes are included. - <code>"Cluster"</code> means that scope is limited to cluster-scoped objects. Namespace objects are cluster-scoped. - <code>"Namespaced"</code> means that scope is limited to namespaced objects.</p></td>
</tr>
</tbody>
</table>

## .spec.matchConstraints.resourceRules

Description
resourceRules describes what operations on what resources/subresources the ValidatingAdmissionPolicy matches. The policy cares about an operation if it matches *any* Rule.

Type
`array`

## .spec.matchConstraints.resourceRules\[\]

Description
NamedRuleWithOperations is a tuple of Operations and Resources with ResourceNames.

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
<td style="text-align: left;"><p><code>apiGroups</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>apiGroups is the API groups the resources belong to. '<strong>' is all groups. If '</strong>' is present, the length of the slice must be one. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>apiVersions</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>apiVersions is the API versions the resources belong to. '<strong>' is all versions. If '</strong>' is present, the length of the slice must be one. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>operations</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>operations is the operations the admission hook cares about - CREATE, UPDATE, DELETE, CONNECT or * for all of those operations and any future admission operations that are added. If '*' is present, the length of the slice must be one. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>resourceNames</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>resourceNames is an optional white list of names that the rule applies to. An empty set means that everything is allowed.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>resources</code></p></td>
<td style="text-align: left;"><p><code>array (string)</code></p></td>
<td style="text-align: left;"><p>resources is a list of resources this rule applies to.</p>
<p>For example: 'pods' means pods. 'pods/log' means the log subresource of pods. '<strong>' means all resources, but not subresources. 'pods/</strong>' means all subresources of pods. '<strong>/scale' means all scale subresources. '</strong>/*' means all resources and their subresources.</p>
<p>If wildcard is present, the validation rule will ensure resources do not overlap with each other.</p>
<p>Depending on the enclosing object, subresources might not be allowed. Required.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>scope</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>scope specifies the scope of this rule. Valid values are "Cluster", "Namespaced", and "*" "Cluster" means that only cluster-scoped resources will match this rule. Namespace API objects are cluster-scoped. "Namespaced" means that only namespaced resources will match this rule. "*" means that there are no scope restrictions. Subresources match the scope of their parent resource. Default is "*".</p>
<p>Possible enum values: - <code>"*"</code> means that all scopes are included. - <code>"Cluster"</code> means that scope is limited to cluster-scoped objects. Namespace objects are cluster-scoped. - <code>"Namespaced"</code> means that scope is limited to namespaced objects.</p></td>
</tr>
</tbody>
</table>

## .spec.mutations

Description
mutations contain operations to perform on matching objects. mutations may not be empty; a minimum of one mutation is required. mutations are evaluated in order, and are reinvoked according to the reinvocationPolicy. The mutations of a policy are invoked for each binding of this policy and reinvocation of mutations occurs on a per binding basis.

Type
`array`

## .spec.mutations\[\]

Description
Mutation specifies the CEL expression which is used to apply the Mutation.

Type
`object`

Required
- `patchType`

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
<td style="text-align: left;"><p><code>applyConfiguration</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>ApplyConfiguration defines the desired configuration values of an object.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>jsonPatch</code></p></td>
<td style="text-align: left;"><p><code>object</code></p></td>
<td style="text-align: left;"><p>JSONPatch defines a JSON Patch.</p></td>
</tr>
<tr>
<td style="text-align: left;"><p><code>patchType</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>patchType indicates the patch strategy used. Allowed values are "ApplyConfiguration" and "JSONPatch". Required.</p>
<p>Possible enum values: - <code>"ApplyConfiguration"</code> ApplyConfiguration indicates that the mutation is using apply configuration to mutate the object. - <code>"JSONPatch"</code> JSONPatch indicates that the object is mutated through JSON Patch.</p></td>
</tr>
</tbody>
</table>

## .spec.mutations\[\].applyConfiguration

Description
ApplyConfiguration defines the desired configuration values of an object.

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
<td style="text-align: left;"><p><code>expression</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>expression will be evaluated by CEL to create an apply configuration. ref: <a href="https://github.com/google/cel-spec">https://github.com/google/cel-spec</a></p>
<p>Apply configurations are declared in CEL using object initialization. For example, this CEL expression returns an apply configuration to set a single field:</p>
<p>Object{ spec: Object.spec{ serviceAccountName: "example" } }</p>
<p>Apply configurations may not modify atomic structs, maps or arrays due to the risk of accidental deletion of values not included in the apply configuration.</p>
<p>CEL expressions have access to the object types needed to create apply configurations:</p>
<p>- 'Object' - CEL type of the resource object. - 'Object.&lt;fieldName&gt;' - CEL type of object field (such as 'Object.spec') - 'Object.&lt;fieldName1&gt;.&lt;fieldName2&gt;…​&lt;fieldNameN&gt;` - CEL type of nested field (such as 'Object.spec.containers')</p>
<p>CEL expressions have access to the contents of the API request, organized into CEL variables as well as some other useful variables:</p>
<p>- 'object' - The object from the incoming request. The value is null for DELETE requests. - 'oldObject' - The existing object. The value is null for CREATE requests. - 'request' - Attributes of the API request([ref](/pkg/apis/admission/types.go#AdmissionRequest)). - 'params' - Parameter resource referred to by the policy binding being evaluated. Only populated if the policy has a ParamKind. - 'namespaceObject' - The namespace object that the incoming object belongs to. The value is null for cluster-scoped resources. - 'variables' - Map of composited variables, from its name to its lazily evaluated value. For example, a variable named 'foo' can be accessed as 'variables.foo'. - 'authorizer' - A CEL Authorizer. May be used to perform authorization checks for the principal (user or service account) of the request. See <a href="https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz">https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz</a> - 'authorizer.requestResource' - A CEL ResourceCheck constructed from the 'authorizer' and configured with the request resource.</p>
<p>The <code>apiVersion</code>, <code>kind</code>, <code>metadata.name</code> and <code>metadata.generateName</code> are always accessible from the root of the object. No other metadata properties are accessible.</p>
<p>Only property names of the form <code>[a-zA-Z_.-/][a-zA-Z0-9_.-/]*</code> are accessible. Required.</p></td>
</tr>
</tbody>
</table>

## .spec.mutations\[\].jsonPatch

Description
JSONPatch defines a JSON Patch.

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
<td style="text-align: left;"><p><code>expression</code></p></td>
<td style="text-align: left;"><p><code>string</code></p></td>
<td style="text-align: left;"><p>expression will be evaluated by CEL to create a [JSON patch](<a href="https://jsonpatch.com/">https://jsonpatch.com/</a>). ref: <a href="https://github.com/google/cel-spec">https://github.com/google/cel-spec</a></p>
<p>expression must return an array of JSONPatch values.</p>
<p>For example, this CEL expression returns a JSON patch to conditionally modify a value:</p>
<p>[ JSONPatch{op: "test", path: "/spec/example", value: "Red"}, JSONPatch{op: "replace", path: "/spec/example", value: "Green"} ]</p>
<p>To define an object for the patch value, use Object types. For example:</p>
<p>[ JSONPatch{ op: "add", path: "/spec/selector", value: Object.spec.selector{matchLabels: {"environment": "test"}} } ]</p>
<p>To use strings containing '/' and '~' as JSONPatch path keys, use "jsonpatch.escapeKey". For example:</p>
<p>[ JSONPatch{ op: "add", path: "/metadata/labels/" + jsonpatch.escapeKey("example.com/environment"), value: "test" }, ]</p>
<p>CEL expressions have access to the types needed to create JSON patches and objects:</p>
<p>- 'JSONPatch' - CEL type of JSON Patch operations. JSONPatch has the fields 'op', 'from', 'path' and 'value'. See [JSON patch](<a href="https://jsonpatch.com/">https://jsonpatch.com/</a>) for more details. The 'value' field may be set to any of: string, integer, array, map or object. If set, the 'path' and 'from' fields must be set to a [JSON pointer](<a href="https://datatracker.ietf.org/doc/html/rfc6901/">https://datatracker.ietf.org/doc/html/rfc6901/</a>) string, where the 'jsonpatch.escapeKey()' CEL function may be used to escape path keys containing '/' and '~'. - 'Object' - CEL type of the resource object. - 'Object.&lt;fieldName&gt;' - CEL type of object field (such as 'Object.spec') - 'Object.&lt;fieldName1&gt;.&lt;fieldName2&gt;…​&lt;fieldNameN&gt;` - CEL type of nested field (such as 'Object.spec.containers')</p>
<p>CEL expressions have access to the contents of the API request, organized into CEL variables as well as some other useful variables:</p>
<p>- 'object' - The object from the incoming request. The value is null for DELETE requests. - 'oldObject' - The existing object. The value is null for CREATE requests. - 'request' - Attributes of the API request([ref](/pkg/apis/admission/types.go#AdmissionRequest)). - 'params' - Parameter resource referred to by the policy binding being evaluated. Only populated if the policy has a ParamKind. - 'namespaceObject' - The namespace object that the incoming object belongs to. The value is null for cluster-scoped resources. - 'variables' - Map of composited variables, from its name to its lazily evaluated value. For example, a variable named 'foo' can be accessed as 'variables.foo'. - 'authorizer' - A CEL Authorizer. May be used to perform authorization checks for the principal (user or service account) of the request. See <a href="https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz">https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz</a> - 'authorizer.requestResource' - A CEL ResourceCheck constructed from the 'authorizer' and configured with the request resource.</p>
<p>CEL expressions have access to [Kubernetes CEL function libraries](<a href="https://kubernetes.io/docs/reference/using-api/cel/#cel-options-language-features-and-libraries">https://kubernetes.io/docs/reference/using-api/cel/#cel-options-language-features-and-libraries</a>) as well as:</p>
<p>- 'jsonpatch.escapeKey' - Performs JSONPatch key escaping. '~' and '/' are escaped as '~0' and '~1' respectively).</p>
<p>Only property names of the form <code>[a-zA-Z_.-/][a-zA-Z0-9_.-/]*</code> are accessible. Required.</p></td>
</tr>
</tbody>
</table>

## .spec.paramKind

Description
ParamKind is a tuple of Group Kind and Version.

Type
`object`

| Property | Type | Description |
|----|----|----|
| `apiVersion` | `string` | apiVersion is the API group version the resources belong to. In format of "group/version". Required. |
| `kind` | `string` | kind is the API kind the resources belong to. Required. |

## .spec.variables

Description
variables contain definitions of variables that can be used in composition of other expressions. Each variable is defined as a named CEL expression. The variables defined here will be available under `variables` in other expressions of the policy except matchConditions because matchConditions are evaluated before the rest of the policy.

The expression of a variable can refer to other variables defined earlier in the list but not those after. Thus, variables must be sorted by the order of first appearance and acyclic.

Type
`array`

## .spec.variables\[\]

Description
Variable is the definition of a variable that is used for composition. A variable is defined as a named expression.

Type
`object`

Required
- `name`

- `expression`

| Property | Type | Description |
|----|----|----|
| `expression` | `string` | expression is the expression that will be evaluated as the value of the variable. The CEL expression has access to the same identifiers as the CEL expressions in Validation. |
| `name` | `string` | name is the name of the variable. The name must be a valid CEL identifier and unique among all variables. The variable can be accessed in other expressions through `variables` For example, if name is "foo", the variable will be available as `variables.foo` |

# API endpoints

The following API endpoints are available:

- `/apis/admissionregistration.k8s.io/v1/mutatingadmissionpolicies`

  - `DELETE`: delete collection of MutatingAdmissionPolicy

  - `GET`: list or watch objects of kind MutatingAdmissionPolicy

  - `POST`: create a MutatingAdmissionPolicy

- `/apis/admissionregistration.k8s.io/v1/watch/mutatingadmissionpolicies`

  - `GET`: watch individual changes to a list of MutatingAdmissionPolicy. deprecated: use the 'watch' parameter with a list operation instead.

- `/apis/admissionregistration.k8s.io/v1/mutatingadmissionpolicies/{name}`

  - `DELETE`: delete a MutatingAdmissionPolicy

  - `GET`: read the specified MutatingAdmissionPolicy

  - `PATCH`: partially update the specified MutatingAdmissionPolicy

  - `PUT`: replace the specified MutatingAdmissionPolicy

- `/apis/admissionregistration.k8s.io/v1/watch/mutatingadmissionpolicies/{name}`

  - `GET`: watch changes to an object of kind MutatingAdmissionPolicy. deprecated: use the 'watch' parameter with a list operation instead, filtered to a single item with the 'fieldSelector' parameter.

## /apis/admissionregistration.k8s.io/v1/mutatingadmissionpolicies

HTTP method
`DELETE`

Description
delete collection of MutatingAdmissionPolicy

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`Status`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-Status) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`GET`

Description
list or watch objects of kind MutatingAdmissionPolicy

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`MutatingAdmissionPolicyList`](../objects/index.xml#io-k8s-api-admissionregistration-v1-MutatingAdmissionPolicyList) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`POST`

Description
create a MutatingAdmissionPolicy

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 201 - Created | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 202 - Accepted | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/admissionregistration.k8s.io/v1/watch/mutatingadmissionpolicies

HTTP method
`GET`

Description
watch individual changes to a list of MutatingAdmissionPolicy. deprecated: use the 'watch' parameter with a list operation instead.

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`WatchEvent`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-WatchEvent) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/admissionregistration.k8s.io/v1/mutatingadmissionpolicies/{name}

| Parameter | Type     | Description                         |
|-----------|----------|-------------------------------------|
| `name`    | `string` | name of the MutatingAdmissionPolicy |

Global path parameters

HTTP method
`DELETE`

Description
delete a MutatingAdmissionPolicy

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
read the specified MutatingAdmissionPolicy

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PATCH`

Description
partially update the specified MutatingAdmissionPolicy

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 201 - Created | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

HTTP method
`PUT`

Description
replace the specified MutatingAdmissionPolicy

| Parameter | Type | Description |
|----|----|----|
| `dryRun` | `string` | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed |
| `fieldValidation` | `string` | fieldValidation instructs the server on how to handle objects in the request (POST/PUT/PATCH) containing unknown or duplicate fields. Valid values are: - Ignore: This will ignore any unknown fields that are silently dropped from the object, and will ignore all but the last duplicate field that the decoder encounters. This is the default behavior prior to v1.23. - Warn: This will send a warning via the standard warning response header for each unknown field that is dropped from the object, and for each duplicate field that is encountered. The request will still succeed if there are no other errors, and will only persist the last of any duplicate fields. This is the default in v1.23+ - Strict: This will fail the request with a BadRequest error if any unknown fields would be dropped from the object, or if any duplicate fields are present. The error returned from the server will contain all unknown and duplicate fields encountered. |

Query parameters

| Parameter | Type | Description |
|----|----|----|
| `body` | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |  |

Body parameters

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 201 - Created | [`MutatingAdmissionPolicy`](../extension_apis/mutatingadmissionpolicy-admissionregistration-k8s-io-v1.xml#mutatingadmissionpolicy-admissionregistration-k8s-io-v1) schema |
| 401 - Unauthorized | Empty |

HTTP responses

## /apis/admissionregistration.k8s.io/v1/watch/mutatingadmissionpolicies/{name}

| Parameter | Type     | Description                         |
|-----------|----------|-------------------------------------|
| `name`    | `string` | name of the MutatingAdmissionPolicy |

Global path parameters

HTTP method
`GET`

Description
watch changes to an object of kind MutatingAdmissionPolicy. deprecated: use the 'watch' parameter with a list operation instead, filtered to a single item with the 'fieldSelector' parameter.

| HTTP code | Reponse body |
|----|----|
| 200 - OK | [`WatchEvent`](../objects/index.xml#io-k8s-apimachinery-pkg-apis-meta-v1-WatchEvent) schema |
| 401 - Unauthorized | Empty |

HTTP responses
