You can customize the behavior of the External Secrets Operator for Red Hat OpenShift operand components by configuring custom annotations, deployment lifecycle settings, and environment variables through the `ExternalSecretsConfig` custom resource (CR).

These configurations provide administrators with fine-grained control over the external-secrets deployment.

You can customize the External Secrets Operator for Red Hat OpenShift operand by using the `ExternalSecretsConfig` custom resource (CR). The CR supports a set of deployment and runtime options, such as custom annotations, revision history limits, environment variables, resource limits, tolerations, and proxy settings—so you can control how the operand is deployed and run without editing the operand resources directly.

All supported options are defined in the `ExternalSecretsConfig` CR (for example under the `spec.controllerConfig` for controller-related settings). The Operator reconciles the operand from this CR. Changes made directly to operand resources are overwritten. Use the `ExternalSecretsConfig` CR as the only supported way to customize the operand.

For the complete list of fields and allowed values, see the `ExternalSecretsConfig` API reference in the External Secrets Operator for Red Hat OpenShift documentation.

<div>

<div class="title">

Additional resources

</div>

- [External Secrets Operator for Red Hat OpenShift APIs](../external_secrets_operator/external-secrets-operator-api.xml#external-secrets-operator-api)

</div>

# Set a log level for the External Secrets Operator for Red Hat OpenShift

You can configure the log verbosity for the lifecycle manager. You must adjust this setting to troubleshoot issues related to the installation, upgrade, or configuration of the operator itself, rather than secret synchronization.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

</div>

<div>

<div class="title">

Procedure

</div>

- Update the subscription object for the External Secrets Operator for Red Hat OpenShift to provide the verbosity level for the operator logs by running the following command:

  ``` terminal
  $ oc -n <external_secrets_operator_namespace> patch subscription openshift-external-secrets-operator --type='merge' -p '{"spec":{"config":{"env":[{"name":"OPERATOR_LOG_LEVEL","value":"<log_level>"}]}}}'
  ```

  where:

  external_secrets_operator_namespace
  Specifies the namespace where the Operator is installed.

  log_level
  Specifies the level of log detail. Values range from 1-5. The default is 2.

</div>

<div>

<div class="title">

Verification

</div>

1.  The External Secrets Operator pod is redeployed. Verify that the log level of the External Secrets Operator for Red Hat OpenShift is updated by running the following command:

    ``` terminal
    $ oc set env deploy/external-secrets-operator-controller-manager -n external-secrets-operator --list | grep -e OPERATOR_LOG_LEVEL -e container
    ```

    The following example verifies that the log level of the External Secrets Operator for Red Hat OpenShift is updated.

    ``` terminal
    # deployments/external-secrets-operator-controller-manager, container manager
    OPERATOR_LOG_LEVEL=2
    ```

2.  Verify that the log level of the External Secrets Operator for Red Hat OpenShift is updated by running the `oc logs` command:

    ``` terminal
    $ oc logs -n external-secrets-operator -f deployments/external-secrets-operator-controller-manager -c manager
    ```

</div>

# Set a log level for the External Secrets Operator for Red Hat OpenShift operand

You can troubleshoot common issues, such as secret synchronization failures, provider authentication errors, or data formatting problems, by configuring the log verbosity for the core controller.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Set the log level value by editing the `spec.appConfig.logLevel` section:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    ...
    spec:
      appConfig:
        logLevel: <log_level>
    ```

    where:

    log_level
    Supports the value range of 1-5. The log level gets mapped to the following operand support levels:

    - 1 - warnings

    - 2 - error logs

    - 3 - info logs

    - 4 and 5 - debug logs

3.  Save your changes and exit the editor.

</div>

# Configure cert-manager for the external-secrets certificate requirements

You can optionally configure cert-manager to manage certificates for the External Secrets Operator for Red Hat OpenShift webhook and plugins. If you do not use cert-manager, the Operator automatically generates webhook certificates, but you must manually configure certificates for any plugins.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

- You have installed the cert-manager Operator for Red Hat OpenShift. For more information, see "Installing the cert-manager Operator for Red Hat OpenShift"

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` custom resource by running the following command:

    ``` terminal
    $  oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Configure `cert-manager` by editing the `spec.controllerConfig.certProvider.certManager` section as follows:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    ...
    spec:
      controllerConfig:
        certProvider:
          certManager:
            injectAnnotations: "true"
            issuerRef:
              name: <issuer_name>
              kind: <issuer_kind>
              group: <issuer_group>
            mode: Enabled
    ```

    where:

    injectAnnotation
    Must be set to `true` when enabled.

    name
    Specifies the name of the issuer object referenced in `ExternalSecretsConfig`.

    kind
    Specifies the API issuer. Can be set to either `Issuer` or `ClusterIssuer`.

    group
    Specifies the API issuer group. The group name must be `cert-manager.io`.

    mode
    Must be set to `Enabled`. This is an immutable field and cannot be modified once it is configured.

3.  Save your changes.

4.  After you update the `cert-manager` configurations in the `externalsecretsconfig.operator.openshift.io` object, you must manually delete `external-secrets-cert-controller` deployment by running the following command. This prevents performance degradation of the `external-secrets` application.

    ``` terminal
    $ oc delete deployments.apps external-secrets-cert-controller -n external-secrets
    ```

5.  Optionally, you can delete other resources created for the `cert-controller` by running the following commands:

    ``` terminal
    $ oc delete clusterrolebindings.rbac.authorization.k8s.io external-secrets-cert-controller
    ```

    ``` terminal
    $ oc delete clusterroles.rbac.authorization.k8s.io external-secrets-cert-controller
    ```

    ``` terminal
    $ oc delete serviceaccounts external-secrets-cert-controller -n external-secrets
    ```

    ``` terminal
    $ oc delete secrets external-secrets-webhook -n external-secrets
    ```

</div>

<div id="external-secrets-log-levels_additional-resources">

<div class="title">

Additional resources

</div>

- [External Secrets Operator for Red Hat OpenShift APIs](../external_secrets_operator/external-secrets-operator-api.xml#external-secrets-operator-api)

- [cert-manager Operator for Red Hat Openshift](../cert_manager_operator/index.xml#cert-manager-operator-about)

- [Installing the cert-manager-Operator for Red Hat Openshift](../cert_manager_operator/cert-manager-operator-install.xml#cert-manager-operator-install)

</div>

# Configure the bitwardenSecretManagerProvider plugin

You must configure the `bitwardenSecretManagerProvider` plugin to enable communication with the Bitwarden API. This configuration enables the Operator to authenticate and fetch secrets for synchronization.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` custom resource by running the following command:

    ``` terminal
    $  oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Edit the `spec.plugins.bitwardenSecretManagerProvider` section as follows to enable the Bitwarden Secrets Manager:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    ...
    spec:
      plugins:
        bitwardenSecretManagerProvider:
          mode: Enabled
          secretRef:
            name: <secret_object_name>
    ```

    where:

    name
    The name of the secret containing the certificate key pair for the plugin. The key name in the secret for the certificate must be `tls.crt`. The key name for the private key must be `tls.key`. The key name for the Certificate Authority (CA) certificate key name must be `ca.crt`. Configuring the secret is optional when the cert-manager certificate provider is configured.

3.  Save your changes and exit the editor.

4.  If you disable the plugin the following resources must be deleted manually by running the following commands:

    ``` terminal
    $ oc delete deployments.apps bitwarden-sdk-server -n external-secrets
    ```

    ``` terminal
    $ oc delete certificates.cert-manager.io bitwarden-tls-certs -n external-secrets
    ```

    ``` terminal
    $ oc delete service bitwarden-sdk-server -n external-secrets
    ```

    ``` terminal
    $ oc delete serviceaccounts bitwarden-sdk-server -n external-secrets
    ```

</div>

# Add custom annotations to external-secrets resources

To customize your resources, you can define up to 20 custom annotations in the custom resource (CR). The Operator merges the annotations with the defaults, prioritizes them, and safely preserves annotations set by external systems.

When an annotation is removed from the CR, the Operator automatically removes it from all managed resources during the next reconciliation. Annotations set by external sources, such as Kubernetes system annotations or annotations added by other controllers, are preserved and are not affected by the Operator.

Annotation keys containing the following reserved domain prefixes are not allowed and are rejected by validation if applied:

- `kubernetes.io/` (including subdomains such as `*.kubernetes.io/`)

- `k8s.io/` (including subdomains such as `*.k8s.io/`)

- `openshift.io/` (including subdomains such as `*.openshift.io/`)

- `cert-manager.io/`

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Add the `annotations` field under `spec.controllerConfig` as follows:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    metadata:
      name: cluster
    spec:
      controllerConfig:
        annotations:
          prometheus.io/scrape: "true"
          example.com/environment: "production"
    ```

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that annotations are applied to the external-secrets deployment by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.metadata.annotations}' | jq .
    ```

    The output should include the custom annotations you specified.

2.  Verify that annotations are applied to the pod template by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.metadata.annotations}' | jq .
    ```

    The output should include the custom annotations you specified.

3.  Verify that annotations are applied to other managed resources such as Services by running the following command:

    ``` terminal
    $ oc get service external-secrets-webhook -n external-secrets -o jsonpath='{.metadata.annotations}' | jq .
    ```

    The output should include the custom annotations you specified.

</div>

# Configure the revisionHistoryLimit for external-secrets components

Configure the number of old `ReplicaSet` objects retained for rollback by setting the `revisionHistoryLimit` parameter for `external-secrets` components.

The following components can be configured:

| Component name | Description |
|----|----|
| `ExternalSecretsCoreController` | The main `external-secrets` controller. |
| `Webhook` | The `external-secrets` webhook server. |
| `CertController` | The certificate controller for webhook TLS. |
| `BitwardenSDKServer` | The Bitwarden SDK server plugin. |

Each component can only have one configuration entry. A maximum of 4 component configuration entries are allowed, one per component.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Add the `componentConfigs` field under `spec.controllerConfig` as follows:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    metadata:
      name: cluster
    spec:
      controllerConfig:
        componentConfigs:
          - componentName: ExternalSecretsCoreController
            deploymentConfigs:
              revisionHistoryLimit: 5
          - componentName: Webhook
            deploymentConfigs:
              revisionHistoryLimit: 3
    ```

    where

    `spec.controllerConfig.componentConfigs.componentName.deploymentConfigs.revisionHistoryLimit`
    Specifies the number of old `ReplicaSet` objects to retain for rollback. The value must be at least 1 to ensure rollback capability. The maximum value is 50. If not specified, the default is 10.

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the `revisionHistoryLimit` parameter is applied to the deployment by running the following command:

  ``` terminal
  $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.revisionHistoryLimit}'
  ```

  The output should display the value you configured.

</div>

# Set custom environment variables for external-secrets components

To configure component behavior at runtime or integrate with external services, set custom environment variables for individual `external-secrets` components.

Custom environment variables are merged with the default environment variables set by the Operator. User-specified variables take precedence in case of conflicts with the Operator defaults. A maximum of 50 custom environment variables can be specified per component.

The environment variable names starting with the following prefixes are reserved:

- `HOSTNAME`

- `KUBERNETES_`

- `EXTERNAL_SECRETS_`

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have created the `ExternalSecretsConfig` custom resource.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Add the `overrideEnv` field under the desired component in the `spec.controllerConfig.componentConfigs` stanza as follows:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    metadata:
      name: cluster
    spec:
      controllerConfig:
        componentConfigs:
          - componentName: ExternalSecretsCoreController
            overrideEnv:
              - name: Example
                value: "4"
    ```

    where

    `spec.controllerConfig.componentConfigs.overrideEnv.name`
    Specifies the name of the environment variable. Environment variable names starting with `HOSTNAME`, `KUBERNETES_`, or `EXTERNAL_SECRETS_` are reserved and are not allowed.

    `spec.controllerConfig.componentConfigs.overrideEnv.value`
    Specifies the value of the environment variable.

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the environment variable is set on the deployment by running the following command:

  ``` terminal
  $ oc set env deployment/external-secrets -n external-secrets --list
  ```

  The output should include the custom environment variable you specified.

</div>

# Enable optional features for External Secrets Operator for Red Hat OpenShift

The External Secrets Operator for Red Hat OpenShift supports optional capabilities that can be enabled cluster-wide through the `ExternalSecretsManager` custom resource (CR). Features are disabled by default and must be explicitly enabled.

You can enable or disable a feature at any time. The Operator reconciles the core controller deployment when the feature state changes, without requiring a restart or reinstallation.

> [!WARNING]
> `UnsafeAllowGenericTargets` is a pre-release feature. It is not recommended for production use. Enabling this feature allows `ExternalSecret` resources to write secret data to arbitrary Kubernetes resource types beyond Secret objects. This might cause data managed by other controllers to be overwritten and can expose sensitive values through non-secret resources. This feature provides no additional access control beyond standard Kubernetes role-based access control (RBAC).

When enabled, `ExternalSecret` resources can target arbitrary Kubernetes resource types as their sync destination, instead of being limited to `Secret` objects.

The Operator passes the `--unsafe-allow-generic-targets=true` flag to the core `external-secrets` controller. The webhook and cert-controller are not affected.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have installed the External Secrets Operator for Red Hat OpenShift and created the `ExternalSecretsConfig` CR.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsManager` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsmanagers.operator.openshift.io cluster
    ```

2.  Add the `features` field under `spec` and set the desired feature mode:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsManager
    metadata:
      name: cluster
    spec:
      features:
        - name: UnsafeAllowGenericTargets
          mode: Enabled
    ```

    To disable the feature, set `mode: Disabled` or remove the entry from the features list.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the feature flag is passed to the core controller by running the following command:

    ``` terminal
    $ oc get deployment external-secrets \
      -n external-secrets \
      -o jsonpath='{.spec.template.spec.containers[0].args}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    [
      "--concurrent=1",
      "--metrics-addr=:8080",
      "--loglevel=warn",
      "--zap-time-encoding=epoch",
      "--enable-leader-election=true",
      "--enable-push-secret-reconciler=true",
      "--enable-cluster-store-reconciler=true",
      "--enable-cluster-external-secret-reconciler=true",
      "--unsafe-allow-generic-targets=true"
    ]
    ```

    </div>

    When the feature is enabled, the output includes `--unsafe-allow-generic-targets=true`. When disabled or not configured, the flag is absent.

2.  Verify that the `ExternalSecretsManager` CR reflects the configured feature by running the following command:

    ``` terminal
    $ oc get externalsecretsmanagers.operator.openshift.io cluster -o jsonpath='{.spec.features}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    [
      {
        "mode": "Enabled",
        "name": "UnsafeAllowGenericTargets"
      }
    ]
    ```

    </div>

</div>

# Mount a custom trusted certificate authority bundle for external-secrets

You can configure the External Secrets Operator for Red Hat OpenShift to trust a custom certificate authority (CA) bundle when the `external-secrets` core controller communicates with external secret backends over transport layer socket (TLS).

This is required when your organization uses a private CA or a self-signed certificate that is not included in the default system truststore.

To enable mounting a custom trusted CA, you reference a `ConfigMap` that contains the Privacy Enhanced Mail (PEM)-encoded CA certificates in the `spec.controllerConfig.trustedCABundle` field of the `ExternalSecretsConfig` custom resource (CR). The Operator mounts the bundle into the core controller pod and configures the TLS library to use it alongside the default system trust stores.

The External Secrets Operator for Red Hat OpenShift applies the following rules to the CA bundle `ConfigMap`:

- The `ConfigMap` must reside in the `external-secrets` namespace and must contain only PEM-encoded X.509 CA certificates. Leaf certificates and private key PEM blocks are rejected.

- If the `ConfigMap` key contains an invalid bundle, the `ExternalSecretsConfig` CR enters a `Degraded` state. The Operator automatically recovers and mounts the bundle when the `ConfigMap` is corrected, without requiring manual intervention.

- If the referenced `ConfigMap` does not exist, the Operator removes any previously mounted CA bundle from the core controller deployment and sets the `ExternalSecretsConfig` CR to a `Degraded` state until the `ConfigMap` is created.

- The CA bundle is mounted only on the core `external-secrets` controller container. The webhook and cert-controller containers are not affected.

- If the `ConfigMap` has the `config.openshift.io/inject-trusted-cabundle: "true"` label and a cluster proxy is configured, the Operator skips the user-defined mount. The cluster-wide CA bundle injected by the Cluster Network Operator (CNO) is already available to the controller through the proxy CA bundle mechanism.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have installed the External Secrets Operator for Red Hat OpenShift and created the `ExternalSecretsConfig` CR.

- A `ConfigMap` containing PEM-encoded X.509 CA certificates exists in the `external-secrets` namespace.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create the `ConfigMap` containing your CA bundle by running the following command:

    ``` terminal
    $ oc create configmap user-ca-bundle \
      --from-file=ca-bundle.crt=/path/to/ca.pem \
      -n external-secrets
    ```

2.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

3.  Add the `trustedCABundle` field under `spec.controllerConfig`:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    metadata:
      name: cluster
    spec:
      controllerConfig:
        trustedCABundle:
          name: user-ca-bundle
          key: ca-bundle.crt
    ```

    where:

    `spec.controllerConfig.trustedCABundle.name`
    Specifies the name of the `ConfigMap` in the `external-secrets` namespace that contains the CA certificate bundle.

    `spec.controllerConfig.trustedCABundle.key`
    Optional. Specifies the key within the `ConfigMap` that holds the PEM-encoded CA bundle. The default is `ca-bundle.crt`.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the CA bundle volume is mounted on the core controller deployment by running the following command:

    ``` terminal
    $ oc get deployment external-secrets \
      -n external-secrets \
      -o jsonpath='{.spec.template.spec.volumes}' | jq '.[] | select(.name=="user-ca-bundle")'
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "configMap": {
        "defaultMode": 420,
        "items": [
          {
            "key": "ca-bundle.crt",
            "path": "ca-bundle.crt"
          }
        ],
        "name": "trusted-ca-bundle-for-es"
      },
      "name": "user-ca-bundle"
    }
    ```

    </div>

