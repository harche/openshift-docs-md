You can upgrade clusters provisioned by the O-Cloud Manager by creating a new `ClusterTemplate` custom resource (CR) version for the target release and updating the `ProvisioningRequest` CR to reference it. The O-Cloud Manager supports image-based upgrades for single-node OpenShift Container Platform clusters and standard platform upgrades for multi-node clusters.

You can perform these upgrades by editing the `ProvisioningRequest` CR directly or through the Provisioning REST API. For more information about updating using the Provisioning API, see "Upgrade clusters with the Provisioning API".

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Prepare cluster templates for a new release

Before you can upgrade a cluster, you must create a new `ClusterTemplate` custom resource (CR) version for the target OpenShift Container Platform release. Because `ClusterTemplate` CRs and their referenced `ConfigMap` CRs are immutable after validation, upgrading to a new release requires creating new versions of these resources with updated cluster installation defaults, policy templates, and upgrade configuration.

- The GitOps repository is configured and ArgoCD synchronizes resources to the hub cluster.

- The target OpenShift Container Platform version is available as a `ClusterImageSet` on the hub cluster.

- For multi-node OpenShift Container Platform clusters in disconnected environments, you have mirrored the target release payload to your local registry.

- For single-node OpenShift clusters in disconnected environments, you have mirrored the seed image to your local registry.

1.  Create new `clustertemplates` and `policytemplates` directories in the GitOps repository for the target release version, following the same directory structure as existing versions:

    ``` terminal
    clustertemplates/
    ├── version_4.Y.Z/
    │   └── sno-ran-du/
    └── version_4.Y.Z+1/        # new release directory
        └── sno-ran-du/

    policytemplates/
    ├── version_4.Y.Z/
    │   └── sno-ran-du/
    └── version_4.Y.Z+1/        # new release directory
        └── sno-ran-du/
    ```

