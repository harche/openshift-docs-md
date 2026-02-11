A user performs a range of operations while working on OpenShift Container Platform such as the following:

- Managing clusters

- Building, deploying, and managing applications

- Managing deployment processes

- Creating and maintaining Operator catalogs

OpenShift Container Platform offers a set of command-line interface (CLI) tools that simplify these tasks by enabling users to perform various administration and development operations from the terminal. These tools expose simple commands to manage the applications, as well as interact with each component of the system.

# List of CLI tools

The following set of CLI tools are available in OpenShift Container Platform:

- [OpenShift CLI (`oc`)](../cli_reference/openshift_cli/getting-started-cli.xml#cli-getting-started): This is the most commonly used CLI tool by OpenShift Container Platform users. It helps both cluster administrators and developers to perform end-to-end operations across OpenShift Container Platform using the terminal. Unlike the web console, it allows the user to work directly with the project source code using command scripts.

- [Knative CLI (kn)](../cli_reference/kn-cli-tools.xml#kn-cli-tools): The Knative (`kn`) CLI tool provides simple and intuitive terminal commands that can be used to interact with OpenShift Serverless components, such as Knative Serving and Eventing.

- [Pipelines CLI (tkn)](../cli_reference/tkn_cli/installing-tkn.xml#installing-tkn): OpenShift Pipelines is a continuous integration and continuous delivery (CI/CD) solution in OpenShift Container Platform, which internally uses Tekton. The `tkn` CLI tool provides simple and intuitive commands to interact with OpenShift Pipelines using the terminal.

- [opm CLI](../cli_reference/opm/cli-opm-install.xml#cli-opm-install): The `opm` CLI tool helps the Operator developers and cluster administrators to create and maintain the catalogs of Operators from the terminal.
