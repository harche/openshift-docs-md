Define probes and watchdogs in the `VirtualMachine` resource to configure virtual machine (VM) health checks. Health checks monitor and report the internal state of a VM.

You can configure VM health checks by defining readiness and liveness probes in the `VirtualMachine` resource.

# About readiness and liveness probes

Use readiness and liveness probes to detect and handle unhealthy virtual machines (VMs). You can include one or more probes in the specification of the VM to ensure that traffic does not reach a VM that is not ready for it and that a new VM is created when a VM becomes unresponsive.

A *readiness probe* determines whether a VM is ready to accept service requests. If the probe fails, the VM is removed from the list of available endpoints until the VM is ready.

A *liveness probe* determines whether a VM is responsive. If the probe fails, the VM is deleted and a new VM is created to restore responsiveness.

You can configure readiness and liveness probes by setting the `spec.readinessProbe` and the `spec.livenessProbe` fields of the `VirtualMachine` object. These fields support the following tests:

HTTP GET
The probe determines the health of the VM by using a web hook. The test is successful if the HTTP response code is between 200 and 399. You can use an HTTP GET test with applications that return HTTP status codes when they are completely initialized.

TCP socket
The probe attempts to open a socket to the VM. The VM is only considered healthy if the probe can establish a connection. You can use a TCP socket test with applications that do not start listening until initialization is complete.

Guest agent ping
The probe uses the `guest-ping` command to determine if the QEMU guest agent is running on the virtual machine.

## Defining an HTTP readiness probe

You can define an HTTP readiness probe by setting the `spec.readinessProbe.httpGet` field of the virtual machine (VM) configuration.

- You have installed the OpenShift CLI (`oc`).

1.  Include details of the readiness probe in the VM configuration file.

    Sample readiness probe with an HTTP GET test:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      annotations:
      name: fedora-vm
      namespace: example-namespace
    # ...
    spec:
      template:
        spec:
          readinessProbe:
            httpGet:
              port: 1500
              path: /healthz
              httpHeaders:
              - name: Custom-Header
                value: Awesome
            initialDelaySeconds: 120
            periodSeconds: 20
            timeoutSeconds: 10
            failureThreshold: 3
            successThreshold: 3
    # ...
    ```

    - `spec.template.spec.readinessProbe.httpGet` defines the HTTP GET request to perform to connect to the VM.

    - `spec.template.spec.readinessProbe.httpGet.port` defines the port of the VM that the probe queries. In the above example, the probe queries port 1500.

    - `spec.template.spec.readinessProbe.httpGet.path` defines the path to access on the HTTP server. In the above example, if the handler for the server’s /healthz path returns a success code, the VM is considered to be healthy. If the handler returns a failure code, the VM is removed from the list of available endpoints.

    - `spec.template.spec.readinessProbe.initialDelaySeconds` defines the time, in seconds, after the VM starts before the readiness probe is initiated.

    - `spec.template.spec.readinessProbe.periodSeconds` defines the delay, in seconds, between performing probes. The default delay is 10 seconds. This value must be greater than `timeoutSeconds`.

    - `spec.template.spec.readinessProbe.timeoutSeconds` defines the number of seconds of inactivity after which the probe times out and the VM is assumed to have failed. The default value is 1. This value must be lower than `periodSeconds`.

    - `spec.template.spec.readinessProbe.failureThreshold` defines the number of times that the probe is allowed to fail. The default is 3. After the specified number of attempts, the pod is marked `Unready`.

    - `spec.template.spec.readinessProbe.successThreshold` defines the number of times that the probe must report success, after a failure, to be considered successful. The default is 1.

2.  Create the VM by running the following command:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

## Defining a TCP readiness probe

You can define a TCP readiness probe by setting the `spec.readinessProbe.tcpSocket` field of the virtual machine (VM) configuration.

- You have installed the OpenShift CLI (`oc`).

1.  Include details of the TCP readiness probe in the VM configuration file.

    Sample readiness probe with a TCP socket test:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      annotations:
      name: fedora-vm
      namespace: example-namespace
    # ...
    spec:
      template:
        spec:
          readinessProbe:
            initialDelaySeconds: 120
            periodSeconds: 20
            tcpSocket:
              port: 1500
            timeoutSeconds: 10
    # ...
    ```

    - `spec.template.spec.readinessProbe.initialDelaySeconds` defines the time, in seconds, after the VM starts before the readiness probe is initiated.

    - `` spec.template.spec.readinessProbe.periodSeconds`defines the delay, in seconds, between performing probes. The default delay is 10 seconds. This value must be greater than `timeoutSeconds ``.

    - `spec.template.spec.readinessProbe.tcpSocket` defines the TCP action to perform.

    - `spec.template.spec.readinessProbe.tcpSocket.port` defines the port of the VM that the probe queries.

    - `spec.template.spec.readinessProbe.timeoutSeconds` defines the number of seconds of inactivity after which the probe times out and the VM is assumed to have failed. The default value is 1. This value must be lower than `periodSeconds`.

