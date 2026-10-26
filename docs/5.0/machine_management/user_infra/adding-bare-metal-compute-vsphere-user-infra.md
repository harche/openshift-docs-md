You can expand an existing OpenShift Container Platform cluster on VMware vSphere by adding bare-metal compute machines or virtual machines (VMs) without vSphere integration.

This workflow applies to compute machines added after cluster installation, regardless of the original installation method. The existing cluster retains its vSphere platform configuration and control plane.

# Compute machines without vSphere integration

Provision physical or virtual compute machines manually and install Red Hat Enterprise Linux CoreOS (RHCOS) with your OpenShift Container Platform cluster’s worker configuration. These nodes join the cluster without vSphere integration.

The target cluster is the existing OpenShift Container Platform cluster on vSphere that the new compute machines join. Run the OpenShift CLI (`oc`) commands in this workflow against the target cluster.

For a virtual machine (VM), use a virtualization environment other than vSphere, such as OpenShift Virtualization. That environment supplies the processor, memory, virtual disks, and network interfaces. Create the VM in that environment, and then install RHCOS inside the VM by using the ISO procedure. The VM needs network access to the target cluster and its worker Ignition configuration.

For VMs hosted on vSphere, use the procedures for adding vSphere compute machines.

The ISO procedure uses `coreos-installer install` with `--platform=metal` for both physical machines and VMs. The `metal` value selects the Ignition platform for the new worker; the target cluster retains its vSphere platform configuration.

You must provision and replace the added machines manually. The Machine API, compute machine sets, and cluster autoscaler do not provision or replace these machines. The Machine Config Operator (MCO) manages node configuration and operating system updates through machine config pools (MCPs).

If the added workers require configuration changes that differ from the existing workers, use a custom MCP to target those changes. The custom pool must inherit the worker configuration.

The requirement to disable the native vSphere Container Storage Interface (CSI) driver applies to workload storage in the target cluster. Storage for a VM’s virtual disks is configured in its virtualization environment.

<div>

<div class="title">

Additional resources

</div>

