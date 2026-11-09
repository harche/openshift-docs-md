With hosted control planes on Microsoft Azure, you can reduce the cost associated with dedicated control-plane node VMs for each cluster. You can provision compute nodes as Azure Virtual Machine Scale sets for dynamic scaling, and ensure credential isolation with per-cluster Azure service principals.

# Overview of hosted control planes on Azure

You can deploy and manage hosted clusters on an OpenShift management cluster that runs in Microsoft Azure. With a self-managed deployment model, you manage your own OpenShift cluster.

## Architecture of hosted control planes on Azure

At a high level, the architecture of hosted control planes on Azure consists of three layers:

Management cluster
An Azure OpenShift cluster that hosts the HyperShift Operator and the control planes for your hosted clusters.

Control plane
Kubernetes control-plane components that run as pods on the management cluster.

Data plane
Compute nodes that run as Azure virtual machines (VMs) in your Azure subscription.

The architecture uses Azure Workload Identity for secure, credential-free authentication between OpenShift Container Platform components and Azure services. As a result, you do not need to manage long-lived service principal credentials, and you get better security through federated identity credentials.

## Deployment workflow for hosted control planes on Azure

Deploying self-managed hosted control planes on Azure involves a three-phase process in the following order:

Phase 1: Set up Azure Workload Identity
This phase establishes secure authentication infrastructure so that OpenShift Container Platform components can access Azure services. During this phase, the security infrastructure that your hosted clusters require is created:

- Managed identities for each OpenShift Container Platform component, including the image registry, ingress, CSI drivers, cloud provider, network operator, and so on

- OIDC issuer in Azure Blob Storage for service account token validation

- Federated credentials that establish trust relationships between Azure Entra ID and OpenShift Container Platform service accounts

Phase 2: Set up the management cluster
In this phase, you prepare your OpenShift Container Platform management cluster on Azure to host and manage hosted clusters. During this phase, you install the following components:

- Azure DNS zones, for private and public-private topologies

- External DNS, for private and public-private topologies

- HyperShift Operator

Phase 3: Create hosted clusters
In this phase, you create and configure hosted clusters. This phase involves the following steps:

1.  Setting up infrastructure

2.  Creating a hosted cluster

3.  Integrating workload identity

4.  Configuring private endpoint access (optional)

<div>

<div class="title">

Additional resources

</div>

- [Azure Workload Identity documentation](https://azure.github.io/azure-workload-identity/docs/)

</div>

## Azure infrastructure and credentials

Before you get started with hosted control planes on Microsoft Azure, get familiar with the required Azure resources and the necessary permissions.

### Summary of requirements

You need the following resources, tools, access, and permissions to set up hosted control planes on Azure:

Azure resources
- An OpenShift Container Platform management cluster on Azure.

- An Azure subscription with contributor and user-access administrator permissions.

- (Optional) A parent DNS zone in Azure for delegating cluster DNS records. This DNS zone is required only if you plan to use external DNS.

Tools and access
- Azure command-line interface (CLI), `az`, configured with your subscription

- OpenShift CLI (`oc`)

- hosted control planes CLI, `hcp`

- `jq` command-line JSON processor

- Cloud Credential Operator utility (`ccoctl`)

- A valid OpenShift Container Platform pull secret

Permissions
- Subscription-level contributor and user access administrator roles

- Microsoft Graph API permissions for creating service principals

### DNS management options

You can set up hosted control planes on Azure with or without external DNS. If you plan to use a private or a public-private topology, external DNS is required. See the following table for more information:

|  | With external DNS | Without external DNS |
|----|----|----|
| **Best for** | Production, multi-cluster | Development, testing |
| **API server DNS** | Custom (`api-cluster.example.com`) | Azure Load Balancer (`abc123.region.cloudapp.azure.com`) |
| **Setup complexity** | Low, requires DNS zones and service principals | None |
| **Management** | Fully automatic | Manual or Azure-provided |

DNS approaches for hosted control planes on Azure

### Resource group strategy

Cluster-specific resource groups are created and deleted with each hosted cluster. These resources include managed resource groups for cluster infrastructure. If you use custom networking, these resources also include Virtual Network (VNet) resource groups and Network Security Group (NSG) resource groups.

### Security considerations for hosted control planes on Azure

Hosted control planes on Azure employs the following security best practices:

- Workload identity federation, which eliminates long-lived credentials by using OIDC-based authentication.

- Least-privilege access, where each component has its own managed identity with minimal required permissions.

- Network isolation, where you can use custom VNets and NSGs to implement network segmentation and security policies.

- Federated credentials, where trust relationships are scoped to specific service accounts, preventing unauthorized access.

- Private connectivity, available as an option through Azure Private Link, which provides private API server access to ensure that control-plane traffic never traverses the public internet. Private connectivity is available for private and public-private topologies only.

# Setting up Azure resources

Before you can create management and hosted clusters for your deployment of hosted control planes on Azure, you need to set up an OIDC issuer, Workload Identities, and your Azure infrastructure.

## Setting up an OIDC issuer

To prepare to deploy hosted control planes on Azure, you need to set up an OIDC issuer for hosted clusters.

<div>

<div class="title">

Prerequisites

</div>

- The Azure command-line interface (CLI) is installed and configured.

- The `jq` command-line JSON processor is installed.

- The Cloud Credential Operator utility (`ccoctl`) is installed. For more information, see "How to obtain the ccoctl tool for OpenShift 4".

- The appropriate Azure permissions are set.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Set your environment variables as shown in the following example:

    ``` terminal
    PERSISTENT_RG_NAME="os4-common"
    LOCATION="eastus"
    AZURE_CREDS="/path/to/azure-creds.json"
    SUBSCRIPTION_ID="my-subscription-id"
    ```

2.  Create a persistent resource group by entering the following command:

    ``` terminal
    $ az group create --name $PERSISTENT_RG_NAME --location $LOCATION
    ```

3.  Configure an OIDC issuer URL by using the Cloud Credential Operator tool to complete the following steps:

    1.  Set the OIDC issuer variables as shown in the following example:

        ``` terminal
        OIDC_STORAGE_ACCOUNT_NAME="yourstorageaccount"
        TENANT_ID="your-tenant-id"
        ```

    2.  Create an RSA key pair and save the private and public key by entering the following command:

        ``` terminal
        $ ccoctl azure create-key-pair
        ```

    3.  Set variables for the token issuer key paths as shown in the following example:

        ``` terminal
        SA_TOKEN_ISSUER_PRIVATE_KEY_PATH="/path/to/serviceaccount-signer.private"
        SA_TOKEN_ISSUER_PUBLIC_KEY_PATH="/path/to/serviceaccount-signer.public"
        ```

    4.  Create an OIDC issuer by entering the following command:

        ``` terminal
        $ ccoctl azure create-oidc-issuer \
            --oidc-resource-group-name ${PERSISTENT_RG_NAME} \
            --tenant-id ${TENANT_ID} \
            --region ${LOCATION} \
            --name ${OIDC_STORAGE_ACCOUNT_NAME} \
            --subscription-id ${SUBSCRIPTION_ID} \
            --public-key-file ${SA_TOKEN_ISSUER_PUBLIC_KEY_PATH}
        ```

    5.  Set the OIDC issuer URL as shown in the following example:

        ``` terminal
        OIDC_ISSUER_URL="https://${OIDC_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/${OIDC_STORAGE_ACCOUNT_NAME}"
        ```

</div>

<div>

<div class="title">

Verification

</div>

- Try to access the OIDC issuer by entering the following command:

  ``` terminal
  $ curl -s "${OIDC_ISSUER_URL}/.well-known/openid-configuration" | jq .
  ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [How to obtain the ccoctl tool for OpenShift 4 (Red Hat Knowledgebase article)](https://access.redhat.com/solutions/7001811)

</div>

## Creating Azure Workload Identities

To ensure control over Identity and Access Management (IAM) resources in your Azure deployment, create Workload Identities separately from your infrastructure.

Workload Identities authenticate hosted cluster components to Azure services by using OIDC federation. You must create identities separately and then consume them during infrastructure or cluster creation.

<div>

<div class="title">

Prerequisites

</div>

- You have an Azure credentials file in the following format:

  <div class="formalpara">

  <div class="title">

  Example file

  </div>

  ``` terminal
  {
    "subscriptionId": "your-subscription-id",
    "tenantId": "your-tenant-id",
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret"
  }
  ```

  </div>

- You have a resource group to create the managed identities in.

- You have an OIDC issuer URL for Workload Identity federation. For more information, see "Setting up an OIDC issuer".

</div>

<div>

<div class="title">

Procedure

</div>

1.  Set environment variables as shown in the following example:

    ``` terminal
    CLUSTER_NAME="my-self-managed-cluster"
    INFRA_ID="${CLUSTER_NAME}-$(openssl rand -hex 4)"
    ```

2.  On the hosted control planes command-line interface, `hcp`, enter the following command:

    ``` terminal
    $ hcp create iam azure \
        --name <my_cluster_name> \
        --infra-id <infra_id> \
        --azure-creds <azure_credentials_file> \
        --resource-group-name <resource_group> \
        --oidc-issuer-url <oidc_issuer_url> \
        --output-file <workload_identities_file> \
        --location <my_region> \
        --cloud <my_cloud_environment>
    ```

    where:

    `<my_cluster_name>`
    Specifies the name of the cluster you intend to create.

    `<infra_id>`
    Specifies the unique identifier for naming Azure resources. Typically, this identifier is the cluster name with a suffix.

    `<azure_credentials_file>`
    Specifies the Azure credentials file with permission to create managed identities and federated credentials.

    `<resource_group>`
    Specifies the name of the resource group where you intend to create identities.

    `<oidc_issuer_url>`
    Specifies the URL of the OIDC identity provider for Workload Identity federation.

    `<workload_identities_file>`
    Specifies the output file path, such as `my-cluster-name-iam-output.json`.

    You can also add these optional flags to the `hcp create iam azure` command:

    `<my_region>`
    Specifies the Azure region for the managed identities. The default value is `eastus`.

    `<my_cloud_environment>`
    Specifies the Azure cloud environment. The default value is `AzurePublicCloud`.

</div>

<div>

<div class="title">

Verification

</div>

- Review the output file, which looks like the following example:

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  {
    "disk": {
      "tenantID": "...",
      "clientID": "...",
      "resourceID": "/subscriptions/.../providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-cluster-abc123-disk"
    },
    "file": {
      "tenantID": "...",
      "clientID": "...",
      "resourceID": "..."
    },
    "imageRegistry": { ... },
    "ingress": { ... },
    "cloudProvider": { ... },
    "nodePoolManagement": { ... },
    "network": { ... },
    "controlPlaneOperator": { ... }
  }
  ```

  </div>

  The output includes 8 user-assigned identities, one per cluster component, along with federated credentials for each identity:

  - Disk CSI driver

  - File CSI driver

  - Image registry

  - Ingress Operator

  - Cloud provider

  - Node pool management

  - Network Operator

  - Control Plane Operator

</div>

## Creating Azure infrastructure

Create an Azure infrastructure separately so that when you create a hosted cluster on Azure, you can use pre-existing infrastructure.

<div>

<div class="title">

Prerequisites

</div>

- You have an Azure credentials file with the following format:

  ``` json
  {
    "subscriptionId": "<my_subscription_id>",
    "tenantId": "<my_tenant_id>",
    "clientId": "<my_client_id>",
    "clientSecret": "<my_client_secret>"
  }
  ```

- You have an existing public DNS zone in your Azure subscription for your base domain.

- You created Workload Identities. For more information, see "Creating Azure Workload Identities".

</div>

<div>

<div class="title">

Procedure

</div>

- To create the infrastructure with a new virtual network, subnet, and network security group, enter the following command:

  ``` terminal
  $ hcp create infra azure \
    --name <my_cluster_name> \
    --infra-id <infra_id> \
    --azure-creds <azure_credentials_file> \
    --base-domain <base_domain> \
    --location <location> \
    --workload-identities-file <workload_identities_file> \
    --assign-identity-roles \
    --dns-zone-rg-name <dns_zone_rg> \
    --output-file <output_infra_file>
  ```

  where:

  - `--name` specifies the name of the hosted cluster you intend to create.

  - `--infra-id` specifies a unique name that identifies your infrastructure. This value is used to name and tag Azure resources. Typically, it is the name of your cluster with a suffix appended to it.

  - `--azure-creds` specifies an Azure credentials file that has permission to create infrastructure resources, such as virtual networks, subnets, and load balancers.

  - `--base-domain` specifies the base domain for the ingress of your hosted cluster. The base domain must correspond to an existing public DNS zone in your Azure subscription.

  - `--location` specifies the Azure region where you want to create the infrastructure, such as `eastus` or `westus2`.

  - `--workload-identities-file` specifies the path to the JSON file that contains the Workload Identity configuration.

  - `--assign-identity-roles` specifies that automatic RBAC role assignment is enabled for Workload Identities.

  - `--dns-zone-rg-name` specifies the name of the resource group that contains your public DNS zone.

  - `--output-file` specifies the file where the details of the infrastructure are stored in YAML format.

- To create the infrastructure with an existing virtual network, subnet, and network security group, enter the following command:

  ``` terminal
  $ hcp create infra azure \
    --name <my_cluster_name> \
    --infra-id <infra_id> \
    --azure-creds <azure_credentials_file> \
    --base-domain <base_domain> \
    --location <location> \
    --workload-identities-file <workload_identities_file> \
    --vnet-id /subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Network/virtualNetworks/<vnet_name> \
    --subnet-id /subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Network/virtualNetworks/<vnet_name>/subnets/<subnet_name> \
    --network-security-group-id /subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Network/networkSecurityGroups/<network_security_group_name> \
    --assign-identity-roles \
    --dns-zone-rg-name <dns_zone_rg> \
    --output-file <output_infra_file>
  ```

  where:

  - `--name` specifies the name of the hosted cluster you intend to create.

  - `--infra-id` specifies a unique name that identifies your infrastructure. This value is used to name and tag Azure resources. Typically, it is the name of your cluster with a suffix appended to it.

  - `--azure-creds` specifies an Azure credentials file that has permission to create infrastructure resources, such as virtual networks, subnets, and load balancers.

  - `--base-domain` specifies the base domain for the ingress of your hosted cluster. The base domain must correspond to an existing public DNS zone in your Azure subscription.

  - `--location` specifies the Azure region where you want to create the infrastructure, such as `eastus` or `westus2`.

  - `--workload-identities-file` specifies the path to the JSON file that contains the Workload Identity configuration.

  - `--vnet-id` specifies your existing virtual network ID, which includes your subscription ID and your virtual network name.

  - `--subnet-id` specifies the ARM resource ID of your subnet, which includes your subscription ID, virtual network name, and subnet name.

  - `--network-security-group-id` specifies your existing network security group ID, which includes your subscription ID and your network security group name.

  - `--assign-identity-roles` specifies that automatic RBAC role assignment is enabled for Workload Identities.

  - `--dns-zone-rg-name` specifies the name of the resource group that contains your public DNS zone.

  - `--output-file` specifies the file where the details of the infrastructure are stored in YAML format.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Creating Azure Workload Identities](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-workload-id_hcp-deploy-azure)

