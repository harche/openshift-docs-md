You can configure a dedicated proxy for the authentication stack to reach external identity providers without using the cluster-wide egress proxy. This limits proxy-based egress to authentication components only.

# Component-scoped proxy for authentication

A component-scoped proxy allows the Cluster Authentication Operator (CAO) and the OAuth server to reach external identity providers (IdPs) without using the cluster-wide egress proxy. This limits proxy-based egress to authentication components only.

The OAuth server calls IdP endpoints on every login for OpenID Connect (OIDC) discovery, token exchange, user info retrieval, and group membership resolution. The CAO validates IdP connectivity through the proxy on each configuration change.

> [!IMPORTANT]
> Component-scoped proxy for authentication is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

## When to use a component-scoped proxy

Use a component-scoped proxy to restrict proxy-based egress to authentication components. Use the cluster-wide proxy when all components share the same proxy.

When `spec.proxy` is set on the `Authentication` operator resource, it fully replaces the cluster-wide proxy for authentication components. No fields are inherited.

## Proxy precedence

The authentication stack resolves proxy configuration as follows:

1.  When `spec.proxy` is set, authentication components use only those settings.

2.  When `spec.proxy` is absent, authentication components fall back to the cluster-wide proxy.

3.  When neither is configured, no proxy is used.

## Scope and limitations

The component-scoped proxy applies to the following:

- Cluster Authentication Operator (CAO)

- OAuth server

The component-scoped proxy does not apply to the following:

- Hosted control planes: The CAO does not run in these environments.

- MicroShift: The authentication stack is not present.

- External OIDC mode: Not included in the initial implementation.

- Per-identity-provider proxy: Different proxy settings for different identity providers are not supported.

LDAP group sync `CronJob` resources are not managed by the authentication operator. Configure proxy settings on the `CronJob` pod specification independently.

# Configuring a component-scoped proxy for authentication

You can configure a component-scoped proxy for the authentication stack by setting the `spec.proxy` field on the `Authentication` operator resource.

<div>

<div class="title">

Prerequisites

</div>

- You have cluster administrator privileges.

- You have installed the OpenShift CLI (`oc`).

- You have installed the `jq` CLI tool.

- The `AuthenticationComponentProxy` feature gate is enabled by applying the `TechPreviewNoUpgrade` or `DevPreviewNoUpgrade` feature set. For more information, see "Enabling features using feature gates".

- You have a working HTTP or HTTPS proxy server accessible from the cluster nodes.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Optional: If the proxy requires a custom CA certificate, create a config map in the `openshift-config` namespace containing the CA bundle:

    1.  Create a file called `auth-proxy-ca-bundle.yaml` with the following content:

        ``` yaml
        apiVersion: v1
        kind: ConfigMap
        metadata:
          name: auth-proxy-ca-bundle
          namespace: openshift-config
        data:
          ca-bundle.crt: |
            -----BEGIN CERTIFICATE-----
            <PEM_encoded_CA_certificate>
            -----END CERTIFICATE-----
        ```

        `name`
        Specifies the config map name. Use this name in the `spec.proxy.trustedCA.name` field.

        `namespace`
        Specifies the namespace. Must be `openshift-config`.

        `ca-bundle.crt`
        Specifies the Privacy-Enhanced Mail (PEM)-encoded CA certificate bundle. The key must be `ca-bundle.crt`.

    2.  Create the config map by running the following command:

        ``` terminal
        $ oc create -f auth-proxy-ca-bundle.yaml
        ```

        Alternatively, if you already have the CA certificate file, you can create the config map directly by running the following command:

        ``` terminal
        $ oc create configmap auth-proxy-ca-bundle \
          --from-file=ca-bundle.crt=<path_to_ca_certificate> \
          -n openshift-config
        ```

        `<path_to_ca_certificate>`
        Specifies the path to the PEM-encoded CA certificate file.

2.  Edit the `Authentication` operator resource to add the proxy configuration by running the following command:

    ``` terminal
    $ oc edit authentication.operator.openshift.io cluster
    ```

