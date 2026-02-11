This topic provides recommended performance and scalability practices for control planes in OpenShift Container Platform.

# Recommended practices for scaling the cluster

The guidance in this section is only relevant for installations with cloud provider integration.

Apply the following best practices to scale the number of worker machines in your OpenShift Container Platform cluster. You scale the worker machines by increasing or decreasing the number of replicas that are defined in the worker machine set.

When scaling up the cluster to higher node counts:

- Spread nodes across all of the available zones for higher availability.

- Scale up by no more than 25 to 50 machines at once.

- Consider creating new compute machine sets in each available zone with alternative instance types of similar size to help mitigate any periodic provider capacity constraints. For example, on AWS, use m5.large and m5d.large.

> [!NOTE]
> Cloud providers might implement a quota for API services. Therefore, gradually scale the cluster.

The controller might not be able to create the machines if the replicas in the compute machine sets are set to higher numbers all at one time. The number of requests the cloud platform, which OpenShift Container Platform is deployed on top of, is able to handle impacts the process. The controller will start to query more while trying to create, check, and update the machines with the status. The cloud platform on which OpenShift Container Platform is deployed has API request limits; excessive queries might lead to machine creation failures due to cloud platform limitations.

Enable machine health checks when scaling to large node counts. In case of failures, the health checks monitor the condition and automatically repair unhealthy machines.

> [!NOTE]
> When scaling large and dense clusters to lower node counts, it might take large amounts of time because the process involves draining or evicting the objects running on the nodes being terminated in parallel. Also, the client might start to throttle the requests if there are too many objects to evict. The default client queries per second (QPS) and burst rates are currently set to `50` and `100` respectively. These values cannot be modified in OpenShift Container Platform.

# Control plane node sizing

The control plane node resource requirements depend on the number and type of nodes and objects in the cluster. The following control plane node size recommendations are based on the results of a control plane density focused testing, or *Cluster-density*. This test creates the following objects across a given number of namespaces:

- 1 image stream

- 1 build

- 5 deployments, with 2 pod replicas in a `sleep` state, mounting 4 secrets, 4 config maps, and 1 downward API volume each

- 5 services, each one pointing to the TCP/8080 and TCP/8443 ports of one of the previous deployments

- 1 route pointing to the first of the previous services

- 10 secrets containing 2048 random string characters

- 10 config maps containing 2048 random string characters

| Number of worker nodes | Cluster-density (namespaces) | CPU cores | Memory (GB) |
|----|----|----|----|
| 24 | 500 | 4 | 16 |
| 120 | 1000 | 8 | 32 |
| 252 | 4000 | 16, but 24 if using the OVN-Kubernetes network plug-in | 64, but 128 if using the OVN-Kubernetes network plug-in |
| 501, but untested with the OVN-Kubernetes network plug-in | 4000 | 16 | 96 |

The data from the table above is based on an OpenShift Container Platform running on top of AWS, using r5.4xlarge instances as control-plane nodes and m5.2xlarge instances as worker nodes.

On a large and dense cluster with three control plane nodes, the CPU and memory usage will spike up when one of the nodes is stopped, rebooted, or fails. The failures can be due to unexpected issues with power, network, underlying infrastructure, or intentional cases where the cluster is restarted after shutting it down to save costs. The remaining two control plane nodes must handle the load in order to be highly available, which leads to increase in the resource usage. This is also expected during upgrades because the control plane nodes are cordoned, drained, and rebooted serially to apply the operating system updates, as well as the control plane Operators update. To avoid cascading failures, keep the overall CPU and memory resource usage on the control plane nodes to at most 60% of all available capacity to handle the resource usage spikes. Increase the CPU and memory on the control plane nodes accordingly to avoid potential downtime due to lack of resources.

> [!IMPORTANT]
> The node sizing varies depending on the number of nodes and object counts in the cluster. It also depends on whether the objects are actively being created on the cluster. During object creation, the control plane is more active in terms of resource usage compared to when the objects are in the `Running` phase.

Operator Lifecycle Manager (OLM) runs on the control plane nodes and its memory footprint depends on the number of namespaces and user installed operators that OLM needs to manage on the cluster. Control plane nodes need to be sized accordingly to avoid OOM kills. Following data points are based on the results from cluster maximums testing.

