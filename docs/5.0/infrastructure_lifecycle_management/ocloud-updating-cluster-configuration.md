After a cluster is provisioned, you can apply configuration changes, update firmware, and modify cluster metadata by updating the `ProvisioningRequest` custom resource (CR) or by creating a new `ClusterTemplate` CR version with updated defaults. The O-Cloud Manager detects changes and orchestrates the Day 2 operations on the running cluster.

You can perform these operations by editing the `ProvisioningRequest` CR directly or through the Provisioning REST API. For more information about using the Provisioning API, see "Update cluster configuration with the Provisioning API".

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Update policy configuration parameters

When workload requirements change — for example, reallocating CPU cores between isolated and reserved sets, adjusting hugepage sizes, or tuning SR-IOV parameters — you can update Day 2 configuration values on a provisioned cluster by modifying the `policyTemplateParameters` field in the `ProvisioningRequest` custom resource (CR). The O-Cloud Manager propagates the updated values to the cluster policy `ConfigMap` CR, and Red Hat Advanced Cluster Management (RHACM) policies re-apply the configuration on the spoke cluster.

<div class="note">

Only policy configuration values exposed in the `spec.templateParameters.policyTemplateParameters` field of the associated `ClusterTemplate` CR can be updated through the `ProvisioningRequest` CR.

</div>

- The cluster is fully provisioned with `provisioningPhase: fulfilled` on the `ProvisioningRequest` CR.

- The parameters you want to update are defined in `spec.templateParameters.policyTemplateParameters` field of the associated `ClusterTemplate` CR.

1.  Edit the `ProvisioningRequest` CR by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  Update the configuration parameters to the desired values:

    ``` yaml
    # ...
    spec:
      templateParameters:
        policyTemplateParameters:
          sriov-network-vlan-1: "222"
          sriov-network-pfNames-1: '["ens2f0"]'
    # ...
    ```

    - `spec.templateParameters.policyTemplateParameters` contains the policy configuration values to update. The O-Cloud Manager writes these values to the cluster-specific `<cluster-name>-pg` ConfigMap resource in the `ztp-<clustertemplate-namespace>` namespace.

    - Values specified here take precedence over the defaults defined in the policy `ConfigMap` CR referenced by the `ClusterTemplate` CR.

3.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

    The O-Cloud Manager updates the `<cluster-name>-pg` `ConfigMap` CR with the new values. RHACM policies referencing these values report a `NonCompliant` status and are re-enforced on the spoke cluster.

- Verify that the configuration change was applied successfully by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid>
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME                                   DISPLAYNAME   AGE    PROVISIONPHASE   PROVISIONDETAILS
  123e4567-e89b-12d3-a456-426614174000                 90m    fulfilled        Provisioning request has completed successfully
  ```

  The `provisioningPhase` returns to `fulfilled` after all policies are re-enforced and compliant on the spoke cluster.

<!-- -->

- If the `provisioningPhase` shows `failed`, identify which policy is non-compliant by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> \
    -o jsonpath='{.status.extensions.policies}' | jq .
  ```

  The output lists each policy with its `compliant` status, `policyName`, and `remediationAction`. A policy with `"compliant": "NonCompliant"` indicates the configuration that failed to apply on the spoke cluster.

# Update cluster labels and annotations

When you need to change how policies target a cluster, for example adding operational metadata to indicate maintenance windows, you can update labels and annotations on a provisioned cluster and its nodes by modifying the `clusterInstanceParameters` field in the `ProvisioningRequest` custom resource (CR). The O-Cloud Manager propagates the changes to the `ManagedCluster` and `BareMetalHost` CRs on the hub cluster.

<div class="note">

`ManagedCluster` and node labels and annotations are the only `clusterInstanceParameters` fields that can be edited after cluster installation. All other fields are immutable and are rejected by the O-Cloud Manager.

</div>

- The cluster is fully provisioned with `provisioningPhase: fulfilled` on the `ProvisioningRequest` CR.

