# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from models import TaskPackage, TaskPackageVersion
from serializers import MapListViewSerializer, CreateMapMessageViewSerializer, CreateTaskpackageVersionSerializer, \
    MapVersionListViewSerializer
from utils.permission import AdminPerssion
from rest_framework.generics import CreateAPIView


class MapList(ReadOnlyModelViewSet):
    """
    获取图号信息      GET
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MapListViewSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == 1:
            queryset = TaskPackage.objects.filter(is_delete=False)
        else:
            queryset = TaskPackage.objects.filter(user_id=user.id).filter(is_delete=False)
        return queryset


class CreateMapMessage(CreateAPIView):
    """
    创建图号信息      POST
    """
    permission_classes = [IsAuthenticated, AdminPerssion]
    serializer_class = CreateMapMessageViewSerializer


class CreateTaskpackageVersion(CreateAPIView):
    """
    创建图号版本
    """
    permission_classes = [IsAuthenticated, AdminPerssion]
    serializer_class = CreateTaskpackageVersionSerializer


class MapVersionList(ReadOnlyModelViewSet):
    """
    获取图号版本信息      GET
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MapVersionListViewSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == 1:
            queryset = TaskPackageVersion.objects.filter(is_delete=False)
        else:
            queryset = TaskPackageVersion.objects.filter(user_id=user.id).filter(is_delete=False)
        return queryset
