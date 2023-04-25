from file_uploader.utils import Location


class NearestVPSMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            user_ip = user_ip.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        request.nearest_vps = Location().get_nearest_vps(user_ip)

        response = self.get_response(request)

        return response
