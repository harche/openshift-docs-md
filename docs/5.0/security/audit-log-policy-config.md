You can control the amount of information that is logged to the API server audit logs by choosing the audit log policy profile to use.

# About audit log policy profiles

To monitor activity and maintain compliance, you can apply audit log profiles that define the level of detail recorded for API server requests. While more comprehensive profiles provide request bodies for troubleshooting, they also increase resource overhead on the host system.

Audit log profiles define how to log requests that come to the OpenShift API server, Kubernetes API server, OpenShift OAuth API server, and OpenShift OAuth server.

OpenShift Container Platform provides the following predefined audit policy profiles:

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 66%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Profile</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>Default</code></p></td>
<td style="text-align: left;"><p>Logs only metadata for read and write requests; does not log request bodies except for OAuth access token requests. This is the default policy.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>WriteRequestBodies</code></p></td>
<td style="text-align: left;"><p>In addition to logging metadata for all requests, logs request bodies for every write request to the API servers (<code>create</code>, <code>update</code>, <code>patch</code>, <code>delete</code>, <code>deletecollection</code>). This profile has more resource overhead than the <code>Default</code> profile. <sup>[1]</sup></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>AllRequestBodies</code></p></td>
<td style="text-align: left;"><p>In addition to logging metadata for all requests, logs request bodies for every read and write request to the API servers (<code>get</code>, <code>list</code>, <code>create</code>, <code>update</code>, <code>patch</code>). This profile has the most resource overhead. <sup>[1]</sup></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>None</code></p></td>
<td style="text-align: left;"><p>No requests are logged, including OAuth access token requests and OAuth authorize token requests. Custom rules are ignored when this profile is set.</p>
<div class="warning">
<p>Do not disable audit logging by using the <code>None</code> profile unless you are fully aware of the risks of not logging data that can be beneficial when troubleshooting issues. If you disable audit logging and a support situation arises, you might need to enable audit logging and reproduce the issue to troubleshoot properly.</p>
</div></td>
</tr>
</tbody>
</table>

1.  Sensitive resources, such as `Secret`, `Route`, and `OAuthClient` objects, are only logged at the metadata level. OpenShift OAuth server events are only logged at the metadata level.

By default, OpenShift Container Platform uses the `Default` audit log profile. You can use another audit policy profile that also logs request bodies, but be aware of the increased resource usage such as CPU, memory, and I/O.

# Configuring the audit log policy

You can configure the audit log policy to use when logging requests that come to the API servers.

- You have access to the cluster as a user with the `cluster-admin` role.

1.  Edit the `APIServer` resource:

    ``` terminal
    $ oc edit apiserver cluster
    ```

