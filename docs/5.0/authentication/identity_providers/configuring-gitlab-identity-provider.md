Configure the `gitlab` identity provider so users can log in to OpenShift Container Platform with GitLab account credentials through OAuth.

# Identity providers in OpenShift Container Platform

You can configure identity providers by creating a custom resource (CR) that describes the provider and adding it to the cluster. Identity providers enable user authentication in OpenShift Container Platform beyond the default `kubeadmin` user.

<div class="note">

OpenShift Container Platform usernames containing `/`, `:`, and `%` are not supported.

</div>

# About GitLab authentication

Review GitLab authentication options for OpenShift Container Platform. Use this integration when you want users to log in with GitLab account credentials through OAuth or OpenID Connect.

If you use GitLab version 7.7.0 to 11.0, you connect using OAuth integration. If you use GitLab version 11.1 or later, you can use OpenID Connect (OIDC) to connect instead of OAuth.

- [OAuth integration](https://docs.gitlab.com/ce/integration/oauth_provider.html)

- [OpenID Connect](https://docs.gitlab.com/ce/integration/openid_connect_provider.html)

# Creating the secret

Create a `Secret` object in the `openshift-config` namespace to store the client secret and related credentials for the identity provider configuration.

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

# Creating a 'ConfigMap'

Create a `ConfigMap` object in the `openshift-config` namespace to store the certificate authority bundle that identity providers use to validate secure connections to the remote authentication service.

1.  Define an OpenShift Container Platform `ConfigMap` object containing the certificate authority by running the following command:

    ``` terminal
    $ oc create configmap ca-config-map --from-file=ca.crt=/path/to/ca -n openshift-config
    ```

2.  Optional: Apply the following YAML to create the config map:

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

    The certificate authority must be stored in the `ca.crt` key of the `ConfigMap` object.

# Sample GitLab custom resource

Review the sample GitLab `OAuth` custom resource (CR) to understand provider parameters and acceptable values before you configure the identity provider in your cluster.

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

where:

`spec.identityProviders.name`
Specifies that the provider name is prefixed to the GitLab numeric user ID to form an identity name. It is also used to build the callback URL.

`spec.identityProviders.mappingMethod`
Specifies how mappings are established between identities from this provider and `User` objects.

`spec.identityProviders.gitlab.clientID`
Specifies the client ID of a registered GitLab OAuth application. The application must be configured with a callback URL of `https://oauth-openshift.apps.<cluster-name>.<cluster-domain>/oauth2callback/<idp-provider-name>`.

`spec.identityProviders.gitlab.clientSecret`
Specifies a reference to an OpenShift Container Platform `Secret` object containing the client secret issued by GitLab.

`spec.identityProviders.gitlab.url`
Specifies the host URL of a GitLab provider. This could either be `https://gitlab.com/` or any other self-hosted instance of GitLab.

`spec.identityProviders.gitlab.ca`
Specifies a reference to an OpenShift Container Platform `ConfigMap` object containing the PEM-encoded certificate authority bundle to use in validating server certificates for the configured URL. This value is optional.

- [Identity provider parameters](../../authentication/understanding-identity-provider.xml#identity-provider-parameters_understanding-identity-provider)

# Adding an identity provider to your cluster

Apply the identity provider custom resource (CR) to your cluster so users can authenticate with the configured identity provider.

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

2.  Log in to the cluster as a user from your identity provider, entering the password when prompted. Run the following command:

    ``` terminal
    $ oc login -u <username>
    ```

3.  Confirm that the user logged in successfully and that the username displays by running the following command:

    ``` terminal
    $ oc whoami
    ```

# Additional resources

- [GitLab.com](https://gitlab.com/)
