Before installing an OpenShift Container Platform cluster that uses single-root I/O virtualization (SR-IOV) or Open vSwitch with the Data Plane Development Kit (OVS-DPDK) on Red Hat OpenStack Platform (RHOSP), review the requirements for each technology and complete all the preparatory tasks.

# Requirements for clusters on RHOSP that use either SR-IOV or OVS-DPDK

If you use SR-IOV or OVS-DPDK with your deployment, you must meet certain requirements.

Ensure that RHOSP compute nodes use a flavor that supports huge pages.

## Requirements for clusters on RHOSP that use SR-IOV

To use single-root I/O virtualization (SR-IOV) with your deployment, you must meet specific requirements.

The requirements are as follows:

- You can plan your Red Hat OpenStack Platform (RHOSP) SR-IOV deployment. See "Planning an SR-IOV deployment (Red Hat OpenStack Platform (RHOSP) documentation)".

- OpenShift Container Platform must support the NICs that you use. For a list of supported NICs, see "About Single Root I/O Virtualization (SR-IOV) hardware networks".

- For each node that will have an attached SR-IOV NIC, your RHOSP cluster must have:

  - One instance from the RHOSP quota

  - One port attached to the machines subnet

  - One port for each SR-IOV Virtual Function

  - A flavor with at least 16 GB memory, 4 vCPUs, and 25 GB storage space

- SR-IOV deployments often employ performance optimizations, such as dedicated or isolated CPUs. For maximum performance, configure your underlying RHOSP deployment to use these optimizations, and then run OpenShift Container Platform compute machines on the optimized infrastructure.

  - You can configure performant RHOSP compute nodes. See "Configuring the Compute Service for Instance Creation".

<!-- -->

- [Planning and Configuring the Network Functions Virtualization (NFV) Red Hat OpenStack Platform (RHOSP) Deployment](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.2/html-single/network_functions_virtualization_planning_and_configuration_guide/index#assembly_sriov_parameters)

- [Configuring the Compute Service for Instance Creation](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html-single/configuring_the_compute_service_for_instance_creation/configuring-compute-nodes-for-performance#configuring-compute-nodes-for-performance)

## Requirements for clusters on RHOSP that use OVS-DPDK

To use Open vSwitch with the Data Plane Development Kit (OVS-DPDK) with your deployment, you must meet specific requirements.

The requirements are as follows:

- Plan your OVS-DPDK deployment. For more information, see "Planning your OVS-DPDK deployment (Red Hat OpenStack Platform (RHOSP) documentation)".

- Configure your OVS-DPDK deployment. For more information, see "Configuring an OVS-DPDK deployment (Red Hat OpenStack Platform (RHOSP) documentation)".

<!-- -->

- [Planning your OVS-DPDK deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/plan-ovs-dpdk-deploy_rhosp-nfv)

- [Configuring an OVS-DPDK deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/config-dpdk-deploy_rhosp-nfv)

## Creating SR-IOV networks for compute machines

If your Red Hat OpenStack Platform (RHOSP) deployment supports single root I/O virtualization (SR-IOV), you can provision SR-IOV networks that compute machines run on.

You must configure your RHOSP platform before you install a cluster that uses SR-IOV on the platform.

<div class="note">

The procedure uses an example of creating an external flat network and an external, VLAN-based network that can be attached to a compute machine. Depending on your RHOSP deployment, other network types might be required.

</div>

- Your cluster supports SR-IOV.

  <div class="note">

  If you are unsure about what your cluster supports, review the OpenShift Container Platform SR-IOV hardware networks documentation.

  </div>

- You created radio and uplink provider networks as part of your RHOSP deployment. The names `radio` and `uplink` are used in all example commands to represent these networks.

1.  On a command line, create a radio RHOSP network:

    ``` terminal
    $ openstack network create radio --provider-physical-network radio --provider-network-type flat --external
    ```

2.  Create an uplink RHOSP network:

    ``` terminal
    $ openstack network create uplink --provider-physical-network uplink --provider-network-type vlan --external
    ```

3.  Create a subnet for the radio network:

    ``` terminal
    $ openstack subnet create --network radio --subnet-range <radio_network_subnet_range> radio
    ```

4.  Create a subnet for the uplink network:

    ``` terminal
    $ openstack subnet create --network uplink --subnet-range <uplink_network_subnet_range> uplink
    ```

- [Planning an SR-IOV deployment](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html-single/network_functions_virtualization_planning_and_configuration_guide/index#assembly_sriov_parameters)

# Preparing to install a cluster that uses OVS-DPDK

You must configure your RHOSP platform before you install a cluster that uses OVS-DPDK on it.

After you perform preinstallation tasks, install your cluster by following the most relevant OpenShift Container Platform on RHOSP installation instructions. You can then perform the tasks outlined in the additional resources section.

- Create a flavor and deploy an instance for OVS-DPDK before you install a cluster on RHOSP.

<!-- -->

- [Creating a flavor and deploying an instance for OVS-DPDK](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/config-dpdk-deploy_rhosp-nfv#create-flavor-deploy-instance-ovsdpdk_cfgdpdk-nfv)

# Next steps after completing preparatory tasks

After you completed preparatory configurations, you can complete additional tasks.

These additional tasks are listed as follows:

- [Configure the Node Tuning Operator with huge pages support](../../scalability_and_performance/what-huge-pages-do-and-how-they-are-consumed-by-apps.xml#what-huge-pages-do_huge-pages).

- After you deploy your cluster, you can [install the SR-IOV Network Operator](../../networking/networking_operators/sr-iov-operator/installing-sriov-operator.xml#installing-sr-iov-operator_installing-sriov-operator), [configure an SR-IOV network device](../../networking/hardware_networks/configuring-sriov-device.xml#nw-sriov-networknodepolicy-object_configuring-sriov-device), and [create a compute machine set on RHOSP](../../machine_management/creating_machinesets/creating-machineset-osp.xml#machineset-yaml-osp-sr-iov_creating-machineset-osp).

- After you deploy your cluster, you can improve the performance of your cluster by completing any of the following tasks:

  - Create a [test pod template for clusters that use OVS-DPDK on RHOSP](../../networking/hardware_networks/using-dpdk-and-rdma.xml#nw-openstack-ovs-dpdk-testpmd-pod_using-dpdk-and-rdma).

  - Create a [ test pod template for clusters that use SR-IOV on RHOSP](../../networking/hardware_networks/configuring-sriov-device.xml#nw-openstack-sr-iov-testpmd-pod_configuring-sriov-device).

  - Create a [performance profile template for clusters that use OVS-DPDK on RHOSP](../../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#installation-openstack-ovs-dpdk-performance-profile_cnf-tuning-low-latency-nodes-with-perf-profile).
