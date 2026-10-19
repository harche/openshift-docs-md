After provisioning clusters with a basic template, you can configure advanced hardware management to control how the O-Cloud Manager selects hosts, applies hardware profiles, and handles specific site variation. This includes defining resource selectors with hardware data criteria in the `ClusterTemplate` CR and overriding template defaults in the `ProvisioningRequest` CR for individual deployment sites.

You can perform these operations by editing the `ProvisioningRequest` CR directly or through the Provisioning REST API. For more information about advanced provisioning with the Provisioning API, see "Provision with hardware overrides using the Provisioning API".

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Template reuse strategies

Every `ClusterTemplate` CR defines base hardware requirements in its `hwMgmtDefaults` section, including node groups, roles, and resource selectors that the O-Cloud Manager uses to automatically select hosts from the available pool. When you deploy the same template across multiple sites, you can use the following approaches for handling hardware variation.

Define hardware selection in the template
Use the `hwMgmtDefaults` section of the `ClusterTemplate` CR to specify node groups and resource selectors. This is the base configuration that applies to all clusters provisioned with this template. You can use label selectors, `hardwaredata/` selectors, or both to match hosts. For details, see "Select hosts by hardware specifications".

Override template defaults for each site
Use this approach when deployments share the same cluster topology, OpenShift Container Platform release version, and Day 2 configuration policies but differ in hardware at each site, such as server model, firmware profile, or rack location. The `ProvisioningRequest` CR supplies site-specific values in `hwMgmtParameters` that override the `ClusterTemplate` CR’s `hwMgmtDefaults` at provisioning time. This avoids creating a separate template for every site. For details, see "Override hardware profiles for each deployment site".

Create a new `ClusterTemplate` CR
Use this approach when deployments differ in cluster topology (single-node versus multi-node), node count, OpenShift Container Platform release version, or Day 2 policy configuration. These structural differences require a separate template because they affect installation flow, `ConfigMap` defaults, or policy rendering beyond what hardware overrides can address.

<div class="note">

`ClusterTemplate` CRs and their referenced `ConfigMap` CRs are immutable after validation by the O-Cloud Manager. To change `hwMgmtDefaults` or any other template default, you must create a new `ClusterTemplate` CR version and update the `ProvisioningRequest` CR to reference it.

</div>

# Select hosts by hardware specifications

You can define the base hardware selection criteria in a `ClusterTemplate` CR using the `resourceSelector` field in `hwMgmtDefaults` specification.

The `resourceSelector` field supports both label selectors that match `BareMetalHost` CR labels and `hardwaredata/` selectors that match against the inspected `HardwareData` CR for physical characteristics such as CPU, memory, NICs, and storage devices. You can use either or both together. This base configuration applies to all clusters provisioned with this template unless overridden with the `hwMgmtParameters` field in the `ProvisioningRequest` CR.

- The O-Cloud Manager Operator is installed on the hub cluster.

- Bare-metal servers are onboarded and their `HardwareData` CRs are populated by Bare Metal Operator inspection.

- If your template references `HardwareProfile` CRs, those CRs must exist in the O-Cloud Manager Operator namespace ,`oran-o2ims`, regardless of the namespace where the `ClusterTemplate` CR is stored.