2.  Create a `ClusterInstance` defaults ConfigMap resource for the new version with the updated `clusterImageSetNameRef`:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: clusterinstance-defaults-v1
      namespace: <template_namespace>
    data:
      clusterinstance-defaults: |
        clusterImageSetNameRef: "<target_version>"
        extraLabels:
          ManagedCluster:
            cluster-version: "<version_label>"
            <template_name>-policy: "v1"
    ```

    where:

    `<template_namespace>`
    Specifies the namespace for the new `ClusterTemplate` version, such as `sno-ran-du-v4-Y-Z+1`.

    `<target_version>`
    Specifies the target OpenShift Container Platform version, such as `4.22.0`.

    `<version_label>`
    Specifies a label value identifying the cluster version, such as `v4-22-0`.

    `<template_name>`
    Specifies the template name used for policy binding, such as `sno-ran-du`.

    <div class="note">

    The remaining configuration in the cluster instance defaults `ConfigMap` CR must remain identical to the original `ConfigMap` CR used for provisioning. For example, the `extraManifestsRefs` field must reference the same `ConfigMap` CR as the original version.

    </div>

3.  Create policy templates for the new version with updated Operator index images and any new configuration manifests.

4.  Create the `ClusterTemplate` CR for the target release with upgrade configuration. The `upgradeDefaults` section differs depending on the cluster topology:

    1.  For single-node OpenShift Container Platform clusters, configure the `upgradeDefaults` section with `imageBasedGroupUpgrade` specifications, and include the `upgradeParameters` schema to enable cluster overrides:

        ``` yaml
        apiVersion: clcm.openshift.io/v1alpha1
        kind: ClusterTemplate
        metadata:
          name: <template_name>.v4-Y-Z+1-1
          namespace: <template_namespace>
        spec:
          name: <template_name>
          version: v4-Y-Z+1-1
          release: "<target_version>"
          templateDefaults:
            clusterInstanceDefaults: clusterinstance-defaults-v1
            policyTemplateDefaults: policytemplate-defaults-v1
            upgradeDefaults:
              imageBasedGroupUpgrade:
                ibuSpec:
                  seedImageRef:
                    image: "quay.io/seed-repo/seed-image:<target_version>"
                    version: "<target_version>"
                  oadpContent:
                    - name: <template_name>-ibu-platform-backup-<version_label>
                      namespace: openshift-adp
                  autoRollbackOnFailure:
                    initMonitorTimeoutSeconds: 1800
                plan:
                  - actions: ["Prep"]
                    rolloutStrategy:
                      maxConcurrency: 1
                      timeout: 15
                  - actions: ["AbortOnFailure"]
                    rolloutStrategy:
                      maxConcurrency: 1
                      timeout: 5
                  - actions: ["Upgrade"]
                    rolloutStrategy:
                      maxConcurrency: 1
                      timeout: 60
                  - actions: ["AbortOnFailure"]
                    rolloutStrategy:
                      maxConcurrency: 1
                      timeout: 5
                  - actions: ["FinalizeUpgrade"]
                    rolloutStrategy:
                      maxConcurrency: 1
                      timeout: 5
          templateParameterSchema:
            properties:
              # ... other parameters such as nodeClusterName and oCloudSiteId
              upgradeParameters:
                properties:
                  imageBasedGroupUpgrade:
                    type: object
                    properties:
                      ibuSpec:
                        properties:
                          autoRollbackOnFailure:
                            properties:
                              initMonitorTimeoutSeconds:
                                minimum: 0
                                type: integer
                            type: object
                          oadpContent:
                            items:
                              properties:
                                name:
                                  type: string
                                namespace:
                                  type: string
                              type: object
                            type: array
                          seedImageRef:
                            properties:
                              image:
                                minLength: 1
                                type: string
                              pullSecretRef:
                                properties:
                                  name:
                                    type: string
                                type: object
                              version:
                                type: string
                            type: object
                        type: object
                      plan:
                        items:
                          properties:
                            actions:
                              items:
                                type: string
                              maxItems: 4
                              type: array
                            rolloutStrategy:
                              properties:
                                maxConcurrency:
                                  type: integer
                                timeout:
                                  type: integer
                              type: object
                          type: object
                        maxItems: 6
                        type: array
                type: object
            required:
              - nodeClusterName
              - oCloudSiteId
              - policyTemplateParameters
              - clusterInstanceParameters
            type: object
        ```

        where:

        `<template_name>`
        Specifies the base template name, such as `sno-ran-du`.

        `<template_namespace>`
        Specifies the namespace for the new `ClusterTemplate` version.

        `<target_version>`
        Specifies the target OpenShift Container Platform version.

        `<version_label>`
        Specifies the version label used in the OADP backup `ConfigMap` CR, such as `v4-Y-Z+1-1`.

        `spec.templateDefaults.upgradeDefaults`
        Defines the default upgrade configuration for image-based upgrades on single-node OpenShift clusters.

        `ibuSpec.seedImageRef`
        Specifies the seed container image and target platform version for the upgrade.

        <div class="important">

        For disconnected environments, the spoke cluster cannot reach public registries. You must set `ibuSpec.seedImageRef.image` to the mirrored seed image in your local registry, for example:

        ``` yaml
            upgradeDefaults:
              imageBasedGroupUpgrade:
                ibuSpec:
                  seedImageRef:
                    image: "registry.example.com:5000/seed-repo/seed-image:<target_version>"
                    version: "<target_version>"
        ```

        </div>

        `ibuSpec.oadpContent`
        References `ConfigMap` resources that contain OADP `Backup` and `Restore` CRs for application data protection during the upgrade.

        `ibuSpec.autoRollbackOnFailure.initMonitorTimeoutSeconds`
        Defines the time in seconds to wait before automatically rolling back a failed upgrade. The default is `1800`, which is 30 minutes.

        `plan`
        Defines the ordered execution stages for the image-based upgrade. Each stage specifies the actions to perform, the maximum number of clusters to upgrade concurrently, and the timeout in minutes for that stage.

        `spec.templateParameterSchema`
        Defines the full schema for parameters that can be overridden for a specific cluster in the `ProvisioningRequest` CR. Use the `upgradeParameters` section to permit individual deployments to customize upgrades, such as the seed image, rollback timeout, or rollout concurrency.

    2.  For multi-node clusters, configure the `upgradeDefaults.clusterVersion` section with the target upgrade channel and version, and include the `upgradeParameters` schema to enable cluster overrides:

        ``` yaml
        apiVersion: clcm.openshift.io/v1alpha1
        kind: ClusterTemplate
        metadata:
          name: <template_name>.v4-Y-Z+1-1
          namespace: <template_namespace>
        spec:
          name: <template_name>
          version: v4-Y-Z+1-1
          release: "<target_version>"
          templateDefaults:
            clusterInstanceDefaults: clusterinstance-defaults-v1
            policyTemplateDefaults: policytemplate-defaults-v1
            upgradeDefaults:
              clusterVersion:
                clusterUpgradeTimeout: 4h
                cvSpec:
                  channel: "stable-<target_version>"
                  desiredUpdate:
                    version: "<target_version>"
          templateParameterSchema:
            properties:
              # ... other parameters (nodeClusterName, oCloudSiteId, etc.) ...
              upgradeParameters:
                properties:
                  clusterVersion:
                    type: object
                    properties:
                      clusterUpgradeTimeout:
                        type: string
                      intermediateVersion:
                        type: string
                      cvSpec:
                        type: object
                        properties:
                          channel:
                            type: string
                          upstream:
                            type: string
                          desiredUpdate:
                            type: object
                            properties:
                              version:
                                type: string
                              image:
                                type: string
                              force:
                                type: boolean
                              architecture:
                                type: string
                                enum:
                                  - "Multi"
                                  - ""
                type: object
            required:
              - nodeClusterName
              - oCloudSiteId
              - policyTemplateParameters
              - clusterInstanceParameters
            type: object
        ```

        where:

        `<template_name>`
        Specifies the base template name, such as `std-ran-du`.

        `<template_namespace>`
        Specifies the namespace for the new `ClusterTemplate` version.

        `<target_version>`
        Specifies the target OpenShift Container Platform version.

        `spec.templateDefaults.upgradeDefaults`
        Defines the default upgrade configuration for standard platform upgrades on multi-node clusters.

        `clusterVersion.cvSpec.channel`
        Specifies the update channel for the target release.

        `clusterVersion.cvSpec.desiredUpdate.version`
        Specifies the target OpenShift Container Platform version.

        <div class="important">

        For disconnected environments, the spoke cluster cannot reach public registries or the public update graph. You must set `cvSpec.desiredUpdate.image` to the mirrored release image in your local registry, set `cvSpec.upstream` to a local OpenShift Update Service (OSUS) instance, and keep the `cvSpec.desiredUpdate.version` aligned with the mirrored release:

        ``` yaml
            upgradeDefaults:
              clusterVersion:
                clusterUpgradeTimeout: 4h
                cvSpec:
                  channel: "stable-<target_version>"
                  upstream: "https://osus.example.com/graph"
                  desiredUpdate:
                    version: "<target_version>"
                    image: "registry.example.com:5000/ocp/release@sha256:<digest>"
        ```

        For more information about updating clusters in disconnected environments with OSUS, see "Updating a cluster in a disconnected environment using the OpenShift Update Service" in *Disconnected environments*.

        </div>

        `spec.templateParameterSchema`
        Defines the full schema for parameters that can be overridden for a specific cluster in the `ProvisioningRequest` CR. Use the `upgradeParameters` section to permit individual deployments to customize the upgrade timeout, intermediate version for EUS-to-EUS upgrades, or target release.

        `clusterVersion.clusterUpgradeTimeout`
        Defines the maximum time allowed for the upgrade to complete.

        `clusterVersion.intermediateVersion`
        Specifies an intermediate OpenShift Container Platform version for EUS-to-EUS upgrades. If not specified, the controller auto-selects the highest valid intermediate version from the update graph.

        <div class="note">

        Do not configure both `imageBasedGroupUpgrade` and `clusterVersion` in the same `ClusterTemplate` CR. Each template must target a single cluster topology.

        </div>

5.  Commit the new resources to the GitOps repository and wait for ArgoCD to synchronize them to the hub cluster.

- Verify that the new `ClusterTemplate` CR is validated on the hub cluster by running the following command:

  ``` terminal
  $ oc get clustertemplates.clcm.openshift.io -n <template_namespace>
  ```

  <div class="formalpara-title">

  **Example output**

  </div>

  ``` terminal
  NAME                   AGE   STATE       DETAILS
  sno-ran-du.v4-22-0-1   10m   Validated   Cluster template has been validated
  ```

  Verify that the STATE column shows `Validated`. If the state shows `Failed`, check the DETAILS column for the validation error.

<!-- -->

- [Mirroring images for a disconnected installation](../disconnected/installing-mirroring-installation-images.xml#installing-mirroring-installation-images)

- [Updating a cluster in a disconnected environment using the OpenShift Update Service](../disconnected/updating/disconnected-update-osus.xml#updating-disconnected-cluster-osus)

# Upgrade a single-node cluster with image-based upgrade

You can upgrade a single-node OpenShift Container Platform cluster by updating the `ProvisioningRequest` custom resource (CR) to reference a new `ClusterTemplate` CR version configured for image-based upgrade. The O-Cloud Manager creates an `ImageBasedGroupUpgrade` CR that orchestrates the upgrade using a seed image containing the pre-installed target version.

- The OpenShift API for Data Protection (OADP) Operator and the Lifecycle Agent (LCA) Operator are installed on the spoke cluster, deployed through Red Hat Advanced Cluster Management (RHACM) policies in the `PolicyGenerator`.

- A compatible seed image for the target OpenShift Container Platform version has been created, and both the target cluster and the seed image have a shared container partition configured for image-based upgrade.

- The spoke cluster is fully provisioned with `provisioningPhase: fulfilled` on the `ProvisioningRequest` CR.

- A new `ClusterTemplate` CR version is prepared for the target release with `upgradeDefaults.imageBasedGroupUpgrade` configured and the `templateParameterSchema.upgradeParameters` schema defined.

1.  Update the `ProvisioningRequest` CR to reference the new `ClusterTemplate` version by running the following command:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateName":"<template_name>","templateVersion":"<new_version>"}}'
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

    `<template_name>`
    Specifies the template name, such as `sno-ran-du`.

    `<new_version>`
    Specifies the new `ClusterTemplate` version for the target release, such as `v4-Y-Z+1-1`.

    The O-Cloud Manager detects the version change and creates an `ImageBasedGroupUpgrade` CR to orchestrate the upgrade.

    <div class="note">

    The `upgradeDefaults` in the `ClusterTemplate` CR define default image-based group upgrade parameters including the seed image, OADP content references, rollback timeout, and the stage rollout plan.

    </div>

<!-- -->

1.  Verify that the upgrade completed successfully by running the following command on the hub cluster:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid>
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                                   DISPLAYNAME   AGE    PROVISIONPHASE   PROVISIONDETAILS
    123e4567-e89b-12d3-a456-426614174000                 120m   fulfilled        Upgrade is completed
    ```

