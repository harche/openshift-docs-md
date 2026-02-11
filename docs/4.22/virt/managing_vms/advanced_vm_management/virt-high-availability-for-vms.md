You can enable high availability for virtual machines (VMs) by manually deleting a failed node to trigger VM failover or by configuring remediating nodes.

<div class="formalpara-title">

**Manually deleting a failed node**

</div>

If a node fails and machine health checks are not deployed on your cluster, virtual machines with `runStrategy: Always` configured are not automatically relocated to healthy nodes. To trigger VM failover, you must manually delete the `Node` object.

See [Deleting a failed node to trigger virtual machine failover](../../../virt/nodes/virt-triggering-vm-failover-resolving-failed-node.xml#virt-triggering-vm-failover-resolving-failed-node).

<div class="formalpara-title">

**Configuring remediating nodes**

</div>

You can configure remediating nodes by installing the Self Node Remediation Operator or the Fence Agents Remediation Operator from the software catalog and enabling machine health checks or node remediation checks.

For more information on remediation, fencing, and maintaining nodes, see the [Workload Availability for Red Hat OpenShift](https://docs.redhat.com/en/documentation/workload_availability_for_red_hat_openshift/24.3) documentation.
