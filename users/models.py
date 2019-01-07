# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class User(AbstractUser):
    isadmin = models.BooleanField(default=False, verbose_name=u"是否管理员")
    reallyname = models.CharField(max_length=150, default="未命名", null=True, verbose_name=u"真实姓名")

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

