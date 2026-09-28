You can tune fencing parameters if your two-node OpenShift Container Platform cluster experiences unwanted fencing events because of the latency spikes, slow BMC responses, or other timing issues.

# Overview of tuning fencing parameters

You can tune fencing parameters in OpenShift Container Platform two-node clusters to address specific operational issues without affecting default settings. Tuning prevents spurious node fencing during normal operations, resolves timeout failures, and improves cluster stability under load. Use preset configurations for common scenarios or customize individual parameters to match your system environment needs.

Tune fencing parameters only when you observe specific problems in your cluster. Do not change parameters preemptively. Adjust only the parameter that addresses your observed symptom.

You might need to tune parameters in the following scenarios:

Spurious fencing during load spikes
Healthy nodes get fenced during `MachineConfig` rollouts, cluster upgrades, or heavy I/O operations. Use the `tolerant-detection` preset or increase the Corosync `token` value.

Slow or unreliable BMC
Fence operations time out or fail intermittently. Use the `slow-bmc` preset or increase the fence agent timeouts.

kubelet stuck after reboot
The kubelet start operation times out when waiting for NetworkManager, leaving the resource blocked. Increase the `KUBELET_OP_START_TIMEOUT` value.

etcd stop failures under load
The etcd service takes too long to shut down, which triggers fencing. Increase the `ETCD_OP_STOP_TIMEOUT` value.

The fencing parameter tuning script generates a `MachineConfig` resource that deploys a `systemd` service on both control plane nodes. This service runs `pcs` commands to apply your chosen parameter values to the Pacemaker and Corosync cluster configuration. Preset configurations override only the parameters relevant to your scenario and leave all other values at their defaults.

The `MachineConfig` resource deploys the following components on each control plane node:

`/etc/fencing-parameter-tuning/values.conf`
This configuration file stores your parameter values.

`/usr/local/bin/fencing-parameter-tuning.sh`
This script includes preset configurations for common scenarios and applies the values using `pcs` commands. Use a preset when your symptom matches a known category, or edit individual parameter values for fine-grained control.

`fencing-parameter-tuning.service`
This `systemd` service runs the `fencing-parameter-tuning.sh` script after Pacemaker starts on each boot.

The script runs on only one node whose hostname appears alphabetically-first because Pacemaker synchronizes configuration changes between nodes internally.

<div class="note">

The tuning values persist in the Pacemaker cluster configuration independently of the `MachineConfig` resource. Deleting the `MachineConfig` resource removes the files and service but does not revert the tuned values.

</div>

# Applying a fencing tuning preset

You can apply predefined fencing tuning configurations to resolve some common issues. Each preset adjusts only the parameters relevant to your specific scenario.

Some of the common issues are as follows:

`tolerant-detection`
Raise the Corosync token from `3000` ms to `5000` ms. Use this preset when nodes are fenced during `MachineConfig` rollouts, heavy I/O, or network reconfiguration such as the OVS bridge race on IPv6 reboots.

`slow-bmc`
Increases fence agent timeouts for BMC hardware where the default values are insufficient, for example HPE ProLiant with iLO. Sets `power_timeout=120`, `shell_timeout=15`, `login_timeout=15`, and `retry_on=3`.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have the `oc` CLI tool installed.

- Both control plane nodes are `Ready` and all Pacemaker resources are started.

