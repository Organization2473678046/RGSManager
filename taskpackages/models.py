# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
from django.db import models
from users.models import User



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'data/{0}/{1}/{2}/{3}/{4}'.format(datetime.now().strftime("%Y"),
                                             datetime.now().strftime("%m"),
                                             datetime.now().strftime("%d"),
                                             datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), filename)



@python_2_unicode_compatible
class TaskPackage(models.Model):
    """主任务包"""
    name = models.CharField(error_messages={"unique": u"任务包名称已存在"}, max_length=150, unique=True, verbose_name=u"任务包名称")
    owner = models.CharField(max_length=150, null=True, verbose_name=u"主版本作业员")
    exowner = models.CharField(max_length=150, null=True, verbose_name=u"前作业员")
    mapnums = models.CharField(max_length=65536, null=True, verbose_name=u"图号集")
    mapnumcounts = models.IntegerField(default=0, null=True, verbose_name=u"图幅数")
    file = models.FileField(upload_to=user_directory_path, null=True, verbose_name=u"任务包文件")
    status = models.CharField(max_length=10, default='0', verbose_name=u"任务包状态")
    describe = models.CharField(max_length=1000, null=True, verbose_name=u"描述信息")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    isdelete = models.BooleanField(default=False, verbose_name=u"逻辑删除")
    schedule = models.CharField(max_length=32, default=u"未指定状态",verbose_name=u"任务包进度")
    # 子任务包创建未查看的消息提醒
    newtaskpackagesonfornotice = models.IntegerField(default=0, null=True, verbose_name=u"消息提醒")
    reallyname = models.CharField(max_length=150, default=None, null=True, verbose_name=u"作业员真实姓名")

    class Meta:
        verbose_name = u"任务包"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TaskPackageSon(models.Model):
    """子任务包"""
    # TODO 改为大写，去下划线
    SCHEDULECHOICE = (
        (0, u'未指定状态'),
        (1, u'修改缝隙'),
        (2, u'河网环修改'),
        (3, u'有向点修改'),
        (4, u'一对多修改'),
        (5, u'匝道赋值'),
        (6, u'同层拓扑'),
        (7, u'不同层拓扑'),
        (8, u'微短线修改'),
        (9, u'微小面修改'),
        (10, u'急锐角修改'),
        (11, u'等高线拼接'),
        (12, u'完成')
    )

    taskpackage_name = models.CharField(max_length=150, null=True, verbose_name=u"主任务包名称")
    user_username = models.CharField(max_length=150, null=True, verbose_name=u"作业员")  # 子版本上传者
    version = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"子任务包版本号")
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name=u"任务包文件")
    describe = models.CharField(max_length=1000, null=True, blank=True, verbose_name=u"描述信息")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    isdelete = models.BooleanField(default=False, verbose_name=u"逻辑删除")
    schedule = models.IntegerField(choices=SCHEDULECHOICE, default=0, verbose_name=u"任务包进度")

    class Meta:
        verbose_name = u'子任务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


@python_2_unicode_compatible
class TaskPackageOwner(models.Model):
    """任务包拥有者"""
    taskpackage_name = models.CharField(max_length=150, null=True, verbose_name=u"主任务包名称")
    owner = models.CharField(max_length=150, verbose_name=u"作业员")
    exowner = models.CharField(max_length=150, null=True, blank=True, verbose_name=u"前作业员")
    describe = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"文件描述")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    isdelete = models.BooleanField(default=False, verbose_name=u"逻辑删除")

    class Meta:
        verbose_name = u'任务包归属'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner


@python_2_unicode_compatible
class EchartTaskPackage(models.Model):
    user_reallyname = models.CharField(unique=True,max_length=150, null=True, verbose_name=u"作业员")
    count = models.IntegerField(default=0, null=True, verbose_name=u"任务包数量")

    def __str__(self):
        return self.user_username


@python_2_unicode_compatible
class EchartSchedule(models.Model):
    taskpackage_schedule = models.CharField(unique=True,max_length=150,null=True, verbose_name=u"任务包处理进度")
    count = models.IntegerField(default=0, null=True, verbose_name=u"任务包数量")

    def __str__(self):
        return self.taskpackage_schedule