</div>

# Configuring an Azure management cluster for hosted control planes

To configure the management cluster for hosted control planes on Azure, you need to ensure that external DNS and the HyperShift Operator are set up on the cluster.

The configuration steps include configuring the DNS zone, delegating the DNS records for your cluster, and creating a dedicated service principal for external DNS.

<div>

<div class="title">

Prerequisites

</div>

- You installed the multicluster engine Operator 2.5 or later on an OpenShift Container Platform cluster. You can install multicluster engine Operator as an Operator from the OpenShift Container Platform software catalog. Or, if you already use Red Hat Advanced Cluster Management, the Operator is automatically installed. The HyperShift Operator is enabled by default in the operator package for multicluster engine Operator.

- The Azure command-line interface (CLI) is installed and configured.

- The OpenShift CLI (`oc`) is installed.

- You have an OpenShift Container Platform management cluster on Azure.

- If you are using external DNS, the `jq` command-line JSON processor is installed.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Set the DNS configuration variables as shown in the following example:

    ``` bash
    PARENT_DNS_RG="<my_parent_dns_resource_group>"
    PARENT_DNS_ZONE="<my_parent.dns.zone.com>"
    DNS_RECORD_NAME="<my_subdomain>"
    RESOURCE_GROUP_NAME="<my_resource_group>"
    DNS_ZONE_NAME="<my_subdomain.my_parent.dns.zone.com>"
    LOCATION="<my_region>"
    ```

2.  Create the Azure group by entering the following command:

    ``` terminal
    $ az group create \
      --name $RESOURCE_GROUP_NAME \
      --location $LOCATION
    ```

3.  Create the Azure DNS zone by entering the following command:

    ``` terminal
    $ az network dns zone create \
      --resource-group $RESOURCE_GROUP_NAME \
      --name $DNS_ZONE_NAME
    ```

4.  If an existing name server record exists, delete it by entering the following command:

    ``` terminal
    $ az network dns record-set ns delete \
      --resource-group $PARENT_DNS_RG \
      --zone-name $PARENT_DNS_ZONE \
      --name $DNS_RECORD_NAME -y
    ```

5.  Get the name servers from your DNS zone by entering the following command:

    ``` bash
    name_servers=$(az network dns zone show \
      --resource-group $RESOURCE_GROUP_NAME \
      --name $DNS_ZONE_NAME \
      --query nameServers \
      --output tsv)
    ```

6.  Create an array of name servers as shown in the following example:

    ``` bash
    ns_array=()
    while IFS= read -r ns; do
        ns_array+=("$ns")
    done <<< "$name_servers"
    ```

7.  Add name server records to the parent zone as shown in the following example:

    ``` bash
    for ns in "${ns_array[@]}"; do
        az network dns record-set ns add-record \
            --resource-group $PARENT_DNS_RG \
            --zone-name $PARENT_DNS_ZONE \
            --record-set-name $DNS_RECORD_NAME \
            --nsdname "$ns"
    done
    ```

8.  Set the external DNS configuration variables as shown in the following example:

    ``` bash
    EXTERNAL_DNS_NEW_SP_NAME="<external_dns_service_principal>"
    SERVICE_PRINCIPAL_FILEPATH="<path_to_azure_mgmt_json_file>"
    RESOURCE_GROUP_NAME="<my_resource_group>"
    ```

9.  Create the service principal for external DNS by entering the following command:

    ``` bash
    DNS_SP=$(az ad sp create-for-rbac --name ${EXTERNAL_DNS_NEW_SP_NAME})
    EXTERNAL_DNS_SP_APP_ID=$(echo "$DNS_SP" | jq -r '.appId')
    EXTERNAL_DNS_SP_PASSWORD=$(echo "$DNS_SP" | jq -r '.password')
    ```

10. Get the DNS zone ID by entering the following command:

    ``` bash
    DNS_ID=$(az network dns zone show \
      --name ${DNS_ZONE_NAME} \
      --resource-group ${RESOURCE_GROUP_NAME} \
      --query "id" \
      --output tsv)
    ```

11. Assign the `Reader` role to the service principal by entering the following command:

    ``` terminal
    $ az role assignment create \
      --role "Reader" \
      --assignee "${EXTERNAL_DNS_SP_APP_ID}" \
      --scope "${DNS_ID}"
    ```

12. Assign the `Contributor` role to the service principal by entering the following command:

    ``` terminal
    $ az role assignment create \
      --role "Contributor" \
      --assignee "${EXTERNAL_DNS_SP_APP_ID}" \
      --scope "${DNS_ID}"
    ```

13. Save the Azure credentials to a local file by entering the following command:

    ``` terminal
    $ cat > ${SERVICE_PRINCIPAL_FILEPATH} <<EOF
    {
      "tenantId": "$(az account show --query tenantId -o tsv)",
      "subscriptionId": "$(az account show --query id -o tsv)",
      "resourceGroup": "$RESOURCE_GROUP_NAME",
      "aadClientId": "$EXTERNAL_DNS_SP_APP_ID",
      "aadClientSecret": "$EXTERNAL_DNS_SP_PASSWORD"
    }
    EOF
    ```

14. If an existing Kubernetes secret for the Azure credentials exists, delete it by entering the following command:

    ``` terminal
    $ oc delete secret/azure-config-file --namespace "hypershift" || true
    ```

15. Create the Kubernetes secret for the Azure credentials by entering the following command:

    ``` terminal
    $ oc create secret generic azure-config-file \
      --namespace "hypershift" \
      --from-file=credentials=${SERVICE_PRINCIPAL_FILEPATH}
    ```

    The secret must be created in the `hypershift` namespace where the external DNS deployment runs. The `credentials` key name is required because the external DNS pod mounts the secret at `/etc/provider/credentials`.

16. Configure the HyperShift Operator to use external DNS by creating the following `ConfigMap` object:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: hypershift-operator-install-flags
      namespace: local-cluster
    data:
      installFlagsToAdd: "--external-dns-provider=azure --external-dns-secret=azure-config-file --external-dns-domain-filter=<dns_zone>"
      installFlagsToRemove: ""
    ```

    The `--external-dns-secret` flag specifies the name of the Kubernetes secret that contains the Azure credentials. The `data.installFlagsToAdd` parameter specifies the flags to pass to the Operator so it detects the DNS.

17. Apply the config map by entering the following command:

    ``` terminal
    $ oc apply -f hypershift-operator-install-flags.yaml
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Verify that both the HyperShift Operator and the external DNS are running by entering the following command:

  ``` terminal
  $ oc get pods -n hypershift
  ```

  <div class="formalpara">

  <div class="title">

  Example output

  </div>

  ``` terminal
  NAME                           READY   STATUS    RESTARTS   AGE
  external-dns-xxxxx-xxxxx       1/1     Running   0          1m
  operator-xxxxx-xxxxx           1/1     Running   0          1m
  ```

  </div>

</div>

# Creating a hosted cluster on Azure

Hosted clusters are where your applications run. Each hosted cluster has its own control plane that runs on the management cluster and a set of compute node virtual machines (VMs) in Azure.

The hosted cluster uses Workload Identities to securely access Azure services without storing credentials.

<div>

<div class="title">

Prerequisites

</div>

- You installed the Azure command-line interface (CLI).

- You installed the hosted control planes CLI, `hcp`.

- You installed the OpenShift CLI (`oc`).

- You installed the `jq` command-line JSON processor.

- You have a management cluster where the HyperShift Operator is installed and external DNS is configured.

- You set up Azure resources, including Workload Identities, an OIDC issuer, and infrastructure.

- You have the appropriate Azure permissions.

  - At the subscription level, you must have the `Contributor` role and the `User Access Administrator` role.

  - For Microsoft Graph API, you must have the `Application.ReadWrite.OwnedBy` permission.

</div>

<div>

<div class="title">

Procedure

</div>

