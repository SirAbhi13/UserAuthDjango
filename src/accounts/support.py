import random
import string

from rest_framework import status
from rest_framework.response import Response

from utils import db


def generate_unique_username(email):
    # Generate a random username from a combination of email and random characters
    random_chars = "".join(
        random.choices(string.ascii_lowercase, k=4)
    )  # Customize the length as needed
    username = email.split("@")[0] + random_chars

    # Check if the generated username already exists
    while db["user_profiles"].find_one({"username": username}):
        random_chars = "".join(
            random.choices(string.ascii_lowercase, k=4)
        )  # Generate new random characters
        username = email.split("@")[0] + random_chars

    return username


def check_username(username):
    if db["user_profiles"].find_one({"username": username}):
        return True
