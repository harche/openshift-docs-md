You use catalogs to access the versions, patches, and over-the-air updates for extensions and Operators. You use custom resources (CRs) to manage extensions declaratively from the CLI.

> [!NOTE]
> For OpenShift Container Platform 4.17, documented procedures for OLM v1 are CLI-based only. Alternatively, administrators can create and view related objects in the web console by using normal methods, such as the **Import YAML** and **Search** pages. However, the existing **Software Catalog** and **Installed Operators** pages do not yet display OLM v1 components.

# Find Operators to install from a catalog

After you add a catalog to your cluster, you can query the catalog to find Operators and extensions to install.

Currently in Operator Lifecycle Manager (OLM) v1, you cannot query on-cluster catalogs managed by catalogd. In OLM v1, you must use the `opm` and `jq` CLI tools to query the catalog registry.

<div>

<div class="title">

Prerequisites

</div>

- You have added a catalog to your cluster.

- You have installed the `jq` CLI tool.

- You have installed the `opm` CLI tool.

</div>

<div>

<div class="title">

Procedure

</div>

1.  To return a list of extensions that support the `AllNamespaces` install mode and do not use webhooks, enter the following command:

    ``` terminal
    $ opm render <catalog_registry_url>:<tag> \
      | jq -cs '[.[] | select(.schema == "olm.bundle" \
      and (.properties[] | select(.type == "olm.csv.metadata").value.installModes[] \
      | select(.type == "AllNamespaces" and .supported == true)) \
      and .spec.webhookdefinitions == null) | .package] | unique[]'
    ```

    where:

    `catalog_registry_url`
    Specifies the URL of the catalog registry, such as `registry.redhat.io/redhat/redhat-operator-index`.

    `tag`
    Specifies the tag or version of the catalog, such as `v4.17` or `latest`.

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ opm render \
      registry.redhat.io/redhat/redhat-operator-index:v4.17 \
      | jq -cs '[.[] | select(.schema == "olm.bundle" \
      and (.properties[] | select(.type == "olm.csv.metadata").value.installModes[] \
      | select(.type == "AllNamespaces" and .supported == true)) \
      and .spec.webhookdefinitions == null) | .package] | unique[]'
    ```

    </div>

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    "3scale-operator"
    "amq-broker-rhel8"
    "amq-online"
    "amq-streams"
    "amq-streams-console"
    "ansible-automation-platform-operator"
    "ansible-cloud-addons-operator"
    "apicast-operator"
    "authorino-operator"
    "aws-load-balancer-operator"
    "bamoe-kogito-operator"
    "cephcsi-operator"
    "cincinnati-operator"
    "cluster-logging"
    "cluster-observability-operator"
    "compliance-operator"
    "container-security-operator"
    "cryostat-operator"
    "datagrid"
    "devspaces"
    ...
    ```

    </div>

2.  Inspect the contents of an extension’s metadata by running the following command:

    ``` terminal
    $ opm render <catalog_registry_url>:<tag> \
      | jq -s '.[] | select( .schema == "olm.package") \
      | select( .name == "<package_name>")'
    ```

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ opm render \
      registry.redhat.io/redhat/redhat-operator-index:v4.17 \
      | jq -s '.[] | select( .schema == "olm.package") \
      | select( .name == "openshift-pipelines-operator-rh")'
    ```

    </div>

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    {
      "schema": "olm.package",
      "name": "openshift-pipelines-operator-rh",
      "defaultChannel": "latest",
      "icon": {
        "base64data": "iVBORw0KGgoAAAANSUhE...",
        "mediatype": "image/png"
      }
    }
    ```

    </div>

</div>

## Common catalog queries

You can query catalogs by using the `opm` and `jq` CLI tools to help you install, update, and manage the lifecycle of extensions.

The following examples show common catalog queries for extensions:

<div class="formalpara">

<div class="title">

Command syntax

</div>

``` terminal
$ opm render <catalog_registry_url>:<tag> | <jq_request>
```

</div>

where:

`catalog_registry_url`
Specifies the URL of the catalog registry, such as `registry.redhat.io/redhat/redhat-operator-index`.

`tag`
Specifies the tag or version of the catalog, such as `v4.17` or `latest`.

`jq_request`
Specifies the query you want to run on the catalog.

<div class="example">

<div class="title">

Example command

</div>