- Create the `HostedCluster` custom resource by entering the following command:

  ``` terminal
  $ hcp create cluster azure \
    --name "$CLUSTER_NAME" \
    --infra-id "$INFRA_ID" \
    --azure-creds $AZURE_CREDS \
    --location ${LOCATION} \
    --node-pool-replicas 2 \
    --base-domain $BASE_DOMAIN \
    --pull-secret $PULL_SECRET \
    --generate-ssh \
    --release-image ${RELEASE_IMAGE} \
    --sa-token-issuer-private-key-path "${SA_TOKEN_ISSUER_PRIVATE_KEY_PATH}" \
    --oidc-issuer-url "${OIDC_ISSUER_URL}" \
    --dns-zone-rg-name ${PERSISTENT_RG_NAME} \
    --assign-service-principal-roles \
    --infra-json <output_infra_file> \
    --diagnostics-storage-account-type Managed \
    --disable-cluster-capabilities=<capability> \
    --enable-cluster-capabilities=<capability> \
    --external-dns-domain "${DNS_ZONE_NAME}"
  ```

  - For non-production environments, you can create a hosted cluster without external DNS by omitting the `--external-dns-domain` and `--assign-service-principal-roles` flags. In that case, the API server is accessible through an Azure load balancer hostname instead of a custom DNS name.

  - The `--disable-cluster-capabilities` flag is optional. Include it when you want to disable optional capabilities in your hosted cluster. For more information, see "Capabilities for hosted clusters".

  - The `--enable-cluster-capabilities` flag is optional. Include it when you want to enable optional capabilities in your hosted cluster. For more information, see "Capabilities for hosted clusters".

</div>

<div>

<div class="title">

Verification

</div>

1.  Check the cluster status by entering the following command:

    ``` terminal
    $ oc get hostedcluster $CLUSTER_NAME -n clusters
    ```

2.  Wait for the cluster to be complete by entering the following command:

    ``` terminal
    $ oc wait \
      --for=jsonpath='{.status.version.history[0].state}'=Completed \
      hostedcluster/$CLUSTER_NAME \
      -n clusters --timeout=20m
    ```

3.  Create the `kubeconfig` file for the cluster by entering the following command:

    ``` terminal
    $ hcp create kubeconfig \
      --name $CLUSTER_NAME > $CLUSTER_NAME-kubeconfig
    ```

4.  Get the `kubeconfig` file by entering the following command:

    ``` terminal
    $ export KUBECONFIG=$CLUSTER_NAME-kubeconfig
    ```

5.  Access the cluster nodes by entering the following command:

    ``` terminal
    $ oc get nodes
    ```

6.  Access the cluster by entering the following command:

    ``` terminal
    $ oc get clusterversion
    ```

</div>

# Capabilities for hosted clusters

To reduce resource consumption and prevent unnecessary Operators and operands from being deployed, administrators can enable or disable optional OpenShift Container Platform components when they create a hosted cluster.

When capabilities are not specified on a `HostedCluster` resource, the cluster uses the OpenShift Container Platform version’s `DefaultCapabilitySet` settings, excluding the `baremetal` capability. As a result, most optional components are enabled by default.

> [!IMPORTANT]
> Capabilities are immutable after cluster creation. You cannot change them after you create the `HostedCluster` resource.

## Capabilities that you can enable or disable for a hosted cluster

Familiarize yourself with the supported capabilities that you can enable or disable for a `HostedCluster` resource.

The capabilities are described in the following table:

| Capability | Description |
|----|----|
| `ImageRegistry` | The OpenShift Image Registry Operator and its operands, including cloud storage infrastructure, such as S3 buckets and Identity and Access Management (IAM) users. |
| `openshift-samples` | The OpenShift Samples Operator, which manages example `ImageStreams` and templates. |
| `Insights` | The Insights Operator, which collects and uploads cluster telemetry data. |
| `baremetal` | The Bare Metal Infrastructure Operator. This capability is excluded from the default set. If needed, you must explicitly enable it. |
| `Console` | The OpenShift Web Console Operator and its operands. |
| `NodeTuning` | The Node Tuning Operator, which manages node-level performance tuning by using TuneD and performance profiles. |
| `Ingress` | The OpenShift Ingress Operator, which manages the default router of the cluster. |

The following rules apply when you combine capability settings:

No overlap
A capability cannot be in both the `enabled` and `disabled` lists simultaneously.

Console requires Ingress
You can disable the `Ingress` capability only if the `Console` capability is also disabled because the console depends on Ingress.

Version requirement
You must use OpenShift Container Platform 4.20 or later to disable any of the following capabilities: `openshift-samples`, `Insights`, `Console`, `NodeTuning`, and `Ingress`. You can disable `ImageRegistry` and `baremetal` on versions earlier than 4.20.

Bare metal default exclusion
The `baremetal` capability is excluded from the default set. You can add it to the cluster by explicitly enabling it.

## Setting capabilities for a hosted cluster

To reduce unnecessary resource consumption, you can control which optional capabilities are enabled for a hosted cluster when you create the cluster.

> [!IMPORTANT]
> Capabilities are immutable after cluster creation. You cannot change them after you create the `HostedCluster` resource.

You can specify which capabilities are enabled by either using the `hcp` command-line interface (CLI) or by setting the `HostedCluster` manifest.

<div>

<div class="title">

Procedure

</div>

- To specify which capabilities are enabled in a hosted cluster by using the CLI, you can add the `--disable-cluster-capabilities` flag, the `--enable-cluster-capabilities` flag, or both. The following example shows how to disable the `ImageRegistry`, `Console`, and `Ingress` capabilities and enable the `baremetal` capability while you create a hosted cluster on AWS by using the `hcp` command-line interface:

  ``` terminal
  $ hcp create cluster aws \
      --name my-hosted-cluster \
      --disable-cluster-capabilities=ImageRegistry,Console,Ingress \
      --enable-cluster-capabilities=baremetal
  ```

  You can specify multiple capabilities as a comma-separated list. The supported values are as follows:

  - `ImageRegistry`

  - `openshift-samples`

  - `Insights`

  - `baremetal`

  - `Console`

  - `NodeTuning`

  - `Ingress`

- To specify which capabilities are enabled in a hosted cluster by using the `HostedCluster` manifest at cluster creation time, see the following examples:

  - To directly disable capabilities in a hosted cluster, add the `spec.capabilities.disabled` section in the `HostedCluster` resource:

    ``` yaml
    apiVersion: hypershift.openshift.io/v1beta1
    kind: HostedCluster
    metadata:
      name: my-hosted-cluster
      namespace: my-cluster-namespace
    spec:
      capabilities:
        disabled:
          - ImageRegistry
          - Console
          - Ingress
      # ...
    ```

  - To explicitly enable a capability that is not part of the default set of capabilities, such as the `baremetal` capability, see the following example:

    ``` yaml
    apiVersion: hypershift.openshift.io/v1beta1
    kind: HostedCluster
    metadata:
      name: my-hosted-cluster
      namespace: my-cluster-namespace
    spec:
      capabilities:
        enabled:
          - baremetal
      # ...
    ```

  - You can use both `enabled` and `disabled` if no capabilities are in both lists. See the following example:

    ``` yaml
    apiVersion: hypershift.openshift.io/v1beta1
    kind: HostedCluster
    metadata:
      name: my-hosted-cluster
      namespace: my-cluster-namespace
    spec:
      capabilities:
        enabled:
          - baremetal
        disabled:
          - ImageRegistry
          - openshift-samples
      # ...
    ```

</div>

# Private hosted clusters on Azure

By default, hosted clusters are accessible through public DNS and the default router of the management cluster. If you want communication between your compute nodes and the hosted control plane to be private, you can create hosted clusters that use Azure Private Link for communication.

Private endpoint access uses Azure Private Link to expose the internal load balancer of the hosted control plane to the Azure Virtual Network (VNet) of the hosted cluster. Compute nodes resolve the API server hostname by using private DNS zones that point to the private endpoint IP address.

## Preparing a subnet for a private hosted cluster on Azure

Azure Private Link requires a dedicated subnet for network address translator (NAT) IP address allocation. You can manually create the subnet, or it can be automatically created during cluster creation.

By manually creating the subnet, you have control over classless inter-domain routing (CIDR) allocation and naming. The following steps apply to manually creating the subnet. If you want the subnet to be automatically created, skip this procedure.

> [!NOTE]
> Azure Private Link, the NAT subnet, and the internal load balancer of the management cluster must all be in the same Azure region. Private Link is automatically created in the location where the hosted cluster is created. Azure rejects the creation of Private Link if the NAT subnet is in a different region.

<div>

<div class="title">

Prerequisites

</div>

- You have an OpenShift Container Platform management cluster on Azure. For more information, see "Configuring an Azure management cluster for hosted control planes".

- The Azure command-line interface (CLI) is installed and configured.

- The OpenShift CLI (`oc`) is installed.

- If you are using external DNS, the `jq` command-line JSON processor is installed.

- You configured an OIDC issuer. For more information, see "Setting up an OIDC issuer".

</div>

<div>

<div class="title">

Procedure

</div>

1.  Identify the Azure Virtual Network (VNet) of the management cluster.

    1.  Obtain the infrastructure resource group of the management cluster as shown in the following example:

        ``` bash
        $ MGMT_INFRA_RG=$(oc get infrastructure cluster -o jsonpath='{.status.platformStatus.azure.resourceGroupName}')
        ```

    2.  Find the VNet in the infrastructure resource group as shown in the following example:

        ``` bash
        $ MGMT_VNET_NAME=$(az network vnet list --resource-group "${MGMT_INFRA_RG}" --query "[0].name" -o tsv)
        ```

    3.  Set the environment variable for the VNet by entering the following command:

        ``` bash
        $ MGMT_VNET_RG="${MGMT_INFRA_RG}"
        ```

2.  Create the NAT subnet.

    1.  Check the existing address space and subnets to ensure that you do not choose an overlapping classless inter-domain routing (CIDR) range. Enter the following command:

        ``` terminal
        $ az network vnet show \
          --resource-group "${MGMT_VNET_RG}" \
          --name "${MGMT_VNET_NAME}" \
          --query '{addressSpace: addressSpace.addressPrefixes, subnets: subnets[].{name: name, prefix: addressPrefix}}' \
          -o json
        ```

    2.  Create the subnet as shown in the following example:

        ``` terminal
        $ az network vnet subnet create \
          --resource-group "${MGMT_VNET_RG}" \
          --vnet-name "${MGMT_VNET_NAME}" \
          --name "${NAT_SUBNET_NAME}" \
          --address-prefixes 10.1.64.0/24 \
          --disable-private-link-service-network-policies true
        ```

        - The NAT subnet must be in the VNet of the management cluster because Private Link is created alongside the internal load balancer of the management cluster.

        - The `10.1.64.0/24` address prefix is an example only. Replace it with a CIDR range that does not overlap with any other subnet in the VNet of the management cluster. If the VNet uses `10.0.0.0/16`, the NAT subnet must fall within that range, or you must expand the address space of the VNet.

        - The `--disable-private-link-service-network-policies` flag is required and must be set to `true`. Otherwise, Azure rejects the creation of Private Link on the subnet.

