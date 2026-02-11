Cluster administrators can use the Run Once Duration Override Operator to force a limit on the time that run-once pods can be active. After the time limit expires, the cluster tries to terminate the run-once pods. The main reason to have such a limit is to prevent tasks such as builds to run for an excessive amount of time.

To apply the run-once duration override from the Run Once Duration Override Operator to run-once pods, you must enable it on each applicable namespace.

These release notes track the development of the Run Once Duration Override Operator for OpenShift Container Platform.

For an overview of the Run Once Duration Override Operator, see [About the Run Once Duration Override Operator](../../../nodes/pods/run_once_duration_override/index.xml#run-once-about_run-once-duration-override-about).

> [!IMPORTANT]
> The Run Once Duration Override Operator is not currently available for OpenShift Container Platform 4.17. The Operator is planned to be released in the near future.
