from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.support import check_username, generate_unique_username
from firebase_auth.authenticator import generate_custom_token
from utils import db

from .models import user_profiles
from .serializers import UserProfileSerializer


class RegisterView(APIView):
    parser_classes = [JSONParser, FormParser]

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            email = data["email"]
            password = data["password"]

            username = data.get("username")
            if not username:
                # Generate a random username from the email
                username = generate_unique_username(email)

            # Check if the username already exists in the MongoDB collection
            if check_username(username):
                return Response(
                    {"error": "A user with that username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the password is at least 8 characters long
            if len(password) < 8:
                return Response(
                    {
                        "error": "This password is too short. It must contain at least 8 characters"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the user profile in MongoDB
            user_profile = {
                "username": username,
                "email": email,
                "password": password,
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
            }
            db["user_profiles"].insert_one(user_profile)

            response_data = {"username": username, "email": email}
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    parser_classes = [JSONParser, FormParser]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = db["user_profiles"].find_one(
            {"username": username, "password": password}
        )

        if user:
            custom_token = generate_custom_token(user)

            # Return the custom token in the response
            response_data = {
                "username": user["username"],
                "email": user["email"],
                "full_name": f"{user['first_name']}-{user['last_name']}",
                "Authorization:": custom_token,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Username or password is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        user = db["user_profiles"].find_one(
            {"username": username, "password": password}
        )

        if user:
            custom_token = generate_custom_token(user)

            # Return the custom token in the response
            response_data = {
                "username": user["username"],
                "email": user["email"],
                "full_name": f"{user['first_name']}-{user['last_name']}",
                "Authorization:": custom_token,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Username or password is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileView(APIView):
    parser_classes = [JSONParser, FormParser]

    def get(self, request):
        # User is already authenticated and authorized by the middleware
        if request.query_params.get("username") is None:
            return Response(
                {"Errror": "username can't be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_profile = self.get_user_profile(request.query_params.get("username"))

        # Create a serializer instance to customize the response data
        # serializer = UserProfileSerializer(instance=user_profile)

        # Include the 'username' and 'email' fields in the response
        response_data = {
            "username": request.query_params.get("username"),
            "email": user_profile.get("email", ""),
            "full_name": f"{user_profile['first_name']}-{user_profile['last_name']}",
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_user_profile(self, username):
        user_profile = db["user_profiles"].find_one({"username": username})

        return user_profile


class ProfileEditView(APIView):
    parser_classes = [JSONParser, FormParser]

    def post(self, request):
        existing_username = request.data.get("username")
        user_profile = self.get_user_profile(existing_username)

        if not user_profile:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is trying to edit the username
        new_username = request.data.get("new_username")
        if new_username and check_username(new_username):
            return Response(
                {"error": f"User already exists with the username {new_username}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the user's profile with the provided data
        user_profile["first_name"] = request.data.get(
            "first_name", user_profile["first_name"]
        )
        user_profile["last_name"] = request.data.get(
            "last_name", user_profile["last_name"]
        )
        user_profile["username"] = (
            new_username if new_username else user_profile["username"]
        )

        # Save the updated profile data back to the database
        db["user_profiles"].update_one(
            {"username": existing_username}, {"$set": user_profile}
        )

        response_data = {
            "username": user_profile["username"],
            "email": user_profile["email"],
            "full_name": f"{user_profile['first_name']}-{user_profile['last_name']}",
        }

        # Redirect to the profile view after a successful edit
        return Response(response_data, status=status.HTTP_200_OK)

    def get_user_profile(self, username):
        user_profile = db["user_profiles"].find_one({"username": username})

        return user_profile
