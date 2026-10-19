Before you can provision clusters with the O-Cloud Manager, you must install the Operator on the hub cluster, configure the GitOps repository that supplies cluster templates and configuration policies, and set up API authentication. If your environment uses a Service Management and Orchestration (SMO) framework, you must also configure mutual TLS (mTLS) and register with the SMO.

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Install the O-Cloud Manager by using the CLI

You can install the O-Cloud Manager on the hub cluster by creating a `Subscription` custom resource (CR) that deploys the Operator from the Red Hat Ecosystem Catalog.

- You have access to the hub cluster as a user with `cluster-admin` privileges.

- You have installed the OpenShift CLI (`oc`).

- Red Hat Advanced Cluster Management (RHACM) version 2.15 or later is installed on the hub cluster.

- The SiteConfig Operator is enabled in the `MultiClusterHub` CR.

- A default `StorageClass` that supports `ReadWriteOnce` access mode is configured, with at least 20 Gi of available `PersistentVolume` capacity.

1.  Create a namespace for the O-Cloud Manager by running the following command:

    ``` terminal
    $ oc create namespace oran-o2ims
    ```

    \* `oran-o2ims` is the namespace for the O-Cloud Manager.

2.  Create an `OperatorGroup` CR in the `oran-o2ims` namespace such as the following example:

    ``` yaml
    apiVersion: operators.coreos.com/v1
    kind: OperatorGroup
    metadata:
      name: o-cloud-manager
      namespace: oran-o2ims
    ```

    - `metadata.name` specifies a name for the `OperatorGroup` CR, such as `o-cloud-manager`.

3.  Create a `Subscription` CR to install the Operator such as the following example:

    ``` yaml
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: oran-o2ims
      namespace: oran-o2ims
    spec:
      channel: "stable"
      name: o-cloud-manager
      source: redhat-operators
      sourceNamespace: openshift-marketplace
    ```

    `metadata.name` specifies a name for the `Subscription` CR, such as `oran-o2ims`.

4.  Apply the CRs by running the following commands, replacing `<operatorgroup_filename>` and `<subscription_filename>` with the names of the files you created:

    ``` terminal
    $ oc apply -f <operatorgroup_filename>.yaml
    $ oc apply -f <subscription_filename>.yaml
    ```

<!-- -->

1.  Verify that the Operator is installed and running by running the following command:

    ``` terminal
    $ oc get pods -n oran-o2ims
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                                             READY   STATUS    RESTARTS   AGE
    alarms-server-5685f99d59-2n8bh                   1/1     Running   0          114s
    artifacts-server-58f79ccdcc-5xhrc                1/1     Running   0          114s
    cluster-server-6bff69577-jxs6g                   1/1     Running   0          114s
    hardwaremanager-server-69d4d7cdf4-72tpr          1/1     Running   0          114s
    oran-o2ims-controller-manager-6c84d59ff5-xn687   1/1     Running   0          119s
    postgres-server-6bdcb786fb-vqdhk                 1/1     Running   0          114s
    provisioning-server-5559cc6697-xmqv6             1/1     Running   0          114s
    resource-server-79d7cd8495-skt45                 1/1     Running   0          114s
    ```

2.  Verify that the default `Inventory` CR was created by running the following command:

    ``` terminal
    $ oc get inventory -n oran-o2ims
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME      AGE
    default   4m20s
    ```

3.  Verify that the API routes are available by running the following command:

    ``` terminal
    $ oc get routes -n oran-o2ims
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                       HOST/PORT                                PATH                                SERVICES              PORT   TERMINATION          WILDCARD
    oran-o2ims-ingress-8k2wz   o2ims.apps.<cluster_domain>   /O2ims_infrastructureArtifacts      artifacts-server      api    reencrypt/Redirect   None
    oran-o2ims-ingress-dpdbr   o2ims.apps.<cluster_domain>   /O2ims_infrastructureProvisioning   provisioning-server   api    reencrypt/Redirect   None
    oran-o2ims-ingress-fx49w   o2ims.apps.<cluster_domain>   /O2ims_infrastructureInventory      resource-server       api    reencrypt/Redirect   None
    oran-o2ims-ingress-pkkgr   o2ims.apps.<cluster_domain>   /O2ims_infrastructureMonitoring     alarms-server         api    reencrypt/Redirect   None
    oran-o2ims-ingress-tkvlh   o2ims.apps.<cluster_domain>   /O2ims_infrastructureCluster        cluster-server        api    reencrypt/Redirect   None
    ```