``` terminal
$ opm render \
  registry.redhat.io/redhat/redhat-operator-index:v4.17 \
  | jq -cs '[.[] | select(.schema == "olm.bundle" and (.properties[] \
  | select(.type == "olm.csv.metadata").value.installModes[] \
  | select(.type == "AllNamespaces" and .supported == true)) \
  and .spec.webhookdefinitions == null) \
  | .package] | unique[]'
```

</div>

<table>
<caption>Common package queries</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Query</th>
<th style="text-align: left;">Request</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>Available packages in a catalog</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .schema == &quot;olm.package&quot;)&#39;</code></pre></td>
</tr>
<tr>
<td style="text-align: left;"><p>Packages that support <code>AllNamespaces</code> install mode and do not use webhooks</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -cs &#39;[.[] | select(.schema == &quot;olm.bundle&quot; and (.properties[] \
  | select(.type == &quot;olm.csv.metadata&quot;).value.installModes[] \
  | select(.type == &quot;AllNamespaces&quot; and .supported == true)) \
  and .spec.webhookdefinitions == null) \
  | .package] | unique[]&#39;</code></pre></td>
</tr>
<tr>
<td style="text-align: left;"><p>Package metadata</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .schema == &quot;olm.package&quot;) \
  | select( .name == &quot;&lt;package_name&gt;&quot;)&#39;</code></pre></td>
</tr>
<tr>
<td style="text-align: left;"><p>Catalog blobs in a package</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .package == &quot;&lt;package_name&gt;&quot;)&#39;</code></pre></td>
</tr>
</tbody>
</table>

<table>
<caption>Common channel queries</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Query</th>
<th style="text-align: left;">Request</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>Channels in a package</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .schema == &quot;olm.channel&quot; ) \
  | select( .package == &quot;&lt;package_name&gt;&quot;) | .name&#39;</code></pre></td>
</tr>
<tr>
<td style="text-align: left;"><p>Versions in a channel</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .package == &quot;&lt;package_name&gt;&quot; ) \
  | select( .schema == &quot;olm.channel&quot; ) \
  | select( .name == &quot;&lt;channel_name&gt;&quot; ) .entries \
  | .[] | .name&#39;</code></pre></td>
</tr>
<tr>
<td style="text-align: left;"><ul>
<li><p>Latest version in a channel</p></li>
<li><p>Upgrade path</p></li>
</ul></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .schema == &quot;olm.channel&quot; ) \
  | select ( .name == &quot;&lt;channel_name&gt;&quot;) \
  | select( .package == &quot;&lt;package_name&gt;&quot;)&#39;</code></pre></td>
</tr>
</tbody>
</table>

<table>
<caption>Common bundle queries</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;">Query</th>
<th style="text-align: left;">Request</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><p>Bundles in a package</p></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .schema == &quot;olm.bundle&quot; ) \
  | select( .package == &quot;&lt;package_name&gt;&quot;) | .name&#39;</code></pre></td>
</tr>
<tr>
<td style="text-align: left;"><ul>
<li><p>Bundle dependencies</p></li>
<li><p>Available APIs</p></li>
</ul></td>
<td style="text-align: left;"><pre class="terminal"><code>$ opm render &lt;catalog_registry_url&gt;:&lt;tag&gt; \
  | jq -s &#39;.[] | select( .schema == &quot;olm.bundle&quot; ) \
  | select ( .name == &quot;&lt;bundle_name&gt;&quot;) \
  | select( .package == &quot;&lt;package_name&gt;&quot;)&#39;</code></pre></td>
</tr>
</tbody>
</table>

# Cluster extension permissions

Operator Lifecycle Manager (OLM) v1 installs and manages cluster extensions in OpenShift Container Platform by using its own service account with `cluster-admin` permissions. You do not need to create an installer service account or assign permissions for each extension.

Access to the `ClusterExtension` API controls who can install and manage extensions. By default, only cluster administrators have write access. Unrestricted write access to this API delegates `cluster-admin` trust.

The `spec.serviceAccount` field in the `ClusterExtension` API is optional, deprecated, and ignored. Existing extensions that specify this field continue to work after a cluster update. The API server returns a deprecation warning when you create or update an extension that specifies the field. To stop these warnings, remove the `spec.serviceAccount` field from your `ClusterExtension` resource and any manifests that define it.

To delegate extension management, combine a validating admission policy with role-based access control (RBAC).

## Create an installation namespace

To install a cluster extension in OpenShift Container Platform, first create an installation namespace. Specify this namespace in the `spec.namespace` field of the extension manifest.