2.  Verify that the `SSL_CERT_DIR` is set on the core controller container by running the following command:

    ``` terminal
    $ oc set env deployment/external-secrets \
      -n external-secrets \
      --list | grep SSL_CERT_DIR
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    SSL_CERT_DIR=/etc/pki/tls/user-certs:/etc/pki/tls/certs:/etc/ssl/certs
    ```

    </div>

3.  Verify that the `ExternalSecretsConfig` CR is not in a `Degraded` state by running the following command:

    ``` terminal
    $ oc get externalsecretsconfigs.operator.openshift.io cluster \
      -o jsonpath='{.status.conditions[?(@.type=="Degraded")]}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "lastTransitionTime": "2026-06-22T10:29:11Z",
      "message": "",
      "observedGeneration": 5,
      "reason": "Ready",
      "status": "False",
      "type": "Degraded"
    }
    ```

    </div>

    The `Degraded` condition should show `"status": "False"`. If the condition is `True,` review the message field for the specific validation error and correct the referenced `ConfigMap`.

</div>

# Override operand container arguments for the External Secrets Operator for Red Hat OpenShift

You can override container arguments for the `external-secrets` operand deployments by setting environment variables on the External Secrets Operator for Red Hat OpenShift subscription. Use this method when you need to pass additional or replacement `--key=value` flags to operand containers.

