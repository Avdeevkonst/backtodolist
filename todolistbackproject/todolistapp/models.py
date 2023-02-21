from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import jwt
from datetime import datetime, timedelta
from todolistbackproject import settings


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
    """
        The user manager used by django to create users
        as well as staff and superuser
    """
    use_in_migration = True

    def __save_and_return(self, user, password: str, is_staff: bool, is_superuser: bool):
        """
            Save the user inside the database by setting some values and
            using the default database
            :param user: The user model
            :param password: The stored password
            :param is_staff: boolean field to know if it's a staff user
            :param is_superuser: boolean field to know if the user is an administrator
        """
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

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.email,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