1.  Edit the `ProvisioningRequest` CR to update cluster-level or node-level labels and annotations by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

    To add or update cluster-level labels and annotations, modify the `extraLabels` and `extraAnnotations` fields, for example:

    ``` yaml
    # ...
    spec:
      templateParameters:
        clusterInstanceParameters:
          extraAnnotations:
            ManagedCluster:
              environment: production
          extraLabels:
            ManagedCluster:
              region: us-east
    # ...
    ```

    To add or update node-level labels and annotations, modify the node entries within the appropriate node group, for example:

    ``` yaml
    # ...
    spec:
      templateParameters:
        clusterInstanceParameters:
          nodeGroups:
          - name: master
            nodes:
            - hostName: worker-1.cluster.example.com
              extraAnnotations:
                BareMetalHost:
                  maintenance-window: "saturday-0200"
              extraLabels:
                BareMetalHost:
                  rack: rack-a
          # ...
    ```

    - Cluster-level changes are propagated to the `ManagedCluster` CR on the hub cluster.

    - Node-level changes are propagated to the corresponding `BareMetalHost` CRs.

2.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the update was applied successfully by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid>
  ```

- `<uuid>`:: Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME                                   DISPLAYNAME   AGE   PROVISIONPHASE   PROVISIONDETAILS
  123e4567-e89b-12d3-a456-426614174000                 90m   fulfilled        Provisioning request has completed successfully
  ```

  The `provisioningPhase` returns to `fulfilled` after the label and annotation changes are applied to the spoke cluster.

# Update ClusterInstance defaults with template versioning

When cluster-wide installation defaults need to change, for example updating NTP servers or base networking configuration across the fleet, you can update the `ClusterInstance` defaults for a provisioned cluster by creating a new version of the defaults ConfigMap resource, a new `ClusterTemplate` custom resource referencing it, and then updating the `ProvisioningRequest` CR to reference the new template version. Because `ClusterTemplate` CRs and their referenced `ConfigMap` CRs are immutable after validation, each change requires new versions of these resources. This approach preserves the previous configuration as a versioned artifact.

<div class="note">

Some `ClusterInstance` fields are immutable after cluster installation. The SiteConfig Operator rejects changes to fields protected by webhooks from underlying Operators. Editable fields include extra labels, extra annotations, and similar metadata.

</div>

- The cluster is fully provisioned with `provisioningPhase: fulfilled` on the `ProvisioningRequest` CR.

- The GitOps repository is configured and ArgoCD synchronizes resources to the hub cluster.

1.  Create a new version of the `ClusterInstance` defaults ConfigMap resource with the desired updates:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: clusterinstance-defaults-v2
      namespace: <template_namespace>
    data:
      clusterinstance-defaults: |
        clusterImageSetNameRef: "4.Y.Z"
        extraAnnotations:
          ManagedCluster:
            new-annotation: "value"
    ```

    where:

    `<template_namespace>`
    Specifies the namespace where `ClusterTemplate` CRs and associated ConfigMap resources are stored.

    - Update the `metadata.name` to a new version identifier (for example, `clusterinstance-defaults-v2`).

    - Modify only the fields you want to change in the `data.clusterinstance-defaults` section.

2.  Create a new `ClusterTemplate` CR version referencing the updated ConfigMap resource:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: ClusterTemplate
    metadata:
      name: sno-ran-du.v4-Y-Z-2
      namespace: <template_namespace>
    spec:
      name: sno-ran-du
      version: v4-Y-Z-2
      release: "4.Y.Z"
      templateDefaults:
        clusterInstanceDefaults: clusterinstance-defaults-v2
        policyTemplateDefaults: policytemplates-defaults-v1
        hwMgmtDefaults:
          nodeGroupData:
            - name: controller
              role: master
              resourceSelector:
                server-type: <server_type>
    ```

    - Update `metadata.name` and `spec.version` to the new version.

    - Set `spec.templateDefaults.clusterInstanceDefaults` to reference the new ConfigMap resource.

    - The `hwMgmtDefaults` and `policyTemplateDefaults` sections must match the original `ClusterTemplate` CR.

3.  Commit the new resources to the GitOps repository and wait for ArgoCD to synchronize them to the hub cluster.

4.  Update the `ProvisioningRequest` CR to reference the new `ClusterTemplate` version by running the following command:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateVersion":"v4-Y-Z-2"}}'
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

5.  The O-Cloud Manager detects the template version change, updates the `ClusterInstance` CR with the new defaults, and the SiteConfig Operator applies the changes to the spoke cluster.

