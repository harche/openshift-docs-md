For a highly available, small-footprint container platform at your edge sites or resource-constrained environments, you can deploy a two-node OpenShift Container Platform cluster with fencing (TNF). This fencing mechanism protects your applications and data from `split-brain` scenarios by safely isolating a node if communication fails. To match your existing environment, you can deploy this cluster using automated, manual, or agent-based infrastructure methods.

Automated Infrastructure (installer-provisioned)
The cluster installation program controls all aspects of the deployment, including provisioning the underlying cloud or virtualization platforms, configuring network resources, and spinning up the nodes.

Manual Infrastructure (user-provisioned)
You provision and manage your own operating system images, networking, storage, and load balancers before starting the OpenShift deployment. This method offers maximum control over custom enterprise environments.

Agent-Based Infrastructure
You use a bootable ISO image containing an agent that automates the deployment on bare metal or pre-provisioned infrastructure. This combines the flexibility of manual setups with the ease of an automated workflow, making it ideal for disconnected environments.

<div class="important">

Configure node access during installation, for example, by including SSH keys in the `install-config.yaml` file. TNF clusters might require manual intervention in specific error scenarios that can only be resolved through direct node access.

</div>

# Sample install-config.yaml file for a two-node installer-provisioned infrastructure cluster with fencing

You can use the following `install-config.yaml` configuration file as a template for deploying a two-node OpenShift cluster with fencing (TNF) by using the installer-provisioned infrastructure method:

<div class="note">

Back up etcd before proceeding to ensure that you can restore the cluster if an issue occurs.

</div>

<div class="formalpara-title">

**Sample `install-config.yaml` configuration**

</div>

``` yaml
apiVersion: v1
baseDomain: example.com
compute:
- name: worker
  replicas: 0
controlPlane:
  name: master
  replicas: 2
  fencing:
    credentials:
      - hostname: <control_0_hostname>
        address: https://<redfish-api-url>
        username: <username>
        password: <password>
        certificateVerification: Disabled
      - macAddress: <control_1_mac_address>
        address: https://<redfish-api-url>
        username: <username>
        password: <password>
        certificateVerification: Enabled
metadata:
  name: <cluster_name>
platform:
  baremetal:
    apiVIPs:
      - <api_ip>
    ingressVIPs:
      - <wildcard_ip>
    hosts:
      - name: <control_0_hostname>
        role: master
        bmc:
          address: <bmc_address>
          username: <bmc_username>
          password: <bmc_password>
        bootMACAddress: <boot_mac>
      - name: <control_1_hostname>
        role: master
        bmc:
          address: <bmc_address>
          username: <bmc_username>
          password: <bmc_password>
        bootMACAddress: <boot_mac>
pullSecret: '<pull_secret>'
sshKey: '<ssh_public_key>'
```

- `compute.replicas`: Set this field to `0` because a two-node OpenShift Container Platform cluster with fencing does not include compute nodes.

- `controlPlane.replicas`: Set this field to `2` for a two-node OpenShift Container Platform cluster with fencing deployment.

- `fencing.credentials.hostname`: The hostname of the control plane node. You must specify at least one of `hostname` or `macAddress` for each credential entry. If both are specified, `hostname` takes precedence for credential identification.

- `fencing.credentials.macAddress`: The MAC address of an operating system visible network interface on the control plane node. You can use this field as an alternative to `hostname` for identifying the node. This must be a MAC address from a non-loopback network interface on the host (for example, the boot NIC), not the BMC management interface MAC. MAC addresses are stable hardware identifiers that do not change if the hostname is modified after installation.

- `fencing.credentials.certificateVerification`: Set this field to `Disabled` if your Redfish URL uses self-signed certificates, which is common for internally-hosted endpoints. Set this field to `Enabled` for URLs with valid CA-signed certificates.

- `metadata.name`: The cluster name is used as a prefix for hostnames and DNS records.

- `platform.baremetal.apiVIPs` and `platform.baremetal.ingressVIPs` : Virtual IPs for the API and Ingress endpoints. Ensure they are reachable by all nodes and external clients.

- `pullSecret`: Contains credentials required to pull container images for the cluster components.

- `sshKey`: The SSH public key for accessing cluster nodes after installation.

# Sample install-config.yaml file for a two-node user-provisioned infrastructure cluster with fencing

You can use the following `install-config.yaml` configuration file as a template for deploying a two-node OpenShift Container Platform cluster with fencing by using the user-provisioned infrastructure method:

<div class="note">

Back up etcd before proceeding to ensure that you can restore the cluster if an issue occurs.

</div>

