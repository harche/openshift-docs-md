The Network Observability CLI (oc netobserv) is a standalone OpenShift CLI (`oc`) plugin used to debug and troubleshoot cluster network traffic. It operates independently of the Network Observability Operator to gather immediate network performance diagnostics.

# About the Network Observability CLI

Use the Network Observability CLI (`oc netobserv`) to quickly debug and troubleshoot networking issues. This tool provides instant, live insight into flows and packets without installing the Network Observability Operator.

The Network Observability CLI is a flow and packet visualization tool that relies on eBPF agents to stream collected data to an ephemeral collector pod. It requires no persistent storage during the capture. After the run, the output is transferred to your local machine.

<div class="important">

CLI capture is meant to run only for short durations, such as 8-10 minutes. If it runs for too long, it can be difficult to delete the running process.

</div>

# Installing the Network Observability CLI

The Network Observability CLI gives you a lightweight way to quickly debug and troubleshoot network observability. It must be installed separately.

Installing the Network Observability CLI (`oc netobserv`) is a separate procedure from the Network Observability Operator installation. This means that, even if the Operator is installed from the software catalog, the `CLI` must be installed separately.

<div class="note">

Users can optionally use Krew to install the `netobserv` CLI plugin. For more information, see "Installing a CLI plugin with Krew".

</div>

- You must install the OpenShift CLI (`oc`).

- You must have a macOS or Linux operating system.

- You must install either `docker` or `podman`.

<div class="note">

You can use `podman` or `docker` to run the installation commands. This procedure uses `podman`.

</div>

1.  Log in to the **Red Hat registry** by running the following command:

    ``` terminal
    $ podman login registry.redhat.io
    ```

2.  Extract the `oc-netobserv` file from the image by running the following commands:

    ``` terminal
    $ podman create --name netobserv-cli registry.redhat.io/network-observability/network-observability-cli-rhel9:1.11
    $ podman cp netobserv-cli:/oc-netobserv .
    $ podman rm netobserv-cli
    ```

3.  Move the extracted file to a directory that is on the system’s `PATH`, such as `/usr/local/bin/`, by running the following command:

    ``` terminal
    $ sudo mv oc-netobserv /usr/local/bin/
    ```

<!-- -->

1.  Verify that `oc netobserv` is available:

    ``` terminal
    $ oc netobserv version
    ```

    This command should produce an outcome similar to the following example:

<!-- -->

    Netobserv CLI version <version>

- [Installing and using CLI plugins](../../../cli_reference/openshift_cli/extending-cli-plugins.xml#cli-installing-plugins_cli-extend-plugins)

- [Installing the CLI Manager Operator](../../../cli_reference/cli_manager/cli-manager-install.xml#installing-cli-manager)
