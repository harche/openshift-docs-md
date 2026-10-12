You can create reusable virtual machine (VM) blueprints from existing VMs and use them to deploy consistent VMs across namespaces.

# Native virtual machine templates

A `VirtualMachineTemplate` is a native, in-cluster resource that defines a reusable virtual machine (VM) blueprint with parameterized values. You can use `VirtualMachineTemplates` to deploy consistent VMs across namespaces, capturing storage state such as `DataVolume` snapshots and cloned disks.

Unlike traditional templates, `VirtualMachineTemplates` are native to OpenShift Container Platform and support new use cases, such as creating templates from existing VMs and importing and exporting templates to and from the cluster.

The `VirtualMachineTemplate` feature introduces two custom resource definitions (CRDs):

`VirtualMachineTemplate`
Defines a reusable VM blueprint with parameters. Each template contains a VM specification with parameter placeholders and a list of parameter definitions that control how those placeholders are resolved during processing.

`VirtualMachineTemplateRequest`
Creates a `VirtualMachineTemplate` from an existing VM. You can use this CRD to clone a configured VM into a reusable template.

# Convert a virtual machine to a reusable template

You can create a `VirtualMachineTemplate` from an existing virtual machine (VM) by submitting a `VirtualMachineTemplateRequest` custom resource (CR). The template captures the configuration of the source VM, including its storage, so that you can deploy consistent copies of the VM.

<div class="warning">

The template creation process does not generalize the source VM. All secrets, credentials, and machine-specific identifiers from the source VM remain in the resulting template. Review and parameterize sensitive values before distributing the template.

</div>

<div class="note">

To perform the same operation by using the CLI, run the `virtctl template create --vm-name <vm_name>` command. The command creates a `VirtualMachineTemplateRequest` CR on your behalf.

</div>

- The source VM is stopped.

- You have the `virtualmachinetemplaterequest/create` permission in the source VM namespace.

- You have permission to create `VirtualMachineTemplates` and `DataVolumes` in the target namespace.

- The disks of the source VM belong to a storage class that supports Container Storage Interface (CSI) volume snapshots. To list the volume snapshot classes that are available in the cluster, run the following command:

  ``` terminal
  $ oc get volumesnapshotclass
  ```

  The `DRIVER` column lists the CSI provisioner for each volume snapshot class. The storage class of the source VM disks must specify one of these provisioners in its `provisioner` field.

1.  Create a `VirtualMachineTemplateRequest` manifest:

    ``` yaml
    apiVersion: template.kubevirt.io/v1beta1
    kind: VirtualMachineTemplateRequest
    metadata:
      name: promote-to-catalog
      namespace: shared-templates
    spec:
      templateName: my-golden-vm
      virtualMachineRef:
        name: my-configured-vm
        namespace: my-namespace
    ```

    where:

    `metadata.namespace`
    Specifies the namespace where the template is created. If you omit this field, the template is created in the current namespace.

    `templateName`
    Specifies the name for the template to be created.

    `virtualMachineRef.name`
    Specifies the name of the source VM.

    `virtualMachineRef.namespace`
    Specifies the namespace of the source VM.

2.  Apply the manifest:

    ``` terminal
    $ oc apply -f promote-to-catalog.yaml
    ```

3.  Wait for the template to be created:

    ``` terminal
    $ oc wait vmtr promote-to-catalog -n shared-templates --for=condition=Ready
    ```

- Verify that the template was created in the target namespace:

  ``` terminal
  $ oc get vmt my-golden-vm -n shared-templates
  ```

# Convert an existing template to a virtual machine template

You can convert an existing `Template` object to a `VirtualMachineTemplate` manifest by using the `virtctl` CLI. Convert your templates to migrate existing virtual machine (VM) definitions to native virtual machine templates.

- You have installed the `virtctl` CLI.

- The source template contains exactly one `VirtualMachine` object. Templates that define multiple objects are not supported.