<div class="formalpara-title">

**Sample `install-config.yaml` configuration**

</div>

``` yaml
apiVersion: v1
baseDomain: example.com
compute:
- name: worker
  replicas: 0
controlPlane:
  name: master
  replicas: 2
  fencing:
    credentials:
      - hostname: <control_0_hostname>
        address: https://<redfish-api-url>
        username: <username>
        password: <password>
      - macAddress: <control_1_mac_address>
        address: https://<redfish-api-url>
        username: <username>
        password: <password>
metadata:
  name: <cluster_name>
platform:
  none: {}
pullSecret: '<pull_secret>'
sshKey: '<ssh_public_key>'
```

- `compute.replicas`: Set this field to `0` because a two-node OpenShift Container Platform cluster with fencing does not include worker nodes.

- `controlPlane.replicas`: Set this field to `2` for a two-node fencing deployment.

- `fencing.credentials.hostname`: The hostname of the control plane node. You must specify at least one of `hostname` or `macAddress` for each credential entry. If both are specified, `hostname` takes precedence for credential identification.

- `fencing.credentials.macAddress`: The MAC address of an OS-visible network interface on the control plane node. You can use this field as an alternative to `hostname` for identifying the node. This must be a MAC address from a non-loopback network interface on the host (for example, the boot NIC), not the BMC management interface MAC. MAC addresses are stable hardware identifiers that do not change if the hostname is modified after installation.

- `metadata.name`: Cluster name is used as a prefix for hostnames and DNS records.

- `platform.none` Set the platform to `none` for user-provisioned infrastructure deployments. Bare-metal hosts are pre-provisioned outside of the installation program.

- `pullSecret`: Contains credentials required to pull container images for the cluster components.

- `sshKey`: The SSH public key for accessing cluster nodes after installation.

# Sample install-config.yaml file for a two-node cluster with fencing for Agent-based Installer

You can use the following `install-config.yaml` configuration file as a template for deploying a two-node OpenShift Container Platform cluster with fencing (TNF) by using the Agent-based Installer method.

See the following sample `install-config.yaml` configuration file for bare-metal:

``` yaml
apiVersion: v1
baseDomain: example.com
controlPlane:
  name: master
  replicas: 2
  fencing:
    credentials:
    - hostname: master-0
      address: redfish+https://<bmc_ip_0>:<bmc_port>/redfish/v1/Systems/<system_id_0>
      username: <bmc_username>
      password: <bmc_password>
      certificateVerification: Disabled
    - macAddress: <mac_address_1>
      address: redfish+https://<bmc_ip_1>:<bmc_port>/redfish/v1/Systems/<system_id_1>
      username: <bmc_username>
      password: <bmc_password>
      certificateVerification: Disabled
compute:
- name: worker
  replicas: 0
metadata:
  name: <cluster_name>
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  networkType: OVNKubernetes
  machineNetwork:
  - cidr: <machine_network_cidr>
  serviceNetwork:
  - 172.30.0.0/16
platform:
  baremetal:
    apiVIPs:
    - <api_vip>
    ingressVIPs:
    - <ingress_vip>
pullSecret: '<pull_secret>'
sshKey: '<ssh_public_key>'
```

- `platform.baremetal.apiVIPs` and `ingressVIPs`: Specifies virtual IPs for the API and Ingress endpoints. Required for bare-metal platform; not applicable for `none`.

For other bare metal specific fields, see "Installation configuration parameters for the Agent-based Installer".

The following sample `install-config.yaml` configuration file is for the attribute platform with value `none`.

You must provide DNS name resolution and load balancing infrastructure.

``` yaml
apiVersion: v1
baseDomain: example.com
controlPlane:
  name: master
  replicas: 2
  fencing:
    credentials:
    - hostname: master-0
      address: redfish+https://<bmc_ip_0>:<bmc_port>/redfish/v1/Systems/<system_id_0>
      username: <bmc_username>
      password: <bmc_password>
      certificateVerification: Disabled
    - macAddress: <mac_address_1>
      address: redfish+https://<bmc_ip_1>:<bmc_port>/redfish/v1/Systems/<system_id_1>
      username: <bmc_username>
      password: <bmc_password>
      certificateVerification: Disabled
compute:
- name: worker
  replicas: 0
metadata:
  name: <cluster_name>
networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  networkType: OVNKubernetes
  machineNetwork:
  - cidr: <machine_network_cidr>
  serviceNetwork:
  - 172.30.0.0/16
platform:
  none: {}
pullSecret: '<pull_secret>'
sshKey: '<ssh_public_key>'
```

