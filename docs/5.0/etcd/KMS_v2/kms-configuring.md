You can configure external KMS encryption for etcd to centralize key management and meet regulatory compliance requirements.

> [!IMPORTANT]
> Kubernetes KMS v2 is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

# Enable KMS encryption

You can enable Key Management Service (KMS) encryption for etcd data to centralize key management and meet compliance requirements.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- You have enabled the `TechPreviewNoUpgrade` feature set, which activates the `KMSEncryption` feature gate.

- You have a HashiCorp Vault Enterprise instance that is externally hosted and accessible from your cluster. Vault Enterprise must not be hosted inside the cluster service network. Vault Community Edition is not supported.

- You have configured your Vault instance with:

  - Transit secrets engine enabled at a mount path, such as the default `transit/` path

  - Encryption key created with type `aes256-gcm96` (recommended for FIPS 140-3 compliance)

  - Vault policy that allows the KMS plugin to encrypt, decrypt, and read key information

  - Authentication method, such as `AppRole`, configured with the policy attached

- You have the fully qualified OCI image pull spec with SHA256 digest for the KMS plugin image. You can obtain the image from the Red Hat Ecosystem Catalog or from Docker Hub. For more information, see "HashiCorp Vault KMS plugin container image" and "Red Hat Ecosystem Catalog". In disconnected environments, the image is mirrored to an accessible registry.

- You have the `skopeo` and `jq` tools installed.

- You have configured a Vault policy with the following capabilities:

  ``` hcl
  path "transit/encrypt/kms-key" {
    capabilities = ["update"]
  }

  path "transit/decrypt/kms-key" {
    capabilities = ["update"]
  }

  path "transit/keys/kms-key" {
    capabilities = ["read"]
  }

  path "sys/license/status" {
    capabilities = ["read"]
  }
  ```

  Replace `transit` with your Transit mount path and `kms-key` with your Vault Transit key name.

- You have created an etcd backup.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Obtain the SHA256 digest for the KMS plugin image by entering the following command:

    ``` terminal
    $ skopeo inspect docker://quay.io/redhat-isv-containers/698df066f8d1ddf179c15ef9:<version> | jq -r '.Digest'
    ```

    Replace `<version>` with the plugin version compatible with your cluster, such as `0.1.0-beta-ubi`.

    Use the resulting digest to construct the fully qualified pull spec in the format `quay.io/redhat-isv-containers/698df066f8d1ddf179c15ef9@sha256:<digest>`.

2.  Create a secret in the `openshift-config` namespace with your Vault authentication credentials by entering the following command:

    ``` terminal
    $ oc create secret generic vault-approle-secret \
      --from-literal=role-id=<your_role_id> \
      --from-literal=secret-id=<your_secret_id> \
      -n openshift-config
    ```

    Replace `<your_role_id>` and `<your_secret_id>` with your Vault AppRole credentials.

3.  Optional: If your Vault server uses a custom TLS certificate authority, create a config map in the `openshift-config` namespace with the CA bundle by entering the following command:

    ``` terminal
    $ oc create configmap vault-ca-bundle \
      --from-file=ca-bundle.crt=<path_to_ca_bundle> \
      -n openshift-config
    ```

4.  Edit the `APIServer` custom resource by entering the following command:

    ``` terminal
    $ oc edit apiserver cluster
    ```