> [!NOTE]
> This is a temporary feature available only in the External Secrets Operator for Red Hat OpenShift 1.1 and 1.2 z-streams. External Secrets Operator for Red Hat OpenShift 1.3.0 adds support in the `ExternalSecretsConfig` API to configure the same behavior. Consider migrating to the `ExternalSecretsConfig` API when upgrading to External Secrets Operator 1.3.0. This subscription-based method is scheduled to be deprecated and removed in External Secrets Operator for Red Hat OpenShift 1.4.0.

<div>

<div class="title">

Prerequisites

</div>

- Your installed External Secrets Operator for Red Hat OpenShift version is 1.1 or 1.2.

- You have access to the cluster as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

- Update the Subscription for the External Secrets Operator to set the operand argument overrides by running the following command:

  ``` terminal
  $ oc -n <external_secrets_operator_namespace> patch subscription openshift-external-secrets-operator --type='merge' -p '{"spec":{"config":{"env":[{"name":"OPERAND_EXTERNAL_SECRETS_ARGS","value":"<controller_args>"},{"name":"OPERAND_WEBHOOK_ARGS","value":"<webhook_args>"},{"name":"OPERAND_CERT_CONTROLLER_ARGS","value":"<cert_controller_args>"},{"name":"OPERAND_BITWARDEN_SDK_SERVER_ARGS","value":"<bitwarden_args>"}]}}}'
  ```

  where:

  `<external_secrets_operator_namespace>`
  Specifies the namespace where the Operator is installed.

  `<controller_args>`
  Specifies a comma-separated list of `--key` or `--key=value` flags for the `external-secrets` core controller. For example, `--concurrent=2,--loglevel=debug`.

  `<webhook_args>`
  Specifies a comma-separated list of flags for the webhook. Commas inside a flag value are preserved when the next flag begins with `--`. For example, `--tls-ciphers=TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,--loglevel=debug`.

  `<cert_controller_args>`
  Specifies a comma-separated list of flags for the `cert-controller`. For example, `--crd-requeue-interval=10m,--loglevel=debug`.

  `<bitwarden_args>`
  Specifies a comma-separated list of flags for the `bitwarden-sdk-server`. For example, `--key-file=/certs/key.pem,--cert-file=/certs/cert.pem`.

  Set only the environment variables you need. Omit any unused entries from the `env` list.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the environment variables are set on the Operator by running the following command:

    ``` terminal
    $ oc set env deploy/external-secrets-operator-controller-manager -n <external_secrets_operator_namespace> --list | grep -e OPERAND_ -e container
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    $ deployments/external-secrets-operator-controller-manager, container manager
    OPERAND_EXTERNAL_SECRETS_ARGS=--concurrent=2,--loglevel=debug
    OPERAND_WEBHOOK_ARGS=--tls-ciphers=TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,--loglevel=debug
    ```

    </div>

