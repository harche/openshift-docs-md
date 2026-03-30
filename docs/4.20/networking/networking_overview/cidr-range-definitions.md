To ensure stable and accurate network routing in OpenShift Container Platform clusters that use OVN-Kubernetes, define non-overlapping Classless Inter-Domain Routing (CIDR) subnet ranges. Establishing unique ranges prevents IP address conflicts so that internal traffic reaches its intended destination without interference.

<div class="important">

For OpenShift Container Platform 4.17 and later versions, clusters use `169.254.0.0/17` for IPv4 and `fd69::/112` for IPv6 as the default masquerade subnet. You must avoid these ranges. For upgraded clusters, there is no change to the default masquerade subnet.

</div>

<div class="tip">

You can use the [Red Hat OpenShift Network Calculator](https://access.redhat.com/labs/ocpnc/) to decide your networking needs before setting CIDR range during cluster creation.

You must have a Red Hat account to use the calculator.

</div>

The following subnet types are mandatory for a cluster that uses OVN-Kubernetes:

- Join: Uses a join switch to connect gateway routers to distributed routers. A join switch reduces the number of IP addresses for a distributed router. For a cluster that uses the OVN-Kubernetes plugin, an IP address from a dedicated subnet is assigned to any logical port that attaches to the join switch.

- Masquerade: Prevents collisions for identical source and destination IP addresses that are sent from a node as hairpin traffic to the same node after a load balancer makes a routing decision.

- Transit: A transit switch is a type of distributed switch that spans across all nodes in the cluster. A transit switch routes traffic between different zones. For a cluster that uses the OVN-Kubernetes plugin, an IP address from a dedicated subnet is assigned to any logical port that attaches to the transit switch.

<div class="note">

You can change the join, masquerade, and transit CIDR ranges for your cluster as a postinstallation task.

</div>

OVN-Kubernetes, the default network provider in OpenShift Container Platform 4.14 and later versions, internally uses the following IP address subnet ranges:

- `V4JoinSubnet`: `100.64.0.0/16`

- `V6JoinSubnet`: `fd98::/64`

- `V4TransitSwitchSubnet`: `100.88.0.0/16`

- `V6TransitSwitchSubnet`: `fd97::/64`

- `defaultV4MasqueradeSubnet`: `169.254.0.0/17`

- `defaultV6MasqueradeSubnet`: `fd69::/112`

<div class="important">

The earlier list includes join, transit, and masquerade IPv4 and IPv6 address subnets. If your cluster uses OVN-Kubernetes, do not include any of these IP address subnet ranges in any other CIDR definitions in your cluster or infrastructure.

</div>

- [Configuring OVN-Kubernetes internal IP address subnets](../../networking/ovn_kubernetes_network_provider/configure-ovn-kubernetes-subnets.xml#configure-ovn-kubernetes-subnets)

# Machine CIDR

To establish the network scope for cluster nodes in OpenShift Container Platform, specify an IP address range in the Machine Classless Inter-Domain Routing (CIDR) parameter. Defining this range ensures that all machines within the environment have valid, routable addresses for internal cluster communication.

<div class="note">

You cannot change Machine CIDR ranges after you create your cluster.

</div>

The default is `10.0.0.0/16`. This range must not conflict with any connected networks.

- [Cluster Network Operator configuration](../../networking/networking_operators/cluster-network-operator.xml#nw-operator-cr_cluster-network-operator)

# Service CIDR

To allocate IP addresses for cluster services in OpenShift Container Platform, specify an IP address range in the Service Classless Inter-Domain Routing (CIDR) parameter. Defining this range ensures that internal services have a dedicated block of addresses for reliable communication without overlapping with node or pod networks.

The range must be large enough to accommodate your workload. The address block must not overlap with any external service accessed from within the cluster. The default is `172.30.0.0/16`.

# Pod CIDR

To allocate internal network addresses for cluster workloads in OpenShift Container Platform, specify an IP address range in the pod Classless Inter-Domain Routing (CIDR) field. Defining this range ensures that pods can communicate with each other reliably without overlapping with the node or service networks.

The pod CIDR is the same as the `clusterNetwork` CIDR and the cluster CIDR. The range must be large enough to accommodate your workload. The address block must not overlap with any external service accessed from within the cluster. The default is `10.128.0.0/14`. You can expand the range after cluster installation.

- [Cluster Network Operator configuration](../../networking/networking_operators/cluster-network-operator.xml#nw-operator-cr_cluster-network-operator)

- [Configuring the cluster network range](../../networking/configuring_network_settings/configuring-cluster-network-range.xml#configuring-cluster-network-range)

# Host prefix

To allocate a dedicated pool of IP addresses for pods on each node in OpenShift Container Platform, specify the subnet prefix length in the hostPrefix parameter. Defining an appropriate prefix ensures that every machine has sufficient unique addresses to support its scheduled workloads without exhausting the cluster’s network resources.

For example, if the host prefix is set to `/23`, each machine is assigned a `/23` subnet from the pod CIDR address range. The default is `/23`, allowing 510 cluster nodes and 510 pod IP addresses per node.

Consider another example where you set the `clusterNetwork.cidr` parameter to `10.128.0.0/16`, you define the complete address space for the cluster. This assigns a pool of 65,536 IP addresses to your cluster. If you then set the `hostPrefix` parameter to `/23`, you define a subnet slice to each node in the cluster, where the `/23` slice becomes a subnet of the `/16` subnet network. This assigns 512 IP addresses to each node, where 2 IP addresses get reserved for networking and broadcasting purposes. The following example calculation uses these IP address figures to determine the maximum number of nodes that you can create for your cluster:

``` text
65536 / 512 = 128
```

You can use the [Red Hat OpenShift Network Calculator](https://access.redhat.com/labs/ocpnc/) to calculate the maximum number of nodes for your cluster.

# CIDR ranges for hosted control planes

To successfully deploy hosted control planes on OpenShift Container Platform, define the network environment by using specific Classless Inter-Domain Routing (CIDR) subnet ranges. Establishing these nonoverlapping ranges ensures reliable communication between cluster components and prevents internal IP address conflicts.

The following Classless Inter-Domain Routing (CIDR) subnet ranges are the default settings for hosted control planes:

- `v4InternalSubnet`: 100.65.0.0/16 (OVN-Kubernetes)

- `clusterNetwork`: 10.132.0.0/14 (pod network)

- `serviceNetwork`: 172.31.0.0/16

By using one of the default subnet ranges, you can avoid CIDR overlap with the management cluster and avoid connectivity issues. However, you can use other CIDR subnet ranges if they do not overlap with the management cluster.
