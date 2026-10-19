After you define cluster templates and onboard bare-metal servers, you can provision clusters by submitting a `ProvisioningRequest` custom resource (CR) with site-specific parameters. The O-Cloud Manager allocates hardware, installs the cluster, and applies Day 2 configuration automatically.

You can perform these operations by editing the `ProvisioningRequest` CR directly or through the Provisioning REST API. For more information about using the Provisioning API, see "Manage provisioning requests with the Provisioning API ".

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Provision a cluster using a ProvisioningRequest

You can provision a cluster by creating a `ProvisioningRequest` custom resource that references a validated `ClusterTemplate` CR and supplies site-specific parameters. The O-Cloud Manager validates the request, allocates hardware from resource pools, and orchestrates the end-to-end provisioning flow.

- You have `cluster-admin` permissions on the hub cluster.

- You prepared the O-Cloud Manager environment, including installing the O-Cloud Manager Operator and configuring the GitOps repository.

- You defined and applied a valid `ClusterTemplate` CR on the hub cluster.

- You onboarded bare-metal servers with resource selector labels matching the `ClusterTemplate` CR requirements.

1.  Create a `ProvisioningRequest` CR that references the `ClusterTemplate` CR and supplies site-specific parameters:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: ProvisioningRequest
    metadata:
      name: 123e4567-e89b-12d3-a456-426614174000
    spec:
      name: sno1-request
      description: "SNO cluster for site rack-a"
      templateName: sno-ran-du
      templateVersion: v4-Y-Z-1
      templateParameters:
        nodeClusterName: sno1
        oCloudSiteId: site-rack-a
        clusterInstanceParameters:
          clusterName: sno1
          nodeGroups:
            - name: master
              nodeNetwork:
                config:
                  dns-resolver:
                    config:
                      server:
                        - 192.0.2.22
              nodes:
              - hostName: sno1.example.com
                nodeNetwork:
                  interfaces:
                    - name: ens3f0
                      addresses:
                        ipv4: ["192.0.2.10/24"]
        policyTemplateParameters:
          cpu-isolated: "2-31"
          cpu-reserved: "0-1,32-33"
    ```

    - `metadata.name` must be a valid UUID. Any attempt to create a `ProvisioningRequest` CR with an invalid name is rejected by the webhook.

    - `spec.templateName` and `spec.templateVersion` identify the `ClusterTemplate` CR to use.

    - `spec.templateParameters.clusterInstanceParameters` provides site-specific values that are merged with the values in the `ConfigMap` CR that define the cluster instance defaults. The merged data is used to render the `ClusterInstance` CR.

    - `nodeGroups[].name` must match an existing `nodeGroups` entry in the `ConfigMap` CR that defines the cluster instance defaults. The interface name `nodeGroups[].nodes[].nodeNetwork.interfaces[].name` must also already exist in the defaults.

    - `spec.templateParameters.policyTemplateParameters` provides site-specific values for Day 2 configuration policies. These values take precedence over the defaults. Specify only values that differ from the defaults.

      <div class="note">

      You cannot override `extraLabels` and `extraAnnotations` keys that are already defined in the `clusterinstance-defaults` `ConfigMap` CR at the group or node level. You can only append new keys. All other fields follow standard merge rules where site-specific values take precedence over defaults.

      </div>

2.  Apply the `ProvisioningRequest` resource to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

    <div class="note">

    Each provisioning stage has a default timeout: 90 minutes for hardware provisioning, 90 minutes for cluster installation, and 30 minutes for cluster configuration. You can override these timeouts in the `ClusterTemplate` by setting `hardwareProvisioningTimeout` in `hwMgmtDefaults`, `clusterInstallationTimeout` in the `clusterinstance-defaults` ConfigMap, or `clusterConfigurationTimeout` in the `policytemplates-defaults` ConfigMap.

    </div>

- Verify that provisioning completes successfully by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io 123e4567-e89b-12d3-a456-426614174000
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME                                   DISPLAYNAME    AGE   PROVISIONPHASE   PROVISIONDETAILS
  123e4567-e89b-12d3-a456-426614174000   sno1-request   71m   fulfilled        The cluster provisioning has completed successfully
  ```

  A `provisioningPhase` of `fulfilled` indicates that hardware allocation, cluster installation, and configuration are all complete.

