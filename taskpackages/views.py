# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import threading

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from taskpackages.models import TaskPackage, TaskPackageSon, TaskPackageOwner, EchartTaskPackage, EchartSchedule, \
    TaskPackageScheduleSet, RegionTask
from users.models import User
from utils.permission import AdminPerssion
from .serializers import TaskPackageSerializer, TaskPackageSonSerializer, TaskPackageOwnerSerializer, \
    EchartTaskpackageSerializer, EchartScheduleSerializer, ScheduleSerializer, RegionTaskSerializer, EchartTaskpackageSerializer, EchartScheduleSerializer, ScheduleSerializer, RegionTaskSerializer



class TaskPackagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 50
    page_query_param = 'page'


class TaskPackageSonPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10
    page_query_param = 'page'


class TaskPackageOwnerPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10
    page_query_param = 'page'


class SchedulePagination(PageNumberPagination):
    page_size = 9999
    page_size_query_param = 'limit'
    max_page_size = 9999
    page_query_param = 'page'


class RegionTaskPagination(PageNumberPagination):
    page_size = 9999
    page_size_query_param = 'limit'
    max_page_size = 9999
    page_query_param = 'page'

    # def get_page_size(self, request):
    #     if self.page_size_query_param:
    #         try:
    #             return _positive_int(
    #                 request.query_params[self.page_size_query_param],
    #                 strict=True,
    #                 cutoff=self.max_page_size
    #             )
    #         except (KeyError, ValueError):
    #             pass
    #
    #     return self.page_size


class TaskPackageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list: 查询所有任务包
    create: 划分任务包,需要前端传递任务包区域
    """
    pagination_class = TaskPackagePagination
    serializer_class = TaskPackageSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # filter_backends = [SearchFilter, OrderingFilter]
    # filter_fields = ["describe", "name", "owner", "schedule","regiontask_name"]
    ordering_fields = ("id", "name", "owner", "mapnumcounts", "updatetime", "newtaskpackagesonfornotice")
    ordering = ("-newtaskpackagesonfornotice",)
    search_fields = ('describe', 'name', 'owner', "mapnums", 'schedule', 'reallyname')

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), AdminPerssion()]

        return [IsAuthenticated()]

    def get_queryset(self):
        # 超时判断
        regiontask_name = self.request.query_params.get("regiontask_name")
        taskpackages = TaskPackage.objects.filter(regiontask_name=regiontask_name)
        for taskpackage in taskpackages:
            taskpackage_owner = TaskPackageOwner.objects.filter(taskpackage_name=taskpackage.name,
                                                                regiontask_name=regiontask_name,
                                                                isdelete=False).order_by("-createtime").first()
            if taskpackage_owner is not None:
                if taskpackage_owner.endtime < datetime.now():
                    taskpackage_owner.isoverdue = True
                    taskpackage_owner.save()
                    taskpackage.isoverdue = True
                    taskpackage.save()

        # 访问接口文档时,会访问这个函数,此时request is None,如果加了过滤之后,访问接口文档时会报警告
        # UserWarning: <class 'taskpackages.views.TaskPackageViewSet'> is not compatible with schema generation
        #   "{} is not compatible with schema generation".format(view.__class__)
        # print self.request
        # 防止访问接口文档时报警告
        if self.request is not None:
            user = self.request.user
            if self.action == 'list':
                if user.isadmin:
                    # return TaskPackage.objects.filter(regiontask_name=regiontask_name, isdelete=False).order_by("id")
                    return TaskPackage.objects.filter(regiontask_name=regiontask_name, isdelete=False)
                else:
                    # return TaskPackage.objects.filter(regiontask_name=regiontask_name, owner=user.username,
                    #                                   isdelete=False).order_by("id")
                    return TaskPackage.objects.filter(regiontask_name=regiontask_name, owner=user.username,
                                                      isdelete=False)
            return None
        return []


class TaskPackageSonViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list:根据主任务包名字,返回所有子任务包
    create:上传子任务包
    """

    pagination_class = TaskPackageSonPagination
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPackageSonSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            taskpackage_name = self.request.query_params.get("taskpackage_name")
            regiontask_name = self.request.query_params.get("regiontask_name")
            try:
                taskpackage = TaskPackage.objects.get(name=taskpackage_name, regiontask_name=regiontask_name)
                if taskpackage.newtaskpackagesonfornotice != 0 and user.isadmin:
                    taskpackage.newtaskpackagesonfornotice = 0
                    taskpackage.save()
            except TaskPackage.DoesNotExist:
                return []
            # try:
            #     taskpackage = TaskPackage.objects.get(name=taskpackage_name)
            # except TaskPackage.DoesNotExist:
            #     return []
            else:
                if user.isadmin:
                    return TaskPackageSon.objects.filter(taskpackage_name=taskpackage.name,
                                                         regiontask_name=regiontask_name, isdelete=False)
                else:
                    # 非管理员只能查看自己名下任务包的子版本
                    if user.username == taskpackage.owner:
                        return TaskPackageSon.objects.filter(taskpackage_name=taskpackage.name,
                                                             regiontask_name=regiontask_name, isdelete=False)
                    else:
                        return []
        return None


class TaskPackageOwnerViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    list: 获取@记录
    create: @功能
    """
    pagination_class = TaskPackageOwnerPagination
    serializer_class = TaskPackageOwnerSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]

        return [IsAuthenticated(), AdminPerssion()]

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            taskpackage_name = self.request.query_params.get("taskpackage_name")
            regiontask_name = self.request.query_params.get("regiontask_name")
            try:
                taskpackage = TaskPackage.objects.get(name=taskpackage_name, regiontask_name=regiontask_name)
            except TaskPackage.DoesNotExist:
                return []
            else:
                if user.isadmin:
                    return TaskPackageOwner.objects.filter(isdelete=False, taskpackage_name=taskpackage.name,
                                                           regiontask_name=regiontask_name)
                else:
                    return TaskPackageOwner.objects.filter(owner=user.username, taskpackage_name=taskpackage.name,
                                                           regiontask_name=regiontask_name,
                                                           isdelete=False)
        return None


class EchartTaskpackageViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    list: 图表数据获取（用户所对应任务包数量）
    """
    permission_classes = [IsAuthenticated]
    queryset = EchartTaskPackage.objects.filter(count__gt=0)
    serializer_class = EchartTaskpackageSerializer

    def list(self, request, *args, **kwargs):
        regiontask_name = self.request.query_params.get("regiontask_name")
        if not regiontask_name:
            return Response(u"请选择任务区域", status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.all()
        for user in users:
            count = TaskPackage.objects.filter(owner=user.username, regiontask_name=regiontask_name).count()
            try:
                echarttaskpackage = EchartTaskPackage.objects.get(user_reallyname=user.reallyname,
                                                                  regiontask_name=regiontask_name)
            except EchartTaskPackage.DoesNotExist:
                EchartTaskPackage.objects.create(user_reallyname=user.reallyname, regiontask_name=regiontask_name,
                                                 count=count)
            else:
                echarttaskpackage.count = count
                echarttaskpackage.save()

        echarttaskpackages = self.get_queryset().filter(regiontask_name=regiontask_name)
        serializer = self.get_serializer(echarttaskpackages, many=True)

        return Response(serializer.data)


class EchartScheduleViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    list: 图表数据获取（进度所对应任务包数量）
    """
    permission_classes = [IsAuthenticated]
    queryset = EchartSchedule.objects.filter(count__gt=0)
    serializer_class = EchartScheduleSerializer

    def list(self, request, *args, **kwargs):
        regiontask_name = self.request.query_params.get("regiontask_name")
        if not regiontask_name:
            return Response(u"请选择任务区域", status=status.HTTP_400_BAD_REQUEST)

        # time.sleep(60)
        # schedules = [schedule.schedule for schedule in TaskPackageScheduleSet.objects.filter(regiontask_name=regiontask_name)]
        schedules = TaskPackageScheduleSet.objects.filter(regiontask_name=regiontask_name)

        schedules = [schedule.schedule for schedule in
                     TaskPackageScheduleSet.objects.filter(regiontask_name=regiontask_name)] + [u'未指定状态']

        for schedule in schedules:
            count = TaskPackage.objects.filter(schedule=schedule.schedule, regiontask_name=regiontask_name).count()
            try:
                echartschedule = EchartSchedule.objects.get(taskpackage_schedule=schedule,
                                                            regiontask_name=regiontask_name)
            except:
                EchartSchedule.objects.create(taskpackage_schedule=schedule, count=count,
                                              regiontask_name=regiontask_name)
            else:
                echartschedule.count = count
                echartschedule.save()

        echartschedules = self.get_queryset().filter(regiontask_name=regiontask_name)
        serializer = self.get_serializer(echartschedules, many=True)

        return Response(serializer.data)


class ScheduleViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    list: 根据任务区域查询对应的进度
    create: 创建进度
    update: 修改进度
    destroy: 删除进度
    """
    serializer_class = ScheduleSerializer
    pagination_class = SchedulePagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ("id", "schedule")
    ordering = ("id",)
    search_fields = ("id", "schedule")

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        return [IsAuthenticated(), AdminPerssion()]

    def get_queryset(self):
        if self.action == "list":
            regiontask_name = self.request.query_params.get("regiontask_name")
            return TaskPackageScheduleSet.objects.filter(regiontask_name=regiontask_name)
        else:
            return TaskPackageScheduleSet.objects.all()


class RegionTaskView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    list: 获取所有任务区域;如果传递了区域名字regiontask_name参数,则值返回对应区域的信息
    create: 创建任务区域
    update: 更新任务区域信息
    """
    serializer_class = RegionTaskSerializer
    pagination_class = RegionTaskPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ("id", "name", 'status', 'describe', 'createtime')
    ordering = ("id",)
    search_fields = ("id", "name", 'status', 'describe', 'createtime')

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        return [IsAuthenticated(), AdminPerssion()]

    def get_queryset(self):
        if self.action == "list":
            regiontask_name = self.request.query_params.get("regiontask_name")
            if regiontask_name:
                return RegionTask.objects.filter(name=regiontask_name)
            else:
                return RegionTask.objects.all()
        elif self.action == "update":
            return RegionTask.objects.all()
        else:
            return None





# 超期提醒管理员
class OverdueViewSetAdmin(GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPackageOwnerSerializer

    def get_queryset(self):
        regiontask_name = self.request.query_params.get("regiontask_name")
        taskpackages = TaskPackage.objects.all()
        for taskpackage in taskpackages:
            taskpackage_owner = TaskPackageOwner.objects.filter(taskpackage_name=taskpackage.name,
                                                                regiontask_name=regiontask_name).order_by(
                "-createtime").first()
            if taskpackage_owner is not None:
                if taskpackage_owner.endtime < datetime.now():
                    if taskpackage_owner.isoverdue is not True:
                        taskpackage_owner.isoverdue = True
                        taskpackage_owner.save()
                        taskpackage.isoverdue = True
                        taskpackage.save()

        taskpackage = TaskPackage.objects.get(id=int(self.request.query_params.get("id")))
        return TaskPackageOwner.objects.filter(taskpackage_name=taskpackage.name,
                                               regiontask_name=taskpackage.regiontask_name,
                                               isdelete=False).order_by("-createtime")


class OverdueViewSetWorker(GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPackageOwnerSerializer
    pagination_class = TaskPackagePagination

    def get_queryset(self):
        user = self.request.user
        taskpackages = TaskPackage.objects.all()
        for taskpackage in taskpackages:
            taskpackage_owner = TaskPackageOwner.objects.filter(taskpackage_name=taskpackage.name).order_by(
                "-createtime").first()
            if taskpackage_owner is not None:
                if taskpackage_owner.endtime < datetime.now():
                    if taskpackage_owner.isoverdue is not True:
                        taskpackage_owner.isoverdue = True
                        taskpackage_owner.save()
                        taskpackage.isoverdue = True
                        taskpackage.save()

        taskpackages = TaskPackage.objects.filter(isoverdue=True, owner=user.username)
        taskpackageowner_list = []
        for taskpackage in taskpackages:
            taskpackage__owner = TaskPackageOwner.objects.filter(taskpackage_name=taskpackage.name).order_by(
                "-createtime").first()
            taskpackageowner_list.append(taskpackage__owner)
        return taskpackageowner_list


# 根据图幅号返回具体作业包的信息
class TaskpackageData(GenericViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated, AdminPerssion]
    serializer_class = TaskPackageOwnerSerializer

    def get_queryset(self):
        regiontask_name = self.request.query_params.get("regiontask_name")
        mapnum = self.request.query_params.get("mapnum")

        if self.action == "list":
            if mapnum and regiontask_name is not None:
                taskpackage = TaskPackage.objects.filter(mapnums__icontains=mapnum).first()
                taskpackage_owner = TaskPackageOwner.objects.filter(isdelete=False, regiontask_name=regiontask_name,
                                                taskpackage_name=taskpackage.name).order_by("-createtime").first()
                if taskpackage_owner is not None:
                    return [taskpackage_owner]
        else:
            return None


"""
>>>>>>> V0.10
class RegionTaskChunkUploadView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    
    
    # 分块上传文件
    
    # permission_classes = [IsAuthenticated, AdminPerssion]
    serializer_class = RegionTaskChunkSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        return [IsAuthenticated(), AdminPerssion()]

    def get_queryset(self):
        if self.action == "list":
            regiontask_name = self.request.query_params.get("regiontask_name")
            if regiontask_name:
                return RegionTaskChunk.objects.filter(name=regiontask_name).order_by('id')
            else:
                return RegionTaskChunk.objects.all().order_by('id')
        else:
            return None
"""

"""
# 子任务包文件分块上传
class TaskPackageChunkViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = TaskPackageChunk.objects.all()
    serializer_class = TaskPackageChunkSerializer
"""
