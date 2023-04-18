import datetime
import os
import time
import paramiko
from celery import Celery, shared_task
from file_uploader.vps import vps_list
from file_uploader.models import Replication, VPS


@shared_task()
def replication(nearest_vps, file,  username, password, file_location, destination):

    for vps in vps_list:
        if vps.get('ip_address') != nearest_vps.get('ip_address'):

            start_time = datetime.datetime.utcnow()

            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.RSAKey.from_private_key_file('/Users/olegbilobok/.ssh/id_rsa', password='oleh')
            ssh.connect(vps.get('ip_address'), username=username, pkey=key)
            sftp = ssh.open_sftp()
            sftp.put(file_location, f"{destination}/{file}")
            sftp.close()
            ssh.close()

            end_time = datetime.datetime.utcnow()

            transfer_duration = (end_time - start_time).total_seconds()

            dest_vps = VPS.objects.using(vps.get("ip_address")).filter(ip_address=vps.get("ip_address")).first()

            source_vps = VPS.objects.using(vps.get("ip_address")).\
                filter(ip_address=nearest_vps.get('ip_address')).first()

            Replication.objects.using(vps.get("ip_address")).create(source_vps=source_vps,
                                                                    dest_vps=dest_vps,
                                                                    link=file,
                                                                    transfer_duration=transfer_duration)
