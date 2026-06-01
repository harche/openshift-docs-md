You can troubleshoot and restore a two-node OpenShift Container Platform cluster with fencing (TNF) after a disruption event. Manually recover services when automated recovery is unavailable, replace degraded control plane nodes, and use the `fencing_validator` script to verify cluster health.

# Manually recovering from a disruption event when automated recovery is unavailable

You might need to perform manual recovery steps if a disruption event prevents fencing from functioning correctly. In this case, you can run commands directly on the control plane nodes to recover the cluster. There are four main recovery scenarios, which should be attempted in the following order:

1.  Update fencing secrets: Refresh the Baseboard Management Console (BMC) credentials if they are incorrect or outdated.

2.  Recover from a single-node failure: Restore functionality when only one control plane node is down.

3.  Recover from a complete node failure: Restore functionality when both control plane nodes are down.

4.  Replace a control plane node that cannot be recovered: Replace the node to restore cluster functionality.

- You have administrative access to the control plane nodes.

- You can connect to the nodes by using SSH.

<div class="note">

Do an etcd backup before proceeding to ensure that you can restore the cluster if any issues occur.

</div>

1.  Update the fencing secrets:

    1.  If the Cluster API is unavilable, update fencing secret by running the following command on one of the cluster nodes:

        ``` terminal
        $ sudo pcs stonith update <node_name>_redfish username=<user_name> password=<password>
        ```

        After the Cluster API recovers, or the Cluster API is already available, update fencing secret in the cluster to ensure it stays in sync, as described in the following step.

    2.  Edit the username and password for the existing fencing secret for the control plane node by running the following commads:

        ``` terminal
        $ oc project openshift-etcd
        ```

        ``` terminal
        $ oc edit secret <node_name>-fencing
        ```

        If the cluster recovers after updating the fencing secrets, no further action is required. If the issue persists, proceed to the next step.

2.  Recover from a single-node failure:

    1.  Gather initial diagnostics by running the following command:

        ``` terminal
        $ sudo pcs status --full
        ```

        This command provides a detailed view of the current cluster and resource states. You can use the output to identify issues with fencing or etcd startup.

    2.  Run the following additional diagnostic commands, if necessary:

        Reset the resources on your cluster and instruct Pacemaker to attempt to start them fresh by running the following command:

        ``` terminal
        $ sudo pcs resource cleanup
        ```

        Review all Pacemaker activity on the node by running the following command:

        ``` terminal
        $ sudo journalctl -u pacemaker
        ```

        Diagnose etcd resource startup issues by running the following command:

        ``` terminal
        $ sudo journalctl -u pacemaker | grep podman-etcd
        ```

    3.  View the fencing configuration for the node by running the following command:

        ``` terminal
        $ sudo pcs stonith config <node_name>_redfish
        ```

        If fencing is required but is not functioning, ensure that the Redfish fencing endpoint is accessible and verify that the credentials are correct.

    4.  If etcd is not starting despite fencing being operational, restore etcd from a backup by running the following commands:

        ``` terminal
        $ sudo cp -r /var/lib/etcd-backup/* /var/lib/etcd/
        ```

        ``` terminal
        $ sudo chown -R etcd:etcd /var/lib/etcd
        ```

        If the recovery is successful, no further action is required. If the issue persists, proceed to the next step.

3.  Recover from a complete node failure:

    1.  Power on both control plane nodes.

        Pacemaker starts automatically and begins the recovery operation when it detects both nodes are online. If the recovery does not start as expected, use the diagnostic commands described in the previous step to investigate the issue.

    2.  Reset the resources on your cluster and instruct Pacemaker to attempt to start them fresh by running the following command:

        ``` terminal
        $ sudo pcs resource cleanup
        ```

    3.  Check resource start order by running the following command:

        ``` terminal
        $ sudo pcs status --full
        ```

    4.  Inspect the pacemaker service journal if kubelet fails by running the following commands:

        ``` terminal
        $ sudo journalctl -u pacemaker
        ```

        ``` terminal
        $ sudo journalctl -u kubelet
        ```

    5.  Handle out-of-sync etcd.

        If one node has a more up-to-date etcd, Pacemaker attempts to fence the lagging node and start it as a learner. If this process stalls, verify the Redfish fencing endpoint and credentials by running the following command:

        ``` terminal
        $ sudo pcs stonith config
        ```

        If the recovery is successful, no further action is required. If the issue persists, perform manual recovery as described in the next step.

