from django.http import FileResponse
from django.shortcuts import render, redirect
import datetime
import os
from file_uploader.utils import Location, save_data, file_name, get_link_data, log_data, read_log_data, download
from file_uploader.vps import vps_list
from file_uploader.tasks import replication
from file_uploader.models import FileUpload, VPS, FileDownload, Replication


proxies = {
    'usa': '168.11.52.41',
    'europe': '161.97.97.155',
    'asia': '103.162.51.117'
}


def index(request):

    # Redirect user to the nearest vps
    # user_ip = request.remote_addr

    nearest_vps = Location().get_nearest_vps(proxies['europe'])
    # request.session.clear()
    # request.session['nearest_vps'] = nearest_vps

    # return redirect(f'http://{nearest_vps.get("ip_address")}/upload')
    return redirect('upload')


def upload_file(request):

    # Upload file to nearest vps

    # user_ip = request.remote_addr
    # nearest_vps = request.session.get('nearest_vps')
    nearest_vps = Location().get_nearest_vps(proxies['europe'])

    if request.method == "POST":

        file_link = request.POST.get('data')

        file_basename = file_name(file_link)

        response = get_link_data(file_link)

        path = f"{os.path.abspath('file_uploader/uploads')}/{file_basename}"

        save_file = save_data(path, response)

        # Write info about vps to VPS model to db on each server
        vps = VPS.objects.all()
        if not vps:
            for ip in [vps.get('ip_address') for vps in vps_list]:
                for vps in vps_list:
                    VPS.objects.using(ip).create(name=vps.get('vps_number'),
                                                 location=vps.get('city'),
                                                 ip_address=vps.get('ip_address'))

        # Create file into source vps

        source_vps = VPS.objects.using(nearest_vps.get('ip_address')).filter(name=nearest_vps.get('vps_number')).first()
        print('s_v', source_vps)
        file = FileUpload.objects.using(nearest_vps.get('ip_address')).create(link=file_basename,
                                                                              upload_duration=save_file.get('duration'),
                                                                              source_vps=source_vps)
        print(file)

        # log_info = {
        #     'vps_number': nearest_vps.get('vps_number'),
        #     'vps_city': nearest_vps.get('city'),
        #     'vps_ip': nearest_vps.get('ip_address'),
        #     'upload_duration': save_file.get('duration'),
        #     'upload_time': save_file.get('end_time').strftime('%Y-%m-%d %H:%M:%S'),
        #     'download_link': file_basename
        # }
        #
        # log_data('uploads.log', log_info)

        # Send file for the replication

        # for vps in vps_list:
        #     if vps.get('ip_address') != nearest_vps.get('ip_address'):
        #         replication.delay(vps.get('ip_address'), 'root', 'oleh', path, path)

        # Send data to celery task to make the replication to other servers

        replication.delay(nearest_vps, file_basename, 'root', 'oleh', path, '/root/test')

        return redirect('files')

    if request.method == "GET":
        return render(request, 'file_upload.html')


def get_upload_files(request):

    nearest_vps = Location().get_nearest_vps(proxies['europe'])

    # Get upload logs to display fo user
    context = {}
    # display_data = read_log_data(f"{os.path.abspath('uploads.log')}")
    # context['data'] = display_data

    upload_data = FileUpload.objects.using(nearest_vps.get('ip_address')).all()
    context['data'] = upload_data

    return render(request, 'file_upload_results.html', context)


def download_file(request, filename):

    # Download file from the nearest vps

    # nearest_vps = request.session.get('nearest_vps')
    nearest_vps = Location().get_nearest_vps(proxies['europe'])

    start_time = datetime.datetime.utcnow()

    file_path = os.path.join(f"{os.path.abspath('file_uploader/uploads')}", filename)

    response = download(file_path, filename)

    end_time = datetime.datetime.utcnow()

    duration = (end_time - start_time).total_seconds()

    # Log relevant information about download

    file = FileUpload.objects.using(nearest_vps.get('ip_address')).filter(link=filename).first()
    FileDownload.objects.using(nearest_vps.get('ip_address')).create(file=file, download_duration=duration, source_vps=file.source_vps)


    # log_info = {
    #     'vps_number': nearest_vps.get('vps_number'),
    #     'vps_city': nearest_vps.get('city'),
    #     'vps_ip': nearest_vps.get('ip_address'),
    #     'download_duration': duration,
    #     'download_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
    #     'downloaded_file': filename
    # }
    #
    # log_data('downloads.log', log_info)

    return response


def get_download_files(request):
    nearest_vps = Location().get_nearest_vps(proxies['europe'])

    # Get download logs to display for user
    context = {}
    # display_data = read_log_data(f"{os.path.abspath('downloads.log')}")
    # context['data'] = display_data
    download_data = FileDownload.objects.using(nearest_vps.get('ip_address')).all()
    context['data'] = download_data

    return render(request, 'file_download_results.html', context)