1.  Create a file named `apply-fencing-tuning.sh` with the following content:

    ``` bash
    #!/bin/bash
    set -euo pipefail

    COROSYNC_TOKEN=3000
    KUBELET_OP_START_TIMEOUT=180s
    KUBELET_OP_STOP_TIMEOUT=100s
    KUBELET_OP_MONITOR_TIMEOUT=100s
    KUBELET_OP_MONITOR_INTERVAL=60s
    ETCD_OP_STOP_TIMEOUT=90s
    ETCD_OP_START_TIMEOUT=600s
    FENCE_POWER_TIMEOUT=25
    FENCE_SHELL_TIMEOUT=3
    FENCE_LOGIN_TIMEOUT=5
    FENCE_POWER_WAIT=0
    FENCE_RETRY_ON=1
    FENCE_DELAY=0

    apply_preset_tolerant_detection() { COROSYNC_TOKEN=5000; }
    apply_preset_slow_bmc() {
      FENCE_POWER_TIMEOUT=120; FENCE_SHELL_TIMEOUT=15
      FENCE_LOGIN_TIMEOUT=15; FENCE_RETRY_ON=3
    }
    print_presets() {
      cat <<'EOF'
    Available presets:
      tolerant-detection  Corosync token 3000ms -> 5000ms (load spike tolerance)
      slow-bmc            Fence agent timeouts for slow BMC hardware (e.g. HPE iLO)
    EOF
    }

    # === ARGUMENT HANDLING ===
    if [ "${1:-}" = "--preset" ]; then
      PRESET="${2:-}"
      if [ -z "$PRESET" ] || [ "$PRESET" = "list" ]; then
        print_presets; [ "$PRESET" = "list" ] && exit 0
        echo "ERROR: --preset requires a name." >&2; exit 1
      fi
      case "$PRESET" in
        tolerant-detection) apply_preset_tolerant_detection ;;
        slow-bmc) apply_preset_slow_bmc ;;
        *) echo "ERROR: unknown preset '$PRESET'." >&2; print_presets; exit 1 ;;
      esac
      echo "Using preset: $PRESET"
    elif [ "${1:-}" = "--revert" ]; then
      echo "Reverting to default values..."
      COROSYNC_TOKEN=3000; KUBELET_OP_START_TIMEOUT=180s
      KUBELET_OP_STOP_TIMEOUT=100s; KUBELET_OP_MONITOR_TIMEOUT=100s
      KUBELET_OP_MONITOR_INTERVAL=60s; ETCD_OP_STOP_TIMEOUT=90s
      ETCD_OP_START_TIMEOUT=600s; FENCE_POWER_TIMEOUT=25
      FENCE_SHELL_TIMEOUT=3; FENCE_LOGIN_TIMEOUT=5
      FENCE_POWER_WAIT=0; FENCE_RETRY_ON=1; FENCE_DELAY=0
    fi

    if [ "$COROSYNC_TOKEN" -lt 3000 ] || [ "$COROSYNC_TOKEN" -gt 10000 ]; then
      echo "ERROR: COROSYNC_TOKEN=$COROSYNC_TOKEN outside safe range (3000-10000ms)." >&2
      exit 1
    fi
    command -v oc >/dev/null 2>&1 || { echo "ERROR: oc not found in PATH." >&2; exit 1; }
    oc whoami >/dev/null 2>&1 || { echo "ERROR: not logged in. Run 'oc login' first." >&2; exit 1; }

    VALUES_CONF="COROSYNC_TOKEN=${COROSYNC_TOKEN}
    KUBELET_OP_START_TIMEOUT=${KUBELET_OP_START_TIMEOUT}
    KUBELET_OP_STOP_TIMEOUT=${KUBELET_OP_STOP_TIMEOUT}
    KUBELET_OP_MONITOR_TIMEOUT=${KUBELET_OP_MONITOR_TIMEOUT}
    KUBELET_OP_MONITOR_INTERVAL=${KUBELET_OP_MONITOR_INTERVAL}
    ETCD_OP_STOP_TIMEOUT=${ETCD_OP_STOP_TIMEOUT}
    ETCD_OP_START_TIMEOUT=${ETCD_OP_START_TIMEOUT}
    FENCE_POWER_TIMEOUT=${FENCE_POWER_TIMEOUT}
    FENCE_SHELL_TIMEOUT=${FENCE_SHELL_TIMEOUT}
    FENCE_LOGIN_TIMEOUT=${FENCE_LOGIN_TIMEOUT}
    FENCE_POWER_WAIT=${FENCE_POWER_WAIT}
    FENCE_RETRY_ON=${FENCE_RETRY_ON}
    FENCE_DELAY=${FENCE_DELAY}"

    TUNING_SCRIPT='#!/bin/bash
    set -euo pipefail
    source /etc/fencing-parameter-tuning/values.conf
    MY_HOST=$(hostname)
    PEER_HOST=$(pcs status nodes 2>/dev/null | grep " Online:" | tr '"'"' '"'"' '"'"'\n'"'"' | \
      grep -v "Online:\|^$" | grep -v "^${MY_HOST}$" | sort | head -1)
    if [ -n "$PEER_HOST" ] && [ "$MY_HOST" \> "$PEER_HOST" ]; then
      echo "Not the primary node, skipping."; exit 0
    fi
    pcs_retry() {
      for i in 1 2 3; do
        if "$@"; then return 0; fi; echo "Retry $i/3..."; sleep 5
      done; return 1
    }
    if [ "$COROSYNC_TOKEN" -lt 3000 ] || [ "$COROSYNC_TOKEN" -gt 10000 ]; then
      echo "ERROR: token out of range"; exit 1
    fi
    FENCE_TYPE=$(pcs stonith config | grep "class=stonith type=" | \
      awk -F"type=" "{print \$2}" | tr -d ")" | head -1)
    pcs_retry pcs cluster config update totem token="${COROSYNC_TOKEN}"
    pcs_retry pcs resource update kubelet op start \
      timeout="${KUBELET_OP_START_TIMEOUT}" start-delay=15s
    pcs_retry pcs resource update kubelet op stop \
      timeout="${KUBELET_OP_STOP_TIMEOUT}"
    pcs_retry pcs resource update kubelet op monitor \
      timeout="${KUBELET_OP_MONITOR_TIMEOUT}" interval="${KUBELET_OP_MONITOR_INTERVAL}"
    pcs_retry pcs resource update etcd op stop timeout="${ETCD_OP_STOP_TIMEOUT}"
    pcs_retry pcs resource update etcd op start timeout="${ETCD_OP_START_TIMEOUT}"
    for SID in $(pcs stonith config | grep "^Resource:" | awk "{print \$2}"); do
      if pcs stonith describe "$FENCE_TYPE" | grep -q "^  power_timeout"; then
        pcs_retry pcs stonith update "$SID" power_timeout="${FENCE_POWER_TIMEOUT}" \
          shell_timeout="${FENCE_SHELL_TIMEOUT}" login_timeout="${FENCE_LOGIN_TIMEOUT}" \
          power_wait="${FENCE_POWER_WAIT}" retry_on="${FENCE_RETRY_ON}" delay="${FENCE_DELAY}"
      fi
    done
    echo "Fencing parameter tuning applied successfully."'

    VALUES_B64=$(echo "$VALUES_CONF" | base64 | tr -d '\n')
    SCRIPT_B64=$(echo "$TUNING_SCRIPT" | base64 | tr -d '\n')

    cat <<MCEOF | oc apply -f -
    apiVersion: machineconfiguration.openshift.io/v1
    kind: MachineConfig
    metadata:
      name: 99-fencing-parameter-tuning
      labels:
        machineconfiguration.openshift.io/role: master
    spec:
      config:
        ignition:
          version: 3.5.0
        systemd:
          units:
            - name: fencing-parameter-tuning.service
              enabled: true
              contents: |
                [Unit]
                Description=Apply fencing parameter tuning for TNF clusters
                After=pacemaker.service
                Requires=pacemaker.service
                StartLimitIntervalSec=300
                StartLimitBurst=5
                [Service]
                Type=oneshot
                ExecStart=/usr/local/bin/fencing-parameter-tuning.sh
                RemainAfterExit=yes
                TimeoutStartSec=120
                Restart=on-failure
                RestartSec=30
                [Install]
                WantedBy=multi-user.target
        storage:
          files:
            - path: /etc/fencing-parameter-tuning/values.conf
              mode: 0644
              overwrite: true
              contents:
                source: "data:text/plain;charset=utf-8;base64,${VALUES_B64}"
            - path: /usr/local/bin/fencing-parameter-tuning.sh
              mode: 0755
              overwrite: true
              contents:
                source: "data:text/plain;charset=utf-8;base64,${SCRIPT_B64}"
    MCEOF

    echo "MachineConfig applied. MCO will roll out to both master nodes (~10-15 min)."
    echo "Monitor: oc get mcp master -w"
    if [ "${1:-}" = "--revert" ]; then
      echo "After rollout, remove: oc delete mc 99-fencing-parameter-tuning"
    fi
    ```

