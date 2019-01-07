#!C:/Python27/ArcGIS10.2/python.exe
#-*- coding:utf-8 -*-
"""
#============================================
#
# Project: RGSManager
# Name: The file name is ziptools
# Purpose: 
# Auther: Administrator
# Tel: 17372796660
#
#============================================
#
"""

import sys
import os
import zipfile

reload(sys)
sys.setdefaultencoding('utf8')

def zipUpFolder(folder, outZipFile):
    # zip the data
    try:
        zip = zipfile.ZipFile(outZipFile, 'w', zipfile.ZIP_DEFLATED)
        zipws(unicode(folder), zip, "CONTENTS_ONLY")
        zip.close()
    except RuntimeError:
        # Delete zip file if exists
        if os.path.exists(outZipFile):
            os.unlink(outZipFile)
        zip = zipfile.ZipFile(outZipFile, 'w', zipfile.ZIP_STORED)
        zipws(unicode(folder), zip, "CONTENTS_ONLY")
        zip.close()

def zipws(path, zip, keep):
    path = os.path.normpath(path)
    for (dirpath, dirnames, filenames) in os.walk(path):
        # Iterate over every filename
        for file in filenames:
            # Ignore .lock files
            if not file.endswith('.lock'):
                try:
                    if keep:
                        zip.write(os.path.join(dirpath, file),
                        os.path.join(os.path.basename(path), os.path.join(dirpath, file)[len(path)+len(os.sep):]))
                    else:
                        zip.write(os.path.join(dirpath, file),
                        os.path.join(dirpath[len(path):], file))

                except Exception as e:
                    #Message "    Error adding %s: %s"
                    print "zip error"

    return None




