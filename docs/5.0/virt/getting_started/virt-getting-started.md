Explore OpenShift Virtualization by taking guided tours, installing the Operator, and configuring a basic environment. Learn how to migrate from your current platform, then learn more about how to deploy and manage virtual machines (VMs) by following the additional resources links.

<div class="note">

Cluster configuration procedures require `cluster-admin` privileges.

</div>

# Getting started tour

The **Getting started** tour introduces several key aspects of using OpenShift Virtualization. There are two ways to start the tour.

- You have access to the OpenShift Container Platform web console.

<!-- -->

- If you see the **Welcome to OpenShift Virtualization** dialog, click **Start Tour**.

- Otherwise, go to **Virtualization** → **Settings** → **User** → **Getting started resources** → **Guided tour**.

# Quick start tours

You can explore several OpenShift Virtualization capabilities by taking quick start tours in the web console.

- You have access to the OpenShift Container Platform web console.

1.  Click the **Help** icon **?** in the menu bar on the header of the OpenShift Container Platform web console.

2.  Select **Quick Starts**. You can filter the list of tours by entering the keyword `virtual` in the **Filter** field.

# Self-service Technical Supportability Review

You can use the self-service Technical Supportability Review (TSR) on the Red Hat Customer Portal to validate your cluster configuration against Red Hat common practices.

<div class="note">

The `must-gather` tool collects diagnostic information about your cluster, including resource definitions, service logs, and configuration data. For more information, see "Gathering data about your cluster" in the OpenShift Container Platform documentation.

</div>

The self-service TSR uses AI to evaluate your cluster’s `must-gather` data and provides a prioritized executive summary of recommendations. This serves as a starting point to help you identify and resolve potential issues before they impact your environment.

The TSR performs hundreds of checks across the OpenShift Container Platform platform, including OpenShift Virtualization. Coverage is continually expanding.

## When to use the self-service TSR tool

Integrating the self-service TSR into your regular operational workflow can be helpful in the following scenarios:

Routine benchmarking
Use the TSR quarterly to benchmark cluster health and plan for routine maintenance activities.

Pre-flight checks
Validate your cluster configuration before major structural changes, including upgrades, migrations, and expansions.

Critical event preparation
Confirm cluster stability ahead of high-traffic business events, such as seasonal peaks, or operational milestones, such as year-end shutdowns, business continuity drills, and compliance audits.

## How to access the TSR

To run a self-service review, upload your cluster’s `must-gather` data to the **Analyze** tab in the **Support** section of the Red Hat Customer Portal. For a direct link, see "Technical Supportability Review with AI tool" in the Additional resources section. The **Analyze** feature generates a prioritized executive summary that identifies your cluster’s top risks and recommends corrective actions. Review the recommendations and implement the suggested corrective actions to address the identified risks.

The self-service TSR provides a solid baseline for cluster health. If you need additional guidance or a more comprehensive review, contact your Red Hat account team to arrange an assisted review through a Technical Account Manager (TAM) or Red Hat consultant. An assisted review includes human analysis, deeper coverage, and access to checks that are updated more frequently than the self-service version.

