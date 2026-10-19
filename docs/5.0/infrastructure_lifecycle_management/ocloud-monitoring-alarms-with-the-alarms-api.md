You can monitor infrastructure and cluster health by querying alarms through the O-Cloud Manager Alarms API. The Alarms API aggregates alerts from RHACM Observability into standardized alarm records. You can query, filter, and acknowledge alarms, and create subscriptions to receive real-time notifications when alarm states change.

<div class="note">

The Alarms API aggregates alerts from RHACM Observability into standardized alarm records that conform to the O-RAN O2 IMS specification for the telecommunications use case.

</div>

<div class="important">

The O-Cloud Manager is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

- [Observability in RHACM](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.17/html/observability/index)

# Query and filter infrastructure alarms

You can query the O-Cloud Manager Alarms API to list active infrastructure and cluster alarms. The Alarms API aggregates alerts from RHACM Observability Alertmanager and exposes them as O-RAN O2 IMS compliant alarm records with standardized severity levels, timestamps, and resource associations.

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables.

- RHACM Observability is configured and running on the hub cluster.

1.  Set the Alarms API base URL by running the following command:

    ``` terminal
    $ export ALARMS_URL="https://${API_BASE_URL}/O2ims_infrastructureMonitoring/v1"
    ```

2.  List all active alarms by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${ALARMS_URL}/alarms" | jq
    ```

    <div class="formalpara-title">

    **Example output**

    </div>

    ``` json
    [
      {
        "alarmEventRecordId": "e213f273-b6fa-48db-9aa2-a00df5de5747",
        "alarmDefinitionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "probableCauseId": "00000000-0000-0000-0000-000000000000",
        "alarmRaisedTime": "2025-09-10T19:45:16.78Z",
        "alarmChangedTime": "2025-09-25T16:25:12.977032Z",
        "alarmAcknowledged": false,
        "perceivedSeverity": 3,
        "extensions": {
          "alertname": "UpdateAvailable",
          "severity": "info",
          "summary": "Your upstream update recommendation service recommends you update your cluster."
        }
      }
    ]
    ```

3.  Filter alarms by severity by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${ALARMS_URL}/alarms?filter=(eq,perceivedSeverity,0)" | jq
    ```

    The `perceivedSeverity` field uses the values mapped from Prometheus alert severity labels.

4.  Filter alarms by acknowledgment status by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${ALARMS_URL}/alarms?filter=(eq,alarmAcknowledged,false)" | jq
    ```

5.  Get a specific alarm by its identifier by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${ALARMS_URL}/alarms/<alarm_id>" | jq
    ```

    - Replace `<alarm_id>` with the `alarmEventRecordId` value.

- A successful response returns a JSON array of alarm records. An empty array indicates no alarms match the filter criteria.

# Acknowledge an alarm

You can acknowledge an alarm through the O-Cloud Manager Alarms API. Acknowledging an alarm does not resolve it, but marks it as reviewed.

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables.

- You identified the alarm to acknowledge by querying alarms.

<!-- -->

- Acknowledge an alarm by running the following command:

  ``` terminal
  $ curl -ks \
    -H "Authorization: Bearer ${MY_TOKEN}" \
    -H "Content-Type: application/merge-patch+json" \
    -X PATCH \
    -d '{"alarmAcknowledged": true}' \
    "https://${API_BASE_URL}/O2ims_infrastructureMonitoring/v1/alarms/<alarm_id>" | jq
  ```

  Replace `<alarm_id>` with the `alarmEventRecordId` of the alarm to acknowledge.

  <div class="note">

  The PATCH endpoint also supports modifying `perceivedSeverity` to manually override the severity level of an alarm record.

  </div>

<!-- -->

- Verify the alarm is acknowledged by running the following command:

  ``` terminal
  $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
    "https://${API_BASE_URL}/O2ims_infrastructureMonitoring/v1/alarms/<alarm_id>" | jq '.alarmAcknowledged'
  ```

  The output returns `true` if the alarm is acknowledged.

# Manage alarm subscriptions

You can create alarm subscriptions through the O-Cloud Manager Alarms API to receive real-time HTTP notifications when alarm states change. When a subscription is active, the O-Cloud Manager sends callbacks to the specified endpoint whenever a matching alarm event occurs.

- You authenticated to the O-Cloud Manager REST API and set the `API_BASE_URL` and `MY_TOKEN` environment variables.

- You configured SMO integration for the O-Cloud Manager. Alarm subscription creation is blocked until the SMO attributes are configured in the `Inventory` custom resource (CR).

- Your webhook endpoint is reachable from the hub cluster and responds to GET requests with a `204` status code.

1.  Set the Alarms API base URL by running the following command:

    ``` terminal
    $ export ALARMS_URL="https://${API_BASE_URL}/O2ims_infrastructureMonitoring/v1"
    ```

2.  Create an alarm subscription by running the following command:

    ``` terminal
    $ curl -ks -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${MY_TOKEN}" \
      -d '{
        "consumerSubscriptionId": "69253c4b-8398-4602-855d-783865f5f25c",
        "filter": "NEW",
        "callback": "https://smo.example.com/v1/alarms"
      }' \
      "${ALARMS_URL}/alarmSubscriptions" | jq
    ```

    - `consumerSubscriptionId` must be a valid UUID identifying this subscription on the consumer side.

    - `callback` is the URL where the O-Cloud Manager sends alarm notifications.

    - `filter` specifies which alarm event type to exclude from notifications. If you omit the filter, all alarm events are reported:

      - `NEW` — Exclude notifications when a new alarm is raised.

      - `CHANGE` — Exclude notifications when an existing alarm changes, for example a severity change.

      - `CLEAR` — Exclude notifications when an alarm is cleared.

      - `ACKNOWLEDGE` — Exclude notifications when an alarm is acknowledged.

      <div class="note">

      If SMO attributes are not configured in the `Inventory` CR, subscription creation fails with the error: "provisioning of Alarm Subscriptions is blocked until the SMO attributes are configured."

      </div>

3.  List all alarm subscriptions by running the following command:

    ``` terminal
    $ curl -ks -H "Authorization: Bearer ${MY_TOKEN}" \
      "${ALARMS_URL}/alarmSubscriptions" | jq
    ```

4.  Delete an alarm subscription by running the following command:

    ``` terminal
    $ curl -ks -X DELETE \
      -H "Authorization: Bearer ${MY_TOKEN}" \
      "${ALARMS_URL}/alarmSubscriptions/<subscription_id>"
    ```

    - Replace `<subscription_id>` with the subscription identifier returned when the subscription was created.

- After creating a subscription, verify it appears in the subscription list. Trigger a test alert on a managed cluster and confirm that your webhook endpoint receives the notification callback.
