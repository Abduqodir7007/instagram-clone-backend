from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import *
from users.utils import (
    check_email_or_phone_number,
    send_code_to_email,
    check_user_input,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignUpSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields["email_phone_number"] = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id"]

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)

        code = user.create_code(user.auth_type)
        if user.auth_type == VIA_EMAIL:
            send_code_to_email(user.email, code)
        if user.auth_type == VIA_PHONE:
            pass
        user.save()

        return user

    @staticmethod
    def auth_validate(data):

        input = data.get("email_phone_number")

        input_type = check_email_or_phone_number(input)
        if input_type == "email":
            data = {"email": input, "auth_type": VIA_EMAIL}
        elif input_type == "phone_number":
            data = {"phone_number": input, "auth_type": VIA_PHONE}
        else:
            data = {"success": False}

            raise ValidationError(data)
        return data

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    def validate_email_phone_number(self, value):
        if User.objects.filter(email=value).exists():
            data = {"msg": "This email already exists"}
            raise ValidationError(data)
        elif User.objects.filter(phone_number=value).exists():
            data = {"msg": "This phone number already exists"}

            raise ValidationError(data)

        return value

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class VerifyCodeViewSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        if not 4 < len(value) < 6:
            data = {"msg": "Invalid code"}
            raise ValidationError(data)

        return value


class LoginViewSerializer(TokenObtainPairSerializer):

    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(LoginViewSerializer, self).__init__(*args, **kwargs)
        self.fields["user_input"] = serializers.CharField(write_only=True)
        self.fields["username"] = serializers.CharField(write_only=True, required=False)

    def auth_validate(self, data):
        user_input = data.get("user_input")
        user_input_type = check_user_input(user_input)

        if user_input_type == "email":
            user = User.objects.get(email=user_input)
            username = user.username
        elif user_input_type == "phone_number":
            user = User.objects.get(phone_number=user_input)
            username = user.username
        elif user_input_type == "username":
            username = user_input
        else:
            data = {"success": False, "msg": "Invalid input"}
            raise ValidationError(data)
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            self.user = user
        else:
            raise ValidationError({"success": False, "msg": "Invalid credentials"})
        return user

    def validate(self, data):

        self.auth_validate(data)
        data = self.user.token()  # type : ignore   
        return data


class ChangeUserInfoViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            data = {"msg": "Passwords should be the same"}
            raise ValidationError(data)

        if password:
            validate_password(password)
            validate_password(confirm_password)

        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()

        return instance