The `spec.namespace` field does not restrict the resources or permissions of an extension to the installation namespace. Depending on the bundle and configuration, an extension can create resources or use permissions in other namespaces or across the cluster.

> [!IMPORTANT]
> Cluster extensions are cluster-scoped.

<div>

<div class="title">

Prerequisites

</div>

- Access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.

</div>

<div>

<div class="title">

Procedure

</div>

- Create the installation namespace by running the following command:

  ``` terminal
  $ oc adm new-project <new_namespace>
  ```

</div>

# Install a cluster extension in all namespaces

You can install an extension from a catalog by creating a custom resource (CR) and applying it to the cluster. Operator Lifecycle Manager (OLM) v1 supports installing cluster extensions, including OLM (Classic) Operators in the `registry+v1` bundle format, that are scoped to the cluster.

> [!NOTE]
> For OpenShift Container Platform 4.17, documented procedures for OLM v1 are CLI-based only. Alternatively, administrators can create and view related objects in the web console by using normal methods, such as the **Import YAML** and **Search** pages. However, the existing **Software Catalog** and **Installed Operators** pages do not yet display OLM v1 components.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster by using an account with `cluster-admin` permissions.

- You have created the installation namespace.

- You have identified a supported package and an available version or channel in a catalog on the cluster.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a CR, similar to the following example:

    ``` yaml
    apiVersion: olm.operatorframework.io/v1
    kind: ClusterExtension
    metadata:
      name: <clusterextension_name>
    spec:
      namespace: <installed_namespace>
      source:
        sourceType: Catalog
        catalog:
          packageName: <package_name>
          channels:
            - <channel_name>
          version: <version_or_version_range>
          upgradeConstraintPolicy: CatalogProvided
    ```

    where:

    `spec.namespace`
    Specifies the namespace where you want the bundle installed, such as `pipelines` or `my-extension`. Extensions are still cluster-scoped and might contain resources that are installed in different namespaces.

    `spec.source.catalog.channels`
    Specifies channel names as an array, such as `pipelines-1.14` or `latest`. This field is optional.

    `spec.source.catalog.version`
    Specifies the version or version range, such as `1.14.0`, `1.14.x`, or `>=1.16`, of the package you want to install or update. This field is optional.

    `spec.source.catalog.upgradeConstraintPolicy`
    Specifies the upgrade constraint policy. If unspecified, the default setting is `CatalogProvided`. The `CatalogProvided` setting only updates if the new version satisfies the upgrade constraints set by the package author. To force an update or rollback, set the field to `SelfCertified`. This field is optional.

    <div class="formalpara">

    <div class="title">

    Example `pipelines-operator.yaml` CR

    </div>

    ``` yaml
    apiVersion: olm.operatorframework.io/v1
    kind: ClusterExtension
    metadata:
      name: pipelines-operator
    spec:
      namespace: pipelines
      source:
        sourceType: Catalog
        catalog:
          packageName: openshift-pipelines-operator-rh
          version: "1.14.x"
    ```

    </div>

2.  Apply the CR to the cluster by running the following command:

    ``` terminal
    $ oc apply -f pipelines-operator.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    clusterextension.olm.operatorframework.io/pipelines-operator created
    ```

    </div>

</div>

<div>

<div class="title">

Verification

</div>

