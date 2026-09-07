The `virt-platform-autopilot` controller replaces manual postinstallation configuration by automatically applying opinionated defaults to the virtualization platform and installed optional components. You can customize or opt out of any managed configuration.

# How automated postinstallation configuration works

After you install OpenShift Virtualization, the `virt-platform-autopilot` controller continuously reconciles managed resources to keep the expected state and correct configuration drift. It also configures optional components such as the Kube Descheduler Operator and the Cluster Observability Operator if they are installed.

The `virt-platform-autopilot` controller manages the following configurations:

Load-aware descheduler
Configures the Kube Descheduler Operator to balance virtual machine (VM) workloads across nodes based on CPU and memory use. Requires the Kube Descheduler Operator to be installed.

Observability enhancements
Enhances observability with additional Prometheus alerting rules and advanced Perses dashboards in the OpenShift Container Platform web console.

Swap enablement
Enables OpenShift Container Platform worker nodes to safely use swap for virtualization workloads. Swap requires pre-provisioned, dedicated storage to be available.

## Soft dependency model

The `virt-platform-autopilot` controller does not install optional components. It configures components that are already installed on the cluster. If an optional component is not installed, the `virt-platform-autopilot` controller skips that configuration and continues without error.

When you install an optional component later, the `virt-platform-autopilot` controller detects it on the next reconciliation cycle and applies the relevant configuration automatically.

## Reconciliation and anti-thrashing behavior

The `virt-platform-autopilot` controller continuously reconciles managed resources to keep the expected state. If an external process changes a managed resource, the `virt-platform-autopilot` controller detects the drift and restores the expected state.

To prevent thrashing, the `virt-platform-autopilot` controller monitors the rate of changes to managed resources. If the `virt-platform-autopilot` controller detects rapid or repeated changes, it pauses reconciliation for the affected resources. This prevents a loop where the `virt-platform-autopilot` controller and another controller repeatedly overwrite each other’s changes. You can monitor paused resources by using the `kubevirt_autopilot_paused_resources` metric.

# Customize or opt-out of managed configurations

The `virt-platform-autopilot` controller applies opinionated defaults, but you can override managed configurations to suit your environment.

Customize specific values
Keep a resource managed by the controller, but apply a JSON patch on top of the reconciled configuration to retain your custom settings.

Exclude specific fields from reconciliation
Keep a resource managed by the controller, but mask individual fields so that the controller ignores them during reconciliation.

Stop reconciliation of a resource
Mark a resource as unmanaged so that the controller does not reconcile it after it is created. You take full ownership of that resource’s configuration.

Exclude a resource entirely
Prevent the controller from creating or reconciling a resource by disabling it in the `HyperConverged` custom resource (CR).

You can combine these approaches across different resources in the same cluster.

## Exclude a resource from being managed by the `virt-platform-autopilot` controller

Disabled resources are not created or reconciled automatically by the `virt-platform-autopilot` controller. You can disable a resource by adding it to the `platform.kubevirt.io/disabled-resources` annotation in the `HyperConverged` custom resource (CR).

- You have installed the OpenShift CLI (`oc`).

- You have logged in to the cluster as a user with `cluster-admin` privileges.

- The `virt-platform-autopilot` controller is enabled on the cluster.

1.  Edit the `HyperConverged` CR and add resources to the `platform.kubevirt.io/disabled-resources` annotation:

    Example `HyperConverged` CR:

    ``` yaml
    apiVersion: hco.kubevirt.io/v1beta1
    kind: HyperConverged
    metadata:
      annotations:
        platform.kubevirt.io/disabled-resources: |
          - kind: KubeDescheduler
            name: cluster
          - kind: MachineConfig
            name: 90-worker-swap-online
    ```

2.  Apply your changes to the `HyperConverged` CR by running the following command:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

## Customize specific values in a managed resource

You can customize specific values in a managed resource. The resource remains managed by the `virt-platform-autopilot` controller, but the controller applies an extra JSON patch on top of the reconciled configuration to retain your custom settings.

<div class="important">

Deleting an unmanaged resource causes any annotations on that resource to be lost. The `virt-platform-autopilot` controller then creates a new, opinionated version of the resource.

To prevent the `virt-platform-autopilot` controller from recreating deleted resources, you must disable the resource. You can disable resources by adding them to the `platform.kubevirt.io/disabled-resources` annotation in the `HyperConverged` custom resource (CR).

For more information, see "Exclude a resource from being managed by the `virt-platform-autopilot` controller".

</div>

- You have installed the OpenShift CLI (`oc`).

- You have logged in to the cluster as a user with `cluster-admin` privileges.

- The `virt-platform-autopilot` controller is enabled on the cluster.

- The `platform.kubevirt.io/mode=unmanaged` and `platform.kubevirt.io/ignore-fields` annotations must not be present on the resource.