# Install the O-Cloud Manager by using the web console

As a cluster administrator, you can install the O-Cloud Manager by using the OpenShift Container Platform web console.

- Log in as a user with `cluster-admin` privileges.

1.  In the OpenShift Container Platform web console, navigate to **Ecosystem** → **Software Catalog**.

2.  Search for the **O-Cloud Manager** from the list of available Operators, and then click **Install**.

3.  On the **Install Operator** page, keep the default selections for **Update Channel**, **Version**, **Installation mode**, and **Installed Namespace**.

4.  Click **Install**.

<!-- -->

1.  To confirm that the installation is successful:

    1.  Navigate to the **Ecosystem** → **Installed Operators** page.

    2.  Check that the Operator is installed and that its status is `Succeeded`.

2.  If the Operator is not installed successfully, check the status of the Operator and review the logs:

    1.  Navigate to the **Ecosystem** → **Installed Operators** page and inspect the `Status` column for any errors or failures.

    2.  Navigate to the **Workloads** → **Pods** page and check the logs in any pods in the Operator namespace that are reporting issues.

# Configure the GitOps repository for O-Cloud Manager resources

Configure a Git repository with the directory layout required by the O-Cloud Manager, including cluster templates, configuration policy definitions, hardware profiles, and server inventory. ArgoCD synchronizes this repository content to the hub cluster where the O-Cloud Manager uses it for cluster provisioning.

<div class="note">

This repository layout differs from the GitOps Zero Touch Provisioning (ZTP) GitOps layout. In GitOps ZTP, the Git repository contains a `ClusterInstance` CR for each site, representing the full cluster definition. In the O-Cloud Manager flow, the repository contains reusable templates, defaults, and policies. Individual clusters are instantiated by creating a `ProvisioningRequest` CR that references a template and supplies site-specific parameters. The `ProvisioningRequest` CR can be applied directly to the hub cluster or managed through a separate GitOps repository.

</div>

- The O-Cloud Manager Operator is installed on the hub cluster.

- The Red Hat OpenShift GitOps Operator is installed.

- You have a Git repository accessible by ArgoCD on the hub cluster.

1.  Create your Git repository. See the following recommended directory layout:

    ``` text
    ├── clustertemplates/
    │   ├── hardwareprofiles/
    │   ├── inventory/
    │   └── version_4.Y.Z/
    │       ├── sno-ran-du/
    │       │   ├── clusterinstance-defaults-v1.yaml
    │       │   ├── policytemplates-defaults-v1.yaml
    │       │   ├── pull-secret.yaml
    │       │   ├── extra-manifest/
    │       │   ├── ns.yaml
    │       │   └── sno-ran-du-v4-Y-Z-1.yaml
    │       └── std-ran-du/
    │           ├── clusterinstance-defaults-v1.yaml
    │           ├── policytemplates-defaults-v1.yaml
    │           ├── pull-secret.yaml
    │           ├── ns.yaml
    │           └── std-ran-du-v4-Y-Z-1.yaml
    └── policytemplates/
        └── version_4.Y.Z/
            ├── sno-ran-du/
            │   ├── ns.yaml
            │   ├── msc-binding.yaml
            │   └── sno-ran-du-pg-v4-Y-Z-v1.yaml
            ├── std-ran-du/
            │   ├── ns.yaml
            │   ├── msc-binding.yaml
            │   └── std-ran-du-pg-v4-Y-Z-v1.yaml
            └── source-crs/
    ```

    - `clustertemplates/` contains CRs that define how clusters are provisioned:

      - `hardwareprofiles/` contains `HardwareProfile` custom CRs that define firmware levels and BIOS settings for classes of bare-metal servers.

      - `inventory/` contains `BareMetalHost` CRs for sites where server inventory is managed through GitOps.

      - `version_4.Y.Z/` organizes content by the target OpenShift Container Platform release version.

      - `sno-ran-du/` and `std-ran-du/` are template directories for single-node and standard multi-node cluster topologies respectively.

      - `sno-ran-du-v4-Y-Z-1.yaml` is a `ClusterTemplate` CR that defines the cluster blueprint, including the parameter schema, node group definitions, and references to default ConfigMaps.

      - `clusterinstance-defaults-v1.yaml` is a `ConfigMap` containing default values for cluster installation parameters such as network configuration, image sets, and node settings. The `ProvisioningRequest` can override or supplement these values with site-specific parameters.

      - `policytemplates-defaults-v1.yaml` is a `ConfigMap` containing default values for Day 2 configuration policy parameters such as CPU allocation, hugepages, and SR-IOV settings.

      - `extra-manifest/` contains additional manifests applied during cluster installation.

    - `policytemplates/` contains `PolicyGenerator` CRs that define Day 2 configuration policies applied to managed clusters after provisioning:

      - `sno-ran-du-pg-v4-Y-Z-v1.yaml` is a `PolicyGenerator` CR that references source CRs and generates the policies enforced on the spoke cluster.

      - `source-crs/` contains the source CRs, such as subscriptions, performance profiles, and SR-IOV configurations, referenced by the policy generators.

