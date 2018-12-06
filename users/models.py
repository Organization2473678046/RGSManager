# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Users(AbstractUser):
    role = models.BooleanField(default=False, verbose_name=u"角色")

    class Meta:
        db_table = 'tb_users'
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