1.  Convert the template and save the output:

    ``` terminal
    $ virtctl template convert -f <template_file> > <vm_template_file>
    ```

    where:

    `<template_file>`
    Specifies the file that contains the source `Template` object.

    `<vm_template_file>`
    Specifies the file to write the `VirtualMachineTemplate` manifest to.

    <div class="note">

    To convert a `Template` object that already exists in the cluster, specify its name instead of a file, for example: `virtctl template convert <template_name>`. To print the converted manifest in JSON format, add the `-o json` flag.

    </div>

2.  Review the converted manifest and adjust the parameter definitions as needed.

3.  Apply the manifest:

    ``` terminal
    $ oc apply -f <vm_template_file>
    ```

- Verify that the template was created:

  ``` terminal
  $ oc get vmt <template_name>
  ```

# Create a virtual machine from a template

You can process a `VirtualMachineTemplate` to create a new virtual machine (VM) with your own parameter values.

- You have installed the `virtctl` CLI.

- A `VirtualMachineTemplate` exists in the cluster.

- For server-side processing, you have the `process/create` subresource permission on the `VirtualMachineTemplate` resource. This permission is not required for local processing.

1.  View the parameters defined in the template:

    ``` terminal
    $ virtctl template process <template_name> --print-params
    ```

2.  Optional: Preview the VM manifest that the template produces by omitting the `--create` flag:

    ``` terminal
    $ virtctl template process <template_name> -p <PARAMETER>=<value>
    ```

    where:

    `<template_name>`
    Specifies the name of the template to process.

    `<PARAMETER>`
    Specifies the name of a parameter that is defined in the template.

    `<value>`
    Specifies the value to assign to the parameter.

    The manifest is printed in YAML format. To print it in JSON format, add the `-o json` flag.

3.  Optional: Process the template on the client instead of the server by adding the `--local` flag:

    ``` terminal
    $ virtctl template process <template_name> --local
    ```

    Local processing prints the resulting manifest and does not require the `process/create` subresource permission. You can apply the output by using the `oc apply -f` command.

4.  Create a VM from the template:

    ``` terminal
    $ virtctl template process <template_name> -p <PARAMETER>=<value> --create
    ```

    You must specify a value for each required parameter by using the `-p` flag. To set multiple parameters, repeat the `-p` flag.

    <div class="note">

    You cannot combine the `--create` flag with the `--local` flag. Creating a VM directly from a template requires the `create` subresource API.

    </div>

- Verify that the VM was created:

  ``` terminal
  $ oc get vm
  ```

# Virtual machine template commands

You can use the `virtctl template` commands to create, process, and convert virtual machine (VM) templates from the command line. These commands perform the same operations as the corresponding custom resources.

| Command                                                                  | Description                                                                                                                                                                                        |
|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `virtctl template create --vm-name <vm_name>`                            | Create a `VirtualMachineTemplate` from an existing VM by creating a `VirtualMachineTemplateRequest` custom resource (CR). The template is created in the current namespace with a randomized name. |
| `virtctl template create --vm-name <vm_name> --name <template_name>`     | Create a template, specifying a name for the template.                                                                                                                                             |
| `virtctl template create --vm-name <vm_name> --vm-namespace <namespace>` | Create a template from a source VM that runs in a different namespace. The template is created in the current namespace.                                                                           |

Template creation commands

| Command                                                                    | Description                                                                                                                          |
|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `virtctl template process <template_name> --print-params`                  | Print the parameters of a template, including the description, generator, and default value of each parameter.                       |
| `virtctl template process <template_name> -p <PARAMETER>=<value>`          | Process a template on the server and print the resulting `VirtualMachine` manifest. Repeat the `-p` flag to set multiple parameters. |
| `virtctl template process <template_name> --params-file <file_name>`       | Process a template by using parameters from a JSON or YAML file.                                                                     |
| `virtctl template process <template_name> -p <PARAMETER>=<value> --create` | Process a template and create the resulting VM by using the `process` subresource API.                                               |
| `virtctl template process <template_name> --local`                         | Process a template from the cluster on the client instead of calling the `process` subresource API.                                  |
| `virtctl template process -f <template_file>`                              | Process a template file on the client. Specify `-` to read the template from standard input.                                         |
| `virtctl template process <template_name> -o json`                         | Print the processed manifest in JSON format. The default format is YAML.                                                             |

