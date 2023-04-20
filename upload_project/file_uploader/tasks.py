import datetime
import paramiko
from celery import shared_task
from file_uploader.vps import vps_list
from file_uploader.models import Replication, VPS


@shared_task()
def replication(nearest_vps, file,  username, password, path):

    for vps in vps_list:
        if vps.get('ip_address') != nearest_vps.get('ip_address'):

            start_time = datetime.datetime.utcnow()

            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.RSAKey.from_private_key_file('root/.ssh/id_rsa', password=password)
            ssh.connect(vps.get('ip_address'), username=username, pkey=key)
            sftp = ssh.open_sftp()
            sftp.put(path, f"{path}/{file}")
            sftp.close()
            ssh.close()

            end_time = datetime.datetime.utcnow()

            transfer_duration = (end_time - start_time).total_seconds()

            destination_vps = VPS.objects.using(vps.get("ip_address")).filter(ip_address=vps.get("ip_address")).first()

            source_vps = VPS.objects.using(vps.get("ip_address")).\
                filter(ip_address=nearest_vps.get('ip_address')).first()

            Replication.objects.using(vps.get("ip_address")).create(source_vps=source_vps,
                                                                    dest_vps=destination_vps,
                                                                    link=file,
                                                                    transfer_duration=transfer_duration)
