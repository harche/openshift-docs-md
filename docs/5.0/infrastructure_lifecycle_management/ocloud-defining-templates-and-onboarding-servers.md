Before you can provision clusters with the O-Cloud Manager, you must define reusable cluster blueprints and register bare-metal servers in resource pools. These resources establish the hardware profiles, default configurations, and allocation criteria that the O-Cloud Manager uses when processing a provisioning request.

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Configure hardware profiles for bare-metal nodes

You can optionally define a `HardwareProfile` custom resource (CR) to specify the required firmware levels and BIOS settings for a class of bare-metal servers. The O-Cloud Manager applies the hardware profile during provisioning to ensure servers meet the required hardware state before cluster installation begins.

<div class="note">

Hardware profiles are optional. If you do not specify a hardware profile, the O-Cloud Manager skips firmware and BIOS configuration during provisioning and uses the server in its current hardware state.

</div>

- The O-Cloud Manager Operator is installed on the hub cluster.

- You know the target firmware versions and BIOS settings for your server hardware.

1.  Create a `HardwareProfile` CR that defines the required hardware state, such as the following example:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: HardwareProfile
    metadata:
      name: <hardware_profile_name>
      namespace: oran-o2ims
    spec:
      bios:
        attributes:
          BootMode: Uefi
          <bios_attribute_name>: <bios_attribute_value>
      bmcFirmware:
        version: "<bmc_firmware_version>"
        url: "<bmc_firmware_url>"
      biosFirmware:
        version: "<bios_firmware_version>"
        url: "<bios_firmware_url>"
      nicFirmware:
        - version: "<nic_firmware_version>"
          url: "<nic_firmware_url>"
    ```

    where:

    `<hardware_profile_name>`
    Specifies a descriptive name for the hardware profile, for example `server-type-bios-settings`. The `HardwareProfile` CR must be created in the O-Cloud Manager Operator namespace, `oran-o2ims`, regardless of the namespace where the `ClusterTemplate` CR is stored.

    `spec.bios.attributes`
    Defines the desired BIOS settings as key-value pairs.

    `spec.bmcFirmware`
    Defines the target BMC controller firmware. Configure a `version` and an optional `url` pointing to the firmware binary.

    `spec.biosFirmware`
    Defines the target BIOS firmware. Configure a `version` and an optional `url` pointing to the firmware binary.

    `spec.nicFirmware`
    Defines the target NIC firmware as a list, allowing you to specify firmware for multiple NICs. Each entry configures a `version` and an optional `url` pointing to the firmware binary.

    <div class="note">

    All firmware fields are optional. Specify only the components you need to manage. For example, you can define only `spec.bios.attributes` without any firmware fields if firmware management is not required.

    </div>

2.  Apply the `HardwareProfile` resource to the hub cluster, or commit it to the `hardwareprofiles/` directory in the GitOps repository for ArgoCD synchronization.

- Verify that the `HardwareProfile` resource exists on the hub cluster:

  ``` terminal
  $ oc get hardwareprofiles.clcm.openshift.io -A
  ```

# Onboard bare-metal servers to resource pools

You can register bare-metal servers with the O-Cloud Manager by defining an infrastructure hierarchy and creating `BareMetalHost` custom resources (CRs) with resource selector labels. Onboarded servers become available for allocation when a `ProvisioningRequest` CR references a `ClusterTemplate` CR with matching resource selectors.

- The O-Cloud Manager Operator is installed on the hub cluster.

- You have Baseboard Management Controller (BMC) credentials for each server.

1.  Create the infrastructure hierarchy by defining `Location`, `OCloudSite`, and `ResourcePool` CRs, for example:

    ``` yaml
    apiVersion: ocloud.openshift.io/v1alpha1
    # A geographic place. Specify at least one of address, coordinate, or civicAddress.
    kind: Location
    metadata:
      name: dc1
      namespace: <server_namespace>
    spec:
      description: "Data Center 1"
      address: "123 Example Street"
    ---
    apiVersion: ocloud.openshift.io/v1alpha1
    # A logical site at a Location. References the parent Location by name.
    kind: OCloudSite
    metadata:
      name: site-rack-a
      namespace: <server_namespace>
    spec:
      description: "Rack A at Data Center 1"
      globalLocationName: dc1
    ---
    apiVersion: ocloud.openshift.io/v1alpha1
    # A group of bare-metal resources at a site. References the parent OCloudSite by name.
    kind: ResourcePool
    metadata:
      name: <resource_pool_name>
      namespace: <server_namespace>
    spec:
      description: "<resource_pool_description>"
      oCloudSiteName: site-rack-a
    ```

    where:

    `<server_namespace>`
    Specifies the namespace where server and infrastructure resources are stored. The recommended convention is one namespace per resource pool.

    `<resource_pool_name>`
    Specifies a descriptive name for the resource pool, for example `compute-pool-1`.

    `<resource_pool_description>`
    Describes the purpose or hardware type of the resource pool.

2.  Create a `Secret` CR containing the BMC credentials for the server, for example:

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: <bmc_secret_name>
      namespace: <server_namespace>
    type: Opaque
    data:
      username: <base64_encoded_username>
      password: <base64_encoded_password>
    ```

    where:

    `<bmc_secret_name>`
    Specifies the name of the secret. This name is referenced by the `BareMetalHost` resource.

    `<base64_encoded_username>`
    Specifies the Base64-encoded BMC username.

    `<base64_encoded_password>`
    Specifies the Base64-encoded BMC password.

