from django.urls import path
from .views import *

urlpatterns = [
    path("register/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("new/code/", GetNewCodeView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("change/info/", ChangeUserInfoView.as_view()),
]