2.  Make the script executable by running the following command:

    ``` terminal
    $ chmod +x apply-fencing-tuning.sh
    ```

3.  List the available presets by running the following command:

    ``` terminal
    $ ./apply-fencing-tuning.sh --preset list
    ```

4.  Apply the preset that matches your scenario by running the following command:

    ``` terminal
    $ ./apply-fencing-tuning.sh --preset <preset_name>
    ```

    Replace `<preset_name>` with `tolerant-detection` or `slow-bmc`.

5.  Wait for the Machine Config Operator (MCO) to roll out the change to both control plane nodes. This process takes approximately 10-15 minutes and reboots each node sequentially.

    ``` terminal
    $ oc get mcp master -w
    ```

    Wait until `UPDATED` is `True` and `UPDATING` is `False`.

- Verify that both nodes are `Ready` by running the following command:

  ``` terminal
  $ oc get nodes
  ```

- If you applied the `tolerant-detection` preset, verify the Corosync token value by running the following command:

  ``` terminal
  $ oc debug node/<master-node> -- chroot /host pcs cluster config show | grep token
  ```

  The output shows `token: 5000`.

- If you applied the `slow-bmc` preset, verify the fence agent timeouts by running the following command:

  ``` terminal
  oc debug node/<master-node> -- chroot /host pcs stonith config \
    | grep -E 'Resource:|[[:space:]]+(power_timeout|shell_timeout|login_timeout|power_wait|retry_on|delay)='
  ```

  The output shows `power_timeout=120`, `shell_timeout=15`, `login_timeout=15`, and `retry_on=3`.