2.  Verify that the operand `Deployment` container arguments were updated by running the following command:

    ``` terminal
    $ oc get deploy/external-secrets-webhook -n <operand_namespace> -o jsonpath='{.spec.template.spec.containers[0].args}'
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    $ ["webhook","--dns-name=external-secrets-webhook.external-secrets.svc","--port=10250","--cert-dir=/tmp/certs","--check-interval=15m0s","--metrics-addr=:8080","--healthz-addr=:8081","--loglevel=debug","--zap-time-encoding=epoch","--tls-ciphers=TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"]
    ```

    </div>

</div>

# Replicas for external-secrets components

Set the `replicas` field to run more than one pod for each `external-secrets` component in the External Secrets Operator for Red Hat OpenShift. Multiple replicas keep the component available if a pod fails.

The following components support replica settings:

| Component name | Description |
|----|----|
| `ExternalSecretsCoreController` | Main `external-secrets` controller |
| `Webhook` | `external-secrets` webhook server |
| `CertController` | Certificate controller for webhook Transport Layer Security (TLS) certificates |
| `BitwardenSDKServer` | Bitwarden SDK server plugin |

Components that support replica settings

You can add one configuration entry for each component, for a maximum of four entries.

## Leader election

Leader election ensures that only one replica of a controller processes changes at a time, even when several replicas are running.