5.  Add the KMS configuration to the `spec.encryption` section:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
      name: cluster
    spec:
      encryption:
        type: KMS
        kms:
          type: Vault
          vault:
            kmsPluginImage: <registry>/<repository>@sha256:<digest>
            vaultAddress: https://vault.example.com:8200
            vaultNamespace: my-namespace
            vaultAuthNamespace: my-auth-namespace
            vaultKeyPath: transit/keys/kms-key
            tls:
              caBundle:
                name: vault-ca-bundle
              serverName: vault.example.com
            authentication:
              type: AppRole
              appRole:
                secret:
                  name: vault-approle-secret
    ```

    where:

    `kmsPluginImage`
    Specifies the KMS plugin container image as a fully qualified OCI pull spec with SHA256 digest. Image tags and short names are not allowed. In disconnected environments, use the mirrored location.

    `vaultAddress`
    Specifies the HTTPS URL of the Vault server. Paths, query parameters, and fragments are not allowed.

    `vaultNamespace`
    Specifies the Vault namespace. This value is optional.

    `vaultAuthNamespace`
    Specifies the Vault namespace for authentication when it differs from the Transit namespace. Defaults to the `vaultNamespace` value. This value is optional.

    `vaultKeyPath`
    Specifies the Transit encryption key path in the format `<mount>/keys/<key_name>`.

    `tls.caBundle.name`
    Specifies the config map in the `openshift-config` namespace containing the CA bundle. Required only if Vault uses a custom CA.

    `tls.serverName`
    Specifies the TLS server name for certificate verification. This value is optional.

    `authentication.appRole.secret.name`
    Specifies the secret name in the `openshift-config` namespace containing the AppRole credentials.

6.  Save and exit.

    The `kube-apiserver`, `openshift-apiserver`, and `authentication` Operators validate the configuration and roll out new revisions.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify the encryption type by entering the following command:

    ``` terminal
    $ oc get apiserver cluster -o jsonpath='{.spec.encryption.type}'
    ```

    The output shows `KMS`.

2.  Check the KMS plugin health and configuration validation by entering the following command:

    ``` terminal
    $ oc get kubeapiserver cluster -ojsonpath='{.status.encryptionStatus}' | jq .
    ```

    Verify that `preflight.result.status` shows `Succeeded` and all nodes in `healthReports` show `Healthy`.

3.  Monitor the `kube-apiserver` rollout progress by entering the following command:

    ``` terminal
    $ oc get co kube-apiserver
    ```

    <div class="formalpara">

    <div class="title">

    Example output during rollout

    </div>

    ``` terminal
    NAME             VERSION      AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
    kube-apiserver   5.0.0-rc.4   True        True          False      35m     NodeInstallerProgressing: 2 nodes are at revision 6; 1 node is at revision 7
    ```

    </div>

    When `PROGRESSING` shows `False`, the rollout is complete.

4.  Check the encryption migration status by entering the following command:

    ``` terminal
    $ oc get kubeapiserver cluster -o jsonpath='{.status.conditions[?(@.type=="Encrypted")]}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output when complete

    </div>

    ``` json
    {
      "lastTransitionTime": "2026-09-24T16:41:48Z",
      "message": "All resources encrypted: secrets, configmaps",
      "reason": "EncryptionCompleted",
      "status": "True",
      "type": "Encrypted"
    }
    ```

    </div>

    Wait for `reason` to show `EncryptionCompleted` before you verify encryption in etcd.