Template processing commands

| Command                                            | Description                                                                                              |
|----------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| `virtctl template convert <template_name>`         | Convert an existing `Template` object in the cluster to a `VirtualMachineTemplate` manifest.             |
| `virtctl template convert -f <template_file>`      | Convert an existing `Template` object from a file. Specify `-` to read the template from standard input. |
| `virtctl template convert <template_name> -o json` | Print the converted manifest in JSON format. The default format is YAML.                                 |

Template conversion commands

<div class="note">

The following flag combinations are rejected:

- `--create` with `--file`, `--local`, or `--print-params`

- `--file` with `--name` or `--local`

- `--param` with `--params-file`

Because `--file` processes a template on the client, you do not need to specify `--local` with it.

</div>

# VirtualMachineTemplate parameter fields

Each parameter in `spec.parameters` of a `VirtualMachineTemplate` resource supports the following fields. You can use these fields to define static defaults, require user input, or auto-generate values when creating VMs from a template.

| Field         | Description                                                                                                                                                                              |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`        | The unique identifier for the parameter. This string acts as a substitution variable, for example, `${NAME}`, anywhere within the template’s `virtualMachine` specification.             |
| `value`       | The static default value applied to the parameter. This field cannot be used if `required` is set to `true`.                                                                             |
| `generate`    | The mechanism used to dynamically create a value if the user omits it. Set this to `expression` to generate a random string based on the regex pattern defined in the `from` field.      |
| `from`        | The regular expression (regex) pattern that dictates the format of the generated string. This field is mandatory when `generate` is set to `expression`.                                 |
| `required`    | A boolean flag that determines whether the user must explicitly supply the parameter. If `true`, template processing fails without input. Cannot be combined with `value` or `generate`. |
| `displayName` | An optional human-readable name for a graphical user interface (GUI) display.                                                                                                            |
| `description` | An optional description of the purpose of the parameter.                                                                                                                                 |

Parameter fields

## Parameter types

Static parameters
Have a fixed default value that is used if no override is provided.

``` yaml
- name: INSTANCETYPE
  value: u1.medium
  description: Instance type for the VM
```

Required parameters
Must be provided during processing.

``` yaml
- name: PASSWORD
  required: true
  description: Password for the cloud-init user
```

Generated parameters
Produce random values based on a pattern.

``` yaml
- name: NAME
  generate: expression
  from: "fedora-[a-z0-9]{16}"
  description: Unique VM name
```

Optional parameters
Have no default value or generator. If not provided, the placeholder is replaced with an empty string.

## Example VirtualMachineTemplate

The following example defines a template with a generated name, a default instance type, and a required password parameter:

``` yaml
apiVersion: template.kubevirt.io/v1beta1
kind: VirtualMachineTemplate
metadata:
  name: fedora-template
spec:
  parameters:
    - name: NAME
      generate: expression
      from: "fedora-[a-z0-9]{16}"
      description: Unique VM name
    - name: INSTANCETYPE
      value: u1.medium
      description: Instance type for the VM
    - name: PASSWORD
      required: true
      description: Password for the cloud-init user
  virtualMachine:
    metadata:
      name: ${NAME}
    spec:
      instancetype:
        kind: VirtualMachineClusterInstancetype
        name: ${INSTANCETYPE}
      preference:
        kind: VirtualMachineClusterPreference
        name: fedora
      runStrategy: Halted
      template:
        spec:
          domain:
            devices: {}
          volumes:
            - containerDisk:
                image: quay.io/containerdisks/fedora:latest
              name: rootdisk
            - cloudInitNoCloud:
                userData: |-
                  #cloud-config
                  user: fedora
                  password: ${PASSWORD}
                  chpasswd: { expire: False }
              name: cloudinitdisk
```

# Additional resources

- [CSI volume snapshots](../../storage/container_storage_interface/persistent-storage-csi-snapshots.xml#persistent-storage-csi-snapshots)