2.  Verify the upgrade progress on the spoke cluster by running the following commands:

    1.  Get the status of the upgrade by running the following command:

        ``` terminal
        $ oc get ibu
        ```

    2.  Get the status of the machine config pools by running the following command:

        ``` terminal
        $ oc get mcp
        ```

- If the `provisioningPhase` shows `failed`, check the `UpgradeCompleted` condition for failure details by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> \
    -o jsonpath='{.status.conditions[?(@.type=="UpgradeCompleted")]}'
  ```

  The `reason` field categorizes the failure: `TimedOut` indicates the upgrade exceeded the configured timeout, `PreconditionChecksFailed` indicates unmet requirements such as schema validation or version mismatch, and `Failed` indicates a runtime error. The `message` field provides specific details about the cause.

<!-- -->

- [Understanding the image-based upgrade for single-node OpenShift clusters](../edge_computing/image_based_upgrade/cnf-understanding-image-based-upgrade.xml#cnf-understanding-image-based-upgrade)

# Upgrade a multi-node cluster

You can upgrade a multi-node OpenShift Container Platform cluster by updating the `ProvisioningRequest` custom resource (CR) to reference a new `ClusterTemplate` CR version configured for the target release.

The O-Cloud Manager patches the `ClusterVersion` CR on the spoke cluster, where the Cluster Version Operator (CVO) orchestrates the component-by-component update of the control plane and worker nodes.

- The `ManagedServiceAccount` addon is enabled on the hub cluster. To verify, check the `MultiClusterEngine` CR by running the following command:

  ``` terminal
  $ oc get multiclusterengines.multicluster.openshift.io multiclusterengine \
      -o jsonpath='{.spec.overrides.components[?(@.name=="managedserviceaccount")].enabled}'
  ```

  If it returns `false` or is not present, enable it by editing the `MultiClusterEngine` CR.

- You completed the standard pre-upgrade preparation tasks on the spoke cluster, such as creating an etcd backup and reviewing deprecated APIs. For further information, see "Preparing to update a cluster".

- The spoke cluster is fully provisioned with `provisioningPhase: fulfilled` on the `ProvisioningRequest` CR.

- A new `ClusterTemplate` CR version is prepared for the target release with `upgradeDefaults.clusterVersion` configured and the `templateParameterSchema.upgradeParameters` schema defined.

1.  Update the `ProvisioningRequest` CR to reference the new `ClusterTemplate` version by running the following command:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateName":"<template_name>","templateVersion":"<new_version>"}}'
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

    `<template_name>`
    Specifies the template name, such as `std-ran-du`.

    `<new_version>`
    Specifies the new `ClusterTemplate` version for the target release, such as `v4-22-0-v1`.

    The O-Cloud Manager detects the version change and orchestrates the upgrade.

    <div class="note">

    For EUS-to-EUS upgrades, the O-Cloud Manager pauses all worker `MachineConfigPool` resources, triggers the intermediate version upgrade on the control plane first, then the target version upgrade, and finally unpauses the pools and waits for workers to update. This prevents workers from rebooting twice. If `intermediateVersion` is not specified in the `upgradeDefaults`, the controller auto-selects the highest valid intermediate version from the update graph.

    Upgrades might remain at the machine config pool phase for extended periods during control plane rolling reboots.

    </div>

<!-- -->

1.  Verify that the upgrade completed successfully by running the following command on the hub cluster:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid>
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                                   DISPLAYNAME   AGE    PROVISIONPHASE   PROVISIONDETAILS
    123e4567-e89b-12d3-a456-426614174000                 180m   fulfilled        Upgrade to version 4.22.0 completed
    ```