3.  Create a `BareMetalHost` CR with the required labels to associate the server with a resource pool, for example:

    ``` yaml
    apiVersion: metal3.io/v1alpha1
    kind: BareMetalHost
    metadata:
      name: <server_name>
      namespace: <server_namespace>
      labels:
        resources.clcm.openshift.io/resourcePoolName: <resource_pool_name>
        interfacelabel.clcm.openshift.io/boot-interface: <boot_interface_name>
        resourceselector.clcm.openshift.io/server-type: <server_type>
        resourceselector.clcm.openshift.io/rack-location: rack-a-row-3
      annotations:
        bmac.agent-install.openshift.io/allow-provisioned-host-management: ""
    spec:
      online: false
      bmc:
        address: redfish-virtualmedia+https://192.168.1.100/redfish/v1/Systems/System.Embedded.1
        credentialsName: <bmc_secret_name>
        disableCertificateVerification: true
    ```

    where:

    `<server_name>`
    Specifies a unique name for the `BareMetalHost` resource.

    `<server_namespace>`
    Specifies the namespace where server resources are stored. The recommended convention is one namespace per resource pool.

    `resources.clcm.openshift.io/resourcePoolName`
    Required. Must match an existing `ResourcePool` resource’s `metadata.name`. Links this server to the infrastructure hierarchy. Without this label, the server does not appear in the O-Cloud Manager inventory.

    `interfacelabel.clcm.openshift.io/boot-interface`
    Required if `spec.bootMACAddress` is not set. Specifies the physical NIC name used for booting, for example `ens3f0`. The O-Cloud Manager uses this label to resolve the boot MAC address from hardware inventory data.

    `resourceselector.clcm.openshift.io/server-type`
    Optional. You can create any labels with the `resourceselector.clcm.openshift.io/` prefix to classify servers by hardware type, rack location, or other site-specific criteria. These labels are matched against the `resourceSelector` criteria in the `ClusterTemplate` CR during host selection.

    `bmac.agent-install.openshift.io/allow-provisioned-host-management`
    Optional. Allows the O-Cloud Manager to manage a host that is already in a provisioned state. The O-Cloud Manager sets this annotation automatically during node allocation if not already present.

    `spec.online: false`
    Prevents the server from being powered on before provisioning. The O-Cloud Manager manages power state during provisioning.

    `spec.bmc.address`
    Specifies the BMC connection URL in the format `<protocol>+https://<bmc_ip>/redfish/v1/Systems/<system_id>`. Use `redfish-virtualmedia` for generic Redfish or `idrac-virtualmedia` for Dell iDRAC.

    `spec.bmc.credentialsName`
    Specifies the name of the `Secret` resource containing the BMC credentials created in the previous step.

4.  Apply the CRs to the hub cluster by running the following commands:

    ``` terminal
    $ oc apply -f <infrastructure_hierarchy_filename>.yaml
    $ oc apply -f <bmc_secret_filename>.yaml
    $ oc apply -f <baremetalhost_filename>.yaml
    ```

    - Replace `<infrastructure_hierarchy_filename>.yaml`, `<bmc_secret_filename>.yaml`, and `<baremetalhost_filename>.yaml` with the names of the files.

      After the `BareMetalHost` CR is created, the Bare Metal Operator connects to the BMC, inspects the physical hardware, and populates a `HardwareData` CR with CPU, memory, NIC, and storage details. This data is used for hardware data filtering during resource selection.

<!-- -->

1.  Verify that the infrastructure hierarchy resources are created by running the following commands:

    ``` terminal
    $ oc get locations.ocloud.openshift.io
    $ oc get ocloudsites.ocloud.openshift.io
    $ oc get resourcepools.ocloud.openshift.io
    ```

2.  Verify that the `BareMetalHost` CR is registered and inspection is complete by running the following command:

    ``` terminal
    $ oc get bmh -A
    ```

    The server should show a provisioning state of `available` after inspection completes, indicating it is ready for allocation.