- For the `ExternalSecretsCoreController` and `CertController` components, the External Secrets Operator for Red Hat OpenShift always sets `--enable-leader-election=true` in the container arguments. Leader election stays enabled even when you set `replicas` to 1. During rolling updates, two pods can briefly run, and only one replica processes changes.

- For `Webhook` and `BitwardenSDKServer`, neither component uses leader election, regardless of the `replicas` count.

# Configure replicas for external-secrets components

Run more than one pod of an `external-secrets` component in the External Secrets Operator by setting the `replicas` field in the `ExternalSecretsConfig` custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have installed the OpenShift CLI (`oc`).

- You have created the `ExternalSecretsConfig` CR.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Add the `componentConfigs` field under `spec.controllerConfig` as follows:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    metadata:
      name: cluster
    spec:
      controllerConfig:
        componentConfigs:
          - componentName: ExternalSecretsCoreController
            deploymentConfigs:
              replicas: 2
          - componentName: Webhook
            deploymentConfigs:
              replicas: 2
    ```

    where:

    `spec.controllerConfig.componentConfigs.componentName.deploymentConfigs.replicas`
    Specifies the desired number of pod replicas for the component deployment. The value must be at least 1. The maximum value is 10. If you do not specify a value, the default is 1.

3.  Save the file.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the deployment uses the `replicas` value by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.replicas}'
    ```

    The output displays the `replicas` value you configured.