# Delete a provisioned cluster

You can delete a cluster provisioned by the O-Cloud Manager by deleting its `ProvisioningRequest` custom resource (CR). The O-Cloud Manager initiates a cleanup flow that removes the cluster, releases the allocated hardware, and returns the bare-metal servers to the resource pool for re-use.

- The cluster was provisioned using a `ProvisioningRequest` CR.

- You have `cluster-admin` permissions on the hub cluster.

1.  Delete the `ProvisioningRequest` CR by running the following command:

    ``` terminal
    $ oc delete provisioningrequests.clcm.openshift.io <uuid>
    ```

    - Replace `<uuid>` with the UUID of the `ProvisioningRequest` CR.

      <div class="note">

      Cluster deprovisioning and resource cleanup typically takes several minutes.

      </div>

2.  Monitor the deletion progress by running the following command, replacing `<uuid>` with the UUID of the `ProvisioningRequest` CR:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid> -w
    ```

    - Replace `<uuid>` with the UUID of the `ProvisioningRequest` CR.

      The resource is removed from the cluster after all cleanup operations complete.

- Verify that the `BareMetalHost` CR returns to the `Available` provisioning state:

  ``` terminal
  $ oc get bmh -A
  ```

  Servers in the `Available` state are ready to be allocated by a new `ProvisioningRequest` CR.

# Manage provisioning requests with the Provisioning API

You can create, monitor, update, and delete provisioning requests through the O-Cloud Manager Provisioning API. This interface is designed for Service Management and Orchestration (SMO) frameworks and external automation systems. The Provisioning API accepts the same parameters as the `ProvisioningRequest` custom resource (CR).

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables. For more information, see "Prepare the O-Cloud Manager environment".

- A validated `ClusterTemplate` CR exists on the hub cluster.

- Bare-metal servers with resource selector labels matching the `ClusterTemplate` CR requirements are onboarded.

1.  Set the Provisioning API base URL by running the following command:

    ``` terminal
    $ export PROV_URL="https://${API_BASE_URL}/O2ims_infrastructureProvisioning/v1"
    ```

2.  Create a provisioning request by running the following command:

    ``` terminal
    $ curl -ks -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${MY_TOKEN}" \
      "${PROV_URL}/provisioningRequests" -d \
      '{
        "provisioningRequestId": "123e4567-e89b-12d3-a456-426614174000",
        "name": "sno1-request",
        "description": "SNO cluster for site rack-a",
        "templateName": "sno-ran-du",
        "templateVersion": "v4-Y-Z-1",
        "templateParameters": {
          "nodeClusterName": "sno1",
          "oCloudSiteId": "site-rack-a",
          "clusterInstanceParameters": {
            "clusterName": "sno1",
            "nodeGroups": [
              {
                "name": "master",
                "nodes": [
                  {
                    "hostName": "sno1.example.com",
                    "nodeNetwork": {
                      "interfaces": [
                        {
                          "name": "ens3f0",
                          "addresses": { "ipv4": ["192.0.2.10/24"] }
                        }
                      ]
                    }
                  }
                ]
              }
            ]
          },
          "policyTemplateParameters": {
            "cpu-isolated": "2-31",
            "cpu-reserved": "0-1,32-33"
          }
        }
      }' | jq
    ```

    - The `provisioningRequestId` must be a valid UUID.

    - The `templateParameters` structure is identical to the `spec.templateParameters` field of the `ProvisioningRequest` CR. For details on each parameter, see *Provision a cluster using a ProvisioningRequest*.

      <div class="note">

      For advanced templating strategies and to configure hardware selection overrides for specific sites, see "Configure advanced hardware management".

      </div>

3.  Check provisioning status by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${PROV_URL}/provisioningRequests/123e4567-e89b-12d3-a456-426614174000" | jq -r '.status'
    ```

4.  Delete a provisioning request to deprovision the cluster by running the following command:

    ``` terminal
    $ curl -ks -X DELETE -H "Authorization: Bearer ${MY_TOKEN}" \
      "${PROV_URL}/provisioningRequests/123e4567-e89b-12d3-a456-426614174000"
    ```

- After creating a provisioning request, query its status and verify that the `provisioningPhase` progresses from `pending` to `progressing` to `fulfilled`.
