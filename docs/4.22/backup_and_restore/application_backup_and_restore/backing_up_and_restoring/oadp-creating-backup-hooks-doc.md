When performing a backup, it is possible to specify one or more commands to execute in a container within a pod, based on the pod being backed up.

The commands can be configured to performed before any custom action processing (*Pre* hooks), or after all custom actions have been completed and any additional items specified by the custom action have been backed up (*Post* hooks).

You create backup hooks to run commands in a container in a pod by editing the `Backup` custom resource (CR).

- Add a hook to the `spec.hooks` block of the `Backup` CR, as in the following example:

  ``` yaml
  apiVersion: velero.io/v1
  kind: Backup
  metadata:
    name: <backup>
    namespace: openshift-adp
  spec:
    hooks:
      resources:
        - name: <hook_name>
          includedNamespaces:
          - <namespace>
          excludedNamespaces:
          - <namespace>
          includedResources: []
          - pods
          excludedResources: []
          labelSelector:
            matchLabels:
              app: velero
              component: server
          pre:
            - exec:
                container: <container>
                command:
                - /bin/uname
                - -a
                onError: Fail
                timeout: 30s
          post:
  ...
  ```

  - Optional: You can specify namespaces to which the hook applies. If this value is not specified, the hook applies to all namespaces.

  - Optional: You can specify namespaces to which the hook does not apply.

  - Currently, pods are the only supported resource that hooks can apply to.

  - Optional: You can specify resources to which the hook does not apply.

  - Optional: This hook only applies to objects matching the label. If this value is not specified, the hook applies to all objects.

  - Array of hooks to run before the backup.

  - Optional: If the container is not specified, the command runs in the first container in the pod.

  - This is the entry point for the `init` container being added.

  - Allowed values for error handling are `Fail` and `Continue`. The default is `Fail`.

  - Optional: How long to wait for the commands to run. The default is `30s`.

  - This block defines an array of hooks to run after the backup, with the same parameters as the pre-backup hooks.
