# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import hashlib
import os
import shutil
import zipfile
from unrar import rarfile
from rest_framework import serializers
from rest_framework.exceptions import APIException
from RGSManager.settings import BASE_DIR
from celery_app.createregiontask import createregiontask
from celery_app.regionchunk import regionmerge
from models import TaskPackage, TaskPackageSon, TaskPackageOwner, EchartTaskPackage, EchartSchedule, \
    TaskPackageScheduleSet, RegionTask, RegionTaskChunk, RegionTaskMerge
from django.conf import settings
from rest_framework import status
from celery_app.clipfromsde import clipfromsde
from users.models import User
from django.conf import settings


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
            raise serializers.ValidationError(u"作业员 {} 不存在".format(owner))
        else:
            validated_data["reallyname"] = user.reallyname

        regiontask_name = validated_data.get("regiontask_name")
        try:
            regiontask = RegionTask.objects.get(name=regiontask_name)
        except RegionTask.DoesNotExist:
            raise serializers.ValidationError(u"任务区域 {} 不存在".format(regiontask_name))
        try:
            taskpackage = TaskPackage.objects.get(regiontask_name=regiontask_name, name=validated_data["name"])
        except:
            pass
        else:
            raise serializers.ValidationError(u"任务包名称 {} 已存在".format(validated_data["name"]))

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
        regiontask = RegionTask.objects.get(name=taskpackage.regiontask_name)
        mapindexsdepath = regiontask.mapindexsde
        rgssdepath = regiontask.rgssde
        # 进入celery进行作业包的异步裁切
        clipfromsde.delay(mapindexsdepath, rgssdepath, mapnumlist, MEDIA, taskname, taskpackage.id, taskpackageson.id)

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
            raise serializers.ValidationError(u"任务区域 {} 不存在".format(regiontask_name))

        taskpackage_name = validated_data.get("taskpackage_name")
        try:
            taskpackage = TaskPackage.objects.filter(isdelete=False).get(name=taskpackage_name,
                                                                         regiontask_name=regiontask_name)
        except TaskPackage.DoesNotExist:
            raise serializers.ValidationError(u"{0}名为 {1} 的任务包不存在".format(regiontask_name, taskpackage_name))
        else:
            user = self.context["request"].user
            # 只有管理员和主任务包拥有者才能上该任务包的子版本
            if not user.isadmin and user.username != taskpackage.owner:
                raise PermissionValidationError(u"用户 {} 无权限".format(user.username))
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
        regiontask_name = validated_data.get("regiontask_name")
        try:
            regiontask = RegionTask.objects.get(name=regiontask_name)
        except RegionTask.DoesNotExist:
            raise serializers.ValidationError(u"任务区域 {} 不存在".format(regiontask_name))

        taskpackage_name = validated_data.get("taskpackage_name")
        try:
            taskpackage = TaskPackage.objects.get(name=taskpackage_name, regiontask_name=regiontask_name)
        except TaskPackage.DoesNotExist:
            # raise serializers.ValidationError(u"任务包{}不存在".format(taskpackage_name))
            raise serializers.ValidationError(u"{0}名为 {1} 的任务包不存在".format(regiontask_name, taskpackage_name))
        else:
            if validated_data["owner"] == taskpackage.owner:
                raise serializers.ValidationError(u"该任务包已经在 {} 名下".format(validated_data["owner"]))

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



class EchartScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchartSchedule
        fields = ["taskpackage_schedule", "count", "regiontask_name"]


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackageScheduleSet
        fields = ["id", "schedule", "regiontask_name"]

    def validate(self, validated_data):
        # action = self.context["view"].action
        # if action == "create":
        #     try:
        #         TaskPackageScheduleSet.objects.get(schedule=attrs["schedule"], regiontask_name=attrs["regiontask_name"])
        #     except:
        #         pass
        #     else:
        #         raise serializers.ValidationError(
        #             "新增进度失败，区域“{0}”下进度“{1}”重复".format(attrs["regiontask_name"], attrs["schedule"]))
        #     return attrs
        # else:
        #     schedule_id = self.context["request"].parser_context["kwargs"]["pk"]
        #     try:
        #         instance = TaskPackageScheduleSet.objects.get(id=schedule_id)
        #         regiontask_name = instance.regiontask_name
        #         TaskPackageScheduleSet.objects.get(schedule=attrs["schedule"], regiontask_name=regiontask_name)
        #     except:
        #         pass
        #     else:
        #         raise serializers.ValidationError("修改进度失败，区域“{0}”下进度“{1}”重复".format(regiontask_name, attrs["schedule"]))
        #     return attrs

        # 防止同一个项目区域内,进度名字重复
        print self.context['view'].action
        schedule = validated_data.get("schedule")
        regiontask_name = validated_data.get("regiontask_name")

        print self.context['view'].kwargs
        if self.context['view'].action == 'update':
            id = self.context['view'].kwargs.get('pk')
            try:
                taskPackageschedule = TaskPackageScheduleSet.objects.get(id=id)
            except:
                pass
            else:
                regiontask_name = taskPackageschedule.regiontask_name

        print regiontask_name
        try:
            taskPackageschedule = TaskPackageScheduleSet.objects.get(schedule=schedule, regiontask_name=regiontask_name)
        except:
            pass
        else:
            raise serializers.ValidationError(u"{0} 名为 {1} 的进度已存在".format(regiontask_name, schedule))
        return validated_data


class RegionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionTask
        fields = ["id", "name", "file", "status", "basemapservice", "mapindexfeatureservice", "mapindexmapservice",
                  "mapindexschedulemapservice", "describe", "createtime"]
        extra_kwargs = {
            "basemapservice": {"read_only": True},
            "mapindexfeatureservice": {"read_only": True},
            "mapindexmapservice": {"read_only": True},
            "mapindexschedulemapservice": {"read_only": True},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
        }

    def create(self, validated_data):
        regiontask = RegionTask.objects.create(**validated_data)
        return regiontask

    def update(self, instance, validated_data):
        regiontask = super(RegionTaskSerializer, self).update(instance, validated_data)
        print regiontask.file.path

        createregiontask.delay(regiontask.id, regiontask.file.path, regiontask.name)
        return regiontask


class RegionTaskChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionTaskChunk
        fields = ["file", "chunk", "chunks", "filemd5", "chunkmd5", "name"]

    def create(self, validated_data):
        instance = RegionTaskChunk.objects.create(name=validated_data["name"],
                                                  file=self.context['request'].data.get('file'),
                                                  # file=validated_data["file"],
                                                  chunk=validated_data["chunk"],
                                                  chunks=validated_data["chunks"],
                                                  filemd5=validated_data["filemd5"],
                                                  chunkmd5=validated_data["chunkmd5"]
                                                  )

        name = instance.name
        chunk = instance.chunk
        path = instance.file.path
        filemd5 = instance.filemd5
        chunks = instance.chunks
        # chunkmd5 = instance.chunkmd5
        # regionchunk.delay(path, chunkmd5, name, chunk)
        # 检验文件块md5
        if os.path.isfile(instance.file.path):
            myhash = hashlib.md5()
            f = open(instance.file.path, 'rb')
            while True:
                b = f.read(8096)
                if not b:
                    break
                myhash.update(b)
            f.close()
            if myhash.hexdigest() == instance.chunkmd5:
                # print u"文件切片MD5校验通过"
                pass
            else:
                path = instance.file.path.split("\\")
                path.pop()
                file_path = "\\".join(path)  # 读取文件块路径
                shutil.rmtree(file_path)
                instance.delete()
                raise serializers.ValidationError("区域:{0};文件切片编号:{1};MD5校验错误".format(name, chunk))
                # print u"文件切片MD5校验错误"
        else:
            instance.delete()

            raise serializers.ValidationError("区域:{0};文件切片编号:{1};切片上传失败".format(name, chunk))
            # print u"文件不存在"

        # 合并文件
        if validated_data["chunk"] == validated_data["chunks"] - 1:
            regionmerge.delay(path, filemd5, name, chunks)
            # path_list = os.path.join(BASE_DIR, instance.file.path).split("\\")
            # path_list.pop()
            # fromdir = "\\".join(path_list)  # 读取文件块路径
            # filename = instance.name  # 合成后文件名字
            # save_path = os.path.join(BASE_DIR, u'media\\file\\{0}\\{1}\\{2}\\{3}'.format(
            #     datetime.now().strftime("%Y"),
            #     datetime.now().strftime("%m"),
            #     datetime.now().strftime("%d"),
            #     instance.name))  # 合成后存放路径
            # if not os.path.exists(save_path):  # 判断文件夹是否存在
            #     os.makedirs(save_path)
            # outfile = open(os.path.join(save_path, filename), 'wb')  # 打开合并后存储文件夹
            # num = 0
            # files = RegionTaskChunk.objects.filter(name=instance.name).order_by("chunk")  # 读取文件块名字并根据块数排序
            # while num < instance.chunks:  # 判断合并文件次数
            #     file = files.values_list("file")[num][0].split("/")[-1]  # 获取单个文件名
            #     filepath = os.path.join(fromdir, file)
            #     infile = open(filepath, 'rb')
            #     data = infile.read()
            #     outfile.write(data)
            #     del data
            #     num += 1
            #     infile.close()
            # outfile.close()
            #
            # # 校验合并后文件md5
            # file = save_path + "\\" + filename  # 获取合并后文件路径
            # if os.path.isfile(file):  # 判断文件是否存在
            #     myhash = hashlib.md5()
            #     f = open(file, 'rb')
            #     while True:
            #         b = f.read(8096)
            #         if not b:
            #             break
            #         myhash.update(b)
            #     f.close()
            #     print myhash.hexdigest()
            #     if myhash.hexdigest() == instance.filemd5:  # 判断MD5是否与前端传的数据一致
            #         print u"合成后MD5校验通过"
            #         pass
            #     else:
            #         shutil.rmtree(save_path)
            #         shutil.rmtree(fromdir)
            #         print u"合成后MD5校验错误"
            #         raise serializers.ValidationError("文件{0}MD5校验错误".format(instance.name))
            # else:
            #     raise serializers.ValidationError("文件{0}切片丢失".format(instance.name))
            #     # print u"文件不存在"
            #
            #
            # try:
            #     # 创建合成后文件表记录
            #     instance_merge = RegionTaskMerge.objects.create(name=instance.name, md5=instance.filemd5)
            #     instance_merge.file = file
            #     instance_merge.save()
            # except:
            #     shutil.rmtree(fromdir)
            #     shutil.rmtree(save_path)
            #     print "合成记录表错误"
            #     raise serializers.ValidationError("“{0}”合成记录数据错误".format(instance.name))
            #
            # try:
            # # 创建地图区域文件表记录
            #     instance_regiontask = RegionTask.objects.get(name=instance.name)
            #     instance_regiontask.file = file
            #     instance_regiontask.md5 = instance.filemd5
            #     instance_regiontask.save()
            # except:
            #     shutil.rmtree(save_path)
            #     shutil.rmtree(fromdir)
            #     print "地区区域记录表错误"
            #     raise serializers.ValidationError("“{0}”地图区域记录修改失败".format(instance.name))

        return instance

































