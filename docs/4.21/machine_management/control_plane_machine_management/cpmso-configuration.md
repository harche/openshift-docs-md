This example YAML snippet shows the base structure for a control plane machine set custom resource (CR).

# Sample YAML for a control plane machine set custom resource

The base of the `ControlPlaneMachineSet` CR is structured the same way for all platforms.

<div class="formalpara">

<div class="title">

Sample `ControlPlaneMachineSet` CR YAML file

</div>

``` yaml
apiVersion: machine.openshift.io/v1
kind: ControlPlaneMachineSet
metadata:
  name: cluster
  namespace: openshift-machine-api
spec:
  replicas: 3
  selector:
    matchLabels:
      machine.openshift.io/cluster-api-cluster: <cluster_id>
      machine.openshift.io/cluster-api-machine-role: master
      machine.openshift.io/cluster-api-machine-type: master
  state: Active
  strategy:
    type: RollingUpdate
  template:
    machineType: machines_v1beta1_machine_openshift_io
    machines_v1beta1_machine_openshift_io:
      failureDomains:
        platform: <platform>
        <platform_failure_domains>
      metadata:
        labels:
          machine.openshift.io/cluster-api-cluster: <cluster_id>
          machine.openshift.io/cluster-api-machine-role: master
          machine.openshift.io/cluster-api-machine-type: master
      spec:
        providerSpec:
          value:
            <platform_provider_spec>
```

</div>

- Specifies the name of the `ControlPlaneMachineSet` CR, which is `cluster`. Do not change this value.

- Specifies the number of control plane machines. Only clusters with three control plane machines are supported, so the `replicas` value is `3`. Horizontal scaling is not supported. Do not change this value.

- Specifies the infrastructure ID that is based on the cluster ID that you set when you provisioned the cluster. You must specify this value when you create a `ControlPlaneMachineSet` CR. If you have the OpenShift CLI (`oc`) installed, you can obtain the infrastructure ID by running the following command:

  ``` terminal
  $ oc get -o jsonpath='{.status.infrastructureName}{"\n"}' infrastructure cluster
  ```

- Specifies the state of the Operator. When the state is `Inactive`, the Operator is not operational. You can activate the Operator by setting the value to `Active`.

  > [!IMPORTANT]
  > Before you activate the Operator, you must ensure that the `ControlPlaneMachineSet` CR configuration is correct for your cluster requirements. For more information about activating the Control Plane Machine Set Operator, see "Getting started with control plane machine sets".

- Specifies the update strategy for the cluster. The allowed values are `OnDelete` and `RollingUpdate`. The default value is `RollingUpdate`. For more information about update strategies, see "Updating the control plane configuration".

- Specifies the cloud provider platform name. Do not change this value.

- Specifies the `<platform_failure_domains>` configuration for the cluster. The format and values of this section are provider-specific. For more information, see the sample failure domain configuration for your cloud provider.

- Specifies the `<platform_provider_spec>` configuration for the cluster. The format and values of this section are provider-specific. For more information, see the sample provider specification for your cloud provider.

<div>

<div class="title">

Additional resources

</div>

- [Getting started with control plane machine sets](../../machine_management/control_plane_machine_management/cpmso-getting-started.xml#cpmso-getting-started)

- [Updating the control plane configuration](../../machine_management/control_plane_machine_management/cpmso-managing-machines.xml#cpmso-feat-config-update_cpmso-managing-machines)

</div>

# Control plane machine set configuration options

You can configure your control plane machine set to customize your cluster to your needs.

## Adding a custom prefix to control plane machine names

You can customize the prefix of machine names that the control plane machine set creates. This can be done by editing the `ControlPlaneMachineSet` custom resource (CR).

<div>

<div class="title">

Procedure

</div>

1.  Edit the `ControlPlaneMachineSet` CR by running the following command:

    ``` terminal
    $ oc edit controlplanemachineset.machine.openshift.io cluster \
      -n openshift-machine-api
    ```

2.  Edit the `.spec.machineNamePrefix` field of the `ControlPlaneMachineSet` CR:

    ``` yaml
    apiVersion: machine.openshift.io/v1
    kind: ControlPlaneMachineSet
    metadata:
      name: cluster
      namespace: openshift-machine-api
    spec:
      machineNamePrefix: <machine_prefix>
    # ...
    ```

    where `<machine_prefix>` specifies a prefix name that follows the requirements for a lowercase RFC 1123 subdomain.

    > [!IMPORTANT]
    > A lowercase RFC 1123 subdomain must consist of only lowercase alphanumeric characters, hyphens ('-'), and periods ('.'). Each block, separated by periods, must start and end with an alphanumeric character. Hyphens are not allowed at the start or end of a block, and consecutive periods are not permitted.

3.  Save your changes.

</div>

<div>

<div class="title">

Next steps

</div>

- If you changed only the value of the `machineNamePrefix` parameter, clusters that use the default `RollingUpdate` update strategy are not automatically updated. To propagate this change, you must replace your control plane machines manually, regardless of the update strategy for the cluster. For more information, see "Replacing a control plane machine".

</div>

<div>

<div class="title">

Additional resources

</div>

- [Replacing a control plane machine](../../machine_management/control_plane_machine_management/cpmso-managing-machines.xml#cpmso-feat-replace_cpmso-managing-machines)

</div>

# Provider-specific configuration options

The `<platform_provider_spec>` and `<platform_failure_domains>` sections of the control plane machine set manifests are provider specific. For provider-specific configuration options for your cluster, see the following resources:

- [Control plane configuration options for Amazon Web Services](../../machine_management/control_plane_machine_management/cpmso_provider_configurations/cpmso-config-options-aws.xml#cpmso-config-options-aws)

- [Control plane configuration options for Google Cloud](../../machine_management/control_plane_machine_management/cpmso_provider_configurations/cpmso-config-options-gcp.xml#cpmso-config-options-gcp)

- [Control plane configuration options for Microsoft Azure](../../machine_management/control_plane_machine_management/cpmso_provider_configurations/cpmso-config-options-azure.xml#cpmso-config-options-azure)

- [Control plane configuration options for Nutanix](../../machine_management/control_plane_machine_management/cpmso_provider_configurations/cpmso-config-options-nutanix.xml#cpmso-config-options-nutanix)

- [Control plane configuration options for Red Hat OpenStack Platform (RHOSP)](../../machine_management/control_plane_machine_management/cpmso_provider_configurations/cpmso-config-options-openstack.xml#cpmso-config-options-openstack)

- [Control plane configuration options for VMware vSphere](../../machine_management/control_plane_machine_management/cpmso_provider_configurations/cpmso-config-options-vsphere.xml#cpmso-config-options-vsphere)
