#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import sys
import os

import psycopg2
from unrar import rarfile
import zipfile

reload(sys)
sys.setdefaultencoding('utf8')



import arcpy

def append_mapnums():
    conn = psycopg2.connect(dbname=u"mmanageV8.0",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    SQL = "SELECT name,file FROM taskpackages_taskpackage"
    cur.execute(SQL)
    name_file = cur.fetchall()
    num = 0
    error_list = []
    base_path = u"E:\\RGSManager\\media\\"
    while True:
        if num >=2:
            break
        database_path = name_file[num][1]
        file_path = base_path + database_path
        file_dir = os.path.dirname(file_path)         # 解压后文件保存路径
        file_name = name_file[num][0]                 # 文件名
        num += 1

        z = zipfile.is_zipfile(file_path)
        r = rarfile.is_rarfile(file_path)
        if z:
            # -ibck: 后台运行; -o+:覆盖已存在文件
            rar_command = '"C:\Program Files\WinRAR\WinRAR.exe" x %s %s -ibck -o+' % (file_path, file_dir)
            rar_command = rar_command.encode('gbk')
            os.system(rar_command)
            # print rar_command.decode('gbk')
            # print u"解压成功"
        elif r:
            fz = rarfile.RarFile(file_path, 'r')
            for file in fz.namelist():
                fz.extract(file, file_dir)
            # print u"解压成功"
        else:
            print(u'This is not zip or rar')
            return False


        taskpath = file_dir + "\\" + file_name
        path = os.path.join(taskpath,u"Source", u"接图表.gdb", u"DLG_50000", u"GBmaprange")

        # 查找任务包名字和图号
        try:
            cursor = arcpy.da.SearchCursor(path, ["new_jbmapn"])
        except Exception as e:
            error_list.append(file_name)
            print "任务包 '{0}' 接图表无法找到".format(file_name)
            continue
        taskpackage_name = file_name
        for row in cursor:
            SQL = "SELECT mapnums from taskpackages_taskpackage where name='{0}'".format(taskpackage_name)  # 按任务包名字查询原mapnums
            cur.execute(SQL)
            mapnums = cur.fetchall()
            old_mapnum = mapnums[0][0]      # 提取原有mapnums
            if old_mapnum is None:
                SQL = "UPDATE taskpackages_taskpackage set mapnums='{0}' where name='{1}'".format(row[0], taskpackage_name)
            else:
                SQL = "UPDATE taskpackages_taskpackage set mapnums='{0}' where name='{1}'".format(old_mapnum +","+ row[0], taskpackage_name)
            # print SQL                       # 添加mapnums
            cur.execute(SQL)
            conn.commit()
            print "任务包 {0} 属性添加成功".format(file_name)

    conn.close()
    print "以下任务包接图表文件查找失败"
    print error_list


if __name__ == "__main__":

    append_mapnums()

