from django.db import models


class VPS(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self):
        return f"id: {self.id}, name: {self.name}, location: {self.location}, ip_address: {self.ip_address}"


class FileUpload(models.Model):
    link = models.CharField(max_length=255)
    upload_duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    source_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='files_uploaded')

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self):
        return f"id: {self.id}, link: {self.link}, upload_duration: {self.upload_duration}," \
               f"source_vps: {self.source_vps}"


class FileDownload(models.Model):
    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='files_downloaded')
    download_duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    source_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='files_downloaded')

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self):
        return f"id: {self.id}, file: {self.file}, download_duration: {self.download_duration}," \
               f"source_vps: {self.source_vps}"


class Replication(models.Model):
    source_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='replications_sent')
    dest_vps = models.ForeignKey(VPS, on_delete=models.CASCADE, related_name='replications_received')
    # file = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='replications')
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    transfer_duration = models.IntegerField()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self):
        return f"id: {self.id}, source_vps: {self.source_vps}, dest_vps: {self.dest_vps}, link: {self.link}," \
               f"transfer_duration: {self.transfer_duration}"
