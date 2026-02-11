The isolating nature of namespaces means that users cannot by default clone resources between namespaces.

To enable a user to clone a virtual machine to another namespace, a user with the `cluster-admin` role must create a new cluster role. Bind this cluster role to a user to enable them to clone virtual machines to the destination namespace.

# Creating RBAC resources for cloning data volumes

You can create a new cluster role that enables permissions for all actions for the `datavolumes` resource.

<div>

<div class="title">

Prerequisites

</div>

- You have installed the OpenShift CLI (`oc`).

- You must have cluster admin privileges.

</div>

> [!NOTE]
> If you are a non-admin user that is an administrator for both the source and target namespaces, you can create a `Role` instead of a `ClusterRole` where appropriate.

<div>

<div class="title">

Procedure

</div>

1.  Create a `ClusterRole` manifest:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: <datavolume-cloner>
    rules:
    - apiGroups: ["cdi.kubevirt.io"]
      resources: ["datavolumes/source"]
      verbs: ["*"]
    ```

    - Unique name for the cluster role.

2.  Create the cluster role in the cluster:

    ``` terminal
    $ oc create -f <datavolume-cloner.yaml>
    ```

    - The file name of the `ClusterRole` manifest created in the previous step.

3.  Create a `RoleBinding` manifest that applies to both the source and destination namespaces and references the cluster role created in the previous step.

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: <allow-clone-to-user>
      namespace: <Source namespace>
    subjects:
    - kind: ServiceAccount
      name: default
      namespace: <Destination namespace>
    roleRef:
      kind: ClusterRole
      name: datavolume-cloner
      apiGroup: rbac.authorization.k8s.io
    ```

    - Unique name for the role binding.

    - The namespace for the source data volume.

    - The namespace to which the data volume is cloned.

    - The name of the cluster role created in the previous step.

4.  Create the role binding in the cluster:

    ``` terminal
    $ oc create -f <datavolume-cloner.yaml>
    ```

    - The file name of the `RoleBinding` manifest created in the previous step.

</div>
