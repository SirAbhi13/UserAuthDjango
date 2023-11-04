from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import db

from .models import user_profiles
from .serializers import UserProfileSerializer


class RegisterView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            username = data["username"]
            email = data["email"]
            password = data["password"]
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")

            # Check if the username or email already exists in the MongoDB collection
            if db["user_profiles"].find_one(
                {"$or": [{"username": username}, {"email": email}]}
            ):
                return Response(
                    {"error": "A user with that username or email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the user profile in MongoDB
            user_profile = {
                "username": username,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            }
            db["user_profiles"].insert_one(user_profile)

            response_data = {"username": username, "email": email}
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