- Verify that the update succeeds by checking the `ProvisioningRequest` CR status by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -o jsonpath='{.status.provisioningStatus.provisioningPhase}'
  ```

  The `provisioningPhase` returns to `fulfilled` after the changes are applied. Any issues are reported in `status.conditions`.

# Update firmware and BIOS settings on running clusters

When you need to update firmware patches, or when performance tuning demands updated BIOS settings such as enabling or disabling hyperthreading, you can update firmware versions and BIOS settings on a provisioned cluster by creating a new `HardwareProfile` custom resource (CR) and updating the `ProvisioningRequest` CR to reference it. The O-Cloud Manager coordinates a rolling update across node groups, applying changes with minimal workload disruption.

The Day 2 firmware update differs from Day 0 provisioning in the following ways:

- Node groups are processed by role: control-plane nodes are updated serially first, then worker nodes.

- Worker nodes can be updated in parallel based on the `maxUnavailable` setting from the corresponding `MachineConfigPool` on the spoke cluster.

- On multi-node clusters, each node is cordoned and drained before firmware is applied. On single-node OpenShift Container Platform clusters, cordon and drain are skipped.

<!-- -->

- The cluster is fully provisioned with `provisioningPhase: fulfilled` on the `ProvisioningRequest` CR.

- The `ClusterTemplate` CR defines `hwMgmtParameters` in its `spec.templateParameterSchema` to accept hardware profile overrides.

- No other firmware update or upgrade operation is in progress.

- The firmware download URLs in the new `HardwareProfile` CR are accessible from the BMC management network.

- Optional: Adjust the `maxUnavailable` setting on the worker `MachineConfigPool` on the spoke cluster to control how many worker nodes are updated in parallel.

1.  Create a new `HardwareProfile` CR with the desired firmware versions and BIOS settings:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: HardwareProfile
    metadata:
      name: <new_hardware_profile_name>
      namespace: oran-o2ims
    spec:
      bios:
        attributes:
          BootMode: Uefi
          WorkloadProfile: HpcProfile
      bmcFirmware:
        version: "<target_bmc_version>"
      biosFirmware:
        version: "<target_bios_version>"
    ```

    where:

    `<new_hardware_profile_name>`
    Specifies a descriptive name for the new hardware profile, such as `server-type-bios-2.6.3-bmc-7.20.30.50`.

    `<target_bios_version>`
    Specifies the target BIOS firmware version.

    `<target_bmc_version>`
    Specifies the target BMC firmware version.

    <div class="note">

    All firmware fields in the `HardwareProfile` CR are optional. Specify only the components you need to update. For example, define only `spec.bios.attributes` without any firmware version fields to update BIOS settings without changing firmware versions.

    </div>

2.  Apply the new `HardwareProfile` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

3.  Update the `ProvisioningRequest` CR to reference the new `HardwareProfile` by running the following command:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateParameters":{"hwMgmtParameters":{"nodeGroupData":[{"name":"<node_group>","hwProfile":"<new_hardware_profile_name>"}]}}}}'
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

    `<node_group>`
    Specifies the node group to update, such as `controller` or `worker`.

    `<new_hardware_profile_name>`
    Specifies the name of the new `HardwareProfile` CR.

    The O-Cloud Manager detects the profile change and propagates it through the `NodeAllocationRequest` CR to the hardware manager. The hardware manager computes the firmware differences, updates the Metal3 `HostFirmwareSettings` and `HostFirmwareComponents` CRs, and triggers host reboots to apply the updates.

