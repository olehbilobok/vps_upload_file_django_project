# Generated by Django 4.2 on 2023-04-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_uploader', '0002_rename_download_time_filedownload_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='link',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='replication',
            name='link',
            field=models.CharField(max_length=1000),
        ),
    ]
