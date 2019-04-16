# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.permission import AdminPerssion
from models import User
from .serializers import UserSerializer, UserListSerializer


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 50
    page_query_param = 'page'

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


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            return User.objects.filter(id=user.id)
        elif self.action == "retrieve":
            user = User.objects.get(id = int(self.kwargs["pk"]))
            if user.isadmin is True:
                user.set_password("root12345")
            else:
                user.set_password("12345")
            user.save()
            return User.objects.all()



class UserManageViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):

    serializer_class = UserListSerializer
    pagination_class = UserPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ("id", "username", "date_joined")
    ordering = ("-date_joined",)
    search_fields = ('date_joined', 'username', 'reallyname')

    def get_permissions(self):
        if self.action == "update":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), AdminPerssion()]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(is_superuser=False)
        else:
            return User.objects.all()