5.  Verify that secrets are encrypted in etcd:

    > [!WARNING]
    > Wait for the `kube-apiserver` rollout to complete on all control plane nodes before you verify encryption. Secrets created while nodes run an earlier revision are not encrypted with KMS.

    1.  Create a test secret by entering the following command:

        ``` terminal
        $ oc create secret generic test-secret --from-literal=key=value -n default
        ```

    2.  Get an etcd pod name by entering the following command:

        ``` terminal
        $ oc get pods -n openshift-etcd -l app=etcd -o name | head -1
        ```

    3.  Check the secret data in etcd by entering the following command:

        ``` terminal
        $ oc exec -n openshift-etcd <etcd_pod_name> -- etcdctl get /kubernetes.io/secrets/default/test-secret --print-value-only | hexdump -C | head -1
        ```

        <div class="formalpara">

        <div class="title">

        Example output

        </div>

        ``` terminal
        00000000  6b 38 73 3a 65 6e 63 3a  6b 6d 73 3a 76 32 3a 31  |k8s:enc:kms:v2:1|
        ```

        </div>

        The output begins with `k8s:enc:kms:v2:` followed by encrypted binary data.

    4.  Delete the test secret by entering the following command:

        ``` terminal
        $ oc delete secret test-secret -n default
        ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [HashiCorp Vault KMS plugin container image](https://hub.docker.com/r/hashicorp/vault-kube-kms)

- [Red Hat Ecosystem Catalog](https://catalog.redhat.com/search?gs&q=vault-kms)

- [Vault Transit Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/transit)

- [Vault API: Create Key](https://developer.hashicorp.com/vault/api-docs/secret/transit#create-key)

- [Vault Policies](https://developer.hashicorp.com/vault/docs/concepts/policies)

- [Vault Authentication Methods](https://developer.hashicorp.com/vault/docs/auth)

</div>

# Rotate the Vault encryption key

You can rotate your Vault Transit encryption key to generate a new key version while maintaining access to data encrypted with earlier versions.

> [!WARNING]
> After rotating the Vault encryption key, OpenShift Container Platform does not automatically re-encrypt existing etcd data with the new key version. Existing data remains encrypted with the previous key version. The Vault-side rotation steps are safe to perform because Vault retains all previous key versions for decryption.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- You have access to your Vault instance with permissions to rotate keys.

- Kubernetes KMS v2 encryption is enabled and functioning.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Rotate the Vault encryption key by entering the following command:

    ``` terminal
    $ vault write -f transit/keys/kms-key/rotate
    ```

    Replace `kms-key` with your Vault Transit key name. Vault creates a new key version while retaining earlier versions for decryption.

2.  Verify the new key version by entering the following command:

    ``` terminal
    $ vault read transit/keys/kms-key
    ```

    The `latest_version` field shows the current key version number.

</div>

<div>

<div class="title">

Verification

</div>

- Verify that existing secrets remain accessible by entering the following command:

  ``` terminal
  $ oc get secret -A
  ```

  All secrets should be readable without errors. Vault maintains all key versions and automatically uses the appropriate version for decryption.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Vault Transit: Rotate Key](https://developer.hashicorp.com/vault/api-docs/secret/transit#rotate-key)

- [Vault Transit: Rewrap Data](https://developer.hashicorp.com/vault/api-docs/secret/transit#rewrap-data)

- [Vault Transit: Key Rotation](https://developer.hashicorp.com/vault/docs/secrets/transit#key-rotation)

</div>

# Migrate from local encryption to KMS encryption

You can migrate from local etcd encryption to KMS encryption to centralize key management.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- You have enabled the `TechPreviewNoUpgrade` feature set to enable the `KMSEncryption` feature gate.

- Your cluster is currently using `aescbc` or `aesgcm` encryption.

- You have created the credential secret and optional CA bundle config map in the `openshift-config` namespace.

- You have the fully qualified OCI image pull spec with SHA256 digest for the KMS plugin image.

</div>

> [!IMPORTANT]
> Create an etcd backup before migrating.

<div>

<div class="title">

Procedure

</div>

1.  Back up the current etcd encryption configuration by entering the following command:

    ``` terminal
    $ oc get apiserver cluster -o yaml > apiserver-backup.yaml
    ```

2.  Edit the APIServer custom resource by entering the following command:

    ``` terminal
    $ oc edit apiserver cluster
    ```

3.  Change the encryption type from `aescbc` or `aesgcm` to `KMS` and add the inline Vault configuration by using the following example:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
      name: cluster
    spec:
      encryption:
        type: KMS
        kms:
          type: Vault
          vault:
            kmsPluginImage: <registry>/<repository>@sha256:<digest>
            vaultAddress: https://vault.example.com:8200
            vaultKeyPath: transit/keys/kms-key
            authentication:
              type: AppRole
              appRole:
                secret:
                  name: vault-approle-secret
    ```

4.  Save and exit.

    After configuration validation succeeds, migration starts.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify migration completion for the OpenShift API server by entering the following command:

    ``` terminal
    $ oc get openshiftapiserver -o jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{"\n"}{end}'
    ```

2.  Verify migration completion for the Kubernetes API server by entering the following command:

    ``` terminal
    $ oc get kubeapiserver -o jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{"\n"}{end}'
    ```

3.  Verify migration completion for the authentication Operator by entering the following command:

    ``` terminal
    $ oc get authentication.operator.openshift.io -o jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{"\n"}{end}'
    ```

    All outputs show `EncryptionCompleted`.

</div>

# Migrating between KMS providers

You can migrate between KMS providers without an intermediate local encryption step. During migration, OpenShift Container Platform runs both KMS plugins concurrently until re-encryption completes.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- KMS encryption is enabled and functioning with the current provider.

- You have created the credential secret and optional CA bundle config map for the new provider in the `openshift-config` namespace.

