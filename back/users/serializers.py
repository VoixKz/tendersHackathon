from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=True,
        max_length=128,
        write_only=True,
    )
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "role")


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "role")

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            role=validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, attrs):

        email_exists = CustomUser.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)
