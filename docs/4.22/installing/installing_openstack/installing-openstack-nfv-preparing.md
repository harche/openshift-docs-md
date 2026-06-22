Before you install a OpenShift Container Platform cluster that uses single-root I/O virtualization (SR-IOV) or Open vSwitch with the Data Plane Development Kit (OVS-DPDK) on Red Hat OpenStack Platform (RHOSP) or Red Hat OpenStack Services on OpenShift (RHOSO), you must understand the requirements for each technology and then perform preparatory tasks.

# Requirements for clusters on RHOSP or RHOSO that use either SR-IOV or OVS-DPDK

If you use SR-IOV or OVS-DPDK with your deployment, you must meet the following requirements:

- OpenStack compute nodes must use a flavor that supports huge pages.

## Requirements for clusters on RHOSP or RHOSO that use SR-IOV

To use single-root I/O virtualization (SR-IOV) with your deployment, you must meet the following requirements:

- If you use Red Hat OpenStack Platform (RHOSP), [plan your RHOSP SR-IOV deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/plan-sriov-deploy_rhosp-nfv).

- If you use Red Hat OpenStack Services on OpenShift (RHOSO), [plan your RHOSO SR-IOV deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_a_network_functions_virtualization_environment/plan-sriov-deploy_rhoso-nfv) by referring to *Deploying a network functions virtualization environment*.

- OpenShift Container Platform must support the NICs that you use. For a list of supported NICs, see "About Single Root I/O Virtualization (SR-IOV) hardware networks" in the "Hardware networks" subsection of the "Networking" documentation.

- For each node that will have an attached SR-IOV NIC, your OpenStack cluster must have:

  - One instance from the quota

  - One port attached to the machines subnet

  - One port for each SR-IOV Virtual Function

  - A flavor with at least 16 GB memory, 4 vCPUs, and 25 GB storage space

- SR-IOV deployments often employ performance optimizations, such as dedicated or isolated CPUs. For maximum performance, configure your underlying OpenStack deployment to use these optimizations, and then run OpenShift Container Platform compute machines on the optimized infrastructure.

  - If you use RHOSP, see [Configuring CPUs on Compute nodes](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_the_compute_service_for_instance_creation/assembly_configuring-cpus-on-compute-nodes).

  - If you use RHOSO, see [NFV performance considerations](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html-single/deploying_a_network_functions_virtualization_environment/index#nfv-perf_rhoso-nfv) in *Deploying a network functions virtualization environment*.

## Requirements for clusters on RHOSP or RHOSO that use OVS-DPDK

To use Open vSwitch with the Data Plane Development Kit (OVS-DPDK) with your deployment, you must meet the following requirements:

- If you use Red Hat OpenStack Platform (RHOSP):

  - Plan your OVS-DPDK deployment by referring to [Planning your OVS-DPDK deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/plan-ovs-dpdk-deploy_rhosp-nfv) in *Configuring network functions virtualization*.

  - Configure your OVS-DPDK deployment according to [Configuring an OVS-DPDK deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/config-dpdk-deploy_rhosp-nfv) in *Configuring network functions virtualization*.

- If you use Red Hat OpenStack Services on OpenShift (RHOSO):

  - Plan your OVS-DPDK deployment by referring to [Planning an OVS-DPDK deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_a_network_functions_virtualization_environment/plan-ovs-dpdk-deploy_rhoso-nfv) in *Deploying a network functions virtualization environment*.

  - Configure your OVS-DPDK deployment according to [Creating the data plane for SR-IOV and DPDK environments](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_a_network_functions_virtualization_environment/assembly_create-data-plane-sriov-dpdk_rhoso-nfv) in *Deploying a network functions virtualization environment*.

# Preparing to install a cluster that uses SR-IOV

You must configure your OpenStack platform before you install a cluster that uses SR-IOV on it.

## Creating SR-IOV networks for compute machines

If your Red Hat OpenStack Platform (RHOSP) deployment supports [single root I/O virtualization (SR-IOV)](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html-single/network_functions_virtualization_planning_and_configuration_guide/index#assembly_sriov_parameters), you can provision SR-IOV networks that compute machines run on.

<div class="note">

The following instructions entail creating an external flat network and an external, VLAN-based network that can be attached to a compute machine. Depending on your RHOSP deployment, other network types might be required.

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

# Preparing to install a cluster that uses OVS-DPDK

You must configure your OpenStack platform before you install a cluster that uses OVS-DPDK on it.

- If you use Red Hat OpenStack Platform (RHOSP), create a flavor and deploy an instance for OVS-DPDK before you install a cluster on RHOSP.

- If you use Red Hat OpenStack Services on OpenShift (RHOSO), create a custom OVS-DPDK compute service before you install a cluster on RHOSO.

After you perform preinstallation tasks, install your cluster by following the most relevant OpenShift Container Platform on OpenStack installation instructions. Then, perform the tasks under "Next steps" on this page.

- [Creating a flavor and deploying an instance for OVS-DPDK](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_network_functions_virtualization/config-dpdk-deploy_rhosp-nfv#create-flavor-deploy-instance-ovsdpdk_cfgdpdk-nfv)

- [Creating a custom OVS-DPDK Compute service](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_a_network_functions_virtualization_environment/assembly_create-data-plane-sriov-dpdk_rhoso-nfv)

# Next steps

- For either type of deployment:

  - [Configure the Node Tuning Operator with huge pages support](../../scalability_and_performance/what-huge-pages-do-and-how-they-are-consumed-by-apps.xml#what-huge-pages-do_huge-pages).

- To complete SR-IOV configuration after you deploy your cluster:

  - [Install the SR-IOV Operator](../../networking/networking_operators/sr-iov-operator/installing-sriov-operator.xml#installing-sr-iov-operator_installing-sriov-operator).

  - [Configure your SR-IOV network device](../../networking/hardware_networks/configuring-sriov-device.xml#nw-sriov-networknodepolicy-object_configuring-sriov-device).

  - [Create SR-IOV compute machines](../../machine_management/creating_machinesets/creating-machineset-osp.xml#machineset-yaml-osp-sr-iov_creating-machineset-osp).

- Consult the following references after you deploy your cluster to improve its performance:

  - [A test pod template for clusters that use OVS-DPDK on OpenStack](../../networking/hardware_networks/using-dpdk-and-rdma.xml#nw-openstack-ovs-dpdk-testpmd-pod_using-dpdk-and-rdma).

  - [A test pod template for clusters that use SR-IOV on OpenStack](../../networking/hardware_networks/configuring-sriov-device.xml#nw-openstack-sr-iov-testpmd-pod_configuring-sriov-device).

  - [A performance profile template for clusters that use OVS-DPDK on OpenStack](../../scalability_and_performance/cnf-tuning-low-latency-nodes-with-perf-profile.xml#installation-openstack-ovs-dpdk-performance-profile_cnf-tuning-low-latency-nodes-with-perf-profile)
