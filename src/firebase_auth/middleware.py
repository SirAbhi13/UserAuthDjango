from exceptions import InvalidAuthToken, NoAuthToken
from firebase_admin import auth


class CustomTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        custom_token = request.headers.get("custom-token")

        if custom_token:
            try:
                decoded_token = auth.verify_id_token(custom_token)
                request.user = decoded_token  # Set the user in the request object if the token is valid
            except Exception:
                raise InvalidAuthToken("Invalid auth token")

        else:
            raise NoAuthToken("No auth token provided")

        return self.get_response(request)