- You have the fully qualified OCI image pull spec with SHA256 digest for the new KMS plugin image.

- You have created an etcd backup.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit the `APIServer` custom resource by entering the following command:

    ``` terminal
    $ oc edit apiserver cluster
    ```

2.  Update the `kms.vault` configuration with the new provider settings by using the following example:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
      name: cluster
    spec:
      encryption:
        type: KMS
        kms:
          type: Vault
          vault:
            kmsPluginImage: <registry>/<repository>@sha256:<digest>
            vaultAddress: https://vault.example.com:8200
            vaultNamespace: my-namespace
            vaultAuthNamespace: my-auth-namespace
            vaultKeyPath: transit/keys/kms-key
            tls:
              caBundle:
                name: vault-ca-bundle
              serverName: vault.example.com
            authentication:
              type: AppRole
              appRole:
                secret:
                  name: vault-approle-secret
    ```

3.  Save and exit.

    After configuration validation succeeds, the new provider handles encryption while the old provider decrypts existing data.

4.  Monitor migration progress by entering the following command:

    ``` terminal
    $ oc get kubeapiserver cluster -o jsonpath='{.status.conditions[?(@.type=="Encrypted")]}' | jq .
    ```

    Wait for `reason` to show `EncryptionCompleted`.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the OpenShift API server has completed migration by entering the following command:

    ``` terminal
    $ oc get openshiftapiserver -o jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{"\n"}{end}'
    ```

    The output shows `EncryptionCompleted`.

2.  Verify that the Kubernetes API server has completed migration by entering the following command:

    ``` terminal
    $ oc get kubeapiserver -o jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{"\n"}{end}'
    ```

    The output shows `EncryptionCompleted`.

3.  Verify that the authentication Operator has completed migration by entering the following command:

    ``` terminal
    $ oc get authentication.operator.openshift.io -o jsonpath='{range .items[0].status.conditions[?(@.type=="Encrypted")]}{"\n"}{end}'
    ```

    The output shows `EncryptionCompleted`.

</div>

<div>

<div class="title">

Next steps

</div>

- Delete the old credential secret by entering the following command:

  ``` terminal
  $ oc delete secret <old_vault_secret_name> -n openshift-config
  ```

  Replace `<old_vault_secret_name>` with the name of the previous provider’s credential secret.

- Optional: Delete the old CA bundle config map by entering the following command:

  ``` terminal
  $ oc delete configmap <old_vault_configmap_name> -n openshift-config
  ```

  Replace `<old_vault_configmap_name>` with the name of the previous provider’s CA bundle config map.

- After your backup retention period passes, decommission the old KMS key.

  > [!NOTE]
  > Do not decommission the old KMS key until migration completes and all backups encrypted with the old key have expired.

</div>

# Monitoring KMS encryption status

You can monitor KMS encryption status by inspecting operator encryption status conditions, health reports, and preflight results.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- KMS encryption is enabled.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Check overall Operator status by entering the following command:

    ``` terminal
    $ oc get co kube-apiserver
    ```

    The `DEGRADED` column shows `True` if KMS configuration or connectivity problems exist.

2.  Inspect KMS health reports and preflight results by entering the following command:

    ``` terminal
    $ oc get kubeapiserver cluster -ojsonpath='{.status.encryptionStatus}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "healthReports": [
        {
          "keyID": "1",
          "lastCheckedTime": "2026-09-24T16:44:19Z",
          "nodeName": "ip-10-0-1-198.us-east-2.compute.internal",
          "remoteKeyID": "CgQKAnYx...",
          "status": "Healthy"
        },
        {
          "keyID": "1",
          "lastCheckedTime": "2026-09-24T16:44:45Z",
          "nodeName": "ip-10-0-77-162.us-east-2.compute.internal",
          "remoteKeyID": "CgQKAnYx...",
          "status": "Healthy"
        },
        {
          "keyID": "1",
          "lastCheckedTime": "2026-09-24T16:44:25Z",
          "nodeName": "ip-10-0-97-236.us-east-2.compute.internal",
          "remoteKeyID": "CgQKAnYx...",
          "status": "Healthy"
        }
      ],
      "preflight": {
        "observedConfigHash": "GNja6Q==",
        "result": {
          "configHash": "GNja6Q==",
          "remoteKeyID": "always-succeed",
          "status": "Succeeded"
        }
      }
    }
    ```

    </div>

    `healthReports`
    Shows KMS plugin health per control plane node. Each entry includes the node name, key ID, a `status` of `Healthy`, `Unhealthy`, or `Error`, and an optional `detail` field with additional diagnostic information when the status is not `Healthy`.

    `preflight`
    Shows whether the configured KMS settings are valid. The `preflight.result.status` field shows `Succeeded` when the plugin can connect to the external Vault instance and the credentials are valid, or `Failed` when connectivity problems or invalid credentials exist.

3.  Verify the Kubernetes API server encryption status by entering the following command:

    ``` terminal
    $ oc get kubeapiserver cluster -o jsonpath='{.status.conditions[?(@.type=="Encrypted")]}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "lastTransitionTime": "2026-09-24T16:41:48Z",
      "message": "All resources encrypted: secrets, configmaps",
      "reason": "EncryptionCompleted",
      "status": "True",
      "type": "Encrypted"
    }
    ```

    </div>

    Wait for `reason` to show `EncryptionCompleted`.

4.  Verify the authentication Operator encryption status by entering the following command:

    ``` terminal
    $ oc get authentication.operator.openshift.io cluster -o jsonpath='{.status.conditions[?(@.type=="Encrypted")]}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "lastTransitionTime": "2026-09-24T16:22:10Z",
      "message": "All resources encrypted: oauthaccesstokens.oauth.openshift.io, oauthauthorizetokens.oauth.openshift.io",
      "reason": "EncryptionCompleted",
      "status": "True",
      "type": "Encrypted"
    }
    ```

    </div>

    The output shows `EncryptionCompleted`.

5.  Verify the OpenShift API server encryption status by entering the following command:

    ``` terminal
    $ oc get openshiftapiserver cluster -o jsonpath='{.status.conditions[?(@.type=="Encrypted")]}' | jq .
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` json
    {
      "lastTransitionTime": "2026-09-24T16:25:54Z",
      "message": "All resources encrypted: routes.route.openshift.io",
      "reason": "EncryptionCompleted",
      "status": "True",
      "type": "Encrypted"
    }
    ```

    </div>

    The output shows `EncryptionCompleted`.