# Applying custom fencing tuning values

If your scenario does not match a preset, you can edit individual parameter values in the `apply-fencing-tuning.sh` script. Change only the parameters that address your observed symptom.

- You have access to the cluster as a user with the `cluster-admin` role.

- You have the `oc` CLI tool installed.

- Both control plane nodes are in the `Ready` state and all Pacemaker resources are started.

1.  Save the `apply-fencing-tuning.sh` script to a local file.

2.  Open the script in a text editor and modify the values in the `DEFAULT VALUES` section at the top of the script. For example, to increase the Corosync token to `6000` ms and the etcd stop timeout to `120` seconds:

    <div class="formalpara-title">

    **Example**

    </div>

    ``` bash
    COROSYNC_TOKEN=6000

    ETCD_OP_STOP_TIMEOUT=120s
    ```

    For valid ranges and fencing risk for each parameter, see "Fencing tuning parameter reference".

3.  Run the script by running the following command:

    ``` terminal
    $ ./apply-fencing-tuning.sh
    ```

4.  Wait for the Machine Config Operator (MCO) to roll out the change to both control plane nodes:

    ``` terminal
    $ oc get mcp master -w
    ```

    Wait until `UPDATED` is `True` and `UPDATING` is `False`.

<!-- -->

1.  Verify the Corosync token value by running the following command:

    ``` terminal
    $ oc debug node/<master-node> -- chroot /host pcs cluster config show | grep token
    ```