4.  If you need to manually recover from an event when one of the nodes is not recoverable, follow the procedure in "Replacing control plane nodes in a two-node OpenShift cluster".

    When a cluster loses a single node, it enters the degraded mode. In this state, Pacemaker automatically unblocks quorum and allows the cluster to temporarily operate on the remaining node.

    If both nodes fail, you must restart both nodes to reestablish quorum so that Pacemaker can resume normal cluster operations.

    If only one of the two nodes can be restarted, follow the node replacement procedure to manually reestablish quorum on the surviving node.

    If manual recovery is still required and it fails, collect a must-gather and SOS report, and file a bug.

<div class="formalpara-title">

**Verification**

</div>

For information about verifying that both control plane nodes and etcd are operating correctly, see "Verifying etcd health in a two-node OpenShift cluster with fencing".

- [Restoring etcd from a backup](../../../backup_and_restore/control_plane_backup_and_restore/backing-up-etcd.xml#backup-etcd-restoring_backing-up-etcd).

- [Verifying etcd health in a two-node OpenShift cluster with fencing](../installing_tnf/install-post-tnf.xml#installation-verifying-etcd-health_install-post-tnf)

# Replacing control plane nodes in a two-node OpenShift cluster with fencing

You can replace a failed control plane node in a two-node OpenShift cluster. The replacement node must use the same host name and IP address as the failed node.

- You have a functioning survivor control plane node.

- You have verified that either the machine is not running or the node is not ready.

- You have access to the cluster as a user with the `cluster-admin` role.

- You know the host name and IP address of the failed node.

<div class="note">

Do an etcd backup before proceeding to ensure that you can restore the cluster if any issues occur.

</div>

1.  Check the quorum state by running the following command:

    ``` terminal
    $ sudo pcs quorum status
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` terminal
    Quorum information
    ------------------
    Date:             Fri Oct  3 14:15:31 2025
    Quorum provider:  corosync_votequorum
    Nodes:            2
    Node ID:          1
    Ring ID:          1.16
    Quorate:          Yes

    Votequorum information
    ----------------------
    Expected votes:   2
    Highest expected: 2
    Total votes:      2
    Quorum:           1
    Flags:            2Node Quorate WaitForAll

    Membership information
    ----------------------
        Nodeid      Votes    Qdevice Name
             1          1         NR master-0 (local)
             2          1         NR master-1
    ```

    1.  If quorum is lost and one control plane node is still running, restore quorum manually on the survivor node by running the following command:

        ``` terminal
        $ sudo pcs quorum unblock
        ```

    2.  If only one node failed, verify that etcd is running on the survivor node by running the following command:

        ``` terminal
        $ sudo pcs resource status etcd
        ```

    3.  If etcd is not running, restart etcd by running the following command:

        ``` terminal
        $ sudo pcs resource cleanup etcd
        ```

        If etcd still does not start, force it manually on the survivor node, skipping fencing:

        <div class="important">

        Before running this commands, ensure that the node being replaced is inaccessible. Otherwise, you risk etcd corruption.

        </div>

        ``` terminal
        $ sudo pcs resource debug-stop etcd
        ```

        ``` terminal
        $ sudo OCF_RESKEY_CRM_meta_notify_start_resource='etcd' pcs resource debug-start etcd
        ```

        After recovery, etcd must be running successfully on the survivor node.

2.  Delete etcd secrets for the failed node by running the following commands:

    ``` terminal
    $ oc project openshift-etcd
    ```

    ``` terminal
    $ oc delete secret etcd-peer-<node_name>
    ```

    ``` terminal
    $ oc delete secret etcd-serving-<node_name>
    ```

    ``` terminal
    $ oc delete secret etcd-serving-metrics-<node_name>
    ```

    <div class="note">

    To replace the failed node, you must delete its etcd secrets first. When etcd is running, it might take some time for the API server to respond to these commands.

    </div>

3.  Delete resources for the failed node:

    1.  If you have the `BareMetalHost` (BMH) objects, list them to identify the host you are replacing by running the following command:

        ``` terminal
        $ oc get bmh -n openshift-machine-api
        ```

    2.  Delete the BMH object for the failed node by running the following command:

        ``` terminal
        $ oc delete bmh/<bmh_name> -n openshift-machine-api
        ```

    3.  List the `Machine` objects to identify the object that maps to the node that you are replacing by running the following command:

        ``` terminal
        $ oc get machines.machine.openshift.io -n openshift-machine-api
        ```

    4.  Get the label with the machine hash value from the `Machine` object by running the following command:

        ``` terminal
        $ oc get machines.machine.openshift.io/<machine_name> -n openshift-machine-api \
          -o jsonpath='Machine hash label: {.metadata.labels.machine\.openshift\.io/cluster-api-cluster}{"\n"}'
        ```

        Replace `<machine_name>` with the name of a `Machine` object in your cluster. For example, `ostest-bfs7w-ctrlplane-0`.

        You need this label to provision a new `Machine` object.

    5.  Delete the `Machine` object for the failed node by running the following command:

        ``` terminal
        $ oc delete machines.machine.openshift.io/<machine_name>-<failed nodename> -n openshift-machine-api
        ```

        <div class="note">

        The node object is deleted automatically after deleting the `Machine` object.

        </div>

4.  Recreate the failed host by using the same name and IP address:

    <div class="important">

    You must perform this step only if you are using installer-provisioned infrastructure or the Machine API to create the original node. For information about replacing a failed bare-metal control plane node, see "Replacing an unhealthy etcd member on bare metal".

    </div>

    1.  Remove the BMH and `Machine` objects. The machine controller automatically deletes the node object.

    2.  Provision a new machine by using the following sample configuration:

        <div class="formalpara-title">

        **Example `Machine` object configuration**

        </div>

        ``` yaml
        apiVersion: machine.openshift.io/v1beta1
        kind: Machine
        metadata:
          annotations:
            metal3.io/BareMetalHost: openshift-machine-api/{bmh_name}
          finalizers:
          - machine.machine.openshift.io
          labels:
            machine.openshift.io/cluster-api-cluster: {machine_hash_label}
            machine.openshift.io/cluster-api-machine-role: master
            machine.openshift.io/cluster-api-machine-type: master
          name: {machine_name}
          namespace: openshift-machine-api
        spec:
          authoritativeAPI: MachineAPI
          metadata: {}
          providerSpec:
            value:
              apiVersion: baremetal.cluster.k8s.io/v1alpha1
              customDeploy:
                method: install_coreos
              hostSelector: {}
              image:
                checksum: ""
                url: ""
              kind: BareMetalMachineProviderSpec
              metadata:
                creationTimestamp: null
              userData:
                name: master-user-data-managed
        ```

        - `metadata.annotations.metal3.io/BareMetalHost`: Replace `{bmh_name}` with the name of the BMH object that is associated with the host that you are replacing.

        - `labels.machine.openshift.io/cluster-api-cluster`: Replace `{machine_hash_label}` with the label that you fetched from the machine you deleted.

        - `metadata.name`: Replace `{machine_name}` with the name of the machine you deleted.

    3.  Create the new BMH object and the secret to store the BMC credentials by running the following command:

        ``` terminal
        cat <<EOF | oc apply -f -
        apiVersion: v1
        kind: Secret
        metadata:
          name: <secret_name>
          namespace: openshift-machine-api
        data:
          password: <password>
          username: <username>
        type: Opaque
        ---
        apiVersion: metal3.io/v1alpha1
        kind: BareMetalHost
        metadata:
          name: {bmh_name}
          namespace: openshift-machine-api
        spec:
          automatedCleaningMode: disabled
          bmc:
            address: <redfish_url>/{uuid}
            credentialsName: <name>
            disableCertificateVerification: true
          bootMACAddress: {boot_mac_address}
          bootMode: UEFI
          externallyProvisioned: false
          online: true
          rootDeviceHints:
            deviceName: /dev/disk/by-id/scsi-<serial_number>
          userData:
            name: master-user-data-managed
            namespace: openshift-machine-api
        EOF
        ```

        - `metadata.name`: Specify the name of the secret.

        - `metadata.name`: Replace `{bmh_name}` with the name of the BMH object that you deleted.

        - `bmc.address`: Replace `{uuid}` with the UUID of the node that you created.

        - `bmc.credentialsName`: Replace `name` with the name of the secret that you created.

        - `bootMACAddress`: Specify the MAC address of the provisioning network interface. This is the MAC address the node uses to identify itself when communicating with Ironic during provisioning.

5.  Verify that the new node has reached the `Provisioned` state by running the following command:

    ``` terminal
    $ oc get bmh -o wide
    ```

    The value of the `STATUS` column in the output of this command must be `Provisioned`.

    <div class="note">

    The provisioning process can take 10 to 20 minutes to complete.

    </div>

6.  Verify that both control plane nodes are in the `Ready` state by running the following command:

    ``` terminal
    $ oc get nodes
    ```

    The value of the `STATUS` column in the output of this command must be `Ready` for both nodes.

7.  Apply the `detached` annotation to the BMH object to prevent the Machine API from managing it by running the following command:

    ``` terminal
    $ oc annotate bmh <bmh_name> -n openshift-machine-api baremetalhost.metal3.io/detached='' --overwrite
    ```

8.  Rejoin the replacement node to the pacemaker cluster by running the following command:

    <div class="note">

    Run the following command on the survivor control plane node, not the node being replaced.

    </div>

    ``` terminal
    $ sudo pcs cluster node remove <node_name>
    ```

    ``` terminal
    $ sudo pcs cluster node add <node_name> addr=<node_ip> --start --enable
    ```

9.  Delete stale jobs for the failed node by running the following command:

    ``` terminal
    $ oc project openshift-etcd
    ```

    ``` terminal
    $ oc delete job tnf-auth-job-<node_name>
    ```

    ``` terminal
    $ oc delete job tnf-after-setup-job-<node_name>
    ```

<div class="formalpara-title">

**Verification**

</div>

For information about verifying that both control plane nodes and etcd are operating correctly, see "Verifying etcd health in a two-node OpenShift cluster with fencing".

# Verifying etcd health in a two-node OpenShift cluster with fencing

After completing node recovery or maintenance procedures, verify that both control plane nodes and etcd are operating correctly.

- You have access to the cluster as a user with `cluster-admin` privileges.

- You can access at least one control plane node through SSH.

1.  Check the overall node status by running the following command:

    ``` terminal
    $ oc get nodes
    ```

    This command verifies that both control plane nodes are in the `Ready` state, indicating that they can receive workloads for scheduling.

2.  Verify the status of the `cluster-etcd-operator` by running the following command:

    ``` terminal
    $ oc describe co/etcd
    ```

    The `cluster-etcd-operator` manages and reports on the health of your etcd setup. Reviewing its status helps you identify any ongoing issues or degraded conditions.

3.  Review the etcd member list by running the following command:

    ``` terminal
    $ oc rsh -n openshift-etcd <etcd_pod> etcdctl member list -w table
    ```

    This command shows the current etcd members and their roles. Look for any nodes marked as `learner`, which indicates that they are in the process of becoming voting members.

4.  Review the Pacemaker resource status by running the following command on either control plane node:

    ``` terminal
    $ sudo pcs status --full
    ```

    This command provides a detailed overview of all resources managed by Pacemaker. You must ensure that the following conditions are met:

    - Both nodes are online.

    - The `kubelet` and `etcd` resources are running.

    - Fencing is correctly configured for both nodes.

# Fencing validator script overview

A two-node OpenShift Container Platform cluster with fencing (TNF) relies on the Shoot The Other Node In The Head (STONITH) mechanism to ensure data integrity during node failures. If the fencing subsystem is misconfigured, the cluster might fail to recover safely, resulting in data corruption or a split-brain scenario.

Before the introduction of this utility, administrators or support engineers had to manually verify several subsystems, including:

- Pacemaker status

- STONITH device configurations

- Daemon health

- etcd quorum

- Fencing secrets

The `fencing_validator` script automates these manual checks into a single command, providing clear pass or fail results and descriptive error messages to reduce troubleshooting time and human error.

The `fencing_validator` is a Bash-based diagnostic utility available on every control-plane node in a TNF OpenShift Container Platform cluster. As a health check tool for the fencing subsystem, it verifies that the STONITH stack is correctly configured and operational.

The script is located at `/usr/local/bin/fencing_validator` on both control-plane nodes. The script is automatically installed by the Machine Config Operator (MCO). There is no manual installation step required.

When you deploy a TNF cluster, the MCO renders a set of `MachineConfig` manifests specific to that topology. One of these manifests is `fencing-validator.yaml`, located in the MCO source at `templates/master/00-master/two-node-with-fencing/files/fencing-validator.yaml`. This `MachineConfig` writes the script to `/usr/local/bin/fencing_validator` with executable mode `0755` on every control-plane node. The script is available as soon as the node has finished applying its `MachineConfig`, that is, after initial deployment or after any MCO-driven reboot.

<div class="important">

The script is deployed on TNF clusters only. It does not appear on standard HA clusters, Single-node OpenShift, or Two-Node with Arbiter clusters.

</div>

You can use the script for the following:

- Post-deployment validation: Use the utility to verify that the TNF configuration is correct and fully functional after deployment.

- Troubleshooting: Identify the specific underlying issues when a TNF setup fails to operate as expected.

- Pre-upgrade validation: Confirm the health of the fencing stack to ensure the cluster is stable enough to proceed with a version upgrade.

- Support interactions: Execute the script and provide the output to support engineers to facilitate the rapid resolution of technical issues.

## Fencing validator script prerequisites

Use the `fencing_validator` script to verify your fencing configuration on a two-node OpenShift Container Platform cluster. This script, deployed automatically by the Machine Config Operator, ensures that power management interfaces are correctly configured to prevent data corruption during a node failure. To run it, ensure the `jq` utility is installed, and you have both Kubernetes API access (`oc`) and SSH access to the control-plane nodes.

You can see what the script would do without actually performing any validation for TNF by running the following command:

``` terminal
$ oc debug node/<node_name> --chroot /host /usr/local/bin/fencing_validator --dry-run
```

## Command-line options for fencing validator script

To quickly verify a high-availability configuration of your two-node OpenShift Container Platform cluster with fencing (TNF), you can review the available command-line options and environment variables for the `fencing_validator` script. This reference helps you customize your connection methods, set execution timeouts, and safely test node reboots to ensure your fencing mechanism is reliable before moving to production.

You can see different command-line options for the `fencing_ validator` script by running the following command:

``` terminal
$ oc debug node/<node_name> --chroot /host /usr/local/bin/fencing_validator --help
```

The following table details command-line options for the `oc debug node` command:

| Flag           | Description                                                                                                                                                                                                                                                                           |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--user`       | SSH username for remote node access. The default value is `core`. Optionally, you can use `SSH_USER` environment variable to set the value.                                                                                                                                           |
| `--ssh-key`    | Path to SSH private key. Optionally, you can use the `SSH_KEY` environment variable to set the value.                                                                                                                                                                                 |
| `--kubeconfig` | Path to kubeconfig file. Optionally, you can use the `KUBECONFIG` environment variable to set the value.                                                                                                                                                                              |
| `--transport`  | How the script connects to the other node. The possible values are `auto`, `ssh`, and `ocdebug`. The default value is `auto`. Optionally, you can use the `TRANSPORT` environment variable to set the value. For more information, see "Transport mode for fencing validator script". |
| `--timeout`    | Maximum wait time for recovery loops. Optionally, you can use the `TIMEOUT` environment variable to set the value. By default, it is 1200 seconds or 20 minutes.                                                                                                                      |
| `--hosts`      | Comma-separated pair of node hostnames or IP addresses.                                                                                                                                                                                                                               |
| `--host-a`     | Explicitly set the first node.                                                                                                                                                                                                                                                        |
| `--host-b`     | Explicitly set the second node.                                                                                                                                                                                                                                                       |
| `--disruptive` | Enable destructive fencing tests (reboots nodes). Optionally, you can use the `DISRUPTIVE` environment variable to set the value.                                                                                                                                                     |
| `--dry-run`    | Show what could be the result of the `fencing_validator` script without doing actual validations. Optionally, you can use the `DRY_RUN` environment variable to set the value.                                                                                                        |
| `-h`, `--help` | Show usage information.                                                                                                                                                                                                                                                               |

You can set all the flags by using the following environment variables:

- `IP_A / IP_B`: set host addresses directly

- `OC_BIN`: custom `oc` binary path

- `OC_REQ_TIMEOUT`: per-API-call timeout. The default value is 10 seconds.

- `CMD_EXEC_TIMEOUT_SECS`: per-command timeout. The default value is 60 seconds.

## Fencing validator script for non-disruptive checks

To ensure your two-node OpenShift Container Platform cluster with fencing (TNF) remains highly available without risking downtime, you can run the `fencing_validator` script in validation mode. This script performs a series of read-only health checks to verify cluster quorum, daemon health, and STONITH device status without disrupting active services.

The simplest way to run the script is from a debug session on either control plane node by running the following command:

``` terminal
$ oc debug node/<node_name> --chroot /host /usr/local/bin/fencing_validator
```

This command does not reboot or fence any nodes. These checks are read-only and safe to run at any time. They run the following non-disruptive checks and report the results:

1.  **OpenShift version check** - Confirms the cluster is running OpenShift Container Platform 4.20.0 or later.

2.  **Node count check** - Confirms exactly 2 control-plane nodes exist.

3.  **Transport connectivity** - Establishes a connection to both nodes (via SSH or `oc debug`).

4.  **STONITH device check** - Verifies that STONITH devices are present and enabled in Pacemaker.

5.  **Pacemaker status** - Confirms both nodes are reporting ONLINE in the Pacemaker cluster.

6.  **Daemon health** - Checks that `corosync`, `pacemaker`, and `pcsd` services are active on both nodes.

7.  **etcd quorum** - Verifies that etcd has 2 healthy voting members and the cluster has quorum.

8.  **Fencing secrets** - Confirms that the fencing credential secrets (used by STONITH to authenticate to the BMC/IPMI) exist and are correctly bound to each node.

    When all non-disruptive checks pass, the output resembles the following:

``` terminal
[INFO]
====
OpenShift version: 4.20.0 - OK [INFO]  Detected 2 control-plane nodes [INFO]  Transport: ssh [OK]    STONITH devices found and enabled [OK]    Both nodes ONLINE in Pacemaker [OK]    All daemons healthy on both nodes [OK]    etcd quorum healthy (2/2 voters) [OK]    Fencing secrets correctly bound [INFO]  All non-disruptive checks passed When something fails:
====
```

\+ When non-disruptive checks fail, the output resembles the following:

``` terminal
[INFO]
====
OpenShift version: 4.20.0 - OK [INFO]  Detected 2 control-plane nodes [INFO]  Transport: ssh [ERROR] No STONITH devices found - fencing is not configured
====
```

## Fencing validator script for disruptive checks

You can validate your cluster’s resilience and perform disruptive checks from a peer node by using the `fencing_validator` script. By executing these simulated failures, you can ensure your high-availability environment correctly isolates and recovers from errors.

You can trigger the Shoot The Other Node In The Head (STONITH) action for the failed node and cut off its access to shared resources and prevent data corruption by running the following command:

``` terminal
$ pcs stonith fence <node>
```

You can check whether a two-node OpenShift Container Platform cluster with fencing (TNF) setup actually works by running the following command:

``` terminal
$ oc debug node/<node_name> --chroot /host /usr/local/bin/fencing_validator --disruptive
```

<div class="warning">

The `--disruptive` flag fences each control plane node one at a time and verifies recovery. The `--disruptive` flag performs the STONITH fence operations such as power cycle or VM reset. It does not perform graceful shutdown, and causes temporary workload disruption.

</div>

The fencing validator script with `--disruptive` flag runs the following checks:

1.  **Fence Node A** - Triggers STONITH to reboot the first control-plane node.

2.  **Verify NotReady** - Waits for Kubernetes to report the node A as `NotReady`, which confirms the reboot happened.

3.  **Verify recovery** - Waits for the node A to come back to the `Ready` state, rejoin the Pacemaker cluster as `ONLINE`, and for etcd to regain quorum.

4.  **Post-recovery daemon check** - Re-checks all daemons are healthy after recovery.

5.  **Fence Node B** - Triggers STONITH to reboot the second node.

6.  . **Verify NotReady** - Waits for Kubernetes to report the node B as `NotReady`, which confirms the reboot happened.

7.  **Verify recovery** - Waits for the node B to come back to the `Ready` state, rejoin the Pacemaker cluster as `ONLINE`, and for etcd to regain quorum.

8.  **Post-recovery daemon check** - Re-checks all daemons are healthy after recovery.

## Exit codes for fencing-validator script

The `fencing_validator` script uses specific exit codes so automation and support tooling can programmatically determine what went wrong.

The following table lists the specific exit codes that the `fencing_validator` script returns, mapping each numerical value to its corresponding diagnostic state to assist with automated troubleshooting.

| Exit code | Description                                                              |
|-----------|--------------------------------------------------------------------------|
| 0         | All checks passed                                                        |
| 1         | Generic or unexpected failure                                            |
| 20        | STONITH devices are missing or not enabled                               |
| 21        | One or both nodes are not ONLINE in Pacemaker                            |
| 22        | One or more required daemons (corosync, pacemaker, pcsd) are not running |
| 23        | etcd does not have quorum or not all members are healthy                 |
| 26        | Fencing secrets are missing or do not match the expected nodes           |

## Transport mode for fencing validator script

The `fencing_validator` script connects to control-plane nodes to run validation commands. Use the `--transport` flag or the `TRANSPORT` environment variable to define the connection method.

The `--transport` flag supports the following options:

- `auto`: This is the default option. The script first attempts `SSH` to both nodes. If `SSH` succeeds, it uses `SSH` for the session. If `SSH` fails, it falls back to `oc debug`. If neither works on both nodes, the script exits with an error.

- `ssh`: This option uses `SSH` to connect as the user defined by `--user`. The `--user` value defaults to `core`.

  - Permissions: Requires password-less `sudo` access on all nodes.

  - Automation: The script runs in `BatchMode`, disables interactive prompts, and skips host-key checking.

  - Authentication: Use the `--ssh-key` flag to provide a specific SSH key for all connections.

- `oc debug`: Connects by running the following command against each node:

  ``` terminal
  $ oc debug node/<node> --chroot /host
  ```

You do not need SSH access. The `fencing_validator` script only requires a valid `KUBECONFIG` with `cluster-admin` privileges.

For non-disruptive checks, both transports behave identically. However, the transport mode is critical when using the `--disruptive` option. During these tests, the script dispatches the `fence` command asynchronously using `systemd-run` or no hup as a fallback. This fire-and-forget method ensures the command completes even if the `oc debug` session terminates when the node fences.
