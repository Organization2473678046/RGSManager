#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import sys
import os
import arcpy
import shutil
import datetime

import chardet
import psycopg2
from unrar import rarfile
import time
from celery_app import app
from ziptools import zipUpFolder
import zipfile

# reload(sys)
# sys.setdefaultencoding('utf8')


@app.task
def createregiontask(regiontask_id, regiontask_filepath, service_name):
    # str_type = chardet.detect(regiontask_filepath)
    # print str_type['encoding'], "-----------"
    # 解压文件
    file_dir = os.path.dirname(regiontask_filepath)  # 解压后文件保存路径
    # 压缩包名字
    file_name = os.path.basename(regiontask_filepath)
    print file_name
    print regiontask_filepath
    # str_type = chardet.detect(regiontask_filepath)
    # print str_type['encoding'], "-----------"
    # regiontask_filepath = os.path.normpath(regiontask_filepath)
    z = zipfile.is_zipfile(regiontask_filepath)
    r = rarfile.is_rarfile(regiontask_filepath)
    if z:
        # save_list = regiontask_filepath.split(u"/")
        # save_list.pop()
        # save_path = u"/".join(save_list)
        print regiontask_filepath

        # rar_command = '"C:\Program Files\WinRAR\WinRAR.exe" x %s %s' % (regiontask_filepath, file_dir)
        rar_command = '"D:\Program Files\WinRAR\WinRAR.exe" x %s %s' % (regiontask_filepath, file_dir)
        rar_command = rar_command.encode('gbk')
        # print rar_command
        os.system(rar_command)
        print rar_command.decode('gbk')
        # print u"解压zip成功{0}".format(regiontask_id)
        print u"解压 {0} 成功".format(file_name)

    elif r:
        fz = rarfile.RarFile(regiontask_filepath, 'r')
        for file in fz.namelist():
            fz.extract(file, file_dir)
        # filename = regiontask_filepath.split("\\")[-1].split(".rar")[0]
        # file_path = os.path.join(file_dir, filename)
        # print u"解压rar成功{0}".format(regiontask_id)
        print u"解压 {0} 成功".format(file_name)
    else:
        print('This is not zip or rar')
        return False

    print '结束'.encode('gbk')
    return

    time_ymdhms = datetime.datetime.now().strftime(u"%Y%m%d%H%M%S")
    # os.listdir 返回指定目录下的所有文件和目录名。
    dir_list = os.listdir(file_dir)

    # 创建空间库
    print u"开始创建空间库"
    for dir in dir_list:
        gdbpath = os.path.join(file_dir, dir)
        if dir.startswith("RGS"):
            datatype = u"rgs"
            ARCGIS_create_database(gdbpath, time_ymdhms, datatype)
            print u"创建rgs文件成功"
        elif dir.startswith("接图表"):
            datatype = "mapindex"
            ARCGIS_create_database(gdbpath, time_ymdhms, datatype)
            print "创建mapindex文件成功"

    mapindexsde = "mapindex" + time_ymdhms + ".sde"

    # 添加用于标记颜色的status字段
    ARCGIS_add_field(mapindexsde)
    print u"暂不可自动发服务，请手动修改字段所需属性，注册版本，保存MXD文件，注册PG数据源，共享服务"
    # 发布服务
    # ARCGIS_service(service_name)

    # 填充postgres中服务字段
    Posrgres_change_regiontask(regiontask_id, service_name)
    return True


# 创建空间数据库
def ARCGIS_create_database(gdbpath, time_ymdhms, datatype):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    authorization_file = os.path.join(SCRIPT_DIR, u"server10.2.ecp")
    database_name = datatype + time_ymdhms
    # arcpy.AddMessage(database_name)
    arcpy.CreateEnterpriseGeodatabase_management(database_platform=u"PostgreSQL", instance_name=u"localhost",
                                                 database_name=database_name, account_authentication=u"DATABASE_AUTH",
                                                 database_admin=u"postgres", database_admin_password=u"Lantucx2018",
                                                 sde_schema=u"SDE_SCHEMA", gdb_admin_name=u"sde",
                                                 gdb_admin_password=u"sde", tablespace_name=u"#",
                                                 authorization_file=authorization_file)

    connsdepath = SCRIPT_DIR
    connsde = datatype + time_ymdhms + u".sde"
    # arcpy.AddMessage(connsde)
    conn = {}
    conn[u"out_folder_path"] = connsdepath
    conn[u"out_name"] = connsde
    conn[u"database_platform"] = u"PostgreSQL"
    conn[u"instance"] = u"localhost"
    conn[u"account_authentication"] = u"DATABASE_AUTH"
    conn[u"database"] = database_name
    conn[u"username"] = u"sde"
    conn[u"password"] = u"sde"
    conn[u"save_user_pass"] = u"SAVE_USERNAME"
    arcpy.CreateDatabaseConnection_management(**conn)

    arcpy.env.workspace = gdbpath
    sdepath = os.path.join(SCRIPT_DIR, connsde)
    for ds in arcpy.ListDatasets(feature_type=u'feature') + [u'']:
        if ds != u'':
            dspath = os.path.join(gdbpath, ds)
            sdedspath = os.path.join(sdepath, ds)
            arcpy.Copy_management(dspath, sdedspath)
            # arcpy.AddMessage(dspath)
        else:
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                fcpath = os.path.join(gdbpath, ds, fc)
                sdedspath = os.path.join(sdepath, ds, fc)
                arcpy.Copy_management(fcpath, sdedspath)
                # arcpy.AddMessage(fcpath)
    return True


