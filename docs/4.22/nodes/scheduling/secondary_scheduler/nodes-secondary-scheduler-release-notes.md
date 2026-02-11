Review the Secondary Scheduler Operator for Red Hat OpenShift release notes to track its development and learn what is new and changed with each release.

The Secondary Scheduler Operator allows you to deploy a custom secondary scheduler in your OpenShift Container Platform cluster.

For more information, see [About the Secondary Scheduler Operator](../../../nodes/scheduling/secondary_scheduler/index.xml#nodes-secondary-scheduler-about_nodes-secondary-scheduler-about).

# Release notes for Secondary Scheduler Operator for Red Hat OpenShift 1.5.0

Review the release notes for Secondary Scheduler Operator 1.5.0 to learn what is new and updated with this release.

Issued: 29 October 2025

The following advisory is available for the Secondary Scheduler Operator for Red Hat OpenShift 1.5.0:

- [RHBA-2025:19251](https://access.redhat.com/errata/RHBA-2025:19251)

## New features and enhancements

- This release of the Secondary Scheduler Operator updates the Kubernetes version to 1.33.

## Known issues

- Currently, you cannot deploy additional resources, such as config maps, CRDs, or RBAC policies through the Secondary Scheduler Operator. Any resources other than roles and role bindings that are required by your custom secondary scheduler must be applied externally. ([WRKLDS-645](https://issues.redhat.com/browse/WRKLDS-645))
