# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys,os

kilobytes = 1024
megabytes = kilobytes*1000
chunksize = int(200*megabytes)

def split(fromfile,todir,chunksize=chunksize):
    if not os.path.exists(todir):
        os.mkdir(todir)
    else:
        for fname in os.listdir(todir):
            os.remove(os.path.join(todir,fname))
    partnum = 0
    inputfile = open(fromfile,'rb')
    while True:
        chunk = inputfile.read(chunksize)
        if not chunk:
            break
        partnum += 1
        filename = os.path.join(todir,('part%04d'%partnum))
        fileobj = open(filename,'wb')
        if partnum:
            fileobj.write(chunk)
        fileobj.close()
    return partnum

def split1():
    fromfile  = "gb.gdb.rar"
    todir     = "test"
    chunksize = 10240000
    absfrom,absto = map(os.path.abspath,[fromfile,todir])
    try:
        parts = split(fromfile,todir,chunksize)
    except:
        print 'Error during split:'
        print sys.exc_info()[0],sys.exc_info()[1]
    else:
        print u'被划分文件:', absfrom, u',划分后存储路径:',absto,u'单个文件大小',chunksize, u'划分个数',parts




def joinfile(fromdir,filename,todir):
    if not os.path.exists(todir):
        os.mkdir(todir)
    if not os.path.exists(fromdir):
        print u"没有%s文件夹"%fromdir
    outfile = open(os.path.join(todir,filename),'wb')
    files = os.listdir(fromdir) #list all the part files in the directory
    files.sort()                #sort part files to read in order
    for file in files:
        filepath = os.path.join(fromdir,file)
        infile = open(filepath,'rb')
        data = infile.read()
        outfile.write(data)
        infile.close()
    outfile.close()


def joinfile2():
    fromdir = "test"
    filename = "gb.gdb.rar"
    todir   = "test2"
    try:
        joinfile(fromdir,filename,todir)
    except:
        print u"文件合并错误"
        print(sys.exc_info()[0],sys.exc_info()[1])

if __name__=='__main__':

    split1()
    joinfile2()