2.  Create an ArgoCD `Application` CR for cluster templates that points to the `clustertemplates/` directory in your Git repository, for example:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: clusters
      namespace: openshift-gitops
    spec:
      destination:
        server: https://kubernetes.default.svc
      project: default
      source:
        path: clustertemplates
        repoURL: https://git.example.com/your-org/ocloud-templates.git
        targetRevision: main
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
      ignoreDifferences:
      - group: metal3.io
        jsonPointers:
        - /spec/preprovisioningNetworkDataName
        - /spec/online
        kind: BareMetalHost
    ```

    - `spec.source.repoURL` specifies the URL of the Git repository containing your cluster templates and configuration resources. Replace with the URL of your repository.

    - `spec.source.path` points to the `clustertemplates/` directory that contains `ClusterTemplate` CRs, defaults, and hardware profiles.

    - `spec.source.targetRevision` specifies the Git branch, tag, or commit to track. Set to the branch that contains your production-ready templates.

    - `spec.syncPolicy.automated` enables automatic synchronization. The `prune` option removes resources from the cluster that are no longer in Git, and `selfHeal` reverts manual changes made on the cluster back to the Git-defined state.

    - `spec.ignoreDifferences` prevents ArgoCD from reverting fields on `BareMetalHost` CRs that the Bare Metal Operator updates dynamically during provisioning.

3.  Create an ArgoCD `Application` CR for policy templates that points to the `policytemplates/` directory:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: policies
      namespace: openshift-gitops
    spec:
      destination:
        server: https://kubernetes.default.svc
      project: default
      source:
        path: policytemplates
        repoURL: https://git.example.com/your-org/ocloud-templates.git
        targetRevision: main
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
    ```

    - `spec.source.repoURL` specifies the URL of the Git repository. This can be the same repository as the cluster templates application if both directories exist in a single repository.

    - `spec.source.path` points to the `policytemplates/` directory that contains Red Hat Advanced Cluster Management (RHACM) policy generator resources and source CRs applied to managed clusters after provisioning.

    - `spec.syncPolicy.automated` enables automatic synchronization with pruning and self-healing, ensuring the hub cluster always reflects the latest policy definitions from Git.

4.  Apply the ArgoCD application CRs by running the following commands:

    ``` terminal
    $ oc apply -f <clusters_application_filename>.yaml
    $ oc apply -f <policies_application_filename>.yaml
    ```

    - Replace `<clusters_application_filename>.yaml` and `<policies_application_filename>.yaml` with the names of the application CRs.

- Verify that ArgoCD has synchronized the cluster templates to the hub cluster:

  ``` terminal
  $ oc get clustertemplates.clcm.openshift.io -A
  ```

  The output lists the `ClusterTemplate` CRs with their validation status. A `ClusterTemplateValidated` condition of `True` indicates that the template is ready for use.

# Configure mTLS for API access

You can configure mutual TLS (mTLS) to require client certificate authentication for all incoming connections to the O-Cloud Manager REST API. This secures API access for any external client, including SMO frameworks, automation platforms, and custom integrations.

- The O-Cloud Manager Operator is installed and running on the hub cluster.

- You have a TLS certificate and private key for the O-Cloud Manager ingress. The certificate must include `server auth` and `client auth` extended key usage.

- You have the CA certificate used to validate incoming client certificates.

