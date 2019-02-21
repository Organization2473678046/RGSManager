#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import psycopg2

reload(sys)
sys.setdefaultencoding('utf8')


def get_user_data(tablename):
    # 获取用户表数据
    conn = psycopg2.connect(dbname="mmanageV7.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    SELECTSQL = "select * from %s order by id" % tablename
    cur.execute(SELECTSQL)
    while True:
        data = cur.fetchone()
        if data:
            print data
            user_insert(data, "users_user")
        else:
            conn.close()
            return


def user_insert(data, tablename):
    # users_user表数据的迁移
    conn = psycopg2.connect(dbname="mmanageV8.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = "insert into %s (username, password,is_superuser, is_staff, is_active,isadmin, reallyname) values ('%s', '%s',%r,%r, %r, %r, '%s')" % (
        tablename, data[4], data[1], data[3], data[8], data[9], data[11], data[12])
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackage_data(tablename):
    # 获取主任务包表数据
    conn = psycopg2.connect(dbname="mmanageV7.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    data_list = cur.fetchall()
    # print data_list
    for data in data_list:
        # data = cur.fetchone()
        # data = list(data)
        print data
        # username = data[2]
        # print type(username)
        # cur.execute(u"-- select reallyname from users_user where username = '%s'" % username)
        # reallyname = cur.fetchone()[0]
        # print reallyname
        # data.append(reallyname)
        taskpackage_insert(data)

    conn.close()


def taskpackage_insert(data):
    """taskpackages_taskpackage表数据的迁移"""
    conn = psycopg2.connect(dbname="mmanageV8.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    if data[3] is None or data[3] == "None":
        sql = u"insert into taskpackages_taskpackage (name,owner,mapnums,file,status,createtime,updatetime,describe,isdelete,mapnumcounts,newtaskpackagesonfornotice,reallyname,schedule,regiontask_name) values ('%s','%s','%s','%s',%r, %r, %r,'%s',%r,%d,%d,'%s','%s','东南区域1800幅')" % (
            data[1], data[2], data[4], data[5], data[6], str(data[7]), str(data[8]), data[9],
            data[10], data[11], data[12], data[13], data[14])
    else:
        # sql = u"insert into taskpackages_taskpackage (name,owner,exowner,mapnums,file,status,describe,createtime,updatetime,isdelete,mapnumcounts, schedule,reallyname) values ('%s','%s','%s','%s','%s',%r, '%s',%r, %r,%r,%d,'%s','%s')" % (
        #     data[1], data[10], data[2], data[3], data[4], data[5], data[9], str(data[7]), str(data[8]), data[6])
        sql = u"insert into taskpackages_taskpackage (name,owner,exowner,mapnums,file,status,createtime,updatetime,describe,isdelete,mapnumcounts,newtaskpackagesonfornotice,reallyname,schedule,regiontask_name) values ('%s','%s','%s','%s','%s',%r, %r, %r,'%s',%r,%d,%d,'%s','%s','东南区域1800幅')" % (
            data[1], data[2], data[3], data[4], data[5], data[6], str(data[7]), str(data[8]), data[9],
            data[10], data[11], data[12], data[13], data[14])
    cur.execute(sql)

    conn.commit()
    conn.close()


def get_taskpackageson_data(tablename):
    # 获取子任务包表数据
    conn = psycopg2.connect(dbname="mmanageV7.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    while True:
        taskpackageson_data = cur.fetchone()
        if taskpackageson_data:
            print taskpackageson_data
            taskpackageson_insert(taskpackageson_data)
        else:
            conn.close()
            return


def taskpackageson_insert(data):
    # taskpackages_taskpackageson表数据的迁移
    conn = psycopg2.connect(dbname="mmanageV8.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = u"insert into taskpackages_taskpackageson (taskpackage_name,version,createtime,updatetime,describe,file,user_username,isdelete, schedule,regiontask_name) values ('%s','%s',%r,%r,'%s','%s','%s',%r,'%s','东南区域1800幅')" % (
        data[1], data[2], str(data[3]), str(data[4]), data[5], data[6], data[7], data[8], data[9])
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackageowner_data(tablename):
    # 获取@表数据
    conn = psycopg2.connect(dbname="mmanageV7.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    while True:
        taskpackageowner_data = cur.fetchone()
        if taskpackageowner_data:
            print taskpackageowner_data
            taskpackageowner_insert(taskpackageowner_data)
        else:
            conn.close()
            return


def taskpackageowner_insert(data):
    # taskpackages_taskpackageowner表数据的迁移
    conn = psycopg2.connect(dbname="mmanageV8.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    if data[3] is None or data[3] == "None":
        sql = u"insert into taskpackages_taskpackageowner (taskpackage_name,owner,createtime,describe,isdelete,regiontask_name) values ('%s','%s',%r,'%s',%r,'东南区域1800幅')" % (
            data[1], data[2], str(data[4]), data[5], data[6])
    else:
        sql = u"insert into taskpackages_taskpackageowner (taskpackage_name,owner,exowner,createtime,describe,isdelete,regiontask_name) values ('%s','%s','%s',%r,'%s',%r,'东南区域1800幅')" % (
            data[1], data[2], data[3], str(data[4]), data[5], data[6])
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackageschedule_data(tablename):
    # 获取进度表
    conn = psycopg2.connect(dbname="mmanageV7.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    while True:
        taskpackageschedule_data = cur.fetchone()
        if taskpackageschedule_data:
            print taskpackageschedule_data
            taskpackageschedule_insert(taskpackageschedule_data)
        else:
            conn.close()
            return


def taskpackageschedule_insert(data):
    # taskpackages_taskpackagescheduleset 表数据的迁移
    conn = psycopg2.connect(dbname="mmanageV8.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = u"insert into taskpackages_taskpackagescheduleset (schedule,regiontask_name) values ('%s','东南区域1800幅')" % (
        data[1])
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackageregiontask_data(tablename):
    # 获取taskpackages_regiontask表数据
    conn = psycopg2.connect(dbname="mmanageV7.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql = u"select * from %s order by id" % tablename
    cur.execute(sql)
    while True:
        taskpackageowner_data = cur.fetchone()
        if taskpackageowner_data:
            print taskpackageowner_data
            taskpackageregiontask_insert(taskpackageowner_data)
        else:
            conn.close()
            return


def taskpackageregiontask_insert(data):
    # taskpackages_regiontask表数据的迁移
    conn = psycopg2.connect(dbname="mmanageV8.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    print data
    for a in data:
        if a is None:
            a = "0"
    sql = u"insert into taskpackages_regiontask (name, file, basemapservice, mapindexfeatureservice, mapindexmapservice, mapindexschedulemapservice, status, mapindexsde, rgssde) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
          # u" ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%r)" % (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10])

    print sql
    cur.execute(sql)
    conn.commit()

    conn.close()


if __name__ == '__main__':
    # 迁移users_user表时,需要去掉first_name,last_name, email,date_joined几个字段的非空约束
    # get_user_data("users_user")

    # 迁移主任务包表
    # get_taskpackage_data("taskpackages_taskpackage")

    # 迁移主任务包子版本
    # get_taskpackageson_data("taskpackages_taskpackageson")

    # 迁移@功能表
    # get_taskpackageowner_data("taskpackages_taskpackageowner")

    # 迁移进度表
    # get_taskpackageschedule_data("taskpackages_taskpackagescheduleset")

    # 迁移地图区域表
    get_taskpackageregiontask_data("taskpackages_regiontask")

    # get_data()
    pass