2.  Create the VM by running the following command:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

## Defining an HTTP liveness probe

Define an HTTP liveness probe by setting the `spec.livenessProbe.httpGet` field of the virtual machine (VM) configuration. You can define both HTTP and TCP tests for liveness probes in the same way as readiness probes. This procedure configures a sample liveness probe with an HTTP GET test.

- You have installed the OpenShift CLI (`oc`).

1.  Include details of the HTTP liveness probe in the VM configuration file.

    Sample liveness probe with an HTTP GET test:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      annotations:
      name: fedora-vm
      namespace: example-namespace
    # ...
    spec:
      template:
        spec:
          livenessProbe:
            initialDelaySeconds: 120
            periodSeconds: 20
            httpGet:
              port: 1500
              path: /healthz
              httpHeaders:
              - name: Custom-Header
                value: Awesome
            timeoutSeconds: 10
    # ...
    ```

    - `spec.tenmplate.spec.livenessProbe.initialDelaySeconds` defines the time, in seconds, after the VM starts before the liveness probe is initiated.

    - `spec.tenmplate.spec.livenessProbe.periodSeconds` defines the delay, in seconds, between performing probes. The default delay is 10 seconds. This value must be greater than `timeoutSeconds`.

    - `spec.tenmplate.spec.livenessProbe.httpGet` defines the HTTP GET request to perform to connect to the VM.

    - `spec.tenmplate.spec.livenessProbe.httpGet.port` defines the port of the VM that the probe queries. In the above example, the probe queries port 1500. The VM installs and runs a minimal HTTP server on port 1500 via cloud-init.

    - `spec.tenmplate.spec.livenessProbe.httpGet.path` defines the path to access on the HTTP server. In the above example, if the handler for the server’s `/healthz` path returns a success code, the VM is considered to be healthy. If the handler returns a failure code, the VM is deleted and a new VM is created.

    - `spec.tenmplate.spec.livenessProbe.timeoutSeconds` defines the number of seconds of inactivity after which the probe times out and the VM is assumed to have failed. The default value is 1. This value must be lower than `periodSeconds`.

2.  Create the VM by running the following command:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

# About watchdogs

Watchdog devices monitor guest operating system responsiveness and trigger recovery actions when a virtual machine becomes unresponsive.

A watchdog device continuously monitors the agent running on a virtual machine (VM). When the guest operating system becomes unresponsive, the watchdog can trigger one of three recovery actions depending on how it is configured.

The `poweroff` action causes the VM to power down immediately. If `spec.runStrategy` is not set to `manual`, the VM automatically reboots after powering down.

The `reset` action reboots the VM in place without allowing the guest operating system to react. When using the reset action, be aware that the reboot time might cause liveness probes to time out. If cluster-level protections detect a failed liveness probe, the VM might be forcibly rescheduled, which increases the overall reboot time.

The `shutdown` action initiates a graceful shutdown by stopping all services before powering down the VM.

<div class="note">

Watchdog functionality is not available for Windows VMs.

</div>

To implement watchdog functionality, you must configure the watchdog device for the VM and install the watchdog agent on the guest operating system.

## Configuring a watchdog device for the virtual machine

You configure a watchdog device for the virtual machine (VM).

- For `x86` systems, the VM must use a kernel that works with the `i6300esb` watchdog device. If you use `s390x` architecture, the kernel must be enabled for `diag288`. Red Hat Enterprise Linux (RHEL) images support `i6300esb` and `diag288`.

- You have installed the OpenShift CLI (`oc`).

1.  Create a `YAML` file with the following contents:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      labels:
        kubevirt.io/vm: <vm-label>
      name: <vm-name>
    spec:
      runStrategy: Halted
      template:
        metadata:
          labels:
            kubevirt.io/vm: <vm-label>
        spec:
          domain:
            devices:
              watchdog:
                name: <watchdog>
                <watchdog-device-model>:
                  action: "poweroff"
    # ...
    ```

    - `spec.template.spec.domain.devices.watchdog.name.<watchdog-device-model>` defines the watchdog device model to use. For `x86` specify `i6300esb`. For `s390x` specify `diag288`.

    - `spec.template.spec.domain.devices.watchdog.name.<watchdog-device-model>.action` defines the watchdog device action. Specify `poweroff`, `reset`, or `shutdown`. The `shutdown` action requires that the guest virtual machine is responsive to ACPI signals. Using `shutdown` is not recommended.

      The example above configures the watchdog device on a VM with the `poweroff` action and exposes the device as `/dev/watchdog`.

      This device can now be used by the watchdog binary.

