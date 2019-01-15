# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.permission import AdminPerssion
from models import User
from .serializers import UserSerializer, UserListSerializer


class UserListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list: 获取作业员列表
    create: 创建用户
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, AdminPerssion]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(isadmin=False)
        else:
            return []


class UserViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