1.  Define the `resourceSelector` in your `ClusterTemplate` CR’s `hwMgmtDefaults.nodeGroupData[]` entry to include hardware data criteria. The following example selects hosts with at least 64 CPU threads, 128 GiB RAM, four 25 Gbps NICs, and two NVMe storage devices:

    ``` yaml
    # ...
    spec:
      templateDefaults:
        hwMgmtDefaults:
          nodeGroupData:
            - name: controller
              role: master
              resourceSelector:
                server-type: dell-xr8620t
                hardwaredata/cpu_model;substring;icase: "Xeon"
                hardwaredata/num_threads;gte: "64"
                hardwaredata/ramMebibytes;gte: "131072"
                hardwaredata/nics;speedGbps>=25;count>=4: "present"
                hardwaredata/storage;type==NVME;count>=2: "present"
    # ...
    ```

    where:

    `server-type: dell-xr8620t`
    A label selector. Short keys without a domain prefix are automatically expanded to `resourceselector.clcm.openshift.io/server-type`. The label must exist on the `BareMetalHost` CR’s `metadata.labels`. You can use fully qualified keys such as `resourceselector.clcm.openshift.io/server-colour` directly.

    `hardwaredata/cpu_model;substring;icase: "Xeon"`
    A string field selector with qualifiers. The `hardwaredata/` prefix indicates matching against the `HardwareData` CR. Available string fields:

    - `productname` - system product name

    - `manufacturer` - system manufacturer

    - `cpu_arch` - CPU architecture such as `x86_64` or `arm64`

    - `cpu_model` - CPU model string

    `hardwaredata/num_threads;gte: "64"`
    An integer field selector with a comparison operator. Available integer fields:

    - `num_threads` - CPU thread count

    - `ramMebibytes` - RAM size in mebibytes

      All values must be quoted strings.

    `hardwaredata/nics;speedGbps>=25;count>=4: "present"`
    A NIC compound selector. NIC criteria use the `hardwaredata/nics` prefix followed by semicolon-separated sub-criteria. The value must always be `"present"`. Available NIC sub-criteria:

    - `model` - NIC model string

    - `speedGbps` - NIC speed in Gbps

    - `count` - number of NICs matching the other sub-criteria

      When `model` or `speedGbps` are specified, they filter the NIC set first. The `count` sub-criterion is then evaluated against the filtered subset.

    `hardwaredata/storage;type==NVME;count>=2: "present"`
    A storage compound selector. Storage criteria use the `hardwaredata/storage` prefix followed by semicolon-separated sub-criteria. The value must always be `"present"`. Available storage sub-criteria:

    - `type` - storage type: `NVME`, `SSD`, or `HDD`

    - `model` - device model string

    - `vendor` - device vendor string

    - `name` - device name or alternate name

    - `sizeBytes` - device size in bytes

    - `count` - number of devices matching the other sub-criteria

      <div class="note">

      All criteria within a `resourceSelector` must match for a `BareMetalHost` CR to be selected. Only hosts in the `Available` provisioning state are evaluated.

      </div>

2.  Apply the `ClusterTemplate` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the `ClusterTemplate` passes validation by running the following command:

  ``` terminal
  $ oc get clustertemplates.clcm.openshift.io -A
  ```

  A `STATE` of `Completed` confirms that the template and its resource selector configuration are valid.

# Override hardware profiles for each deployment site

When deployments share the same cluster topology but differ in hardware at each site, you can use a single `ClusterTemplate` CR across multiple deployment sites by overriding the template’s `hwMgmtDefaults` in each `ProvisioningRequest` CR. The `hwMgmtParameters` field in the `ProvisioningRequest` supplies site-specific values such as server model, firmware profile, or resource selector criteria, which avoids creating a separate template for every site.

- The O-Cloud Manager Operator is installed on the hub cluster.

- A validated `ClusterTemplate` CR exists with `hwMgmtParameters` defined in its `templateParameterSchema`.

- Bare-metal servers at the target site are onboarded with labels matching the override criteria.

1.  Ensure the `ClusterTemplate` CR includes `hwMgmtParameters` in the `templateParameterSchema` to permit overrides. The following snippet shows the required schema section for this example:

    ``` yaml
    # ...
    spec:
      templateParameterSchema:
        properties:
          hwMgmtParameters:
            properties:
              hardwareProvisioningTimeout:
                type: string
              nodeGroupData:
                items:
                  properties:
                    name:
                      type: string
                    hwProfile:
                      type: string
                    resourceSelector:
                      type: object
                      additionalProperties:
                        type: string
                  required:
                    - name
                  type: object
                type: array
            type: object
    # ...
    ```

    The `hwMgmtParameters` schema defines which fields a `ProvisioningRequest` CR can override. Only fields declared in the schema are accepted during validation.