</div>

# KMS encryption troubleshooting

You can diagnose and resolve common KMS encryption issues to maintain secure key management and cluster availability.

## KMS encryption does not activate

Symptom: KMS encryption does not activate after configuring the `APIServer` resource. The `kube-apiserver` Operator reports a degraded condition.

Diagnosis: Check the encryption status, including health reports and preflight results by running the following command:

``` terminal
$ oc get kubeapiserver cluster -ojsonpath='{.status.encryptionStatus}' | jq .
```

The `preflight.result.status` field shows whether configuration validation succeeded. The `healthReports` array shows plugin health per control plane node.

If you need additional detail, check the kube-apiserver Operator logs by running the following command:

``` terminal
$ oc logs -n openshift-kube-apiserver-operator deploy/kube-apiserver-operator | grep -i "kms\|error"
```

Solutions:

- Verify that the Vault server is reachable from control plane nodes.

- Verify that the credential secret in `openshift-config` has valid credentials.

- Verify that the Transit encryption key exists at the path specified in `vaultKeyPath`.

- Verify that the Vault policy grants encrypt, decrypt, and read permissions on the key.

## Invalid KMS configuration

Symptom: `APIServer` resource shows validation errors.

Diagnosis: Check the preflight results in the encryption status by running the following command:

``` terminal
$ oc get kubeapiserver cluster -ojsonpath='{.status.encryptionStatus.preflight}' | jq .
```

The `preflight.result.status` field shows whether the configured KMS settings are valid. A failed preflight indicates connectivity problems with the external Vault instance or invalid credentials.

If you need additional detail, check kube-apiserver Operator logs by running the following command:

``` terminal
$ oc logs -n openshift-kube-apiserver-operator deploy/kube-apiserver-operator | grep -i "kms\|validation\|error"
```

Solutions:

- Verify that the `kms.vault` configuration in the `APIServer` resource has valid field values.

