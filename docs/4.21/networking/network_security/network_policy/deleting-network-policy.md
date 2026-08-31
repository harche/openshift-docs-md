As a cluster administrator, you can delete a network policy from a namespace.

# Delete a network policy using the CLI

You can delete a network policy in a namespace.

<div class="note">

If you log in with `cluster-admin` privileges, you can delete network policies in any namespace in the cluster.

</div>

<div class="note">

If you log in with `cluster-admin` privileges, you can delete network policies in any namespace in the cluster. In the web console, you can delete policies directly in YAML or by using the **Actions** menu.

</div>

- Your cluster uses a network plugin that supports `NetworkPolicy` objects, such as the OVN-Kubernetes network plugin, with `mode: NetworkPolicy` set.

- You installed the OpenShift CLI (`oc`).

- You logged in to the cluster with a user with `admin` privileges.

- You are working in the namespace where the network policy exists.

<!-- -->

- To delete a network policy object, enter the following command. Successful output lists the name of the policy object and the `deleted` status.

  ``` terminal
  $ oc delete networkpolicy <policy_name> -n <namespace>
  ```

  where:

  `<policy_name>`
  Specifies the name of the network policy.

  `<namespace>`
  Optional parameter. If you defined the object in a different namespace than the current namespace, the parameter specifices the namespace.