3.  Obtain the NAT subnet resource ID for later use as shown in the following example:

    ``` bash
    $ NAT_SUBNET_ID=$(az network vnet subnet show \
      --resource-group "${MGMT_VNET_RG}" \
      --vnet-name "${MGMT_VNET_NAME}" \
      --name "${NAT_SUBNET_NAME}" \
      --query id -o tsv)
    ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [Configuring an Azure management cluster for hosted control planes](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-mgmt-cluster_hcp-deploy-azure)

- [Setting up an OIDC issuer](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-oidc_hcp-deploy-azure)

</div>

## Installing the HyperShift Operator with private platform support

To set up an environment that supports private clusters, you must install the HyperShift Operator with flags that configure Azure Private Link management.

> [!NOTE]
> If you already installed the HyperShift Operator but you did not include the `--private-platform Azure` setting, you must run the `hcp install` command again with the private platform flags before you can create private clusters.

<div>

<div class="title">

Prerequisites

</div>

- You have an OpenShift Container Platform management cluster on Azure.

- The Azure command-line interface (CLI) is installed and configured.

- The OpenShift CLI (`oc`) is installed.

- If you are using external DNS, the `jq` command-line JSON processor is installed.

- You configured an OIDC issuer. For more information, see "Setting up an OIDC issuer".

</div>

<div>

<div class="title">

Procedure

</div>

1.  Obtain credentials so that the Operator can manage Private Link resources.

    1.  Obtain the credentials file for Private Link management as shown in the following example:

        ``` bash
        $ AZURE_PRIVATE_CREDS="<path_to_azure_private_credentials_json>"
        ```

    2.  Obtain the infrastructure resource group of the management cluster as shown in the following example:

        ``` bash
        $ MGMT_INFRA_RG=$(oc get infrastructure cluster -o jsonpath='{.status.platformStatus.azure.resourceGroupName}')
        ```

2.  Set the external DNS configuration variables as shown in the following examples:

    ``` bash
    $ SERVICE_PRINCIPAL_FILEPATH="<path_to_azure_mgmt_json_file>"
    ```

    ``` bash
    $ DNS_ZONE_NAME="<my_subdomain_my_parent_dns_zone_com>"
    ```

3.  Install the HyperShift Operator with private platform support as shown in the following example:

    ``` terminal
    $ hcp install \
      --pull-secret ${PULL_SECRET} \
      --private-platform Azure \
      --azure-private-creds ${AZURE_PRIVATE_CREDS} \
      --azure-pls-resource-group ${MGMT_INFRA_RG} \
      --external-dns-provider=azure \
      --external-dns-credentials ${SERVICE_PRINCIPAL_FILEPATH} \
      --external-dns-domain-filter ${DNS_ZONE_NAME}
    ```

    - `--private-platform Azure` specifies that Azure Private Link management is to be enabled in the Operator.

    - `--azure-private-creds` specifies the path to the Azure credentials file that is used for Private Link operations.

      > [!NOTE]
      > Besides using the `--azure-private-creds` flag, you can use one of the following authentication methods. Be sure to use only one authentication method.
      >
      > - `--azure-private-secret` specifies an existing Kubernetes secret that has Azure credentials. This flag has a companion flag, `--azure-private-secret-key`. Its default value is `credentials`, but you can customize it for secrets that have non-standard key names.
      >
      > - `--azure-pls-managed-identity-client-id` specifies the client ID of a managed identity for Private Link operations through Workload Identity federation. If you specify this flag, you must also include the `--azure-pls-subscription-id` flag, which specifies the Azure subscription ID for Private Link operations.

    - `--azure-pls-resource-group` specifies the resource group where the Private Link resources are to be created. This resource group is the same as the resource group of the infrastructure for the management cluster.

    - `--external-dns-credentials` specifies the path to a file that contains DNS credentials. If preferred, you can use the `--external-dns-secret` flag instead to specify a Kubernetes secret that has DNS credentials.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Setting up an OIDC issuer](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-oidc_hcp-deploy-azure)

</div>

## Configuring IAM resources for a private hosted cluster

Create Workload Identities so that your private clusters can manage private endpoints and private DNS zones.

<div>

<div class="title">

Prerequisites

</div>

- You have an OpenShift Container Platform management cluster on Azure that has the HyperShift Operator installed.

- The Azure command-line interface (CLI) is installed and configured.

- The OpenShift CLI (`oc`) is installed.

- If you are using external DNS, the `jq` command-line JSON processor is installed.

- You configured an OIDC issuer. For more information, see "Setting up an OIDC issuer".

</div>

<div>

<div class="title">

Procedure

</div>

1.  Set your environment variables:

    1.  Set your prefix by entering the following command:

        ``` bash
        $ PREFIX="<my_prefix>"
        ```

    2.  Set the cluster name by entering the following command:

        ``` bash
        $ CLUSTER_NAME="${PREFIX}-hc"
        ```

    3.  Set the resource group name by entering the following command:

        ``` bash
        $ RESOURCE_GROUP_NAME="${CLUSTER_NAME}-${PREFIX}"
        ```

    4.  Set the location by entering the following command:

        ``` bash
        $ LOCATION="<my_region>"
        ```

    5.  Set the variable for the path to the Azure credentials file by entering the following command:

        ``` bash
        $ AZURE_CREDS="<path_to_azure_credentials_json>"
        ```

    6.  Set the variable for the OIDC issuer URL by entering the following command:

        ``` bash
        $ OIDC_ISSUER_URL="<my_oidc_url_com>"
        ```

    7.  Set the path to the Workload Identities file by entering the following command:

        ``` bash
        $ WORKLOAD_IDENTITIES_FILE="<path_to_workload_identities_file_json>"
        ```

2.  Create Workload Identities by entering the following command:

    ``` terminal
    $ hcp create iam azure \
      --name "${CLUSTER_NAME}" \
      --infra-id "${PREFIX}" \
      --azure-creds "${AZURE_CREDS}" \
      --location "${LOCATION}" \
      --resource-group-name "${RESOURCE_GROUP_NAME}" \
      --oidc-issuer-url "${OIDC_ISSUER_URL}" \
      --output-file "${WORKLOAD_IDENTITIES_FILE}"
    ```

    The command creates 8 Workload Identities. For `Private` and `PublicAndPrivate` clusters, the Control Plane Operator identity is used to create and manage private endpoints, private DNS zones, Azure Virtual Network (VNet) links, and DNS A records. The Control Plane Identity is assigned the `Contributor` role by default. To use a more restrictive role, use the `--assign-custom-hcp-roles` flag.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Setting up an OIDC issuer](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-oidc_hcp-deploy-azure)

- [Creating Azure Workload Identities](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-workload-id_hcp-deploy-azure)

</div>

## Creating infrastructure for a private hosted cluster

Set up infrastructure so that you can create private hosted clusters.

<div>

<div class="title">

Prerequisites

</div>

- You have an OpenShift Container Platform management cluster on Azure that has the HyperShift Operator installed.

- The Azure command-line interface (CLI) is installed and configured.

- The OpenShift CLI (`oc`) is installed.

- If you are using external DNS, the `yq` command-line YAML processor is installed.

- You configured an OIDC issuer. For more information, see "Setting up an OIDC issuer".

</div>

<div>

<div class="title">

Procedure

</div>

1.  Set your environment variables:

    1.  Set the variable for the DNS zone resource group by entering the following command:

        ``` bash
        $ DNS_ZONE_RG_NAME="os4-common"
        ```

    2.  Set the variable for the base domain of your DNS zone by entering the following command:

        ``` bash
        $ PARENT_DNS_ZONE="<your_base_domain_com>"
        ```

    3.  Set the variable that points to the infrastructure output file by entering the following command:

        ``` bash
        $ INFRA_OUTPUT_FILE="${PREFIX}-infra-output.json"
        ```

2.  Create infrastructure by entering the following command:

    ``` terminal
    $ hcp create infra azure \
      --azure-creds "${AZURE_CREDS}" \
      --infra-id "${PREFIX}" \
      --name "${CLUSTER_NAME}" \
      --location "${LOCATION}" \
      --base-domain "${PARENT_DNS_ZONE}" \
      --dns-zone-rg-name "${DNS_ZONE_RG_NAME}" \
      --workload-identities-file "${WORKLOAD_IDENTITIES_FILE}" \
      --assign-identity-roles \
      --output-file "${INFRA_OUTPUT_FILE}"
    ```

3.  Read the infrastructure output to get the resource IDs that you created, as shown in the following example:

    1.  Read the resource group name by entering the following command:

        ``` bash
        $ MANAGED_RG_NAME=$(yq -r -p yaml '.resourceGroupName' "${INFRA_OUTPUT_FILE}")
        ```

    2.  Read the VNet ID by entering the following command:

        ``` bash
        $ VNET_ID=$(yq -r -p yaml '.vnetID' "${INFRA_OUTPUT_FILE}")
        ```

    3.  Read the subnet ID by entering the following command:

        ``` bash
        $ SUBNET_ID=$(yq -r -p yaml '.subnetID' "${INFRA_OUTPUT_FILE}")
        ```

    4.  Read the network security group ID by entering the following command:

        ``` bash
        $ NSG_ID=$(yq -r -p yaml '.securityGroupID' "${INFRA_OUTPUT_FILE}")
        ```

        Note the resource IDs because you need them to create the private hosted cluster.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Setting up an OIDC issuer](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-oidc_hcp-deploy-azure)

</div>

## Creating a private Azure hosted cluster

Create a private hosted cluster to ensure that the communication between compute nodes and the hosted control plane occurs over Azure Private Link.

<div>

<div class="title">

Prerequisites

</div>

- You configured a subnet, as described in "Preparing a subnet for a private hosted cluster on Azure".

- You installed the HyperShift Operator on an OpenShift Container Platform management cluster on Azure, as described in "Installing the HyperShift Operator with private platform support".

- You created Identity and Access Management (IAM) resources, as described in "Configuring IAM resources for a private hosted cluster".

- You created infrastructure, as described in "Creating infrastructure for a private hosted cluster".

- This procedure relies on environment variables that you created in the prerequisite procedures. Be sure to complete this procedure in the same terminal where you already defined the environment variables.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create the private hosted cluster by entering the following command:

    ``` terminal
    $ hcp create cluster azure \
      --name "$CLUSTER_NAME" \
      --namespace "clusters" \
      --azure-creds ${AZURE_CREDS} \
      --location ${LOCATION} \
      --node-pool-replicas 2 \
      --base-domain ${PARENT_DNS_ZONE} \
      --pull-secret ${PULL_SECRET} \
      --generate-ssh \
      --release-image ${RELEASE_IMAGE} \
      --resource-group-name "${MANAGED_RG_NAME}" \
      --vnet-id "${VNET_ID}" \
      --subnet-id "${SUBNET_ID}" \
      --network-security-group-id "${NSG_ID}" \
      --sa-token-issuer-private-key-path "${SA_TOKEN_ISSUER_PRIVATE_KEY_PATH}" \
      --oidc-issuer-url "${OIDC_ISSUER_URL}" \
      --dns-zone-rg-name ${DNS_ZONE_RG_NAME} \
      --assign-service-principal-roles \
      --workload-identities-file ${WORKLOAD_IDENTITIES_FILE} \
      --external-dns-domain ${DNS_ZONE_NAME} \
      --endpoint-access Private \
      --endpoint-access-private-nat-subnet-id "${NAT_SUBNET_ID}"
    ```

    - When you choose a value for the `--external-dns-domain` flag, ensure that the value does not match `{cluster-name}.{base-domain}`. If you use `{cluster-name}.{base-domain}` for the value, the Control Plane Operator creates a private DNS zone that can shadow the `*.apps` domain, which causes the console and ingress to become unreachable.

    - `--endpoint-access` accepts 3 values:

      - `Public`, which is the default value. When you specify `Public`, the API server is accessible through public endpoint only.

      - `PublicAndPrivate`, where the API server is accessible through both public and private endpoints.

      - `Private`, where the API server is accessible only through Private Link.

        After you create a cluster, you cannot change it between `Public` endpoint and non-public (`PublicAndPrivate` or `Private`) endpoint access.

        If you need to allow `Private` endpoint connections from Azure subscriptions other than the hosted cluster’s subscription, use the following flag: `--endpoint-access-private-additional-allowed-subscriptions "sub-id-1, sub-id-2"`.

</div>

<div>

<div class="title">

Verification

</div>

1.  Check the Private Link resources by entering the following command:

    ``` terminal
    $ oc get azureprivatelinkservices -n clusters-${CLUSTER_NAME}
    ```

2.  Check the status and connections by entering the following command:

    ``` terminal
    $ oc get azureprivatelinkservices -n clusters-${CLUSTER_NAME} -o yaml
    ```

    | Condition | Description |
    |----|----|
    | `AzureInternalLoadBalancerAvailable` | The internal load balancer has a front-end IP address. |
    | `AzurePLSCreated` | Private Link is created in the management cluster. |
    | `AzurePrivateEndpointAvailable` | Private endpoint is created in the hosted cluster VNet. |
    | `AzurePrivateDNSAvailable` | Private DNS zones and A records are created. |
    | `AzurePrivateLinkServiceAvailable` | All components are ready and private connectivity is available. |

    Setup progress conditions

3.  Check the overall cluster status by entering the following command:

    ``` terminal
    $ oc get hostedcluster ${CLUSTER_NAME} -n clusters
    ```

4.  Wait for the status by entering the following command:

    ``` terminal
    $ oc wait --for=condition=Available hostedcluster/${CLUSTER_NAME} -n clusters --timeout=30m
    ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [Preparing a subnet for a private hosted cluster on Azure](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-private-subnet_hcp-deploy-azure)