2.  Verify the upgrade progress on the spoke cluster by running the following commands:

    1.  Get the status of the upgrade by running the following command:

        ``` terminal
        $ oc adm upgrade status
        ```

    2.  Get the status of the machine config pools by running the following command:

        ``` terminal
        $ oc get mcp
        ```

- If the `provisioningPhase` shows `failed`, check the `UpgradeCompleted` condition for failure details by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> \
    -o jsonpath='{.status.conditions[?(@.type=="UpgradeCompleted")]}'
  ```

  The `reason` field categorizes the failure: `TimedOut` indicates the upgrade exceeded the configured timeout, `PreconditionChecksFailed` indicates unmet requirements such as schema validation or version mismatch, and `Failed` indicates a runtime error. The `message` field provides specific details about the cause.

# Override upgrade parameters for a ProvisioningRequest

You can override the default upgrade parameters defined in the `ClusterTemplate` custom resource (CR) by specifying `upgradeParameters` in the `ProvisioningRequest` CR. Override values are merged with the values you defined in the `upgradeDefaults` field of the `ClusterTemplate` CR, with the values specified in the `ProvisioningRequest` CR taking precedence.

<div class="note">

For image-based upgrades, the `plan` field is an array and is merged by index position. Element 0 of the override merges with element 0 of the defaults, element 1 with element 1, and so on.

</div>

<div class="note">

Both `upgradeDefaults` in the `ClusterTemplate` CR and `upgradeParameters` in the `ProvisioningRequest` CR must conform to the `templateParameterSchema` schema defined in the `ClusterTemplate` CR. Invalid overrides are rejected during validation.

</div>

- A `ClusterTemplate` CR is prepared for the target release with `upgradeDefaults` configured.

- The `templateParameterSchema` in the `ClusterTemplate` CR exposes the `upgradeParameters` sub-schema.

1.  Edit the `ProvisioningRequest` CR to add or update the `spec.templateParameters.upgradeParameters` field by running the following command:

    ``` terminal
    $ oc edit provisioningrequests.clcm.openshift.io <uuid>
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

    1.  For single-node image-based upgrades, you can override any upgrade parameter defined in the `templateParameterSchema`. The following example overrides the seed image and stage timeouts:

        ``` yaml
        spec:
          templateParameters:
            upgradeParameters:
              imageBasedGroupUpgrade:
                ibuSpec:
                  seedImageRef:
                    image: "quay.io/seed-repo/seed-image:4.Y.Z+1-v2"
                plan:
                  - actions: ["Prep"] # index 0
                    rolloutStrategy:
                      timeout: 20
                  - actions: ["AbortOnFailure"] # index 1
                  - actions: ["Upgrade"] # index 2
                    rolloutStrategy:
                      timeout: 90
        ```

        - `seedImageRef.image` overrides the seed image to use a different image tag.

        - `rolloutStrategy.timeout` sets the `Prep` stage timeout to 20 minutes and the `Upgrade` stage timeout to 90 minutes.

        - Fields not specified in `upgradeParameters` are inherited from the `upgradeDefaults` field of the `ClusterTemplate` CR.

          <div class="note">

          During an in-progress image-based upgrade, all parameter changes are ignored until the upgrade completes or fails.

          </div>

    2.  For multi-node standard platform upgrades, you can override any upgrade parameter defined in the `templateParameterSchema`. The following example overrides the timeout and channel specifications:

        ``` yaml
        spec:
          templateParameters:
            upgradeParameters:
              clusterVersion:
                clusterUpgradeTimeout: "6h"
                cvSpec:
                  channel: "eus-4.22"
        ```

        <div class="note">

        During an in-progress upgrade, only `clusterVersion.clusterUpgradeTimeout` is recognized as an update. Other parameter changes are ignored until the upgrade completes or fails.

        </div>

