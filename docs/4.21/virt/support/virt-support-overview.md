You can request assistance from Red Hat Support, report bugs, collect data about your environment, and monitor the health of your cluster and virtual machines (VMs) with the following tools.

# Opening support tickets

If you have encountered an issue that requires immediate assistance from Red Hat Support, you can submit a support case.

To report a bug, you can create a Jira issue directly.

## Submitting a support case

To request support from Red Hat Support, follow [the instructions for submitting a support case](../../support/getting-support.xml#support-submitting-a-case_getting-support).

It is helpful to collect debugging data to include with your support request.

### Collecting data for Red Hat Support

You can gather debugging information by performing the following steps:

[Collecting data about your environment](../../virt/support/virt-collecting-virt-data.xml#virt-collecting-data-about-your-environment_virt-collecting-virt-data)
Configure Prometheus and Alertmanager and collect `must-gather` data for OpenShift Container Platform and OpenShift Virtualization.

<!-- -->

[`must-gather` tool for OpenShift Virtualization](../../virt/support/virt-collecting-virt-data.xml#virt-using-virt-must-gather_virt-collecting-virt-data)
Configure and use the `must-gather` tool.

[Collecting data about VMs](../../virt/support/virt-collecting-virt-data.xml#virt-collecting-data-about-vms_virt-collecting-virt-data)
Collect `must-gather` data and memory dumps from VMs.

## Creating a Jira issue

To report a bug, you can create a Jira issue directly by filling out the form on the [**Create Issue**](https://issues.redhat.com/secure/CreateIssueDetails!init.jspa?pid=12323181&issuetype=1&priority=10200) page.

# Web console monitoring

You can monitor the health of your cluster and VMs by using the OpenShift Container Platform web console. The web console displays resource usage, alerts, events, and trends for your cluster and for OpenShift Virtualization components and resources.

| Page                                                                                        | Description                                                    |
|---------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| **Overview** page                                                                           | Cluster details, status, alerts, inventory, and resource usage |
| **Virtualization** → **Overview** tab                                                       | OpenShift Virtualization resources, usage, alerts, and status  |
| **Virtualization** → **Top consumers** tab                                                  | Top consumers of CPU, memory, and storage                      |
| **Virtualization** → **Migrations** tab                                                     | Progress of live migrations                                    |
| **Virtualization** → **VirtualMachines** tab                                                | CPU, memory, and storage usage summary                         |
| **Virtualization** → **VirtualMachines** → **VirtualMachine details** → **Metrics** tab     | VM resource usage, storage, network, and migration             |
| **Virtualization** → **VirtualMachines** → **VirtualMachine details** → **Events** tab      | List of VM events                                              |
| **Virtualization** → **VirtualMachines** → **VirtualMachine details** → **Diagnostics** tab | VM status conditions and volume snapshot status                |

Web console pages for monitoring and troubleshooting
