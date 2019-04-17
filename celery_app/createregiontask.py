#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import sys
import os
import arcpy
import json
import urllib
import urllib2
from datetime import datetime
import psycopg2
from unrar import rarfile
import time
import chardet
from celery_app import app
from ziptools import zipUpFolder
import zipfile
import xml.dom.minidom as DOM

reload(sys)
sys.setdefaultencoding('utf8')


@app.task
def createregiontask(regiontask_id, regiontask_filepath):
    service_name = 'mmanage' + str(regiontask_id)
    file_dir = os.path.dirname(regiontask_filepath)         # 解压后文件保存路径
    file_name = os.path.basename(regiontask_filepath)       # 文件名
    z = zipfile.is_zipfile(regiontask_filepath)
    r = rarfile.is_rarfile(regiontask_filepath)
    if z:
        # -ibck: 后台运行; -o+:覆盖已存在文件
        rar_command = '"C:\Program Files\WinRAR\WinRAR.exe" x %s %s -ibck -o+' % (regiontask_filepath, file_dir)
        rar_command = rar_command.encode('gbk')
        os.system(rar_command)
        print rar_command.decode('gbk')
        print u"解压 {0} 成功".format(file_name)
    elif r:
        fz = rarfile.RarFile(regiontask_filepath, 'r')
        for file in fz.namelist():
            fz.extract(file, file_dir)
        print u"解压 {0} 成功".format(file_name)
    else:
        print(u'This is not zip or rar')
        return False

    time_ymdhms = datetime.now().strftime(u"%Y%m%d%H%M%S")
    dir_list = os.listdir(file_dir)

    # 创建空间库
    print u"开始创建空间库"
    for dir in dir_list:
        dir_abspath = os.path.join(file_dir, dir)
        if os.path.isdir(dir_abspath):
            for subdir in os.listdir(dir_abspath):
                if subdir.startswith(u"接图表"):
                    gdbpath = os.path.join(dir_abspath, subdir)
                    datatype = u"mapindex"
                    ARCGIS_create_database(gdbpath, time_ymdhms, datatype)

                elif subdir.startswith(u"GBRGS"):
                    gdbpath = os.path.join(dir_abspath, subdir)
                    datatype = u"gbrgs"
                    ARCGIS_create_database(gdbpath, time_ymdhms, datatype)

                elif subdir.startswith(u"JBRGS"):
                    gdbpath = os.path.join(dir_abspath, subdir)
                    datatype = u"jbrgs"
                    ARCGIS_create_database(gdbpath, time_ymdhms, datatype)

        if dir.startswith(u"接图表"):
            gdbpath = os.path.join(file_dir, dir)
            datatype = u"mapindex"
            ARCGIS_create_database(gdbpath, time_ymdhms, datatype)
            # print u"创建mapindex数据库成功"
        elif dir.startswith(u"GBRGS"):
            gdbpath = os.path.join(file_dir, dir)
            datatype = u"gbrgs"
            ARCGIS_create_database(gdbpath, time_ymdhms, datatype)

        elif dir.startswith(u"JBRGS"):
            gdbpath = os.path.join(file_dir, dir)
            datatype = u"jbrgs"
            ARCGIS_create_database(gdbpath, time_ymdhms, datatype)

    print u'创建空间库成功'

    mapindexsde = "mapindex" + time_ymdhms + ".sde"
    gbrgssde = "gbrgs" + time_ymdhms + ".sde"
    jbrgssde = "jbrgs" + time_ymdhms + ".sde"
    # mmanage.mxd对应的mapindexsde,要放在当前目录下
    # old_mapindexsde = "mapindex20181137133843.sde"
    old_mapindexsde = "mapindex20181206202724.sde"
    # old_mapindexsde = "mapindex20190417154204.sde"

    # 注册版本,第一个参数为要注册版本的数据集的名称
    print u'开始注册版本'
    mapindexsde_dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)), mapindexsde,
                                       mapindexsde + u".DLG_50000")
    gbrgssde_dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)), gbrgssde, gbrgssde + u".DLG_K050")
    jbrgssde_dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)), jbrgssde, jbrgssde + u".DLG_K050")

    arcpy.RegisterAsVersioned_management(mapindexsde_dataset, u'EDITS_TO_BASE')
    arcpy.RegisterAsVersioned_management(gbrgssde_dataset, u'EDITS_TO_BASE')
    arcpy.RegisterAsVersioned_management(jbrgssde_dataset, u'EDITS_TO_BASE')
    print u'注册版本成功'

    # 添加用于标记颜色的status字段
    ARCGIS_add_field(mapindexsde)

    # 发布服务
    is_successfull = ARCGIS_publishService(service_name, old_mapindexsde, mapindexsde)

    if is_successfull:
        # 填充postgresql中对应字段
        Posrgres_change_regiontask(regiontask_id, service_name, mapindexsde, gbrgssde_dataset, jbrgssde_dataset)
        return True
    else:
        return False


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
    # connsde = datatype + time_ymdhms + u".sde"
    connsde = database_name + u".sde"
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

    # print u"创建空间库成功"
    # return True