2.  Verify the resource agent timeouts for kubelet by running the following command:

    ``` terminal
    $ oc debug node/<master-node> -- chroot /host pcs resource config kubelet
    ```

3.  Verify the resource agent timeouts for etcd by running the following command:

    ``` terminal
    $ oc debug node/<master-node> -- chroot /host pcs resource config etcd
    ```

4.  Verify the fence agent timeouts by running the following command:

    ``` terminal
    $ oc debug node/<master-node> -- chroot /host pcs stonith config
    ```

5.  To change values after the initial application, edit the script with new values and run it again. The MCO detects the change and rolls out a new update.

# Reverting fencing tuning to defaults

You can restore fencing parameters to their default values when removing custom tuning from your two-node OpenShift Container Platform cluster. This ensures all changes are properly reverted before deletion.

<div class="important">

Do not run `oc delete mc 99-fencing-parameter-tuning` without reverting first. Deleting the `MachineConfig` resource removes the tuning service but does not undo the Pacemaker changes. The tuned values remain active in the cluster configuration.

</div>

- You have access to the cluster as a user with the `cluster-admin` role.

- You have the `oc` CLI tool installed.

- The fencing parameter tuning `MachineConfig` resource is currently applied.

1.  Run the `apply-fencing-tuning.sh` script with the `--revert` flag by running the following command:

    ``` terminal
    $ ./apply-fencing-tuning.sh --revert
    ```

    For more information about the content of the `apply-fencing-tuning.sh` script, see "Applying a fencing tuning preset".

2.  Wait for the Machine Config Operator (MCO) to roll out the default values to both control plane nodes by running the following command:

    ``` terminal
    $ oc get mcp master -w
    ```

    Wait until `UPDATED` is `True` and `UPDATING` is `False`.

3.  After the rollout completes, delete the `MachineConfig` resource by running the following command:

    ``` terminal
    $ oc delete mc 99-fencing-parameter-tuning
    ```

4.  Wait for the MCO to roll out the deletion:

    ``` terminal
    $ oc get mcp master -w
    ```

<!-- -->

1.  Verify that the Corosync token is back to the default value by running the following command:

    ``` terminal
    $ oc debug node/<master-node> -- chroot /host pcs cluster config show | grep token
    ```

    The output shows `token: 3000`.

2.  Verify that both nodes are in the `Ready` state by running the following command:

    ``` terminal
    $ oc get nodes
    ```

# Fencing tuning parameter reference

You can refer the fencing parameters that you can tune, their default values, and which settings pose the highest risk of triggering unnecessary node fencing.

| Parameter        | Default | Safe range    | Effect                                                                                                                                                                                                                      |
|------------------|---------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `COROSYNC_TOKEN` | 3000    | 3000-10000 ms | How long before a silent node is declared dead and fenced. Lower values provide faster detection but a higher risk of false positives. Higher values are more tolerant of load spikes but slower to detect actual failures. |

Corosync parameters

The token value and resource agent timeouts are independent. Changing the token does not require changing etcd or kubelet timeouts.

| Parameter                     | Default | Fencing risk                                                                 |
|-------------------------------|---------|------------------------------------------------------------------------------|
| `KUBELET_OP_START_TIMEOUT`    | 180s    | None. Start failure blocks the resource and requires `pcs resource cleanup`. |
| `KUBELET_OP_STOP_TIMEOUT`     | 100s    | **Direct.** Stop failure always triggers fencing.                            |
| `KUBELET_OP_MONITOR_TIMEOUT`  | 100s    | Indirect. Monitor failure triggers recovery, which runs stop then start.     |
| `KUBELET_OP_MONITOR_INTERVAL` | 60s     | None. Controls health check frequency.                                       |

Kubelet resource agent parameters