- [Technical Supportability Review with AI tool](https://access.redhat.com/support/cases/#/analyze)

- [Red Hat Technical Supportability Review with AI: Proactive AI-Driven Cluster Assessments for OpenShift Container Platform](https://access.redhat.com/solutions/7141255)

# Additional resources

- [Plan your bare-metal cluster for OpenShift Virtualization](../../installing/installing_bare_metal/preparing-to-install-on-bare-metal.xml#virt-planning-bare-metal-cluster-for-ocp-virt_preparing-to-install-on-bare-metal)

- [Prepare your cluster for OpenShift Virtualization](../../virt/install/preparing-cluster-for-virt.xml#preparing-cluster-for-virt)

- [Learn about storage volumes for VM disks](../../virt/install/preparing-cluster-for-virt.xml#virt-about-storage-volumes-for-vm-disks_virt-requirements)

- [Use a CSI-enabled storage provider](../../storage/container_storage_interface/persistent-storage-csi.xml#persistent-storage-csi)

- [Configure local storage for virtual machines](../../virt/storage/virt-configuring-local-storage-with-hpp.xml#virt-configuring-local-storage-with-hpp)

- [Install the OpenShift Virtualization Operator](../../virt/install/installing-virt.xml#virt-installing-virt-operator_installing-virt)

- [Install the Kubernetes NMState Operator](../../networking/networking_operators/k8s-nmstate-about-the-k8s-nmstate-operator.xml#installing-the-kubernetes-nmstate-operator-cli_k8s-nmstate-about-the-k8s-nmstate-operator)

- [Specify nodes for virtual machines](../../virt/managing_vms/advanced_vm_management/virt-specifying-nodes-for-vms.xml#virt-specifying-nodes-for-vms)

- [Install and use the `virtctl` command-line interface (CLI) tool](../../virt/getting_started/virt-using-the-cli-tools.xml#virt-using-the-cli-tools)

- [Create a VM from a Red Hat image](../../virt/creating_vm/virt-creating-vms-from-rh-images-overview.xml#virt-creating-vms-from-rh-images-overview)

- [Create a VM from an instance type](../../virt/creating_vm/virt-creating-vms-from-instance-types.xml#virt-creating-vms-from-instance-types)

- [Import a custom image from a web page](../../virt/creating_vm/virt-creating-vms-from-web-images.xml#virt-creating-vms-from-web-images)

- [Upload an image from your local machine](../../virt/creating_vm/virt-creating-vms-uploading-images.xml#virt-creating-vms-uploading-images)

- [Clone a persistent volume claim (PVC)](../../virt/creating_vm/virt-creating-vms-by-cloning-pvcs.xml#virt-creating-vms-by-cloning-pvcs)

- [Connect a VM to a Linux bridge network](../../virt/vm_networking/virt-connecting-vm-to-linux-bridge.xml#virt-connecting-vm-to-linux-bridge)

- [Connect a VM to an Open Virtual Network (OVN)-Kubernetes secondary network](../../virt/vm_networking/virt-connecting-vm-to-ovn-secondary-network.xml#virt-connecting-vm-to-ovn-secondary-network)

- [Connect a VM to a Single Root I/O Virtualization (SR-IOV) network](../../virt/vm_networking/virt-connecting-vm-to-sriov.xml#virt-connecting-vm-to-sriov)

- [Connect to a virtual machine console](../../virt/managing_vms/virt-accessing-vm-consoles.xml#virt-accessing-vm-consoles)

- [SSH access for virtual machines](../../virt/managing_vms/ssh/virt-accessing-vm-ssh.xml#virt-accessing-vm-ssh)

- [Connect to the desktop viewer by using the web console](../../virt/managing_vms/virt-accessing-vm-consoles.xml#virt-connecting-desktop-viewer-web_virt-accessing-vm-consoles)

- [Manage a VM by using the web console](../../virt/managing_vms/virt-controlling-vm-states.xml#virt-controlling-vm-states)

- [Export a VM](../../virt/managing_vms/virt-exporting-vms.xml#virt-accessing-exported-vm-manifests_virt-exporting-vms)

- [Review post-installation configuration options](../../virt/post_installation_configuration/virt-post-install-config.xml#virt-post-install-config)

- [Configure storage options and automatic boot source updates](../../virt/storage/virt-storage-config-overview.xml#virt-storage-config-overview)

- [Learn about monitoring and health checks](../../virt/monitoring/virt-monitoring-overview.xml#virt-monitoring-overview)

- [Learn about live migration](../../virt/live_migration/virt-about-live-migration.xml#virt-about-live-migration)

- [Back up and restore VMs by using the OpenShift API for Data Protection (OADP)](../../backup_and_restore/application_backup_and_restore/installing/installing-oadp-kubevirt.xml#installing-oadp-kubevirt)

- [Tune and scale your cluster](https://access.redhat.com/articles/6994974)
