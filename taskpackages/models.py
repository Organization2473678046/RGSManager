# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from users.models import Users
import datetime


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.user.id, datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), filename)


@python_2_unicode_compatible
class TaskPackage(models.Model):
    name = models.CharField(max_length=128, verbose_name=u"任务包名称")
    user = models.ForeignKey(Users, related_name='taskpackage', null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name=u"作业员")
    mapnums = models.CharField(max_length=65536, null=True, blank=True, verbose_name=u"图号")
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name=u"任务包路径")
    status = models.CharField(max_length=16, default=u'0', verbose_name=u"任务包状态")
    is_delete = models.BooleanField(default=False, verbose_name=u"逻辑删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    describe = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"文件描述")

    class Meta:
        db_table = 'tb_taskpackage'
        verbose_name = u"任务包名称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.filename


class TaskPackageVersion(models.Model):
    version = models.CharField(max_length=16, default='v1.0', verbose_name=u"版本号")
    taskpackage = models.ForeignKey(TaskPackage, related_name='taskpackageversion', blank=True,
                                         on_delete=models.SET_NULL, verbose_name=u"任务包名称")
    is_delete = models.BooleanField(default=False, verbose_name=u"逻辑删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    describe = models.CharField(max_length=256, null=True, blank=True, verbose_name=u"文件描述")
    file = models.FileField(upload_to=user_directory_path, verbose_name=u"任务包路径")

    class Meta:
        db_table = 'tb_taskpackageversion'
        verbose_name = u'任务包版本'
        verbose_name_plural = verbose_name