2.  Verify that the `ExternalSecretsCoreController` component uses leader election by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.spec.containers[?(@.name=="external-secrets")].args}'
    ```

    The output includes `--enable-leader-election=true`.

3.  Optional: Verify that a replica holds a leader election lease in the operand namespace by running the following command:

    ``` terminal
    $ oc get lease -n external-secrets
    ```

    The output lists a lease with a non-empty holder identity for the active leader.

4.  Optional: If the cluster runs the `CertController` component, verify that the component uses leader election by running the following command:

    ``` terminal
    $ oc get deployment external-secrets-cert-controller -n external-secrets -o jsonpath='{.spec.template.spec.containers[?(@.name=="cert-controller")].args}'
    ```

    The output includes `--enable-leader-election=true`.

</div>

# Advanced overrides for external-secrets component deployments

You can customize pod placement, container arguments, and resource settings for External Secrets Operator components. Advanced overrides let you change deployment settings when dedicated configuration fields do not provide the options you need.

> [!WARNING]
> Do not set the `advancedOverrides` field unless necessary. A field outside the allowed paths fails validation and sets the `ExternalSecretsConfig` custom resource (CR) to the `Degraded` condition.

The following components support the `advancedOverrides` field:

| Component name | Description |
|----|----|
| `ExternalSecretsCoreController` | Main `external-secrets` controller |
| `Webhook` | `external-secrets` webhook server |
| `CertController` | Certificate controller for the webhook Transport Layer Security certificates |
| `BitwardenSDKServer` | Bitwarden SDK server plugin |

Components that support the `advancedOverrides` field

You can add one configuration entry per component, up to four entries.

Set the `advancedOverrides` field in the relevant entry of the `spec.controllerConfig.componentConfigs` list in the `ExternalSecretsConfig` CR.

You can use only the following `Deployment` field paths in the `advancedOverrides` field:

`spec.template.spec.affinity`
Specifies the rules that place the pods on specific nodes or keep them apart from other pods.

`spec.template.spec.tolerations`
Specifies the taints that the pods can tolerate when scheduled on nodes.

`spec.template.spec.nodeSelector`
Specifies the node labels that a node must have for the pods to run on it.

`spec.template.spec.topologySpreadConstraints`
Specifies how the pods spread across zones or nodes.

`spec.template.spec.containers[*].args`
Specifies the command-line flags that the containers use at startup.

`spec.template.spec.containers[*].resources`
Specifies the CPU and memory requests and limits for the containers.

If you configure the same deployment setting through both the `advancedOverrides` field and a dedicated field, such as `spec.appConfig.affinity`, the `advancedOverrides` value applies.

Set the following fields in the relevant `componentConfigs` entry, not in its `advancedOverrides` field:

- `deploymentConfigs.replicas`

- `deploymentConfigs.revisionHistoryLimit`

- `overrideEnv`

The External Secrets Operator merges overrides from the `args` field with the managed arguments by flag name. The External Secrets Operator keeps the other default flags. Specify only the flags that you want to change or add. For the `ExternalSecretsCoreController` and `CertController` components, `--enable-leader-election=true` remains enabled unless you override it.

# Override scheduling, arguments, and resources for external-secrets components

Customize an `external-secrets` component deployment to meet your scheduling and resource requirements or to change its container arguments. Set the `advancedOverrides` field for the relevant component in the `componentConfigs` list of the `ExternalSecretsConfig` custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- You have installed the OpenShift CLI (`oc`).

- You have installed `jq`.

- You have created the `ExternalSecretsConfig` CR.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ExternalSecretsConfig` CR by running the following command:

    ``` terminal
    $ oc edit externalsecretsconfigs.operator.openshift.io cluster
    ```