- [Installing the HyperShift Operator with private platform support](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-private-operator_hcp-deploy-azure)

- [Configuring IAM resources for a private hosted cluster](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-private-iam_hcp-deploy-azure)

- [Creating infrastructure for a private hosted cluster](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-private-infra_hcp-deploy-azure)

</div>

## Accessing a private Azure hosted cluster

After you create a private hosted cluster, you need to take additional steps to access it.

<div>

<div class="title">

Prerequisites

</div>

- You completed the steps in "Creating a private Azure hosted cluster".

</div>

<div>

<div class="title">

Procedure

</div>

- To access a private hosted cluster by generating a `kubeconfig` file, enter the following command:

  ``` terminal
  $ hcp create kubeconfig \
    --name ${CLUSTER_NAME} \
    --port-forward > ${CLUSTER_NAME}-kubeconfig
  ```

- If you have access to the management cluster, you can port forward to the API server to access the private hosted cluster.

  1.  Port forward to the `kube-apiserver` service by entering the following command:

      ``` terminal
      $ kubectl port-forward svc/kube-apiserver \
        -n clusters-${CLUSTER_NAME} 6443:6443 &
      ```

  2.  Access the hosted cluster by using the `kubeconfig` file:

      ``` bash
      $ KUBECONFIG=${CLUSTER_NAME}-kubeconfig oc get nodes
      ```

- If you have a virtual machine (VM) in an Azure Virtual Network (VNet) that is peered with the hosted cluster’s VNet, you can access the API server, but you must first link the private DNS zones to the peered VNet.

  > [!NOTE]
  > The Control Plane Operator links private DNS zones only to the hosted cluster’s VNet. If you want to resolve the API server hostname from a peered VNet, you must manually link the private DNS zones to that VNet as shown in the following steps. Otherwise, DNS resolution fails from the peered VNet.

  1.  Link the private DNS zone to your peered VNet as shown in the following example:

      ``` bash
      $ PEERED_VNET_ID="/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Network/virtualNetworks/<vnet>"
      ```

  2.  Enter the following command:

      ``` terminal
      $ az network private-dns link vnet create \
        --resource-group "${MANAGED_RG_NAME}" \
        --zone-name "${CLUSTER_NAME}.hypershift.local" \
        --name "peered-vnet-link" \
        --virtual-network "${PEERED_VNET_ID}" \
        --registration-enabled false
      ```

  3.  If you also need base-domain resolution, enter the following command:

      ``` terminal
      $ az network private-dns link vnet create \
        --resource-group "${MANAGED_RG_NAME}" \
        --zone-name "${PARENT_DNS_ZONE}" \
        --name "peered-vnet-basedomain-link" \
        --virtual-network "${PEERED_VNET_ID}" \
        --registration-enabled false
      ```

  4.  Access the cluster as shown in the following example:

      ``` bash
      $ KUBECONFIG=${CLUSTER_NAME}-kubeconfig oc get nodes
      ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [Creating a private Azure hosted cluster](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-private-hosted_hcp-deploy-azure)

</div>

## Troubleshooting private hosted clusters on Azure

If your private hosted cluster gets stuck, check the `AzurePrivateLinkService` custom resource conditions.

<div>

<div class="title">

Procedure

</div>

1.  Enter the following command to check the Private Link conditions:

    ``` terminal
    $ oc get azureprivatelinkservices \
      -n clusters-${CLUSTER_NAME} \
      -o jsonpath='{.items[0].status.conditions}' | jq .
    ```

2.  Review the output and compare it to the following condition table:

    | Condition | Possible cause |
    |----|----|
    | `AzureInternalLoadBalancerAvailable` = `False` | The `private-router` service has not received an internal load balancer IP address yet. Check the service status and Azure networking. |
    | `AzurePLSCreated` = `False` | Private Link creation failed. Check the NAT subnet policies, credentials, and the HyperShift Operator logs. |
    | `AzurePrivateEndpointAvailable` = `False` | Private endpoint creation failed or the connection was not approved. Check the Private Link auto-approval list and the Control Plane Operator logs. |
    | `AzurePrivateDNSAvailable` = `False` | The DNS zone or record creation failed. In the Azure subscription that stores the infrastructure resources for the hosted cluster, check the Control Plane Operator identity permissions. |

    Private cluster stuck conditions

</div>

# PublicAndPrivate topology for hosted clusters on Azure

The `PublicAndPrivate` topology enables dual-path routing so that external automation and private workloads can reach the Kubernetes API Server endpoint simultaneously. As a result, you can meet compliance requirements without sacrificing CI/CD pipeline access.

The topology you select at cluster creation determines which Azure resources are provisioned and whether the Kubernetes API Server endpoint is reachable from the public internet, a private Azure VNet, or both.

Hosted clusters on Azure support 3 Kubernetes API Server endpoint access topologies: `Public`, `Private`, and `PublicAndPrivate`.

`Public` (default)
The Kubernetes API Server endpoint is accessible from the public internet only. No private Azure networking resources are created. Use this topology for non-regulated environments or CI/CD workloads that do not require private control-plane access.

`PublicAndPrivate`
The Kubernetes API Server endpoint is accessible from the public internet and from a private Azure VNet simultaneously. Azure creates both public and private networking resources. Use this topology when external automation requires public API access and internal workloads require private network isolation.

`Private`
The Kubernetes API Server endpoint is accessible only from a private Azure VNet. No public Azure Load Balancer is created for the Kubernetes API Server endpoint. Use this topology for regulated environments where the control plane must never be reachable from the public internet.

## Azure resources provisioned by topology

| Resource                     | `Public` | `PublicAndPrivate` | `Private` |
|------------------------------|----------|--------------------|-----------|
| Azure Public Load Balancer   | Yes      | Yes                | No        |
| Azure Internal Load Balancer | No       | Yes                | Yes       |
| Azure Private Link Service   | No       | Yes                | Yes       |
| Azure Private Endpoint       | No       | Yes                | Yes       |
| Private DNS Zones            | No       | Yes                | Yes       |

Azure resources by topology

> [!NOTE]
> The Azure Private Link Service, Azure Private Endpoint, and Private DNS Zones rows apply only to self-managed hosted control planes clusters using the `PrivateLink` private type.

On self-managed hosted clusters (Azure Private Link), the topology directly drives the `IngressController` `LoadBalancer` scope. A dedicated Azure Private Link Service infrastructure is created per cluster for private access. The `PrivateLink` private type provisions an Internal Load Balancer, Private Link Service, Private Endpoint, and Private DNS zones for each cluster independently.

## Ingress and Private Link architecture for hosted clusters on Azure

Understanding the shared ingress and Private Link architecture helps you correctly interpret the connectivity behavior of the Kubernetes API Server and avoid misconfiguration during verification. For self-managed hosted control planes, each cluster with private topology receives a dedicated Private Link Service infrastructure.

The topology directly drives the `IngressController` `LoadBalancer` scope:

- `Public` topology: `ExternalLoadBalancer` scope

- `Private` or `PublicAndPrivate` topology: `InternalLoadBalancer` scope

Each cluster with private topology also receives a dedicated Azure Private Link Service infrastructure (Internal load balancer → Private Link Service → Private Endpoint → Private DNS zones).

## Creating a hosted control plane with a PublicAndPrivate topology

You can create a hosted cluster with `PublicAndPrivate` Kubernetes API Server topology to enable simultaneous public-internet access and private Azure VNet access.

`PublicAndPrivate` topology suits regulated environments that require private control-plane networking while maintaining CI/CD pipeline access from the public internet.

> [!IMPORTANT]
> The `topology` field is immutable for transitions involving `Public` topology. You can change between `PublicAndPrivate` and `Private` after cluster creation, but you cannot change to or from `Public` without creating a new cluster. Plan your topology selection carefully before provisioning.

<div>

<div class="title">

Prerequisites

</div>

- You have an Azure account with permissions to create hosted clusters and the required workload identities, including the Control Plane Operator workload identity.

- You have an Azure VNet in your target region.

- You have a public Azure DNS zone for the externally published DNS records of the cluster.

- You have a dedicated NAT subnet in the VNet of the management cluster with `privateLinkServiceNetworkPolicies` disabled.

- The HyperShift Operator is installed with the `--private-platform Azure` flag.

- When the `--private-platform` flag is set to `Azure`, the HyperShift Operator requires one of the following flags: `--azure-private-creds`, `--azure-private-secret`, or `--azure-pls-managed-identity-client-id`. The Operator uses those credentials to look up the internal load balancer and create the Private Link Service in the management cluster resource group.

- External DNS is configured on the management cluster with Azure credentials and a domain filter that enables the DNS to manage records in that zone.

</div>

> [!IMPORTANT]
> For private Azure hosted clusters, do not set the domain of the OAuth route hostname to `<cluster_name>.<base_domain>` or to a parent domain of `<cluster_name>.<base_domain>`. The resulting Private DNS zone can shadow `*.apps` records and break console and route resolution.
>
> For example, if you have the `hcp-two` cluster name and `example.com` base domain, do not use `hcp-two.example.com`. Use a non-overlapping domain, such as `external-dns.example.com`. This configuration cannot be corrected after cluster creation; you must re-create the cluster with a different domain.

<div>

<div class="title">

Procedure

</div>

1.  Create a `HostedCluster` manifest, as shown in the following example.

    > [!NOTE]
    > This example shows only the topology-specific fields.

    ``` yaml
    apiVersion: hypershift.openshift.io/v1beta1
    kind: HostedCluster
    metadata:
      name: <cluster_name>
      namespace: clusters
    spec:
      platform:
        type: Azure
        azure:
          topology: PublicAndPrivate
          private:
            type: PrivateLink
            privateLink:
              natSubnetID: <nat_subnet_resource_id>
    ```

    where:

    `<cluster_name>`
    Specifies the name of your hosted cluster.

    `<nat_subnet_resource_id>`
    Specifies the Azure resource ID of the NAT subnet. This subnet must have `privateLinkServiceNetworkPolicies` disabled and must reside in the VNet of the management cluster. This subnet is optional; if it is omitted, the controller creates the NAT subnet in the VNet of the management cluster’s internal load balancer. For more information, see "Preparing a subnet for a private hosted cluster on Azure".

2.  Apply the manifest to your cluster by entering the following command:

    ``` terminal
    $ oc apply -f <manifest_file>.yaml
    ```

3.  Monitor the cluster provisioning status by entering the following command:

    ``` terminal
    $ oc get hostedcluster <cluster_name> -n clusters -w
    ```

</div>

<div>

<div class="title">

Verification

</div>

- Check the `Available` condition to confirm the control plane is up by entering the following command:

  ``` terminal
  $ oc get hostedcluster <cluster_name> -n clusters \
    -o jsonpath='{.status.conditions[?(@.type=="Available")]}'
  ```

  For a full connectivity verification procedure, see "Verifying endpoint accessibility for a PublicAndPrivate hosted cluster on Azure".

</div>

<div>

<div class="title">

Additional resources

</div>

- [Preparing a subnet for a private hosted cluster on Azure](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-private-subnet_hcp-deploy-azure)

</div>

## Verifying endpoint accessibility for a PublicAndPrivate hosted cluster on Azure

After you create a hosted cluster on Azure with `PublicAndPrivate` topology, you must verify that the Kubernetes API Server endpoint is reachable from both the public internet and the private Azure VNet.

Successful verification confirms that the control plane is healthy, private connectivity resources are provisioned, and DNS is resolving correctly. Verification is crucial, as topology misconfiguration is partially irreversible.

<div>

<div class="title">

Prerequisites

</div>

- You have a running hosted cluster on Azure with `PublicAndPrivate` topology.

- The `oc` CLI is installed and authenticated to the cluster management plane.

- For private VNet verification, you have access to a jump server VM or other host inside the VNet of the hosted cluster, or the ability to use port-forwarding from inside the VNet.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Check the HostedCluster `Available` condition to confirm the control plane is running by entering the following command:

    ``` terminal
    $ oc get hostedcluster <cluster_name> -n clusters \
      -o jsonpath='{.status.conditions[?(@.type=="Available")]}'
    ```

    Replace `<cluster_name>` with the name of your hosted cluster.

    Verify that `"status":"True"` is displayed in the output.

2.  Retrieve the `AzurePrivateLinkService` CR conditions to verify that the private link chain is fully provisioned by entering the following command:

    ``` terminal
    $ oc get azureprivatelinkservices -n clusters-<cluster_name> -o yaml
    ```

    Verify that all five conditions are `True`:

    - `AzureInternalLoadBalancerAvailable`

    - `AzurePLSCreated`

    - `AzurePrivateEndpointAvailable`

    - `AzurePrivateDNSAvailable`

    - `AzurePrivateLinkServiceAvailable`

      If any condition is `False`, see "AzurePrivateLinkService conditions reference" for diagnosis guidance.

3.  Verify DNS resolution of the private API hostname from inside the VNet of the hosted cluster.

    From a host inside the VNet, resolve the private API hostname by entering the following command:

    ``` terminal
    $ nslookup <api_hostname_from_kubeconfig>
    ```

    Include only the hostname from the `server:` URL of the `kubeconfig`, without the `https://` prefix or port, and do not append the `<base_domain>`. The API hostname must resolve to the Private endpoint IP address from inside the VNet. If the hostname resolves to a public IP, verify that the Private DNS zone is correctly linked to the VNet of the hosted cluster.