3.  Add the `spec.proxy` field with your proxy settings:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: Authentication
    metadata:
      name: cluster
    spec:
      managementState: Managed
      proxy:
        httpProxy: "http://proxy.example.com:3128"
        httpsProxy: "http://proxy.example.com:3128"
        noProxy:
          - ".example.com"
          - "idp.internal.example.com"
        trustedCA:
          name: "auth-proxy-ca-bundle"
    ```

    `httpProxy`
    Specifies the proxy URL for HTTP requests. At least one of `httpProxy` or `httpsProxy` is required.

    `httpsProxy`
    Specifies the proxy URL for HTTPS requests. At least one of `httpProxy` or `httpsProxy` is required.

    `noProxy`
    Specifies hostnames, domains, CIDR ranges, or IP addresses that bypass the proxy. Cluster-internal defaults (`.cluster.local`, `.svc`, `127.0.0.1`, the Kubernetes API service IP, and `localhost`) are appended automatically. Maximum 64 entries.

    `trustedCA`
    Specifies the config map name in `openshift-config` containing the proxy CA bundle under the key `ca-bundle.crt`. Required only if the proxy uses TLS interception or a private CA. Omit this block if you did not create a CA config map in step 1.

4.  Save the file to apply the changes.

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the configuration was accepted by running the following command:

  ``` terminal
  $ oc get authentication.operator.openshift.io cluster -o jsonpath='{.spec.proxy}' | jq .
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` json
  {
    "httpProxy": "http://proxy.example.com:3128",
    "httpsProxy": "http://proxy.example.com:3128",
    "noProxy": [
      ".example.com",
      "idp.internal.example.com"
    ],
    "trustedCA": {
      "name": "auth-proxy-ca-bundle"
    }
  }
  ```

  </div>

- Verify that the authentication operator is not reporting errors by running the following command:

  ``` terminal
  $ oc get clusteroperator authentication
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME             VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
  authentication   {product-version}.0     True        False         False      10m
  ```

  </div>

  The `AVAILABLE` column shows `True` and the `DEGRADED` column shows `False`.

- Optional: Test authentication through the proxy by running the following command:

  ``` terminal
  $ oc login
  ```

</div>

Changing the proxy URL triggers an OAuth server redeployment. On single-node OpenShift Container Platform deployments, this causes a brief authentication outage. Updates to `trustedCA` config map content are hot-reloaded without redeployment.

> [!WARNING]
> A misconfigured proxy can prevent the OAuth server from reaching the identity provider, locking all users out of the cluster. To recover, log in with `kubeadmin` credentials or client certificate authentication, both of which bypass OAuth, and correct the proxy configuration.

<div>

<div class="title">

Additional resources

</div>

