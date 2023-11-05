from django.http import HttpResponseNotFound
from firebase_admin import auth

from .authenticator import verify_custom_token
from .exceptions import InvalidAuthToken, NoAuthToken


class CustomTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path == "/accounts/profile/edit/"
            or request.path == "/accounts/profile/view/"
        ):
            custom_token = request.headers.get("Custom-Token")
            if custom_token:
                try:
                    if verify_custom_token(custom_token):
                        return self.get_response(request)

                except Exception:
                    return HttpResponseNotFound("Error! Invalid auth token provided")

            else:
                return HttpResponseNotFound("Error! No auth token found!")
        return self.get_response(request)
