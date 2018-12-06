# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from models import TaskPackage, TaskPackageVersion
from serializers import MapListViewSerializer, CreateMapMessageViewSerializer, CreateTaskpackageVersionSerializer, \
    MapVersionListViewSerializer
from utils.pagination import MyPageNumberPagination
from utils.permission import AdminPerssion
from rest_framework.generics import CreateAPIView, ListAPIView


# 获取图号信息
class MapList(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MapListViewSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user = self.request.user

        if user.role == 1:
            queryset = TaskPackage.objects.filter(is_delete=False)
        else:
            queryset = TaskPackage.objects.filter(user_id=user.id).filter(is_delete=False)
        return queryset


# 创建图号信息
class CreateMapMessage(CreateAPIView):
    permission_classes = [IsAuthenticated, AdminPerssion]
    serializer_class = CreateMapMessageViewSerializer


# 创建图号版本
class CreateTaskpackageVersion(CreateAPIView):
    permission_classes = [IsAuthenticated, AdminPerssion]
    serializer_class = CreateTaskpackageVersionSerializer


# 获取图号版本信息
class MapVersionList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MapVersionListViewSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        id = self.kwargs.get('id')
        if user.role is True:
            return TaskPackageVersion.objects.filter(is_delete=False).filter(taskpackage_id=id)
        else:
            return TaskPackageVersion.objects.filter(user_id=user.id).filter(taskpackage_id=id).filter(is_delete=False)