1.  Create a TLS `Secret` containing the O-Cloud Manager certificate and private key. The `tls.crt` field must contain the full certificate chain with the device certificate first, intermediate certificates next, and the root certificate last.

    1.  To create the `Secret` using cert-manager, create a `Certificate` CR such as the following:

        ``` yaml
        apiVersion: cert-manager.io/v1
        kind: Certificate
        metadata:
          name: oran-o2ims-tls-certificate
          namespace: oran-o2ims
        spec:
          secretName: oran-o2ims-tls-certificate
          subject:
            organizations:
              - ORAN
          commonName: o2ims.apps.<cluster_domain>
          usages:
            - server auth
            - client auth
          dnsNames:
            - o2ims.apps.<cluster_domain>
          issuerRef:
            name: <issuer_name>
            kind: ClusterIssuer
            group: cert-manager.io
        ```

        where:

        `<cluster_domain>`
        Specifies the hub cluster domain name, for example `hub.example.com`.

        `<issuer_name>`
        Specifies the name of your cert-manager `ClusterIssuer` resource.

    2.  Alternatively, to create the `Secret` manually from existing certificate files, run the following command:

        ``` terminal
        $ oc create secret tls -n oran-o2ims oran-o2ims-tls-certificate \
          --cert <path_to_cert> \
          --key <path_to_key>
        ```

        where:

        `<path_to_cert>`
        Specifies the path to the full certificate chain file.

        `<path_to_key>`
        Specifies the path to the private key file.

2.  Create a `ConfigMap` containing the CA certificates used to validate incoming client certificates by running the following command:

    ``` terminal
    $ oc create configmap -n openshift-config ingress-client-ca-certs \
      --from-file=ca-bundle.pem=<path_to_client_ca>
    ```

    where:

    `<path_to_client_ca>`
    Specifies the path to the CA certificate file that validates incoming client certificates.

3.  Configure the `IngressController` to require mTLS for incoming connections by applying the following YAML:

    ``` yaml
    apiVersion: operator.openshift.io/v1
    kind: IngressController
    metadata:
      name: default
      namespace: openshift-ingress-operator
    spec:
      clientTLS:
        allowedSubjectPatterns:
          - "<subject_pattern>"
        clientCA:
          name: ingress-client-ca-certs
        clientCertificatePolicy: Required
    ```

    where:

    `<subject_pattern>`
    Optional. A regular expression that restricts access to specific certificate subjects, for example `^/O=ORAN/OU=SMO/`. Remove the `allowedSubjectPatterns` field to accept any valid client certificate signed by the configured CA.

    <div class="warning">

    If the ingress controller is shared with other applications, setting `clientCertificatePolicy: Required` enforces client certificates on all incoming connections. Consider creating a secondary ingress controller for the O-Cloud Manager domain to avoid impacting other applications. Set `clientCertificatePolicy: Optional` if you cannot enforce mTLS globally but have OAuth enabled.

    </div>

4.  Update the `Inventory` CR to reference the TLS certificate by running the following command:

    ``` terminal
    $ oc patch inventory default -n oran-o2ims --type merge \
      -p '{"spec":{"ingress":{"tls":{"secretName":"oran-o2ims-tls-certificate"}}}}'
    ```

- Verify that the ingress controller is configured for mTLS by running the following command:

  ``` terminal
  $ oc get ingresscontroller default -n openshift-ingress-operator \
    -o jsonpath='{.spec.clientTLS}'
  ```

  The output shows the configured `clientCertificatePolicy`, `clientCA`, and any `allowedSubjectPatterns`.

# Register the O-Cloud Manager with an SMO

Optionally, for telcommunications use cases, you can register the O-Cloud Manager with a Service Management and Orchestration (SMO) system by updating the `Inventory` custom resource (CR) with the SMO endpoint, OAuth credentials, and CA certificate configuration. Registration is a one-time operation that enables the SMO to manage infrastructure through the O2 IMS REST APIs.

- The O-Cloud Manager Operator is installed and running on the hub cluster.

- You configured mTLS for API access. For more information, see "Configure mTLS for API access".

- You have the SMO endpoint URL and registration endpoint path.

- You have OAuth2 client credentials for the O-Cloud Manager, obtained from the OAuth2 authorization server administrator.

- You have the CA certificate bundle if the SMO or OAuth2 server uses certificates signed by a non-public CA.

1.  If the SMO or OAuth2 server TLS certificates are signed by a non-public CA, create a `ConfigMap` with the CA certificate bundle and configure the cluster proxy by running the following commands:

    ``` terminal
    $ oc create configmap -n openshift-config <ca_configmap_name> \
      --from-file=ca-bundle.crt=<path_to_ca_bundle>
    $ oc patch proxy/cluster --type=merge \
      --patch='{"spec":{"trustedCA":{"name": "<ca_configmap_name>"}}}'
    ```

    where:

    `<ca_configmap_name>`
    Specifies a name for the `ConfigMap` that stores the CA certificate bundle, for example `custom-ca-certs`.

    `<path_to_ca_bundle>`
    Specifies the local file path to the CA certificate bundle that contains the certificates needed to trust the SMO and OAuth2 server endpoints.

    <div class="warning">

    If the cluster proxy already references a custom CA bundle, append the new certificates to the existing bundle rather than replacing it.

    </div>

