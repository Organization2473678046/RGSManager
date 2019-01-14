# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.test import TestCase
# Create your tests here.

import os
import sys
import psycopg2

reload(sys)
sys.setdefaultencoding('utf8')


def get_user_data(tablename):
    # 获取用户表数据
    conn = psycopg2.connect(dbname="mmanageV5.0",
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
    conn = psycopg2.connect(dbname="mmanageV6.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()

    sql = "insert into %s (username, password,is_superuser, is_staff, is_active,date_joined,isadmin, reallyname) values ('%s', '%s',%r,%r, %r,%r, %r, '%s')" % (
        tablename, data[4], data[1], data[3], data[8], data[9], str(data[10]), data[11], data[12])
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackage_data(tablename):
    # 获取主任务包表数据
    conn = psycopg2.connect(dbname="mmanageV5.0",
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
        data = list(data)
        print data
        username = data[2]
        # print type(username)
        cur.execute(u"select reallyname from users_user where username = '%s'" % username)
        reallyname = cur.fetchone()[0]
        print reallyname
        data.append(reallyname)
        print data
        taskpackage_insert(data)

    conn.close()


def taskpackage_insert(data):
    """taskpackages_taskpackage表数据的迁移"""
    conn = psycopg2.connect(dbname="mmanageV6.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    if data[3] is None or data[3] == "None":
        sql = u"insert into taskpackages_taskpackage (name,owner,mapnums,file,status,describe,createtime,updatetime,isdelete,mapnumcounts, schedule,newtaskpackagesonfornotice,reallyname) values ('%s','%s','%s','%s',%r, '%s',%r, %r,%r,%d,'%s',%d,'%s')" % (
            data[1], data[2], data[4], data[5], data[6], data[9], str(data[7]), str(data[8]),
            data[10], data[11], data[12], data[13], data[14])
    else:
        sql = u"insert into taskpackages_taskpackage (name,owner,exowner,mapnums,file,status,describe,createtime,updatetime,isdelete,mapnumcounts, schedule,newtaskpackagesonfornotice,reallyname) values ('%s','%s','%s','%s','%s',%r, '%s',%r, %r,%r,%d,'%s',%d,'%s')" % (
            data[1], data[2], data[3], data[4], data[5], data[6], data[9], str(data[7]), str(data[8]),
            data[10], data[11], data[12], data[13], data[14])
    cur.execute(sql)

    conn.commit()
    conn.close()


def get_taskpackageson_data(tablename):
    # 获取子任务包表数据
    conn = psycopg2.connect(dbname="mmanageV5.0",
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
    conn = psycopg2.connect(dbname="mmanageV6.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    schedule_list = ["未指定状态", "修改缝隙", "河网环修改", "有向点修改", "一对多修改", "匝道赋值", "同层拓扑", "不同层拓扑", "微短线修改", "微小面修改", "急锐角修改",
                     "等高线拼接", "完成"]
    sql = u"insert into taskpackages_taskpackageson (taskpackage_name,user_username,version,file,describe,createtime,updatetime,isdelete, schedule) values ('%s','%s','%s','%s','%s',%r,%r,%r,%d)" % (
        data[1], data[7], data[2], data[6], data[5], str(data[3]), str(data[4]), data[8], schedule_list[data[9]])
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_taskpackageowner_data(tablename):
    # 获取@表数据
    conn = psycopg2.connect(dbname="mmanageV5.0",
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
    conn = psycopg2.connect(dbname="mmanageV6.0",
                            user="postgres",
                            password="Lantucx2018",
                            host="localhost",
                            port="5432")
    cur = conn.cursor()
    if data[3] is None or data[3] == "None":
        sql = u"insert into taskpackages_taskpackageowner (taskpackage_name,owner,describe,createtime,isdelete) values ('%s','%s','%s',%r,FALSE )" % (
            data[1], data[2], data[5], str(data[4]))
    else:
        sql = u"insert into taskpackages_taskpackageowner (taskpackage_name,owner,exowner,describe,createtime,isdelete) values ('%s','%s','%s','%s',%r,FALSE )" % (
            data[1], data[2], data[3], data[5], str(data[4]))
    print sql
    cur.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # 迁移users_user表需要去掉first_name,last_name, email非空约束
    get_user_data("users_user")

    # 迁移主任务包表
    # get_taskpackage_data("taskpackages_taskpackage")

    # 迁移主任务包子版本
    # get_taskpackageson_data("taskpackages_taskpackageson")

    # 迁移@功能表
    # get_taskpackageowner_data("taskpackages_taskpackageowner")

    pass
