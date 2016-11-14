
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db import models


class BackupUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password=None):
        user = self.model(
            email=email, username=username)
        user.set_password(password)
        user.is_active = True
        return user

    def create_superuser(self, username, email,
                         is_staff, is_superuser, password):
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()
        return user


class BackupUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="User", max_length=50, unique=True)
    email = models.EmailField(
        verbose_name=(u'E-mail'),
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True)

    full_name = models.CharField(
        verbose_name='Full name', max_length=100,
        null=True, blank=True)

    short_name = models.CharField(
        verbose_name='Short Name', max_length=50,
        null=True, blank=True)

    is_staff = models.BooleanField(
        verbose_name=('Is staff ?'), default=False)

    is_active = models.BooleanField(
        verbose_name=(u'Is active ?'), default=True)

    created_at = models.DateTimeField(
        verbose_name=(u'Created at'), default=timezone.now)

    last_access = models.DateTimeField(
        verbose_name=(u'Last Acess'),
        default=timezone.now)

    objects = BackupUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_superuser', 'is_staff']

    class Meta:
        verbose_name = (u'User')
        verbose_name_plural = (u'Users')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.username
