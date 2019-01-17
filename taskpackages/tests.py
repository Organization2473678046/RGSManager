# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import os
import sys

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManager.settings")
import django
django.setup()

if __name__ == "__main__":
    # from taskpackages.models import TaskPackage
    # tasks = TaskPackage.objects.all().values_list("name")
    # print tasks
    # print tasks[0]
    # print type(tasks[0])

    pass