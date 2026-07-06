As an administrator, you can expose a set of host and virtual machine (VM) metrics to a guest VM by enabling the `downwardMetrics` feature gate and configuring a downward metrics device. You can view these metrics by using the command line or the `vm-dump-metrics` tool.

<div class="note">

On Red Hat Enterprise Linux (RHEL) 9, use the command line to view downward metrics.

The `vm-dump-metrics` tool is not supported on the Red Hat Enterprise Linux (RHEL) 9 platform.

</div>

# Enabling or disabling the downward metrics feature gate in a YAML file

To expose downward metrics for a host virtual machine, you can enable the `downwardMetrics` feature gate by editing a YAML file.

- You must have administrator privileges to enable the feature gate.

- You have installed the OpenShift CLI (`oc`).

1.  Open the HyperConverged custom resource (CR) in your default editor by running the following command:

    ``` terminal
    $ oc edit hco kubevirt-hyperconverged -n openshift-cnv
    ```

2.  Choose to enable or disable the downwardMetrics feature gate as follows:

    - To enable the `downwardMetrics` feature gate, add a feature gate entry with `name: downwardMetrics`. For example:

      ``` yaml
      apiVersion: hco.kubevirt.io/v1
      kind: HyperConverged
      metadata:
        name: kubevirt-hyperconverged
        namespace: openshift-cnv
      spec:
        featureGates:
          - name: downwardMetrics
      # ...
      ```

    - To disable the `downwardMetrics` feature gate, set the `state` to `Disabled`. For example:

      ``` yaml
      apiVersion: hco.kubevirt.io/v1
      kind: HyperConverged
      metadata:
        name: kubevirt-hyperconverged
        namespace: openshift-cnv
      spec:
        featureGates:
          - name: downwardMetrics
            state: Disabled
      # ...
      ```

# Enabling or disabling the downward metrics feature gate from the CLI

To expose downward metrics for a host virtual machine, you can enable the `downwardMetrics` feature gate by using the command line.

- You must have administrator privileges to enable the feature gate.

- You have installed the OpenShift CLI (`oc`).

<!-- -->

- Choose to enable or disable the `downwardMetrics` feature gate as follows:

  - Enable the `downwardMetrics` feature gate by running the command shown in the following example:

    ``` terminal
    $ oc patch hco kubevirt-hyperconverged -n openshift-cnv \
      --type json -p '[{"op": "add", "path": "/spec/featureGates/-", \
      "value": {"name": "downwardMetrics"}}]'
    ```

  - Disable the `downwardMetrics` feature gate by running the command shown in the following example:

    ``` terminal
    $ oc patch hco kubevirt-hyperconverged -n openshift-cnv \
      --type json -p '[{"op": "add", "path": "/spec/featureGates/-", \
      "value": {"name": "downwardMetrics", "state": "Disabled"}}]'
    ```

# Configuring a downward metrics device

You can enable the capturing of downward metrics for a host VM by creating a configuration file that includes a `downwardMetrics` device. Adding this device establishes that the metrics are exposed through a `virtio-serial` port.

- You must first enable the `downwardMetrics` feature gate.

<!-- -->

- Edit or create a YAML file that includes a `downwardMetrics` device, as shown in the following example:

  ``` yaml
  apiVersion: kubevirt.io/v1
  kind: VirtualMachine
  metadata:
    name: fedora
    namespace: default
  spec:
    dataVolumeTemplates:
      - metadata:
          name: fedora-volume
        spec:
          sourceRef:
            kind: DataSource
            name: fedora
            namespace: openshift-virtualization-os-images
          storage:
            resources: {}
    instancetype:
      name: u1.medium
    runStrategy: Always
    template:
      metadata:
        labels:
          app.kubernetes.io/name: headless
      spec:
        domain:
          devices:
            downwardMetrics: {}
        subdomain: headless
        volumes:
          - dataVolume:
              name: fedora-volume
            name: rootdisk
          - cloudInitNoCloud:
              userData: |
                #cloud-config
                chpasswd:
                  expire: false
                password: '<password>'
                user: fedora
            name: cloudinitdisk
  ```

- `spec.domain.devices.downwardMetrics` defines the `downwardMetrics` device.

- `spec.volumes.cloudInitNoCloud.userdata.password` defines the password for the `fedora` user.

# Viewing downward metrics by using the CLI

You can view downward metrics by entering a command from inside a guest virtual machine (VM).

- Run the following commands:

  ``` terminal
  $ sudo sh -c 'printf "GET /metrics/XML\n\n" > /dev/virtio-ports/org.github.vhostmd.1'
  ```

  ``` terminal
  $ sudo cat /dev/virtio-ports/org.github.vhostmd.1
  ```

# Viewing downward metrics by using the vm-dump-metrics tool

To view downward metrics, install the `vm-dump-metrics` tool and then use the tool to expose the metrics results.

<div class="note">

On Red Hat Enterprise Linux (RHEL) 9, use the command line to view downward metrics. The vm-dump-metrics tool is not supported on the Red Hat Enterprise Linux (RHEL) 9 platform.

</div>

1.  Install the `vm-dump-metrics` tool by running the following command:

    ``` terminal
    $ sudo dnf install -y vm-dump-metrics
    ```

2.  Retrieve the metrics results by running the following command:

    ``` terminal
    $ sudo vm-dump-metrics
    ```

    Example output:

    ``` xml
    <metrics>
      <metric type="string" context="host">
        <name>HostName</name>
        <value>node01</value>
    [...]
      <metric type="int64" context="host" unit="s">
        <name>Time</name>
        <value>1619008605</value>
      </metric>
      <metric type="string" context="host">
        <name>VirtualizationVendor</name>
        <value>kubevirt.io</value>
      </metric>
    </metrics>
    ```

# Additional resources

- [Viewing downward metrics by using the command line](../../virt/monitoring/virt-exposing-downward-metrics.xml#virt-viewing-downward-metrics-cli_virt-exposing-downward-metrics)