- Verify that the firmware update completed successfully by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid>
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME                                   DISPLAYNAME   AGE    PROVISIONPHASE   PROVISIONDETAILS
  123e4567-e89b-12d3-a456-426614174000                 150m   fulfilled        Provisioning request has completed successfully
  ```

  The `provisioningPhase` returns to `fulfilled` after all nodes have been updated and validated.

<!-- -->

- If the `provisioningPhase` shows `failed`, identify which node encountered an error by running the following command:

  ``` terminal
  $ oc get allocatednodes.clcm.openshift.io -A \
    -o custom-columns=NAME:.metadata.name,REASON:.status.conditions[*].reason,MSG:.status.conditions[*].message
  ```

  A node with `reason: Failed` or `reason: TimedOut` indicates the node that requires attention. Check the corresponding `HostFirmwareComponents` and `HostFirmwareSettings` CRs on the affected `BareMetalHost` for further details.

# Retry a failed configuration change

When a Day 2 configuration change fails due to transient issues such as network connectivity, policy rendering errors, or firmware download timeouts, you can retry the operation by updating the `ProvisioningRequest` custom resource (CR) specifications. The O-Cloud Manager detects the change and starts a new configuration attempt.

<div class="note">

Configuration timeouts and failures can be retried by updating the relevant fields in the `ProvisioningRequest` CR. However, provisioning timeouts and failures cannot be retried. If a provisioning timeout or failure occurs, the `ProvisioningRequest` CR must be deleted and recreated.

</div>

- A Day 2 configuration change on the `ProvisioningRequest` CR has failed or timed out (`HardwareConfigured` or `ConfigurationApplied` condition shows `reason: TimedOut` or `reason: Failed`).

1.  Check the status conditions by running the following command:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid> -o yaml
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

    Look for the `HardwareConfigured` or `ConfigurationApplied` condition with `reason: TimedOut` or `reason: Failed` and review the `message` field for details.

2.  For hardware configuration failures, check the `BareMetalHost` state before retrying by running the following command:

    ``` terminal
    $ oc get bmh -n <bmh_namespace>
    ```

    where:

    `<bmh_namespace>`
    Specifies the namespace containing the `BareMetalHost` resources.

    <div class="important">

    If a `BareMetalHost` is in `servicing` state, wait for it to complete before retrying. If a `BareMetalHost` is in `servicing error` state, the retry might not succeed, especially for persistent power management errors.

    </div>

3.  Update the `ProvisioningRequest` spec to trigger a new configuration attempt by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    Make any spec change to the `ProvisioningRequest` CR, such as updating the `hwMgmtParameters` to reference a corrected `HardwareProfile` CR or adjusting `policyTemplateParameters` values.

    The O-Cloud Manager increments the internal `ConfigTransactionId`, clears the terminal state, and starts a new configuration attempt.

- Verify that the configuration attempt succeeds by monitoring the relevant condition by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -w
  ```

  The `provisioningPhase` transitions from `failed` to `pending` to `progressing` and back to `fulfilled` on successful completion.

# Update cluster configuration with the Provisioning API

You can update Day 2 configuration on a provisioned cluster through the Provisioning REST API by sending an update request with modified `policyTemplateParameters` values. This method is used by SMO frameworks and external automation systems that manage clusters programmatically. To apply new template defaults, you must first create a new `ClusterTemplate` CR version on the hub cluster because `ClusterTemplate` CRs and their referenced `ConfigMap` CRs are immutable after validation.

- You authenticated to the O-Cloud Manager REST API and set the `MY_TOKEN` environment variable.

- The cluster is fully provisioned with `provisioningPhase: fulfilled`.

- If updating template defaults, a new `ClusterTemplate` CR version with the updated `ConfigMap` CRs exists and is validated on the hub cluster.

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

4.  Modify the `current-request.json` file to update the values in `templateParameters.policyTemplateParameters`. The following example changes CPU allocation parameters:

    ``` json
    {
      "name": "sno1-provisioning-request",
      "description": "SNO RAN DU cluster at site-east-1",
      "provisioningRequestId": "<uuid>",
      "templateName": "sno-ran-du",
      "templateVersion": "v4-Y-Z-1",
      "templateParameters": {
        "nodeClusterName": "sno1",
        "oCloudSiteId": "site-east-1",
        "policyTemplateParameters": {
          "cpu-isolated": "2-63",
          "cpu-reserved": "0-1"
        },
        "clusterInstanceParameters": {
          "clusterName": "sno1",
          "nodeGroups": [ ... ]
        }
      }
    }
    ```

    - Only parameters defined in the `ClusterTemplate` CR’s `templateParameterSchema` are accepted.

    - To apply new template defaults, update `templateVersion` to reference a new `ClusterTemplate` version with the updated `ConfigMap` defaults.

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

- Query the provisioning request status and verify that configuration is applied by running the following command:

  ``` terminal
  $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
    "${PROV_URL}/provisioningRequests/<uuid>" | jq -r '.status.provisioningPhase'
  ```

  The `provisioningPhase` transitions from `progressing` to `fulfilled` when the updated policies are applied on the spoke cluster.
