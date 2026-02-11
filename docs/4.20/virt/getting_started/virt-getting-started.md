You can explore the features and functionalities of OpenShift Virtualization by installing and configuring a basic environment.

<div class="note">

Cluster configuration procedures require `cluster-admin` privileges.

</div>

# Tours and quick starts

You can start exploring OpenShift Virtualization by taking tours in the OpenShift Container Platform web console.

**Getting started tour**

This short guided tour introduces several key aspects of using OpenShift Virtualization. There are two ways to start the tour:

- On the **Welcome to OpenShift Virtualization** dialog, click **Start Tour**.

- Go to **Virtualization** → **Overview** → **Settings** → **User** → **Getting started resources** and click **Guided tour**.

**Quick starts**

Quick start tours are available for several OpenShift Virtualization features. To access quick starts, complete the following steps:

1.  Click the **Help** icon **?** in the menu bar on the header of the OpenShift Container Platform web console.

2.  Select **Quick Starts**.

You can filter the available tours by entering the keyword `virtual` in the **Filter** field.

# Planning and installing OpenShift Virtualization

Plan and install OpenShift Virtualization on an OpenShift Container Platform cluster:

- [Plan your bare metal cluster for OpenShift Virtualization](../../installing/installing_bare_metal/preparing-to-install-on-bare-metal.xml#virt-planning-bare-metal-cluster-for-ocp-virt_preparing-to-install-on-bare-metal).

- [Prepare your cluster for OpenShift Virtualization](../../virt/install/preparing-cluster-for-virt.xml#preparing-cluster-for-virt).

- [Install the OpenShift Virtualization Operator](../../virt/install/installing-virt.xml#virt-installing-virt-operator_installing-virt).

- [Install the `virtctl` command-line interface (CLI) tool](../../virt/getting_started/virt-using-the-cli-tools.xml#installing-virtctl_virt-using-the-cli-tools).

**Planning and installation resources**

- [About storage volumes for virtual machine disks](../../virt/install/preparing-cluster-for-virt.xml#virt-about-storage-volumes-for-vm-disks_preparing-cluster-for-virt).

- [Using a CSI-enabled storage provider](../../storage/container_storage_interface/persistent-storage-csi.xml#persistent-storage-csi).

- [Configuring local storage for virtual machines](../../virt/storage/virt-configuring-local-storage-with-hpp.xml#virt-configuring-local-storage-with-hpp).

- [Installing the Kubernetes NMState Operator](../../networking/networking_operators/k8s-nmstate-about-the-k8s-nmstate-operator.xml#installing-the-kubernetes-nmstate-operator-cli).

- [Specifying nodes for virtual machines](../../virt/managing_vms/advanced_vm_management/virt-specifying-nodes-for-vms.xml#virt-specifying-nodes-for-vms).

- [`Virtctl` commands](../../virt/getting_started/virt-using-the-cli-tools.xml#virtctl-commands_virt-using-the-cli-tools).

# Creating and managing virtual machines

Create a virtual machine (VM):

- [Create a VM from a Red Hat image](../../virt/creating_vms_advanced/creating_vms_advanced_web/virt-creating-vms-from-rh-images-overview.xml#virt-creating-vms-from-rh-images-overview).

  You can create a VM by using a Red Hat template or an [instance type](../../virt/creating_vm/virt-creating-vms-from-instance-types.xml#virt-creating-vms-from-instance-types).

- You can create a VM by [importing a custom image from a container registry or a web page](../../virt/creating_vms_advanced/creating_vms_advanced_web/virt-creating-vms-from-web-images.xml#virt-creating-vms-from-web-images), by [uploading an image from your local machine](../../virt/creating_vms_advanced/creating_vms_advanced_web/virt-creating-vms-uploading-images.xml#virt-creating-vms-uploading-images), or by [cloning a persistent volume claim (PVC)](../../virt/creating_vms_advanced/creating_vms_cli/virt-creating-vms-by-cloning-pvcs.xml#virt-creating-vms-by-cloning-pvcs).

Connect a VM to a secondary network:

- [Linux bridge network](../../virt/vm_networking/virt-connecting-vm-to-linux-bridge.xml#virt-connecting-vm-to-linux-bridge).

- [Open Virtual Network (OVN)-Kubernetes secondary network](../../virt/vm_networking/virt-connecting-vm-to-ovn-secondary-network.xml#virt-connecting-vm-to-ovn-secondary-network).

- [Single Root I/O Virtualization (SR-IOV) network](../../virt/vm_networking/virt-connecting-vm-to-sriov.xml#virt-connecting-vm-to-sriov).

  <div class="note">

  VMs are connected to the pod network by default.

  </div>

Connect to a VM:

- Connect to the [serial console](../../virt/managing_vms/virt-accessing-vm-consoles.xml#serial-console_virt-accessing-vm-consoles) or [VNC console](../../virt/managing_vms/virt-accessing-vm-consoles.xml#vnc-console_virt-accessing-vm-consoles) of a VM.

- [Connect to a VM by using SSH](../../virt/managing_vms/virt-accessing-vm-ssh.xml#virt-accessing-vm-ssh).

- [Connect to the desktop viewer for Windows VMs](../../virt/managing_vms/virt-accessing-vm-consoles.xml#desktop-viewer_virt-accessing-vm-consoles).

Manage a VM:

- [Manage a VM by using the web console](../../virt/managing_vms/virt-controlling-vm-states.xml#virt-controlling-vm-states).

- [Manage a VM by using the `virtctl` CLI tool](../../virt/getting_started/virt-using-the-cli-tools.xml#virtctl-commands_virt-using-the-cli-tools).

- [Export a VM](../../virt/managing_vms/virt-exporting-vms.xml#virt-accessing-exported-vm-manifests_virt-exporting-vms).

# Migrating to OpenShift Virtualization

To migrate virtual machines from an external provider such as VMware vSphere, Red Hat OpenStack Platform (RHOSP), Red Hat Virtualization, or another OpenShift Container Platform cluster, use the Migration Toolkit for Virtualization (MTV). You can also migrate Open Virtual Appliance (OVA) files created by VMware vSphere.

<div class="note">

Migration Toolkit for Virtualization is not part of OpenShift Virtualization and requires separate installation. For this reason, all links in this procedure lead outside of OpenShift Virtualization documentation.

</div>

- The Migration Toolkit for Virtualization Operator [is installed](https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/2.8/html/installing_and_using_the_migration_toolkit_for_virtualization/installing-the-operator_mtv#installing-the-operator_mtv).

<!-- -->

- [Migrate virtual machines from VMware vSphere](https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/2.8/html/installing_and_using_the_migration_toolkit_for_virtualization/migrating-vmware#adding-source-provider_vmware).

- [Migrate virtual machines from Red Hat OpenStack Platform (RHOSP)](https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/2.8/html/installing_and_using_the_migration_toolkit_for_virtualization/migrating-osp_ostack#adding-source-provider_ostack).

- [Migrate virtual machines from Red Hat Virtualization](https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/2.8/html/installing_and_using_the_migration_toolkit_for_virtualization/migrating-rhv_rhv#adding-source-provider_rhv).

- [Migrate virtual machines from OpenShift Virtualization](https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/2.8/html/installing_and_using_the_migration_toolkit_for_virtualization/migrating-virt_cnv#adding-source-provider_cnv).

- [Migrate virtual machines from OVA files created by VMware vSphere](https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/2.8/html/installing_and_using_the_migration_toolkit_for_virtualization/migrating-ova_ova#adding-source-provider_ova).

# Next steps

- [Review postinstallation configuration options](../../virt/post_installation_configuration/virt-post-install-config.xml#virt-post-install-config).

- [Configure storage options and automatic boot source updates](../../virt/storage/virt-storage-config-overview.xml#virt-storage-config-overview).

- [Learn about monitoring and health checks](../../virt/monitoring/virt-monitoring-overview.xml#virt-monitoring-overview).

- [Learn about live migration](../../virt/live_migration/virt-about-live-migration.xml#virt-about-live-migration).

- [Back up and restore VMs by using the OpenShift API for Data Protection (OADP)](../../backup_and_restore/application_backup_and_restore/installing/installing-oadp-kubevirt.xml#installing-oadp-kubevirt).

- [Tune and scale your cluster](https://access.redhat.com/articles/6994974).