2.  Create a `ConfigMap` with the trust bundle injection label so that the O-Cloud Manager can access both private and public CA certificates:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      labels:
        config.openshift.io/inject-trusted-cabundle: "true"
      name: o2ims-trusted-ca-bundle
      namespace: oran-o2ims
    ```

3.  Apply the `ConfigMap` by running the following command:

    ``` terminal
    $ oc apply -f <trusted_ca_bundle_filename>.yaml
    ```

    - Replace `<trusted_ca_bundle_filename>.yaml` with the name of the file.

4.  Create a `Secret` containing the OAuth client credentials by running the following command:

    ``` terminal
    $ oc create secret generic -n oran-o2ims oauth-client-secrets \
      --from-literal=client-id=<oauth_client_id> \
      --from-literal=client-secret=<oauth_client_secret>
    ```

    where:

    `<oauth_client_id>`
    Specifies the OAuth2 client ID issued by the SMO’s authorization server.

    `<oauth_client_secret>`
    Specifies the corresponding OAuth2 client secret.

5.  Update the `Inventory` CR in the `oran-o2ims` namespace to configure the SMO connection. For example, add the following to the `spec` section of the `Inventory` CR:

    ``` yaml
    # ...
    spec:
      smo:
        url: https://<smo_hostname>
        registrationEndpoint: <registration_endpoint>
        tls:
          secretName: oran-o2ims-tls-certificate
        oauth:
          url: https://<oauth_server_hostname>/realms/<realm>
          clientSecretName: oauth-client-secrets
          tokenEndpoint: /protocol/openid-connect/token
          scopes:
            - profile
            - openid
            - role:ocloud-manager
          usernameClaim: preferred_username
          groupsClaim: roles
      caBundleName: o2ims-trusted-ca-bundle
    # ...
    ```

    where:

    `<smo_hostname>`
    Specifies the hostname or URL of the SMO server.

    `<registration_endpoint>`
    Specifies the registration endpoint path on the SMO, for example `/mock_smo/v1/ocloud_observer`.

    `spec.smo.tls.secretName`
    Specifies the TLS `Secret`, see "Configure mTLS for API access" for more information. The O-Cloud Manager uses this certificate for outgoing connections to the SMO.

    `<oauth_server_hostname>/realms/<realm>`
    Specifies the OAuth2 authorization server hostname and realm used for token exchange.

    `clientSecretName`
    Specifies the name of the `Secret` resource containing the OAuth client credentials created in the previous step.

    `caBundleName`
    Specifies the name of the `ConfigMap` resource containing the trusted CA bundle. Omit this field if the SMO and OAuth server certificates are signed by a publicly trusted CA.

6.  Apply the updated `Inventory` CR by running the following command:

    ``` terminal
    $ oc apply -f <inventory_filename>.yaml
    ```

    - Replace `<inventory_filename>.yaml` with the name of the file.

- Verify that registration with the SMO completed successfully:

  ``` terminal
  $ oc describe inventories.ocloud.openshift.io default -n oran-o2ims
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` text
  Status:
    Deployment Status:
      Conditions:
        Last Transition Time:  2024-10-04T15:39:46Z
        Message:               Registered with SMO at: https://smo.example.com
        Reason:                SmoRegistrationSuccessful
        Status:                True
        Type:                  SmoRegistrationCompleted
  ```

# Authenticate using a service account token

You can authenticate to the O-Cloud Manager REST API by using a service account token. This method is suitable for development, testing, and standalone automation environments that do not require OAuth2 with mutual TLS (mTLS).

- You have `cluster-admin` permissions on the hub cluster.

- You installed the O-Cloud Manager Operator.

1.  Create a service account with API access permissions by running the following commands:

    ``` terminal
    $ oc create serviceaccount -n oran-o2ims <service_account_name>
    ```

    ``` terminal
    $ oc adm policy add-cluster-role-to-user oran-o2ims-admin-role \
      -n oran-o2ims -z <service_account_name>
    ```

    where:

    `<service_account_name>`
    Specifies a name for the service account used to access the API.

    `oran-o2ims-admin-role`
    An aggregated cluster role deployed by the Operator that grants read, write, and subscription access to all O-Cloud Manager API endpoints.

