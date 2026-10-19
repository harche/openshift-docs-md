After a multi-node cluster is provisioned, you can adjust its capacity by adding, removing, or replacing worker nodes by updating the `ProvisioningRequest` custom resource. The O-Cloud Manager automatically coordinates hardware allocation, node provisioning, and cluster membership changes.

You can perform these operations by editing the `ProvisioningRequest` CR directly or through the Provisioning REST API. For more information about scaling with the Provisioning API, see "Scale worker nodes with the Provisioning API ".

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Add a worker node to a provisioned cluster

To increase available compute capacity, you can add a worker node to a multi-node cluster by appending a new node entry to the `ProvisioningRequest` custom resource (CR). The O-Cloud Manager allocates a matching bare-metal server from the resource pool, provisions it, and joins it to the cluster automatically.

<div class="note">

Scaling is supported only for worker nodes on multi-node clusters. You cannot add nodes to single-node OpenShift Container Platform clusters. Scaling and upgrade operations cannot run concurrently on the same cluster.

</div>

- The cluster is fully provisioned with `ClusterProvisioned=Completed` status on the `ProvisioningRequest` CR.

- Available `BareMetalHost` resources exist in the resource pool with labels matching the worker node group `resourceSelector` defined in the `ClusterTemplate` CR.

- The `ClusterTemplate` CR in use includes a `worker` entry in both `hwMgmtDefaults.nodeGroupData` and the `clusterinstance-defaults` ConfigMap.

- No upgrade operation is in progress on the cluster.

1.  Edit the `ProvisioningRequest` CR to append the new worker node to the worker group by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  Append the new node entry to the `worker` node group in `spec.templateParameters.clusterInstanceParameters.nodeGroups`:

    ``` yaml
    # ...
    spec:
      templateParameters:
        clusterInstanceParameters:
          nodeGroups:
            - name: master
              nodes:
                - hostName: master-1.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.11/24"]
                - hostName: master-2.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.12/24"]
                - hostName: master-3.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.13/24"]
            - name: worker
              nodes:
                - hostName: worker-1.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.21/24"]
                - hostName: worker-2.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.22/24"]
                - hostName: worker-3.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.23/24"]
            # ...
    ```

    - The new worker node `worker-3.cluster.example.com` is appended to the `worker` node group. The `nodeGroups[].name` must match an existing entry in the `clusterinstance-defaults` `ConfigMap` CR.

      <div class="note">

      If the cluster was provisioned from a 3-node template that does not include a `worker` group in the cluster instance default `ConfigMap` CR, you must first create a new `ClusterTemplate` CR version whose cluster instance default `ConfigMap` CR and `hwMgmtDefaults.nodeGroupData` section include the worker group. Update the `ProvisioningRequest` CR to reference the new template version, then add the worker nodes.

      </div>

3.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the `ProvisioningRequest` CR transitions back to `fulfilled` after the new node joins the cluster by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -o jsonpath='{.status.provisioningStatus.provisioningPhase}'
  ```

  The `ProvisioningRequest` CR transitions from `fulfilled` to `pending` to `progressing` and back to `fulfilled` once the new worker node is provisioned and reaches `Ready` state.

<!-- -->

- If the `provisioningPhase` shows `failed`, identify which phase encountered an error by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> \
    -o jsonpath='{.status.conditions}' | jq '.[] | select(.status=="False")'
  ```

  The output shows the condition that failed, with a `message` field describing the cause. Common failures include hardware allocation timeout when no `BareMetalHost` resources match the resource selector criteria.

# Remove a worker node from a provisioned cluster

To reduce compute capacity, you can remove a worker node from a multi-node cluster by removing its entry from the `ProvisioningRequest` custom resource (CR). The O-Cloud Manager coordinates the drain, resource cleanup, and hardware deallocation automatically.

<div class="note">

Only worker nodes can be removed. Attempting to remove a control-plane node is rejected by the O-Cloud Manager. Node removal and upgrade operations cannot run concurrently on the same cluster.

</div>

- The cluster is fully provisioned with `ClusterProvisioned=Completed` status on the `ProvisioningRequest` CR.

- No upgrade operation is in progress on the cluster.