2.  Apply the updated `ProvisioningRequest` CR to the hub cluster, or commit it to the GitOps repository for ArgoCD synchronization.

- Verify that the override is accepted by checking that the upgrade proceeds with the modified parameters by running the following command:

  ``` terminal
  $ oc get provisioningrequests.clcm.openshift.io <uuid> -o jsonpath='{.status.conditions[?(@.type=="UpgradeCompleted")]}'
  ```

# Retry a failed single-node OpenShift cluster upgrade

When an image-based upgrade fails on a single-node OpenShift cluster, the recovery path depends on the failure reason reported in the `UpgradeCompleted` condition. Input errors can be corrected in place, while runtime failures require reverting to the original `ClusterTemplate` version after the automatic rollback completes.

- The `UpgradeCompleted` condition on the `ProvisioningRequest` CR shows `reason: PreconditionChecksFailed`, `reason: Failed`, or `reason: TimedOut`.

1.  Check the `UpgradeCompleted` condition to determine the failure type by running the following command:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid> \
      -o jsonpath='{.status.conditions[?(@.type=="UpgradeCompleted")]}'
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  If the `reason` is `PreconditionChecksFailed`, fix the input error directly:

    The upgrade was not started because a precondition was not met, such as a schema validation failure or version mismatch. Patch the `ProvisioningRequest` CR with corrected `upgradeParameters` or fix the referenced `ClusterTemplate` CR. The O-Cloud Manager re-evaluates the upgrade automatically after the change is detected.

