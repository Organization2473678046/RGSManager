# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import APIException
from models import TaskPackage, TaskPackageSon, TaskPackageOwner, EchartTaskPackage, EchartSchedule, \
    TaskPackageScheduleSet, RegionTask
from django.conf import settings
from rest_framework import status
from celery_app.clipfromsde import clipfromsde
from users.models import User


class PermissionValidationError(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class TaskPackageSerializer(serializers.ModelSerializer):
    exreallyname = serializers.SerializerMethodField(label=u"前任作业员真实姓名")

    class Meta:
        model = TaskPackage
        fields = ["id", "name", "owner", "exowner", "mapnums", "mapnumcounts", "file", "status", "createtime",
                  "updatetime", "describe", "schedule", "exreallyname", "reallyname", "newtaskpackagesonfornotice",
                  "regiontask_name"]
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
            "newtaskpackagesonfornotice": {"required": False, "read_only": True},
            "regiontask_name": {"required": True}
        }

    def get_exreallyname(self, obj):
        username = obj.exowner
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
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

        regiontask_name = validated_data.get("regiontask_name")
        try:
            regiontask = RegionTask.objects.get(name=regiontask_name)
        except RegionTask.DoesNotExist:
            raise serializers.ValidationError(u"任务区域不存在")

        return validated_data

    def create(self, validated_data):
        taskpackage = super(TaskPackageSerializer, self).create(validated_data)
        # taskpackage = TaskPackage.objects.create(**validated_data)
        # taskpackage = TaskPackage(**validated_data)
        taskpackageson = TaskPackageSon.objects.create(
            taskpackage_name=taskpackage.name,
            version="v0.0",
            describe=taskpackage.describe,
            user_username=taskpackage.owner,
            file=taskpackage.file,
            regiontask_name=taskpackage.regiontask_name,
        )

        MEDIA = settings.MEDIA_ROOT
        mapnumlist = validated_data["mapnums"]
        taskname = validated_data["name"]
        # 进入celery进行作业包的异步裁切
        clipfromsde.delay(mapnumlist, MEDIA, taskname, taskpackage.id, taskpackageson.id)

        return taskpackage


# class ScheduleChoiceField(serializers.ChoiceField):
#     """自定义序列化器返回choice字段"""
#
#     def to_representation(self, obj):
#         return self._choices[obj]


class TaskPackageSonSerializer(serializers.ModelSerializer):
    handle_progress = serializers.BooleanField(allow_null=True)
    taskpackage_file_id = serializers.IntegerField(allow_null=True)
    # schedule = ScheduleChoiceField(choices=SCHEDULE_CHOICE, label=u"任务包处理进度")
    reallyname = serializers.SerializerMethodField(label=u"作业员真实姓名")

    class Meta:
        model = TaskPackageSon
        fields = ["taskpackage_name", "version", "createtime", "updatetime", "describe", "file", "user_username",
                  "handle_progress", "taskpackage_file_id", "schedule", "reallyname", "regiontask_name"]
        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "user_username": {"read_only": True, "help_text": u"子任务包归属者"},
            "version": {"read_only": True},
            "file": {"required": True, "allow_null": False, "error_messages": {"required": u"请选择文件"}},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "updatetime": {"format": '%Y-%m-%d %H:%M:%S'},
            # "handle_progress":{"required": False},
            # "taskpackage_file_id":{"required": False},
            "regiontask_name": {"required": True}
        }

    def get_reallyname(self, obj):
        username = obj.user_username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        reallyname = user.reallyname
        return reallyname

    def validate(self, validated_data):
        regiontask_name = validated_data.get("regiontask_name")
        try:
            regiontask = RegionTask.objects.get(name=regiontask_name)
        except RegionTask.DoesNotExist:
            raise serializers.ValidationError(u"任务区域不存在")

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
        regiontask_name = validated_data["regiontask_name"]
        taskpackageson_nums = TaskPackageSon.objects.filter(taskpackage_name=taskpackage.name,
                                                            regiontask_name=regiontask_name).count()
        version = "v" + str(taskpackageson_nums) + ".0"

        taskpackageson = TaskPackageSon.objects.create(
            taskpackage_name=validated_data["taskpackage_name"],
            user_username=validated_data["user_username"],
            version=version,
            file=validated_data["file"],
            describe=validated_data["describe"],
            schedule=validated_data["schedule"],
            regiontask_name=regiontask_name
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
        fields = ["id", "taskpackage_name", "owner", "exowner", "createtime", "describe", "reallyname", "exreallyname",
                  "regiontask_name"]
        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "owner": {"required": True, "allow_null": False, "help_text": u"要@的作业员"},
            "exowner": {"read_only": True},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "regiontask_name": {"required": True}
        }

    def get_reallyname(self, obj):
        username = obj.owner
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        reallyname = user.reallyname
        return reallyname

    def get_exreallyname(self, obj):
        username = obj.exowner
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        exreallyname = user.reallyname
        return exreallyname

    def validate(self, validated_data):
        taskpackage_name = validated_data.get("taskpackage_name")
        regiontask_name = validated_data.get("regiontask_name")
        try:
            taskpackage = TaskPackage.objects.get(name=taskpackage_name, regiontask_name=regiontask_name)
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
            describe=validated_data["describe"],
            regiontask_name=validated_data["regiontask_name"]
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
        fields = ["user_reallyname", "count", "regiontask_name"]
        # extra_kwargs={
        #     "regiontask_name": {"required": True}
        # }


class EchartScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchartSchedule
        fields = ["taskpackage_schedule", "count", "regiontask_name"]


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackageScheduleSet
        fields = ["id", "schedule", "regiontask_name"]


class RegionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionTask
        fields = '__all__'
        extra_kwargs = {
            "basemapservice": {"read_only": True},
            "mapindexfeatureservice": {"read_only": True},
            "mapindexmapservice": {"read_only": True},
            "mapindexschedulemapservice": {"read_only": True},
        }
