#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding:utf-8 -*-
import sys
import os
import arcpy
import shutil
from datetime import datetime
import psycopg2
from celery_app import app
from ziptools import zipUpFolder
import zipfile

reload(sys)
sys.setdefaultencoding('utf8')


@app.task
def createregiontask(regiontask_id, regiontask_filepath):
    # 解压文件
    file_dir = os.path.dirname(regiontask_filepath)
    r = zipfile.is_zipfile(regiontask_filepath)
    if r:
        fz = zipfile.ZipFile(regiontask_filepath, 'r')
        for file in fz.namelist():
            fz.extract(file, file_dir)
    else:
        print('This is not zip')

    filename = regiontask_filepath.split("\\")[-1].split(".zip")[0]
    unzipfile = os.path.join(file_dir, filename)
    print unzipfile

    # 操作空间库

    # 修改关系库中的数据
    dbname = u"mmanageV7.0"
    tablename = u"taskpackages_regiontask"
    status = u"处理完成"
    basemapservice = u'basemapservice'
    mapindexfeatureservice = u"mapindexfeatureservice"
    mapindexmapservice = u"mapindexmapservice"
    mapindexschedulemapservice = u"mapindexschedulemapservice"


    changeDJdbregiontasktable(dbname, tablename, regiontask_id, status, basemapservice,
                              mapindexfeatureservice, mapindexmapservice, mapindexschedulemapservice)
    return True


def changeDJdbregiontasktable(dbname, tablename, regiontask_id, status, basemapservice,
                              mapindexfeatureservice, mapindexmapservice, mapindexschedulemapservice):
    conn = psycopg2.connect(dbname=dbname,
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    UPDATESQL = u"update %s set status='%s',basemapservice='%s',mapindexfeatureservice='%s',mapindexmapservice='%s',mapindexschedulemapservice='%s' where ID=%d" % (
        tablename, status, basemapservice, mapindexfeatureservice, mapindexmapservice, mapindexschedulemapservice,regiontask_id)
    cur.execute(UPDATESQL)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    pass
