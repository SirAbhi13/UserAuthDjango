from distutils.command.check import check

from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.support import check_username, generate_unique_username
from utils import db

from .models import user_profiles
from .serializers import UserProfileSerializer


class RegisterView(APIView):
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
