# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from models import Users
from serializers import  WorkerListSerialziers, CreateUserSerizlizer, UserMessageList
from utils.permission import AdminPerssion
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView


class CreateUserView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateUserSerizlizer



class RoleView(ListAPIView):
    """
    获取用户信息      GET
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserMessageList

    def get_queryset(self):
        query_set = Users.objects.filter(id=self.request.user.id)
        return query_set



class WorkerList(ReadOnlyModelViewSet):
    """
    获取作业员列表     GET
    """
    permission_classes = [IsAuthenticated, AdminPerssion]
    queryset = Users.objects.filter(role=False)
    serializer_class = WorkerListSerialziers

