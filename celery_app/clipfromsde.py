#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding:utf-8 -*-
"""
#============================================
#
# Project: mycelery
# Name: The file name is clipfromsde
# Purpose:
# Auther: Administrator
# Tel: 17372796660
#
#============================================
#
"""

import sys
import os
import arcpy
import shutil
from datetime import datetime
import psycopg2
from celery_app import app
from ziptools import zipUpFolder

reload(sys)
sys.setdefaultencoding('utf8')


@app.task
def clipfromsde(mapindexsdepath, gbrgssdepath, jbrgssdepath, mapnumlist, MEDIA, taskname, taskpackage_id, taskpackageson_id):
    mapindexsde = os.path.basename(mapindexsdepath)
    gbrgsde = os.path.basename(gbrgssdepath)
    jbrgsde = os.path.basename(jbrgssdepath)
    changeSDEmapindex(mapnumlist, mapindexsde, status=2)

    taskdirname = u"data/{0}/{1}/{2}/{3}/{4}".format(datetime.now().strftime("%Y"),
                                                     datetime.now().strftime("%m"),
                                                     datetime.now().strftime("%d"),
                                                     datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), taskname)

    taskdirnameup = os.path.dirname(taskdirname)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # 三楼服务器sde
    # rgsde = u"rgs20181206202724.sde"
    # mapindexsde=u"mapindex20181206202724.sde"

    # 二楼服务器sde
    # rgsde = u"rgs20181207133843.sde"
    # mapindexsde=u"mapindex20181207133843.sde"

    # 根据传过来的sdepath获取sde
    # mapindexsde = mapindexsdepath.split("\\")[-1]
    # rgsde = rgssdepath.split("\\")[-1]


    tempath = os.path.join(SCRIPT_DIR, u"tasktemplate")
    taskpath = os.path.join(MEDIA, taskdirname)
    shutil.copytree(tempath, taskpath)
    jtbpath = os.path.join(taskpath, u"Source", u"接图表.gdb", u"DLG_50000", u"GBmaprange")
    SQList = []
    for mapnum in mapnumlist.split(u","):
        SQL = u"new_jbmapn = '%s'" % mapnum
        SQList.append(SQL)
    SQLstr = u" or ".join(SQList)
    # print SQLstr


    # arcpy.env.workspace = os.path.join(SCRIPT_DIR, mapindexsde)
    arcpy.env.workspace = mapindexsdepath
    for ds in arcpy.ListDatasets(feature_type='feature') + ['']:
        if ds == mapindexsde + u".DLG_50000":
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                if fc == mapindexsde + u".GBmaprange":
                    fcpath = os.path.join(arcpy.env.workspace, ds, fc)
                    arcpy.Select_analysis(fcpath, jtbpath, SQLstr)


    # arcpy.env.workspace = os.path.join(SCRIPT_DIR, rgsde)
    arcpy.env.workspace = gbrgssdepath
    for ds in arcpy.ListDatasets(feature_type='feature') + ['']:
        if ds == gbrgsde + u".DLG_K050":
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                fcpath = os.path.join(arcpy.env.workspace, ds, fc)
                taskgbpath = os.path.join(taskpath, u"Source", u"GBRGS.gdb", u"DLG_K050", fc.split(".")[2])
                arcpy.Clip_analysis(fcpath, jtbpath, taskgbpath)

    # arcpy.env.workspace = os.path.join(SCRIPT_DIR, rgsde)
    arcpy.env.workspace = jbrgssdepath
    for ds in arcpy.ListDatasets(feature_type='feature') + ['']:
        if ds == jbrgsde + u".DLG_K050":
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                fcpath = os.path.join(arcpy.env.workspace, ds, fc)
                taskgbpath = os.path.join(taskpath, u"Source", u"JBRGS.gdb", u"DLG_K050", fc.split(".")[2])
                arcpy.Clip_analysis(fcpath, jtbpath, taskgbpath)

    outZipFile = os.path.join(MEDIA, taskdirnameup, taskname + u".zip")
    zipUpFolder(taskpath, outZipFile)
    dbname = u"mmanageV0.10"
    tablename = u"taskpackages_taskpackage"
    taskpackagesontablename = u"taskpackages_taskpackageson"
    statusfieldname = u"status"
    filefieldname = u"file"
    MEDIAfilepath = taskdirnameup + u"/" + taskname + u".zip"
    changeDJdbtasktable(dbname, tablename, taskpackage_id, statusfieldname, filefieldname, MEDIAfilepath,
                        taskpackageson_id, taskpackagesontablename)
    changeSDEmapindex(mapnumlist, mapindexsde, status=3)
    return True


def changeDJdbtasktable(dbname, tablename, taskpackage_id, statusfieldname, filefieldname, MEDIAfilepath,
                        taskpackageson_id, taskpackagesontablename):
    conn = psycopg2.connect(dbname=dbname,
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    # print "tt"
    cur = conn.cursor()
    UPDATESQL = u"UPDATE %s set %s = '1',%s='%s' where ID=%d" % (
        tablename, statusfieldname, filefieldname, MEDIAfilepath, taskpackage_id)
    # SQL="SELECT * FROM %s" %tablename
    # print UPDATESQL
    cur.execute(UPDATESQL)

    UPDATESQL1 = u"UPDATE %s set %s='%s' where ID=%d" % (
        taskpackagesontablename, filefieldname, MEDIAfilepath, taskpackageson_id)
    # SQL="SELECT * FROM %s" %tablename
    # print UPDATESQL
    cur.execute(UPDATESQL1)

    conn.commit()
    conn.close()


def changeSDEmapindex(mapnumlist, mapindexsde, status):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    workspace = os.path.join(SCRIPT_DIR, mapindexsde)
    sde_conn = arcpy.ArcSDESQLExecute(workspace)
    tbl = mapindexsde + u".GBmaprange"
    col = u"flag"
    val = u"1"

    for mapnum in mapnumlist.split(u","):
        col1 = u"new_jbmapn = '%s'" % mapnum
        # sql = "update mapindex20181204150827.sde.GBmaprange set flag="1 where {3} = {4}".format(tbl, col, val, col1,col1_val)
        sql = "update {0} set status='{1}' where {2}".format(tbl, status, col1)

        # sql="select objectid from mapindex20181204150827.sde.GBmaprange"
        sde_conn.execute(sql)
    sde_conn.commitTransaction()
    del sde_conn
    return True


if __name__ == "__main__":
    mapindexsdepath = u'E:\\RGSManager\\celery_app\\mapindex20190417165250.sde'
    gbrgssdepath = u'E:\\RGSManager\\celery_app\\gbrgs20190417165250.sde'
    jbrgssdepath = u'E:\\RGSManager\\celery_app\\jbrgs20190417165250.sde'
    # jbrgssdepath = u'E:\\RGSManager\\celery_app\\jbrgs20190417165250.sde\\jbrgs20190417165250.sde.DLG_K050'
    mapnumlist = "I49E019022,I49E019023,I49E019024"
    MEDIA = 'E:\\RGSManager\\media'
    taskname = u'任务包3号'
    taskpackage_id = 4
    taskpackageson_id = 7
    clipfromsde(mapindexsdepath, gbrgssdepath, jbrgssdepath, mapnumlist, MEDIA, taskname, taskpackage_id, taskpackageson_id)
    # changeDJdbtasktable(u"mmanageV1.0",u"taskpackages_taskpackage",1,u"status",u"file",u"user_1/npm_lazy.rar")
    # changeSDEmapindex(u"I49E019021,I49E019022,I49E019023")
