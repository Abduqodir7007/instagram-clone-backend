from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, AllowAny


class SignUpView(CreateAPIView):
    authentication_class = [
        AllowAny,
    ]
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class VerifyCodeView(APIView):
    authentication_class = [
        IsAuthenticated,
    ]
    serializer_class = VerifyCodeViewSerializer

    def post(self, request):
        user = request.user
        serializer = VerifyCodeViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get("code")  # type: ignore
        self.check_code(user, code)
        token = user.token()

        data = {
            "success": True,
            "access": str(token["access"]),
            "refresh": str(token["refresh"]),
        }

        return Response(data)

    @staticmethod
    def check_code(user, code):
        valid_code = user.codes.filter(
            is_confirmed=False, expiration_time__gte=datetime.now(), code=code
        )

        if not valid_code.exists():
            data = {"message": "Tasdiqlash kodingiz xato yoki eskirgan"}
            raise ValidationError(data)
        else:
            valid_code.update(is_confirmed=True)

        if user.auth_status == NEW:
            user.auth_status = CODE_VEREFIED
            user.save()

        return True


class GetNewCodeView(APIView):
    def get(self, request):
        user = request.user
        self.check_code_exists(user)
        code = user.create_code(user.auth_type)
        send_code_to_email(user.email, code)
        data = {"msg": "New code sent"}
        return Response(data)

    @staticmethod
    def check_code_exists(user):
        curr_code = user.codes.filter(
            user=user, expiration_time__gte=datetime.now(), is_confirmed=False
        )
        if curr_code.exists():
            data = {"msg": "You have valid code use it."}
            raise ValidationError(data)


class LoginView(TokenObtainPairView):
    serializer_class = LoginViewSerializer