# 添加字段
def ARCGIS_add_field(mapindexsde):
    field_name = u'status_test'
    jtbname = u'.GBmaprange'
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    tablename = os.path.join(SCRIPT_DIR, mapindexsde, mapindexsde + u".DLG_50000", mapindexsde + jtbname)

    arcpy.AddField_management(in_table=tablename, field_name=field_name, field_type="TEXT", field_precision="#",
                              field_scale="#", field_length="100", field_alias="#", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="#")
    print u"{0} 添加 {1} 字段成功".format(mapindexsde, field_name)


# 发布服务
def ARCGIS_publishService(service_name, old_mapindexsde, mapindexsde):
    print u"开始发布服务----------"

    # 更换mxd文件数据源,返回新的mxd文件
    new_mxdfile = ARGIS_replaceDataSource(service_name, old_mapindexsde, mapindexsde)

    # MXD_name = service_name + u".mxd"
    wrkspc = os.path.dirname(os.path.abspath(__file__)) + "/"
    # print wrkspc + MXD_name
    # mapDoc = arcpy.mapping.MapDocument(wrkspc + MXD_name)
    mapDoc = arcpy.mapping.MapDocument(new_mxdfile)
    # con = u"C:/Users/Administrator/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/arcgis on 192.168.3.120_6080 (系统管理员).ags"
    con = u"C:/Users/Administrator/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/arcgis on localhost_6080 (系统管理员).ags"

    sddraft_name = wrkspc + service_name
    sddraft = sddraft_name + '.sddraft'
    sd = wrkspc + service_name + '.sd'
    summary = 'Population Density by County'
    tags = 'county, counties, population, density, census'

    # 将地图文档(.mxd)文件转换为服务定义草稿(.sddraft)文件。
    arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service_name, 'ARCGIS_SERVER',
                                   con, True, None, summary, tags)

    # 添加要素服务
    new_sddraft = ARGIS_addFeatureService(sddraft_name)

    # 注册数据库
    connection_name = service_name + datetime.now().strftime("%Y%m%d%H%M%S")
    ARGIS_registerDB(connection_name, mapindexsde, con)

    # 分析草稿
    # Analyze the service definition draft
    analysis = arcpy.mapping.AnalyzeForSD(new_sddraft)
    print "The following information was returned during analysis of the MXD:"
    for key in ('messages', 'warnings', 'errors'):
        print '----' + key.upper() + '---'
        vars = analysis[key]
        for ((message, code), layerlist) in vars.iteritems():
            print '    ', message, ' (CODE %i)' % code
            print '       applies to:',
            for layer in layerlist:
                print layer.name,
            print

    # Stage and upload the service if the sddraft analysis did not contain errors
    # 如果sddraft分析不包含错误，则阶段化并上传服务
    if analysis['errors'] == {}:
        # 执行StageService,这将创建服务定义
        arcpy.StageService_server(new_sddraft, sd)
        # 执行UploadServiceDefinition,这将上传服务定义并发布服务
        # try:
        #     arcpy.UploadServiceDefinition_server(sd, con)
        # except:
        #     ARGIS_deleteservice("localhost", service_name + ".MapServer", "siteadmin", "Lantucx2018")
        #     print u'服务 {} 发布失败,正在尝试第二次'.format(service_name)
        #     try:
        #         arcpy.UploadServiceDefinition_server(sd, con)
        #     except:
        #         if os.path.dirname(new_mxdfile):
        #             os.remove(new_mxdfile)
        #         if os.path.exists(sd):
        #             os.remove(sd)
        #         return u"服务发布失败"
        #     else:
        #         # print u"服务发布成功"
        #         print "Service successfully published"
        #         if os.path.exists(sd):
        #             os.remove(sd)
        # else:
        #     # print u"服务发布成功"
        #     print "Service successfully published"
        # if os.path.exists(sd):
        #     os.remove(sd)
        count = 1
        while True:
            count += 1
            try:
                arcpy.UploadServiceDefinition_server(sd, con)
            except:
                ARGIS_deleteservice("localhost", service_name + ".MapServer", "siteadmin", "Lantucx2018")
                print u'服务 {0} 发布失败,正在尝试第{1}次'.format(service_name,str(count))
            else:
                print "Service successfully published"
                if os.path.exists(sd):
                    os.remove(sd)
                break
        return True
    else:
        # 如果sddraft分析包含错误，则显示它们
        print analysis['errors']
        print "Service could not be published because errors were found during analysis."
        return False


