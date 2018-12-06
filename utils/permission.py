# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.permissions import BasePermission


class AdminPerssion(BasePermission):
    message = "管理员权限可以访问"

    def has_permission(self, request, view):
        if request.user.role is False:
            return False
        return True