# 添加字段
def ARCGIS_add_field(mapindexsde):
    field_name = u'status'
    jtbname = u'.GBmaprange'
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    tablename = os.path.join(SCRIPT_DIR, mapindexsde, mapindexsde + u".DLG_50000", mapindexsde + jtbname)

    arcpy.AddField_management(in_table=tablename, field_name=field_name, field_type="TEXT", field_precision="#",
                              field_scale="#", field_length="100", field_alias="#", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="#")
    print u"添加 {0} 字段成功".format(field_name)


# 发布服务
def ARCGIS_service(service_name):
    print u"即将发布服务，请注册版本，修改所需字段属性并保存MXD文件"
    # time.sleep(300)
    print u"开始发布服务"
    MXD_name = service_name + u".mxd"
    wrkspc = os.path.dirname(os.path.abspath(__file__)) + "\\"
    print wrkspc + MXD_name
    mapDoc = arcpy.mapping.MapDocument(wrkspc + MXD_name)
    # con = "C:/Users/Administrator/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/arcgis on localhost_6080 (系统管理员).ags"
    con = "C:/Users/Administrator/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/arcgis on 192.168.3.120_6080 (系统管理员).ags"
    sddraft = wrkspc + service_name + '.sddraft'
    sd = wrkspc + service_name + '.sd'
    summary = 'Population Density by County'
    tags = 'county, counties, population, density, census'

    # 将地图文档(.mxd)文件转换为服务定义草稿(.sddraft)文件。
    analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service_name, 'ARCGIS_SERVER',
                                              con, True, None, summary, tags)

    # 如果sddraft分析不包含错误，则阶段化并上传服务
    if analysis['errors'] == {}:
        arcpy.StageService_server(sddraft, sd)
        arcpy.UploadServiceDefinition_server(sd, con)
        print u"服务发布成功"
    else:
        # 如果sddraft分析包含错误，则显示它们
        print analysis['errors']


# 修postgres数据库中regiontask表
def Posrgres_change_regiontask(regiontask_id, service_name):
    tablename = u"taskpackages_regiontask"
    status = u"处理完成"
    basemapservice = u"http://192.168.3.120:6080/arcgis/rest/services/ditu/MapServer"
    mapindexfeatureservice = u"http://192.168.3.120:6080/arcgis/rest/services/" + service_name + u"/FeatureServer"
    mapindexmapservice = u"http://192.168.3.120:6080/arcgis/rest/services/" + service_name + u"/MapServer"
    mapindexschedulemapservice = u"未指定"

    SQL = u"update %s set status='%s',basemapservice='%s',mapindexfeatureservice='%s',mapindexmapservice='%s',mapindexschedulemapservice='%s' where ID=%d" % (
        tablename, status, basemapservice, mapindexfeatureservice, mapindexmapservice, mapindexschedulemapservice,
        regiontask_id)
    Postgres_change(SQL)
    print u"postgres数据库更新成功"


# postgres数据库通用
def Postgres_change(SQL):
    conn = psycopg2.connect(dbname=u"mmanageV8.0",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    conn.close()


def aa(regiontask_filepath):
    file_dir = os.path.dirname(regiontask_filepath)

    fz = zipfile.ZipFile(regiontask_filepath, 'r')
    for file in fz.namelist():
        fz.extract(file, file_dir)


if __name__ == "__main__":
    service_name = "test05"

    # createregiontask(5, u'G:/RGSManager/media/data/2019/02/19/2019-02-19-14-48-04-601000/arcgis数据库.zip', service_name)
    # ARCGIS_service(service_name)
    # createregiontask(1, u'G:/RGSManager/media/data/2019/02/20/2019-02-20-17-35-43-515000/arcgis数据库.zip', service_name)
    # createregiontask(1,
    #                  u'D:/PycharmProjects/V9/RGSManager/media/data/2019/02/22/2019-02-22-14-50-42-196000/mmanageV7.rar',
    #                  "111")

    createregiontask(1,
                     u'D:/PycharmProjects/V9/RGSManager/media/data/2019/02/22/2019-02-22-14-50-42-196000/测试一下.zip',
                     "111")