- [Configure advanced hardware management](../infrastructure_lifecycle_management/ocloud-configuring-advanced-hardware-management.xml#ocloud-configuring-advanced-hardware-management)

# Create a ClusterTemplate CR for single-node cluster provisioning

You can define a `ClusterTemplate` custom resource (CR) that serves as a reusable blueprint for provisioning clusters. The template specifies the cluster topology, hardware requirements, and default configuration. It also defines a validation schema for the site-specific parameters that site engineers provide in a `ProvisioningRequest` CR.

A `ClusterTemplate` CR references `ConfigMap` resources that contain defaults for cluster installation and Day 2 policy configuration. The `ConfigMap` CR for cluster installation defaults defines the common configuration across all clusters provisioned with a template, including cluster-level settings and the shared node configuration for each node group.

When a site engineer creates a `ProvisioningRequest` resource, the O-Cloud Manager merges the site-specific parameters from the request with these defaults to produce the final cluster and policy definitions.

<div class="note">

For multi-node clusters with distinct hardware requirements for each node role, see "Create a ClusterTemplate CR for multi-node cluster provisioning".

For advanced hardware selection using hardware data selectors and site-specific overrides, see "Configure advanced hardware management".

</div>

- The O-Cloud Manager Operator is installed on the hub cluster.

- The GitOps repository is configured and synchronized with ArgoCD.

- Bare-metal servers are onboarded to resource pools with appropriate resource selector labels.

- If firmware or BIOS management is required, `HardwareProfile` resources are defined.

1.  Create a namespace for the `ClusterTemplate` and its associated resources by running the following command:

    ``` terminal
    $ oc create namespace <template_namespace>
    ```

    where:

    `<template_namespace>`
    Specifies the target namespace for the `ClusterTemplate` resource and associated `ConfigMap` resources.

2.  Create a `ConfigMap` CR containing default values for cluster installation parameters, such as the following example for a single-node OpenShift cluster:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: clusterinstance-defaults-v1
      namespace: <template_namespace>
    data:
      clusterinstance-defaults: |
        baseDomain: example.com
        extraLabels:
          ManagedCluster:
            cluster-version: "v4-Y-Z"
            sno-ran-du-policy: "v1"
        clusterImageSetNameRef: "4.Y.Z"
        pullSecretRef:
          name: pull-secret
        networkType: OVNKubernetes
        clusterNetwork:
          - cidr: 203.0.113.0/24
            hostPrefix: 23
        machineNetwork:
          - cidr: 192.0.2.0/24
        serviceNetwork:
          - cidr: 233.252.0.0/24
        # sshPublicKey: "ssh-rsa AAAA..."
        additionalNTPSources:
          - 1.pool.ntp.org
        templateRefs:
          - name: ai-cluster-templates-v1
            namespace: open-cluster-management
        # Restricts the cluster to a minimal capability set for resource-constrained deployments
        # installConfigOverrides: '{"capabilities": {"baselineCapabilitySet": "None", "additionalEnabledCapabilities": ["NodeTuning", "OperatorLifecycleManager", "Ingress"]}}'
        # Ignition configuration override applied during cluster installation
        # ignitionConfigOverride: '{"ignition": {"version": "3.2.0"}, "storage": {"files": [...]}}'
        cpuPartitioningMode: AllNodes
        extraManifestsRefs:
          - name: sno-ran-du-extra-manifest-v1
        nodeGroups:
          - name: master
            role: master
            bootMode: UEFI
            ironicInspect: "disabled"
            automatedCleaningMode: disabled
            rootDeviceHints:
              deviceName: /dev/disk/by-path/pci-0000:01:00.0-nvme-1
            nodeNetwork:
              interfaces:
                - name: ens3f0
                  label: boot-interface
                - name: ens3f1
                  label: data-interface
              config:
                routes:
                  config:
                    - destination: 0.0.0.0/0
                      next-hop-interface: ens3f0
                      table-id: 254
                interfaces:
                  - ipv6:
                      enabled: false
                    ipv4:
                      enabled: true
                    name: ens3f0
                    state: up
                    type: ethernet
            templateRefs:
              - name: ai-node-templates-v1
                namespace: open-cluster-management
    ```

    `extraLabels.ManagedCluster`
    The `cluster-version` label is mandatory. This label, along with any additional custom labels such as `sno-ran-du-policy`, is used to bind Red Hat Advanced Cluster Management (RHACM) policies for cluster configuration rendered from the PolicyGenerator manifest.

    `nodeGroups[].name`
    Must match `hwMgmtDefaults.nodeGroupData[].name` defined in the `ClusterTemplate` CR, which also correspond to the `MachineConfigPool` name on the managed cluster.

    - The `boot-interface` label on a network interface is required. Using this label, the O-Cloud Manager resolves the boot NIC’s MAC address from hardware inventory data.

      <div class="note">

      For image-based installation (IBI) provisioning, replace the `templateRefs` values with `ibi-cluster-templates-v1` and `ibi-node-templates-v1`. These templates instruct the installation program to use the seed image on the preinstalled host instead of performing a full installation. The Image Based Install (IBI) Operator must be enabled in the `MultiClusterEngine` resource, and servers must be preinstalled with the seed image using the live installation ISO before provisioning.

      </div>

3.  Create a `ConfigMap` CR containing default values for Day 2 configuration policy parameters, such as the following example:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: policytemplates-defaults-v1
      namespace: <template_namespace>
    data:
      policytemplate-defaults: |
        sriov-network-vlan-1: "140"
        sriov-network-pfNames-1: '["ens2f0"]'
        cpu-isolated: "0-1,64-65"
        cpu-reserved: "2-10"
        hugepages-default: "1G"
        hugepages-size: "1G"
        hugepages-count: "32"
        install-plan-approval: "Automatic"
    ```

    The `ConfigMap` resource must contain a `policytemplate-defaults` key. The value is a YAML string defining the default policy parameters. Site-specific values from the `ProvisioningRequest` resource take precedence over these defaults when both specify the same parameter. All parameters referenced as placeholders in the PolicyGenerator manifest must be declared here or supplied through the `ProvisioningRequest` CR.

4.  Create an RHACM `PolicyGenerator` manifest, such as the following example, that defines the Day 2 configuration policies for clusters provisioned with this `ClusterTemplate` CR:

    <div class="note">

    The `PolicyGenerator` CR is the mechanism that turns policy defaults into enforceable policies on managed clusters. When a `ProvisioningRequest` CR is created, the O-Cloud Manager creates a `ConfigMap` CR named `<cluster-name>-pg` on the hub cluster, populated by merging the values from the policy defaults `ConfigMap` with any overrides from the `ProvisioningRequest` CR.

    The `PolicyGenerator` CR uses templating expressions (`{{hub …​ hub}}`) as placeholders that RHACM resolves at runtime by reading values from this `<cluster-name>-pg` `ConfigMap` CR. The result is `Policy` CRs that RHACM enforces on the managed cluster.

    </div>

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PolicyGenerator
    metadata:
      name: sno-ran-du-pg-v4-Y-Z-v1
    policyDefaults:
      namespace: ztp-<template_namespace>
      placement:
        labelSelector:
          cluster-version: "v4-Y-Z"
          sno-ran-du-policy: "v1"
      policyAnnotations:
        clustertemplates.clcm.openshift.io/templates: "sno-ran-du.v4-Y-Z-1"
      remediationAction: enforce
      orderPolicies: true
    policies:
    - name: v1-subscriptions-policy
      manifests:
        - path: source-crs/cluster-logging/ClusterLogSubscription.yaml
          patches:
          - spec:
              source: redhat-operators
              installPlanApproval:
                '{{hub $configMap:=(lookup "v1" "ConfigMap" "" (printf "%s-pg" .ManagedClusterName)) hub}}{{hub dig "data" "install-plan-approval" "Manual" $configMap hub}}'
    - name: v1-perf-configuration-policy
      manifests:
        - path: source-crs/node-tuning-operator/PerformanceProfile-SetSelector.yaml
          patches:
          - spec:
              cpu:
                isolated: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "cpu-isolated" hub}}'
                reserved: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "cpu-reserved" hub}}'
              hugepages:
                defaultHugepagesSize: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "hugepages-default" hub}}'
    ```

    `policyDefaults.namespace`
    Must follow the naming convention `ztp-<clustertemplate-namespace>`. The O-Cloud Manager uses this convention to locate policies associated with a `ClusterTemplate` namespace.

    `policyDefaults.placement.labelSelector`
    Must match the `extraLabels.ManagedCluster` labels defined in the `clusterinstance-defaults` `ConfigMap` CR. These labels bind the policies to the correct managed clusters.

    `policyAnnotations.clustertemplates.clcm.openshift.io/templates`
    A comma-separated list of `ClusterTemplate` CRs, populated using the `metadata.name` field, that this `PolicyGenerator` CR is associated with. This enables the O-Cloud Manager to track policy compliance for provisioning status reporting.

    `policyDefaults.orderPolicies`
    Set to `true` to apply the policies in the order you define under the `policies` field. The O-Cloud Manager does not use the Topology Aware Lifecycle Manager to order policy application, so you must set the order in the `PolicyGenerator` CR.

    `source-crs/`
    Contains the base manifests for Day 2 configuration resources such as `PerformanceProfile` CRs, `SriovNetworkNodePolicy` CRs, and Operator subscriptions. These CRs must match the target OpenShift Container Platform release version.

    <div class="note">

    All parameters referenced as placeholders, such as `cpu-isolated` and `install-plan-approval`, must be declared in the `templateParameterSchema.policyTemplateParameters` section of the `ClusterTemplate` CR and supplied either through the policy defaults `ConfigMap` CR or the `ProvisioningRequest` CR.

    </div>

5.  Create the `ClusterTemplate` CR, such as the following example:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: ClusterTemplate
    metadata:
      name: sno-ran-du.v4-Y-Z-1
      namespace: <template_namespace>
    spec:
      name: sno-ran-du
      version: v4-Y-Z-1
      release: 4.Y.Z
      templateDefaults:
        hwMgmtDefaults:
          hardwareProvisioningTimeout: "90m"
          nodeGroupData:
            - name: master
              role: master
              resourceSelector:
                server-type: <server_type>
        clusterInstanceDefaults: clusterinstance-defaults-v1
        policyTemplateDefaults: policytemplates-defaults-v1
      templateParameterSchema:
        properties:
          nodeClusterName:
            type: string
          oCloudSiteId:
            type: string
          hwMgmtParameters:
            properties:
              hardwareProvisioningTimeout:
                type: string
              nodeGroupData:
                type: array
                items:
                  type: object
                  required:
                    - name
                  properties:
                    name:
                      type: string
                      minLength: 1
                    role:
                      type: string
                      enum:
                        - master
                        - worker
                    hwProfile:
                      type: string
                    resourcePoolId:
                      type: string
                    resourceSelector:
                      type: object
                      additionalProperties:
                        type: string
            type: object
          policyTemplateParameters:
            properties:
              sriov-network-vlan-1:
                type: string
              sriov-network-vlan-2:
                type: string
              sriov-network-pfNames-1:
                type: string
              sriov-network-pfNames-2:
                type: string
              cpu-isolated:
                type: string
              cpu-reserved:
                type: string
              hugepages-default:
                type: string
              hugepages-size:
                type: string
              hugepages-count:
                type: string
              install-plan-approval:
                type: string
            type: object
          clusterInstanceParameters:
            properties:
              additionalNTPSources:
                items:
                  type: string
                type: array
              apiVIPs:
                items:
                  type: string
                maxItems: 2
                type: array
              baseDomain:
                type: string
              clusterName:
                type: string
              extraAnnotations:
                additionalProperties:
                  additionalProperties:
                    type: string
                  type: object
                type: object
              extraLabels:
                additionalProperties:
                  additionalProperties:
                    type: string
                  type: object
                type: object
              ingressVIPs:
                items:
                  type: string
                maxItems: 2
                type: array
              machineNetwork:
                items:
                  properties:
                    cidr:
                      type: string
                  required:
                    - cidr
                  type: object
                type: array
              nodeGroups:
                items:
                  properties:
                    name:
                      type: string
                      minLength: 1
                    extraAnnotations:
                      additionalProperties:
                        additionalProperties:
                          type: string
                        type: object
                      type: object
                    extraLabels:
                      additionalProperties:
                        additionalProperties:
                          type: string
                        type: object
                      type: object
                    nodeLabels:
                      additionalProperties:
                        type: string
                      type: object
                    nodeNetwork:
                      properties:
                        config:
                          type: object
                          x-kubernetes-preserve-unknown-fields: true
                      type: object
                    nodes:
                      items:
                        properties:
                          hostName:
                            type: string
                          extraAnnotations:
                            additionalProperties:
                              additionalProperties:
                                type: string
                              type: object
                            type: object
                          extraLabels:
                            additionalProperties:
                              additionalProperties:
                                type: string
                              type: object
                            type: object
                          nodeLabels:
                            additionalProperties:
                              type: string
                            type: object
                          nodeNetwork:
                            properties:
                              interfaces:
                                minItems: 1
                                items:
                                  properties:
                                    name:
                                      type: string
                                      minLength: 1
                                    addresses:
                                      properties:
                                        ipv4:
                                          items:
                                            type: string
                                            minLength: 1
                                          minItems: 1
                                          type: array
                                        ipv6:
                                          items:
                                            type: string
                                            minLength: 1
                                          minItems: 1
                                          type: array
                                      minProperties: 1
                                      type: object
                                  required:
                                    - name
                                    - addresses
                                  type: object
                                type: array
                            required:
                              - interfaces
                            type: object
                        required:
                          - hostName
                          - nodeNetwork
                        type: object
                      type: array
                  required:
                    - name
                    - nodes
                  type: object
                type: array
              serviceNetwork:
                items:
                  properties:
                    cidr:
                      type: string
                  required:
                    - cidr
                  type: object
                type: array
              sshPublicKey:
                type: string
            required:
              - clusterName
              - nodeGroups
            type: object
        required:
          - nodeClusterName
          - oCloudSiteId
          - policyTemplateParameters
          - clusterInstanceParameters
        type: object
    ```

    where:

    `metadata.name`
    Must follow the format `<name>.<version>` and must be unique across all namespaces.

    `<template_namespace>`
    Specifies the namespace where the `ClusterTemplate` CR and its associated `ConfigMap` CRs are stored.

    `spec.name`
    Specifies the base name of the template. Combined with `spec.version` to form the `metadata.name` value.

    `spec.version`
    Specifies the version of the template.

    `spec.release`
    Specifies the OpenShift Container Platform release version to install. Must match the `clusterImageSetNameRef` value in the `clusterinstance-defaults` `ConfigMap` resource.

    `spec.templateDefaults.hwMgmtDefaults`
    Defines hardware management settings for provisioning, including node groups and a hardware provisioning timeout. This example shows a minimal configuration with a single node group and a simple label selector. For advanced hardware selection using hardware data selectors and site-specific overrides, see "Configure advanced hardware management".

    `spec.templateDefaults.hwMgmtDefaults.nodeGroupData[].name`
    Must match the target `MachineConfigPool` name on the managed cluster, for example, `master` or `worker`. This name must also match `nodeGroups[].name` in the `clusterinstance-defaults` `ConfigMap` resource.

    `<server_type>`
    Specifies the resource selector label value used to match bare-metal hosts during provisioning. This must match a `resourceselector.clcm.openshift.io/` label on onboarded `BareMetalHost` CRs.

    `spec.templateDefaults.clusterInstanceDefaults`
    References the name of the `ConfigMap` resource that contains default cluster installation parameters. These defaults are merged with the site-specific values from the `ProvisioningRequest` CR to produce the final `ClusterInstance` resource.

    `spec.templateDefaults.policyTemplateDefaults`
    References the name of the `ConfigMap` resource that contains default Day 2 configuration policy parameters. Site-specific values from the `ProvisioningRequest` CR take precedence over these defaults.

    `spec.templateParameterSchema`
    Defines the OpenAPI v3 schema that validates parameters supplied in a `ProvisioningRequest` CR. The schema must include `nodeClusterName`, `oCloudSiteId`, `policyTemplateParameters`, and `clusterInstanceParameters`. The `hwMgmtParameters` section is optional and enables site-specific hardware overrides.