2.  Add the `componentConfigs` field under the `spec.controllerConfig`. Include only the overrides that you need, as in the following example:

    ``` yaml
    apiVersion: operator.openshift.io/v1alpha1
    kind: ExternalSecretsConfig
    metadata:
      name: cluster
    spec:
      controllerConfig:
        componentConfigs:
          - componentName: ExternalSecretsCoreController
            advancedOverrides:
              spec:
                template:
                  spec:
                    affinity:
                      podAntiAffinity:
                        preferredDuringSchedulingIgnoredDuringExecution:
                          - weight: 100
                            podAffinityTerm:
                              topologyKey: kubernetes.io/hostname
                              labelSelector:
                                matchLabels:
                                  app: external-secrets
                    topologySpreadConstraints:
                      - maxSkew: 1
                        topologyKey: topology.kubernetes.io/zone
                        whenUnsatisfiable: ScheduleAnyway
                    containers:
                      - name: external-secrets
                        args:
                          - --concurrent=20
                          - --client-burst=200
                          - --client-qps=100
                        resources:
                          requests:
                            cpu: 200m
                            memory: 256Mi
                          limits:
                            cpu: "1"
                            memory: 512Mi
    ```

    where:

    `spec.controllerConfig.componentConfigs.componentName`
    Specifies the component to override, such as `ExternalSecretsCoreController`, `Webhook`, `CertController`, or `BitwardenSDKServer`.

    `spec.controllerConfig.componentConfigs.advancedOverrides`
    Specifies the changes to apply to the `Deployment` of the component. Include only the allowed `Deployment` field paths. You can omit `containers[].name`. If you set `containers[].name`, the name must match the component container name.

3.  Save the file.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the `ExternalSecretsConfig` CR is ready by running the following command:

    ``` terminal
    $ oc get externalsecretsconfigs.operator.openshift.io cluster -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
    ```

    The output is `True`.

2.  Verify that the `Deployment` uses the `affinity` override by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.spec.affinity}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "podAntiAffinity": {
        "preferredDuringSchedulingIgnoredDuringExecution": [
          {
            "podAffinityTerm": {
              "labelSelector": {
                "matchLabels": {
                  "app": "external-secrets"
                }
              },
              "topologyKey": "kubernetes.io/hostname"
            },
            "weight": 100
          }
        ]
      }
    }
    ```

    </div>

3.  Verify that the `Deployment` uses the `topologySpreadConstraints` override by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.spec.topologySpreadConstraints}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    [
      {
        "maxSkew": 1,
        "topologyKey": "topology.kubernetes.io/zone",
        "whenUnsatisfiable": "ScheduleAnyway"
      }
    ]
    ```

    </div>

4.  Verify that the `Deployment` uses the container `resources` override by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.spec.containers[?(@.name=="external-secrets")].resources}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "limits": {
        "cpu": "1",
        "memory": "512Mi"
      },
      "requests": {
        "cpu": "200m",
        "memory": "256Mi"
      }
    }
    ```

    </div>

5.  Verify that the External Secrets Operator merges the `args` overrides with the default flags by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.spec.containers[?(@.name=="external-secrets")].args}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    [
      "--concurrent=20",
      "--metrics-addr=:8080",
      "--loglevel=warn",
      "--zap-time-encoding=epoch",
      "--enable-leader-election=true",
      "--enable-push-secret-reconciler=true",
      "--enable-cluster-store-reconciler=true",
      "--enable-cluster-external-secret-reconciler=true",
      "--client-burst=200",
      "--client-qps=100"
    ]
    ```

    </div>

</div>

# Transport Layer Security profile support

Control secure connections for the External Secrets Operator for Red Hat OpenShift through the cluster Transport Layer Security (TLS) profile. The profile determines the minimum TLS version and cipher suites for the Operator and its operands.

The cluster defines the profile in the `apiserver.config.openshift.io/cluster` `APIServer` custom resource (CR). When the profile is in effect, the External Secrets Operator applies it to the following components:

- The secure serving endpoints of the External Secrets Operator for metrics and the webhook.