2.  Apply the YAML file to your cluster by running the following command:

    ``` yaml
    $ oc apply -f <file_name>.yaml
    ```

<!-- -->

1.  Run the following command to verify that the VM is connected to the watchdog device:

    <div class="important">

    Verification steps are provided for testing watchdog functionality only and must not be run on production machines.

    </div>

    ``` terminal
    $ lspci | grep watchdog -i
    ```

2.  Run one of the following commands to confirm the watchdog is active:

    - Trigger a kernel panic:

      ``` terminal
      # echo c > /proc/sysrq-trigger
      ```

    - Stop the watchdog service:

      ``` terminal
      # pkill -9 watchdog
      ```

## Installing the watchdog agent on the guest

You can install the watchdog agent on the guest and start the `watchdog` service.

1.  Log in to the virtual machine as root user.

2.  This step is only required when installing on IBM Z® (`s390x`). Enable `watchdog` by running the following command:

    ``` terminal
    # modprobe diag288_wdt
    ```

3.  Verify that the `/dev/watchdog` file path is present in the VM by running the following command:

    ``` terminal
    # ls /dev/watchdog
    ```

4.  Install the `watchdog` package and its dependencies:

    ``` terminal
    # yum install watchdog
    ```

5.  Uncomment the following line in the `/etc/watchdog.conf` file and save the changes:

    ``` terminal
    #watchdog-device = /dev/watchdog
    ```

6.  Enable the `watchdog` service to start on boot:

    ``` terminal
    # systemctl enable --now watchdog.service
    ```

# Defining a guest agent ping probe

You can define a guest agent ping probe by setting the `spec.readinessProbe.guestAgentPing` field of the virtual machine (VM) configuration.

- The QEMU guest agent must be installed and enabled on the virtual machine.

- You have installed the OpenShift CLI (`oc`).

