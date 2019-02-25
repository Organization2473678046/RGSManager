# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManager.settings")
import django
django.setup()

from taskpackages.models import TaskPackage

def get_all_data():

    return TaskPackage.objects.all()






