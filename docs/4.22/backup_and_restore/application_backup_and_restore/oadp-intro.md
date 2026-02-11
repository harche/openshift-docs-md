The OpenShift API for Data Protection (OADP) product safeguards customer applications on OpenShift Container Platform. It offers comprehensive disaster recovery protection, covering OpenShift Container Platform applications, application-related cluster resources, persistent volumes, and internal images. OADP is also capable of backing up both containerized applications and virtual machines (VMs).

However, OADP does not serve as a disaster recovery solution for [etcd](../../backup_and_restore/control_plane_backup_and_restore/backing-up-etcd.xml#backup-etcd) or OpenShift Operators.

<div class="important">

OADP support is applicable to customer workload namespaces and cluster scope resources.

Full cluster [backup](../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/backing-up-applications.xml#backing-up-applications) and [restore](../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/restoring-applications.xml#restoring-applications) are not supported.

</div>

# OpenShift API for Data Protection APIs

OADP provides APIs that enable multiple approaches to customizing backups and preventing the inclusion of unnecessary or inappropriate resources.

OADP provides the following APIs:

- [Backup](../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/backing-up-applications.xml#backing-up-applications)

- [Restore](../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/restoring-applications.xml#restoring-applications)

- [Schedule](../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-scheduling-backups-doc.xml#oadp-scheduling-backups-doc)

- [BackupStorageLocation](../../backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.xml#oadp-about-backup-snapshot-locations_installing-oadp-aws)

- [VolumeSnapshotLocation](../../backup_and_restore/application_backup_and_restore/backing_up_and_restoring/oadp-backing-up-pvs-csi-doc.xml#oadp-backing-up-pvs-csi-doc)

## Support for OpenShift API for Data Protection

<table>
<caption>Supported versions of OADP</caption>
<colgroup>
<col style="width: 10%" />
<col style="width: 12%" />
<col style="width: 12%" />
<col style="width: 13%" />
<col style="width: 13%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Version</p></td>
<td style="text-align: left;"><p>OCP version</p></td>
<td style="text-align: left;"><p>General availability</p></td>
<td style="text-align: left;"><p>Full support ends</p></td>
<td style="text-align: left;"><p>Maintenance ends</p></td>
<td style="text-align: left;"><p>Extended Update Support (EUS)</p></td>
<td style="text-align: left;"><p>Extended Update Support Term 2 (EUS Term 2)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.5</p></td>
<td style="text-align: left;"><ul>
<li><p>4.19</p></li>
</ul></td>
<td style="text-align: left;"><p>17 June 2025</p></td>
<td style="text-align: left;"><p>Release of 1.6</p></td>
<td style="text-align: left;"><p>Release of 1.7</p></td>
<td style="text-align: left;"><p>EUS must be on OCP 4.20</p></td>
<td style="text-align: left;"><p>EUS Term 2 must be on OCP 4.20</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.4</p></td>
<td style="text-align: left;"><ul>
<li><p>4.14</p></li>
<li><p>4.15</p></li>
<li><p>4.16</p></li>
<li><p>4.17</p></li>
<li><p>4.18</p></li>
</ul></td>
<td style="text-align: left;"><p>10 Jul 2024</p></td>
<td style="text-align: left;"><p>Release of 1.5</p></td>
<td style="text-align: left;"><p>Release of 1.6</p></td>
<td style="text-align: left;"><p>27 Jun 2026</p>
<p>EUS must be on OCP 4.16</p></td>
<td style="text-align: left;"><p>27 Jun 2027</p>
<p>EUS Term 2 must be on OCP 4.16</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.3</p></td>
<td style="text-align: left;"><ul>
<li><p>4.12</p></li>
<li><p>4.13</p></li>
<li><p>4.14</p></li>
<li><p>4.15</p></li>
</ul></td>
<td style="text-align: left;"><p>29 Nov 2023</p></td>
<td style="text-align: left;"><p>10 Jul 2024</p></td>
<td style="text-align: left;"><p>Release of 1.5</p></td>
<td style="text-align: left;"><p>31 Oct 2025</p>
<p>EUS must be on OCP 4.14</p></td>
<td style="text-align: left;"><p>31 Oct 2026</p>
<p>EUS Term 2 must be on OCP 4.14</p></td>
</tr>
</tbody>
</table>

Supported versions of OADP

### Unsupported versions of the OADP Operator

|         |                      |                    |                   |
|---------|----------------------|--------------------|-------------------|
| Version | General availability | Full support ended | Maintenance ended |
| 1.2     | 14 Jun 2023          | 29 Nov 2023        | 10 Jul 2024       |
| 1.1     | 01 Sep 2022          | 14 Jun 2023        | 29 Nov 2023       |
| 1.0     | 09 Feb 2022          | 01 Sep 2022        | 14 Jun 2023       |

Previous versions of the OADP Operator which are no longer supported

For more details about EUS, see [Extended Update Support](https://access.redhat.com/support/policy/updates/openshift#eus).

For more details about EUS Term 2, see [Extended Update Support Term 2](https://access.redhat.com/support/policy/updates/openshift#eust2).

- [Backing up etcd](../../backup_and_restore/control_plane_backup_and_restore/backing-up-etcd.xml#backup-etcd)
