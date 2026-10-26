For simplified planning of updates, you can use OpenShift Lightspeed to check update availability, evaluate compatibility with your cluster, and produce an update assessment that you can review as you prepare for a cluster update.

> [!IMPORTANT]
> Creating cluster update assessments with OpenShift Lightspeed is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.
>
> For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

The assessment tool uses OpenShift Lightspeed Service (OLS) to run an `AgenticRun` custom resource (CR), which is used to perform an update precheck and compatibility analysis, and store proposed plans in an `AnalysisResult` CR for you to review.

You can then review the assessment before deciding whether or not to manually start a cluster update using a method of your choosing. The assessment tool does not trigger cluster updates.

> [!IMPORTANT]
> Always review AI-generated content before using it.

# AI assessments using OpenShift Lightspeed

When you install OpenShift Lightspeed on your cluster, it enables the **Cluster Update** page of the web console, where you can create AI generated cluster update assessments.

On the web console, the **Cluster Update** page offers an agentic AI update experience that is driven by OpenShift Lightspeed, enabling you to simplify update planning and research.

When you use OpenShift Lightspeed to generate a cluster update assessment, an assessment tool directs a user-provided Large Language Model (LLM) to perform a preliminary check for cluster update readiness.

The tool then gives you the risk of a cluster update to a target version. You can decide whether or not to initiate the update based on this assessment and your own review of the cluster state.

The assessment tool does not execute an update, it only analyzes the cluster and provides update recommendations. All cluster state data is processed only by the LLM provider you configured OpenShift Lightspeed Service (OLS) to use.

## AI assessment tool workflow and skills

The assessment tool performs the following workflow when you use it to analyze an update path:

1.  The assessment tool patches an `AgenticRunApproval` custom resource, which triggers an analysis request.

2.  An AI agent runs the analysis request inside a read-only sandbox using OLS.

3.  In the sandbox, the agent uses your configured LLM to execute prechecks on categories such as cluster health, node status, Operator compatibility, conditional update risks, deprecated APIs, and so on.

4.  The LLM produces an analysis about these categories, as well as an AI risk score and an assessment of whether or not the update is recommended, and the tool renders this assessment for you to review.

During this analysis, the assessment tool uses the following two skills:

- `cluster-update-advisor`: This skill interprets readiness results and cluster conditions such as `ClusterVersion`, `ClusterOperators`, node conditions, and alerts.

- `product-lifecycle`: This skill checks Operator product lifecycle data for lifecycle freshness, and recommends updates for Operators with less than 4 months of remaining lifecycle support.

# Generating an update assessment

Use OpenShift Lightspeed on the web console to create an AI-generated assessment of the cluster’s readiness to update to your target version.

<div>

<div class="title">

Prerequisites

</div>

- You have access to the cluster with `cluster-admin` privileges.

- You have access to the OpenShift Container Platform web console.

- You installed OpenShift Lightspeed Service (OLS) and configured it to use a Large Language Model (LLM).

- You installed and configured the Lightspeed Agentic Operator.

</div>

<div>

<div class="title">

Procedure

</div>

1.  On the web console, navigate to **Administration** → **Cluster Update**.

2.  Select a target version from the **Select Update Path** dropdown menu.

3.  Click **Analyse**.

4.  Review the assessment produced by AI to determine the readiness of your cluster for an update to the target version.

</div>

# Additional resources

- [Red Hat OpenShift Lightspeed documentation](https://docs.redhat.com/en/documentation/red_hat_openshift_lightspeed/latest)
