from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


def avatar_upload_path(instance, filename):
    return f'avatars/{instance.username}/{filename}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, age, avatar=None, password=None):
        if not email:
            raise ValueError('Email is required!')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            age=age,
            avatar=avatar,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            username,
            age,
            avatar=None,
            password=None
            ):
        user = self.create_user(
            email=email,
            username=username,
            age=age,
            avatar=avatar,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class DarkLitUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    username = models.CharField(
        max_length=100,
        verbose_name='Username',
        unique=True,
        blank=False,
        null=False
    )
    age = models.IntegerField(
        verbose_name='User age',
        blank=False,
        null=False
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'age']

    def __str__(self):
        return self.username