4.  Confirm API reachability from the public internet by using the hosted cluster `kubeconfig` by entering the following command:

    ``` terminal
    $ oc get nodes --kubeconfig <path_to_hosted_cluster_kubeconfig>
    ```

    Replace `<path_to_hosted_cluster_kubeconfig>` with the path to the hosted cluster kubeconfig file.

    A successful node listing confirms that the public Kubernetes API Server endpoint is reachable.

5.  Confirm API reachability from inside the private Azure VNet.

    From a jump server VM or other host inside the private Azure VNet, run the following command:

    ``` terminal
    $ oc get nodes --kubeconfig <path_to_hosted_cluster_kubeconfig>
    ```

    A successful node listing confirms that the private Kubernetes API Server endpoint is reachable from within the VNet.

    > [!IMPORTANT]
    > By default, private DNS zones are linked only to the hosted cluster’s VNet. If you require DNS resolution from peered VNets, manually link the Private DNS zone to each peered VNet after cluster creation. Failure to link peered VNets results in DNS resolution failures from those networks.

</div>

## Topology transition rules and constraints

The `topology` field in a `HostedCluster` resource is immutable for transitions involving the `Public` topology.

Transitions between `PublicAndPrivate` and `Private` are allowed after cluster creation. Any change to or from `Public` requires creating a new cluster.

To avoid an irreversible misconfiguration, review these constraints carefully before you select a topology.

| From topology | To topology | Allowed after creation | Action required |
|----|----|----|----|
| `Public` | `Private` | No | Create a new cluster. |
| `Public` | `PublicAndPrivate` | No | Create a new cluster. |
| `Private` | `Public` | No | Create a new cluster. |
| `PublicAndPrivate` | `Public` | No | Create a new cluster. |
| `PublicAndPrivate` | `Private` | Yes | Update the `HostedCluster` resource. |
| `Private` | `PublicAndPrivate` | Yes | Update the `HostedCluster` resource. |

Topology transition rules

| Dimension | `Public` | `PublicAndPrivate` | `Private` |
|----|----|----|----|
| Kubernetes API Server access | Public internet only | Public internet + private Azure VNet | Private Azure VNet only |
| External DNS required | No | Yes | Yes |
| `private` field required | No | Yes | Yes |
| `IngressController` scope | `ExternalLoadBalancer` | `InternalLoadBalancer` | `InternalLoadBalancer` |

Azure hosted control planes topology comparison

> [!IMPORTANT]
> Topology selection is a one-time, irreversible decision for any cluster that starts with or transitions to `Public` topology. Before you create a cluster, choose the topology that satisfies your compliance requirements. If you must move from `Public` to a private topology, or from a private topology to `Public`, you must create a new cluster.

## AzurePrivateLinkService conditions reference

The `AzurePrivateLinkService` custom resource exposes 5 status conditions that you inspect to verify the end-to-end private link chain for a hosted cluster with `Private` or `PublicAndPrivate` topology.

All 5 conditions must be `True` before the private Kubernetes API Server path is considered provisioned. Use the following conditions to diagnose incomplete or failed private connectivity.

To retrieve the current conditions from the cluster, run the following command:

``` terminal
$ oc get azureprivatelinkservices -n clusters-<cluster_name> -o yaml
```

Replace `<cluster_name>` with the name of your hosted cluster.

| Condition name | Expected state | What it indicates |
|----|----|----|
| `AzureInternalLoadBalancerAvailable` | `True` | If this condition is missing, verify that the HyperShift Operator’s Azure Private Link credentials, or managed identity, can read the load balancers in the management cluster resource group, and check the `AzurePLSCreated` condition message for errors. |
| `AzurePLSCreated` | `True` | The Azure Private Link Service instance has been provisioned and is registered. `AzureInternalLoadBalancerAvailable` must be `True` before this condition can become `True`. |
| `AzurePrivateEndpointAvailable` | `True` | The Azure Private Endpoint has been created and its connection to the Private Link Service has been approved. If `False`, the PE might be in a pending state awaiting approval; check the Azure portal for pending PE connection requests. |
| `AzurePrivateDNSAvailable` | `True` | The Azure Private DNS zone and DNS records for the private Kubernetes API Server hostname have been provisioned. If `False`, DNS records might not yet be propagated; wait and re-check. For peered VNets, verify that the Private DNS zone is linked to each peered VNet. |
| `AzurePrivateLinkServiceAvailable` | `True` | The HyperShift Operator sets `AzurePrivateLinkServiceAvailable` and `AzurePLSCreated` to `True` as soon as the Private Link Service is ready, before the Private Endpoint and DNS records exist. The Control Plane Operator sets the final value only after the Private Endpoint and DNS are reconciled. The value for `AzurePrivateLinkServiceAvailable` can be `True` briefly while the chain is still incomplete. To get a more reliable signal, check `AzurePrivateEndpointAvailable` and `AzurePrivateDNSAvailable`. |

AzurePrivateLinkService status conditions

> [!NOTE]
> All 5 conditions must be `True` before you attempt to connect to the Kubernetes API Server endpoint over the private network path. If any condition is `False`, diagnose sequentially from `AzureInternalLoadBalancerAvailable` through `AzurePrivateLinkServiceAvailable`, as each resource depends on the previous one being provisioned.

# Example: Autoscaling a hosted cluster on Azure

To balance node pools on your Azure hosted cluster, you can configure autoscaling for the cluster.

When you scale up `NodePool` objects, the Cluster API Provider for Azure provisions individual Azure virtual machines.

To configure autoscaling for a hosted cluster on Azure, you edit the `spec.autoscaling` parameters in the `HostedCluster` resource. The following example shows a `HostedCluster` resource with 2 Azure node pools.

> [!NOTE]
> This example shows only the autoscaling-related fields.

``` yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: HostedCluster
metadata:
  name: my-cluster
  namespace: my-cluster-namespace
spec:
  autoscaling:
    scaling: ScaleUpAndScaleDown
    maxNodesTotal: 12
    expanders:
      - Random
    scaleDown:
      delayAfterAddSeconds: 300
      unneededDurationSeconds: 600
      utilizationThresholdPercent: 40
    balancingIgnoredLabels:
      - "custom.label/environment"
    maxFreeDifferenceRatioPercent: 70
---
apiVersion: hypershift.openshift.io/v1beta1
kind: NodePool
metadata:
  name: my-cluster-nodepool-1
  namespace: my-cluster-namespace
spec:
  clusterName: my-cluster
  autoScaling:
    min: 1
    max: 6
  platform:
    azure:
      vmSize: Standard_D4s_v3
      # ...
---
apiVersion: hypershift.openshift.io/v1beta1
kind: NodePool
metadata:
  name: my-cluster-nodepool-2
  namespace: my-cluster-namespace
spec:
  clusterName: my-cluster
  autoScaling:
    min: 1
    max: 6
  platform:
    azure:
      vmSize: Standard_D4s_v3
      # ...
```

- `spec.autoScaling.min` must be greater than or equal to `1` on platforms that do not support scale-from-zero.

  On Amazon Web Services (AWS) and Azure hosted clusters running OpenShift Container Platform 4.18 or later, you can set `spec.autoScaling.min` to `0` for eligible tainted workload pools. For more information, see "Configuring autoscaling to and from zero on hosted control planes node pools".

  > [!NOTE]
  > Earlier versions of this example stated that scaling from zero (`autoScaling.min: 0`) is not supported on Azure. OpenShift Container Platform 4.18 and later support `min: 0` on Amazon Web Services (AWS) and Azure when the HyperShift Operator backport is available.

# Backup and restore for hosted control planes on Azure

You can back up and restore a self-managed hosted control planes on Microsoft Azure by using OpenShift API for Data Protection (OADP) 1.6.

Automated backups capture the etcd state and associated Azure infrastructure resources. If etcd data loss or corruption occurs, you can restore the cluster from a snapshot on the same management cluster.

## Limitations for disaster recovery on hosted control planes on Azure

Review the following limitations before you design a disaster recovery (DR) strategy for hosted control planes on Azure. The same-cluster-only restriction and mandatory compute node reprovisioning have the most significant impact on DR architecture and site selection.

| Limitation | Details |
|----|----|
| Same-cluster restore only | Cross-management-cluster restore is not currently supported. Only same-cluster restore, restoring to the management cluster from which the backup was taken, is validated for Azure. |
| OADP required | Automated restore requires OADP 1.6 with the built-in `hypershift` plugin. No manual restore path is supported for self-managed Azure hosted control planes. |
| `restoreSnapshotURL` immutability | The `spec.etcd.managed.storage.restoreSnapshotURL` field is enforced as immutable by validation (`MaxItems=1`). The OADP plugin sets this field automatically at `HostedCluster` creation time during a restore. You cannot update the field after the `HostedCluster` resource is created, and you do not need to set it manually. |
| No in-place restore | The existing `HostedCluster` resource must be deleted before restore. Restoring to a running cluster is not supported. All etcd persistent volume claims (PVCs) must be removed before the restore command is run. |
| Compute node reprovisioning | Compute nodes are reprovisioned after a restore. Plan for workload disruption during recovery. Applications running on compute nodes experience downtime while nodes are reprovisioned and rejoin the cluster. |
| Technology Preview (`HCPEtcdBackup` feature gate) | etcd snapshot restore requires the `HCPEtcdBackup` feature gate on the HyperShift Operator. This feature is a Technology Preview feature and is not intended for production use. |
| Single snapshot per restore | Only one snapshot URL is accepted per restore (`MaxItems=1`). Fallback snapshot support, where you automatically retry a restore with a secondary snapshot if the first fails, is not available. Select a good backup before you run the restore command. |

## Setting up backup and restore for hosted control planes on Azure

Set up your hosted control planes on Azure environment to run automated backups.

OpenShift API for Data Protection (OADP) 1.6 with the built-in `hypershift` plugin is the supported backup and restore solution for hosted control planes on Azure. The `hypershift` plugin is included in OADP 1.6 by default and does not require a custom plugin image.

The plugin supports two backup modes:

