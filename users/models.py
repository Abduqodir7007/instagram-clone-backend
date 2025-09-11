import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.validators import RegexValidator
from datetime import timedelta, datetime
from rest_framework_simplejwt.tokens import RefreshToken

EXPIRATION_TIME = 3

VIA_EMAIL, VIA_PHONE = "via_email", "via_phone"
NEW, CODE_VEREFIED, DONE, PHOTO = "new", "code_verefied", "done", "photo"


class BaseModel(models.Model):
    id = models.UUIDField(
        unique=True, default=uuid.uuid4(), editable=False, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VEREFIED, CODE_VEREFIED),
        (DONE, DONE),
        (PHOTO, PHOTO),
    )

    phone_number = models.CharField(
        max_length=255,
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
        blank=True,
        null=True,
        unique=True,
    )
    auth_type = models.CharField(choices=AUTH_TYPE, null=True, blank=True)
    auth_status = models.CharField(choices=AUTH_STATUS, default=NEW)
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def create_code(self, auth_type):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(5)])
        UserConfirmation.objects.create(
            code=code, user_id=self.id, verify_type =auth_type
        )
        return code

    def check_username(self):
        if not self.username:
            self.username = f"instagram_{str(uuid.uuid4()).split('-')[-1]}"
            while User.objects.filter(username=self.username).exists():
                self.username = f"{self.username}{random.randint(0,9)}"

    def check_pass(self):
        if not self.password:
            self.password = f"instagram_{str(uuid.uuid4()).split('-')[-1]}"

    def hash_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def token(self):
        token = RefreshToken.for_user(self)
        data = {"access": str(token.access_token), "refresh": str(token)}

        return data

    def clean(self) -> None:

        self.check_username()
        self.check_pass()
        self.hash_password()

    def save(self, *args, **kwargs):

        self.clean()
        super(User, self).save(*args, **kwargs)


class UserConfirmation(BaseModel):

    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL),
    )
    verify_type = models.CharField(choices=TYPE_CHOICES, null=True, blank=True)
    code = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="codes")
    expiration_time = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
        super(UserConfirmation, self).save(*args, **kwargs)