1.  View the Operator or extension’s CR in the YAML format by running the following command:

    ``` terminal
    $ oc get clusterextension pipelines-operator -o yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    apiVersion: v1
    items:
    - apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        annotations:
          kubectl.kubernetes.io/last-applied-configuration: |
            {"apiVersion":"olm.operatorframework.io/v1","kind":"ClusterExtension","metadata":{"annotations":{},"name":"pipes"},"spec":{"namespace":"pipelines","source":{"catalog":{"packageName":"openshift-pipelines-operator-rh","version":"1.14.x"},"sourceType":"Catalog"}}}
        creationTimestamp: "2025-02-18T21:48:13Z"
        finalizers:
        - olm.operatorframework.io/cleanup-unpack-cache
        - olm.operatorframework.io/cleanup-contentmanager-cache
        generation: 1
        name: pipelines-operator
        resourceVersion: "72725"
        uid: e18b13fb-a96d-436f-be75-a9a0f2b07993
      spec:
        namespace: pipelines
        source:
          catalog:
            packageName: openshift-pipelines-operator-rh
            upgradeConstraintPolicy: CatalogProvided
            version: 1.14.x
          sourceType: Catalog
      status:
        conditions:
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: Deprecated
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: PackageDeprecated
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: ChannelDeprecated
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: BundleDeprecated
        - lastTransitionTime: "2025-02-18T21:48:16Z"
          message: Installed bundle registry.redhat.io/openshift-pipelines/pipelines-operator-bundle@sha256:f7b19ce26be742c4aaa458d37bc5ad373b5b29b20aaa7d308349687d3cbd8838
            successfully
          observedGeneration: 1
          reason: Succeeded
          status: "True"
          type: Installed
        - lastTransitionTime: "2025-02-18T21:48:16Z"
          message: desired state reached
          observedGeneration: 1
          reason: Succeeded
          status: "True"
          type: Progressing
        install:
          bundle:
            name: openshift-pipelines-operator-rh.v1.14.5
            version: 1.14.5
    kind: List
    metadata:
      resourceVersion: ""
    ```

    </div>

    where:

    `spec.channel`
    Displays the channel defined in the CR of the extension.

    `spec.version`
    Displays the version or version range defined in the CR of the extension.

    `status.conditions`
    Displays information about the status and health of the extension.

    `type: Deprecated`
    Displays whether one or more of following are deprecated:

    `type: PackageDeprecated`
    Displays whether the resolved package is deprecated.

    `type: ChannelDeprecated`
    Displays whether the resolved channel is deprecated.

    `type: BundleDeprecated`
    Displays whether the resolved bundle is deprecated.

    The value of `False` in the `status` field indicates that the `reason: Deprecated` condition is not deprecated. The value of `True` in the `status` field indicates that the `reason: Deprecated` condition is deprecated.

    `installedBundle.name`
    Displays the name of the bundle installed.

    `installedBundle.version`
    Displays the version of the bundle installed.

</div>

# Configure a watch namespace for a cluster extension (Technology Preview)

You can configure the watch namespace for extensions that support namespace-scoped resource watching.

> [!IMPORTANT]
> Configuring watch namespace for a cluster extension is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

<div>

<div class="title">

Prerequisites

</div>

- You have access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.

- You have enabled the `TechPreviewNoUpgrade` feature set on the cluster.

- You have created the installation namespace.

- You have verified the supported install modes for the extension and determined the required `watchNamespace` configuration.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a custom resource (CR) based on where you want the extension to watch for resources:

    - To configure the extension to watch its own installation namespace:

      ``` yaml
      apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        name: <extension_name>
      spec:
        namespace: <installation_namespace>
        config:
          configType: Inline
          inline:
            watchNamespace: <installation_namespace>
        source:
          sourceType: Catalog
          catalog:
            packageName: <package_name>
            version: <version>
            upgradeConstraintPolicy: CatalogProvided
      ```

      where:

      `config.inline.watchNamespace`
      Specifies the namespace to watch for resources. For requirements and valid values, see "Extension configuration".

    - To configure the extension to watch a different namespace:

      ``` yaml
      apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        name: <extension_name>
      spec:
        namespace: <installation_namespace>
        config:
          configType: Inline
          inline:
            watchNamespace: <watched_namespace>
        source:
          sourceType: Catalog
          catalog:
            packageName: <package_name>
            version: <version>
            upgradeConstraintPolicy: CatalogProvided
      ```

2.  Apply the CR to the cluster by running the following command:

    ``` terminal
    $ oc apply -f <cluster_extension_cr>.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the extension installed successfully by running the following command:

  ``` terminal
  $ oc get clusterextension <extension_name> -o yaml
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` yaml
  apiVersion: olm.operatorframework.io/v1
  kind: ClusterExtension
  metadata:
    name: <extension_name>
  spec:
    namespace: <installation_namespace>
    config:
      configType: Inline
      inline:
        watchNamespace: <installation_namespace>
  status:
    conditions:
    - type: Installed
      status: "True"
      reason: Succeeded
  ```

  </div>

</div>

<div>

<div class="title">

Additional resources

</div>

