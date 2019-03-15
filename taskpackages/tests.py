# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
import os
import sys

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManager.settings")
import django

django.setup()
from taskpackages.models import RegionTask, TaskPackageScheduleSet,TaskPackage

if __name__ == "__main__":
    # from taskpackages.models import TaskPackage
    # tasks = TaskPackage.objects.all().values_list("name")
    # print tasks
    # print tasks[0]
    # print type(tasks[0])

    # 批量修改createtime
    # regiontasks = RegionTask.objects.all().order_by('id')[:14]
    # i = 1
    # # j = str(i)
    # for regiontask in regiontasks:
    #     regiontask.createtime = "2019-02-{} 08:44:11.369+08".format(i)
    #     regiontask.save()
    #     i += 1
    # pass

    # taskPackageschedule = TaskPackageScheduleSet.objects.get(schedule='匝道赋值', regiontask_name='东南区域1800幅')
    # print taskPackageschedule

    # count = 1
    # while True:
    #     count += 1
    #     try:
    #         # arcpy.UploadServiceDefinition_server(sd, con)
    #         TaskPackageScheduleSet.objects.get(id=1)
    #     except:
    #         print '没查到'
    #     else:
    #         print "Service successfully published"
    #         # if os.path.exists(sd):
    #         #     os.remove(sd)
    #         break


    # 批量修改status
    schedules = TaskPackageScheduleSet.objects.filter(regiontask_name='东南区域1800幅').order_by('id')[2:]
    for schedule in schedules:
       TaskPackageScheduleSet.objects.create(schedule=schedule.schedule,regiontask_name='写Python脚本的时候')

    pass