3.  If the `reason` is `TimedOut` or `Failed`, wait for the automatic rollback to complete and then retry:

    1.  Wait for the automatic rollback to complete. The `ImageBasedGroupUpgrade` plan includes `AbortOnFailure` actions that handle rollback and cleanup automatically.

    2.  Revert the `ProvisioningRequest` CR to the original `ClusterTemplate` version by running the following command:

        ``` terminal
        $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
          -p '{"spec":{"templateName":"<template_name>","templateVersion":"<original_version>"}}'
        ```

        where:

        `<template_name>`
        Specifies the template name, such as `sno-ran-du`.

        `<original_version>`
        Specifies the original `ClusterTemplate` version, such as `v4-Y-Z-1`.

    3.  Wait for the `ProvisioningRequest` CR to return to `provisioningPhase: fulfilled`.

    4.  Investigate and resolve the root cause of the failure based on the `message` field from the `UpgradeCompleted` condition, such as a network timeout or seed image issue.

    5.  Re-trigger the upgrade by updating the `ProvisioningRequest` CR to the target `ClusterTemplate` version by running the following command:

        ``` terminal
        $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
          -p '{"spec":{"templateName":"<template_name>","templateVersion":"<target_version>"}}'
        ```

        where:

        `<target_version>`
        Specifies the new `ClusterTemplate` version for the target release.

