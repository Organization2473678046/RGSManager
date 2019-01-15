# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db.models import QuerySet
from django.test import TestCase

# Create your tests here.
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManager.settings")
import django
django.setup()


if __name__ == '__main__':
    from taskpackages.models import TaskPackage
    from taskpackages.models import RegionTask
    # obj1 = TaskPackage.objects.values("owner")
    # print obj1
    # obj = TaskPackage.objects.values("owner").distinct()
    # print len(obj)
    # print obj.count()
    #
    # print obj

    # taskpackage = TaskPackage.objects.get(name="task1",regiontask_name="东南区域")
    # print taskpackage

    # r = RegionTask.objects.filter(name="111")

    # if not None:
    #     print "2222"
    # if r == QuerySet([]):
    #     print 111
    # print r
    pass