- Verify that `kmsPluginImage` is a fully qualified OCI pull spec with a SHA256 digest.

- Verify that `vaultAddress` is a valid HTTPS URL without path or query parameters.

- Verify that the credential secret referenced by `authentication.appRole.secret.name` exists in the `openshift-config` namespace.

## KMS permissions errors

Symptom: Encryption migration fails with permission errors.

Diagnosis: Check Operator logs by running the following command:

``` terminal
$ oc logs -n openshift-kube-apiserver-operator deploy/kube-apiserver-operator | grep -i "kms\|permission\|access denied"
```

Solutions:

- Verify that the credential secret has valid and unexpired credentials.

- Verify that the Vault policy grants encrypt and decrypt permissions.

- Verify that the encryption key is enabled and not scheduled for deletion.

## Expired or deleted KMS key

Symptom: API server cannot decrypt encrypted resources.

Diagnosis: Check API server logs and verify key status by running the following command:

``` terminal
$ oc logs -n openshift-kube-apiserver -l apiserver=true | grep -i "decrypt\|kms.*error"
```

Solutions:

- Re-enable the encryption key if it was disabled.

- Restore from backup if the key was permanently deleted.

- Cancel key deletion if it is scheduled.

- Ensure the KMS provider retains access to earlier key versions.

> [!WARNING]
> Deleted KMS keys prevent data recovery. Align key retention with backup policies.

## API server degraded or unavailable

Symptom: API server becomes degraded or unresponsive after enabling KMS encryption.

Diagnosis: Check the encryption status health reports by running the following command:

``` terminal
$ oc get kubeapiserver cluster -ojsonpath='{.status.encryptionStatus.healthReports}' | jq .
```

Health reports show per-node plugin status. An `Unhealthy` status indicates connectivity or credential problems between that node and the Vault instance.

Check overall Operator status by running the following command:

``` terminal
$ oc get clusteroperator kube-apiserver
```

If you need additional detail, check API server logs by running the following command:

``` terminal
$ oc logs -n openshift-kube-apiserver -l apiserver=true --tail=200 | grep -i kms
```

Solutions:

- Check network connectivity between control plane nodes and Vault.

- Verify network policies and firewalls allow communication.

- Check Vault for rate limiting.

- Verify DNS resolution and TLS certificate validation.

## Encryption migration stuck or slow

Symptom: Encryption migration takes unusually long or is stuck.

Diagnosis: Check Operator status and migration logs by running the following commands:

``` terminal
$ oc get clusteroperator kube-apiserver
```

``` terminal
$ oc logs -n openshift-kube-apiserver-operator deploy/kube-apiserver-operator | grep -i migration
```

Solutions:

- Migration time depends on data size. Monitor progress with Operator conditions.

- Check Vault audit logs for rate limiting or throttling.

- Check network performance between control plane nodes and Vault.

## Collecting debug information

Collect cluster status and logs by running the following commands:

``` terminal
$ oc adm must-gather
```

``` terminal
$ oc get apiserver cluster -o yaml > apiserver.yaml
```

``` terminal
$ oc get kubeapiserver cluster -ojsonpath='{.status.encryptionStatus}' | jq . > encryption-status.json
```

``` terminal
$ oc logs -n openshift-kube-apiserver-operator deploy/kube-apiserver-operator > kube-apiserver-operator.log
```

``` terminal
$ oc logs -n openshift-kube-apiserver -l apiserver=true --tail=500 > kube-apiserver.log
```

Collect KMS provider information:

- Vault audit logs

- Vault key policy and permissions

- Authentication credentials status

- Network connectivity test results

> [!NOTE]
> Redact credentials, tokens, and sensitive data before sharing logs.

# Additional resources

- [Enabling features using feature gates](../../nodes/clusters/nodes-cluster-enabling-features.xml#nodes-cluster-enabling-features)

- [Using a KMS provider for data encryption](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/)

- [HashiCorp Vault Transit Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/transit)

- [Use Vault as a Kubernetes KMS provider](https://developer.hashicorp.com/vault/docs/deploy/kubernetes/kms)

- [HashiCorp Vault KMS plugin container image](https://hub.docker.com/r/hashicorp/vault-kube-kms)
