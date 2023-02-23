from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from datetime import datetime, timedelta
from todolistbackproject import settings
import json


class TodoListModel(models.Model):

    STATUS_CHOICE = [
        ('C', 'Created'), ('P', 'In progress'), ('D', 'Done')
    ]

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE, default='C', max_length=100)
    owner = models.ForeignKey('UserModel', related_name='tasks', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class UserManager(BaseUserManager):
    use_in_migration = True

    def __save_and_return(self, user, password: str, is_staff: bool, is_superuser: bool):
        try:
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError:
            return None

    def create_user(self, email: str, password: str = None, is_superuser: bool = False):

        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email)
        return self.__save_and_return(user=user, password=password,
                                      is_superuser=is_superuser, is_staff=False)

    def create_staffuser(self, email: str, password: str):
        user = self.create_user(email=email, password=password)
        return self.__save_and_return(user=user, password=password, is_superuser=False, is_staff=True)

    def create_superuser(self, email: str, password: str):
        user = self.create_user(email=email, password=password)
        return self.__save_and_return(user=user, password=password, is_superuser=True, is_staff=True)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
        Define the model of the user
    """
    objects = UserManager()

    username = None
    email = models.EmailField('email address', unique=True)
    is_ban = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    # def token(self):
    #     refresh = RefreshToken.for_user(self)
    #     token = {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }
    #     return token
              