| Parameter               | Default | Fencing risk                                                                 |
|-------------------------|---------|------------------------------------------------------------------------------|
| `ETCD_OP_STOP_TIMEOUT`  | 90s     | **Direct.** Stop failure always triggers fencing.                            |
| `ETCD_OP_START_TIMEOUT` | 600s    | None. Start failure blocks the resource and requires `pcs resource cleanup`. |

Etcd resource agent parameters

<div class="note">

The fence agent parameter values depend on your BMC hardware. Test your fence agent response times before setting these values by running the following command:

``` terminal
$ fence_<type> -a <bmc_ip> -l <user> -p <pass> -o status
```

</div>

| Parameter             | Default | Description                                              |
|-----------------------|---------|----------------------------------------------------------|
| `FENCE_POWER_TIMEOUT` | 25      | Wait for BMC to confirm power state change after ON/OFF. |
| `FENCE_SHELL_TIMEOUT` | 3       | Wait for BMC to respond to a command.                    |
| `FENCE_LOGIN_TIMEOUT` | 5       | Wait for BMC login prompt after connecting.              |
| `FENCE_POWER_WAIT`    | 0       | Wait after toggling power before checking new state.     |
| `FENCE_RETRY_ON`      | 1       | Number of power-on retry attempts.                       |
| `FENCE_DELAY`         | 0       | Fixed wait before executing the fence action.            |

Fence agent parameters

<div class="important">

Do not modify `pcmk_delay_base`. This parameter is managed by the cluster etcd Operator with different values per node to control the fencing race. Changing it can cause both nodes to fence simultaneously.

</div>

You must tune the following parameters that can cause fencing:

- `COROSYNC_TOKEN`: Corosync heartbeat expiry triggers fencing.

- `KUBELET_OP_STOP_TIMEOUT`: Stop failure always triggers fencing.

- `ETCD_OP_STOP_TIMEOUT`: Stop failure triggers fencing with cascade risk on clone-wide operations.

- `Fence agent timeouts`: Slow or failed fencing blocks cluster recovery.

You can tune the following parameters only for stuck resources which cannot cause fencing:

- `KUBELET_OP_START_TIMEOUT`: Start failure blocks resource and requires `pcs resource cleanup`.

- `ETCD_OP_START_TIMEOUT`: Start failure blocks resource and requires `pcs resource cleanup`.

- `KUBELET_OP_MONITOR_TIMEOUT`: Monitor failure triggers recovery, which runs stop then start.

# Cluster etcd Operator overwrite matrix

You can observe which fencing parameters persist after the cluster etcd Operator reconciles, such as during credential changes or Operator restarts.

The cluster etcd Operator manages initial Pacemaker configuration. The following table shows which tuned parameters survive Operator reconciliation:

| Category                    | Parameters                                                                           | Safe from Operator? | Details                                                                                                                                                                                                                 |
|-----------------------------|--------------------------------------------------------------------------------------|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Corosync                    | `token`                                                                              | Yes                 | The Operator never sets Corosync totem values. Tuning survives job re-runs and node replacement.                                                                                                                        |
| Kubelet resource operations | `start`, `stop`, `monitor` timeouts                                                  | Yes                 | The Operator creates the kubelet resource once. Operation timeouts set by using `pcs resource update` are not overwritten by subsequent Operator runs.                                                                  |
| Etcd resource operations    | `start`, `stop` timeouts                                                             | Yes                 | Same behavior as kubelet. Created once and guarded by a presence check.                                                                                                                                                 |
| STONITH fence agent         | `power_timeout`, `shell_timeout`, `login_timeout`, `power_wait`, `retry_on`, `delay` | Yes                 | The `pcs stonith update` command only modifies specified attributes. The Operator does not set these values.                                                                                                            |
| STONITH `pcmk_delay_base`   |  —                                                                                   | **No**              | The Operator sets different values per node, for example `10s` and `1s`, to control the fencing race. A fencing credential change triggers the Operator to re-run and reset these values. Do not modify this parameter. |