- [Enabling features using feature gates](../nodes/clusters/nodes-cluster-enabling-features.xml#nodes-cluster-enabling-features)

</div>

# Authentication operator proxy field reference

The `spec.proxy` object of the `Authentication` operator resource (`operator.openshift.io/v1`) defines proxy and trusted CA settings for authentication components.

| Field | Type | Description |
|----|----|----|
| `httpProxy` | `string` | Specifies the proxy URL for HTTP requests. Must use the `http` or `https` scheme with a non-empty hostname and no path, query parameters, or fragment. User credentials are allowed (for example, `http://user:password@proxy:3128`). Maximum 2048 characters. At least one of `httpProxy` or `httpsProxy` is required. |
| `httpsProxy` | `string` | Specifies the proxy URL for HTTPS requests. Same format rules as `httpProxy`. At least one of `httpProxy` or `httpsProxy` is required. |
| `noProxy` | `[]string` | Specifies hostnames, domains, CIDR ranges, or IP addresses that bypass the proxy. Each entry must be 1-253 characters. Maximum 64 entries. Duplicates are not permitted. Cluster-internal defaults (`.cluster.local`, `.svc`, `127.0.0.1`, the Kubernetes API service IP, and `localhost`) are appended automatically. |
| `trustedCA.name` | `string` | Specifies the name of a config map in the `openshift-config` namespace containing a CA certificate bundle under the key `ca-bundle.crt`. This bundle is appended to the system truststore for proxy TLS connections. When omitted, only the system truststore is used. Must be a valid DNS subdomain name (RFC 1123): at most 253 characters, lowercase alphanumeric characters, hyphens, or periods. |

`spec.proxy` fields

## Behavioral notes

- When `spec.proxy` is set, it fully replaces the cluster-wide proxy for authentication. No fields are inherited.

- The proxy validation controller tests IdP connectivity on every configuration change and emits `OperatorStatusChanged` events when endpoints are unreachable.

- Proxy-level failures such as connection refused or TLS handshake errors cause the `Available` condition to report `False`. The `Degraded` condition remains `False` but includes diagnostic details from the `ProxyConfigController` sub-controller in its message.

- The operator injects `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables into the OAuth server pod specification. Changes to these values trigger a redeployment.

- The `trustedCA` config map is synced from `openshift-config` to `openshift-authentication` by the operator. The OAuth server hot-reloads the mounted CA file without redeployment.

# Troubleshooting authentication proxy connectivity

If you encounter issues with the component-scoped proxy, you can diagnose and resolve them by reviewing operator conditions, events, and pod environment variables.

Proxy-related operator events
The authentication operator emits events when proxy configuration changes cause failures. Check recent events by running the following command:

``` terminal
$ oc get events -n openshift-authentication-operator --sort-by=.lastTimestamp
```

Look for events with `reason: OperatorStatusChanged` that reference proxy connection errors. Verify that the proxy URL is correct, the proxy server is running, and the cluster nodes can reach the proxy.

Authentication operator reports proxy errors
A proxy-level failure such as connection refused, DNS resolution failure, or TLS handshake error causes the `Available` condition to report `False`. The `Degraded` condition message includes diagnostic details from the `ProxyConfigController` sub-controller even though the `Degraded` status remains `False`. Check the operator status by running the following command:

``` terminal
$ oc get clusteroperator authentication -o jsonpath='{.status.conditions}' | jq .
```

<div class="formalpara">

<div class="title">

Example output

</div>

``` json
[
  {
    "type": "Available",
    "status": "False",
    "reason": "OAuthServerRouteEndpointAccessibleController_EndpointUnavailable",
    "message": "OAuthServerRouteEndpointAccessibleControllerAvailable: Get \"https://oauth-openshift.apps.example.com/healthz\": proxyconnect tcp: dial tcp: lookup proxy.example.com: no such host"
  },
  {
    "type": "Progressing",
    "status": "True",
    "reason": "OAuthServerDeployment_PodsUpdating",
    "message": "deployment/oauth-openshift: 3/3 pods have been updated to the latest generation and 1/3 pods are available"
  },
  {
    "type": "Degraded",
    "status": "False",
    "reason": "AsExpected",
    "message": "ProxyConfigControllerDegraded: failed to reach endpoint with error: Get \"https://oauth-openshift.apps.example.com/healthz\": proxyconnect tcp: dial tcp: lookup proxy.example.com: no such host"
  }
]
```

</div>

The `Available` condition shows `False` when the proxy is unreachable. The `Degraded` condition remains `False` but includes proxy error details from the `ProxyConfigController` in its message. Check both conditions when diagnosing proxy issues.

Verify that the proxy server is running, the proxy URL and port are correct, and the `trustedCA` config map contains valid PEM-encoded certificates.

All users locked out after proxy misconfiguration
A misconfigured proxy can lock out all OAuth-authenticated users. To recover access:

1.  Log in by using `kubeadmin` credentials or client certificate authentication, both of which bypass OAuth.

2.  Correct the proxy configuration by running the following command:

    ``` terminal
    $ oc edit authentication.operator.openshift.io cluster
    ```

3.  Verify that the authentication operator returns to a healthy state by running the following command:

    ``` terminal
    $ oc get clusteroperator authentication
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME             VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
    authentication   {product-version}.0     True        False         False      10m
    ```

    </div>

CA bundle not trusted by OAuth server
If the OAuth server cannot verify the proxy TLS certificate, check the following:

- The config map exists in `openshift-config` with valid PEM-encoded certificates under the key `ca-bundle.crt`.

- The `spec.proxy.trustedCA.name` value matches the actual config map name.

- The CA certificate chain is complete, including intermediate certificates.

  The operator syncs the config map from `openshift-config` to `openshift-authentication` automatically.

Brief authentication outage on single-node OpenShift Container Platform
Changing the proxy URL triggers an OAuth server redeployment. On single-node deployments, this causes a brief outage because only one replica is available. Make proxy URL changes during a maintenance window. Updates to `trustedCA` config map content are hot-reloaded without redeployment.

LDAP group sync failing through proxy
LDAP group sync `CronJob` resources are not managed by the authentication operator. Configure proxy environment variables on the `CronJob` pod specification independently. For example:

``` yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ldap-group-sync
spec:
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: sync
            env:
            - name: HTTPS_PROXY
              value: "http://proxy.example.com:3128"
```

Cluster-wide proxy and component-scoped proxy both configured
The component-scoped proxy fully replaces the cluster-wide proxy for authentication components. To verify which proxy is active, inspect the OAuth server pod environment variables by running the following command:

``` terminal
$ oc get deployment oauth-openshift -n openshift-authentication -o jsonpath='{.spec.template.spec.containers[0].env}' | jq .
```

<div class="formalpara">

<div class="title">

Example output

</div>

``` json
[
  {
    "name": "HTTP_PROXY",
    "value": "http://proxy.example.com:3128"
  },
  {
    "name": "HTTPS_PROXY",
    "value": "http://proxy.example.com:3128"
  },
  {
    "name": "NO_PROXY",
    "value": ".cluster.local,.example.com,.svc,127.0.0.1,172.30.0.1,idp.internal.example.com,localhost"
  }
]
```

</div>

The `NO_PROXY` value includes your configured entries and automatically appended cluster-internal defaults.

# Additional resources

- [Configuring the cluster-wide proxy](../networking/configuring_network_settings/enable-cluster-wide-proxy.xml#enable-cluster-wide-proxy)

- [Configuring an OpenID Connect identity provider](../authentication/identity_providers/configuring-oidc-identity-provider.xml#configuring-oidc-identity-provider)

- [Configuring the internal OAuth server](../authentication/configuring-internal-oauth.xml#configuring-internal-oauth)

- [Syncing LDAP groups](../authentication/ldap-syncing.xml#ldap-syncing)