| Number of namespaces | OLM memory at idle state (GB) | OLM memory with 5 user operators installed (GB) |
|----|----|----|
| 500 | 0.823 | 1.7 |
| 1000 | 1.2 | 2.5 |
| 1500 | 1.7 | 3.2 |
| 2000 | 2 | 4.4 |
| 3000 | 2.7 | 5.6 |
| 4000 | 3.8 | 7.6 |
| 5000 | 4.2 | 9.02 |
| 6000 | 5.8 | 11.3 |
| 7000 | 6.6 | 12.9 |
| 8000 | 6.9 | 14.8 |
| 9000 | 8 | 17.7 |
| 10,000 | 9.9 | 21.6 |

> [!IMPORTANT]
> You can modify the control plane node size in a running OpenShift Container Platform 4.17 cluster for the following configurations only:
>
> - Clusters installed with a user-provisioned installation method.
>
> - AWS clusters installed with an installer-provisioned infrastructure installation method.
>
> - Clusters that use a control plane machine set to manage control plane machines.
>
> For all other configurations, you must estimate your total node count and use the suggested control plane node size during installation.

> [!NOTE]
> In OpenShift Container Platform 4.17, half of a CPU core (500 millicore) is now reserved by the system by default compared to OpenShift Container Platform 3.11 and previous versions. The sizes are determined taking that into consideration.

## Selecting a larger Amazon Web Services instance type for control plane machines

If the control plane machines in an Amazon Web Services (AWS) cluster require more resources, you can select a larger AWS instance type for the control plane machines to use.

> [!NOTE]
> The procedure for clusters that use a control plane machine set is different from the procedure for clusters that do not use a control plane machine set.
>
> If you are uncertain about the state of the `ControlPlaneMachineSet` CR in your cluster, you can [verify the CR status](../../machine_management/control_plane_machine_management/cpmso-getting-started.xml#cpmso-checking-status_cpmso-getting-started).

### Changing the Amazon Web Services instance type by using a control plane machine set

You can change the Amazon Web Services (AWS) instance type that your control plane machines use by updating the specification in the control plane machine set custom resource (CR).

<div>

<div class="title">

Prerequisites

</div>

- Your AWS cluster uses a control plane machine set.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Edit your control plane machine set CR by running the following command:

    ``` terminal
    $ oc --namespace openshift-machine-api edit controlplanemachineset.machine.openshift.io cluster
    ```

2.  Edit the following line under the `providerSpec` field:

    ``` yaml
    providerSpec:
      value:
        ...
        instanceType: <compatible_aws_instance_type>
    ```

    - Specify a larger AWS instance type with the same base as the previous selection. For example, you can change `m6i.xlarge` to `m6i.2xlarge` or `m6i.4xlarge`.

3.  Save your changes.

    - For clusters that use the default `RollingUpdate` update strategy, the Operator automatically propagates the changes to your control plane configuration.

    - For clusters that are configured to use the `OnDelete` update strategy, you must replace your control plane machines manually.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Managing control plane machines with control plane machine sets](../../machine_management/control_plane_machine_management/cpmso-managing-machines.xml#cpmso-managing-machines)

</div>

### Changing the Amazon Web Services instance type by using the AWS console

You can change the Amazon Web Services (AWS) instance type that your control plane machines use by updating the instance type in the AWS console.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the AWS console with the permissions required to modify the EC2 Instance for your cluster.

- You have access to the OpenShift Container Platform cluster as a user with the `cluster-admin` role.

</div>

<div>

<div class="title">

Procedure

</div>

1.  Open the AWS console and fetch the instances for the control plane machines.

2.  Choose one control plane machine instance.

    1.  For the selected control plane machine, back up the etcd data by creating an etcd snapshot. For more information, see "Backing up etcd".

    2.  In the AWS console, stop the control plane machine instance.

    3.  Select the stopped instance, and click **Actions** → **Instance Settings** → **Change instance type**.

    4.  Change the instance to a larger type, ensuring that the type is the same base as the previous selection, and apply changes. For example, you can change `m6i.xlarge` to `m6i.2xlarge` or `m6i.4xlarge`.

    5.  Start the instance.

    6.  If your OpenShift Container Platform cluster has a corresponding `Machine` object for the instance, update the instance type of the object to match the instance type set in the AWS console.

3.  Repeat this process for each control plane machine.

</div>

<div>

<div class="title">

Additional resources

</div>

- [Backing up etcd](../../backup_and_restore/control_plane_backup_and_restore/backing-up-etcd.xml#backing-up-etcd)

- [AWS documentation about changing the instance type](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-resize.html)

</div>
