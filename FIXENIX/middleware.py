from django.http import HttpResponsePermanentRedirect

class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        # Redirect from www to non-www
        if host.startswith("www."):
            new_url = request.build_absolute_uri().replace("www.", "", 1)
            return HttpResponsePermanentRedirect(new_url)

        # Redirect from non-www to www (if needed, swap the condition)
        # if not host.startswith("www."):
        #     new_url = request.build_absolute_uri().replace("://", "://www.", 1)
        #     return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)
