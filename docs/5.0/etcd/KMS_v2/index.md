You can configure Kubernetes Key Management Service (KMS) v2 on OpenShift Container Platform to centralize encryption key management and meet regulatory compliance requirements.

> [!IMPORTANT]
> Kubernetes KMS v2 is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

# About Kubernetes KMS v2 encryption

Kubernetes KMS v2 uses an external Key Management Service to encrypt etcd data and centralize key management.

Kubernetes KMS v2 provides:

- Customer-managed encryption keys stored in an external KMS

- Centralized key management and auditing

- Regulatory compliance support

## KMS plugin architecture

The KMS plugin configuration is specified inline in the `APIServer` resource. Encryption controllers deploy the KMS plugin and manage encryption key secrets.

The workflow is consists of the following steps:

1.  You create the credential secret and optional CA bundle in the `openshift-config` namespace.

2.  You configure the `APIServer` resource with the KMS provider settings and plugin image.

3.  The encryption controllers deploy the KMS plugin and begin encrypting etcd data.

> [!NOTE]
> HashiCorp Vault Enterprise is the only supported KMS provider. Vault Community Edition is not supported. Vault Enterprise must be externally hosted and must not run inside the cluster service network.

## Encrypted resources

When you enable KMS encryption, OpenShift Container Platform encrypts the following resources in etcd:

- Secrets

- ConfigMaps

- Routes

- OAuth access tokens

- OAuth authorize tokens

> [!NOTE]
> Resource types, namespaces, and object names are not encrypted.

<div>

<div class="title">

Additional resources

</div>

- [Using a KMS provider for data encryption](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/)

</div>

# KMS Technology Preview limitations

Review the current Kubernetes KMS v2 limitations to plan deployments and avoid unsupported configurations.

> [!IMPORTANT]
> KMS encryption is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

## Current limitations

- HashiCorp Vault Enterprise is the only supported KMS provider. Vault Community Edition is not supported.

- Vault Enterprise must be externally hosted. Hosting Vault inside the cluster service network is not supported.

- After rotating a Vault Transit encryption key, OpenShift Container Platform does not automatically re-encrypt existing etcd data with the new key version.

- The KMS plugin image must be in pinned digest format, such as `registry.example.com/vault-plugin@sha256:<digest>`. Image tags are not allowed.

- In disconnected environments or clusters that use custom internal registries, you must manually mirror the KMS plugin image to an accessible registry.

- The KMS plugin does not expose Prometheus metrics in this Technology Preview phase.

- Unused KMS plugins are not removed from the `EncryptionConfiguration` after migration. You must decommission old providers manually.

- The `KMSEncryption` feature gate requires the `TechPreviewNoUpgrade` feature set. Clusters with this feature set cannot be upgraded.

# Additional resources

- [Enabling features using feature gates](../../nodes/clusters/nodes-cluster-enabling-features.xml#nodes-cluster-enabling-features)

- [Using a KMS provider for data encryption](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/)

- [HashiCorp Vault Transit Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/transit)

- [Use Vault as a Kubernetes KMS provider](https://developer.hashicorp.com/vault/docs/deploy/kubernetes/kms)
