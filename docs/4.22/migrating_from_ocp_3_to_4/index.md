OpenShift Container Platform 4 clusters are different from OpenShift Container Platform 3 clusters. OpenShift Container Platform 4 clusters contain new technologies and functionality that result in a cluster that is self-managing, flexible, and automated. To learn more about migrating from OpenShift Container Platform 3 to 4 see [About migrating from OpenShift Container Platform 3 to 4](../migrating_from_ocp_3_to_4/about-migrating-from-3-to-4.xml#about-migrating-from-3-to-4).

# Differences between OpenShift Container Platform 3 and 4

Before migrating from OpenShift Container Platform 3 to 4, you can check [differences between OpenShift Container Platform 3 and 4](../migrating_from_ocp_3_to_4/planning-migration-3-4.xml#planning-migration-3-4). Review the following information:

- [Architecture](../architecture/architecture.xml#architecture)

- [Installation and update](../architecture/architecture-installation.xml#architecture-installation)

- [Storage](../storage/index.xml#index), [network](../networking/networking_overview/understanding-networking.xml#understanding-networking), [security](../security/index.xml#index), and [monitoring considerations](../observability/monitoring/about-ocp-monitoring.xml#about-ocp-monitoring)

# Planning network considerations

Before migrating from OpenShift Container Platform 3 to 4, review the [differences between OpenShift Container Platform 3 and 4](../migrating_from_ocp_3_to_4/planning-migration-3-4.xml#planning-migration-3-4) for information about the following areas:

- [DNS considerations](../migrating_from_ocp_3_to_4/planning-considerations-3-4.xml#dns-considerations_planning-considerations-3-4)

  - [Isolating the DNS domain of the target cluster from the clients](../migrating_from_ocp_3_to_4/planning-considerations-3-4.xml#migration-isolating-dns-domain-of-target-cluster-from-clients_planning-considerations-3-4).

  - [Setting up the target cluster to accept the source DNS domain](../migrating_from_ocp_3_to_4/planning-considerations-3-4.xml#migration-setting-up-target-cluster-to-accept-source-dns-domain_planning-considerations-3-4).

You can migrate stateful application workloads from OpenShift Container Platform 3 to 4 at the granularity of a namespace. To learn more about MTC see [Understanding MTC](../migrating_from_ocp_3_to_4/about-mtc-3-4.xml#about-mtc-3-4).

> [!NOTE]
> If you are migrating from OpenShift Container Platform 3, see [About migrating from OpenShift Container Platform 3 to 4](../migrating_from_ocp_3_to_4/about-migrating-from-3-to-4.xml#about-migrating-from-3-to-4) and [Installing the legacy Migration Toolkit for Containers Operator on OpenShift Container Platform 3](../migrating_from_ocp_3_to_4/installing-3-4.xml#migration-installing-legacy-operator_installing-3-4).

# Installing MTC

Review the following tasks to install the MTC:

1.  [Install the Migration Toolkit for Containers Operator on target cluster by using Operator Lifecycle Manager (OLM)](../migrating_from_ocp_3_to_4/installing-3-4.xml#migration-installing-mtc-on-ocp-4_installing-3-4).

2.  [Install the legacy Migration Toolkit for Containers Operator on the source cluster manually](../migrating_from_ocp_3_to_4/installing-3-4.xml#migration-installing-legacy-operator_installing-3-4).

3.  [Configure object storage to use as a replication repository](../migrating_from_ocp_3_to_4/installing-3-4.xml#configuring-replication-repository_installing-3-4).

# Upgrading MTC

You [upgrade the Migration Toolkit for Containers (MTC)](../migrating_from_ocp_3_to_4/upgrading-3-4.xml#upgrading-3-4) on OpenShift Container Platform 4.17 by using OLM. You upgrade MTC on OpenShift Container Platform 3 by reinstalling the legacy Migration Toolkit for Containers Operator.

# Reviewing premigration checklists

Before you migrate your application workloads with the Migration Toolkit for Containers (MTC), review the [premigration checklists](../migrating_from_ocp_3_to_4/premigration-checklists-3-4.xml#premigration-checklists-3-4).

# Migrating applications

You can migrate your applications by using the MTC [web console](../migrating_from_ocp_3_to_4/migrating-applications-3-4.xml#migrating-applications-mtc-web-console_migrating-applications-3-4) or [the command line](../migrating_from_ocp_3_to_4/advanced-migration-options-3-4.xml#migrating-applications-cli_advanced-migration-options-3-4).

# Advanced migration options

You can automate your migrations and modify MTC custom resources to improve the performance of large-scale migrations by using the following options:

- [Running a state migration](../migrating_from_ocp_3_to_4/advanced-migration-options-3-4.xml#migration-state-migration-cli_advanced-migration-options-3-4)

- [Creating migration hooks](../migrating_from_ocp_3_to_4/advanced-migration-options-3-4.xml#migration-hooks_advanced-migration-options-3-4)

- [Editing, excluding, and mapping migrated resources](../migrating_from_ocp_3_to_4/advanced-migration-options-3-4.xml#migration-plan-options_advanced-migration-options-3-4)

- [Configuring the migration controller for large migrations](../migrating_from_ocp_3_to_4/advanced-migration-options-3-4.xml#migration-controller-options_advanced-migration-options-3-4)

# Troubleshooting migrations

You can perform the following troubleshooting tasks:

- [Viewing migration plan resources by using the MTC web console](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-viewing-migration-plan-resources_troubleshooting-3-4)

- [Viewing the migration plan aggregated log file](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-viewing-migration-plan-log_troubleshooting-3-4)

- [Using the migration log reader](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-using-mig-log-reader_troubleshooting-3-4)

- [Accessing performance metrics](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-accessing-performance-metrics_troubleshooting-3-4)

- [Using the `must-gather` tool](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-using-must-gather_troubleshooting-3-4)

- [Using the Velero CLI to debug `Backup` and `Restore` CRs](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-debugging-velero-resources_troubleshooting-3-4)

- [Using MTC custom resources for troubleshooting](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#migration-using-mtc-crs-for-troubleshooting_troubleshooting-3-4)

- [Checking common issues and concerns](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#common-issues-and-concerns_troubleshooting-3-4)

# Rolling back a migration

You can [roll back a migration](../migrating_from_ocp_3_to_4/troubleshooting-3-4.xml#rolling-back-migration_troubleshooting-3-4) by using the MTC web console, by using the CLI, or manually.

# Uninstalling MTC and deleting resources

You can [uninstall the MTC and delete its resources](../migrating_from_ocp_3_to_4/installing-3-4.xml#migration-uninstalling-mtc-clean-up_installing-3-4) to clean up the cluster.
