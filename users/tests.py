# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.test import TestCase

# Create your tests here.
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManageV5.settings")
import django
django.setup()


if __name__ == '__main__':
    from taskpackages.models import TaskPackage
    obj1 = TaskPackage.objects.values("owner")
    print obj1
    obj = TaskPackage.objects.values("owner").distinct()
    print len(obj)
    print obj.count()

    print obj

    pass