# 修改mxd文件数据源
def ARGIS_replaceDataSource(service_name, old_mapindexsde, mapindexsde):
    print u'开始修改mxd文件数据源'
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    old_datasource = os.path.join(SCRIPT_DIR, old_mapindexsde)
    new_datasource = os.path.join(SCRIPT_DIR, mapindexsde)
    old_mxdfile = os.path.join(SCRIPT_DIR, 'mmanage.mxd')


    mxd = arcpy.mapping.MapDocument(old_mxdfile)
    mxd.findAndReplaceWorkspacePaths(old_datasource, new_datasource, False)
    # 获取mxd文件的图层
    lyr = arcpy.mapping.ListLayers(mxd)[0]
    print lyr
    # lyr.replaceDataSource("D:\PycharmProjects\ClipTask\mapindex20190215145916.sde","SDE_WORKSPACE","DLG_50000")
    dataset_name = mapindexsde + '.GBmaprange'
    lyr.replaceDataSource(new_datasource, "SDE_WORKSPACE", dataset_name)
    # lyr.name = "mapindex20190215145916.sde.GBmaprange"
    lyr.name = dataset_name
    new_mxdfile_name = service_name + '.mxd'
    new_mxdfile = os.path.join(SCRIPT_DIR, new_mxdfile_name)
    mxd.saveACopy(new_mxdfile)
    del mxd
    print u"修改mxd文件数据源成功"
    return new_mxdfile


