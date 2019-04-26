#!C:/Python27/ArcGIS10.2/python.exe
#-*- coding:utf-8 -*-
"""
#============================================
#
# Project: RGSManager
# Name: The file name is create_gis_server_connect_file
# Purpose: 
# Auther: w176177082
# Tel: 17372796660
#
#============================================
#
"""

import arcpy
import socket
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def create_gis_server_connect_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_name = u"connect.ags"
    agsfile=os.path.join(script_dir,out_name)
    if not os.path.exists(agsfile):
        print u"开始创建连接ArcGIS Server的ags文件"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        outdir = script_dir
        out_folder_path = outdir
        localhostip=get_localhost_ip()
        server_url = u"http://{}:6080/arcgis/admin".format(localhostip)
        use_arcgis_desktop_staging_folder = False
        staging_folder_path = outdir
        username = u"siteadmin"
        password = u"Lantucx2018"

        arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                    out_folder_path,
                                                    out_name,
                                                    server_url,
                                                    "ARCGIS_SERVER",
                                                    use_arcgis_desktop_staging_folder,
                                                    staging_folder_path,
                                                    username,
                                                    password,
                                                    "SAVE_USERNAME")
        print u"连接ArcGIS Server的ags文件创建成功"

        return True

def get_localhost_ip():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return ip


if __name__ == "__main__":
    create_gis_server_connect_file()
    #get_localhost_ip()
    #create_gis_server_connect_file()
