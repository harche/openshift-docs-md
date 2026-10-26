To improve secret security and integrate with enterprise secret management systems, you can use the Secrets Store CSI Driver Operator to mount secrets from external stores without persisting them on the cluster after pod termination.

# Overview of Secrets Store CSI Driver Operator

The Secrets Store CSI Driver Operator mounts secrets from external secret management systems, such as Azure Key Vault, into pods by using a provider plugin. The secrets do not persist on the system after pod termination.

Secret objects are stored with Base64 encoding. etcd provides encryption at rest for these secrets, but when secrets are retrieved, they are decrypted and presented to the user. If role-based access control is not configured properly on your cluster, anyone with API or etcd access can retrieve or modify a secret. Additionally, anyone who is authorized to create a pod in a namespace can use that access to read any secret in that namespace.

The Secrets Store CSI Driver Operator, `secrets-store.csi.k8s.io`, enables OpenShift Container Platform to mount multiple secrets, keys, and certificates stored in enterprise-grade external secrets stores into pods as a volume. The Secrets Store CSI Driver Operator communicates with the provider using gRPC to fetch the mount contents from the specified external secrets store. After the volume is attached, the data in it is mounted into the container’s file system. Secrets store volumes are mounted in-line.

For more information about CSI inline volumes, see "CSI inline ephemeral volumes".

Familiarity with persistent storage and configuring CSI volumes is recommended when working with a CSI driver. For more information, see "Understanding persistent storage" and "Configuring CSI volumes".

<div>

<div class="title">

Additional resources

</div>