2.  Update the `spec.audit.profile` field:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
    ...
    spec:
      audit:
        profile: WriteRequestBodies
    ```

    where:

    `profile`
    Set to `Default`, `WriteRequestBodies`, `AllRequestBodies`, or `None`. The default profile is `Default`.

    <div class="warning">

    It is not recommended to disable audit logging by using the `None` profile unless you are fully aware of the risks of not logging data that can be beneficial when troubleshooting issues. If you disable audit logging and a support situation arises, you might need to enable audit logging and reproduce the issue in order to troubleshoot properly.

    </div>

3.  Save the file to apply the changes.

- Verify that a new revision of the Kubernetes API server pods is rolled out. It can take several minutes for all nodes to update to the new revision.

  ``` terminal
  $ oc get kubeapiserver -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{"\n"}{"\n"}'
  ```

  Review the `NodeInstallerProgressing` status condition for the Kubernetes API server to verify that all nodes are at the latest revision. The output shows `AllNodesAtLatestRevision` upon successful update:

  ``` terminal
  AllNodesAtLatestRevision
  3 nodes are at revision 12
  ```

  In this example, the latest revision number is `12`.

  If the output shows a message similar to one of the following messages, the update is still in progress. Wait a few minutes and try again.

  - `3 nodes are at revision 11; 0 nodes have achieved new revision 12`

  - `2 nodes are at revision 11; 1 nodes are at revision 12`

# Configuring the audit log policy with custom rules

You can configure an audit log policy that defines custom rules. You can specify multiple groups and define which profile to use for that group.

These custom rules take precedence over the top-level profile field. The custom rules are evaluated from top to bottom, and the first that matches is applied.

<div class="important">

If you set the top-level profile field to `None`, an API server, such as the Kubernetes API server, ignores custom rules and disables audit logging.

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

1.  Edit the `APIServer` resource:

    ``` terminal
    $ oc edit apiserver cluster
    ```

2.  Add the `spec.audit.customRules` field:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
    ...
    spec:
      audit:
        customRules:
        - group: system:authenticated:oauth
          profile: WriteRequestBodies
        - group: system:authenticated
          profile: AllRequestBodies
        profile: Default
    ```

    where:

    `customRules`
    Add one or more groups and specify the profile to use for that group. These custom rules take precedence over the top-level profile field. The custom rules are evaluated from top to bottom, and the first that matches is applied.

    `profile`
    Set to `Default`, `WriteRequestBodies`, or `AllRequestBodies`. If you do not set this top-level profile field, it defaults to the `Default` profile.

3.  Save the file to apply the changes.

- Verify that a new revision of the Kubernetes API server pods is rolled out. It can take several minutes for all nodes to update to the new revision.

  ``` terminal
  $ oc get kubeapiserver -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{"\n"}{"\n"}'
  ```

  Review the `NodeInstallerProgressing` status condition for the Kubernetes API server to verify that all nodes are at the latest revision. The output shows `AllNodesAtLatestRevision` upon successful update:

  ``` terminal
  AllNodesAtLatestRevision
  3 nodes are at revision 12
  ```

  In this example, the latest revision number is `12`.

  If the output shows a message similar to one of the following messages, the update is still in progress. Wait a few minutes and try again.

  - `3 nodes are at revision 11; 0 nodes have achieved new revision 12`

  - `2 nodes are at revision 11; 1 nodes are at revision 12`

# Disabling audit logging

You can disable audit logging for OpenShift Container Platform. When you disable audit logging, even OAuth access token requests and OAuth authorize token requests are not logged.

<div class="warning">

It is not recommended to disable audit logging by using the `None` profile unless you are fully aware of the risks of not logging data that can be beneficial when troubleshooting issues. If you disable audit logging and a support situation arises, you might need to enable audit logging and reproduce the issue in order to troubleshoot properly.

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

1.  Edit the `APIServer` resource:

    ``` terminal
    $ oc edit apiserver cluster
    ```

2.  Set the `spec.audit.profile` field to `None`:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
    ...
    spec:
      audit:
        profile: None
    ```

    <div class="note">

    You can also disable audit logging only for specific groups by specifying custom rules in the `spec.audit.customRules` field.

    </div>

3.  Save the file to apply the changes.

- Verify that a new revision of the Kubernetes API server pods is rolled out. It can take several minutes for all nodes to update to the new revision.

  ``` terminal
  $ oc get kubeapiserver -o=jsonpath='{range .items[0].status.conditions[?(@.type=="NodeInstallerProgressing")]}{"\n"}{"\n"}'
  ```

  Review the `NodeInstallerProgressing` status condition for the Kubernetes API server to verify that all nodes are at the latest revision. The output shows `AllNodesAtLatestRevision` upon successful update:

  ``` terminal
  AllNodesAtLatestRevision
  3 nodes are at revision 12
  ```

  In this example, the latest revision number is `12`.

  If the output shows a message similar to one of the following messages, the update is still in progress. Wait a few minutes and try again.

  - `3 nodes are at revision 11; 0 nodes have achieved new revision 12`

  - `2 nodes are at revision 11; 1 nodes are at revision 12`
