Accelerate the resolution of cluster and virtual machine (VM) issues by using the integrated diagnostic tools and support provided by OpenShift Virtualization.

To gather debugging information, configure Prometheus and Alertmanager and collect `must-gather` data for OpenShift Container Platform and OpenShift Virtualization.

# Opening a support case

Open a support case with Red Hat Support when you encounter an issue that requires immediate assistance.

## Collecting data for Red Hat Support

Gather information about the issue affecting your environment to submit with your support case. This aids Red Hat Support in effectively diagnosing your issue.

Gather troubleshooting information by using the following tools:

- Configure Prometheus and Alertmanager.

<!-- -->

- Configure and use the `must-gather` tool.

- Collect `must-gather` data and memory dumps from VMs.

- Collect `must-gather` data for OpenShift Container Platform and OpenShift Virtualization

## Submitting a support case

Submit a support case to resolve a cluster issue that is affecting the ability of OpenShift Virtualization to function properly in your environment.

You can submit a support case to Red Hat Support by using the Customer Support page. Include data that you collected about your issue with your support request.

## Creating a Jira issue

To report an issue with your environment to Red Hat Support, create a Jira issue in the OpenShift Virtualization (CNV) Jira project.

1.  Log in to Red Hat Atlassian Jira.

2.  Access the **Create Issue** page.

3.  Select OpenShift Virtualization (CNV) as the **Project**.

4.  Select **Bug** as the **Issue Type**.

5.  Click **Next**.

6.  Complete the **Summary** and **Description** fields. In the **Description** field, include a detailed description of the issue.

7.  Submit any collected troubleshooting information.

    1.  Add any textual troubleshooting information, such as command outputs, in the **Description** field.

    2.  Add troubleshooting files using the **Attachment** field.

8.  Select the appropriate component from **Components**.

9.  Click **Create**.

10. Review the details of the bug you created.

# Web console monitoring

Monitor cluster and virtual machine (VM) health with the OpenShift Container Platform web console.

The OpenShift Container Platform web console displays resource usage, alerts, events, and trends for your cluster and for OpenShift Virtualization components and resources.

| Page                                                                                                               | Description                                                    |
|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| **Virtualization** → **VirtualMachines** → **Overview** page                                                       | Cluster details, status, alerts, inventory, and resource usage |
| **Virtualization** → **VirtualMachines** → **Overview** → **Overview** tab                                         | OpenShift Virtualization resources, usage, alerts, and status  |
| **Virtualization** → **Migrations** page                                                                           | Progress of live migrations                                    |
| **Virtualization** → **VirtualMachines** → **Virtual machines** tab                                                | CPU, memory, and storage usage summary                         |
| **Virtualization** → **VirtualMachines** → **Virtual machines** → **VirtualMachine details** → **Metrics** tab     | VM resource usage, storage, network, and migration             |
| **Virtualization** → **VirtualMachines** → **Virtual machines** → **VirtualMachine details** → **Events** tab      | List of VM events                                              |
| **Virtualization** → **VirtualMachines** → **Virtual machines** → **VirtualMachine details** → **Diagnostics** tab | VM status conditions and volume snapshot status                |

Web console pages for monitoring and troubleshooting

# Additional resources

- [Submitting a support case](../../support/getting-support.xml#support-submitting-a-case_getting-support)

- [Collecting data about your environment](../../virt/support/virt-collecting-virt-data.xml#virt-collecting-data-about-your-environment_virt-collecting-virt-data)

- [Using the `must-gather` tool for OpenShift Virtualization](../../virt/support/virt-collecting-virt-data.xml#virt-using-virt-must-gather_virt-collecting-virt-data)

- [Collecting data about virtual machines](../../virt/support/virt-collecting-virt-data.xml#virt-collecting-data-about-vms_virt-collecting-virt-data)
