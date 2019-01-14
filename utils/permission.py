# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.permissions import BasePermission
from taskpackages.models import TaskPackage


class AdminPerssion(BasePermission):
    message = "管理员权限才可以访问"

    def has_permission(self, request, view):
        if request.user.isadmin is False or request.user=="AnonymousUser":
            return False
        return True


class UserPerssion(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.username == obj.owner:
            return True

        return False