<!-- -->

1.  Verify that the upgrade completed successfully by running the following command on the hub cluster:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid>
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                                   DISPLAYNAME   AGE    PROVISIONPHASE   PROVISIONDETAILS
    123e4567-e89b-12d3-a456-426614174000                 240m   fulfilled        Upgrade is completed
    ```

2.  Verify the upgrade progress on the spoke cluster by running the following commands:

    1.  Get the status of the upgrade by running the following command:

        ``` terminal
        $ oc get ibu
        ```

    2.  Get the status of the machine config pools by running the following command:

        ``` terminal
        $ oc get mcp
        ```

# Retry a failed multi-node cluster upgrade

When a standard platform upgrade fails on a multi-node OpenShift Container Platform cluster, the recovery path depends on the failure reason reported in the `UpgradeCompleted` condition. Input errors can be corrected in place, while timeout failures require investigating the spoke cluster and determining whether to retry or reconcile a manually completed upgrade.

- The `UpgradeCompleted` condition on the `ProvisioningRequest` CR shows `reason: PreconditionChecksFailed`, or `reason: TimedOut`.

- You have access to the spoke cluster for investigation if the failure reason is `TimedOut`.

1.  Check the `UpgradeCompleted` condition to determine the failure type by running the following command:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid> \
      -o jsonpath='{.status.conditions[?(@.type=="UpgradeCompleted")]}'
    ```

    where:

    `<uuid>`
    Specifies the UUID of the `ProvisioningRequest` CR for the target cluster.

2.  If the `reason` is `PreconditionChecksFailed`, fix the input error directly:

    The upgrade was not started or was rejected because a precondition was not met, such as a schema validation failure, version mismatch, or invalid `ClusterVersion` configuration. Patch the `ProvisioningRequest` CR with corrected `upgradeParameters` values or fix the referenced `ClusterTemplate` CR. The O-Cloud Manager re-evaluates the upgrade automatically after the change is detected.

3.  If the `reason` is `TimedOut`, investigate the spoke cluster to determine the root cause. Check the `UpgradeCompleted` condition `message` for details, which might include Cluster Version Operator conditions such as `Failing` or `Upgradeable=False`.

4.  Resolve the root cause on the spoke cluster, such as fixing a degraded Operator or clearing a misconfigured policy.