# 添加要素服务
def ARGIS_addFeatureService(sddraft_name):
    print u'开始添加要素服务'
    # sddraft = "C:/Users/ltcx/AppData/Local/ESRI/Desktop10.2/Staging/arcgis on localhost_6080 (系统管理员)/20191111test.sddraft"
    old_sddraft = sddraft_name + '.sddraft'
    soe = 'FeatureServer'
    soeProperty = 'title'
    soePropertyValue = 'USACounties'

    # Read the sddraft xml.
    doc = DOM.parse(old_sddraft)
    # Find all elements named TypeName. This is where the server object extension (SOE) names are defined.
    typeNames = doc.getElementsByTagName('TypeName')
    for typeName in typeNames:
        # Get the TypeName whose properties we want to modify.
        if typeName.firstChild.data == soe:
            extention = typeName.parentNode
            for extElement in extention.childNodes:
                # Enabled SOE.
                if extElement.tagName == 'Enabled':
                    extElement.firstChild.data = 'true'
                # Modify SOE property. We have to drill down to the relevant property.
                if extElement.tagName == 'Props':
                    for propArray in extElement.childNodes:
                        for propSet in propArray.childNodes:
                            for prop in propSet.childNodes:
                                if prop.tagName == "Key":
                                    if prop.firstChild.data == soeProperty:
                                        if prop.nextSibling.hasChildNodes():
                                            prop.nextSibling.firstChild.data = soePropertyValue
                                        else:
                                            txt = doc.createTextNode(soePropertyValue)
                                            prop.nextSibling.appendChild(txt)

    # outXml = "C:/Users/ltcx/AppData/Local/ESRI/Desktop10.2/Staging/arcgis on localhost_6080 (系统管理员)/20191111test1.sddraft"
    outXml = sddraft_name + '1' + ".sddraft"
    f = open(outXml, 'w')
    doc.writexml(f)
    f.close()
    print u'添加要素服务成功'
    if os.path.exists(old_sddraft):
        os.remove(old_sddraft)
    return outXml


# 注册数据库
def ARGIS_registerDB(connection_name, mapindexsde, con):
    print u'开始注册数据库'
    # con = "C:/Users/ltcx/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/arcgis on localhost_6080 (系统管理员).ags"
    # server_conn = "c:/connections/MYSERVER.ags"
    # db_conn = "D:/PycharmProjects/ClipTask/mapindex20190220100911.sde"
    db_conn = mapindexsde
    print con
    print db_conn
    # arcpy.AddDataStoreItem(con, "DATABASE", "Wilma", db_conn, db_conn)
    # 每次注册数据库第3个参数不能一样
    arcpy.AddDataStoreItem(con, "DATABASE", connection_name, db_conn, db_conn)
    print u'注册数据库成功'


# 生成token
def ARGIS_gentoken(url, username, password, expiration=60):
    query_dict = {'username': username,
                  'password': password,
                  'expiration': str(expiration),
                  'client': 'requestip'}
    query_string = urllib.urlencode(query_dict)
    return json.loads(urllib.urlopen(url + "?f=json", query_string).read())['token']


# 删除服务
def ARGIS_deleteservice(server, servicename, username, password, token=None, port=6080):
    if token is None:
        token_url = "http://{}:{}/arcgis/admin/generateToken".format(server, port)
        print token_url
        token = ARGIS_gentoken(token_url, username, password)
    delete_service_url = "http://{}:{}/arcgis/admin/services/{}/delete?token={}".format(server, port, servicename,
                                                                                        token)
    urllib2.urlopen(delete_service_url, ' ').read()  # The ' ' forces POST


# 修postgres数据库中regiontask表
def Posrgres_change_regiontask(regiontask_id, service_name, mapindexsde, gbrgssde, jbrgssde):
    print u"正在更新PostgreSQL数据库"
    tablename = u"taskpackages_regiontask"
    status = u"处理完成"
    basemapservice = u"http://192.168.3.120:6080/arcgis/rest/services/ditu/MapServer"
    mapindexfeatureservice = u"http://192.168.3.120:6080/arcgis/rest/services/" + service_name + u"/FeatureServer"
    mapindexmapservice = u"http://192.168.3.120:6080/arcgis/rest/services/" + service_name + u"/MapServer"
    # mapindexschedulemapservice = u"未指定"
    mapindexsde_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), mapindexsde)
    gbrgssde_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), gbrgssde)
    jbrgssde_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), jbrgssde)

    SQL = u"update %s set status='%s',basemapservice='%s',mapindexfeatureservice='%s',mapindexmapservice='%s',mapindexsde='%s',gbrgssde='%s', jbrgssde='%s' where ID=%d" % (
        tablename, status, basemapservice, mapindexfeatureservice, mapindexmapservice,
        mapindexsde_filepath, gbrgssde_filepath, jbrgssde_filepath,regiontask_id)
    Postgres_executeSQL(SQL)
    print u"PostgreSQL数据库更新成功"


