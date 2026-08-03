Configure the `gitlab` identity provider using [GitLab.com](https://gitlab.com/) or any other GitLab instance as an identity provider.

# Identity providers in OpenShift Container Platform

You can configure identity providers by creating a custom resource (CR) that describes the provider and adding it to the cluster. Identity providers enable user authentication in OpenShift Container Platform beyond the default `kubeadmin` user.

<div class="note">

OpenShift Container Platform usernames containing `/`, `:`, and `%` are not supported.

</div>

# About GitLab authentication

Configuring GitLab authentication allows users to log in to OpenShift Container Platform with their GitLab credentials.

If you use GitLab version 7.7.0 to 11.0, you connect using the [OAuth integration](https://docs.gitlab.com/ce/integration/oauth_provider.html). If you use GitLab version 11.1 or later, you can use [OpenID Connect](https://docs.gitlab.com/ce/integration/openid_connect_provider.html) (OIDC) to connect instead of OAuth.

# Creating the secret

Create a Secret in the `openshift-config` namespace to store identity provider client secrets, certificates, or keys, so the OAuth custom resource (CR) can reference them.

1.  Create a `Secret` object containing the client secret by running the following command:

    ``` terminal
    $ oc create secret generic <secret_name> --from-literal=clientSecret=<secret> -n openshift-config
    ```

2.  Optional: Apply the following YAML to create the secret:

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: <secret_name>
      namespace: openshift-config
    type: Opaque
    data:
      clientSecret: <base64_encoded_client_secret>
    ```

3.  Create a `Secret` object from a file by running the following command:

    ``` terminal
    $ oc create secret generic <secret_name> --from-file=<path_to_file> -n openshift-config
    ```

# Creating a config map

Identity providers use OpenShift Container Platform `ConfigMap` objects in the `openshift-config` namespace to contain the certificate authority bundle. These are primarily used to contain certificate bundles needed by the identity provider.

- Define an OpenShift Container Platform `ConfigMap` object containing the certificate authority by using the following command. The certificate authority must be stored in the `ca.crt` key of the `ConfigMap` object.

  ``` terminal
  $ oc create configmap ca-config-map --from-file=ca.crt=/path/to/ca -n openshift-config
  ```

  <div class="tip">

  You can alternatively apply the following YAML to create the config map:

  ``` yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: ca-config-map
    namespace: openshift-config
  data:
    ca.crt: |
      <CA_certificate_PEM>
  ```

  </div>

# Sample GitLab CR

The following custom resource (CR) shows the parameters and acceptable values for a GitLab identity provider.

<div class="formalpara-title">

**GitLab CR**

</div>

``` yaml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: gitlabidp
    mappingMethod: claim
    type: GitLab
    gitlab:
      clientID: {...}
      clientSecret:
        name: gitlab-secret
      url: https://gitlab.com
      ca:
        name: ca-config-map
```

- This provider name is prefixed to the GitLab numeric user ID to form an identity name. It is also used to build the callback URL.

- Controls how mappings are established between this provider’s identities and `User` objects.

- The client ID of a [registered GitLab OAuth application](https://docs.gitlab.com/ce/api/oauth2.html). The application must be configured with a callback URL of `https://oauth-openshift.apps.<cluster-name>.<cluster-domain>/oauth2callback/<idp-provider-name>`.

- Reference to an OpenShift Container Platform `Secret` object containing the client secret issued by GitLab.

- The host URL of a GitLab provider. This could either be `https://gitlab.com/` or any other self hosted instance of GitLab.

- Optional: Reference to an OpenShift Container Platform `ConfigMap` object containing the PEM-encoded certificate authority bundle to use in validating server certificates for the configured URL.

<!-- -->

- See [Identity provider parameters](../../authentication/understanding-identity-provider.xml#identity-provider-parameters_understanding-identity-provider) for information on parameters, such as `mappingMethod`, that are common to all identity providers.

# Adding an identity provider to your cluster

Apply the OAuth custom resource (CR) to add an identity provider to your cluster so users can authenticate with external credentials instead of the default `kubeadmin` user.

- You installed an OpenShift Container Platform cluster.

- You defined the CR for your identity provider.

- You are logged in as an administrator.

1.  Apply the defined CR by running the following command:

    ``` terminal
    $ oc apply -f </path/to/CR>
    ```

    <div class="note">

    If a CR does not exist, `oc apply` creates a new CR and might trigger the following warning: `Warning: oc apply should be used on resources created by either oc create --save-config or oc apply`. In this case you can safely ignore this warning.

    </div>

2.  Log in to the cluster as a user from your identity provider by running the following command, which prompts for your username and password:

    ``` terminal
    $ oc login -u <username>
    ```

3.  Confirm that the user logged in successfully and that the username displays by running the following command:

    ``` terminal
    $ oc whoami
    ```
