# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from taskpackages.models import TaskPackage, TaskPackageSon, TaskPackageOwner, EchartTaskPackage, EchartSchedule, \
    TaskPackageScheduleSet, TaskPackageChunk
from users.models import User
from utils.permission import AdminPerssion
from .serializers import TaskPackageSerializer, TaskPackageSonSerializer, TaskPackageOwnerSerializer, \
    EchartTaskpackageSerializer, EchartScheduleSerializer, ScheduleSerializer, TaskPackageChunkSerializer


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


class TaskPackageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list: 查询所有任务包
    create: 划分任务包
    """
    pagination_class = TaskPackagePagination
    serializer_class = TaskPackageSerializer
    # filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ("id", "name", "owner", "mapnumcounts", "updatetime", "newtaskpackagesonfornotice")
    ordering = ("-newtaskpackagesonfornotice")
    # filter_fields = ["describe", "name", "owner", "schedule"]
    search_fields = ('describe', 'name', 'owner', 'schedule', 'reallyname')

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), AdminPerssion()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if user.isadmin:
                return TaskPackage.objects.filter(isdelete=False)
            else:
                return TaskPackage.objects.filter(isdelete=False, owner=user.username)
        return None


class TaskPackageSonViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    # TODO 返回左右子任务包,不明白
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
            try:
                taskpackage = TaskPackage.objects.get(name=taskpackage_name)
                if taskpackage.newtaskpackagesonfornotice != 0 and user.isadmin:
                    taskpackage.newtaskpackagesonfornotice = 0
                    taskpackage.save()
            except TaskPackage.DoesNotExist as e:
                return []
            # try:
            #     taskpackage = TaskPackage.objects.get(name=taskpackage_name)
            # except TaskPackage.DoesNotExist:
            #     return []
            else:
                if user.isadmin:
                    return TaskPackageSon.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
                else:
                    if user.username == taskpackage.owner:
                        return TaskPackageSon.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
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
            try:
                taskpackage = TaskPackage.objects.get(name=taskpackage_name)
            except TaskPackage.DoesNotExist:
                return []
            else:
                if user.isadmin:
                    return TaskPackageOwner.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
                else:
                    return TaskPackageOwner.objects.filter(owner=user.username, taskpackage_name=taskpackage.name,
                                                           isdelete=False)
        return None


# TODO 和URL保持一致，是否应该放在序列化器中实现
class EchartTaskpackageViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    list: 图表数据获取（用户所对应任务包数量）
    """
    permission_classes = [IsAuthenticated]
    queryset = EchartTaskPackage.objects.filter(count__gt=0)
    serializer_class = EchartTaskpackageSerializer

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            count = TaskPackage.objects.filter(owner=user.username).count()
            try:
                echarttaskpackage = EchartTaskPackage.objects.get(user_reallyname=user.reallyname)
            except EchartTaskPackage.DoesNotExist:
                EchartTaskPackage.objects.create(user_reallyname=user.reallyname, count=count)
            else:
                echarttaskpackage.count = count
                echarttaskpackage.save()

        echarttaskpackages = self.get_queryset()
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

        schedules = TaskPackageScheduleSet.objects.all()
        for schedule in schedules:
            count = TaskPackage.objects.filter(schedule=schedule).count()
            try:
                echartschedule = EchartSchedule.objects.get(taskpackage_schedule=schedule)
            except:
                EchartSchedule.objects.create(taskpackage_schedule=schedule, count=count)
            else:
                echartschedule.count = count
                echartschedule.save()

        echartschedules = self.get_queryset()
        serializer = self.get_serializer(echartschedules, many=True)

        return Response(serializer.data)


# 进度增删改查
class ScheduleViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):

    serializer_class = ScheduleSerializer
    queryset = TaskPackageScheduleSet.objects.all()
    permission_classes = [IsAuthenticated, AdminPerssion]



# 文件分块上传
class TaskPackageChunkViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = TaskPackageChunk.objects.all()
    serializer_class = TaskPackageChunkSerializer