1.  Include details of the guest agent ping probe in the VM configuration file. For example:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      annotations:
      name: fedora-vm
      namespace: example-namespace
    # ...
    spec:
      template:
        spec:
          readinessProbe:
            guestAgentPing: {}
            initialDelaySeconds: 120
            periodSeconds: 20
            timeoutSeconds: 10
            failureThreshold: 3
            successThreshold: 3
    # ...
    ```

    - `spec.template.spec.readinessProbe.guestAgentPing` defines the guest agent ping probe to connect to the VM.

    - `spec.template.spec.readinessProbe.initialDelaySeconds` defines the time, in seconds, after the VM starts before the guest agent probe is initiated. This value is optional.

    - `spec.template.spec.readinessProbe.periodSeconds` defines the delay, in seconds, between performing probes. The default delay is 10 seconds. This value must be greater than `timeoutSeconds`. This value is optional

    - `spec.template.spec.readinessProbe.timeoutSeconds` defines the number of seconds of inactivity after which the probe times out and the VM is assumed to have failed. The default value is 1. This value must be lower than `periodSeconds`. This value is optional.

    - `spec.template.spec.readinessProbe.failureThreshold` defines the number of times that the probe is allowed to fail. The default is 3. After the specified number of attempts, the pod is marked `Unready`. This value is optional.

    - `spec.template.spec.readinessProbe.successThreshold` defines the number of times that the probe must report success, after a failure, to be considered successful. The default is 1. This value is optional.

2.  Create the VM by running the following command:

    ``` terminal
    $ oc create -f <file_name>.yaml
    ```

## About pausing guest agent ping probes

During maintenance operations such as guest OS updates, the QEMU guest agent might become temporarily unavailable. If a `GuestAgentPing` liveness probe is configured, probe failures cause the kubelet to restart the pod, which destroys the running virtual machine (VM).

You can prevent unwanted pod restarts by temporarily pausing `GuestAgentPing` probes. Setting the `kubevirt.io/pause-guest-agent-probes` annotation on a `VirtualMachineInstance` (VMI) resource causes `virt-launcher` to return immediate success for `GuestAgentPing` probes without contacting the QEMU guest agent.

This is a manual, temporary measure. You must set the annotation yourself before maintenance and remove it yourself when maintenance is complete. The annotation is not set or removed automatically. If the `GuestAgentPing` probe is no longer needed, update the VM spec to remove the probe instead of relying on the annotation.

Consider pausing probes in the following scenarios:

- Guest OS updates that require one or more reboots, such as Windows updates

- Any planned maintenance where the guest agent will be temporarily unavailable

<div class="important">

- This annotation only affects `GuestAgentPing` probes. HTTP, TCP, and exec probes are not affected.

- The annotation takes effect within seconds on the next `virt-launcher` sync cycle.

- You must manually remove the annotation after maintenance to resume normal probe behavior. Probes remain paused indefinitely while the annotation is set.

- If you no longer require the `GuestAgentPing` probe, remove it from the VM spec rather than keeping the annotation set permanently.

</div>

## Pausing and resuming guest agent ping probes

You can temporarily pause `GuestAgentPing` probes on a virtual machine instance (VMI) by adding an annotation. This prevents the kubelet from restarting the pod during maintenance operations when the guest agent is temporarily unavailable.

- A running VMI with a `GuestAgentPing` liveness / readiness probe configured.

- You have installed the OpenShift CLI (`oc`).

1.  Pause probes by annotating the VMI:

    ``` terminal
    $ oc annotate vmi <vmi_name> kubevirt.io/pause-guest-agent-probes=true
    ```

2.  Verify that the annotation is set:

    ``` terminal
    $ oc get vmi <vmi_name> -o jsonpath='{.metadata.annotations.kubevirt\.io/pause-guest-agent-probes}'
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    true
    ```

3.  Optional: Verify that `virt-launcher` has picked up the annotation by checking its logs:

    ``` terminal
    $ oc logs -n <namespace> virt-launcher-<vmi_name>-<id> -c compute | grep "probe pause state"
    ```

4.  Perform your maintenance operations, such as guest OS updates.

5.  Resume probes by removing the annotation:

    ``` terminal
    $ oc annotate vmi <vmi_name> kubevirt.io/pause-guest-agent-probes-
    ```

# Additional resources

- [Monitoring application health by using health checks](../../applications/application-health.xml#application-health)
