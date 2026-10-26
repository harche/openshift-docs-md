To scale a OpenShift Container Platform cluster that uses user-provisioned infrastructure, you can manually add compute machines during or after installation. The postinstallation process requires some of the same configuration files and parameters that you used for installation.

# Adding compute machines to Amazon Web Services

You can add more compute machines to your OpenShift Container Platform cluster on AWS.

See [Adding compute machines to AWS by using CloudFormation templates](../../machine_management/user_infra/adding-aws-compute-user-infra.xml#adding-aws-compute-user-infra) for more information.

# Adding compute machines to Microsoft Azure

You can add more compute machines to your OpenShift Container Platform cluster on Microsoft Azure.

See [Creating additional worker machines in Azure](../../installing/installing_azure/upi/installing-azure-user-infra.xml#installation-creating-azure-worker_installing-azure-user-infra) for more information.

# Adding compute machines to Azure Stack Hub

You can add more compute machines to your OpenShift Container Platform cluster on Azure Stack Hub.

See [Creating additional worker machines in Azure Stack Hub](../../installing/installing_azure_stack_hub/upi/installing-azure-stack-hub-user-infra.xml#installation-creating-azure-worker_installing-azure-stack-hub-user-infra) for more information.

# Adding compute machines to Google Cloud

You can add more compute machines to your OpenShift Container Platform cluster on GCP.

See [Creating additional worker machines in Google Cloud](../../installing/installing_gcp/installing-restricted-networks-gcp.xml#installation-creating-gcp-worker_installing-restricted-networks-gcp) for more information.

# Adding compute machines to vSphere

You can add compute machines hosted on VMware vSphere to your OpenShift Container Platform cluster by using compute machine sets or by provisioning the machines manually.

See [use compute machine sets](../../machine_management/creating_machinesets/creating-machineset-vsphere.xml#creating-machineset-vsphere) for more information.

You can also provision additional vSphere virtual machines (VMs) manually and add them to your cluster.

See [Adding compute machines to vSphere manually](../../machine_management/user_infra/adding-vsphere-compute-user-infra.xml#adding-vsphere-compute-user-infra) for more information.

You can manually add bare-metal compute machines or VMs hosted outside vSphere to your existing cluster. These nodes join without vSphere integration.

For more information, see [Add compute machines without vSphere integration](../../machine_management/user_infra/adding-bare-metal-compute-vsphere-user-infra.xml#adding-bare-metal-compute-vsphere-user-infra).

# Adding compute machines to bare metal

You can add more compute machines to your OpenShift Container Platform cluster on bare metal.

See [Adding compute machines to bare metal](../../machine_management/user_infra/adding-bare-metal-compute-user-infra.xml#adding-bare-metal-compute-user-infra) for more information.
