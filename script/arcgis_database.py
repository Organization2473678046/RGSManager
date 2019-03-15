#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import urllib
import urllib2
from datetime import datetime
import arcpy
import xml.dom.minidom as DOM
import json

import psycopg2


reload(sys)
sys.setdefaultencoding('utf8')



# 创建空间库
def ARCGIS_create_database(gdbpath, time_ymdhms, datatype):

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    authorization_file = os.path.join(SCRIPT_DIR, u"server10.2.ecp")
    database_name = datatype + time_ymdhms
    arcpy.CreateEnterpriseGeodatabase_management(database_platform=u"PostgreSQL", instance_name=u"localhost",
                                                 database_name=database_name,
                                                 account_authentication=u"DATABASE_AUTH",
                                                 database_admin=u"postgres", database_admin_password=u"Lantucx2018",
                                                 sde_schema=u"SDE_SCHEMA", gdb_admin_name=u"sde",
                                                 gdb_admin_password=u"sde", tablespace_name=u"#",
                                                 authorization_file=authorization_file)
    connsdepath = SCRIPT_DIR
    connsde = database_name + u".sde"
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
        else:
            for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
                fcpath = os.path.join(gdbpath, ds, fc)
                sdedspath = os.path.join(sdepath, ds, fc)
                arcpy.Copy_management(fcpath, sdedspath)
    print u'创建空间库成功'
    return datatype + time_ymdhms + ".sde"



# 添加字段
def ARCGIS_add_field(new_mapindexsde, field_name, new_sde):
    jtbname = u'.GBmaprange' + new_sde
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    tablename = os.path.join(SCRIPT_DIR, new_mapindexsde, new_mapindexsde + u".DLG_50000", new_mapindexsde + jtbname)

    arcpy.AddField_management(in_table=tablename, field_name=field_name, field_type="TEXT", field_precision="#",
                              field_scale="#", field_length="100", field_alias="#", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="#")
    print u"{0} 添加 {1} 字段成功".format(new_mapindexsde, field_name)


