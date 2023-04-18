from django.db import models


class VPS(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()


class FileUpload(models.Model):
    link = models.CharField(max_length=255)
    upload_duration = models.FloatField()
    upload_time = models.DateTimeField(auto_now_add=True)
    source_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='files_uploaded')


class FileDownload(models.Model):
    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='files_downloaded')
    download_duration = models.FloatField()
    download_time = models.DateTimeField(auto_now_add=True)
    source_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='files_downloaded')


class Replication(models.Model):
    source_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='replications_sent')
    dest_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='replications_received')
    # file = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='replications')
    link = models.CharField(max_length=255)
    transfer_time = models.DateTimeField(auto_now_add=True)
    transfer_duration = models.IntegerField()

