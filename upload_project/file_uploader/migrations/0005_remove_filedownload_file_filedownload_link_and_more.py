# Generated by Django 4.2 on 2023-04-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_uploader', '0004_alter_replication_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedownload',
            name='file',
        ),
        migrations.AddField(
            model_name='filedownload',
            name='link',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='replication',
            name='link',
            field=models.CharField(max_length=1000),
        ),
    ]
