# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os
from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import APIException

from RGSManager.settings import BASE_DIR
from models import TaskPackage, TaskPackageSon, TaskPackageOwner, EchartTaskPackage, EchartSchedule, \
    TaskPackageScheduleSet, TaskPackageChunk, TaskPackageSonMerge
from django.conf import settings
from rest_framework import status
from celery_app.clipfromsde import clipfromsde
from users.models import User


class PermissionValidationError(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class TaskPackageSerializer(serializers.ModelSerializer):
    exreallyname = serializers.SerializerMethodField(label=u"真实姓名")

    # reallyname = serializers.SerializerMethodField(label=u"真实姓名")

    class Meta:
        model = TaskPackage

        fields = ["id", "name", "owner", "exowner", "mapnums", "mapnumcounts", "file", "status", "createtime",
                  "updatetime", "describe", "schedule", "exreallyname", "reallyname", "newtaskpackagesonfornotice"]
        extra_kwargs = {
            "name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "owner": {"required": True, "allow_null": False, "help_text": u"作业员"},
            "exowner": {"read_only": True},
            "mapnums": {"required": True, "write_only": True,
                        "error_messages": {"required": u"请输入图号"}, "help_text": u"图号"},
            "mapnumcounts": {"required": True},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "updatetime": {"format": '%Y-%m-%d %H:%M:%S'},
            "describe": {"allow_null": False},
            # "reallyname":{"required": False},
            "newtaskpackagesonfornotice": {"required": False, "read_only": True}
        }

    # def get_reallyname(self, obj):
    #     username = obj.owner
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist as e:
    #         return None
    #     reallyname = user.reallyname
    #     return reallyname

    def get_exreallyname(self, obj):
        username = obj.exowner
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            return None
        exreallyname = user.reallyname
        return exreallyname

    def validate(self, validated_data):
        owner = validated_data.get("owner")
        try:
            user = User.objects.get(username=owner)
        except User.DoesNotExist:
            raise serializers.ValidationError("作业员不存在")
        else:
            validated_data["reallyname"] = user.reallyname

        return validated_data

    def create(self, validated_data):
        # print validated_data
        taskpackage = super(TaskPackageSerializer, self).create(validated_data)

        taskpackageson = TaskPackageSon.objects.create(
            taskpackage_name=taskpackage.name,
            version="v0.0",
            describe=taskpackage.describe,
            user_username=taskpackage.owner,
            file=taskpackage.file
        )

        MEDIA = settings.MEDIA_ROOT
        mapnumlist = validated_data["mapnums"]
        taskname = validated_data["name"]
        # 进入celery进行作业包的异步裁切
        clipfromsde.delay(mapnumlist, MEDIA, taskname, taskpackage.id, taskpackageson.id)

        return taskpackage


class ScheduleChoiceField(serializers.ChoiceField):
    """自定义序列化器返回choice字段"""

    def to_representation(self, obj):
        return self._choices[obj]


class TaskPackageSonSerializer(serializers.ModelSerializer):
    handle_progress = serializers.BooleanField(allow_null=True)
    taskpackage_file_id = serializers.IntegerField(allow_null=True)
    # schedule = ScheduleChoiceField(choices=SCHEDULE_CHOICE, label=u"任务包处理进度")
    reallyname = serializers.SerializerMethodField(label=u"作业员真实姓名")

    class Meta:
        model = TaskPackageSon
        fields = ["taskpackage_name", "version", "createtime", "updatetime", "describe", "file", "user_username",
                  "handle_progress", "taskpackage_file_id", "schedule", "reallyname"]
        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "user_username": {"read_only": True, "help_text": u"子任务包归属者"},
            "version": {"read_only": True},
            "file": {"required": True, "allow_null": False, "error_messages": {"required": u"请选择文件"}},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "updatetime": {"format": '%Y-%m-%d %H:%M:%S'},
            # "handle_progress":{"required": False},
            # "taskpackage_file_id":{"required": False},
            # "schedule": {"allow_null": False, "help_text": u"任务包进度"}

        }

    def get_reallyname(self, obj):
        username = obj.user_username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            return None
        reallyname = user.reallyname
        return reallyname

    def validate(self, validated_data):

        taskpackage_name = validated_data.get("taskpackage_name")
        try:
            taskpackage = TaskPackage.objects.filter(isdelete=False).get(name=taskpackage_name)
        except TaskPackage.DoesNotExist:
            raise serializers.ValidationError(u"任务包{}不存在".format(taskpackage_name))
        else:
            user = self.context["request"].user
            # 只有管理员和主任务包拥有者才能上该任务包的子版本
            if not user.isadmin and user.username != taskpackage.owner:
                raise PermissionValidationError(u"用户{}无权限".format(user.username))

            validated_data["user_username"] = user.username
            validated_data["taskpackage"] = taskpackage

        return validated_data

    def create(self, validated_data):
        taskpackage = validated_data["taskpackage"]
        taskpackageson_nums = TaskPackageSon.objects.filter(taskpackage_name=taskpackage.name).count()
        version = "v" + str(taskpackageson_nums) + ".0"

        taskpackageson = TaskPackageSon.objects.create(
            taskpackage_name=validated_data["taskpackage_name"],
            user_username=validated_data["user_username"],
            version=version,
            file=validated_data["file"],
            describe=validated_data["describe"],
            schedule=validated_data["schedule"]
        )
        # 将主任务包的file字段,改成最新的子任务包的file,主任务包file字段展示最新的子版本
        taskpackage.file = taskpackageson.file
        taskpackage.describe = taskpackageson.describe
        taskpackage.schedule = taskpackageson.schedule
        taskpackage.newtaskpackagesonfornotice += 1
        taskpackage.updatetime = taskpackageson.createtime
        taskpackage.save()

        return taskpackageson


