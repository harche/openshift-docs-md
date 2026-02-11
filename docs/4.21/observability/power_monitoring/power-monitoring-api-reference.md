<div class="important">

Power monitoring is a Technology Preview feature only. Technology Preview features are not supported with Red Hat production service level agreements (SLAs) and might not be functionally complete. Red Hat does not recommend using them in production. These features provide early access to upcoming product features, enabling customers to test functionality and provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview features, see [Technology Preview Features Support Scope](https://access.redhat.com/support/offerings/techpreview/).

</div>

PowerMonitor is the Schema for the PowerMonitor API.

# PowerMonitoring API specifications

PowerMonitor

PowerMonitor is the schema for the PowerMonitor API.

| Name           | Type                                                                            | Description                                     | Required   |
|----------------|---------------------------------------------------------------------------------|-------------------------------------------------|------------|
| **apiVersion** | string                                                                          | kepler.system.sustainable.computing.io/v1alpha1 | true       |
| **kind**       | string                                                                          | PowerMonitor                                    | true       |
| object         | Refer to the Kubernetes API documentation for the fields of the metadata field. | true                                            | **spec**   |
| object         | PowerMonitorSpec defines the desired state of Power Monitor                     | false                                           | **status** |

## PowerMonitor.spec

PowerMonitorSpec defines the desired state of Power Monitor

| Name       | Type   | Description | Required |
|------------|--------|-------------|----------|
| **kepler** | object |             | true     |

## PowerMonitor.status.conditions

<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 57%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Name</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Required</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>lastTransitionTime</strong></p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>The last time the condition transitioned from one status to another. This should be when the underlying condition changed. If that is not known, then using the time when the API field changed is acceptable.<br />
Format: date-time</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>message</strong></p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>A human-readable message indicating details about the transition. This may be an empty string.</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>reason</strong></p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>Contains a programmatic identifier indicating the reason for the condition’s last transition.</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>status</strong></p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>The status of the condition, which can be one of True, False, or Unknown.</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>type</strong></p></td>
<td style="text-align: left;"><p>string</p></td>
<td style="text-align: left;"><p>The type of Kepler Condition, such as Reconciled or Available.</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>observedGeneration</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>Represents the .metadata.generation that the condition was set based upon. For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date.<br />
Format: int64<br />
Minimum: 0</p></td>
<td style="text-align: left;"><p>false</p></td>
</tr>
</tbody>
</table>

## PowerMonitor.status.kepler

<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 57%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Name</th>
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Description</th>
<th style="text-align: left;">Required</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>currentNumberScheduled</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The number of nodes that are running at least one power-monitor pod and are supposed to run it.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>desiredNumberScheduled</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The total number of nodes that should be running the power-monitor pod.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>numberMisscheduled</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The number of nodes running the power-monitor pod that are not supposed to.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>numberReady</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The number of nodes that should be running the power-monitor pod and have at least one pod with a Ready condition.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>true</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>numberAvailable</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The number of nodes that should be running the power-monitor pod and have at least one pod running and available.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>false</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>numberUnavailable</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The number of nodes that should be running the power-monitor pod but have no pods running and available.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>false</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>updatedNumberScheduled</strong></p></td>
<td style="text-align: left;"><p>integer</p></td>
<td style="text-align: left;"><p>The total number of nodes that are running an updated power-monitor pod.<br />
Format: int32</p></td>
<td style="text-align: left;"><p>false</p></td>
</tr>
</tbody>
</table>
