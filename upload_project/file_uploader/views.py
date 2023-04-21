from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect
import datetime
import os
from file_uploader.utils import Location, save_data, file_name, get_link_data, download
from file_uploader.tasks import replication
from file_uploader.models import FileUpload, VPS, FileDownload, Replication


def index(request):

    # Redirect user to the nearest vps
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        user_ip = user_ip.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    nearest_vps = Location().get_nearest_vps(user_ip)
    request.session['nearest_vps'] = nearest_vps

    return redirect(f'http://{nearest_vps.get("ip_address")}:8000/upload')


def upload_file(request):

    # Upload file to nearest vps

    nearest_vps = request.session.get('nearest_vps')

    if request.method == "POST":

        file_link = request.POST.get('data')

        file_basename = file_name(file_link)

        response = get_link_data(file_link)

        path = f"{os.path.abspath('file_uploader/uploads')}/{file_basename}"

        save_file = save_data(path, response)

        # Create file into source vps
        source_vps = VPS.objects.using(nearest_vps.get('ip_address')).filter(name=nearest_vps.get('vps_number')).first()

        FileUpload.objects.using(nearest_vps.get('ip_address')).create(link=file_basename,
                                                                       upload_duration=save_file.get('duration'),
                                                                       source_vps=source_vps)

        # Send data to celery task to make the replication to other servers

        replication.delay(nearest_vps, file_basename, os.environ.get('USERNAME'), os.environ.get('PASSWORD'), path)

        return redirect('files')

    if request.method == "GET":
        return render(request, 'file_upload.html')


def get_upload_files(request):

    nearest_vps = request.session.get('nearest_vps')

    # Get upload data to display for user
    context = {}
    upload_data = FileUpload.objects.using(nearest_vps.get('ip_address')).all()
    replica = Replication.objects.using(nearest_vps.get('ip_address')).all()
    united_data = sorted(chain(upload_data, replica), key=attrgetter('created_at'), reverse=True)

    context['data'] = united_data

    return render(request, 'file_upload_results.html', context)


def download_file(request, filename):

    # Download file from the nearest vps

    nearest_vps = request.session.get('nearest_vps')

    start_time = datetime.datetime.utcnow()

    file_path = os.path.join(f"{os.path.abspath('file_uploader/uploads')}", filename)

    response = download(file_path, filename)

    end_time = datetime.datetime.utcnow()

    duration = (end_time - start_time).total_seconds()

    # Save relevant information about download to db

    file = FileUpload.objects.using(nearest_vps.get('ip_address')).filter(link=filename).first()
    FileDownload.objects.using(nearest_vps.get('ip_address')).create(file=file,
                                                                     download_duration=duration,
                                                                     source_vps=file.source_vps)

    return response


def get_download_files(request):

    nearest_vps = request.session.get('nearest_vps')

    # Get download data to display for user

    context = {}
    download_data = FileDownload.objects.using(nearest_vps.get('ip_address')).order_by('-created_at').all()
    context['data'] = download_data

    return render(request, 'file_download_results.html', context)