5.  Revert the `ProvisioningRequest` CR to the original `ClusterTemplate` version by running the following command:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateName":"<template_name>","templateVersion":"<original_version>"}}'
    ```

    where:

    `<template_name>`
    Specifies the template name, such as `std-ran-du`.

    `<original_version>`
    Specifies the original `ClusterTemplate` version, such as `v4-Y-Z-1`.

6.  Wait for the `ProvisioningRequest` CR to return to `provisioningPhase: fulfilled`.

7.  Re-trigger the upgrade by updating the `ProvisioningRequest` CR to the target `ClusterTemplate` CR version by running the following command:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateName":"<template_name>","templateVersion":"<target_version>"}}'
    ```

    where:

    `<target_version>`
    Specifies the new `ClusterTemplate` CR version for the target release.

    <div class="note">

    If the administrator completed the upgrade to the target version outside of the O-Cloud Manager, you can skip the revert and re-trigger steps. Instead, add or update a `ManagedCluster` label through the `ProvisioningRequest` `clusterInstanceParameters` to trigger reconciliation:

    ``` terminal
    $ oc patch provisioningrequests.clcm.openshift.io <uuid> --type merge \
      -p '{"spec":{"templateParameters":{"clusterInstanceParameters":{"extraLabels":{"ManagedCluster":{"upgrade-reconcile":"true"}}}}}}'
    ```

    The O-Cloud Manager detects that the spoke cluster is already running the target version and transitions the `ProvisioningRequest` CR to `provisioningPhase: fulfilled`.

    </div>

<!-- -->

1.  Verify that the upgrade completed successfully by running the following command on the hub cluster:

    ``` terminal
    $ oc get provisioningrequests.clcm.openshift.io <uuid>
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    NAME                                   DISPLAYNAME   AGE    PROVISIONPHASE   PROVISIONDETAILS
    123e4567-e89b-12d3-a456-426614174000                 300m   fulfilled        Upgrade to version 4.22.0 completed
    ```

2.  Verify the upgrade progress on the spoke cluster by running the following commands:

    1.  Get the status of the upgrade by running the following command:

        ``` terminal
        $ oc adm upgrade
        ```

    2.  Get the status of the machine config pools by running the following command:

        ``` terminal
        $ oc get mcp
        ```

# Upgrade clusters with the Provisioning API

You can trigger a cluster upgrade through the Provisioning REST API by sending an update request with a new `templateVersion` that references a `ClusterTemplate` CR configured for the target release. Because `ClusterTemplate` CRs and their referenced `ConfigMap` CRs are immutable after validation, a new `ClusterTemplate` CR version must be prepared for the target release before sending the upgrade request. This method is used by SMO frameworks and external automation systems that manage cluster upgrades programmatically.

- You authenticated to the O-Cloud Manager REST API and set the `MY_TOKEN` environment variable.

- The cluster is fully provisioned with `provisioningPhase: fulfilled`.

- A new `ClusterTemplate` CR version configured for the target OpenShift Container Platform release exists on the hub cluster.

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

4.  Modify the `current-request.json` file to update the `templateVersion` field to the new release version. The following example upgrades from version `v4-Y-Z-1` to `v4-Y-Z+1-1`:

    ``` json
    {
      "name": "sno1-provisioning-request",
      "description": "SNO RAN DU cluster at site-east-1",
      "provisioningRequestId": "<uuid>",
      "templateName": "sno-ran-du",
      "templateVersion": "v4-Y-Z+1-1",
      "templateParameters": {
        "nodeClusterName": "sno1",
        "oCloudSiteId": "site-east-1",
        "clusterInstanceParameters": {
          "clusterName": "sno1",
          "nodeGroups": [ ... ]
        },
        "policyTemplateParameters": { ... }
      }
    }
    ```

    - The `templateVersion` value must match the version of the new `ClusterTemplate` CR prepared for the target release.

    - All other fields remain unchanged unless the new template requires different parameter values.

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

- Query the provisioning request status and verify that the upgrade completes by running the following command:

  ``` terminal
  $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
    "${PROV_URL}/provisioningRequests/<uuid>" | jq -r '.status.provisioningPhase'
  ```

  The `provisioningPhase` transitions from `progressing` to `fulfilled` when the upgrade completes successfully.
