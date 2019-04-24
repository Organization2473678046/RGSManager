# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission
from datetime import datetime



class LicensePerssion(BasePermission):
    message = u"授权已过期"
    def has_permission(self, request, view):
        time_ = datetime.strptime("2919-04-18", "%Y-%m-%d")
        if datetime.now() > time_:
            return False
        return True