1.  Add the `platform.kubevirt.io/patch` annotation to a resource with a valid RFC 6902 JSON Patch operations array.

    For example, to prevent the `virt-platform-autopilot` controller from overriding a custom descheduler profile configuration, run the following command:

    ``` terminal
    $ oc annotate kubedescheduler cluster \
      'platform.kubevirt.io/patch=[{"op":"replace","path":"/spec/profileCustomizations","value":{"devKnobs":{}}}]' \
      -n openshift-kube-descheduler-operator
    ```

    The `virt-platform-autopilot` controller continues to manage all other fields on the resource but skips the specified paths.

    <div class="important">

    JSON patches are blocked on sensitive resources, including `MachineConfig` and `KubeletConfig` resources.

    </div>

2.  Optional: To restore `virt-platform-autopilot` controller management for all fields, remove the `platform.kubevirt.io/patch` annotation.

    For example, to restore `virt-platform-autopilot` controller management for all fields of the descheduler configuration, run the following command:

    ``` terminal
    $ oc annotate kubedescheduler cluster \
      platform.kubevirt.io/patch- \
      -n openshift-kube-descheduler-operator
    ```

## Exclude specific fields from reconciliation in a managed resource

You can exclude specific fields from being managed by the `virt-platform-autopilot` controller so that it ignores them during reconciliation.

<div class="important">

Deleting an unmanaged resource causes any annotations on that resource to be lost. The `virt-platform-autopilot` controller then creates a new, opinionated version of the resource.

To prevent the `virt-platform-autopilot` controller from recreating deleted resources, you must disable the resource. You can disable resources by adding them to the `platform.kubevirt.io/disabled-resources` annotation in the `HyperConverged` custom resource (CR).

For more information, see "Exclude a resource from being managed by the `virt-platform-autopilot` controller".

</div>

- You have installed the OpenShift CLI (`oc`).

- You have logged in to the cluster as a user with `cluster-admin` privileges.

- The `virt-platform-autopilot` controller is enabled on the cluster.

- The `platform.kubevirt.io/mode=unmanaged` and `platform.kubevirt.io/patch` annotations must not be present on the resource.

1.  Add the `platform.kubevirt.io/ignore-fields` annotation with a comma-separated list of RFC 6901 JSON Pointer paths.

    For example, to prevent the `virt-platform-autopilot` controller from overriding a systemd unit in a managed `MachineConfig` resource, run the following command:

    ``` terminal
    $ oc annotate machineconfig 90-worker-swap-online \
      platform.kubevirt.io/ignore-fields='/spec/config/systemd/units/0/contents'
    ```

2.  Optional: To restore `virt-platform-autopilot` controller management for all fields, remove the `platform.kubevirt.io/ignore-fields` annotation.

    For example, to restore `virt-platform-autopilot` controller management for all fields of the descheduler configuration, run the following command:

    ``` terminal
    $ oc annotate kubedescheduler cluster \
      platform.kubevirt.io/ignore-fields- \
      -n openshift-kube-descheduler-operator
    ```

## Stop reconciliation of a managed resource

You can stop the `virt-platform-autopilot` controller entirely from reconciling a resource after it is created, by setting the `platform.kubevirt.io/mode=unmanaged` annotation for that resource.

<div class="important">

Deleting an unmanaged resource causes any annotations on that resource to be lost. The `virt-platform-autopilot` controller then creates a new, opinionated version of the resource.

To prevent the `virt-platform-autopilot` controller from recreating deleted resources, you must disable the resource. You can disable resources by adding them to the `platform.kubevirt.io/disabled-resources` annotation in the `HyperConverged` custom resource (CR).

For more information, see "Exclude a resource from being managed by the `virt-platform-autopilot` controller".

</div>

- You have installed the OpenShift CLI (`oc`).

- You have logged in to the cluster as a user with `cluster-admin` privileges.

- The `virt-platform-autopilot` controller is enabled on the cluster.

- The `platform.kubevirt.io/ignore-fields` and `platform.kubevirt.io/patch` annotations must not be present on the resource.

1.  Set the `platform.kubevirt.io/mode` annotation for the resource to `unmanaged`.

    For example, to stop the `virt-platform-autopilot` controller from managing the descheduler configuration, run the following command:

    ``` terminal
    $ oc annotate kubedescheduler cluster \
      platform.kubevirt.io/mode=unmanaged \
      -n openshift-kube-descheduler-operator
    ```

2.  Optional: To restore `virt-platform-autopilot` controller management for a resource, remove the `platform.kubevirt.io/mode` annotation.

    For example, to restore `virt-platform-autopilot` controller management for the descheduler configuration, run the following command:

    ``` terminal
    $ oc annotate kubedescheduler cluster \
      platform.kubevirt.io/mode- \
      -n openshift-kube-descheduler-operator
    ```

# Additional resources

- [Configure higher VM workload density](../../virt/post_installation_configuration/virt-configuring-higher-vm-workload-density.xml#virt-configuring-higher-vm-workload-density)