2.  Create a `ProvisioningRequest` CR that includes `hwMgmtParameters` in `templateParameters` to override the template defaults for this site, for example:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: ProvisioningRequest
    metadata:
      name: a1b2c3d4-e5f6-7890-abcd-ef1234567890
    spec:
      name: site-boston-rack3
      description: "Cluster for Boston site using local server model"
      templateName: sno-ran-du
      templateVersion: v4-Y-Z-1
      templateParameters:
        nodeClusterName: boston-sno1
        oCloudSiteId: site-boston-rack3
        hwMgmtParameters:
          hardwareProvisioningTimeout: "120m"
          nodeGroupData:
            - name: controller
              hwProfile: rh-profile-xr8620t-bios-settings
              resourceSelector:
                server-type: dell-xr8620t
        clusterInstanceParameters:
          clusterName: boston-sno1
          baseDomain: boston.example.com
          nodes:
            - hostName: boston-sno1.boston.example.com
        policyTemplateParameters:
          cpu-isolated: "2-63"
          cpu-reserved: "0-1"
    ```

    where:

    `hwMgmtParameters.hardwareProvisioningTimeout`
    Overrides the timeout duration for hardware provisioning at this site. If not specified, the value from the `ClusterTemplate` CR’s `hwMgmtDefaults` section applies.

    `hwMgmtParameters.nodeGroupData[].name`
    Identifies the node group to override. This value must match the `name` field of a node group in the template’s `hwMgmtDefaults.nodeGroupData[]`. Node groups are matched by name.

    `hwMgmtParameters.nodeGroupData[].hwProfile`
    Overrides the `HardwareProfile` CR for this node group at this site. For example, a site with Dell XR8620t servers uses a different firmware profile than a site with HPE DL110 servers.

    `hwMgmtParameters.nodeGroupData[].resourceSelector`
    Overrides or adds resource selector criteria for this node group. The O-Cloud Manager merges these values with the base selectors from the `ClusterTemplate` CR using the following rules:

    - Override values replace existing values for the same key.

    - New keys in the override are added to the base configuration.

    - Existing keys not present in the override are preserved unchanged.

    - Keys cannot be removed from the base template through an override.

      When both the `ClusterTemplate` CR and the `ProvisioningRequest` CR specify the same field, the `ProvisioningRequest` value takes precedence.

      <div class="note">

      Node groups in the override that do not match any existing group by name are appended as new groups. This supports scaling scenarios where a `ProvisioningRequest` CR adds a `worker` node group not defined in the template defaults.

      </div>

3.  Apply the `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the provisioning request is accepted and progressing by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io a1b2c3d4-e5f6-7890-abcd-ef1234567890
  ```

  A `provisioningPhase` of `fulfilled` indicates that the overridden hardware profile and resource selector were applied successfully and the cluster provisioning completed.

# Provision with hardware overrides using the Provisioning API

You can provision a cluster with per-site hardware overrides through the Provisioning REST API by including `hwMgmtParameters` in the POST request body.

- You authenticated to the O-Cloud Manager REST API and set the `MY_TOKEN` environment variable.

- A validated `ClusterTemplate` CR exists with `hwMgmtParameters` defined in the `templateParameterSchema`.

- Bare-metal servers matching the override `resourceSelector` criteria are onboarded.

1.  Get the O-Cloud Manager API hostname by running the following command:

    ``` terminal
    $ export API_HOST=$(oc get routes -n oran-o2ims -o jsonpath='{.items[0].spec.host}')
    ```

2.  Set the Provisioning API base URL by running the following command:

    ``` terminal
    $ export PROV_URL="https://${API_HOST}/O2ims_infrastructureProvisioning/v1"
    ```

3.  Create a provisioning request with hardware overrides by running the following command:

    ``` terminal
    $ curl -ks -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${MY_TOKEN}" \
      "${PROV_URL}/provisioningRequests" \
      -d @provisioning-request.json | jq
    ```

    The following example shows a `provisioning-request.json` file with `hwMgmtParameters` that override the template defaults:

    ``` json
    {
      "name": "sno-site-a-provisioning-request",
      "description": "SNO RAN DU cluster at site-a",
      "provisioningRequestId": "<uuid>",
      "templateName": "sno-ran-du",
      "templateVersion": "v4-Y-Z-1",
      "templateParameters": {
        "nodeClusterName": "sno-site-a",
        "oCloudSiteId": "site-a",
        "hwMgmtParameters": {
          "hardwareProvisioningTimeout": "120m",
          "nodeGroupData": [
            {
              "name": "controller",
              "hwProfile": "rh-profile-xr8620t-bios-settings",
              "resourceSelector": {
                "server-type": "dell-xr8620t",
                "location": "rack-3"
              }
            }
          ]
        },
        "clusterInstanceParameters": {
          "clusterName": "sno-site-a",
          "baseDomain": "site-a.example.com",
          "nodes": [
            { "hostName": "sno1.site-a.example.com" }
          ]
        },
        "policyTemplateParameters": {
          "cpu-isolated": "2-63",
          "cpu-reserved": "0-1"
        }
      }
    }
    ```

    - The `hwMgmtParameters` values override the `hwMgmtDefaults` defined in the `ClusterTemplate` CR.

    - Only fields included in the template’s `templateParameterSchema` are accepted.

    - The `resourceSelector` labels in `hwMgmtParameters` replace (not merge with) the template defaults for the specified node group.

      <div class="note">

      The `provisioningRequestId` must be a valid UUID. The O-Cloud Manager validates the supplied `hwMgmtParameters` against the schema defined in the referenced `ClusterTemplate` CR before starting provisioning.

      </div>

- Query the provisioning request status and verify that provisioning starts by running the following command:

  ``` terminal
  $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
    "${PROV_URL}/provisioningRequests/<uuid>" | jq -r '.status.provisioningPhase'
  ```

  The `provisioningPhase` transitions from `pending` to `progressing` as hardware provisioning begins, and reaches `fulfilled` when the cluster is fully provisioned and configured.
