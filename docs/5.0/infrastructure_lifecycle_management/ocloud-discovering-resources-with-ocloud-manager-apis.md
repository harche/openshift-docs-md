After you define cluster templates and onboard bare-metal servers, external clients such as Service Management and Orchestration (SMO) frameworks and automation systems can discover available infrastructure, templates, and provisioned clusters through the O-Cloud Manager REST APIs.

The Inventory API provides read-only access to locations, resource pools, and physical resources. The Artifacts API exposes available cluster templates. The Cluster API provides information about provisioned clusters.

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

- [O-Cloud Manager REST API reference](../infrastructure_lifecycle_management/ocloud-rest-api-reference.xml#ocloud-rest-api-reference)

# Query infrastructure resources

You can query the O-Cloud Manager Inventory API to discover available infrastructure resources, including locations, sites, resource pools, and physical servers. This enables a Service Management and Orchestration (SMO) framework or automation system to identify what infrastructure is available before submitting provisioning requests.

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables.

1.  List all resource pools by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/resourcePools" | jq
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` json
    [
      {
        "resourcePoolId": "7108c495-18c9-45ac-be47-e4b900c6f204",
        "oCloudSiteId": "fddfbbae-0fb3-402e-8408-6adbb6ba382a",
        "name": "dell-xr8620t-pool",
        "description": "Dell XR8620t compute resources",
        "extensions": {}
      }
    ]
    ```

2.  List the resources within a specific resource pool by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/resourcePools/<resource_pool_id>/resources" | jq
    ```

    - Replace `<resource_pool_id>` with the target `resourcePoolId` value.

      <div class="formalpara-title">

      **Example output**

      </div>

      ``` json
      [
        {
          "resourceId": "f3e79178-b199-4eb6-bfe3-b1417b7d5b8d",
          "resourcePoolId": "7208c495-18c9-45ac-be47-e4b900c6f204",
          "description": "XR8620t server",
          "resourceTypeId": "d1eabf91-f0e6-5170-97dc-797d35146dad",
          "globalAssetId": "296S2Z3",
          "extensions": {
            "adminState": "LOCKED",
            "operationalState": "DISABLED",
            "usageState": "IDLE",
            "powerState": "OFF",
            "vendor": "Dell Inc.",
            "model": "PowerEdge XR8620t"
          }
        }
      ]
      ```

    - A resource with `usageState: IDLE` and `adminState: LOCKED` is available for allocation by a new provisioning request.

      <div class="note">

      A `BareMetalHost` resource appears in the Inventory API only if it has a `resources.clcm.openshift.io/resourcePoolName` label and has completed hardware inspection. Servers that have not reached the `available` provisioning state or later do not appear in the API response.

      </div>

3.  List all locations to view geographic site information by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/locations" | jq
    ```

4.  List O-Cloud sites within a location by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/oCloudSites" | jq
    ```

5.  List resource types to understand the classification of discovered resources by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/resourceTypes" | jq
    ```

    Each resource in a resource pool references a `resourceTypeId` that maps to an entry in this list.

6.  List deployment managers to view the managed clusters acting as infrastructure management endpoints by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/deploymentManagers" | jq
    ```

7.  Filter resources by a specific field by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureInventory/v2/resourcePools?filter=(eq,name,<pool_name>)" | jq
    ```

    - Replace `<pool_name>` with the name of the resource pool to filter.

# Query available cluster templates

You can query the O-Cloud Manager Artifacts API to discover which cluster templates are available for provisioning.

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables.

- At least one validated `ClusterTemplate` custom resource (CR) exists on the hub cluster.

1.  List all available cluster templates by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureArtifacts/v1/managedInfrastructureTemplates" | jq
    ```

2.  Filter templates by name and version by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureArtifacts/v1/managedInfrastructureTemplates?filter=(eq,name,<template_name>);(eq,version,<template_version>)" | jq
    ```

    - Replace `<template_name>` with the base name of the `ClusterTemplate` CR, for example `sno-ran-du`.

    - Replace `<template_version>` with the template version, for example `v4-18-5-v1`.

3.  Get a specific template by its identifier by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureArtifacts/v1/managedInfrastructureTemplates/<template_id>" | jq
    ```

    - Replace `<template_id>` with the `managedInfrastructureTemplateId` value, which follows the format `<name>.<version>`, for example `sno-ran-du.v4-18-5-v1`.

4.  View the template defaults to understand the preconfigured values by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureArtifacts/v1/managedInfrastructureTemplates/<template_id>/defaults" | jq
    ```

    - Replace `<template_id>` with the `managedInfrastructureTemplateId` value, which follows the format `<name>.<version>`, for example `sno-ran-du.v4-18-5-v1`.

      <div class="formalpara-title">

      **Example output**

      </div>

      ``` json
      {
        "clusterInstanceDefaults": {
          "clusterImageSetNameRef": "4.Y.Z",
          "pullSecretRef": {
            "name": "pull-secret"
          },
          "templateRefs": [
            {
              "name": "ai-cluster-templates-v1",
              "namespace": "open-cluster-management"
            }
          ]
        },
        "policyTemplateDefaults": {
          "cpu-isolated": "2-63",
          "cpu-reserved": "0-1"
        }
      }
      ```

      The defaults response includes the merged content of the `clusterinstance-defaults` and `policytemplates-defaults` ConfigMap resources referenced by the `ClusterTemplate` CR.

# Query provisioned clusters

You can query the O-Cloud Manager Cluster API to discover clusters provisioned through the O-Cloud Manager, their types, and the individual nodes within them. Each managed cluster registered with RHACM corresponds to a node cluster in the API.

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables.

- You provisioned at least one cluster through the O-Cloud Manager.

1.  List all provisioned node clusters by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/nodeClusters" | jq
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` json
    [
      {
        "nodeClusterId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "nodeClusterTypeId": "d1eabf91-f0e6-5170-97dc-797d35146dad",
        "name": "my-sno-cluster",
        "description": "SNO RAN DU cluster",
        "extensions": {
          "clusterID": "c5e3f8a2-1b4d-4e6f-8a9b-0c1d2e3f4a5b",
          "platform": "BareMetal",
          "openshiftVersion": "4.20.4"
        }
      }
    ]
    ```

2.  Get details for a specific cluster by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/nodeClusters/<node_cluster_id>" | jq
    ```

    - Replace `<node_cluster_id>` with the `nodeClusterId` value.

3.  Filter clusters by name by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/nodeClusters?filter=(eq,name,<cluster_name>)" | jq
    ```

    - Replace `<cluster_name>` with the name of the cluster.

4.  List node cluster types to view the classification of managed clusters by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/nodeClusterTypes" | jq
    ```

    Each node cluster references a `nodeClusterTypeId` that maps to an entry in this list, categorizing clusters by platform and version.

5.  List individual nodes within a cluster by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/clusterResources" | jq
    ```

6.  Optional: Create a subscription to receive notifications when cluster resources change:

    1.  Create a cluster resource subscription by running the following command:

        ``` terminal
        $ curl -ks -X POST \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer ${MY_TOKEN}" \
          -d '{
            "consumerSubscriptionId": "69253c4b-8398-4602-855d-783865f5f25c",
            "filter": "",
            "callback": "https://smo.example.com/v1/o2ims_cluster_observer"
          }' \
          "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/subscriptions" | jq
        ```

        - `consumerSubscriptionId` must be a valid UUID identifying this subscription on the consumer side.

        - `callback` is the URL where the O-Cloud Manager sends change notifications. The host of the callback URL must match the domain of the registered SMO or external system. The path can differ. The callback URL must also be reachable from the hub cluster and respond to `GET` requests with a `204` status code. Unreachable endpoints are rejected at subscription creation time.

        - `filter` can be left empty to receive all change notifications.

    2.  List existing subscriptions by running the following command:

        ``` terminal
        $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
          "https://${API_BASE_URL}/O2ims_infrastructureCluster/v1/subscriptions" | jq
        ```