1.  Edit the `ProvisioningRequest` CR to remove the target worker node from the worker group by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  Remove the target worker node entry from the `worker` node group in `spec.templateParameters.clusterInstanceParameters.nodeGroups`. The following example removes `worker-3.cluster.example.com`, scaling from 3 workers to 2 workers:

    ``` yaml
    # ...
    spec:
      templateParameters:
        clusterInstanceParameters:
          nodeGroups:
            - name: master
              nodes:
                - hostName: master-1.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.11/24"]
                - hostName: master-2.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.12/24"]
                - hostName: master-3.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.13/24"]
            - name: worker
              nodes:
                - hostName: worker-1.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.21/24"]
                - hostName: worker-2.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.22/24"]
            # ...
    ```

    <div class="note">

    To remove all worker nodes and scale back to a 3-node cluster, either clear the worker group’s `nodes` list or remove the entire `worker` node group from the `ProvisioningRequest` CR.

    </div>

3.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the `ProvisioningRequest` CR returns to `fulfilled` after the node is removed by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -o jsonpath='{.status.provisioningStatus.provisioningPhase}'
  ```

- `<uuid>`:: Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

  The `ProvisioningRequest` CR transitions from `fulfilled` to `pending` to `progressing` and back to `fulfilled` once the node removal completes and the deprovisioned server returns to `available` state.

<!-- -->

- If the `provisioningPhase` shows `failed`, identify which phase encountered an error by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> \
    -o jsonpath='{.status.conditions}' | jq '.[] | select(.status=="False")'
  ```

  The output shows the condition that failed, with a `message` field describing the cause.

# Replace a worker node in a provisioned cluster

You can replace one or more worker nodes in a single update to the `ProvisioningRequest` custom resource (CR). The O-Cloud Manager processes the replacement sequentially, removing the old nodes before provisioning new ones.

- The cluster is fully provisioned with `ClusterProvisioned=Completed` status on the `ProvisioningRequest` CR.

- Available `BareMetalHost` resources exist in the resource pool with labels matching the worker node group that you define in the `resourceSelector` field.

- No upgrade operation is in progress on the cluster.

1.  Edit the `ProvisioningRequest` CR to simultaneously remove old worker node entries and add new worker node entries in the worker node group by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  Remove the entries for the worker nodes you want to replace and add entries for the replacement nodes in the same edit, for example:

    ``` yaml
    # ...
    spec:
      templateParameters:
        clusterInstanceParameters:
          nodeGroups:
            - name: master
              nodes:
                - hostName: master-1.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.11/24"]
                - hostName: master-2.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.12/24"]
                - hostName: master-3.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.13/24"]
            - name: worker
              nodes:
                - hostName: worker-1.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.21/24"]
                - hostName: worker-4.cluster.example.com
                  nodeNetwork:
                    interfaces:
                      - name: eno1
                        addresses:
                          ipv4: ["192.0.2.24/24"]
    # ...
    ```

    - The old worker node entry `worker-2.cluster.example.com` is removed and a new entry `worker-4.cluster.example.com` is added in the same update.

3.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the `ProvisioningRequest` CR returns to `fulfilled` after the replacement completes by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -o jsonpath='{.status.provisioningStatus.provisioningPhase}'
  ```

  The `ProvisioningRequest` status shows `ClusterProvisioned=InProgress` throughout the swap, with the message reflecting which phase is active. The `provisioningPhase` returns to `fulfilled` when all replacement nodes have joined the cluster.

<!-- -->

- If the `provisioningPhase` shows `failed`, identify which phase encountered an error by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> \
    -o jsonpath='{.status.conditions}' | jq '.[] | select(.status=="False")'
  ```

  The output shows the condition that failed, with a `message` field describing the cause. Common failures include hardware allocation timeout when no `BareMetalHost` resources match the resource selector criteria.

# Cancel a scaling operation

You can cancel a node removal or node replacement operation by re-adding the removed worker nodes to the `ProvisioningRequest` custom resource (CR). The O-Cloud Manager detects the cancellation, stops the removal, and uncordons any nodes that were drained. Node addition operations cannot be canceled.

<div class="note">

Cancellation is only effective while the hardware manager is still draining the node. Once the node has been fully deprovisioned and `BareMetalHost` resource deprovisioning has started, the cancellation window has closed. Re-adding the node at that point triggers a new node addition, which waits for the server to finish deprovisioning before re-provisioning the node.

</div>

- A node removal or node replacement operation is in progress on the `ProvisioningRequest` CR.

- The removed nodes have not yet been fully deprovisioned.

1.  Edit the `ProvisioningRequest` CR to re-add the previously removed worker node entries to the worker group in `spec.templateParameters.clusterInstanceParameters.nodeGroups` by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  Restore the original node entries that were removed in the previous removal or replacement operation.

3.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

    The O-Cloud Manager cancels the removal operation and automatically uncordons any nodes that were drained. The cluster returns to normal operation.

