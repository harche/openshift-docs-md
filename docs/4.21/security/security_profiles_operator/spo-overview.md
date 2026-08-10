With the OpenShift Container Platform Security Profiles Operator (SPO), you can define seccomp and SELinux profiles as custom resources and keep them synchronized across every node in a namespace.

The SPO distributes seccomp and SELinux profile custom resources to each node and keeps them up to date when profiles change. You can also bind policies to pods and record workloads. See Additional resources for advanced tasks such as enabling the log enricher, configuring webhooks and metrics, or restricting profiles to a single namespace, and for advanced audit logging that correlates cluster users with actions during `oc exec`, `oc rsh`, and `oc debug` sessions.

# Additional resources

- [Security Profiles Operator release notes](../../security/security_profiles_operator/spo-release-notes.xml#spo-release-notes)

- [Security Profiles Operator support](../../security/security_profiles_operator/spo-support.xml#spo-support)

- [Understanding the Security Profiles Operator](../../security/security_profiles_operator/spo-understanding.xml#spo-understanding)

- [Enabling the Security Profiles Operator](../../security/security_profiles_operator/spo-enabling.xml#spo-enabling)

- [Managing seccomp profiles](../../security/security_profiles_operator/spo-seccomp.xml#spo-seccomp)

- [Managing SELinux profiles](../../security/security_profiles_operator/spo-selinux.xml#spo-selinux)

- [Advanced Security Profiles Operator tasks](../../security/security_profiles_operator/spo-advanced.xml#spo-advanced)

- [Advanced Audit Logging Framework](../../security/security_profiles_operator/spo-logging.xml#spo-audit-logging)

- [Troubleshooting the Security Profiles Operator](../../security/security_profiles_operator/spo-troubleshooting.xml#spo-inspecting-seccomp-profiles_spo-troubleshooting)

- [Uninstalling the Security Profiles Operator](../../security/security_profiles_operator/spo-uninstalling.xml#spo-uninstalling)

- [seccomp](https://kubernetes.io/docs/tutorials/security/seccomp/)