"""
class TaskPackageChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackageChunk
        fields = ["taskpackage_name", "file", "chunk", "chunks", "file_md5", "chunk_md5", "version", "describe",
                  "user_username", "schedule", "regiontask_name"]

        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "user_username": {"read_only": True, "help_text": u"子任务包归属者"},
            "version": {"read_only": True},
            "file": {"required": True, "allow_null": False, "error_messages": {"required": u"请选择文件"}},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "updatetime": {"format": '%Y-%m-%d %H:%M:%S'},
            "regiontask_name": {"required": True}
        }

    def validate(self, validated_data):

        return validated_data

    def create(self, validated_data):
        instance = TaskPackageChunk.objects.create(taskpackage_name=validated_data["taskpackage_name"],
                                                   file_chunk=self.context['request'].data.get('file'),
                                                   # file_chunk=validated_data["file"],
                                                   chunk=validated_data["chunk"],
                                                   chunks=validated_data["chunks"],
                                                   file_md5=validated_data["file_md5"],
                                                   chunk_md5=validated_data["chunk_md5"],
                                                   describe=validated_data["describe"],
                                                   user_username=validated_data["user_username"],
                                                   schedule=validated_data["schedule"],
                                                   regiontask_name=validated_data["regiontask_name"]
                                                   )
        taskpackageson_nums = TaskPackageSon.objects.filter(taskpackage_name=instance.name,
                                                            regiontask_name=instance.regiontask_name).count()
        instance.version = "v" + str(taskpackageson_nums) + ".0"
        instance.save()

        name = instance.taskpackage_name
        chunk = instance.chunk
        regiontask_name = instance.regiontask_name

        # 检验文件块md5
        if os.path.isfile(instance.file.path):
            myhash = hashlib.md5()
            f = open(instance.file.path, 'rb')
            while True:
                b = f.read(8096)
                if not b:
                    break
                myhash.update(b)
            f.close()
            print myhash.hexdigest()
            if myhash.hexdigest() == instance.chunk_md5:
                # print u"文件切片MD5校验通过"
                pass
            else:
                instance.delete()
                raise serializers.ValidationError("区域:{0};名称:{1};文件切片编号:{2};MD5校验错误".format(name, chunk, regiontask_name))
                # print u"文件切片MD5校验错误"
        else:
            instance.delete()

            raise serializers.ValidationError("区域:{0};名称:{1};文件切片编号:{2};切片上传失败".format(name, chunk, regiontask_name))
            # print u"文件不存在"

        # 合并文件
        if validated_data["chunk"] == validated_data["chunks"] - 1:
            path_list = os.path.join(BASE_DIR, instance.file.path).split("\\")
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
                file = files.values_list("file")[num][0].split("/")[-1]  # 获取单个文件名
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
                    # print u"MD5校验通过"
                    pass
                else:
                    raise serializers.ValidationError("文件{0}合并错误".format(instance.name))
                    # print u"MD5校验错误"
            else:
                raise serializers.ValidationError("文件{0}切片丢失".format(instance.name))
                # print u"文件不存在"

            path = u'file/{0}/{1}/{2}/{3}'.format(datetime.now().strftime("%m"),
                                                  datetime.now().strftime("%d"),
                                                  instance.name,
                                                  instance.name)
            # 创建合成后文件表记录
            instance_merge = TaskPackageSonMerge.objects.create(taskpackage_name=instance.name,
                                                                user_username=instance.user_username,
                                                                version=instance.version,
                                                                schedule=instance.schedule,
                                                                describe=instance.describe,
                                                                regiontask_name=instance.regiontask_name,
                                                                md5=instance.file_md5)
            instance_merge.file = path
            instance_merge.save()

            # 创建子版本表记录
            instance_son = TaskPackageSon.objects.create(taskpackage_name=instance.name,
                                                         md5=instance.file_md5,
                                                         )
            instance_son.file = path
            instance_son.save()

            # 修改主任务包信息

        return instance
"""
