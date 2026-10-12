The Model Context Protocol (MCP) server for Red Hat OpenShift Container Platform provides tools and prompts that you can use to manage virtual machines through a natural language interface. You can direct AI assistants to create, manage, and troubleshoot virtual machines on your behalf.

<div class="important">

MCP Server for Red Hat OpenShift Container Platform is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

# Tools and prompts for the MCP server for OpenShift

The Model Context Protocol (MCP) server for Red Hat OpenShift Container Platform provides tools and prompts for managing OpenShift Virtualization virtual machines through natural language. Tools perform actions, and prompts provide workflow templates for AI assistants.

The Model Context Protocol (MCP) server for OpenShift Container Platform provides the following tools:

`vm_create`
Creates a virtual machine in the cluster. This tool supports the following features:

Workload resolution
Accepts operating system names such as `fedora`, `rhel9`, `rhel10`, `ubuntu`, `centos`, and `windows`. These names are resolved to container disk images. If data sources are available in the cluster, the tool matches against those first.

Instance type resolution
Automatically selects an appropriate instance type based on `size` hints, such as `small`, `medium`, or `large`, and `performance` hints, such as `general-purpose`, `overcommitted`, `compute-optimized`, or `memory-optimized`. You can also specify instance types explicitly.

Preference resolution
Resolves virtual machine preferences from cluster resources or data source defaults.

Networking
Supports attaching secondary network interfaces by using Multus `NetworkAttachmentDefinition` resources.

Run strategy
Virtual machines are created in `Halted` state by default. Set `autostart` to `true` to start the virtual machine immediately after creation.

`vm_create_from_template`
Creates a virtual machine from a `VirtualMachineTemplate` resource. Creating a virtual machine from a template in a different namespace is not supported. This tool supports the following parameters:

- `namespace` (required) - The namespace of the `VirtualMachineTemplate` resource and the resulting virtual machine. Both must be in the same namespace.

- `template_name` (required) - The name of the `VirtualMachineTemplate` resource to create the virtual machine from.

- `parameters` - The parameter values to substitute in the template. Keys are parameter names, such as `VM_NAME`, and values are strings. You must provide values for required parameters. Optional parameters use their default values if omitted. Parameters that use `generate` or `from` are generated automatically if not provided.

`vm_lifecycle`
Manages the lifecycle of an existing virtual machine. This tool supports the following actions:

- `start` - Sets the run strategy to `Always`, starting the virtual machine.

- `stop` - Sets the run strategy to `Halted`, stopping the virtual machine.

- `restart` - Stops and then starts the virtual machine.

- `pause` - Suspends execution of a running virtual machine.

- `unpause` - Resumes execution of a paused virtual machine.

`vm_clone`
Clones an existing virtual machine by creating a `VirtualMachineClone` resource. This creates a copy of the source virtual machine with a new name.

`vm_guest_info`
Retrieves guest operating system details from a virtual machine’s QEMU guest agent. The virtual machine must be running with the guest agent active. This tool supports querying specific information types:

- `all` (default) - Returns all available guest agent data.

- `os` - Operating system metadata, version, and kernel details.

- `filesystem` - Mount points, disk usage, and filesystem details.

- `users` - Currently logged-in users.

- `network` - Network interfaces, MAC addresses, and assigned IP addresses.

The MCP server for OpenShift Container Platform provides the following prompts:

`vm-troubleshoot`
Generates a step-by-step troubleshooting guide for diagnosing virtual machine issues. This prompt collects and presents the following information:

- `VirtualMachine` status

- `VirtualMachineInstance` status

- Virtual machine volumes configuration

- `virt-launcher` pod information

- `virt-launcher` pod logs

- Related Kubernetes events

This prompt requires the `namespace` and `name` of the virtual machine to troubleshoot.

`windows-golden-image`
Creates a Windows golden image by running the `windows-efi-installer` Tekton pipeline. The pipeline downloads a Windows ISO, modifies it for EFI automated installation, creates a virtual machine, installs Windows, and produces a bootable data source suitable as a golden image for Windows virtual machines.

This prompt requires the following: \* A Windows ISO download URL must be provided. \* The user must accept the Microsoft License Agreement (EULA) before the pipeline runs.

`hco-status`
Generates a status report for the HyperConverged Cluster Operator (HCO), which manages OpenShift Virtualization and its related components. This prompt collects and presents the following information:

- HCO conditions and installed component versions

- HCO configuration, including feature gates and virtualization settings

- Status of managed components, such as KubeVirt, the Containerized Data Importer (CDI), and network add-ons

- Events in the HCO namespace

This prompt requires no arguments.

When you use the MCP server for OpenShift Container Platform, you are not required to call tools and prompts manually. These can run in the background after being initiated from natural language requests:

``` text
Create a Fedora virtual machine named test-vm in the my-project namespace.
```

``` text
Diagnose a virtual machine named broken-vm in the vm-test namespace that is not starting.
```

``` text
Generate a status report for the HyperConverged Cluster Operator.
```

# Additional resources

- [Inspect clusters with MCP server for Red Hat OpenShift Container Platform](../../ai_applications/mcp_server/mcp-server-overview.xml#mcp-server-overview)
