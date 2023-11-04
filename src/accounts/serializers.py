from rest_framework import serializers


def check_length(value):
    if len(value) > 100:
        raise serializers.ValidationError("Only 100 characters are allowed for a field")


def check_required(value):
    if value is None:
        raise serializers.ValidationError("Email and password are required.")


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100, required=False, allow_blank=True, validators=[check_length]
    )
    email = serializers.EmailField(
        max_length=100, required=True, validators=[check_length, check_required]
    )
    password = serializers.CharField(
        max_length=100, required=True, validators=[check_length, check_required]
    )
    first_name = serializers.CharField(
        max_length=100, required=False, allow_blank=True, validators=[check_length]
    )
    last_name = serializers.CharField(
        max_length=100, required=False, allow_blank=True, validators=[check_length]
    )