- [Node configuration management with machine config pools](../../machine_configuration/index.xml#architecture-machine-config-pools_machine-config-overview)

- [Create a custom machine config pool for an existing node](../../machine_configuration/machine-config-custom-mcp.xml#machine-config-custom-mcp-existing_machine-config-creating-custom-mcp)

</div>

# Prerequisites for compute machines without vSphere integration

Before you add bare-metal compute machines or virtual machines (VMs) without vSphere integration to your OpenShift Container Platform cluster, prepare the machines, network, and storage.

- You have an existing OpenShift Container Platform cluster installed on vSphere.

- The new physical machines or VMs meet the minimum resource requirements for compute machines, including processor capacity, memory, disk capacity, and disk performance.

- You have console access to each machine and a persistent disk on which to install Red Hat Enterprise Linux CoreOS (RHCOS).

- For VMs, you have created the VMs and configured their virtual disks and network interfaces. You can attach an ISO image and control the boot order.

- You have configured persistent IP addresses and hostnames for the new machines by using Dynamic Host Configuration Protocol (DHCP) or static configuration. You have also configured forward and reverse DNS resolution.

- The new machines and existing cluster nodes can communicate in both directions by using their node IP addresses. For VMs, these are the guest IP addresses. The new machines can also access the API, Machine Config Server, and required image registries.

- For clusters that use virtual IP addresses (VIPs), the VIPs remain reachable if served from an added node. The network must deliver incoming traffic for a VIP to that node, including when the node is on another subnet.

- You have migrated all workloads that depend on vSphere volumes to an alternative storage solution. This includes any platform workloads that use those volumes.

- After migrating the workloads, you have disabled the native vSphere Container Storage Interface (CSI) driver by setting `spec.managementState` to `Removed` in the `csi.vsphere.vmware.com` `ClusterCSIDriver` object.

> [!WARNING]
> Disabling the native vSphere CSI driver affects every node in the target cluster, including the existing vSphere nodes. These nodes lose the ability to provision or attach vSphere volumes. The CSI Operator removes all vSphere storage classes, including `thin-csi`.
>
> Removing the driver does not delete existing persistent volumes (PVs) or persistent volume claims (PVCs), but new pods cannot use them after you remove the driver. Migrate workloads that depend on these volumes to an alternative storage solution before you disable the driver.

<div>

<div class="title">

Additional resources

</div>

- [Minimum resource requirements](../../installing/installing_bare_metal/upi/installing-bare-metal.xml#installation-minimum-resource-requirements_installing-bare-metal)

- [Networking requirements for user-provisioned infrastructure](../../installing/installing_bare_metal/upi/installing-bare-metal.xml#installation-network-user-infra_installing-bare-metal)

- [Consequences of disabling and enabling storage on vSphere](../../storage/container_storage_interface/persistent-storage-csi-vsphere.xml#persistent-storage-csi-vsphere-disable-storage-consequences_persistent-storage-csi-vsphere)

- [Disabling and enabling storage on vSphere](../../storage/container_storage_interface/persistent-storage-csi-vsphere.xml#persistent-storage-csi-vsphere-disable-storage-procedure_persistent-storage-csi-vsphere)

</div>

# Add a compute machine subnet

If new compute machines use an additional subnet, add it to the machine networks in your OpenShift Container Platform cluster’s infrastructure configuration before the machines join.

Apply this procedure to both bare-metal machines and virtual machines (VMs) without vSphere integration. If their subnet is already listed, continue to the ISO installation procedure.

Adding the subnet to the cluster configuration does not configure external routing or establish virtual IP address (VIP) reachability. Configure that connectivity before adding the machines.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the target cluster as a user with the `cluster-admin` role.

- You know the subnets in Classless Inter-Domain Routing (CIDR) notation that your network administrator assigned to the existing machines and the new machines.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Display the configured machine networks by running the following command:

    ``` terminal
    $ oc get infrastructure cluster -o jsonpath='{.spec.platformSpec.vsphere.machineNetworks}{"\n"}'
    ```

2.  Edit the `Infrastructure` object named `cluster` by running the following command:

    ``` terminal
    $ oc edit infrastructure cluster
    ```

3.  In `spec.platformSpec.vsphere.machineNetworks`, retain the existing entries and append the new subnet. If `machineNetworks` is absent, add the list with the existing and new machine subnets.

    The following excerpt shows the location of the list:

    ``` yaml
    spec:
      platformSpec:
        type: VSphere
        vsphere:
          machineNetworks:
          - <existing_machine_network_cidr>
          - <new_machine_network_cidr>
    ```

    where:

    `<existing_machine_network_cidr>`
    Specifies an existing machine subnet. Retain all existing entries.

    `<new_machine_network_cidr>`
    Specifies the subnet for the new machines, for example, `192.0.2.0/24`. Add each new subnet only once.

4.  Save your changes and exit the editor.

</div>

<div>

<div class="title">

Verification

</div>

- Verify that the list contains the existing networks and each new subnet by running the following command:

  ``` terminal
  $ oc get infrastructure cluster -o jsonpath='{.spec.platformSpec.vsphere.machineNetworks}{"\n"}'
  ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [vSphere networking requirements for installer-provisioned and user-provisioned infrastructure](../../installing/installing_vsphere/post-install-vsphere-zones-regions-configuration.xml#vsphere-enabling-multiple-layer2-network_post-install-vsphere-zones-regions-configuration)

- [Adding compute machines to vSphere manually](../../machine_management/user_infra/adding-vsphere-compute-user-infra.xml#adding-vsphere-compute-user-infra)

</div>

# Create compute machines from an ISO image

Install Red Hat Enterprise Linux CoreOS (RHCOS) on physical machines or virtual machines (VMs) by using an ISO image and the worker Ignition configuration from your OpenShift Container Platform cluster on vSphere. The machines join as workers without vSphere integration.

<div>

<div class="title">

Prerequisites

</div>

- You have prepared the machines, network, and storage for adding compute machines without vSphere integration.

- You have added any new machine subnets to the target cluster’s infrastructure configuration.

- You have a Hypertext Transfer Protocol (HTTP) server that the new machines can access to download the Ignition configuration.

- You have installed the OpenShift CLI (`oc`) and `jq` on your workstation.

- You are logged in to the target cluster as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

1.  From your workstation, obtain the ISO download URL from the target cluster by running the following command:

    ``` terminal
    $ oc -n openshift-machine-config-operator get configmap/coreos-bootimages -o jsonpath='{.data.stream}' | jq -r '.architectures["<architecture>"].artifacts.metal.formats.iso.disk.location'
    ```

    Replace `<architecture>` with the processor architecture of the new machines, for example, `x86_64`. The architecture must be supported by the target cluster.

2.  Download the ISO image from the returned URL.

3.  Extract the worker Ignition configuration from the target cluster by running the following command:

    ``` terminal
    $ oc extract -n openshift-machine-api secret/worker-user-data-managed --keys=userData --to=- > worker.ign
    ```

4.  Upload the `worker.ign` file to your HTTP server. Record its URL.

5.  Boot the new machine from the ISO image:

    - For a physical machine, use local installation media or remote ISO redirection.

    - For a VM, attach the ISO image to the VM’s virtual optical drive and configure the VM to boot from it.

6.  From the live installation console, configure networking if Dynamic Host Configuration Protocol (DHCP) does not provide the required settings. You can use `nmcli` or `nmtui` to configure a static address or other network settings.

7.  From the live installation console, verify that the machine can retrieve its Ignition configuration by running the following command:

    ``` terminal
    $ curl --fail http://<http_server>/worker.ign
    ```

    Replace `<http_server>` with the address of your HTTP server. Include the path to `worker.ign` if you placed it in a subdirectory. The command must return the Ignition configuration.

8.  Identify the destination disk by running the following command:

    ``` terminal
    $ lsblk
    ```

9.  Install RHCOS on that disk by running the following command:

    If you configured networking in the live environment, add `--copy-network` to the command to copy the connection profiles in `/etc/NetworkManager/system-connections` to the installed system. This option does not copy the system hostname. Use the documented hostname configuration for your network.

    ``` terminal
    $ sudo coreos-installer install <installation_disk> \
        --ignition-url=http://<http_server>/worker.ign \
        --insecure-ignition \
        --platform=metal
    ```

    where:

    `<installation_disk>`
    Specifies the disk on which to install RHCOS, for example, `/dev/sda` on a physical machine or `/dev/vda` on a VM. Installation overwrites the contents of this disk.

    `<http_server>`
    Specifies the HTTP server and any directory path used in the Ignition URL.

10. After installation completes, remove or detach the ISO media, or change the boot order so that the machine boots from the installed disk. Reboot the machine by running the following command:

    ``` terminal
    $ sudo reboot
    ```

11. Monitor the console as the machine boots from disk. It attempts to join the target cluster and generates certificate signing requests (CSRs).

</div>

<div>

<div class="title">

Verification

</div>

- From your workstation, verify that the new machine has generated CSRs in the target cluster by running the following command:

  ``` terminal
  $ oc get csr
  ```

  Continue by reviewing and approving the CSRs for the machines that you added.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Using advanced networking options for PXE and ISO installations](../../installing/installing_bare_metal/upi/installing-bare-metal.xml#installation-user-infra-machines-advanced_network_installing-bare-metal)

- [Setting the cluster node hostnames through DHCP](../../installing/installing_bare_metal/upi/installing-bare-metal.xml#installation-host-names-dhcp-user-infra_installing-bare-metal)

</div>

# Approve the certificate signing requests for your machines

To allow newly added machines to join your OpenShift Container Platform cluster, confirm that the cluster approves pending certificate signing requests (CSRs), or approve them yourself. Approve client requests first, then server requests.

<div>

<div class="title">

Prerequisites

</div>

- You added machines to your cluster.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Confirm that the cluster recognizes the machines:

    ``` terminal
    $ oc get nodes
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME      STATUS    ROLES   AGE  VERSION
    master-0  Ready     master  63m  v1.36.3
    master-1  Ready     master  63m  v1.36.3
    master-2  Ready     master  64m  v1.36.3
    ```

    </div>

    The output lists all of the machines that you created.

    > [!NOTE]
    > The preceding output might not include the compute nodes until you approve some CSRs.

2.  Review the pending CSRs and ensure that you see the client requests with the `Pending` or `Approved` status for each machine that you added to the cluster:

    ``` terminal
    $ oc get csr
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME        AGE     REQUESTOR                                                                   CONDITION
    csr-8b2br   15m     system:serviceaccount:openshift-machine-config-operator:node-bootstrapper   Pending
    csr-8vnps   15m     system:serviceaccount:openshift-machine-config-operator:node-bootstrapper   Pending
    ...
    ```

    </div>

    In this example, two machines are joining the cluster. You might see more approved CSRs in the list.

3.  If the CSRs were not approved, after all of the pending CSRs for the machines you added are in `Pending` status, approve the CSRs for your cluster machines:

    > [!NOTE]
    > You must approve your CSRs within an hour of adding the machines to the cluster. If you do not approve them within an hour, the certificates rotate, and more than two certificates are present for each node. You must approve all of these certificates. After you approve the client CSR, the kubelet creates a secondary CSR for the serving certificate, which requires manual approval. The `machine-approver` then automatically approves later serving certificate renewal requests if the kubelet requests a new certificate with the same parameters.

    > [!NOTE]
    > For clusters running on platforms that are not machine API enabled, such as bare metal and other user-provisioned infrastructure, you must implement a method of automatically approving the kubelet serving certificate requests (CSRs). If you do not approve a request, the `oc exec`, `oc rsh`, and `oc logs` commands cannot succeed, because the API server requires a serving certificate when it connects to the kubelet. Any operation that contacts the kubelet endpoint requires this certificate approval to be in place. The method must watch for new CSRs, confirm that the `node-bootstrapper` service account in the `system:node` or `system:admin` groups submitted the CSR, and confirm the identity of the node.

    - To approve them individually, run the following command for each valid CSR:

      ``` terminal
      $ oc adm certificate approve <csr_name>
      ```

      where:

      `<csr_name>`
      Specifies the name of a CSR from the list of current CSRs.

    - To approve all pending CSRs, run the following command:

      ``` terminal
      $ oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs --no-run-if-empty oc adm certificate approve
      ```

      > [!NOTE]
      > Some Operators might not become available until you approve some CSRs. Each node submits two CSRs, so you might need to run the command to approve CSRs many times.

4.  After you approve your client requests, review the server requests for each machine that you added to the cluster:

    ``` terminal
    $ oc get csr
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME        AGE     REQUESTOR                                                                   CONDITION
    csr-bfd72   5m26s   system:node:ip-10-0-50-126.us-east-2.compute.internal                       Pending
    csr-c57lv   5m26s   system:node:ip-10-0-95-157.us-east-2.compute.internal                       Pending
    ...
    ```

    </div>

5.  If the remaining CSRs are not approved, and are in the `Pending` status, approve the CSRs for your cluster machines:

    - To approve them individually, run the following command for each valid CSR:

      ``` terminal
      $ oc adm certificate approve <csr_name>
      ```

      where:

      `<csr_name>`
      Specifies the name of a CSR from the list of current CSRs.

    - To approve all pending CSRs, run the following command:

      ``` terminal
      $ oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve
      ```

6.  After you approve all client and server CSRs, the machines have the `Ready` status. Verify this by running the following command:

    ``` terminal
    $ oc get nodes
    ```

    <div class="formalpara">

    <div class="title">

    Example output

    </div>

    ``` terminal
    NAME      STATUS    ROLES   AGE  VERSION
    master-0  Ready     master  73m  v1.36.3
    master-1  Ready     master  73m  v1.36.3
    master-2  Ready     master  74m  v1.36.3
    worker-0  Ready     worker  11m  v1.36.3
    worker-1  Ready     worker  11m  v1.36.3
    ```

    </div>

    > [!NOTE]
    > You might need to wait a few minutes after approval of the server CSRs for the machines to reach the `Ready` status.

</div>

# Remove the cloud provider uninitialized taint from compute nodes

To schedule workloads on bare-metal compute nodes or virtual machines (VMs) without vSphere integration, remove the `node.cloudprovider.kubernetes.io/uninitialized` taint after the nodes join your OpenShift Container Platform cluster.

The vSphere Cloud Controller Manager (CCM) attempts to initialize each node by searching vCenter for a matching virtual machine. For nodes without vSphere integration, the CCM cannot find a match and cannot remove the taint automatically. A node can have the `Ready` status and still have this taint, which prevents workload scheduling.

> [!NOTE]
> The CCM logs error messages similar to `No VM found` for nodes without vSphere integration. These messages are expected for these nodes.

<div>

<div class="title">

Prerequisites

</div>

- The compute nodes have joined the target cluster and their certificate signing requests (CSRs) have been approved.

- You have installed the OpenShift CLI (`oc`).

- You are logged in to the target cluster as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

- Remove the `node.cloudprovider.kubernetes.io/uninitialized` taint from each compute node that you added without vSphere integration by running the following command:

  ``` terminal
  $ oc adm taint nodes <node_name> node.cloudprovider.kubernetes.io/uninitialized:NoSchedule-
  ```

  Replace `<node_name>` with the name of the compute node as shown in the output of `oc get nodes`.

</div>

<div>

<div class="title">

Verification

</div>

1.  Verify that the compute node has the `Ready` status and does not show `SchedulingDisabled` by running the following command:

    ``` terminal
    $ oc get node <node_name>
    ```

    Replace `<node_name>` with the name of the compute node as shown in the output of `oc get nodes`.

2.  Verify that `node.cloudprovider.kubernetes.io/uninitialized` does not appear in the node’s taints by running the following command:

    ``` terminal
    $ oc get node <node_name> -o jsonpath='{.spec.taints}{"\n"}'
    ```

3.  Verify that the machine config pool (MCP) containing the added node has `Updated=True`, `Updating=False`, and `Degraded=False` by running the following command:

    ``` terminal
    $ oc get machineconfigpools
    ```

4.  Obtain the value of the added node’s `kubernetes.io/hostname` label for a test pod by running the following command:

    ``` terminal
    $ oc get node <node_name> -o jsonpath='{.metadata.labels.kubernetes\.io/hostname}{"\n"}'
    ```

5.  Create a file named `compute-node-test.yaml` with the following content. Use an existing test project whose node selector permits scheduling on the added node.

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: compute-node-test
      namespace: <test_namespace>
    spec:
      nodeSelector:
        kubernetes.io/hostname: <node_hostname>
      restartPolicy: Never
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: test
        image: <test_image>
        command: ["/bin/sh", "-c", "sleep 3600"]
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
    ```

    where:

    `<test_namespace>`
    Specifies the existing test project.

    `<node_hostname>`
    Specifies the hostname label value returned by the preceding command.

    `<test_image>`
    Specifies a container image that supports the node’s architecture, runs as a non-root user, and contains `/bin/sh` and `sleep`. For example, use `registry.access.redhat.com/ubi9/ubi-minimal:latest` or a mirrored copy accessible to the cluster.

6.  Create the test pod by running the following command:

    ``` terminal
    $ oc apply -f compute-node-test.yaml
    ```

7.  Verify that the test pod has `STATUS` set to `Running`, `READY` set to `1/1`, and `NODE` set to the added node by running the following command:

    ``` terminal
    $ oc get pod compute-node-test -n <test_namespace> -o wide
    ```

    This command also displays the pod if it has not been assigned to a node. If the pod remains pending or fails to become ready, examine its status and events by running the following command:

    ``` terminal
    $ oc describe pod compute-node-test -n <test_namespace>
    ```

    Resolve any reported scheduling or image-pull errors before continuing. This test verifies pod scheduling and startup on the node.

8.  Delete the test pod by running the following command:

    ``` terminal
    $ oc delete pod compute-node-test -n <test_namespace>
    ```

    Repeat the node and workload checks for each added node.

9.  After the cluster finishes reconciling the new nodes, verify that the cluster Operators have `Available=True`, `Progressing=False`, and `Degraded=False` by running the following command:

    ``` terminal
    $ oc get clusteroperators
    ```

</div>

<div>

<div class="title">

Additional resources

</div>

- [Use node selectors to control pod placement](../../nodes/scheduling/nodes-scheduler-node-selectors.xml#nodes-scheduler-node-selectors-pod_nodes-scheduler-node-selectors)

</div>
