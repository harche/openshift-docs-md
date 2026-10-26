You can disable KMS encryption and migrate to local etcd encryption to simplify operations or resolve external KMS connectivity issues.

> [!IMPORTANT]
> Kubernetes KMS v2 is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

# Disable KMS encryption

You can disable KMS encryption and migrate to local encryption or disable encryption entirely to simplify operations or resolve connectivity issues.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- You have created an etcd backup.

</div>

> [!WARNING]
> Re-encryption of all etcd data occurs when you change the encryption type.

<div>

<div class="title">

Procedure

</div>

1.  Edit the `APIServer` custom resource by entering the following command:

    ``` terminal
    $ oc edit apiserver cluster
    ```

2.  Change the encryption type and remove the `kms` section by using the following example:

    ``` yaml
    apiVersion: config.openshift.io/v1
    kind: APIServer
    metadata:
      name: cluster
    spec:
      encryption:
        type: <encryption>
    ```

    Replace `<encryption>` with `aescbc`, `aesgcm`, or `identity`. The `aescbc` and `aesgcm` types use locally managed encryption keys. The `identity` type disables all encryption and stores data as plain text. You must remove the entire `kms` section because the API rejects it when the encryption type is not `KMS`.

3.  Save and exit.

    OpenShift Container Platform migrates etcd data. The KMS plugin remains as a read-only provider until migration completes.

4.  Monitor the migration progress by entering the following command:

    ``` terminal
    $ oc get kubeapiserver cluster -o jsonpath='{.status.conditions[?(@.type=="Encrypted")]}' | jq .
    ```

    Wait for `reason` to show `EncryptionCompleted`. The `kube-apiserver` is typically the last to complete.

5.  Verify that the `kube-apiserver` pods have rolled out by entering the following command:

    ``` terminal
    $ oc get pods -n openshift-kube-apiserver -l app=openshift-kube-apiserver
    ```

6.  After migration completes, clean up the KMS provider resources by using the following steps:

    1.  Delete the credential secret by entering the following command:

        ``` terminal
        $ oc delete secret vault-approle-secret -n openshift-config
        ```

    2.  Optional: Delete the CA bundle config map by entering the following command:

        ``` terminal
        $ oc delete configmap vault-ca-bundle -n openshift-config
        ```

    3.  After your backup retention period passes, decommission the KMS key.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify the encryption type by entering the following command:

    ``` terminal
    $ oc get apiserver cluster -o jsonpath='{.spec.encryption.type}'
    ```

2.  Verify that a test secret uses the new encryption type:

    1.  Create a test secret by entering the following command:

        ``` terminal
        $ oc create secret generic encryption-test --from-literal=key=value -n default
        ```

    2.  Get an etcd pod name by entering the following command:

        ``` terminal
        $ oc get pods -n openshift-etcd -l app=etcd -o name | head -1
        ```

    3.  Check the encryption prefix by entering the following command:

        ``` terminal
        $ oc exec -n openshift-etcd <etcd_pod_name> -- etcdctl get /kubernetes.io/secrets/default/encryption-test --print-value-only | hexdump -C | head -1
        ```

        The output begins with `k8s:enc:aescbc:v1:`, `k8s:enc:aesgcm:v1:`, or shows readable JSON for `identity`.

    4.  Delete the test secret by entering the following command:

        ``` terminal
        $ oc delete secret encryption-test -n default
        ```

</div>

> [!NOTE]
> Do not delete the KMS key until migration completes.

# Additional resources

- [Using a KMS provider for data encryption](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/)

- [HashiCorp Vault Transit Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/transit)

- [Use Vault as a Kubernetes KMS provider](https://developer.hashicorp.com/vault/docs/deploy/kubernetes/kms)