- [Supported extensions](../../extensions/ce/olmv1-supported-extensions.xml#olmv1-supported-extensions)

- [Projects and namespaces](../../authentication/using-rbac.xml#rbac-projects-namespaces_using-rbac)

- [Example custom resources (CRs) that specify a target version](../../extensions/ce/update-paths.xml#olmv1-about-target-versions_update-paths)

- [Support for version ranges](../../extensions/ce/update-paths.xml#olmv1-version-range-support_update-paths)

</div>

# Updating a cluster extension

You can update your cluster extension or Operator by manually editing the custom resource (CR) and applying the changes.

> [!WARNING]
> Automatic updates can install bundles that grant an extension additional permissions without administrator review. To review each bundle before installation, specify an exact approved version. Review the bundle’s permissions and configuration before approving another version.

<div>

<div class="title">

Prerequisites

</div>

- You have an Operator or extension installed.

- You have installed the `jq` CLI tool.

- You have installed the `opm` CLI tool.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Inspect a package for channel and version information from a local copy of your catalog file by completing the following steps:

    1.  Get a list of channels from a selected package by running the following command:

        ``` terminal
        $ opm render <catalog_registry_url>:<tag> \
          | jq -s '.[] | select( .schema == "olm.channel" ) \
          | select( .package == "openshift-pipelines-operator-rh") | .name'
        ```

        <div class="formalpara">

        <div class="title">

        Example command

        </div>

        ``` terminal
        $ opm render registry.redhat.io/redhat/redhat-operator-index:v4.17 \
          | jq -s '.[] | select( .schema == "olm.channel" ) \
          | select( .package == "openshift-pipelines-operator-rh") | .name'
        ```

        </div>

        <div class="formalpara">

        <div class="title">

        Example output

        </div>

        ``` text
        "latest"
        "pipelines-1.14"
        "pipelines-1.15"
        "pipelines-1.16"
        "pipelines-1.17"
        ```

        </div>

    2.  Get a list of the versions published in a channel by running the following command:

        ``` terminal
        $ opm render <catalog_registry_url>:<tag> \
          | jq -s '.[] | select( .package == "<package_name>" ) \
          | select( .schema == "olm.channel" ) \
          | select( .name == "<channel_name>" ) | .entries \
          | .[] | .name'
        ```

        <div class="formalpara">

        <div class="title">

        Example command

        </div>

        ``` terminal
        $ opm render registry.redhat.io/redhat/redhat-operator-index:v4.17 \
          | jq -s '.[] | select( .package == "openshift-pipelines-operator-rh" ) \
          | select( .schema == "olm.channel" ) | select( .name == "latest" ) \
          | .entries | .[] | .name'
        ```

        </div>

        <div class="formalpara">

        <div class="title">

        Example output

        </div>

        ``` text
        "openshift-pipelines-operator-rh.v1.15.0"
        "openshift-pipelines-operator-rh.v1.16.0"
        "openshift-pipelines-operator-rh.v1.17.0"
        "openshift-pipelines-operator-rh.v1.17.1"
        ```

        </div>

2.  Find out what version or channel is specified in your Operator or extension’s CR by running the following command:

    ``` terminal
    $ oc get clusterextension <operator_name> -o yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ oc get clusterextension pipelines-operator -o yaml
    ```

    </div>

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    apiVersion: v1
    items:
    - apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        annotations:
          kubectl.kubernetes.io/last-applied-configuration: |
            {"apiVersion":"olm.operatorframework.io/v1","kind":"ClusterExtension","metadata":{"annotations":{},"name":"pipes"},"spec":{"namespace":"pipelines","source":{"catalog":{"packageName":"openshift-pipelines-operator-rh","version":"1.14.x"},"sourceType":"Catalog"}}}
        creationTimestamp: "2025-02-18T21:48:13Z"
        finalizers:
        - olm.operatorframework.io/cleanup-unpack-cache
        - olm.operatorframework.io/cleanup-contentmanager-cache
        generation: 1
        name: pipelines-operator
        resourceVersion: "72725"
        uid: e18b13fb-a96d-436f-be75-a9a0f2b07993
      spec:
        namespace: pipelines
        source:
          catalog:
            packageName: openshift-pipelines-operator-rh
            upgradeConstraintPolicy: CatalogProvided
            version: 1.14.x
          sourceType: Catalog
      status:
        conditions:
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: Deprecated
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: PackageDeprecated
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: ChannelDeprecated
        - lastTransitionTime: "2025-02-18T21:48:13Z"
          message: ""
          observedGeneration: 1
          reason: Deprecated
          status: "False"
          type: BundleDeprecated
        - lastTransitionTime: "2025-02-18T21:48:16Z"
          message: Installed bundle registry.redhat.io/openshift-pipelines/pipelines-operator-bundle@sha256:f7b19ce26be742c4aaa458d37bc5ad373b5b29b20aaa7d308349687d3cbd8838
            successfully
          observedGeneration: 1
          reason: Succeeded
          status: "True"
          type: Installed
        - lastTransitionTime: "2025-02-18T21:48:16Z"
          message: desired state reached
          observedGeneration: 1
          reason: Succeeded
          status: "True"
          type: Progressing
        install:
          bundle:
            name: openshift-pipelines-operator-rh.v1.14.5
            version: 1.14.5
    kind: List
    metadata:
      resourceVersion: ""
    ```

    </div>

3.  Edit your CR by using one of the following methods:

    - If you want to pin your Operator or extension to specific version, such as `1.15.0`, edit your CR similar to the following example:

      <div class="formalpara">

      <div class="title">

      Example `pipelines-operator.yaml` CR

      </div>

      ``` yaml
      apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        name: pipelines-operator
      spec:
        namespace: pipelines
        source:
          sourceType: Catalog
          catalog:
            packageName: openshift-pipelines-operator-rh
            version: "1.15.0"
      ```

      </div>

      This example updates the version from `1.14.x` to `1.15.0`.

    - If you want to define a range of acceptable update versions, edit your CR similar to the following example:

      <div class="formalpara">

      <div class="title">

      Example CR with a version range specified

      </div>

      ``` yaml
      apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        name: pipelines-operator
      spec:
        namespace: pipelines
        source:
          sourceType: Catalog
          catalog:
            packageName: openshift-pipelines-operator-rh
            version: ">1.15, <1.17"
      ```

      </div>

      The `spec.source.catalog.version` value specifies that the desired version range is greater than version `1.15` and less than `1.17`.

    - If you want to update to the latest version that can be resolved from a channel, edit your CR similar to the following example:

      <div class="formalpara">

      <div class="title">

      Example CR with a specified channel

      </div>

      ``` yaml
      apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        name: pipelines-operator
      spec:
        namespace: pipelines
        source:
          sourceType: Catalog
          catalog:
            packageName: openshift-pipelines-operator-rh
            channels:
              - latest
      ```

      </div>

      The `spec.source.catalog.channels` value installs the latest release that can be resolved from the specified channel. Updates to the channel are automatically installed. Enter values as an array.

    - If you want to specify a channel and version or version range, edit your CR similar to the following example:

      <div class="formalpara">

      <div class="title">

      Example CR with a specified channel and version range

      </div>

      ``` yaml
      apiVersion: olm.operatorframework.io/v1
      kind: ClusterExtension
      metadata:
        name: pipelines-operator
      spec:
        namespace: pipelines
        source:
          sourceType: Catalog
          catalog:
            packageName: openshift-pipelines-operator-rh
            channels:
              - latest
            version: "<1.16"
      ```

      </div>

      For more information, see "Example custom resources (CRs) that specify a target version".

4.  Apply the update to the cluster by running the following command:

    ``` terminal
    $ oc apply -f pipelines-operator.yaml
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    clusterextension.olm.operatorframework.io/pipelines-operator configured
    ```

    </div>

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the channel and version updates have been applied by running the following command:

  ``` terminal
  $ oc get clusterextension pipelines-operator -o yaml
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` yaml
  apiVersion: olm.operatorframework.io/v1
  kind: ClusterExtension
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"olm.operatorframework.io/v1","kind":"ClusterExtension","metadata":{"annotations":{},"name":"pipes"},"spec":{"namespace":"pipelines","source":{"catalog":{"packageName":"openshift-pipelines-operator-rh","version":"\u003c1.16"},"sourceType":"Catalog"}}}
    creationTimestamp: "2025-02-18T21:48:13Z"
    finalizers:
    - olm.operatorframework.io/cleanup-unpack-cache
    - olm.operatorframework.io/cleanup-contentmanager-cache
    generation: 2
    name: pipes
    resourceVersion: "90693"
    uid: e18b13fb-a96d-436f-be75-a9a0f2b07993
  spec:
    namespace: pipelines
    source:
      catalog:
        packageName: openshift-pipelines-operator-rh
        upgradeConstraintPolicy: CatalogProvided
        version: <1.16
      sourceType: Catalog
  status:
    conditions:
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: Deprecated
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: PackageDeprecated
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: ChannelDeprecated
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: BundleDeprecated
    - lastTransitionTime: "2025-02-18T21:48:16Z"
      message: Installed bundle registry.redhat.io/openshift-pipelines/pipelines-operator-bundle@sha256:8a593c1144709c9aeffbeb68d0b4b08368f528e7bb6f595884b2474bcfbcafcd
        successfully
      observedGeneration: 2
      reason: Succeeded
      status: "True"
      type: Installed
    - lastTransitionTime: "2025-02-18T21:48:16Z"
      message: desired state reached
      observedGeneration: 2
      reason: Succeeded
      status: "True"
      type: Progressing
    install:
      bundle:
        name: openshift-pipelines-operator-rh.v1.15.2
        version: 1.15.2
  ```

  </div>

</div>

<div>

<div class="title">

Troubleshooting

</div>

- If you specify a target version or channel that is deprecated or does not exist, you can run the following command to check the status of your extension:

  ``` terminal
  $ oc get clusterextension <operator_name> -o yaml
  ```

  <div class="formalpara">

  <div class="title">

  Example output for a version that does not exist

  </div>

  ``` text
  apiVersion: olm.operatorframework.io/v1
  kind: ClusterExtension
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"olm.operatorframework.io/v1","kind":"ClusterExtension","metadata":{"annotations":{},"name":"pipes"},"spec":{"namespace":"pipelines","source":{"catalog":{"packageName":"openshift-pipelines-operator-rh","version":"9.x"},"sourceType":"Catalog"}}}
    creationTimestamp: "2025-02-18T21:48:13Z"
    finalizers:
    - olm.operatorframework.io/cleanup-unpack-cache
    - olm.operatorframework.io/cleanup-contentmanager-cache
    generation: 3
    name: pipes
    resourceVersion: "93334"
    uid: e18b13fb-a96d-436f-be75-a9a0f2b07993
  spec:
    namespace: pipelines
    source:
      catalog:
        packageName: openshift-pipelines-operator-rh
        upgradeConstraintPolicy: CatalogProvided
        version: 9.x
      sourceType: Catalog
  status:
    conditions:
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: Deprecated
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: PackageDeprecated
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: ChannelDeprecated
    - lastTransitionTime: "2025-02-18T21:48:13Z"
      message: ""
      observedGeneration: 2
      reason: Deprecated
      status: "False"
      type: BundleDeprecated
    - lastTransitionTime: "2025-02-18T21:48:16Z"
      message: Installed bundle registry.redhat.io/openshift-pipelines/pipelines-operator-bundle@sha256:8a593c1144709c9aeffbeb68d0b4b08368f528e7bb6f595884b2474bcfbcafcd
        successfully
      observedGeneration: 3
      reason: Succeeded
      status: "True"
      type: Installed
    - lastTransitionTime: "2025-02-18T21:48:16Z"
      message: 'error upgrading from currently installed version "1.15.2": no bundles
        found for package "openshift-pipelines-operator-rh" matching version "9.x"'
      observedGeneration: 3
      reason: Retrying
      status: "True"
      type: Progressing
    install:
      bundle:
        name: openshift-pipelines-operator-rh.v1.15.2
        version: 1.15.2
  ```

  </div>

</div>

<div>

<div class="title">

Additional resources

</div>

- [Update paths](../../extensions/ce/update-paths.xml#update-paths)

</div>

# Deleting an Operator

You can delete an Operator and its custom resource definitions (CRDs) by deleting the `ClusterExtension` custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- You have a catalog installed.

- You have an Operator installed.

</div>

<div>

<div class="title">

Procedure

</div>

- Delete an Operator and its CRDs by running the following command:

  ``` terminal
  $ oc delete clusterextension <operator_name>
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` text
  clusterextension.olm.operatorframework.io "<operator_name>" deleted
  ```

  </div>

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the extension CR no longer exists by running the following command:

  ``` terminal
  $ oc get clusterextension <operator_name>
  ```

  The API server returns a `NotFound` error. A namespace that you created before installing the extension remains on the cluster.

</div>

# Downloading the bundle manifests of an extension

Download the bundle manifests of an extension with the `opm` CLI tool. Review the resources and runtime permissions in the manifests before approving the extension for installation.

<div>

<div class="title">

Prerequisites

</div>

- You have access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.

- You have decided which extension you want to install.

- You have installed the `opm` CLI tool.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Inspect the available versions and images of the extension you want to install by running the following command:

    ``` terminal
    $ opm render <registry_url>:<tag_or_version> | \
      jq -cs '.[] | select( .schema == "olm.bundle" ) | \
      select( .package == "<extension_name>") | \
      {"name":.name, "image":.image}'
    ```

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ opm render registry.redhat.io/redhat/redhat-operator-index:v4.17 | \
      jq -cs '.[] | select( .schema == "olm.bundle" ) | \
      select( .package == "openshift-pipelines-operator-rh") | \
      {"name":.name, "image":.image}'
    ```

    </div>

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    {"name":"openshift-pipelines-operator-rh.v1.14.5","image":"registry.redhat.io/openshift-pipelines/pipelines-operator-bundle@sha256:f7b19ce26be742c4aaa458d37bc5ad373b5b29b20aaa7d308349687d3cbd8838"}
    ```

    </div>

2.  Make a directory to extract the image of the bundle that you want to install by running the following command:

    ``` terminal
    $ mkdir <new_dir>
    ```

3.  Change into the directory by running the following command:

    ``` terminal
    $ cd <new_dir>
    ```

4.  Find the image reference of the version that you want to install and run the following command:

    ``` terminal
    $ oc image extract <full_path_to_registry_image>@sha256:<sha>
    ```

    <div class="formalpara">

    <div class="title">

    Example command

    </div>

    ``` terminal
    $ oc image extract registry.redhat.io/openshift-pipelines/pipelines-operator-bundle@sha256:f7b19ce26be742c4aaa458d37bc5ad373b5b29b20aaa7d308349687d3cbd8838
    ```

    </div>

5.  Change into the `manifests` directory by running the following command:

    ``` terminal
    $ cd manifests
    ```

6.  View the contents of the manifests directory by entering the following command. The output lists the manifests of the resources required to install, manage, and operate your extension.

    ``` terminal
    $ tree
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` text
    .
    ├── manifests
    │   ├── config-logging_v1_configmap.yaml
    │   ├── openshift-pipelines-operator-monitor_monitoring.coreos.com_v1_servicemonitor.yaml
    │   ├── openshift-pipelines-operator-prometheus-k8s-read-binding_rbac.authorization.k8s.io_v1_rolebinding.yaml
    │   ├── openshift-pipelines-operator-read_rbac.authorization.k8s.io_v1_role.yaml
    │   ├── openshift-pipelines-operator-rh.clusterserviceversion.yaml
    │   ├── operator.tekton.dev_manualapprovalgates.yaml
    │   ├── operator.tekton.dev_openshiftpipelinesascodes.yaml
    │   ├── operator.tekton.dev_tektonaddons.yaml
    │   ├── operator.tekton.dev_tektonchains.yaml
    │   ├── operator.tekton.dev_tektonconfigs.yaml
    │   ├── operator.tekton.dev_tektonhubs.yaml
    │   ├── operator.tekton.dev_tektoninstallersets.yaml
    │   ├── operator.tekton.dev_tektonpipelines.yaml
    │   ├── operator.tekton.dev_tektonresults.yaml
    │   ├── operator.tekton.dev_tektontriggers.yaml
    │   ├── tekton-config-defaults_v1_configmap.yaml
    │   ├── tekton-config-observability_v1_configmap.yaml
    │   ├── tekton-config-read-rolebinding_rbac.authorization.k8s.io_v1_clusterrolebinding.yaml
    │   ├── tekton-config-read-role_rbac.authorization.k8s.io_v1_clusterrole.yaml
    │   ├── tekton-operator-controller-config-leader-election_v1_configmap.yaml
    │   ├── tekton-operator-info_rbac.authorization.k8s.io_v1_rolebinding.yaml
    │   ├── tekton-operator-info_rbac.authorization.k8s.io_v1_role.yaml
    │   ├── tekton-operator-info_v1_configmap.yaml
    │   ├── tekton-operator_v1_service.yaml
    │   ├── tekton-operator-webhook-certs_v1_secret.yaml
    │   ├── tekton-operator-webhook-config-leader-election_v1_configmap.yaml
    │   ├── tekton-operator-webhook_v1_service.yaml
    │   ├── tekton-result-read-rolebinding_rbac.authorization.k8s.io_v1_clusterrolebinding.yaml
    │   └── tekton-result-read-role_rbac.authorization.k8s.io_v1_clusterrole.yaml
    ├── metadata
    │   ├── annotations.yaml
    │   └── properties.yaml
    └── root
        └── buildinfo
            ├── content_manifests
            │   └── openshift-pipelines-operator-bundle-container-v1.16.2-3.json
            └── Dockerfile-openshift-pipelines-pipelines-operator-bundle-container-v1.16.2-3
    ```

    </div>

</div>