6.  Apply the resources to the hub cluster, or commit them to the GitOps repository for ArgoCD synchronization.

<!-- -->

1.  Verify that the `ClusterTemplate` CR is validated by running the following command:

    ``` terminal
    $ oc get clustertemplates.clcm.openshift.io -A
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAMESPACE          NAME                   AGE   STATE       DETAILS
    ocloud-templates   sno-ran-du.v4-Y-Z-1   18s   Completed   The cluster template validation succeeded
    ```

    A `STATE` of `Completed` with a `ClusterTemplateValidated` condition of `True` indicates that the template passed validation and is ready for use. After successful validation, the `ClusterTemplate` CR and its referenced `ConfigMap` CRs become immutable.

- [About the `BareMetalHost` resource](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#bmo-about-the-baremetalhost-resource_bare-metal-postinstallation-configuration)

# Create a ClusterTemplate CR for multi-node cluster provisioning

You can define a `ClusterTemplate` CR with multiple node groups in the `hwMgmtDefaults.nodeGroupData[]` field when your cluster topology includes multiple groups of nodes, such as control plane and worker nodes. Each node group can define its own role, hardware profile, and resource selectors, to enable the O-Cloud Manager to allocate hardware independently for each group.

A `ClusterTemplate` CR references `ConfigMap` resources that contain defaults for cluster installation and Day 2 policy configuration. The `ConfigMap` CR for cluster installation defaults defines the common configuration across all clusters provisioned with a template, including cluster-level settings and the shared node configuration for each node group.

When a site engineer creates a `ProvisioningRequest` resource, the O-Cloud Manager merges the site-specific parameters from the request with these defaults to produce the final cluster and policy definitions.

- The O-Cloud Manager Operator is installed on the hub cluster.

- The GitOps repository is configured and synchronized with ArgoCD.

- Bare-metal servers are onboarded to resource pools with appropriate resource selector labels.

- If firmware or BIOS management is required, `HardwareProfile` resources are defined.

1.  Create a `ConfigMap` CR that defines the cluster installation defaults for a multi-node topology. The `ConfigMap` CR must include a `nodeGroup` entry for each node role. The following example defines `master` and `worker` groups with distinct network interface configurations:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: clusterinstance-defaults-v1
      namespace: <template_namespace>
    data:
      clusterinstance-defaults: |
        baseDomain: example.com
        extraLabels:
          ManagedCluster:
            cluster-version: "v4-Y-Z"
            std-ran-du-policy: "v1"
        clusterType: HighlyAvailable
        clusterImageSetNameRef: "4.Y.Z"
        pullSecretRef:
          name: pull-secret
        networkType: OVNKubernetes
        clusterNetwork:
          - cidr: 203.0.113.0/24
            hostPrefix: 25
        serviceNetwork:
          - cidr: 198.51.100.0/24
        additionalNTPSources:
          - 1.pool.ntp.org
        templateRefs:
          - name: ai-cluster-templates-v1
            namespace: open-cluster-management
        cpuPartitioningMode: AllNodes
        extraManifestsRefs:
          - name: std-ran-du-extra-manifest-v1
        nodeGroups:
          - name: master
            role: master
            bootMode: UEFI
            ironicInspect: "disabled"
            automatedCleaningMode: disabled
            rootDeviceHints:
              deviceName: /dev/disk/by-path/pci-0000:01:00.0-nvme-1
            nodeNetwork:
              interfaces:
                - name: ens1f0
                  label: boot-interface
                - name: ens1f1
                  label: data-interface
              config:
                routes:
                  config:
                    - destination: 0.0.0.0/0
                      next-hop-interface: ens1f0
                      table-id: 254
                interfaces:
                  - ipv6:
                      enabled: false
                    ipv4:
                      enabled: true
                    name: ens1f0
                    state: up
                    type: ethernet
            templateRefs:
              - name: ai-node-templates-v1
                namespace: open-cluster-management
          - name: worker
            role: worker
            bootMode: UEFI
            ironicInspect: "disabled"
            automatedCleaningMode: disabled
            rootDeviceHints:
              deviceName: /dev/disk/by-path/pci-0000:01:00.0-nvme-1
            nodeNetwork:
              interfaces:
                - name: ens3f0
                  label: boot-interface
                - name: ens3f1
                  label: data-interface
                - name: ens2f0
                  label: sriov-1
                - name: ens2f1
                  label: sriov-2
              config:
                routes:
                  config:
                    - destination: 0.0.0.0/0
                      next-hop-interface: ens3f0
                      table-id: 254
                interfaces:
                  - ipv6:
                      enabled: false
                    ipv4:
                      enabled: true
                    name: ens3f0
                    state: up
                    type: ethernet
            templateRefs:
              - name: ai-node-templates-v1
                namespace: open-cluster-management
    ```

    `extraLabels.ManagedCluster`
    The `cluster-version` label is mandatory. This label, along with any additional custom labels such as `std-ran-du-policy`, is used to bind Red Hat Advanced Cluster Management (RHACM) policies for cluster configuration rendered from the PolicyGenerator manifest.

    `nodeGroups[].name`
    Must match `hwMgmtDefaults.nodeGroupData[].name` in the `ClusterTemplate` CR and the `MachineConfigPool` name on the managed cluster. Define one entry for each hardware node group.

    - Worker nodes in this example include additional SR-IOV interfaces (`sriov-1`, `sriov-2`) for data-plane traffic, demonstrating how different node roles can have distinct network configurations.

2.  Create a `ConfigMap` CR containing default values for Day 2 configuration policy parameters, such as the following example:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: policytemplates-defaults-v1
      namespace: <template_namespace>
    data:
      policytemplate-defaults: |
        sriov-network-vlan-1: "140"
        sriov-network-pfNames-1: '["ens2f0"]'
        sriov-network-vlan-2: "150"
        sriov-network-pfNames-2: '["ens2f1"]'
        cpu-isolated: "0-1,64-65"
        cpu-reserved: "2-10"
        hugepages-default: "1G"
        hugepages-size: "1G"
        hugepages-count: "32"
        install-plan-approval: "Automatic"
    ```

    The `ConfigMap` CR must contain a `policytemplate-defaults` key. The value is a YAML string defining the default policy parameters. Site-specific values from the `ProvisioningRequest` CR take precedence over these defaults when both specify the same parameter. All parameters referenced as placeholders in the `PolicyGenerator` manifest must be declared here or supplied through the `ProvisioningRequest` CR.

3.  Create an RHACM `PolicyGenerator` manifest, such as the following example, that defines the Day 2 configuration policies for clusters provisioned with this `ClusterTemplate` CR:

    <div class="note">

    The `PolicyGenerator` CR is the mechanism that turns policy defaults into enforceable policies on managed clusters. When a `ProvisioningRequest` CR is created, the O-Cloud Manager creates a `ConfigMap` CR named `<cluster-name>-pg` on the hub cluster, populated by merging the values from the policy defaults `ConfigMap` with any overrides from the `ProvisioningRequest` CR.

    The `PolicyGenerator` CR uses templating expressions (`{{hub …​ hub}}`) as placeholders that RHACM resolves at runtime by reading values from this `<cluster-name>-pg` `ConfigMap` CR. The result is `Policy` CRs that RHACM enforces on the managed cluster.

    </div>

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PolicyGenerator
    metadata:
      name: std-ran-du-pg-v4-Y-Z-v1
    policyDefaults:
      namespace: ztp-<template_namespace>
      placement:
        labelSelector:
          cluster-version: "v4-Y-Z"
          std-ran-du-policy: "v1"
      policyAnnotations:
        clustertemplates.clcm.openshift.io/templates: "std-ran-du.v4-Y-Z-1"
      remediationAction: enforce
      orderPolicies: true
    policies:
    - name: v1-subscriptions-policy
      manifests:
        - path: source-crs/cluster-logging/ClusterLogSubscription.yaml
          patches:
          - spec:
              source: redhat-operators
              installPlanApproval:
                '{{hub $configMap:=(lookup "v1" "ConfigMap" "" (printf "%s-pg" .ManagedClusterName)) hub}}{{hub dig "data" "install-plan-approval" "Manual" $configMap hub}}'
    - name: v1-config-policy
      manifests:
        - path: source-crs/node-tuning-operator/x86_64/PerformanceProfile-SetSelector.yaml
          patches:
          - spec:
              cpu:
                isolated: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "cpu-isolated" hub}}'
                reserved: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "cpu-reserved" hub}}'
              hugepages:
                defaultHugepagesSize: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "hugepages-default" hub}}'
                pages:
                  - size: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "hugepages-size" hub}}'
                    count: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "hugepages-count" | toInt hub}}'
              machineConfigPoolSelector:
                pools.operator.machineconfiguration.openshift.io/worker: ""
              nodeSelector:
                node-role.kubernetes.io/worker: ''
        - path: source-crs/sriov-operator/SriovNetwork.yaml
          patches:
          - metadata:
              name: sriov-nw-du-fh
            spec:
              resourceName: du_fh
              vlan: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "sriov-network-vlan-1" | toInt hub}}'
        - path: source-crs/sriov-operator/SriovNetworkNodePolicy-SetSelector.yaml
          patches:
          - metadata:
              name: sriov-nnp-du-fh
            spec:
              deviceType: netdevice
              nicSelector:
                pfNames: '{{hub fromConfigMap "" (printf "%s-pg" .ManagedClusterName) "sriov-network-pfNames-1" | toLiteral hub}}'
              nodeSelector:
                node-role.kubernetes.io/worker: ""
              resourceName: du_fh
    ```

    `policyDefaults.namespace`
    Must follow the naming convention `ztp-<clustertemplate-namespace>`. The O-Cloud Manager uses this convention to locate policies associated with a `ClusterTemplate` namespace.

    `policyDefaults.placement.labelSelector`
    Must match the `extraLabels.ManagedCluster` labels defined in the `clusterinstance-defaults` `ConfigMap` CR. These labels bind the policies to the correct managed clusters.

    `policyAnnotations.clustertemplates.clcm.openshift.io/templates`
    A comma-separated list of `ClusterTemplate` CRs, populated using the `metadata.name` field, that this `PolicyGenerator` CR is associated with. This enables the O-Cloud Manager to track policy compliance for provisioning status reporting.

    `policyDefaults.orderPolicies`
    Set to `true` to apply the policies in the order you define under the `policies` field. The O-Cloud Manager does not use the Topology Aware Lifecycle Manager to order policy application, so you must set the order in the `PolicyGenerator` CR.

    `source-crs/`
    Contains the base manifests for Day 2 configuration resources such as `PerformanceProfile` CRs, `SriovNetworkNodePolicy` CRs, and Operator subscriptions. These CRs must match the target OpenShift Container Platform release version.

    <div class="note">

    All parameters referenced as placeholders, such as `cpu-isolated` and `sriov-network-vlan-1`, must be declared in the `templateParameterSchema.policyTemplateParameters` section of the `ClusterTemplate` CR and supplied either through the policy defaults `ConfigMap` CR or the `ProvisioningRequest` CR.

    </div>

4.  Create a `ClusterTemplate` CR for the multi-node cluster topology, such as the following example that defines distinct hardware for each node group:

    ``` yaml
    apiVersion: clcm.openshift.io/v1alpha1
    kind: ClusterTemplate
    metadata:
      name: std-ran-du.v4-Y-Z-1
      namespace: <template_namespace>
    spec:
      name: std-ran-du
      version: v4-Y-Z-1
      release: 4.Y.Z
      templateDefaults:
        hwMgmtDefaults:
          hardwareProvisioningTimeout: "120m"
          nodeGroupData:
            - name: master
              role: master
              hwProfile: rh-profile-bios-standard
              resourceSelector:
                server-type: dell-xr8620t
                hardwaredata/num_threads;gte: "64"
                hardwaredata/ramMebibytes;gte: "131072"
                hardwaredata/nics;speedGbps>=25;count>=4: "present"
            - name: worker
              role: worker
              hwProfile: rh-profile-bios-dpdk
              resourceSelector:
                server-type: dell-xr7620
                hardwaredata/num_threads;gte: "128"
                hardwaredata/ramMebibytes;gte: "262144"
                hardwaredata/nics;speedGbps>=100;count>=2: "present"
                hardwaredata/storage;type==NVME;count>=4: "present"
        clusterInstanceDefaults: clusterinstance-defaults-v1
        policyTemplateDefaults: policytemplates-defaults-v1
      templateParameterSchema:
        properties:
          nodeClusterName:
            type: string
          oCloudSiteId:
            type: string
          hwMgmtParameters:
            properties:
              hardwareProvisioningTimeout:
                type: string
              nodeGroupData:
                type: array
                items:
                  type: object
                  required:
                    - name
                  properties:
                    name:
                      type: string
                      minLength: 1
                    role:
                      type: string
                      enum:
                        - master
                        - worker
                    hwProfile:
                      type: string
                    resourcePoolId:
                      type: string
                    resourceSelector:
                      type: object
                      additionalProperties:
                        type: string
            type: object
          policyTemplateParameters:
            properties:
              sriov-network-vlan-1:
                type: string
              sriov-network-vlan-2:
                type: string
              sriov-network-pfNames-1:
                type: string
              sriov-network-pfNames-2:
                type: string
              cpu-isolated:
                type: string
              cpu-reserved:
                type: string
              hugepages-default:
                type: string
              hugepages-size:
                type: string
              hugepages-count:
                type: string
              install-plan-approval:
                type: string
            type: object
          clusterInstanceParameters:
            properties:
              additionalNTPSources:
                items:
                  type: string
                type: array
              apiVIPs:
                items:
                  type: string
                maxItems: 2
                type: array
              baseDomain:
                type: string
              clusterName:
                type: string
              extraAnnotations:
                additionalProperties:
                  additionalProperties:
                    type: string
                  type: object
                type: object
              extraLabels:
                additionalProperties:
                  additionalProperties:
                    type: string
                  type: object
                type: object
              ingressVIPs:
                items:
                  type: string
                maxItems: 2
                type: array
              machineNetwork:
                items:
                  properties:
                    cidr:
                      type: string
                  required:
                    - cidr
                  type: object
                type: array
              nodeGroups:
                items:
                  properties:
                    name:
                      type: string
                      minLength: 1
                    extraAnnotations:
                      additionalProperties:
                        additionalProperties:
                          type: string
                        type: object
                      type: object
                    extraLabels:
                      additionalProperties:
                        additionalProperties:
                          type: string
                        type: object
                      type: object
                    nodeLabels:
                      additionalProperties:
                        type: string
                      type: object
                    nodeNetwork:
                      properties:
                        config:
                          type: object
                          x-kubernetes-preserve-unknown-fields: true
                      type: object
                    nodes:
                      items:
                        properties:
                          hostName:
                            type: string
                          extraAnnotations:
                            additionalProperties:
                              additionalProperties:
                                type: string
                              type: object
                            type: object
                          extraLabels:
                            additionalProperties:
                              additionalProperties:
                                type: string
                              type: object
                            type: object
                          nodeLabels:
                            additionalProperties:
                              type: string
                            type: object
                          nodeNetwork:
                            properties:
                              interfaces:
                                minItems: 1
                                items:
                                  properties:
                                    name:
                                      type: string
                                      minLength: 1
                                    addresses:
                                      properties:
                                        ipv4:
                                          items:
                                            type: string
                                            minLength: 1
                                          minItems: 1
                                          type: array
                                        ipv6:
                                          items:
                                            type: string
                                            minLength: 1
                                          minItems: 1
                                          type: array
                                      minProperties: 1
                                      type: object
                                  required:
                                    - name
                                    - addresses
                                  type: object
                                type: array
                            required:
                              - interfaces
                            type: object
                        required:
                          - hostName
                          - nodeNetwork
                        type: object
                      type: array
                  required:
                    - name
                    - nodes
                  type: object
                type: array
              serviceNetwork:
                items:
                  properties:
                    cidr:
                      type: string
                  required:
                    - cidr
                  type: object
                type: array
              sshPublicKey:
                type: string
            required:
              - clusterName
              - nodeGroups
            type: object
        required:
          - nodeClusterName
          - oCloudSiteId
          - policyTemplateParameters
          - clusterInstanceParameters
        type: object
    ```

    where:

    `nodeGroupData[].name`
    Must match the `MachineConfigPool` name on the managed cluster and the corresponding `nodeGroups[].name` in the `clusterinstance-defaults` ConfigMap.

    `nodeGroupData[].role`
    Maps the node group to a cluster node role. Valid values are `master` for control plane nodes and `worker` for compute nodes.

    `nodeGroupData[].hwProfile`
    Specifies the `HardwareProfile` CR to apply to this node group. Each group can reference a different profile, for example a standard BIOS profile for controllers and a DPDK-optimized profile for workers. The referenced `HardwareProfile` CRs must exist in the O-Cloud Manager Operator namespace, `oran-o2ims`.

    `nodeGroupData[].resourceSelector`
    Defines independent selection criteria for each node group. Each group’s selector is evaluated separately against the pool of available `BareMetalHost` CRs. The controller and worker groups can target completely different server types and hardware specifications.

    `templateParameterSchema.hwMgmtParameters`
    Enables site-specific overrides of hardware profiles and resource selectors. Including this in the schema allows site engineers to adjust hardware selection for individual node groups in their `ProvisioningRequest` CR without modifying the template.

    <div class="note">

    The `templateParameterSchema` is identical for both single-node and multi-node topologies. The schema defines which fields are permitted; the number of `nodeGroups` entries is determined by the deployment.

    </div>

5.  Apply the `ClusterTemplate` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

<!-- -->

1.  Verify that the multi-node template passes validation by running the following command:

    ``` terminal
    $ oc get clustertemplates.clcm.openshift.io -n <template_namespace> std-ran-du.v4-Y-Z-1
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAMESPACE          NAME                         AGE   STATE       DETAILS
    ocloud-templates   std-ran-du.v4-Y-Z-1   12s   Completed   The cluster template validation succeeded
    ```

    A `STATE` of `Completed` confirms that all node group configurations, resource selectors, and the parameter schema are valid. When a `ProvisioningRequest` CR references this template, the O-Cloud Manager allocates hosts independently for each node group, matching each group’s `resourceSelector` against available `BareMetalHost` CRs.

- [About the `BareMetalHost` resource](../installing/installing_bare_metal/bare-metal-postinstallation-configuration.xml#bmo-about-the-baremetalhost-resource_bare-metal-postinstallation-configuration)
