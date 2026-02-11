You can destroy a hosted cluster on IBM Power by using the command-line interface (CLI).

# Destroying a hosted cluster on IBM Power by using the CLI

To destroy a hosted cluster on IBM Power, you can use the hcp command-line interface (CLI).

<div>

<div class="title">

Procedure

</div>

- Delete the hosted cluster by running the following command:

  ``` terminal
  $ hcp destroy cluster agent
   --name=<hosted_cluster_name> \
   --namespace=<hosted_cluster_namespace> \
   --cluster-grace-period <duration>
  ```

  - Replace `<hosted_cluster_name>` with the name of your hosted cluster.

  - Replace `<hosted_cluster_namespace>` with the name of your hosted cluster namespace.

  - Specifies the duration to destroy the hosted cluster completely, for example, `20m0s`.

</div>