# 添加任务包名称
def ARCGIS_add_taskpackage(new_mapindexsde):
    conn = psycopg2.connect(dbname=u"mmanageV0.10",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    # Postgres数据库连接
    SQL = "SELECT name,mapnums FROM taskpackages_taskpackage"
    cur = conn.cursor()
    cur.execute(SQL)

    # arcgis数据库连接
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    workspace = os.path.join(SCRIPT_DIR, new_mapindexsde)
    sde_conn = arcpy.ArcSDESQLExecute(workspace)

    while True:
        data = cur.fetchone()
        if data:
            """插入数据"""
            taskpackage_name = data[0]
            mapnum_list = data[1].split(",")
            new_jtb = new_mapindexsde + u".GBmaprange"
            for mapnum in mapnum_list:
                col = "new_jbmapn"
                sql = "update {0} set {1} = '{2}' where {3} = '{4}'".format(new_jtb, "taskpackage_name", taskpackage_name, col, mapnum)
                try:
                    print sql
                    sde_conn.execute(sql)
                except Exception as e:
                    print str(e).encode('utf8')
        else:
            conn.close()
            break
    sde_conn.commitTransaction()
    del sde_conn
    print "arcgis任务包名称修改完成"



def ARCGIS_add_mapnums_schedule(new_mapindexsde, new_name):
    conn = psycopg2.connect(dbname=u"mmanageV0.10",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    # Postgres数据库连接
    SQL = "SELECT name,mapnums,schedule FROM taskpackages_taskpackage"
    cur = conn.cursor()
    cur.execute(SQL)

    # arcgis数据库连接
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    workspace = os.path.join(SCRIPT_DIR, new_mapindexsde)
    sde_conn = arcpy.ArcSDESQLExecute(workspace)

    while True:
        data = cur.fetchone()
        if data:
            """插入数据"""
            new_jtb = new_mapindexsde + u".GBmaprange" + new_name
            sql = "update {0} set mapnum = '{1}',schedule='{2}' where {3} = '{4}'".format(new_jtb, data[1], data[2], "taskpackage_name", data[0])
            try:
                print sql
                sde_conn.execute(sql)
            except Exception as e:
                print str(e).encode('utf8')
        else:
            conn.close()
            break
    sde_conn.commitTransaction()
    del sde_conn
    print "arcgis图号进度添加完成"


# 根据任务包名称融合，生成新的要素类
def ARCGIS_dissolve(mapindexsde, new_name):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    in_features = os.path.join(SCRIPT_DIR, mapindexsde, mapindexsde + u".DLG_50000", mapindexsde + u".GBmaprange")
    out_feature_class = in_features + new_name
    arcpy.Dissolve_management(
        in_features=in_features,
        out_feature_class=out_feature_class,
        dissolve_field="taskpackage_name", statistics_fields="#", multi_part="SINGLE_PART",
        unsplit_lines="DISSOLVE_LINES")

    print "合并成功:{0}".format(out_feature_class)
    return out_feature_class


# 发布服务
def ARCGIS_publishService(service_name, old_mapindexsde, new_mapindexsde, old_MXD, new_name):
    print u"开始发布服务----------"

    """更换mxd文件数据源,返回新的mxd文件"""
    new_mxdfile = ARGIS_replaceDataSource(service_name, old_mapindexsde, new_mapindexsde, old_MXD, new_name)

    # MXD_name = service_name + u".mxd"
    wrkspc = os.path.dirname(os.path.abspath(__file__)) + "/"
    # print wrkspc + MXD_name
    # mapDoc = arcpy.mapping.MapDocument(wrkspc + MXD_name)
    mapDoc = arcpy.mapping.MapDocument(new_mxdfile)
    con = u"C:/Users/Administrator/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/arcgis on localhost_6080 (系统管理员).ags"

    sddraft_name = wrkspc + service_name
    sddraft = sddraft_name + '.sddraft'
    sd = wrkspc + service_name + '.sd'
    summary = 'Population Density by County'
    tags = 'county, counties, population, density, census'

    # 将地图文档(.mxd)文件转换为服务定义草稿(.sddraft)文件。
    arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service_name, 'ARCGIS_SERVER', con, True, None, summary, tags)

    # 添加要素服务
    new_sddraft = ARGIS_addFeatureService(sddraft_name)

    # 注册数据库
    connection_name = service_name + datetime.now().strftime("%Y%m%d%H%M%S")
    ARGIS_registerDB(connection_name, new_mapindexsde, con)

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

    # 如果sddraft分析不包含错误，则阶段化并上传服务
    if analysis['errors'] == {}:
        # 执行StageService,这将创建服务定义
        arcpy.StageService_server(new_sddraft, sd)

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
def ARGIS_replaceDataSource(service_name, old_mapindexsde, new_mapindexsde, old_MXD, new_name):
    print u'开始修改mxd文件数据源'
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    old_datasource = os.path.join(SCRIPT_DIR, old_mapindexsde)
    new_datasource = os.path.join(SCRIPT_DIR, new_mapindexsde)
    old_mxdfile = os.path.join(SCRIPT_DIR, old_MXD)

    mxd = arcpy.mapping.MapDocument(old_mxdfile)
    mxd.findAndReplaceWorkspacePaths(old_datasource, new_datasource, False)
    # 获取mxd文件的图层
    lyr = arcpy.mapping.ListLayers(mxd)[0]
    print lyr
    dataset_name = new_mapindexsde + '.GBmaprange' + new_name   # 此处应该是新的要素类
    lyr.replaceDataSource(new_datasource, "SDE_WORKSPACE", dataset_name)
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

    doc = DOM.parse(old_sddraft)
    typeNames = doc.getElementsByTagName('TypeName')
    for typeName in typeNames:
        if typeName.firstChild.data == soe:
            extention = typeName.parentNode
            for extElement in extention.childNodes:
                if extElement.tagName == 'Enabled':
                    extElement.firstChild.data = 'true'
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
    db_conn = mapindexsde
    print con
    print db_conn
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
    urllib2.urlopen(delete_service_url, ' ').read()




def main():

    """
    接收文件，与地区名称，确定是否创建新的空间库
    如果没有对应区域，注入rgs和接图表生成服务
    如果有对应区域，将rgs注入数据库，将接图表遍历判断是否与第一个有不同处，将第二个接图表融合到第一个中

    :return:
    """










    """创建空间库,接收两个gdb文件，生成对应的sde文件并返回"""
    gdbpath = "E:/RGSManager/script/"
    time_ymdhms = datetime.now().strftime(u"%Y%m%d%H%M%S")
    new_rgssde = ARCGIS_create_database(gdbpath=gdbpath+"RGS.gdb", time_ymdhms=time_ymdhms, datatype="rgs")
    new_mapindexsde = ARCGIS_create_database(gdbpath=gdbpath+"接图表.gdb", time_ymdhms=time_ymdhms, datatype="mapindex")


    """添加taskpackage_name字段用于融合"""
    field_name = u'taskpackage_name'
    new_name = ''
    ARCGIS_add_field(new_mapindexsde, field_name, new_name)


    """根据postgres数据库填充任务包名称字段"""
    ARCGIS_add_taskpackage(new_mapindexsde)


    """按任务包名称融合生成新的要素类"""
    new_name = "01"
    ARCGIS_dissolve(new_mapindexsde, new_name)


    """融合后添加图号字段和进度字段"""
    field_name = "mapnum"
    ARCGIS_add_field(new_mapindexsde, field_name, new_name)
    field_name = "schedule"
    ARCGIS_add_field(new_mapindexsde, field_name, new_name)
    """添加图号字段和进度字段后填充数据"""
    ARCGIS_add_mapnums_schedule(new_mapindexsde, new_name)


    """发服务,接收新旧mapindexsde文件用于更换数据源，service_name为服务名称，服务名称不可重复"""
    service_name = "test_merge01"
    old_rgssde = u"rgs20190301165155.sde"
    old_mapindexsde = "mapindex20190301165155.sde"
    old_MXD = "test_merge.mxd"
    ARCGIS_publishService(service_name, old_mapindexsde, new_mapindexsde, old_MXD, new_name)

    pass

if __name__ == '__main__':
    main()