Volume snapshot backup
Captures persistent volume data by using CSI snapshots. This mode backs up etcd storage volumes and does not require the `HCPEtcdBackup` feature gate. For volume snapshot backup procedures, see "Automated disaster recovery for hosted control planes on Azure".

etcd snapshot backup
Captures a point-in-time etcd snapshot and stores the snapshot URL in the `HostedCluster.status.lastSuccessfulEtcdBackupURL` specification. The OADP plugin injects this URL automatically at restore time. This mode requires the `HCPEtcdBackup` feature gate and is available as a Technology Preview feature.

<div>

<div class="title">

Prerequisites

</div>

- You installed OADP 1.6 on the management cluster. For more information, see [Configuring OADP with Azure](../../backup_and_restore/application_backup_and_restore/installing/installing-oadp-azure.xml#installing-oadp-azure).

- You created an Azure Blob Storage account and container that are accessible from the management cluster.

- You have a Kubernetes secret containing the Azure credentials. For more information, see step 1 in [Setting up automated disaster recovery for hosted control planes on Azure](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-automated-dr-setup_hcp-deploy-azure).

</div>

<div>

<div class="title">

Procedure

</div>

- To configure automated backups, enter the `hcp create oadp-schedule` command. The following example shows how to schedule daily backups.

  ``` terminal
  $ hcp create oadp-schedule \
    --hc-name <hosted_cluster_name> \
    --hc-namespace <hosted_cluster_namespace> \
    --storage-location azure-blob \
    --schedule "0 2 * * *"
    --use-etcd-snapshot
  ```

  where:

  `--hc-name`
  Specifies the name of the `HostedCluster` resource to back up.

  `--hc-namespace`
  Specifies the namespace of the `HostedCluster` resource.

  `--use-etcd-snapshot`
  Specifies that you want to use the etcd snapshot method. If you are using CSI snapshot, do not include this flag.

</div>

<div>

<div class="title">

Verification

</div>

1.  Check the status of the most recent Velero backup by entering the following command:

    ``` terminal
    $ oc get backups.velero.io -n openshift-adp -o wide
    ```

2.  Inspect Velero logs for errors by entering the following command:

    ``` terminal
    $ oc logs -n openshift-adp deployment/velero
    ```

3.  Verify that the `HostedCluster` resource status reports a successful etcd backup URL by entering the following command:

    ``` terminal
    $ oc get hostedcluster <hosted_cluster_name> -n <hosted_cluster_namespace> \
      -o jsonpath='{.status.lastSuccessfulEtcdBackupURL}'
    ```

    A non-empty URL confirms that the etcd snapshot was captured and stored successfully.

</div>

## Restoring a hosted cluster on Azure from an etcd snapshot

You can restore a self-managed Azure hosted control plane from an etcd snapshot by using the HyperShift OADP plugin. The plugin automates the restore sequence through the Control Plane Operator and an `etcd-init` init container.

> [!IMPORTANT]
> The etcd snapshot method is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

The etcd snapshot restore sequence follows this order:

1.  The OADP plugin creates the `HostedCluster` resource and injects the etcd snapshot URL into the `spec.etcd.managed.storage.restoreSnapshotURL` field. The plugin sets this field automatically from the backup; you do not set it manually. The field is immutable after creation, enforced by validation, `MaxItems=1`.

2.  The Control Plane Operator detects the snapshot URL and adds an `etcd-init` init container to the etcd `StatefulSet`.

3.  The `etcd-init` container downloads the snapshot from Azure Blob Storage. During the restore, the OADP plugin generates a SAS-authenticated URL from the stored snapshot URL so that the `etcd-init` container can download the snapshot without direct access to credentials.

4.  After a successful restore, the Control Plane Operator sets the `EtcdSnapshotRestored` condition to `True` on the `HostedControlPlane` resource and removes the `etcd-init` init container. The container is not re-run on pod restart after `EtcdSnapshotRestored=True`.

> [!IMPORTANT]
> Cross-management-cluster restore is not currently supported. You can only restore to the same management cluster from which the backup was taken.

<div>

<div class="title">

Prerequisites

</div>

- You installed OADP 1.6 on the management cluster with the built-in `hypershift` plugin.

- You enabled the `HCPEtcdBackup` feature gate on the HyperShift Operator.

- You have a completed backup, including a valid etcd snapshot URL in the `HostedCluster.status.lastSuccessfulEtcdBackupURL` field.

- The Velero `BackupStorageLocation` for Azure Blob Storage is configured and accessible.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Delete the existing `HostedCluster` and its `NodePool` resources by entering the following command:

    ``` terminal
    $ hcp destroy cluster azure \
      --name <hosted_cluster_name> \
      --namespace <hosted_cluster_namespace>
    ```

    Replace `<hosted_cluster_name>` and `<hosted_cluster_namespace>` with the cluster to delete.

2.  Wait for the `HostedCluster` resource deletion to complete before proceeding by entering the following command:

    ``` terminal
    $ oc wait --for=delete hostedcluster/<hosted_cluster_name> \
      -n <hosted_cluster_namespace> --timeout=10m
    ```

3.  Verify that all etcd persistent volume claims (PVCs) are removed by entering the following command:

    ``` terminal
    $ oc get pvc -n <hosted_cluster_namespace>-<hosted_cluster_name>
    ```

    The command must return no resources. If PVCs remain, delete them before proceeding by entering the following command:

    ``` terminal
    $ oc delete pvc --all -n <hosted_cluster_namespace>-<hosted_cluster_name>
    ```

4.  Enter the OADP restore command to re-create the hosted cluster from the backup:

    ``` terminal
    $ hcp create oadp-restore \
      --hc-name <hosted_cluster_name> \
      --hc-namespace <hosted_cluster_namespace> \
      --from-backup <backup_name> \
      --use-etcd-snapshot
    ```

    where:

    `<hosted_cluster_name>`
    Specifies the name of the `HostedCluster` resource to restore.

    `<hosted_cluster_namespace>`
    Specifies the namespace of the `HostedCluster` resource.

    `<backup_name>`
    Specifies the name of the Velero `Backup` custom resource to restore from.

</div>

<div>

<div class="title">

Verification

</div>

1.  Check the `EtcdSnapshotRestored` condition on the `HostedControlPlane` resource by entering the following command:

    ``` terminal
    $ oc get hostedcontrolplane <hosted_cluster_name> -n <hosted_cluster_namespace>-<hosted_cluster_name> \
      -o jsonpath='{.status.conditions[?(@.type=="EtcdSnapshotRestored")].status}'
    ```

    The output must be `True`.

2.  Verify that the `HostedCluster` resource reports an `Available` status by entering the following command:

    ``` terminal
    $ oc get hostedcluster <hosted_cluster_name> -n <hosted_cluster_namespace> \
      -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'
    ```

    The output must be `True`.

3.  Inspect the etcd pod init container logs to confirm the snapshot download succeeded by entering the following command:

    ``` terminal
    $ oc logs -n <hosted_cluster_namespace>-<hosted_cluster_name> \
      statefulset/etcd -c etcd-init
    ```

    A successful restore produces an output message of `restored snapshot`.

    > [!NOTE]
    > The Control Plane Operator automatically removes the `etcd-init` init container after `EtcdSnapshotRestored=True`. This log check is only feasible while the restore is still in progress. If the container not in the etcd pod because the restore has already completed, check the `EtcdSnapshotRestored` condition in the preceding step rather than the init container logs.

</div>

## Troubleshooting backup and restore for hosted control planes on Azure

If you experience issues during the backup and restore process for hosted control planes on Azure, review the likely causes to find a resolution.

| Symptom | Likely cause | Resolution |
|----|----|----|
| An XML error in `etcd-init` logs | The Azure shared access signature (SAS) token in the snapshot URL expired. | Regenerate the SAS token and run a new backup. Use the new backup name with the `hcp create oadp-restore` command. |
| A `curl 404` error in `etcd-init` logs | The blob URL in the snapshot is wrong or the blob was deleted. | Verify the backup snapshot URL by entering the following command: `oc get hostedcluster <name> -n <namespace> -o jsonpath='{.status.lastSuccessfulEtcdBackupURL}'`. Confirm that the blob exists in the Azure Storage container. |
| `not empty` error; etcd restore does not start | Existing etcd persistent volume claim (PVC) data is present from the previous cluster. | Delete the `HostedCluster` resource and confirm that all PVCs in the hosted cluster namespace are removed before you run the restore command. |
| Velero restore stuck; `Restore` custom resource (CR) does not progress | The Velero controller is not processing the `Restore` CR. | Check Velero pod logs by entering the following command: `oc logs -n openshift-adp deployment/velero`. Verify that the `DataProtectionApplication` (DPA) configuration is correct and the `BackupStorageLocation` is available. |

# Automated disaster recovery for hosted control planes on Azure

You can automate disaster recovery (DR) for hosted control planes on Microsoft Azure by using OpenShift API for Data Protection (OADP) 1.6. The OADP `hypershift` plugin automatically detects the platform and includes the required platform-specific resources in backup and restore operations.

The following limitations apply to OADP-based restore operations on hosted control planes on Azure:

Same-management-cluster-only restore
Cross-management-cluster restore is not currently supported for Azure. Only same-cluster restore, where you restore to the management cluster from which the backup was taken, is supported.

Compute node reprovisioning
Compute nodes are reprovisioned after a restore. Applications running on compute nodes experience downtime while the nodes are reprovisioned and rejoin the cluster. Plan for this disruption when scheduling recovery operations.

## Setting up automated disaster recovery for hosted control planes on Azure

You can automate disaster recovery (DR) for hosted control planes on Microsoft Azure by using OpenShift API for Data Protection (OADP) 1.6.

The OADP `hypershift` plugin auto-detects the platform and includes the required platform-specific resources in backup and restore operations.

<div>

<div class="title">

Prerequisites

</div>

- You installed OADP 1.6 on the management cluster. For instructions, see [Configuring OADP with Azure](../../backup_and_restore/application_backup_and_restore/installing/installing-oadp-azure.xml#installing-oadp-azure).

- You met the `HCPEtcdBackup` feature gate requirement and the etcd snapshot prerequisites listed in [Setting up backup and restore for hosted control planes on Azure](../../hosted_control_planes/hcp-deploy/hcp-deploy-azure.xml#hcp-azure-etcd-snapshot-setup_hcp-deploy-azure).

- You created an Azure Storage Account and Blob Container.

- You have the Azure service principal credentials with access to the Azure Blob Storage account.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Create a Kubernetes secret that provides OADP with access to the Azure Blob Storage account where backups are stored.

    1.  Create a credentials file with the following content:

        ``` ini
        AZURE_SUBSCRIPTION_ID=<azure_subscription_id>
        AZURE_TENANT_ID=<azure_tenant_id>
        AZURE_CLIENT_ID=<azure_client_id>
        AZURE_CLIENT_SECRET=<azure_client_secret>
        AZURE_RESOURCE_GROUP=<azure_resource_group>
        AZURE_CLOUD_NAME=<azure_cloud_name>
        ```

        where:

        `<azure_subscription_id>`
        Specifies the Azure subscription ID.

        `<azure_tenant_id>`
        Specifies the Azure Active Directory tenant ID.

        `<azure_client_id>`
        Specifies the client ID of the Azure service principal.

        `<azure_client_secret>`
        Specifies the client secret of the Azure service principal.

        `<azure_resource_group>`
        Specifies the Azure resource group that contains the storage account.

        `<azure_cloud_name>`
        Specifies the Azure cloud environment. Use `AzurePublicCloud` for standard Azure or `AzureUSGovernmentCloud` for Azure Government.

    2.  Create the secret in the `openshift-adp` namespace by entering the following command:

        ``` terminal
        $ oc create secret generic azure-credentials \
          --namespace openshift-adp \
          --from-file cloud=<path_to_credentials_file>
        ```

        Replace `<path_to_credentials_file>` with the path to the credentials file you created in the previous step.

2.  Create a `DataProtectionApplication` (DPA) custom resource to configure OADP with the Azure provider and the `hypershift` plugin.

    1.  Create a `DataProtectionApplication` manifest, as shown in the following example:

        ``` yaml
        apiVersion: oadp.openshift.io/v1alpha1
        kind: DataProtectionApplication
        metadata:
          name: dpa-azure
          namespace: openshift-adp
        spec:
          configuration:
            velero:
              defaultPlugins:
                - openshift
                - azure
                - csi
                - hypershift
          backupLocations:
            - velero:
                provider: azure
                default: true
                credential:
                  name: azure-credentials
                  key: cloud
                objectStorage:
                  bucket: <blob_container_name>
                  prefix: velero
                  config:
                    resourceGroup: <azure_resource_group>
                    storageAccount: <azure_storage_account_name>
        ```

        where:

        `<blob_container_name>`
        Specifies the name of the Azure Blob Storage container.

        `<azure_resource_group>`
        Specifies the Azure resource group containing the storage account.

        `<azure_storage_account_name>`
        Specifies the Azure Storage Account name.

    2.  Apply the manifest by entering the following command:

        ``` terminal
        $ oc apply -f dpa-azure.yaml
        ```

    3.  Verify that the `BackupStorageLocation` is available by entering the following command:

        ``` terminal
        $ oc get backupstoragelocation -n openshift-adp
        ```

        The output must show a `Phase` of `Available`.

3.  Create a Velero `Backup` CR to back up the hosted control plane and associated Azure infrastructure resources.

    > [!NOTE]
    > The `hcp create oadp-backup` command auto-detects Azure and automatically includes the three required Azure Cluster API resources in the backup: `azureclusters`, `azuremachinetemplates`, and `azuremachines`. Using the CLI command is the recommended approach.

    - Run the backup command:

      ``` terminal
      $ hcp create oadp-backup \
        --hc-name <hosted_cluster_name> \
        --hc-namespace <hosted_cluster_namespace> \
        --storage-location azure-blob
      ```

    - Alternatively, apply a `Backup` manifest directly. The manifest must include the three Azure Cluster API resources in `includedResources`. The `includedResources` list below is illustrative; the CLI command might auto-detect additional resources not listed here. To generate a baseline manifest that matches the CLI output exactly, use `hcp create oadp-backup --render` and adjust as needed.

      <div class="formalpara">

      <div class="title">

      Example `Backup` manifest

      </div>

      ``` yaml
      apiVersion: velero.io/v1
      kind: Backup
      metadata:
        name: <backup_name>
        namespace: openshift-adp
      spec:
        storageLocation: azure-blob
        includedNamespaces:
          - <hosted_cluster_namespace>
          - <hosted_cluster_namespace>-<hosted_cluster_name>
        includedResources:
          - hostedclusters
          - nodepools
          - secrets
          - hostedcontrolplanes
          - azureclusters
          - azuremachinetemplates
          - azuremachines
        ttl: 720h0m0s
      ```

      </div>

      Replace `<backup_name>`, `<hosted_cluster_namespace>`, and `<hosted_cluster_name>` with the names of the backup and the cluster to back up.

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the backup completed successfully by entering the following command:

  ``` terminal
  $ oc get backup <backup_name> -n openshift-adp -o jsonpath='{.status.phase}'
  ```

  The output must be `Completed`.

</div>

## Restoring a hosted cluster on Azure

Restore a hosted control plane from an OADP backup. You can use the `hcp create oadp-restore` command or directly apply a Velero `Restore` custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- The existing `HostedCluster` resource is deleted and all etcd persistent volume claims (PVCs) are removed. For more information about etcd snapshot restore, see [Restoring etcd data by using the etcd snapshot method](../../hosted_control_planes/hcp_high_availability/hcp-backup-etcd-snapshot.xml#hcp-backup-etcd-snapshot-restore_hcp-backup-etcd-snapshot).

- The backup you are restoring from has a `Completed` status.

</div>

<div>

<div class="title">

Procedure

</div>

- To use the CLI to restore the hosted cluster, enter the following command:

  ``` terminal
  $ hcp create oadp-restore \
    --hc-name <hosted_cluster_name> \
    --hc-namespace <hosted_cluster_namespace> \
    --from-backup <backup_name>
  ```

  To restore from an etcd snapshot, add the `--use-etcd-snapshot` flag by entering the following command:

  ``` terminal
  $ hcp create oadp-restore \
    --hc-name <hosted_cluster_name> \
    --hc-namespace <hosted_cluster_namespace> \
    --from-backup <backup_name> \
    --use-etcd-snapshot
  ```

- To apply a `Restore` CR directly, enter the following command:

  ``` yaml
  apiVersion: velero.io/v1
  kind: Restore
  metadata:
    name: <restore_name>
    namespace: openshift-adp
  spec:
    backupName: <backup_name>
    restorePVs: true
    existingResourcePolicy: none
  ```

  - This `Restore` CR does not specify `includedNamespaces`. Velero restores all namespaces from the backup by default. The backup scopes resources to the hosted cluster namespaces (`<hosted_cluster_namespace>` and `<hosted_cluster_namespace>-<hosted_cluster_name>`), so the restore inherits that scope from the backup.

  - `existingResourcePolicy: none` is correct for a disaster recovery restore where the `HostedCluster` resource and all etcd PVCs have been deleted before the restore. If any resource remnants exist; for example, a stale finalizer held a resource, Velero skips them rather than overwriting them silently. If the restore fails due to remaining resources, stop the restore, clean the namespace manually, and retry.

</div>

<div>

<div class="title">

Verification

</div>

- Verify the restore completed by entering the following command:

  ``` terminal
  $ oc get restore <restore_name> -n openshift-adp -o jsonpath='{.status.phase}'
  ```

  The output must be `Completed`. If the output is `PartiallyFailed`, inspect restore warnings by entering the following command:

  ``` terminal
  $ oc describe restore <restore_name> -n openshift-adp
  ```

</div>

# Deleting an Azure hosted cluster and its resources

If you no longer need a hosted cluster, you can remove it and its infrastructure. Any related Workload Identities and OIDC issuers that were created during setup can be reused for other clusters or deleted separately if you no longer need them.

## Deleting a hosted cluster on Azure

If you are no longer using a hosted cluster on Azure, you can delete it.

<div>

<div class="title">

Procedure

</div>

- To delete a hosted cluster, enter the following command:

  ``` terminal
  $ hcp destroy cluster azure \
    --name $CLUSTER_NAME \
    --azure-creds $AZURE_CREDS \
    --dns-zone-rg-name $PERSISTENT_RG_NAME \
    --preserve-resource-group
  ```

  - `--name` specifies your hosted cluster name.

  - `--azure-creds` specifies an Azure credentials file that has permission to create infrastructure resources, such as virtual networks, subnets, and load balancers.

  - `--dns-zone-rg-name` specifies the name of the resource group that contains your DNS zone.

  - `--preserve-resource-group` specifies that the infrastructure will be preserved. If you do not want to preserve the infrastructure, do not include this flag.

</div>

## Deleting Azure infrastructure

If you have Azure infrastructure without a hosted cluster, you can remove the infrastructure if you are not using it.

For example, this scenario can happen if you created the infrastructure standalone but never created a hosted cluster. Or, you might have manually deleted the hosted cluster or management cluster, but the infrastructure resources still exist.

You can delete the entire infrastructure, or delete cluster-specific resources but preserve the main resource group. Preserving the main resource group is helpful when you have other resources in the same resource group that you want to keep.

If you have a hosted cluster and want to delete infrastructure while you delete the hosted cluster, follow the steps in "Deleting a hosted cluster on Azure", but omit the `--preserve-resource-group` flag.

<div>

<div class="title">

Procedure

</div>

- To delete the infrastructure, enter one of the following commands:

  - To delete the infrastructure, including the resource group, enter the following command:

    ``` terminal
    $ hcp destroy infra azure \
      --name <my_cluster_name> \
      --infra-id <infra_id> \
      --azure-creds <azure_credentials_file>
    ```

    - `--name` specifies your hosted cluster name.

    - `--infra-id` specifies a unique name that identifies your infrastructure. This value is used to name and tag Azure resources. Typically, it is the name of your cluster with a suffix appended to it.

    - `--azure-creds` specifies an Azure credentials file that has permission to create infrastructure resources, such as virtual networks, subnets, and load balancers.

  - To preserve the resource group but delete only cluster-specific resources, enter the following command:

    ``` terminal
    $ hcp destroy infra azure \
      --name <my_cluster_name> \
      --infra-id <infra_id> \
      --azure-creds <azure_credentials_file> \
      --preserve-resource-group
    ```

    - `--name` specifies your hosted cluster name.

    - `--infra-id` specifies a unique name that identifies your infrastructure. This value is used to name and tag Azure resources. Typically, it is the name of your cluster with a suffix appended to it.

    - `--azure-creds` specifies an Azure credentials file that has permission to create infrastructure resources, such as virtual networks, subnets, and load balancers.

    - `--preserve-resource-group` specifies that you want to preserve the resource group.

</div>

## Deleting Azure Workload Identities

As part of the process to delete a hosted cluster on Azure, you need to delete the Workload Identities.

To delete the Workload Identities, you enter a command on the hosted control planes command-line interface, `hcp`. The command uses the file that was generated when you created the Workload Identities to identify the identities to delete. Both the managed identities and their federated credentials are removed.

<div>

<div class="title">

Prerequisites

</div>

- If you created infrastructure by using the Workload Identities, delete the infrastructure before you delete the identities.

</div>

<div>

<div class="title">

Procedure

</div>

- Enter the following command:

  ``` terminal
  $ hcp destroy iam azure \
      --azure-creds <azure_credentials_file> \
      --workload-identities-file <workload_identities_file> \
      --resource-group-name <resource_group> \
      --name <my_cluster_name> \
      --infra-id <infra_id> \
      --dns-zone-rg-name <dns_zone_rg> \
      --cloud <my_cloud_environment>
  ```

  - `<azure_credentials_file>` specifies the Azure credentials file with permission to create managed identities and federated credentials.

  - `<workload_identities_file>` specifies the path to the Workload Identities JSON file, such as `my-cluster-name-iam-output.json`.

  - `<resource_group>` specifies the name of the resource group where you created identities.

  - `<my_cluster_name>` specifies the name of your hosted cluster.

  - `<infra_id>` specifies the unique identifier for naming Azure resources. Typically, this identifier is the cluster name with a suffix.

  - `<dns_zone_rg>` specifies the DNS zone resource group.

  - `<my_cloud_environment>` specifies the Azure cloud environment. Setting the `--cloud` flag is optional. The default value is `AzurePublicCloud`.

</div>

## Deleting a private hosted cluster on Azure

If you are no longer using a private hosted cluster on Azure, you can delete it.

The deletion process automatically cleans up Private Link resources in the following order:

1.  The Control Plane Operator removes the private endpoint, private DNS zones, VNet links, and A records.

2.  The `hcp destroy` command removes role-based access control (RBAC) role assignments.

3.  The HyperShift Operator removes Private Link.

<div>

<div class="title">

Procedure

</div>

- To delete a private hosted cluster, enter the following command:

  ``` terminal
  $ hcp destroy cluster azure \
    --name ${CLUSTER_NAME} \
    --azure-creds ${AZURE_CREDS} \
    --resource-group-name ${MANAGED_RG_NAME} \
    --dns-zone-rg-name ${DNS_ZONE_RG_NAME}
  ```

  - `--name` specifies your hosted cluster name.

  - `--azure-creds` specifies an Azure credentials file that has permission to create infrastructure resources, such as virtual networks, subnets, and load balancers. This flag is required because the `hcp destroy cluster azure` command cleans up RBAC role assignments before it deletes infrastructure.

  - `--resource-group-name` specifies the name of the resource group where you created identities.

  - `--dns-zone-rg-name` specifies the name of the resource group that contains your DNS zone.

</div>