- `controlPlane.replicas`: Must be `2` for a two-node OpenShift Container Platform cluster with fencing (TNF).

- `compute[0].replicas`: Must be `0`. A two-node OpenShift Container Platform cluster with fencing does not support compute nodes.

- `controlPlane.fencing.credentials`: Exactly 2 entries required, one per control plane node.

- `fencing.credentials[].hostname`: The hostname of the control plane node. You must specify at least one of `hostname` or `macAddress` for each credential entry. If both are specified, `hostname` takes precedence for credential identification. Whichever identifiers are provided must be unique across credentials.

- `fencing.credentials[].macAddress`: The MAC address of an OS-visible network interface on the control plane node. You can use this field as an alternative to `hostname` for identifying the node. This must be a MAC address from a non-loopback network interface on the host (for example, the boot NIC), not the BMC management interface MAC. For the Agent-based Installer, this value must match one of the corresponding `hosts[].interfaces[].macAddress` values in the `agent-config.yaml` file. MAC addresses are stable hardware identifiers that do not change if the hostname is modified after installation.

- `fencing.credentials[].address`: The Redfish BMC URL. Must use the `redfish+https://` scheme (for example, `redfish+[https://192.168.1.10:443/redfish/v1/Systems/1](https://192.168.1.10:443/redfish/v1/Systems/1))`. IPMI addresses are not supported. Vendor-specific Redfish schemes such as `idrac-redfish+https://` and `ilo5-redfish+https://` are also accepted.

- `fencing.credentials[].username`: BMC username for the node.

- `fencing.credentials[].password`: BMC password for the node.

- `fencing.credentials[].certificateVerification`: Optional. Set to Disabled if your BMC uses self-signed certificates (common for internally-hosted endpoints). Set to Enabled (default) for BMCs with valid CA-signed certificates.

# Sample agent-config.yaml file for a two-node cluster with fencing for Agent-based Installer

You can use the following `agent-config.yaml` configuration file as a template for deploying a two-node OpenShift Container Platform cluster with fencing (TNF) by using the Agent-based Installer method:

See the following sample `agent-config.yaml` file with minimal configuration:

``` yaml
apiVersion: v1beta1
metadata:
  name: <cluster_name>
rendezvousIP: <rendezvous_ip>
```

where:

`rendezvousIP`
Specifies the IP address of the node that acts as the rendezvous host during installation. This node runs the Assisted Service and coordinates the installation of both nodes.

See the following sample `agent-config.yaml` file with host configuration and static networking:

<div class="note">

If your fencing credentials in the `install-config.yaml` use `hostname` to identify nodes, the `hostname` values in the `agent-config.yaml` file must match the `hostname` values in the fencing credentials. If your fencing credentials use `macAddress` instead, the MAC address is matched against the host interfaces and hostname matching is not required.

</div>

<div class="caution">

To prevent installation failures, ensure every `macAddress` in your fencing credentials matches a `hosts[].interfaces[].macAddress` in your `agent-config.yaml` file. The installation program does not flag mismatches. Instead, the installation program creates incomplete host entries that break the installation.

</div>

``` yaml
apiVersion: v1beta1
metadata:
  name: <cluster_name>
rendezvousIP: <rendezvous_ip>
additionalNTPSources:
- 0.rhel.pool.ntp.org
- 1.rhel.pool.ntp.org
hosts:
- hostname: master-0
  role: master
  interfaces:
  - name: <nic_name>
    macAddress: <mac_address_0>
  networkConfig:
    interfaces:
    - name: <nic_name>
      type: ethernet
      state: up
      ipv4:
        enabled: true
        dhcp: false
        address:
        - ip: <master_0_ip>
          prefix-length: <prefix_length>
      ipv6:
        enabled: false
    dns-resolver:
      config:
        server:
        - <dns_server>
    routes:
      config:
      - destination: 0.0.0.0/0
        next-hop-address: <gateway>
        next-hop-interface: <nic_name>
        table-id: 254
- hostname: master-1
  role: master
  interfaces:
  - name: <nic_name>
    macAddress: <mac_address_1>
  networkConfig:
    interfaces:
    - name: <nic_name>
      type: ethernet
      state: up
      ipv4:
        enabled: true
        dhcp: false
        address:
        - ip: <master_1_ip>
          prefix-length: <prefix_length>
      ipv6:
        enabled: false
    dns-resolver:
      config:
        server:
        - <dns_server>
    routes:
      config:
      - destination: 0.0.0.0/0
        next-hop-address: <gateway>
        next-hop-interface: <nic_name>
        table-id: 254
```