class TaskPackageOwnerSerializer(serializers.ModelSerializer):
    exreallyname = serializers.SerializerMethodField(label=u"真实姓名")
    reallyname = serializers.SerializerMethodField(label=u"真实姓名")

    class Meta:
        model = TaskPackageOwner
        fields = ["id", "taskpackage_name", "owner", "exowner", "createtime", "describe", "reallyname", "exreallyname"]
        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "owner": {"required": True, "allow_null": False, "help_text": u"要@的作业员"},
            "exowner": {"read_only": True},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
        }

    def get_reallyname(self, obj):
        username = obj.owner
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            return None
        reallyname = user.reallyname
        return reallyname

    def get_exreallyname(self, obj):
        username = obj.exowner
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            return None
        exreallyname = user.reallyname
        return exreallyname

    def validate(self, validated_data):
        taskpackage_name = validated_data.get("taskpackage_name")
        try:
            taskpackage = TaskPackage.objects.get(name=taskpackage_name)
        except TaskPackage.DoesNotExist:
            raise serializers.ValidationError(u"任务包{}不存在".format(taskpackage_name))
        else:
            if validated_data["owner"] == taskpackage.owner:
                raise serializers.ValidationError(u"该任务包已经在{}名下".format(validated_data["owner"]))

            validated_data["taskpackage"] = taskpackage
            validated_data["exowner"] = taskpackage.owner

        return validated_data

    def create(self, validated_data):
        taskpackage = validated_data["taskpackage"]
        taskpackageowner = TaskPackageOwner.objects.create(
            taskpackage_name=validated_data["taskpackage_name"],
            owner=validated_data["owner"],
            exowner=validated_data["exowner"],
            describe=validated_data["describe"]
        )

        taskpackage.exowner = taskpackage.owner
        taskpackage.owner = validated_data["owner"]
        user = User.objects.get(username=taskpackage.owner)
        taskpackage.reallyname = user.reallyname
        taskpackage.save()

        return taskpackageowner


class EchartTaskpackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchartTaskPackage
        fields = ["user_reallyname", "count"]


class EchartScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchartSchedule
        fields = ["taskpackage_schedule", "count"]


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackageScheduleSet
        fields = ["id", "schedule"]


class TaskPackageChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackageChunk
        fields = ["name", "file_chunk", "chunk", "chunks", "file_md5", "chunk_md5"]

    def create(self, validated_data):
        instance = TaskPackageChunk.objects.create(name=validated_data["name"],
                                                   # file_chunk=self.context['request'].data.get('file'),
                                                   file_chunk=validated_data["file_chunk"],
                                                   chunk=validated_data["chunk"],
                                                   chunks=validated_data["chunks"],
                                                   file_md5=validated_data["file_md5"],
                                                   chunk_md5=validated_data["chunk_md5"]
                                                   )
        # 检验文件块md5
        if os.path.isfile(instance.file_chunk.path):
            myhash = hashlib.md5()
            f = open(instance.file_chunk.path, 'rb')
            while True:
                b = f.read(8096)
                if not b:
                    break
                myhash.update(b)
            f.close()
            print myhash.hexdigest()
            if myhash.hexdigest() == instance.chunk_md5:
                print u"文件切片MD5校验通过"
            else:
                print u"文件切片MD5校验错误"
        else:
            print u"文件不存在"

        # 合并文件
        if validated_data["chunk"] == validated_data["chunks"] - 1:
            path_list = os.path.join(BASE_DIR, instance.file_chunk.path).split("\\")
            path_list.pop()
            fromdir = "\\".join(path_list)  # 读取文件块路径
            filename = instance.name  # 合成后文件名字
            save_path = os.path.join(BASE_DIR, u'media\\file\\{0}\\{1}\\{2}'.format(
                datetime.now().strftime("%m"),
                datetime.now().strftime("%d"),
                instance.name))  # 合成后存放路径
            if not os.path.exists(save_path):  # 判断文件夹是否存在
                os.makedirs(save_path)
            outfile = open(os.path.join(save_path, filename), 'wb')  # 打开合并后存储文件夹
            num = 0
            files = TaskPackageChunk.objects.filter(name=instance.name).order_by("chunk")  # 读取文件块名字并根据块数排序
            while num < instance.chunks:  # 判断合并文件次数
                file = files.values_list("file_chunk")[num][0].split("/")[-1]  # 获取单个文件名
                filepath = os.path.join(fromdir, file)
                infile = open(filepath, 'rb')
                data = infile.read()
                outfile.write(data)
                del data
                num += 1
                infile.close()
            outfile.close()

            # 校验合并后文件md5
            file = save_path + "\\" + filename  # 获取合并后文件路径
            if os.path.isfile(file):  # 判断文件是否存在
                myhash = hashlib.md5()
                f = open(file, 'rb')
                while True:
                    b = f.read(8096)
                    if not b:
                        break
                    myhash.update(b)
                f.close()
                print myhash.hexdigest()
                if myhash.hexdigest() == instance.file_md5:  # 判断MD5是否与前端传的数据一致
                    print u"MD5校验通过"
                else:
                    print u"MD5校验错误"
            else:
                print u"文件不存在"
            path = u'file/{0}/{1}/{2}/{3}'.format(datetime.now().strftime("%m"),
                                                  datetime.now().strftime("%d"),
                                                  instance.name,
                                                  instance.name)
            # 创建合成后文件表记录
            instance_merge = TaskPackageSonMerge.objects.create(taskpackage_name=instance.name,
                                                                md5=instance.file_md5)
            instance_merge.file = path
            instance_merge.save()

            # 创建子版本表记录
            instance_son = TaskPackageSon.objects.create(taskpackage_name=instance.name,
                                                         md5=instance.file_md5)
            instance_son.file=path
            instance_son.save()
        return instance

