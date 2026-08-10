You can restore your OpenShift Container Platform cluster after a disaster by choosing the recovery path for etcd quorum loss, expired certificates, or rollback to an earlier state. Choose the option that matches your failure type before you begin recovery.

<div class="important">

Disaster recovery requires you to have at least one healthy control plane host.

</div>

Quorum restoration
This solution handles situations where you have lost the majority of your control plane hosts, leading to etcd quorum loss and the cluster going offline. This solution does not require an etcd backup.

<div class="note">

If you have a majority of your control plane nodes still available and have an etcd quorum, you can replace a single unhealthy etcd member instead of performing quorum restoration.

</div>

Restoring to an earlier cluster state
This solution handles situations where you want to restore your cluster to an earlier state, for example, if an administrator deletes something critical. If you have taken an etcd backup, you can restore your cluster to an earlier state.

<div class="warning">

Restoring to an earlier cluster state is a destructive and destabilizing action to take on a running cluster. This procedure should only be used as a last resort.

Before you restore, understand the impact a state rollback can have on your cluster.

</div>

Recovering from expired control plane certificates
This solution handles situations where your control plane certificates have expired. For example, if you shut down your cluster before the first certificate rotation, which occurs 24 hours after installation, your certificates are not rotated and expire. You can follow this procedure to recover from expired control plane certificates.

# Testing restore procedures

You can test your cluster restore workflow by simulating etcd failure on nonrecovery nodes and restoring from backup. Use this test to confirm that your etcd backup and restore process works as expected.

<div class="warning">

You must have SSH access to the cluster. Without SSH access, you cannot disable etcd or manage the `kubelet` service on nonrecovery nodes.

</div>

- You have SSH access to control plane hosts.

- You have installed the OpenShift CLI (`oc`).

1.  Use SSH to connect to each of your nonrecovery nodes to disable etcd and the `kubelet` service:

    1.  Disable etcd by running the following command:

        ``` terminal
        $ sudo /usr/local/bin/disable-etcd.sh
        ```

    2.  Delete variable data for etcd by running the following command:

        ``` terminal
        $ sudo rm -rf /var/lib/etcd
        ```

    3.  Disable the `kubelet` service by running the following command:

        ``` terminal
        $ sudo systemctl disable kubelet.service
        ```

2.  Exit every SSH session.

3.  Ensure that your nonrecovery nodes are in a `NOT READY` state by running the following command:

    ``` terminal
    $ oc get nodes
    ```

4.  Restore your cluster to an earlier cluster state using an etcd backup. For more information, see "Restoring to an earlier cluster state".

5.  After you restore the cluster and the API responds, use SSH to connect to each nonrecovery node and enable the `kubelet` service by running the following command:

    ``` terminal
    $ sudo systemctl enable kubelet.service
    ```

6.  Exit every SSH session.

7.  Verify that your nodes return to the `READY` state by running the following command:

    ``` terminal
    $ oc get nodes
    ```

8.  Verify that etcd is available by running the following command:

    ``` terminal
    $ oc get pods -n openshift-etcd
    ```

- [Quorum restoration](../../../backup_and_restore/control_plane_backup_and_restore/disaster_recovery/quorum-restoration.xml#dr-quorum-restoration)

- [Replacing an unhealthy etcd member](../../../backup_and_restore/control_plane_backup_and_restore/replacing-unhealthy-etcd-member.xml#replacing-unhealthy-etcd-member)

- [Restoring to an earlier cluster state](../../../backup_and_restore/control_plane_backup_and_restore/disaster_recovery/scenario-2-restoring-cluster-state.xml#dr-restoring-cluster-state)

- [About restoring cluster state](../../../backup_and_restore/control_plane_backup_and_restore/disaster_recovery/scenario-2-restoring-cluster-state.xml#dr-scenario-2-restoring-cluster-state-about_dr-restoring-cluster-state)

- [Recovering from expired control plane certificates](../../../backup_and_restore/control_plane_backup_and_restore/disaster_recovery/scenario-3-expired-certs.xml#dr-recovering-expired-certs)