- The `external-secrets`, `external-secrets-webhook`, and `external-secrets-cert-controller` operand `Deployment` objects.

- The `bitwarden-sdk-server` operand `Deployment`, when you enable it.

The External Secrets Operator injects the following operand container arguments, derived from the cluster TLS security profile:

- `--tls-min-version=<version>`

- `--tls-ciphers=<cipher_list>`

When the minimum TLS version is 1.3, such as with the `Modern` profile, the External Secrets Operator omits the `--tls-ciphers` argument.

## Transport Layer Security adherence

To apply the cluster TLS security profile to the External Secrets Operator, set the `spec.tlsAdherence` field to `StrictAllComponents` in the `APIServer` CR. This setting requires cluster-wide adherence.

If you leave the `spec.tlsAdherence` field unset or select `LegacyAdheringComponentsOnly`, the External Secrets Operator and the operands retain their default TLS settings.

When the TLS security profile or the adherence policy changes, the External Secrets Operator restarts. The restart reloads the new settings and reconciles operand `Deployment` objects.

# Configure the Transport Layer Security profile

Align secure connections with your cluster policy by configuring the Transport Layer Security (TLS) profile for the External Secrets Operator for Red Hat OpenShift. Enable `StrictAllComponents` adherence in the `APIServer` custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have installed the OpenShift CLI (`oc`).

- You have installed `jq`.

- You have installed the External Secrets Operator for Red Hat OpenShift.

- You have created an `ExternalSecretsConfig` CR and confirmed that the `external-secrets` operand `Deployment` is available.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the cluster `APIServer` CR by running the following command:

    ``` terminal
    $ oc edit apiserver cluster
    ```

2.  Set the `spec.tlsSecurityProfile` field to the profile you require.

    The profile can be `Old`, `Intermediate`, `Modern`, or `Custom`. If you omit this field, the platform default is `Intermediate`.

3.  Set the `spec.tlsAdherence` field to `StrictAllComponents` to apply the cluster TLS security profile to the External Secrets Operator and the operands. The following example shows the resulting configuration with the `Intermediate` profile and cluster-wide adherence:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
      name: cluster
    spec:
      tlsSecurityProfile:
        type: Intermediate
        intermediate: {}
      tlsAdherence: StrictAllComponents
    ```

    where:

    `spec.tlsAdherence`
    If you omit this field or select `LegacyAdheringComponentsOnly`, the External Secrets Operator and the operands use the default TLS settings.

    Explicit operand argument overrides take precedence over TLS arguments derived from the cluster profile.

4.  Save your changes.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify the TLS security profile on the `APIServer` CR by running the following command:

    ``` terminal
    $ oc get apiserver cluster -o jsonpath='{.spec.tlsSecurityProfile}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "intermediate": {},
      "type": "Intermediate"
    }
    ```

    </div>

2.  Verify that the External Secrets Operator pod logged that the cluster TLS profile is in use by running the following command:

    ``` terminal
    $ oc logs -n external-secrets-operator deploy/external-secrets-operator-controller-manager -c manager | grep -i 'cluster TLS'
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    I1116 14:38:46.710262       1 main.go:315] "cluster TLS profile will be used for both operator and operands" logger="setup" profileType="Intermediate"
    ```

    </div>

3.  Verify that the `external-secrets` operand `Deployment` includes the TLS arguments by running the following command:

    ``` terminal
    $ oc get deployment external-secrets -n external-secrets -o jsonpath='{.spec.template.spec.containers[?(@.name=="external-secrets")].args}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    [
      "--concurrent=1",
      "--metrics-addr=:8080",
      "--loglevel=warn",
      "--zap-time-encoding=epoch",
      "--enable-leader-election=true",
      "--enable-push-secret-reconciler=true",
      "--enable-cluster-store-reconciler=true",
      "--enable-cluster-external-secret-reconciler=true",
      "--tls-min-version=1.2",
      "--tls-ciphers=TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"
    ]
    ```

    </div>

4.  Optional: Check the webhook `Deployment` by running the following command:

    ``` terminal
    $ oc get deployment external-secrets-webhook -n external-secrets -o jsonpath='{.spec.template.spec.containers[?(@.name=="webhook")].args}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    [
      "webhook",
      "--dns-name=external-secrets-webhook.external-secrets.svc",
      "--port=10250",
      "--cert-dir=/tmp/certs",
      "--check-interval=5m0s",
      "--metrics-addr=:8080",
      "--healthz-addr=:8081",
      "--loglevel=warn",
      "--zap-time-encoding=epoch",
      "--tls-min-version=1.2",
      "--tls-ciphers=TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"
    ]
    ```

    </div>

</div>

# Additional resources

- [Configuring TLS security profiles](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/security_and_compliance/tls-security-profiles)
