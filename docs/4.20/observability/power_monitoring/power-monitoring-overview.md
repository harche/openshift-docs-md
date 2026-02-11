> [!IMPORTANT]
> Power monitoring is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

# About power monitoring

You can use power monitoring for Red Hat OpenShift to monitor the power usage and identify power-consuming containers running in an OpenShift Container Platform cluster. Power monitoring collects and exports energy-related system statistics from various components, such as CPU and DRAM. It provides estimates and granular power consumption data for Kubernetes pods and namespaces, and reads the power consumption of nodes.

> [!WARNING]
> Power monitoring Technology Preview works only in bare-metal deployments. Most public cloud vendors do not expose Kernel Power Management Subsystems to virtual machines.

# Power monitoring architecture

Power monitoring is made up of the following major components:

The Power Monitoring Operator
For administrators, the Power Monitoring Operator streamlines the monitoring of power usage for workloads by simplifying the deployment and management of Kepler in an OpenShift Container Platform cluster. The setup and configuration for the Power Monitoring Operator are simplified by adding a `PowerMonitor` custom resource definition (CRD). The Operator also manages operations, such as upgrading, removing, configuring, and redeploying Kepler.

Kepler
Kepler is a key component of power monitoring. It is responsible for monitoring the power usage of containers running in OpenShift Container Platform. It generates metrics related to the power usage of both nodes and containers.

# Kepler hardware support

Kepler is the key component of power monitoring that collects real-time CPU power consumption data from a node through the RAPL Subsystem. By understanding the total power consumption of the node and calculating the percent of CPU time each process is using, it is able to estimate the power consumption at a per process and container level.

Kernel Power Management Subsystem
- `rapl-sysfs`: This requires access to the `/sys/class/powercap/intel-rapl` directory.

# About FIPS compliance for Power Monitoring Operator

Starting with version 0.4, Power Monitoring Operator for Red Hat OpenShift is FIPS compliant. When deployed on an OpenShift Container Platform cluster in FIPS mode, it uses Red Hat Enterprise Linux (RHEL) cryptographic libraries validated by National Institute of Standards and Technology (NIST).

For details on the NIST validation program, see [Cryptographic module validation program](https://csrc.nist.gov/Projects/cryptographic-module-validation-program/validated-modules). For the latest NIST status of RHEL cryptographic libraries, see [Compliance activities and government standards](https://access.redhat.com/en/compliance).

To enable FIPS mode, you must install Power Monitoring Operator for Red Hat OpenShift on an OpenShift Container Platform cluster. For more information, see "Do you need extra security for your cluster?".

# Additional resources

- [Power monitoring dashboards overview](../power_monitoring/visualizing-power-monitoring-metrics.xml#power-monitoring-dashboards-overview_visualizing-power-monitoring-metrics)

- [Do you need extra security for your cluster?](../../installing/overview/installing-preparing.xml#installing-preparing-security)
