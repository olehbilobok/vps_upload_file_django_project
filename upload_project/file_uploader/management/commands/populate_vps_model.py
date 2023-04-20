import os
from django.core.management.base import BaseCommand
from file_uploader.models import VPS
from file_uploader.vps import vps_list


class Command(BaseCommand):
    help = 'Populates the VPS model with initial data'

    # Populate the vps model with initial data

    def handle(self, *args, **options):

        # The parameter 'using' is depends on the server where the code is deployed and which db the server uses
        # North Bergen - 'USA_DB_HOST', Singapore - 'ASIA_DB_HOST', Frankfurt - 'EUROPE_DB_HOST'
        vpses = list(VPS.objects.using(os.environ.get('EUROPE_DB_HOST')).all())
        if not vpses:
            for vps in vps_list:
                VPS.objects.using(os.environ.get('EUROPE_DB_HOST')).create(name=vps.get('vps_number'),
                                                                           location=vps.get('city'),
                                                                           ip_address=vps.get('ip_address'))
