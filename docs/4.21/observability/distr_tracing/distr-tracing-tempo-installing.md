Installing the Distributed Tracing Platform involves the following steps:

1.  Installing the Tempo Operator.

2.  Setting up a supported object store and creating a secret for the object store credentials.

3.  Configuring the permissions and tenants.

4.  Depending on your use case, installing your choice of deployment:

    - Microservices-mode `TempoStack` instance

    - Monolithic-mode `TempoMonolithic` instance

# Installing the Tempo Operator

You can install the Tempo Operator by using the web console or the command line.

## Installing the Tempo Operator by using the web console

You can install the Tempo Operator from the OpenShift Container Platform web console.

- You are logged in to the OpenShift Container Platform web console as a cluster administrator with the `cluster-admin` role.

- For Red Hat OpenShift Dedicated, you must be logged in using an account with the `dedicated-admin` role.

- You have completed setting up the required object storage by a supported provider: [Red Hat OpenShift Data Foundation](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation), [MinIO](https://min.io/), [Amazon S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), [Google Cloud Storage](https://cloud.google.com/storage/). For more information, see "Object storage setup".

  <div class="warning">

  Object storage is required and not included with the Distributed Tracing Platform. You must choose and set up object storage by a supported provider before installing the Distributed Tracing Platform.

  </div>

1.  In the web console, search for `Tempo Operator`.

    <div class="tip">

    In OpenShift Container Platform 4.19 or earlier, go to **Operators** → **OperatorHub**.

    In OpenShift Container Platform 4.20 or later, go to **Ecosystem** → **Software Catalog**.

    </div>

2.  Select the **Tempo Operator** that is **provided by Red Hat**.

    <div class="important">

    The following selections are the default presets for this Operator:

    - **Update channel** → **stable**

    - **Installation mode** → **All namespaces on the cluster**

    - **Installed Namespace** → **openshift-tempo-operator**

    - **Update approval** → **Automatic**

    </div>

3.  Select the **Enable Operator recommended cluster monitoring on this Namespace** checkbox.

4.  Select **Install** → **Install** → **View Operator**.

- In the **Details** tab of the page of the installed Operator, under **ClusterServiceVersion details**, verify that the installation **Status** is **Succeeded**.

## Installing the Tempo Operator by using the CLI

You can install the Tempo Operator from the command line.

- An active OpenShift CLI (`oc`) session by a cluster administrator with the `cluster-admin` role.

  <div class="tip">

  - Ensure that your OpenShift CLI (`oc`) version is up to date and matches your OpenShift Container Platform version.

  - Run `oc login`:

    ``` terminal
    $ oc login --username=<your_username>
    ```

  </div>

- You have completed setting up the required object storage by a supported provider: [Red Hat OpenShift Data Foundation](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation), [MinIO](https://min.io/), [Amazon S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), [Google Cloud Storage](https://cloud.google.com/storage/). For more information, see "Object storage setup".

  <div class="warning">

  Object storage is required and not included with the Distributed Tracing Platform. You must choose and set up object storage by a supported provider before installing the Distributed Tracing Platform.

  </div>

1.  Create a project for the Tempo Operator by running the following command:

    ``` terminal
    $ oc apply -f - << EOF
    apiVersion: project.openshift.io/v1
    kind: Project
    metadata:
      labels:
        kubernetes.io/metadata.name: openshift-tempo-operator
        openshift.io/cluster-monitoring: "true"
      name: openshift-tempo-operator
    EOF
    ```

2.  Create an Operator group by running the following command:

    ``` terminal
    $ oc apply -f - << EOF
    apiVersion: operators.coreos.com/v1
    kind: OperatorGroup
    metadata:
      name: openshift-tempo-operator
      namespace: openshift-tempo-operator
    spec:
      upgradeStrategy: Default
    EOF
    ```

3.  Create a subscription by running the following command:

    ``` terminal
    $ oc apply -f - << EOF
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: tempo-product
      namespace: openshift-tempo-operator
    spec:
      channel: stable
      installPlanApproval: Automatic
      name: tempo-product
      source: redhat-operators
      sourceNamespace: openshift-marketplace
    EOF
    ```

- Check the Operator status by running the following command:

  ``` terminal
  $ oc get csv -n openshift-tempo-operator
  ```

# Object storage setup

You can use the following configuration parameters when setting up a supported object storage.

<div class="important">

Using object storage requires setting up a supported object store and creating a secret for the object store credentials before deploying a `TempoStack` or `TempoMonolithic` instance.

</div>

<table>
<caption>Required secret parameters</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Storage provider</th>
<th style="text-align: left;">Secret parameters</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong><a href="https://access.redhat.com/documentation/en-us/red_hat_openshift_data_foundation/">Red Hat OpenShift Data Foundation</a></strong></p></td>
<td style="text-align: left;"><p><code>name: tempostack-dev-odf # example</code></p>
<p><code>bucket: &lt;bucket_name&gt; # requires an ObjectBucketClaim</code></p>
<p><code>endpoint: https://s3.openshift-storage.svc</code></p>
<p><code>access_key_id: &lt;data_foundation_access_key_id&gt;</code></p>
<p><code>access_key_secret: &lt;data_foundation_access_key_secret&gt;</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>MinIO</strong></p></td>
<td style="text-align: left;"><p>See <a href="https://operator.min.io/">MinIO Operator</a>.</p>
<p><code>name: tempostack-dev-minio # example</code></p>
<p><code>bucket: &lt;minio_bucket_name&gt; # MinIO documentation</code></p>
<p><code>endpoint: &lt;minio_bucket_endpoint&gt;</code></p>
<p><code>access_key_id: &lt;minio_access_key_id&gt;</code></p>
<p><code>access_key_secret: &lt;minio_access_key_secret&gt;</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>IBM Cloud Object Storage (COS)</strong></p></td>
<td style="text-align: left;"><p><code>bucket: &lt;ibm_bucket_name&gt;</code></p>
<p><code>endpoint: &lt;ibm_bucket_endpoint&gt;</code></p>
<p><code>access_key_id: &lt;ibm_bucket_access_key&gt;</code></p>
<p><code>access_key_secret: &lt;ibm_bucket_secret_key&gt;</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Amazon S3</strong></p></td>
<td style="text-align: left;"><p><code>name: tempostack-dev-s3 # example</code></p>
<p><code>bucket: &lt;s3_bucket_name&gt; # Amazon S3 documentation</code></p>
<p><code>endpoint: &lt;s3_bucket_endpoint&gt;</code></p>
<p><code>access_key_id: &lt;s3_access_key_id&gt;</code></p>
<p><code>access_key_secret: &lt;s3_access_key_secret&gt;</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Amazon S3 with Security Token Service (STS)</strong></p></td>
<td style="text-align: left;"><p><code>name: tempostack-dev-s3 # example</code></p>
<p><code>bucket: &lt;s3_bucket_name&gt; # Amazon S3 documentation</code></p>
<p><code>region: &lt;s3_region&gt;</code></p>
<p><code>role_arn: &lt;s3_role_arn&gt;</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Microsoft Azure Blob Storage</strong></p></td>
<td style="text-align: left;"><p><code>name: tempostack-dev-azure # example</code></p>
<p><code>container: &lt;azure_blob_storage_container_name&gt; # Microsoft Azure documentation</code></p>
<p><code>account_name: &lt;azure_blob_storage_account_name&gt;</code></p>
<p><code>account_key: &lt;azure_blob_storage_account_key&gt;</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Google Cloud Storage on Google Cloud</strong></p></td>
<td style="text-align: left;"><p><code>name: tempostack-dev-gcs # example</code></p>
<p><code>bucketname: &lt;google_cloud_storage_bucket_name&gt; # requires a bucket created in a Google Cloud project</code></p>
<p><code>key.json: &lt;path/to/key.json&gt; # requires a service account in the bucket’s GCP project for GCP authentication</code></p></td>
</tr>
</tbody>
</table>

Required secret parameters

## Setting up the Amazon S3 storage with the Security Token Service

You can set up the Amazon S3 storage with the Security Token Service (STS) and AWS Command Line Interface (AWS CLI). Optionally, you can also use the Cloud Credential Operator (CCO).

<div class="important">

Using the Distributed Tracing Platform with the Amazon S3 storage and STS is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

- You have installed the latest version of the AWS CLI.

- If you intend to use the CCO, you have installed and configured the CCO in your cluster.

1.  Create an AWS S3 bucket.

2.  Create the following `trust.json` file for the AWS Identity and Access Management (AWS IAM) policy for the purpose of setting up a trust relationship between the AWS IAM role, which you will create in the next step, and the service account of either the `TempoStack` or `TempoMonolithic` instance:

    <div class="formalpara-title">

    **`trust.json`**

    </div>

    ``` yaml
    {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "Federated": "arn:aws:iam::<aws_account_id>:oidc-provider/<oidc_provider>"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
              "StringEquals": {
                "<oidc_provider>:sub": [
                  "system:serviceaccount:<openshift_project_for_tempo>:tempo-<tempo_custom_resource_name>"
                  "system:serviceaccount:<openshift_project_for_tempo>:tempo-<tempo_custom_resource_name>-query-frontend"
               ]
             }
           }
         }
        ]
    }
    ```

    - The OpenID Connect (OIDC) provider that you have configured on the OpenShift Container Platform.

    - The namespace in which you intend to create either a `TempoStack` or `TempoMonolithic` instance. Replace `<tempo_custom_resource_name>` with the `metadata` name that you define in your `TempoStack` or `TempoMonolithic` custom resource.

      <div class="tip">

      You can also get the value for the OIDC provider by running the following command:

      ``` terminal
      $ oc get authentication cluster -o json | jq -r '.spec.serviceAccountIssuer' | sed 's~http[s]*://~~g'
      ```

      </div>

3.  Create an AWS IAM role by attaching the created `trust.json` policy file. You can do this by running the following command:

    ``` terminal
    $ aws iam create-role \
          --role-name "tempo-s3-access" \
          --assume-role-policy-document "file:///tmp/trust.json" \
          --query Role.Arn \
          --output text
    ```

4.  Attach an AWS IAM policy to the created AWS IAM role. You can do this by running the following command:

    ``` terminal
    $ aws iam attach-role-policy \
          --role-name "tempo-s3-access" \
          --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"
    ```

5.  If you are not using the CCO, skip this step. If you are using the CCO, configure the cloud provider environment for the Tempo Operator. You can do this by running the following command:

    ``` terminal
    $ oc patch subscription <tempo_operator_sub> \
              -n <tempo_operator_namespace> \
              --type='merge' -p '{"spec": {"config": {"env": [{"name": "ROLEARN", "value": "'"<role_arn>"'"}]}}}'
    ```

    - The name of the Tempo Operator subscription.

    - The namespace of the Tempo Operator.

    - The AWS STS requires adding the `ROLEARN` environment variable to the Tempo Operator subcription. As the `<role_arn>` value, add the Amazon Resource Name (ARN) of the AWS IAM role that you created in step 3.

6.  In the OpenShift Container Platform, create an object storage secret with keys as follows:

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: <secret_name>
    stringData:
      bucket: <s3_bucket_name>
      region: <s3_region>
      role_arn: <s3_role_arn>
    type: Opaque
    ```

7.  When the object storage secret is created, update the relevant custom resource of the Distributed Tracing Platform instance as follows:

    <div class="formalpara-title">

    **Example `TempoStack` custom resource**

    </div>

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: <name>
      namespace: <namespace>
    spec:
    # ...
      storage:
        secret:
          name: <secret_name>
          type: s3
          credentialMode: token-cco
    # ...
    ```

    - The secret that you created in the previous step.

    - If you are not using the CCO, omit this line. If you are using the CCO, add this parameter with the `token-cco` value.

      <div class="formalpara-title">

      **Example `TempoMonolithic` custom resource**

      </div>

      ``` yaml
      apiVersion: tempo.grafana.com/v1alpha1
      kind: TempoMonolithic
      metadata:
        name: <name>
        namespace: <namespace>
      spec:
      # ...
        storage:
          traces:
            backend: s3
            s3:
              secret: <secret_name>
              credentialMode: token-cco
      # ...
      ```

    - The secret that you created in the previous step.

    - If you are not using the CCO, omit this line. If you are using the CCO, add this parameter with the `token-cco` value.

- [AWS Identity and Access Management Documentation](https://docs.aws.amazon.com/iam/) (AWS documentation)

- [AWS Command Line Interface Documentation](https://docs.aws.amazon.com/cli/) (AWS documentation)

- [Configuring an OpenID Connect identity provider](../../authentication/identity_providers/configuring-oidc-identity-provider.xml#configuring-oidc-identity-provider)

- [Identify AWS resources with Amazon Resource Names (ARNs)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) (AWS documentation)

## Setting up the Azure storage with the Security Token Service

You can set up the Azure storage with the Security Token Service (STS) by using the Azure Command Line Interface (Azure CLI).

<div class="important">

Using the Distributed Tracing Platform with the Azure storage and STS is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

- You have installed the latest version of the Azure CLI.

- You have created an Azure storage account.

- You have created an Azure blob storage container.

1.  Create an Azure managed identity by running the following command:

    ``` terminal
    $ az identity create \
      --name <identity_name> \
      --resource-group <resource_group> \
      --location <region> \
      --subscription <subscription_id>
    ```

    - The name you have chosen for the managed identity.

    - The Azure resource group where you want the identity to be created.

    - The Azure region, which must be the same region as for the resource group.

    - The Azure subscription ID.

2.  Create a federated identity credential for the OpenShift Container Platform service account for use by all components of the Distributed Tracing Platform except the Query Frontend. You can do this by running the following command:

    ``` terminal
    $ az identity federated-credential create \
      --name <credential_name> \
      --identity-name <identity_name> \
      --resource-group <resource_group> \
      --issuer <oidc_provider> \
      --subject <tempo_service_account_subject> \
      --audiences <audience>
    ```

    - Federated identity credentials allow OpenShift Container Platform service accounts to authenticate as an Azure managed identity without storing secrets or using an Azure service principal identity.

    - The name you have chosen for the federated credential.

    - The URL of the OpenID Connect (OIDC) provider for your cluster.

    - The service account subject for your cluster in the following format: `system:serviceaccount:<namespace>:tempo-<tempostack_instance_name>`.

    - The expected audience, which is to be used for validating the issued tokens for the federated identity credential. This is commonly set to `api://AzureADTokenExchange`.

      <div class="tip">

      You can get the URL of the OpenID Connect (OIDC) issuer for your cluster by running the following command:

          $ oc get authentication cluster -o json | jq -r .spec.serviceAccountIssuer

      </div>

3.  Create a federated identity credential for the OpenShift Container Platform service account for use by the Query Frontend component of the Distributed Tracing Platform. You can do this by running the following command:

    ``` terminal
    $ az identity federated-credential create \
      --name <credential_name>-frontend \
      --identity-name <identity_name> \
      --resource-group <resource_group> \
      --issuer <cluster_issuer> \
      --subject <tempo_service_account_query_frontend_subject> \
      --audiences <audience> | jq
    ```

    - Federated identity credentials allow OpenShift Container Platform service accounts to authenticate as an Azure managed identity without storing secrets or using an Azure service principal identity.

    - The name you have chosen for the frontend federated identity credential.

    - The service account subject for your cluster in the following format: `system:serviceaccount:<namespace>:tempo-<tempostack_instance_name>`.

4.  Assign the Storage Blob Data Contributor role to the Azure service principal identity of the created Azure managed identity. You can do this by running the following command:

    ``` terminal
    $ az role assignment create \
      --assignee <assignee_name> \
      --role "Storage Blob Data Contributor" \
      --scope "/subscriptions/<subscription_id>
    ```

    - The Azure service principal identity of the Azure managed identity that you created in step 1.

      <div class="tip">

      You can get the `<assignee_name>` value by running the following command:

          $ az ad sp list --all --filter "servicePrincipalType eq 'ManagedIdentity'" | jq -r --arg idName <identity_name> '.[] | select(.displayName == $idName) | .appId'`

      </div>

5.  Fetch the client ID of the Azure managed identity that you created in step 1:

    ``` bash
    CLIENT_ID=$(az identity show \
      --name <identity_name> \
      --resource-group <resource_group> \
      --query clientId \
      -o tsv)
    ```

    - Copy and paste the `<identity_name>` value from step 1.

    - Copy and paste the `<resource_group>` value from step 1.

6.  Create an OpenShift Container Platform secret for the Azure workload identity federation (WIF). You can do this by running the following command:

    ``` terminal
    $ oc create -n <tempo_namespace> secret generic azure-secret \
      --from-literal=container=<azure_storage_azure_container> \
      --from-literal=account_name=<azure_storage_azure_accountname> \
      --from-literal=client_id=<client_id> \
      --from-literal=audience=<audience> \
      --from-literal=tenant_id=<tenant_id>
    ```

    - The name of the Azure Blob Storage container.

    - The name of the Azure Storage account.

    - The client ID of the managed identity that you fetched in the previous step.

    - Optional: Defaults to `api://AzureADTokenExchange`.

    - Azure Tenant ID.

7.  When the object storage secret is created, update the relevant custom resource of the Distributed Tracing Platform instance as follows:

    <div class="formalpara-title">

    **Example `TempoStack` custom resource**

    </div>

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: <name>
      namespace: <namespace>
    spec:
    # ...
      storage:
        secret:
          name: <secret_name>
          type: azure
    # ...
    ```

    - The secret that you created in the previous step.

      <div class="formalpara-title">

      **Example `TempoMonolithic` custom resource**

      </div>

      ``` yaml
      apiVersion: tempo.grafana.com/v1alpha1
      kind: TempoMonolithic
      metadata:
        name: <name>
        namespace: <namespace>
      spec:
      # ...
        storage:
          traces:
            backend: azure
            azure:
              secret: <secret_name>
      # ...
      ```

    - The secret that you created in the previous step.

- [Install the Azure CLI on Linux](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux) (Azure documentation)

## Setting up the Google Cloud storage with the Security Token Service

You can set up the Google Cloud Storage (GCS) with the Security Token Service (STS) by using the Google Cloud CLI.

<div class="important">

Using the Distributed Tracing Platform with the GCS and STS is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

- You have installed the latest version of the Google Cloud CLI.

1.  Create a GCS bucket on the Google Cloud.

2.  Create or reuse a service account with Google’s Identity and Access Management (IAM):

    ``` bash
    SERVICE_ACCOUNT_EMAIL=$(gcloud iam service-accounts create <iam_service_account_name> \
        --display-name="Tempo Account" \
        --project <project_id>  \
        --format='value(email)' \
        --quiet)
    ```

    - The name of the service account on the Google Cloud.

    - The project ID of the service account on the Google Cloud.

3.  Bind the required Google Cloud roles to the created service account at the project level. You can do this by running the following command:

    ``` terminal
    $ gcloud projects add-iam-policy-binding <project_id> \
        --member "serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role "roles/storage.objectAdmin"
    ```

4.  Retrieve the `POOL_ID` value of the Google Cloud Workload Identity Pool that is associated with the cluster. How you can retrieve this value depends on your environment, so the following command is only an example:

    ``` terminal
    $ OIDC_ISSUER=$(oc get authentication.config cluster -o jsonpath='{.spec.serviceAccountIssuer}') \
    &&
      POOL_ID=$(echo "$OIDC_ISSUER" | awk -F'/' '{print $NF}' | sed 's/-oidc$//')
    ```

5.  Add the IAM policy bindings. You can do this by running the following commands:

    ``` terminal
    $ gcloud iam service-accounts add-iam-policy-binding "$SERVICE_ACCOUNT_EMAIL" \
      --role="roles/iam.workloadIdentityUser" \
      --member="principal://iam.googleapis.com/projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/subject/system:serviceaccount:<tempo_namespace>:tempo-<tempo_name>" \
      --project=<project_id> \
      --quiet \
    &&
      gcloud iam service-accounts add-iam-policy-binding "$SERVICE_ACCOUNT_EMAIL" \
      --role="roles/iam.workloadIdentityUser" \
      --member="principal://iam.googleapis.com/projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/subject/system:serviceaccount:<tempo_namespace>:tempo-<tempo_name>-query-frontend" \
      --project=<project_id> \
      --quiet
    &&
      gcloud storage buckets add-iam-policy-binding "gs://$BUCKET_NAME" \
      --role="roles/storage.admin" \
      --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
      --condition=None
    ```

    - The `$SERVICE_ACCOUNT_EMAIL` is the output of the command in step 2.

6.  Create a credential file for the `key.json` key of the storage secret for use by the `TempoStack` custom resource. You can do this by running the following command:

    ``` terminal
    $ gcloud iam workload-identity-pools create-cred-config \
        "projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/providers/<provider_id>" \
        --service-account="$SERVICE_ACCOUNT_EMAIL" \
        --credential-source-file=/var/run/secrets/storage/serviceaccount/token \
        --credential-source-type=text \
        --output-file=<output_file_path>
    ```

    - The `credential-source-file` parameter must always point to the `/var/run/secrets/storage/serviceaccount/token` path because the Operator mounts the token from this path.

    - The path for saving the output file.

7.  Get the correct audience by running the following command:

    ``` terminal
    $ gcloud iam workload-identity-pools providers describe "$PROVIDER_NAME" --format='value(oidc.allowedAudiences[0])'
    ```

8.  Create a storage secret for the Distributed Tracing Platform by running the following command.

    ``` terminal
    $ oc -n <tempo_namespace> create secret generic gcs-secret \
      --from-literal=bucketname="<bucket_name>" \
      --from-literal=audience="<audience>" \
      --from-file=key.json=<output_file_path>
    ```

    - The bucket name of the Google Cloud Storage.

    - The audience that you got in the previous step.

    - The credential file that you created in step 6.

9.  When the object storage secret is created, update the relevant custom resource of the Distributed Tracing Platform instance as follows:

    <div class="formalpara-title">

    **Example `TempoStack` custom resource**

    </div>

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: <name>
      namespace: <namespace>
    spec:
    # ...
      storage:
        secret:
          name: <secret_name>
          type: gcs
    # ...
    ```

    - The secret that you created in the previous step.

      <div class="formalpara-title">

      **Example `TempoMonolithic` custom resource**

      </div>

      ``` yaml
      apiVersion: tempo.grafana.com/v1alpha1
      kind: TempoMonolithic
      metadata:
        name: <name>
        namespace: <namespace>
      spec:
      # ...
        storage:
          traces:
            backend: gcs
            gcs:
              secret: <secret_name>
      # ...
      ```

    - The secret that you created in the previous step.

- [Install the gcloud CLI](https://cloud.google.com/sdk/docs/install) (Google Cloud Documentation)

- [Service accounts overview](https://cloud.google.com/iam/docs/service-account-overview) (Google Cloud Documentation)

## Setting up IBM Cloud Object Storage

You can set up IBM Cloud Object Storage by using the OpenShift CLI (`oc`).

- You have installed the latest version of OpenShift CLI (`oc`). For more information, see "Getting started with the OpenShift CLI" in *Configure: CLI tools*.

- You have installed the latest version of IBM Cloud Command Line Interface (`ibmcloud`). For more information, see "Getting started with the IBM Cloud CLI" in *IBM Cloud Docs*.

- You have configured IBM Cloud Object Storage. For more information, see "Choosing a plan and creating an instance" in *IBM Cloud Docs*.

  - You have an IBM Cloud Platform account.

  - You have ordered an IBM Cloud Object Storage plan.

  - You have created an instance of IBM Cloud Object Storage.

1.  On IBM Cloud, create an object store bucket.

2.  On IBM Cloud, create a service key for connecting to the object store bucket by running the following command:

    ``` terminal
    $ ibmcloud resource service-key-create <ibm_bucket_name> Writer \
      --instance-name <ibm_bucket_name> --parameters '{"HMAC":true}'
    ```

3.  On IBM Cloud, create a secret with the bucket credentials by running the following command:

    ``` terminal
    $ oc -n <namespace> create secret generic <ibm_cos_secret> \
      --from-literal=bucket="<ibm_bucket_name>" \
      --from-literal=endpoint="<ibm_bucket_endpoint>" \
      --from-literal=access_key_id="<ibm_bucket_access_key>" \
      --from-literal=access_key_secret="<ibm_bucket_secret_key>"
    ```

4.  On OpenShift Container Platform, create an object storage secret with keys as follows:

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: <ibm_cos_secret>
    stringData:
      bucket: <ibm_bucket_name>
      endpoint: <ibm_bucket_endpoint>
      access_key_id: <ibm_bucket_access_key>
      access_key_secret: <ibm_bucket_secret_key>
    type: Opaque
    ```

5.  On OpenShift Container Platform, set the storage section in the `TempoStack` custom resource as follows:

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    # ...
    spec:
    # ...
      storage:
        secret:
          name: <ibm_cos_secret>
          type: s3
    # ...
    ```

    - Name of the secret that contains the IBM Cloud Storage access and secret keys.

- [Getting started with the OpenShift CLI](../../cli_reference/openshift_cli/getting-started-cli.xml#cli-getting-started)

- [Getting started with the IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cli-getting-started) (IBM Cloud Docs)

- [Choosing a plan and creating an instance](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-provision) (IBM Cloud Docs)

- [Getting started with IBM Cloud Object Storage: Before you begin](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-getting-started-cloud-object-storage&q=credential&tags=cloud-object-storage&offset=10#getting-started) (IBM Cloud Docs)

# Configuring the permissions and tenants

Before installing a `TempoStack` or `TempoMonolithic` instance, you must define one or more tenants and configure their read and write access.

<div class="warning">

Tenant access is global. Granting access to a tenant applies to all `TempoStack` and `TempoMonolithic` instances whose configuration includes that tenant.

</div>

You can configure such an authorization setup by using a cluster role and cluster role binding for the Kubernetes Role-Based Access Control (RBAC). By default, no users are granted read or write permissions. For more information, see "Configuring the read permissions for tenants" and "Configuring the write permissions for tenants".

<div class="note">

The OpenTelemetry Collector of the Red Hat build of OpenTelemetry can send trace data to a `TempoStack` or `TempoMonolithic` instance by using the service account with RBAC for writing the data.

</div>

| Component      | Tempo Gateway service | OpenShift OAuth | `TokenReview` API | `SubjectAccessReview` API |
|----------------|-----------------------|-----------------|-------------------|---------------------------|
| Authentication | X                     | X               | X                 |                           |
| Authorization  | X                     |                 |                   | X                         |

Authentication and authorization

## Configuring the read permissions for tenants

You can configure the read permissions for tenants from the **Administrator** view of the web console or from the command line.

- You are logged in to the OpenShift Container Platform web console as a cluster administrator with the `cluster-admin` role.

- For Red Hat OpenShift Dedicated, you must be logged in using an account with the `dedicated-admin` role.

1.  Define the tenants by adding the `tenantName` and `tenantId` parameters with your values of choice to the `TempoStack` custom resource (CR):

    <div class="formalpara-title">

    **Tenant example in a `TempoStack` CR**

    </div>

    ``` yaml
    apiVersion: tempo.grafana.com/v1alpha1
    kind: TempoStack
    metadata:
      name: redmetrics
    spec:
    # ...
      tenants:
        mode: openshift
        authentication:
          - tenantName: dev
            tenantId: "1610b0c3-c509-4592-a256-a1871353dbfa"
    # ...
    ```

    - A `tenantName` value of the user’s choice.

    - A `tenantId` value of the user’s choice.

2.  Add the tenants to a cluster role with the read (`get`) permissions to read traces.

    <div class="formalpara-title">

    **Example RBAC configuration in a `ClusterRole` resource**

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: tempostack-traces-reader
    rules:
      - apiGroups:
          - 'tempo.grafana.com'
        resources:
          - dev
          - prod
        resourceNames:
          - traces
        verbs:
          - 'get'
    ```

    - Lists the tenants, `dev` and `prod` in this example, which are defined by using the `tenantName` parameter in the previous step.

    - Enables the read operation for the listed tenants.

3.  Grant authenticated users the read permissions for trace data by defining a cluster role binding for the cluster role from the previous step.

    <div class="formalpara-title">

    **Example RBAC configuration in a `ClusterRoleBinding` resource**

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: tempostack-traces-reader
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: tempostack-traces-reader
    subjects:
      - kind: Group
        apiGroup: rbac.authorization.k8s.io
        name: system:authenticated
    ```

    - Grants all authenticated users the read permissions for trace data.

## Configuring the write permissions for tenants

You can configure the write permissions for tenants from the **Administrator** view of the web console or from the command line.

- You are logged in to the OpenShift Container Platform web console as a cluster administrator with the `cluster-admin` role.

- For Red Hat OpenShift Dedicated, you must be logged in using an account with the `dedicated-admin` role.

- You have installed the OpenTelemetry Collector and configured it to use an authorized service account with permissions. For more information, see "Creating the required RBAC resources automatically" in the Red Hat build of OpenTelemetry documentation.

1.  Create a service account for use with OpenTelemetry Collector.

    ``` yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: otel-collector
      namespace: <project_of_opentelemetry_collector_instance>
    ```

2.  Add the tenants to a cluster role with the write (`create`) permissions to write traces.

    <div class="formalpara-title">

    **Example RBAC configuration in a `ClusterRole` resource**

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: tempostack-traces-write
    rules:
      - apiGroups:
          - 'tempo.grafana.com'
        resources:
          - dev
        resourceNames:
          - traces
        verbs:
          - 'create'
    ```

    - Lists the tenants.

    - Enables the write operation.

3.  Grant the OpenTelemetry Collector the write permissions by defining a cluster role binding to attach the OpenTelemetry Collector service account.

    <div class="formalpara-title">

    **Example RBAC configuration in a `ClusterRoleBinding` resource**

    </div>

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: tempostack-traces
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: tempostack-traces-write
    subjects:
      - kind: ServiceAccount
        name: otel-collector
        namespace: otel
    ```

    - The service account that you created in a previous step. The client uses it when exporting trace data.

4.  Configure the `OpenTelemetryCollector` custom resource as follows:

    - Add the `bearertokenauth` extension and a valid token to the tracing pipeline service.

    - Add the tenant name in the `otlp/otlphttp` exporters as the `X-Scope-OrgID` headers.

    - Enable TLS with a valid certificate authority file.

      <div class="formalpara-title">

      **Sample OpenTelemetry CR configuration**

      </div>

      ``` yaml
      apiVersion: opentelemetry.io/v1beta1
      kind: OpenTelemetryCollector
      metadata:
        name: cluster-collector
        namespace: <project_of_tempostack_instance>
      spec:
        mode: deployment
        serviceAccount: otel-collector
        config: |
            extensions:
              bearertokenauth:
                filename: "/var/run/secrets/kubernetes.io/serviceaccount/token"
            exporters:
              otlp/dev:
                endpoint: sample-gateway.tempo.svc.cluster.local:8090
                tls:
                  insecure: false
                  ca_file: "/var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt"
                auth:
                  authenticator: bearertokenauth
                headers:
                  X-Scope-OrgID: "dev"
              otlphttp/dev:
                endpoint: https://sample-gateway.<project_of_tempostack_instance>.svc.cluster.local:8080/api/traces/v1/dev
                tls:
                  insecure: false
                  ca_file: "/var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt"
                auth:
                  authenticator: bearertokenauth
                headers:
                  X-Scope-OrgID: "dev"
            service:
              extensions: [bearertokenauth]
              pipelines:
                traces:
                  exporters: [otlp/dev]

      # ...
      ```

      - Service account configured with write permissions.

      - Bearer Token extension to use service account token.

      - The service account token. The client sends the token to the tracing pipeline service as the bearer token header.

      - Specify either the OTLP gRPC Exporter (`otlp/dev`) or the OTLP HTTP Exporter (`otlphttp/dev`).

      - Enabled TLS with a valid service CA file.

      - Header with tenant name.

      - Specify either the OTLP gRPC Exporter (`otlp/dev`) or the OTLP HTTP Exporter (`otlphttp/dev`).

      - The exporter you specified in `exporters` section of the CR.

- [Creating the required RBAC resources automatically](https://docs.redhat.com/en/documentation/red_hat_build_of_opentelemetry/latest/html/installing_red_hat_build_of_opentelemetry/install-otel)

# Installing a TempoStack instance

You can install a `TempoStack` instance by using the web console or command line.

## Installing a TempoStack instance by using the web console

You can install a `TempoStack` instance from the **Administrator** view of the web console.

- You are logged in to the OpenShift Container Platform web console as a cluster administrator with the `cluster-admin` role.

- For Red Hat OpenShift Dedicated, you must be logged in using an account with the `dedicated-admin` role.

- You have completed setting up the required object storage by a supported provider: [Red Hat OpenShift Data Foundation](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation), [MinIO](https://min.io/), [Amazon S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), [Google Cloud Storage](https://cloud.google.com/storage/). For more information, see "Object storage setup".

  <div class="warning">

  Object storage is required and not included with the Distributed Tracing Platform. You must choose and set up object storage by a supported provider before installing the Distributed Tracing Platform.

  </div>

- You have defined one or more tenants and configured the read and write permissions. For more information, see "Configuring the read permissions for tenants" and "Configuring the write permissions for tenants".

  <div class="note">

  A `TempoStack` instance without configured tenants is not supported.

  </div>

1.  Go to **Home** → **Projects** → **Create Project** to create a permitted project of your choice for the `TempoStack` instance that you will create in a subsequent step. Project names beginning with the `openshift-` prefix are not permitted.

2.  Go to **Workloads** → **Secrets** → **Create** → **From YAML** to create a secret for your object storage bucket in the project that you created for the `TempoStack` instance. For more information, see "Object storage setup".

    <div class="formalpara-title">

    **Example secret for Amazon S3 and MinIO storage**

    </div>

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: minio-test
    stringData:
      endpoint: http://minio.minio.svc:9000
      bucket: tempo
      access_key_id: tempo
      access_key_secret: <secret>
    type: Opaque
    ```

3.  Create a `TempoStack` instance.

    <div class="note">

    You can create multiple `TempoStack` instances in separate projects on the same cluster.

    </div>

    1.  Go to **Ecosystem** → **Installed Operators**.

    2.  Select **TempoStack** → **Create TempoStack** → **YAML view**.

    3.  In the **YAML view**, customize the `TempoStack` custom resource (CR):

        <div class="formalpara-title">

        **Example `TempoStack` CR for AWS S3 and MinIO storage and two tenants**

        </div>

        ``` yaml
        apiVersion: tempo.grafana.com/v1alpha1
        kind: TempoStack
        metadata:
          name: simplest
          namespace: <permitted_project_of_tempostack_instance>
        spec:
          storage:
            secret:
              name: <secret_name>
              type: <secret_provider>
          storageSize: <value>Gi
          resources:
            total:
              limits:
                memory: 2Gi
                cpu: 2000m
          tenants:
            mode: openshift
            authentication:
              - tenantName: dev
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfa"
              - tenantName: prod
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfb"
          template:
            gateway:
              enabled: true
            queryFrontend:
              jaegerQuery:
                enabled: true
        ```

        - This CR creates a `TempoStack` deployment, which is configured to receive Jaeger Thrift over the HTTP and OpenTelemetry Protocol (OTLP).

        - The project that you have chosen for the `TempoStack` deployment. Project names beginning with the `openshift-` prefix are not permitted.

        - Red Hat supports only the custom resource options that are available in the Red Hat OpenShift Distributed Tracing Platform documentation.

        - Specifies the storage for storing traces.

        - The secret you created in step 2 for the object storage that had been set up as one of the prerequisites.

        - The value of the `name` field in the `metadata` section of the secret. For example: `minio`.

        - The accepted values are `azure` for Azure Blob Storage; `gcs` for Google Cloud Storage; and `s3` for Amazon S3, MinIO, or Red Hat OpenShift Data Foundation. For example: `s3`.

        - The size of the persistent volume claim for the Tempo Write-Ahead Logging (WAL). The default is `10Gi`. For example: `1Gi`.

        - Optional.

        - The value must be `openshift`.

        - The list of tenants.

        - The tenant name, which is used as the value for the `X-Scope-OrgId` HTTP header.

        - The unique identifier of the tenant. Must be unique throughout the lifecycle of the `TempoStack` deployment. The Distributed Tracing Platform uses this ID to prefix objects in the object storage. You can reuse the value of the UUID or `tempoName` field.

        - Enables a gateway that performs authentication and authorization.

        - Exposes the Jaeger UI, which visualizes the data, via a route at `http://<gateway_ingress>/api/traces/v1/<tenant_name>/search`.

    4.  Select **Create**.

<!-- -->

1.  Use the **Project:** dropdown list to select the project of the `TempoStack` instance.

2.  Go to **Ecosystem** → **Installed Operators** to verify that the **Status** of the `TempoStack` instance is **Condition: Ready**.

3.  Go to **Workloads** → **Pods** to verify that all the component pods of the `TempoStack` instance are running.

4.  Access the Tempo console:

    1.  Go to **Networking** → **Routes** and <span class="keycombo">Ctrl+F</span> to search for `tempo`.

    2.  In the **Location** column, open the URL to access the Tempo console.

        <div class="note">

        The Tempo console initially shows no trace data following the Tempo console installation.

        </div>

## Installing a TempoStack instance by using the CLI

You can install a `TempoStack` instance from the command line.

- An active OpenShift CLI (`oc`) session by a cluster administrator with the `cluster-admin` role.

  <div class="tip">

  - Ensure that your OpenShift CLI (`oc`) version is up to date and matches your OpenShift Container Platform version.

  - Run the `oc login` command:

    ``` terminal
    $ oc login --username=<your_username>
    ```

  </div>

- You have completed setting up the required object storage by a supported provider: [Red Hat OpenShift Data Foundation](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation), [MinIO](https://min.io/), [Amazon S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), [Google Cloud Storage](https://cloud.google.com/storage/). For more information, see "Object storage setup".

  <div class="warning">

  Object storage is required and not included with the Distributed Tracing Platform. You must choose and set up object storage by a supported provider before installing the Distributed Tracing Platform.

  </div>

- You have defined one or more tenants and configured the read and write permissions. For more information, see "Configuring the read permissions for tenants" and "Configuring the write permissions for tenants".

  <div class="note">

  A `TempoStack` instance without configured tenants is not supported.

  </div>

1.  Run the following command to create a permitted project of your choice for the `TempoStack` instance that you will create in a subsequent step:

    ``` terminal
    $ oc apply -f - << EOF
    apiVersion: project.openshift.io/v1
    kind: Project
    metadata:
      name: <permitted_project_of_tempostack_instance>
    EOF
    ```

    - Project names beginning with the `openshift-` prefix are not permitted.

2.  In the project that you created for the `TempoStack` instance, create a secret for your object storage bucket by running the following command:

    ``` terminal
    $ oc apply -f - << EOF
    <object_storage_secret>
    EOF
    ```

    For more information, see "Object storage setup".

    <div class="formalpara-title">

    **Example secret for Amazon S3 and MinIO storage**

    </div>

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: minio-test
    stringData:
      endpoint: http://minio.minio.svc:9000
      bucket: tempo
      access_key_id: tempo
      access_key_secret: <secret>
    type: Opaque
    ```

3.  Create a `TempoStack` instance in the project that you created for it:

    <div class="note">

    You can create multiple `TempoStack` instances in separate projects on the same cluster.

    </div>

    1.  Customize the `TempoStack` custom resource (CR):

        <div class="formalpara-title">

        **Example `TempoStack` CR for AWS S3 and MinIO storage and two tenants**

        </div>

        ``` yaml
        apiVersion: tempo.grafana.com/v1alpha1
        kind: TempoStack
        metadata:
          name: simplest
          namespace: <permitted_project_of_tempostack_instance>
        spec:
          storage:
            secret:
              name: <secret_name>
              type: <secret_provider>
          storageSize: <value>Gi
          resources:
            total:
              limits:
                memory: 2Gi
                cpu: 2000m
          tenants:
            mode: openshift
            authentication:
              - tenantName: dev
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfa"
              - tenantName: prod
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfb"
          template:
            gateway:
              enabled: true
            queryFrontend:
              jaegerQuery:
                enabled: true
        ```

        - This CR creates a `TempoStack` deployment, which is configured to receive Jaeger Thrift over the HTTP and OpenTelemetry Protocol (OTLP).

        - The project that you have chosen for the `TempoStack` deployment. Project names beginning with the `openshift-` prefix are not permitted.

        - Red Hat supports only the custom resource options that are available in the Red Hat OpenShift Distributed Tracing Platform documentation.

        - Specifies the storage for storing traces.

        - The secret you created in step 2 for the object storage that had been set up as one of the prerequisites.

        - The value of the `name` field in the `metadata` section of the secret. For example: `minio`.

        - The accepted values are `azure` for Azure Blob Storage; `gcs` for Google Cloud Storage; and `s3` for Amazon S3, MinIO, or Red Hat OpenShift Data Foundation. For example: `s3`.

        - The size of the persistent volume claim for the Tempo Write-Ahead Logging (WAL). The default is `10Gi`. For example: `1Gi`.

        - Optional.

        - The value must be `openshift`.

        - The list of tenants.

        - The tenant name, which is used as the value for the `X-Scope-OrgId` HTTP header.

        - The unique identifier of the tenant. Must be unique throughout the lifecycle of the `TempoStack` deployment. The Distributed Tracing Platform uses this ID to prefix objects in the object storage. You can reuse the value of the UUID or `tempoName` field.

        - Enables a gateway that performs authentication and authorization.

        - Exposes the Jaeger UI, which visualizes the data, via a route at `http://<gateway_ingress>/api/traces/v1/<tenant_name>/search`.

    2.  Apply the customized CR by running the following command:

        ``` terminal
        $ oc apply -f - << EOF
        <tempostack_cr>
        EOF
        ```

<!-- -->

1.  Verify that the `status` of all `TempoStack` `components` is `Running` and the `conditions` are `type: Ready` by running the following command:

    ``` terminal
    $ oc get tempostacks.tempo.grafana.com simplest -o yaml
    ```

2.  Verify that all the `TempoStack` component pods are running by running the following command:

    ``` terminal
    $ oc get pods
    ```

3.  Access the Tempo console:

    1.  Query the route details by running the following command:

        ``` terminal
        $ oc get route
        ```

    2.  Open `https://<route_from_previous_step>` in a web browser.

        <div class="note">

        The Tempo console initially shows no trace data following the Tempo console installation.

        </div>

# Installing a TempoMonolithic instance

<div class="important">

The `TempoMonolithic` instance is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

You can install a `TempoMonolithic` instance by using the web console or command line.

The `TempoMonolithic` custom resource (CR) creates a Tempo deployment in monolithic mode. The TempoMonolithic deployment contains all Tempo components, such as the compactor, distributor, ingester, querier, and query frontend, in a single container.

A `TempoMonolithic` instance supports storing traces in in-memory storage, a persistent volume, or object storage.

Opt for Tempo deployment in monolithic mode for small deployments, demonstrations, and testing.

<div class="note">

The monolithic deployment of Tempo does not scale horizontally. If you require horizontal scaling, use the `TempoStack` CR for a Tempo deployment in microservices mode.

</div>

## Installing a TempoMonolithic instance by using the web console

<div class="important">

The `TempoMonolithic` instance is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

You can install a `TempoMonolithic` instance from the **Administrator** view of the web console.

- You are logged in to the OpenShift Container Platform web console as a cluster administrator with the `cluster-admin` role.

- For Red Hat OpenShift Dedicated, you must be logged in using an account with the `dedicated-admin` role.

- You have defined one or more tenants and configured the read and write permissions. For more information, see "Configuring the read permissions for tenants" and "Configuring the write permissions for tenants".

  <div class="note">

  A `TempoMonolithic` instance without configured tenants is not supported.

  </div>

1.  Go to **Home** → **Projects** → **Create Project** to create a permitted project of your choice for the `TempoMonolithic` instance that you will create in a subsequent step. Project names beginning with the `openshift-` prefix are not permitted.

2.  Decide which type of supported storage to use for storing traces: in-memory storage, a persistent volume, or object storage.

    <div class="important">

    Object storage is not included with the Distributed Tracing Platform and requires setting up an object store by a supported provider: [Red Hat OpenShift Data Foundation](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation), [MinIO](https://min.io/), [Amazon S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), or [Google Cloud Storage](https://cloud.google.com/storage/).

    Additionally, opting for object storage requires creating a secret for your object storage bucket in the project that you created for the `TempoMonolithic` instance. You can do this in **Workloads** → **Secrets** → **Create** → **From YAML**.

    For more information, see "Object storage setup".

    <div class="formalpara-title">

    **Example secret for Amazon S3 and MinIO storage**

    </div>

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: minio-test
    stringData:
      endpoint: http://minio.minio.svc:9000
      bucket: tempo
      access_key_id: tempo
      access_key_secret: <secret>
    type: Opaque
    ```

    </div>

3.  Create a `TempoMonolithic` instance:

    <div class="note">

    You can create multiple `TempoMonolithic` instances in separate projects on the same cluster.

    </div>

    1.  Go to **Ecosystem** → **Installed Operators**.

    2.  Select **TempoMonolithic** → **Create TempoMonolithic** → **YAML view**.

    3.  In the **YAML view**, customize the `TempoMonolithic` custom resource (CR).

        <div class="formalpara-title">

        **Example `TempoMonolithic` CR**

        </div>

        ``` yaml
        apiVersion: tempo.grafana.com/v1alpha1
        kind: TempoMonolithic
        metadata:
          name: <metadata_name>
          namespace: <permitted_project_of_tempomonolithic_instance>
        spec:
          storage:
            traces:
              backend: <supported_storage_type>
              size: <value>Gi
              s3:
                secret: <secret_name>
            tls:
              enabled: true
              caName: <ca_certificate_configmap_name>
          jaegerui:
            enabled: true
            route:
              enabled: true
          resources:
            total:
              limits:
                memory: <value>Gi
                cpu: <value>m
          multitenancy:
            enabled: true
            mode: openshift
            authentication:
              - tenantName: dev
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfa"
              - tenantName: prod
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfb"
        ```

        - This CR creates a `TempoMonolithic` deployment with trace ingestion in the OTLP protocol.

        - The project that you have chosen for the `TempoMonolithic` deployment. Project names beginning with the `openshift-` prefix are not permitted.

        - Red Hat supports only the custom resource options that are available in the Red Hat OpenShift Distributed Tracing Platform documentation.

        - Specifies the storage for storing traces.

        - Type of storage for storing traces: in-memory storage, a persistent volume, or object storage. The value for a persistent volume is `pv`. The accepted values for object storage are `s3`, `gcs`, or `azure`, depending on the used object store type. The default value is `memory` for the `tmpfs` in-memory storage, which is only appropriate for development, testing, demonstrations, and proof-of-concept environments because the data does not persist when the pod is shut down.

        - Memory size: For in-memory storage, this means the size of the `tmpfs` volume, where the default is `2Gi`. For a persistent volume, this means the size of the persistent volume claim, where the default is `10Gi`. For object storage, this means the size of the persistent volume claim for the Tempo Write-Ahead Logging (WAL), where the default is `10Gi`.

        - Optional: For object storage, the type of object storage. The accepted values are `s3`, `gcs`, and `azure`, depending on the used object store type.

        - Optional: For object storage, the value of the `name` in the `metadata` of the storage secret. The storage secret must be in the same namespace as the `TempoMonolithic` instance and contain the fields specified in "Table 1. Required secret parameters" in the section "Object storage setup".

        - Optional.

        - Optional: Name of a `ConfigMap` object that contains a CA certificate.

        - Exposes the Jaeger UI, which visualizes the data, via a route at `http://<gateway_ingress>/api/traces/v1/<tenant_name>/search`.

        - Enables creation of the route for the Jaeger UI.

        - Optional.

        - Lists the tenants.

        - The tenant name, which is used as the value for the `X-Scope-OrgId` HTTP header.

        - The unique identifier of the tenant. Must be unique throughout the lifecycle of the `TempoMonolithic` deployment. This ID will be added as a prefix to the objects in the object storage. You can reuse the value of the UUID or `tempoName` field.

    4.  Select **Create**.

<!-- -->

1.  Use the **Project:** dropdown list to select the project of the `TempoMonolithic` instance.

2.  Go to **Ecosystem** → **Installed Operators** to verify that the **Status** of the `TempoMonolithic` instance is **Condition: Ready**.

3.  Go to **Workloads** → **Pods** to verify that the pod of the `TempoMonolithic` instance is running.

4.  Access the Jaeger UI:

    1.  Go to **Networking** → **Routes** and <span class="keycombo">Ctrl+F</span> to search for `jaegerui`.

        <div class="note">

        The Jaeger UI uses the `tempo-<metadata_name_of_TempoMonolithic_CR>-jaegerui` route.

        </div>

    2.  In the **Location** column, open the URL to access the Jaeger UI.

5.  When the pod of the `TempoMonolithic` instance is ready, you can send traces to the `tempo-<metadata_name_of_TempoMonolithic_CR>:4317` (OTLP/gRPC) and `tempo-<metadata_name_of_TempoMonolithic_CR>:4318` (OTLP/HTTP) endpoints inside the cluster.

    The Tempo API is available at the `tempo-<metadata_name_of_TempoMonolithic_CR>:3200` endpoint inside the cluster.

## Installing a TempoMonolithic instance by using the CLI

<div class="important">

The `TempoMonolithic` instance is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

You can install a `TempoMonolithic` instance from the command line.

- An active OpenShift CLI (`oc`) session by a cluster administrator with the `cluster-admin` role.

  <div class="tip">

  - Ensure that your OpenShift CLI (`oc`) version is up to date and matches your OpenShift Container Platform version.

  - Run the `oc login` command:

    ``` terminal
    $ oc login --username=<your_username>
    ```

  </div>

- You have defined one or more tenants and configured the read and write permissions. For more information, see "Configuring the read permissions for tenants" and "Configuring the write permissions for tenants".

  <div class="note">

  A `TempoMonolithic` instance without configured tenants is not supported.

  </div>

1.  Run the following command to create a permitted project of your choice for the `TempoMonolithic` instance that you will create in a subsequent step:

    ``` terminal
    $ oc apply -f - << EOF
    apiVersion: project.openshift.io/v1
    kind: Project
    metadata:
      name: <permitted_project_of_tempomonolithic_instance>
    EOF
    ```

    - Project names beginning with the `openshift-` prefix are not permitted.

2.  Decide which type of supported storage to use for storing traces: in-memory storage, a persistent volume, or object storage.

    <div class="important">

    Object storage is not included with the Distributed Tracing Platform and requires setting up an object store by a supported provider: [Red Hat OpenShift Data Foundation](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation), [MinIO](https://min.io/), [Amazon S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/), or [Google Cloud Storage](https://cloud.google.com/storage/).

    Additionally, opting for object storage requires creating a secret for your object storage bucket in the project that you created for the `TempoMonolithic` instance. You can do this by running the following command:

    ``` terminal
    $ oc apply -f - << EOF
    <object_storage_secret>
    EOF
    ```

    For more information, see "Object storage setup".

    <div class="formalpara-title">

    **Example secret for Amazon S3 and MinIO storage**

    </div>

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: minio-test
    stringData:
      endpoint: http://minio.minio.svc:9000
      bucket: tempo
      access_key_id: tempo
      access_key_secret: <secret>
    type: Opaque
    ```

    </div>

3.  Create a `TempoMonolithic` instance in the project that you created for it.

    <div class="tip">

    You can create multiple `TempoMonolithic` instances in separate projects on the same cluster.

    </div>

    1.  Customize the `TempoMonolithic` custom resource (CR).

        <div class="formalpara-title">

        **Example `TempoMonolithic` CR**

        </div>

        ``` yaml
        apiVersion: tempo.grafana.com/v1alpha1
        kind: TempoMonolithic
        metadata:
          name: <metadata_name>
          namespace: <permitted_project_of_tempomonolithic_instance>
        spec:
          storage:
            traces:
              backend: <supported_storage_type>
              size: <value>Gi
              s3:
                secret: <secret_name>
            tls:
              enabled: true
              caName: <ca_certificate_configmap_name>
          jaegerui:
            enabled: true
            route:
              enabled: true
          resources:
            total:
              limits:
                memory: <value>Gi
                cpu: <value>m
          multitenancy:
            enabled: true
            mode: openshift
            authentication:
              - tenantName: dev
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfa"
              - tenantName: prod
                tenantId: "1610b0c3-c509-4592-a256-a1871353dbfb"
        ```

        - This CR creates a `TempoMonolithic` deployment with trace ingestion in the OTLP protocol.

        - The project that you have chosen for the `TempoMonolithic` deployment. Project names beginning with the `openshift-` prefix are not permitted.

        - Red Hat supports only the custom resource options that are available in the Red Hat OpenShift Distributed Tracing Platform documentation.

        - Specifies the storage for storing traces.

        - Type of storage for storing traces: in-memory storage, a persistent volume, or object storage. The value for a persistent volume is `pv`. The accepted values for object storage are `s3`, `gcs`, or `azure`, depending on the used object store type. The default value is `memory` for the `tmpfs` in-memory storage, which is only appropriate for development, testing, demonstrations, and proof-of-concept environments because the data does not persist when the pod is shut down.

        - Memory size: For in-memory storage, this means the size of the `tmpfs` volume, where the default is `2Gi`. For a persistent volume, this means the size of the persistent volume claim, where the default is `10Gi`. For object storage, this means the size of the persistent volume claim for the Tempo Write-Ahead Logging (WAL), where the default is `10Gi`.

        - Optional: For object storage, the type of object storage. The accepted values are `s3`, `gcs`, and `azure`, depending on the used object store type.

        - Optional: For object storage, the value of the `name` in the `metadata` of the storage secret. The storage secret must be in the same namespace as the `TempoMonolithic` instance and contain the fields specified in "Table 1. Required secret parameters" in the section "Object storage setup".

        - Optional.

        - Optional: Name of a `ConfigMap` object that contains a CA certificate.

        - Exposes the Jaeger UI, which visualizes the data, via a route at `http://<gateway_ingress>/api/traces/v1/<tenant_name>/search`.

        - Enables creation of the route for the Jaeger UI.

        - Optional.

        - Lists the tenants.

        - The tenant name, which is used as the value for the `X-Scope-OrgId` HTTP header.

        - The unique identifier of the tenant. Must be unique throughout the lifecycle of the `TempoMonolithic` deployment. This ID will be added as a prefix to the objects in the object storage. You can reuse the value of the UUID or `tempoName` field.

    2.  Apply the customized CR by running the following command:

        ``` terminal
        $ oc apply -f - << EOF
        <tempomonolithic_cr>
        EOF
        ```

<!-- -->

1.  Verify that the `status` of all `TempoMonolithic` `components` is `Running` and the `conditions` are `type: Ready` by running the following command:

    ``` terminal
    $ oc get tempomonolithic.tempo.grafana.com <metadata_name_of_tempomonolithic_cr> -o yaml
    ```

2.  Run the following command to verify that the pod of the `TempoMonolithic` instance is running:

    ``` terminal
    $ oc get pods
    ```

3.  Access the Jaeger UI:

    1.  Query the route details for the `tempo-<metadata_name_of_tempomonolithic_cr>-jaegerui` route by running the following command:

        ``` terminal
        $ oc get route
        ```

    2.  Open `https://<route_from_previous_step>` in a web browser.

4.  When the pod of the `TempoMonolithic` instance is ready, you can send traces to the `tempo-<metadata_name_of_tempomonolithic_cr>:4317` (OTLP/gRPC) and `tempo-<metadata_name_of_tempomonolithic_cr>:4318` (OTLP/HTTP) endpoints inside the cluster.

    The Tempo API is available at the `tempo-<metadata_name_of_tempomonolithic_cr>:3200` endpoint inside the cluster.

# Network policies

The Tempo Operator applies network policies by default.

| Network Policy                                          | Description                                                                                                                                                                                                                                                                                                          |
|---------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<tempostack_metadata_name>-allow-dns`                  | Allows egress DNS queries to the `openshift-dns` DNS service on DNS port 5353.                                                                                                                                                                                                                                       |
| `<tempostack_metadata_name>-compactor`                  | Compactor egress to S3-compatible object storage. There is no port restriction. This network policy grants unrestricted egress traffic to pods labeled as the Tempo compactor, allowing them to initiate connections to any IP address, such as `0.0.0.0/0`, or any namespace, as the object storage ports can vary. |
| `<tempostack_metadata_name>-distributor`                | Distributor ingress and egress rules for trace ingestion and communication with ingesters.                                                                                                                                                                                                                           |
| `<tempostack_metadata_name>-gossip`                     | Inter-component gossip protocol communication on ports 7946, 3200, and 3101.                                                                                                                                                                                                                                         |
| `<tempostack_metadata_name>-ingester`                   | Ingester ingress and egress rules for receiving traces from distributors and serving queriers.                                                                                                                                                                                                                       |
| `<tempostack_metadata_name>-querier`                    | Querier ingress and egress rules for communication with ingesters, query frontend, and object storage.                                                                                                                                                                                                               |
| `<tempostack_metadata_name>-query-frontend`             | Query frontend ingress and egress rules for serving queries and communicating with queriers.                                                                                                                                                                                                                         |
| `<tempostack_metadata_name>-ingress-to-operand-metrics` | Allows OpenShift cluster monitoring to scrape metrics on port 3200.                                                                                                                                                                                                                                                  |

Default network policies

<div class="tip">

You can manually disable these network policies in the `TempoStack` custom resource as follows:

``` yaml
apiVersion: tempo.grafana.com/v1alpha1
kind: TempoStack
metadata:
  name: example
spec:
  networkPolicy:
    enabled: false
```

- Disables the default network policies. The default value is `true`.

</div>

# Additional resources

- [Creating a cluster admin](../../post_installation_configuration/preparing-for-users.xml#creating-cluster-admin_post-install-preparing-for-users)

- [OperatorHub.io](https://operatorhub.io/)

- [Accessing the web console](../../web_console/web-console.xml#web-console)

- [Installing from the software catalog using the web console](../../operators/admin/olm-adding-operators-to-cluster.xml#olm-installing-from-software-catalog-using-web-console_olm-adding-operators-to-a-cluster)

- [Creating applications from installed Operators](../../operators/user/olm-creating-apps-from-installed-operators.xml#olm-creating-apps-from-installed-operators)

- [Getting started with the OpenShift CLI](../../cli_reference/openshift_cli/getting-started-cli.xml#getting-started-cli)
