#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding:utf-8 -*-

import sys
import os
import arcpy
import shutil
from datetime import datetime
import psycopg2
from celery_app import app

reload(sys)
sys.setdefaultencoding('utf8')

@app.task
def over_time():
    conn = psycopg2.connect(dbname=u"mmanageV0.10",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    SQL = "SELECT taskpackage_name,endtime,regiontask_name,id FROM taskpackages_taskpackageowner WHERE isoverdue=FALSE "
    cur.execute(SQL)
    taskpackage_owners = cur.fetchall()
    for taskpackage_owner in taskpackage_owners:
        if taskpackage_owner[1] is not None and taskpackage_owner[1].replace(tzinfo=None) < datetime.now():
            SQL = "SELECT updatetime, id FROM taskpackages_taskpackageson WHERE taskpackage_name='%s' AND regiontask_name='%s' ORDER BY createtime DESC"%(taskpackage_owner[0],taskpackage_owner[2])
            cur.execute(SQL)
            taskpackageson = cur.fetchone()
            if taskpackageson[0] is not None and taskpackageson[0] < taskpackage_owner[1]:
                SQL01 = "UPDATE taskpackages_taskpackageowner SET isoverdue=TRUE WHERE id=%d AND regiontask_name='%s'"%(taskpackage_owner[3],taskpackage_owner[2])
                SQL02 = "UPDATE taskpackages_taskpackage SET isoverdue=TRUE WHERE name='%s' AND regiontask_name='%s'"%(taskpackage_owner[0],taskpackage_owner[2])
                cur.execute(SQL01)
                cur.execute(SQL02)


    conn.commit()
    conn.close()

    return "over_time successful"

if __name__ == '__main__':
    over_time()