- [CSI inline ephemeral volumes](../../storage/container_storage_interface/ephemeral-storage-csi-inline.xml#ephemeral-storage-csi-inline)

- [Understanding persistent storage](../../storage/understanding-persistent-storage.xml#understanding-persistent-storage)

- [Configuring CSI volumes](../../storage/container_storage_interface/persistent-storage-csi.xml#persistent-storage-csi)

</div>

## Secrets store providers

You can store sensitive application data in an external secret management system and use the Secrets Store CSI Driver Operator to mount the secret content as a pod volume.

The Secrets Store CSI Driver Operator has been tested with the following secrets store providers:

- AWS Secrets Manager

- AWS Systems Manager Parameter Store

- Azure Key Vault

- Google Secret Manager

- HashiCorp Vault

> [!IMPORTANT]
> IBM Z supports only HashiCorp Vault.

> [!NOTE]
> Red Hat does not test all factors associated with third-party secrets store provider functionality. For more information about third-party support, see the "Red Hat third-party support policy".

# About CSI

The Container Storage Interface (CSI) enables storage vendors to deliver plugins through a standard interface without modifying Kubernetes core code, replacing traditional embedded storage drivers.

CSI Operators give OpenShift Container Platform users storage options, such as volume snapshots, that are not possible with in-tree volume plugins.

# Support for disconnected environments

You can use certain secrets store providers in disconnected OpenShift Container Platform clusters by configuring VPC endpoints or equivalent connectivity to enable communication between the driver and external secret management systems.

The following secrets store providers support using the Secrets Store CSI driver in disconnected clusters:

- AWS Secrets Manager

- Azure Key Vault

- Google Secret Manager

- HashiCorp Vault

To enable communication between Secrets Store CSI driver and the secrets store provider, configure Virtual Private Cloud (VPC) endpoints or equivalent connectivity to the corresponding secrets store provider, the OpenID Connect (OIDC) issuer, and the Secure Token Service (STS). The exact configuration depends on the secrets store provider, the authentication method, and the type of disconnected cluster.

> [!NOTE]
> For more information about disconnected environments, see "About disconnected environments".

<div>

<div class="title">

Additional resources

</div>

- [About disconnected environments](../../disconnected/about.xml#about)

</div>

# Support for network policies

The Secrets Store CSI Driver Operator uses pre-defined `NetworkPolicies` to control ingress and egress traffic for enhanced security of the Operator and driver components.

The following table summarizes the default ingress and egress rules:

| Component | Ingress ports | Egress ports | Description |
|----|----|----|----|
| Secrets Store CSI Driver Operator | `8443` | `6443` | Accesses metrics and communicates with the API server |
| Secrets Store CSI driver | `8095` | `6443` | Accesses metrics and communicates with the API server |

# Install the Secrets Store CSI driver

To enable OpenShift Container Platform to mount secrets from external secret management systems, install the Secrets Store CSI Driver Operator and create a `ClusterCSIDriver` instance.

<div>

<div class="title">

Prerequisites

</div>

- Access to the OpenShift Container Platform web console.

- Administrator access to the cluster.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Install the Secrets Store CSI Driver Operator:

    1.  Log in to the web console.

    2.  Click **Ecosystem** → **Software Catalog**.

    3.  Locate the Secrets Store CSI Driver Operator by typing "Secrets Store CSI" in the filter box.

    4.  Click the **Secrets Store CSI Driver Operator** button.

    5.  On the **Secrets Store CSI Driver Operator** page, click **Install**.

    6.  On the **Install Operator** page, ensure that:

        - **All namespaces on the cluster (default)** is selected.

        - **Installed Namespace** is set to **openshift-cluster-csi-drivers**.

    7.  Click **Install**.

        After the installation finishes, the Secrets Store CSI Driver Operator is listed in the **Installed Operators** section of the web console.

2.  Create the `ClusterCSIDriver` instance for the driver (`secrets-store.csi.k8s.io`):

    1.  Click **Administration** → **CustomResourceDefinitions** → **ClusterCSIDriver**.

    2.  On the **Instances** tab, click **Create ClusterCSIDriver**.

        Use the following YAML file:

        ``` yaml
        apiVersion: operator.openshift.io/v1
        kind: ClusterCSIDriver
        metadata:
            name: secrets-store.csi.k8s.io
        spec:
          managementState: Managed
        ```

    3.  Click **Create**.

</div>

# Installing the Secrets Store CSI driver by using the CLI

The Secrets Store CSI driver is typically installed in the namespace `openshift-cluster-csi-drivers`. This namespace is present in the cluster as part of the installation of the Cluster Storage Operator.

<div>

<div class="title">

Procedure

</div>

1.  Create an `OperatorGroup` object by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: operators.coreos.com/v1
    kind: OperatorGroup
    metadata:
      name: openshift-cluster-csi-drivers
      namespace: openshift-cluster-csi-drivers
    spec: {}
    EOF
    ```

2.  Create a `Subscription` object by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: secrets-store-csi-driver-operator
      namespace: openshift-cluster-csi-drivers
    spec:
      channel: stable
      installPlanApproval: Automatic
      name: secrets-store-csi-driver-operator
      source: redhat-operators
      sourceNamespace: openshift-marketplace
    EOF
    ```

3.  Wait for the Operator to be up and running. You can check the Operator status by running the following command:

    ``` terminal
    $ oc get csv -n openshift-cluster-csi-drivers
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME    DISPLAY     VERSION         RELEASE   REPLACES   PHASE
    secrets-store-csi-driver-operator.v4.22.0-202607151755   Secrets Store CSI Driver Operator   4.22.0-202607151755                        Succeeded
    ```

    </div>

4.  Create the Cluster CSI driver by running the following command:

    ``` terminal
    $ oc apply -f - <<EOF
    apiVersion: operator.openshift.io/v1
    kind: ClusterCSIDriver
    metadata:
      name: secrets-store.csi.k8s.io
    spec:
      managementState: Managed
    EOF
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the Operator is running:

  ``` terminal
  $ oc get operator -n openshift-cluster-csi-drivers
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME                                                             AGE
  secrets-store-csi-driver-operator.openshift-cluster-csi-drivers   7m55s
  ```

  </div>

- Verify that the pods are running:

  ``` terminal
  $ oc get pods -n openshift-cluster-csi-drivers
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME                                                 READY   STATUS    RESTARTS   AGE
  ....
  ....
  secrets-store-csi-driver-node-bhp2d                  3/3     Running   0          45s
  secrets-store-csi-driver-operator-74696fc7bc-qjrl8   1/1     Running   0          7m40s
  ```

  </div>

</div>

# Configuring secret rotation for the Secrets Store CSI Driver

You can configure secret rotation intervals to control how often mounted secrets are refreshed from external stores, or disable rotation for static secrets based on your specific security and operational requirements.

By default, secret rotation is enabled. When rotation is enabled, the Secrets Store CSI Driver Operator polls the external secret store at a configurable interval to check for secret updates. This process ensures that updates in the external store are automatically reflected in your pods and secrets. By default, polling interval is 2 minutes.

If you enabled synchronization of mounted content as Kubernetes secrets, the Kubernetes secrets are also rotated when the external secrets are updated.

Applications consuming the secret data must watch for file system changes to detect updated secrets. The Secrets Store CSI Driver Operator updates the content of the mounted volume, and applications should reload the secrets when changes are detected.

<div>

<div class="title">

Prerequisites

</div>

- The Secrets Store CSI Driver Operator is installed on the cluster.

- You have access to the cluster with `cluster-admin` privileges.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ClusterCSIDriver` custom resource for the Secrets Store CSI Driver Operator by running the following command:

    ``` terminal
    $ oc edit clustercsidrivers.operator.openshift.io secrets-store.csi.k8s.io
    ```

2.  Locate or add the `secretRotation` section under `spec.driverConfig.secretsStore`. To enable secret rotation with a custom polling interval, set the type to `Custom` and configure the `minimumRefreshAge` field:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: ClusterCSIDriver
    metadata:
      name: secrets-store.csi.k8s.io
    spec:
      driverConfig:
        driverType: SecretsStore
        secretsStore:
          secretRotation:
            type: Custom
            custom:
              minimumRefreshAge: 300
    ```

    where:

    `spec.driverConfig.secretsStore.secretRotation.type`
    Specifies the secret rotation mode. Set to `Custom` to enable secret rotation with a custom interval, or `None` to disable rotation. When rotation is disabled, secrets are fetched only at initial pod mount time.

    `spec.driverConfig.secretsStore.secretRotation.custom.minimumRefreshAge`
    Specifies the minimum number of seconds between rotation attempts. Valid range is 1 to 31,560,000 seconds (approximately 1 year). If omitted when `type` is `Custom`, the platform applies a default of 120 seconds.

    > [!TIP]
    > Choose a refresh interval based on your security and cost requirements:
    >
    > - For secrets that change frequently and require quick updates, use shorter intervals such as `60` (60 seconds) or `120` (2 minutes).
    >
    > - For secrets that change infrequently, use longer intervals such as `600` (10 minutes) or `3600` (1 hour) to reduce transaction costs and performance overhead.

3.  To disable secret rotation completely, set the `type` field to `None`:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: ClusterCSIDriver
    metadata:
      name: secrets-store.csi.k8s.io
    spec:
      driverConfig:
        driverType: SecretsStore
        secretsStore:
          secretRotation:
            type: None
    ```

    When rotation is disabled, secrets are fetched only at initial pod mount time and are not updated thereafter, even if the values change in the external secret store.

4.  Save and apply the changes to the custom resource.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the Secrets Store CSI Driver Operator driver pods are updated with the new configuration by running the following command:

    ``` terminal
    $ oc get pods -n openshift-cluster-csi-drivers | grep secrets-store
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    secrets-store-csi-driver-node-bhp2d                  3/3     Running   0          45s
    secrets-store-csi-driver-node-xyz12                  3/3     Running   0          45s
    secrets-store-csi-driver-operator-74696fc7bc-qjrl8   1/1     Running   0          7m40s
    ```

    </div>

2.  Check the `ClusterCSIDriver` configuration to confirm the rotation settings by running the following command:

    ``` terminal
    $ oc get clustercsidrivers.operator.openshift.io secrets-store.csi.k8s.io -o jsonpath='{.spec.driverConfig.secretsStore.secretRotation}' | jq
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    {
      "custom": {
        "minimumRefreshAge": 300
      },
      "type": "Custom"
    }
    ```

    </div>

3.  For pods that mount secrets from the external store, monitor the file system to verify that the CSI driver rotates secrets according to the configured interval.

</div>

# Configuring token requests for Workload Identity Federation

You can configure the Secrets Store CSI Driver Operator to use Workload Identity Federation (WIF) by specifying the service account token audience. This enables secure, credential-free authentication to external secret management systems across multiple cloud providers.

Workload Identity Federation allows your OpenShift Container Platform workloads to access cloud provider services without storing long-lived credentials. Instead, the Secrets Store CSI Driver Operator uses short-lived service account tokens with a specified audience to authenticate to external secret stores.

<div>

<div class="title">

Prerequisites

</div>

- The Secrets Store CSI Driver Operator is installed on the cluster.

- You are using Workload Identity Federation with a supported provider, such as AWS, Azure, Google Cloud Platform, or HashiCorp Vault.

- You have configured your cloud provider to trust your OpenShift Container Platform cluster’s OIDC provider.

- You have access to the cluster with `cluster-admin` privileges.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ClusterCSIDriver` custom resource for the Secrets Store CSI Driver Operator by running the following command:

    ``` terminal
    $ oc edit clustercsidrivers.operator.openshift.io secrets-store.csi.k8s.io
    ```

2.  Locate or add the `tokenRequests` section under `spec.driverConfig.secretsStore`. Set the type to `Managed` and configure the audience based on your cloud provider requirements:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: ClusterCSIDriver
    metadata:
      name: secrets-store.csi.k8s.io
    spec:
      driverConfig:
        driverType: SecretsStore
        secretsStore:
          tokenRequests:
            type: Managed
            managed:
              audiences:
                - audience: "api://AzureADTokenExchange"
                  expirationSeconds: 3600
    ```

    where:

    `spec.driverConfig.secretsStore.tokenRequests.managed.audiences[].audience`
    Specifies the audience value required by your cloud provider or secret management system. The audience must match the value configured in the trust policy of your cloud provider. For more information regarding audience value associated with different cloud providers, see corresponding cloud provider documentation.

    `spec.driverConfig.secretsStore.tokenRequests.managed.audiences[].expirationSeconds`
    Specifies the token validity duration in seconds. This parameter is optional. Valid range is 600 to 315,360,000 seconds. If omitted, the platform applies a default value.

3.  For environments that require multiple audiences, you can specify multiple audience entries:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: ClusterCSIDriver
    metadata:
      name: secrets-store.csi.k8s.io
    spec:
      driverConfig:
        driverType: SecretsStore
        secretsStore:
          tokenRequests:
            type: Managed
            managed:
              audiences:
                - audience: "sts.amazonaws.com"
                  expirationSeconds: 3600
                - audience: "api://AzureADTokenExchange"
                  expirationSeconds: 3600
    ```

4.  Save and apply the changes to the custom resource.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the Secrets Store CSI Driver Operator driver pods have been updated with the token request configuration by running the following command:

    ``` terminal
    $ oc get pods -n openshift-cluster-csi-drivers | grep secrets-store
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    secrets-store-csi-driver-node-bhp2d                  3/3     Running   0          45s
    secrets-store-csi-driver-node-xyz12                  3/3     Running   0          45s
    secrets-store-csi-driver-operator-74696fc7bc-qjrl8   1/1     Running   0          7m40s
    ```

    </div>

2.  Check the `ClusterCSIDriver` configuration to confirm the token request settings by running the following command:

    ``` terminal
    $ oc get clustercsidrivers.operator.openshift.io secrets-store.csi.k8s.io -o jsonpath='{.spec.driverConfig.secretsStore.tokenRequests}' | jq
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    {
      "managed": {
        "audiences": [
          {
            "audience": "api://AzureADTokenExchange",
            "expirationSeconds": 3600
          }
        ]
      },
      "type": "Managed"
    }
    ```

    </div>

3.  Create a test pod that mounts secrets from your external secret store to verify that Workload Identity Federation authentication works correctly by running the following command:

    ``` terminal
    $ oc apply -f <test_pod_yaml>
    ```

4.  Check the pod logs to confirm successful authentication and secret mounting by running the following command:

    ``` terminal
    $ oc logs <test_pod_name>
    ```

    Successful authentication indicates that the service account token with the specified audience is being accepted by your cloud provider’s identity federation system.

</div>

# Token request configuration parameters

You can configure Workload Identity Federation for the Secrets Store CSI Driver Operator by setting parameters in the `tokenRequests` section under `spec.driverConfig.secretsStore` of the `ClusterCSIDriver` custom resource. It enables credential-free authentication to cloud provider secret stores.

The following table describes the parameters available for configuring service account token requests:

| Parameter | Type | Description |
|----|----|----|
| `type` | String | Specifies the token request management mode. Set to `Managed` to enable Workload Identity Federation with operator-managed token configuration. When omitted, the Operator preserves any existing token request configuration on the `CSIDriver` object. |
| `managed.audiences` | Array of objects | Configures the service account token projection for Workload Identity Federation. Each entry specifies an audience and optional expiration. The Secrets Store CSI Driver Operator uses these tokens to authenticate to external secret management systems without storing long-lived credentials. This field is required when `type` is set to `Managed`. |
| `managed.audiences[].audience` | String | Specifies the intended audience claim (`aud`) for the projected service account token. The audience must match the value expected by the cloud provider’s identity federation system. Different cloud providers require different audience values. This field is required for each audience entry. |
| `managed.audiences[].expirationSeconds` | Integer | Specifies the token validity duration in seconds. Valid range is 600 to 315,360,000 seconds. If omitted, the platform applies a default value. |

Token request configuration parameters

Different cloud providers and secret management systems require specific audience values. For more information on audience values, see corresponding cloud provider documentation.

The following examples demonstrate different token request configurations for various cloud providers:

<div class="formalpara">

<div class="title">

Example 1: Azure Key Vault with Workload Identity

</div>

``` yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
  name: secrets-store.csi.k8s.io
spec:
  driverConfig:
    driverType: SecretsStore
    secretsStore:
      tokenRequests:
        type: Managed
        managed:
          audiences:
            - audience: "api://AzureADTokenExchange"
              expirationSeconds: 3600
```

</div>

<div class="formalpara">

<div class="title">

Example 2: AWS Secrets Manager with IAM Roles for Service Accounts

</div>

``` yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
  name: secrets-store.csi.k8s.io
spec:
  driverConfig:
    driverType: SecretsStore
    secretsStore:
      tokenRequests:
        type: Managed
        managed:
          audiences:
            - audience: "sts.amazonaws.com"
              expirationSeconds: 3600
```

</div>

<div class="formalpara">

<div class="title">

Example 3: HashiCorp Vault with Kubernetes authentication

</div>

``` yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
  name: secrets-store.csi.k8s.io
spec:
  driverConfig:
    driverType: SecretsStore
    secretsStore:
      tokenRequests:
        type: Managed
        managed:
          audiences:
            - audience: "vault.example.com"
```

</div>

<div class="formalpara">

<div class="title">

Example 4: Multiple token audiences for multi-cloud deployments

</div>

``` yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
  name: secrets-store.csi.k8s.io
spec:
  driverConfig:
    driverType: SecretsStore
    secretsStore:
      tokenRequests:
        type: Managed
        managed:
          audiences:
            - audience: "sts.amazonaws.com"
              expirationSeconds: 3600
            - audience: "api://AzureADTokenExchange"
              expirationSeconds: 3600
```

</div>

When configuring token request parameters, consider the following:

- The audience value must exactly match the value configured in your cloud provider’s trust policy or identity federation configuration.

- Token requests enable the Secrets Store CSI Driver Operator to obtain projected service account tokens with the specified audience claim.

- Different workloads can use different service accounts, allowing fine-grained access control through cloud provider IAM policies.

- Workload Identity Federation eliminates the need to store cloud provider credentials in OpenShift Container Platform, improving security.

- You must configure your cloud provider to trust your OpenShift Container Platform cluster’s OIDC provider before using Workload Identity Federation.

- Multiple audience values can be specified to support multi-cloud or hybrid deployments where different external secret stores require different audiences.

<div>

<div class="title">

Next steps

</div>

- [Mounting secrets from an external secrets store to a CSI volume](../../nodes/pods/nodes-pods-secrets-store.xml#mounting-secrets-external-secrets-store_nodes-pods-secrets-store)

</div>

# Uninstall the Secrets Store CSI Driver Operator

To remove the Secrets Store CSI Driver Operator and free cluster resources, uninstall the Operator after stopping applications and removing the CSI driver.

<div>

<div class="title">

Prerequisites

</div>

- Access to the OpenShift Container Platform web console.

- Administrator access to the cluster.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Stop all application pods that use the `secrets-store.csi.k8s.io` provider.

2.  Remove any third-party provider plug-in for your chosen secret store.

3.  Remove the Container Storage Interface (CSI) driver and associated manifests:

    1.  Click **Administration** → **CustomResourceDefinitions** → **ClusterCSIDriver**.

    2.  On the **Instances** tab, for **secrets-store.csi.k8s.io**, on the far left side, click the drop-down menu, and then click **Delete ClusterCSIDriver**.

    3.  When prompted, click **Delete**.

4.  Verify that the CSI driver pods are no longer running.

5.  Uninstall the Secrets Store CSI Driver Operator:

    > [!NOTE]
    > Before you can uninstall the Operator, you must remove the CSI driver first.

    1.  Click **Ecosystem** → **Installed Operators**.

    2.  On the **Installed Operators** page, scroll or type "Secrets Store CSI" into the **Search by name** box to find the Operator, and then click it.

    3.  On the upper, right of the **Installed Operators** \> **Operator details** page, click **Actions** → **Uninstall Operator**.

    4.  When prompted on the **Uninstall Operator** window, click the **Uninstall** button to remove the Operator from the namespace. Any applications deployed by the Operator on the cluster need to be cleaned up manually.

        After uninstalling, the Secrets Store CSI Driver Operator is no longer listed in the **Installed Operators** section of the web console.

</div>

# Additional resources

- [Configuring CSI volumes](../../storage/container_storage_interface/persistent-storage-csi.xml#persistent-storage-csi)