# PostgresSQL数据库通用,执行SQL语句
def Postgres_executeSQL(SQL):
    conn = psycopg2.connect(dbname=u"mmanageV0.10",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    conn.close()


import arcpy
# 补充图号属性
def append_mapnums():
    conn = psycopg2.connect(dbname=u"mmanageV0.10",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    SQL = "SELECT name,file FROM taskpackages_taskpackage"
    cur.execute(SQL)
    name_file = cur.fetchall()
    print name_file
    file_path = ''

    file_dir = os.path.dirname(file_path)         # 解压后文件保存路径
    file_name = os.path.basename(file_path)       # 文件名

    z = zipfile.is_zipfile(file_path)
    r = rarfile.is_rarfile(file_path)
    if z:
        # -ibck: 后台运行; -o+:覆盖已存在文件
        rar_command = '"C:\Program Files\WinRAR\WinRAR.exe" x %s %s -ibck -o+' % (file_path, file_dir)
        rar_command = rar_command.encode('gbk')
        os.system(rar_command)
        print rar_command.decode('gbk')
        print u"解压成功"
    elif r:
        fz = rarfile.RarFile(file_path, 'r')
        for file in fz.namelist():
            fz.extract(file, file_dir)
        print u"解压成功"
    else:
        print(u'This is not zip or rar')
        return False


    taskpath =u"E:\\RGSManager\\celery_app\\测试融合\\Source"
    path = os.path.join(taskpath, u"接图表.gdb", u"DLG_50000", u"GBmaprange")
    # 查找任务包名字和图号
    cursor = arcpy.da.SearchCursor(path, ["new_jbmapn"])
    taskpackage_name = "任务包1号"
    try:

        for row in cursor:
            SQL = "SELECT mapnums from taskpackages_taskpackage where name='{0}'".format(taskpackage_name)  # 按任务包名字查询原mapnums
            cur.execute(SQL)
            mapnums = cur.fetchall()
            old_mapnum = mapnums[0][0]      # 提取原有mapnums

            if old_mapnum is None:
                SQL = "UPDATE taskpackages_taskpackage set mapnums='{0}' where name='{1}'".format(row[0], taskpackage_name)
            else:
                SQL = "UPDATE taskpackages_taskpackage set mapnums='{0}' where name='{1}'".format(old_mapnum +","+ row[0], taskpackage_name)
            print SQL                       # 添加mapnums
            cur.execute(SQL)
            conn.commit()
        conn.close()
    except Exception as e:
        # e = str(e).decode('gbk')
        print [e, ]




if __name__ == "__main__":
    # service_name = "test05"
    createregiontask(01, u'E:\\RGSManager\\media\\data\\DATA.rar')
    # ARCGIS_publishService(service_name)
    # createregiontask(1, u'G:/RGSManager/media/data/2019/02/20/2019-02-20-17-35-43-515000/arcgis数据库.zip', service_name)
    # createregiontask(1,
    #                  u'D:/PycharmProjects/V9/RGSManager/media/data/2019/02/22/2019-02-22-14-50-42-196000/mmanageV7.rar',
    #                  "111")

    # createregiontask(1,
    #                  u'D:/PycharmProjects/V9/RGSManager/media/data/2019/02/22/2019-02-22-14-50-42-196000/测试一下.zip',
    #                  "111")
    # ARGIS_replaceDataSource('mmanage3', )

    # append_mapnums()

    pass