- Verify that the `ProvisioningRequest` CR returns to `fulfilled` by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -o jsonpath='{.status.provisioningStatus.provisioningPhase}'
  ```

# Scale worker nodes with the Provisioning API

You can scale worker nodes through the Provisioning REST API by sending an update request with a modified `nodeGroups` array. To add a worker, append a new node entry to the worker group’s `nodes` list. To remove a worker, remove its entry from the list.

- You authenticated to the O-Cloud Manager REST API and set the `MY_TOKEN` environment variable.

- The cluster is fully provisioned and reports the `provisioningPhase: fulfilled` status.

- The `ClusterTemplate` CR in use includes a `worker` entry in both `hwMgmtDefaults.nodeGroupData` and the `clusterinstance-defaults` ConfigMap.

- If adding workers, available `BareMetalHost` resources exist in the resource pool matching the worker node group’s `resourceSelector` field.

- No upgrade operation is in progress on the cluster.

1.  Get the O-Cloud Manager API hostname by running the following command:

    ``` terminal
    $ export API_HOST=$(oc get routes -n oran-o2ims -o jsonpath='{.items[0].spec.host}')
    ```

2.  Set the Provisioning API base URL by running the following command:

    ``` terminal
    $ export PROV_URL="https://${API_HOST}/O2ims_infrastructureProvisioning/v1"
    ```

3.  Retrieve the current provisioning request by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${PROV_URL}/provisioningRequests/<uuid>" | jq '.provisioningRequestData' > current-request.json
    ```

    where:

    `<uuid>`
    Specifies the UUID of the provisioning request for the target cluster.

    `provisioningRequestData`
    The `provisioningRequestData` filter extracts the request payload from the API response envelope. The output is saved to `current-request.json`.

4.  Modify the `current-request.json` file to add or remove entries in the `templateParameters.clusterInstanceParameters.nodeGroups[].nodes` array. The following example adds a third worker node:

    ``` json
    {
      "name": "cluster1-provisioning-request",
      "description": "Multi-node RAN DU cluster at site-east-1",
      "provisioningRequestId": "<uuid>",
      "templateName": "std-ran-du",
      "templateVersion": "v4-Y-Z-1",
      "templateParameters": {
        "nodeClusterName": "cluster1",
        "oCloudSiteId": "site-east-1",
        "clusterInstanceParameters": {
          "clusterName": "cluster1",
          "nodeGroups": [
            {
              "name": "master",
              "nodes": [
                { "hostName": "master-1.example.com", "nodeNetwork": { "interfaces": [{ "name": "ens1f0", "addresses": { "ipv4": ["192.0.2.11/24"] } }] } },
                { "hostName": "master-2.example.com", "nodeNetwork": { "interfaces": [{ "name": "ens1f0", "addresses": { "ipv4": ["192.0.2.12/24"] } }] } },
                { "hostName": "master-3.example.com", "nodeNetwork": { "interfaces": [{ "name": "ens1f0", "addresses": { "ipv4": ["192.0.2.13/24"] } }] } }
              ]
            },
            {
              "name": "worker",
              "nodes": [
                { "hostName": "worker-1.example.com", "nodeNetwork": { "interfaces": [{ "name": "ens3f0", "addresses": { "ipv4": ["192.0.2.21/24"] } }] } },
                { "hostName": "worker-2.example.com", "nodeNetwork": { "interfaces": [{ "name": "ens3f0", "addresses": { "ipv4": ["192.0.2.22/24"] } }] } },
                { "hostName": "worker-3.example.com", "nodeNetwork": { "interfaces": [{ "name": "ens3f0", "addresses": { "ipv4": ["192.0.2.23/24"] } }] } }
              ]
            }
          ]
        }
      }
    }
    ```

    - `worker-3.example.com` is the new worker node hostname in this example. Each node must include a `nodeNetwork` section with interface addresses.

      <div class="note">

      The `PUT` request replaces the entire provisioning request. Retrieve the current state first, then send the complete modified payload. Do not send partial updates.

      </div>

5.  Send the updated provisioning request by running the following command:

    ``` terminal
    $ curl -ks -X PUT \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${MY_TOKEN}" \
      "${PROV_URL}/provisioningRequests/<uuid>" \
      -d @current-request.json | jq
    ```

    where:

    `<uuid>`
    Specifies the UUID of the provisioning request for the target cluster.

    `@current-request.json`
    Specifies the path to the file containing the updated provisioning request.

- Query the provisioning request status and verify that `provisioningPhase` returns to `fulfilled` by running the following command:

  ``` terminal
  $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
    "${PROV_URL}/provisioningRequests/<uuid>" | jq -r '.status.provisioningPhase'
  ```
