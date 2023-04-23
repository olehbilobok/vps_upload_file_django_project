import datetime
import requests
import uuid
from django.http import HttpResponse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from file_uploader.vps import vps_list


def measure_time(func):

    # Decorator which tracks the time of file uploading and downloading

    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.utcnow()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.utcnow()
        return {'result': result,
                'end_time': end_time,
                'duration': (end_time - start_time).total_seconds()}

    return wrapper


@measure_time
def save_data(path, data):

    # Save file to the uploads directory

    try:
        with open(path, 'wb') as file:
            for chunk in data.iter_content(chunk_size=2000):
                file.write(chunk)

    except FileNotFoundError:
        print(f"Error: File '{path.split('/')[-1]}' not found.")
    except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Error: Network error occurred while saving file.")


def file_name(file_link):

    # Create the unique name for the file

    return str(uuid.uuid4()) + '_' + file_link.split('/')[-1]


def get_link_data(file_link):

    # Get data from the user's link

    try:
        return requests.get(file_link, stream=True)
    except requests.exceptions.ConnectionError as e:
        print(f"ConnectionError: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout: {e}")


def download(path, filename):

    with open(path, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class Location:

    # Define the user, vps locations and the nearest vps to the user

    @staticmethod
    def get_location(ip):

        try:
            geolocator = Nominatim(user_agent="file_uploader")
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            if response.status_code == 200:
                data = response.json()
                location = geolocator.reverse(f"{data['loc']}")
                return location.latitude, location.longitude
        except Exception as e:
            print(e)
            return None

    def get_user_location(self, ip):
        user_location = self.get_location(ip)
        return user_location

    def get_vps_location(self):
        vps_locations = []
        for ip in vps_list:
            location = self.get_location(ip.get('ip_address'))
            if location:
                vps_locations.append(
                    {
                        'vps_number': ip.get('vps_number'),
                        'city': ip.get('city'),
                        'ip_address': ip.get('ip_address'),
                        'location': location
                    }
                )
        return vps_locations

    def get_nearest_vps(self, ip):

        user_location = self.get_user_location(ip)
        vps_locations = self.get_vps_location()

        # Get the shortest distance between file location and vps location

        distance = [{'vps_number': vps.get('vps_number'),
                     'city': vps.get('city'),
                     'ip_address': vps.get('ip_address'),
                     'distance': geodesic(user_location, vps.get('location')).km} for vps in vps_locations]
        nearest_vps = min(distance, key=lambda x: x['distance'])

        return nearest_vps
