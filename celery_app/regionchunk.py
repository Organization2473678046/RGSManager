#!C:/Python27/ArcGIS10.2/python.exe
# -*- coding:utf-8 -*-
# from django.conf import settings

import hashlib
import sys
import os
import shutil
from datetime import datetime
import psycopg2

from RGSManager.settings import BASE_DIR
from celery_app import app
from ziptools import zipUpFolder
import zipfile

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManager.settings")


reload(sys)
sys.setdefaultencoding('utf8')

# @app.task
# def regionchunk(path, chunkmd5, name, chunk):
#     # 检验文件块md5
#     if os.path.isfile(path):
#         myhash = hashlib.md5()
#         f = open(path, 'rb')
#         while True:
#             b = f.read(8096)
#             if not b:
#                 break
#             myhash.update(b)
#         f.close()
#         print myhash.hexdigest()
#         if myhash.hexdigest() == chunkmd5:
#             # print u"文件切片MD5校验通过"
#             pass
#         else:
#             path = path.split("\\")
#             path.pop()
#             file_path = "\\".join(path)  # 读取文件块路径
#             shutil.rmtree(file_path)
#             instance = RegionTaskChunk.objects.filter(name=name, chunk=chunk).first()
#             instance.delete()
#             # raise serializers.ValidationError("区域:{0};文件切片编号:{1};MD5校验错误".format(name, chunk))
#             # print u"文件切片MD5校验错误"
#     else:
#         pass
#         # instance.delete()
#
#         # raise serializers.ValidationError("区域:{0};文件切片编号:{1};切片上传失败".format(name, chunk))
#
#
#     pass


@app.task
def regionmerge(path, filemd5, name, chunks):
    print BASE_DIR
    path_list = os.path.join(BASE_DIR, path).split("\\")
    path_list.pop()
    fromdir = "\\".join(path_list)  # 读取文件块路径
    filename = name  # 合成后文件名字
    save_path = os.path.join(BASE_DIR, u'media\\file\\{0}\\{1}\\{2}\\{3}'.format(
        datetime.now().strftime("%Y"),
        datetime.now().strftime("%m"),
        datetime.now().strftime("%d"),
        name))  # 合成后存放路径
    if not os.path.exists(save_path):  # 判断文件夹是否存在
        os.makedirs(save_path)
    outfile = open(os.path.join(save_path, filename), 'wb')  # 打开合并后存储文件夹
    num = 0
    # files = RegionTaskChunk.objects.filter(name=name).order_by("chunk")  # 读取文件块名字并根据块数排序
    SQL = U"SELECT name FROM taskpackages_regiontaskchunk WHERE NAME='%s' ORDER BY id"%(name)
    changedatabase(SQL)
    files = ''
    while num < chunks:  # 判断合并文件次数
        file = files.values_list("file")[num][0].split("/")[-1]  # 获取单个文件名
        filepath = os.path.join(fromdir, file)
        infile = open(filepath, 'rb')
        data = infile.read()
        outfile.write(data)
        del data
        num += 1
        infile.close()
    outfile.close()

    # 校验合并后文件md5
    file = save_path + "\\" + filename  # 获取合并后文件路径
    if os.path.isfile(file):  # 判断文件是否存在
        myhash = hashlib.md5()
        f = open(file, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        print myhash.hexdigest()
        if myhash.hexdigest() == filemd5:  # 判断MD5是否与前端传的数据一致
            print u"合成后MD5校验通过"
            SQL = u"UPDATE taskpackages_regiontask set status='%s' where name='%s'" % (u"MD5校验通过", name)
            changedatabase(SQL)
        else:
            shutil.rmtree(save_path)
            shutil.rmtree(fromdir)
            print u"合成后MD5校验错误"
            # raise serializers.ValidationError("文件{0}MD5校验错误".format(instance.name))
    else:
        pass
        # raise serializers.ValidationError("文件{0}切片丢失".format(instance.name))




def changedatabase(SQL):
    conn = psycopg2.connect(dbname=u"mmanageV8.0",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    conn.close()
    print u"文件合成校验成功"

def changedatabase1(SQL):
    conn = psycopg2.connect(dbname=u"mmanageV8.0",
                            user=u"postgres",
                            password=u"Lantucx2018",
                            host=u"localhost",
                            port=u"5432")
    
    cur = conn.cursor()
    cur.execute(SQL)
    conn.commit()
    a = cur.fetchall()
    print a
    conn.close()
    print u"文件合成校验成功"




if __name__ == '__main__':
    SQL = "SELECT file FROM taskpackages_regiontaskchunk WHERE filemd5='49682eb9313c6889c83f7657730f64e6'"
    changedatabase1(SQL)