2.  Get the base URL for all O-Cloud Manager API requests from the ingress routes by running the following command:

    ``` terminal
    $ export API_BASE_URL=$(oc get routes -n oran-o2ims -o jsonpath='{.items[0].spec.host}')
    ```

3.  Create a scoped bearer token by running the following command:

    ``` terminal
    $ export MY_TOKEN=$(oc create token -n oran-o2ims <service_account_name> --duration=24h \
      --audience=alarms-server \
      --audience=resource-server \
      --audience=cluster-server \
      --audience=artifacts-server \
      --audience=provisioning-server)
    ```

    - The `--audience` flags scope the token to all O-Cloud Manager API services. Each service validates its own audience claim.

    - The `--duration` flag sets the token lifetime. Adjust as needed for your environment.

4.  Verify the connection by querying the O-Cloud information endpoint by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2" | jq
    ```

- A successful response returns O-Cloud metadata including the unique identifier and supported API versions.

# Authenticate using OAuth2

In production environments, the O-Cloud Manager REST API supports OAuth2 authentication with mutual TLS (mTLS). This method is used by SMO frameworks and external automation systems that require token-based access. You must acquire a JSON Web Token (JWT) from the OAuth2 authorization server configured in the `Inventory` custom resource (CR).

- The O-Cloud Manager Operator is installed and running on the hub cluster.

- You configured mTLS for API access. For more information, see "Configure mTLS for API access".

- You have the TLS client certificate and private key for API access.

- You have the CA certificate bundle that trusts the OAuth2 server and O-Cloud Manager ingress.

1.  Get the base URL for all O-Cloud Manager API requests from the ingress routes by running the following command:

    ``` terminal
    $ export API_BASE_URL=$(oc get routes -n oran-o2ims -o jsonpath='{.items[0].spec.host}')
    ```

2.  Acquire an OAuth2 token from the authorization server by running the following command:

    ``` terminal
    $ export MY_TOKEN=$(curl -s \
      --cert /path/to/client.crt \
      --key /path/to/client.key \
      --cacert /path/to/ca-bundle.crt \
      -X POST https://<oauth_server_hostname>/realms/<realm>/protocol/openid-connect/token \
      -d grant_type=client_credentials \
      -d client_id=<oauth_client_id> \
      -d client_secret=<oauth_client_secret> \
      -d 'scope=profile openid role:ocloud-manager' | jq -j .access_token)
    ```

    where:

    `/path/to/client.crt`
    Specifies the path to the TLS client certificate. This is the same certificate configured in the `Inventory` CR’s `spec.smo.tls.secretName` field.

    `/path/to/client.key`
    Specifies the path to the TLS private key corresponding to the client certificate.

    `/path/to/ca-bundle.crt`
    Specifies the path to the CA certificate bundle that trusts the OAuth2 server.

    `<oauth_server_hostname>/realms/<realm>`
    Specifies the OAuth2 authorization server hostname and realm, matching the `spec.smo.oauth.url` value in the `Inventory` CR.

    `<oauth_client_id>`
    Specifies the OAuth2 client ID for the SMO or API consumer.

    `<oauth_client_secret>`
    Specifies the corresponding OAuth2 client secret.

3.  Verify the connection by querying the O-Cloud information endpoint by running the following command:

    ``` terminal
    $ curl -s \
      --cert /path/to/client.crt \
      --key /path/to/client.key \
      --cacert /path/to/ca-bundle.crt \
      -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2" | jq
    ```

- A successful response returns O-Cloud metadata including the unique identifier and supported API versions.

  <div class="note">

  When using mTLS, include the `--cert`, `--key`, and `--cacert` flags in all subsequent API requests. If the ingress certificate is signed by a publicly trusted CA, the `--cacert` flag can be omitted.

  </div>

# Additional resources

- [Cluster lifecycle with multicluster engine operator overview](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.17/html/clusters/cluster_mce_overview)

- [Understanding TLS security profiles](../security/tls-security-profiles.xml#tls-profiles-understanding_tls-security-profiles)

- [Configuring OAuth clients](../authentication/configuring-oauth-clients.xml#configuring-oauth-clients)

- [Using bound service account tokens](../authentication/bound-service-account-tokens.xml#bound-service-account-tokens)
