#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   filetools.py
@Time    :   2019/04/20 23:52:37
@Author  :   jiegemena 
@Version :   1.0
@Contact :   jiegemena@outlook.com
@Desc    :   None
'''

# here put the import lib

import os
import requests 
import os.path 
import shutil 
import time, datetime

def downfiles(durl,fielpath=None):
    if fielpath is None or len(fielpath) > 0:
        fielpath = durl
    print("downloading with requests",fielpath,durl)
    mkdir(os.path.dirname(fielpath) )

    r = requests.get(durl) 
    with open(fielpath, "wb") as code:
        code.write(r.content)


def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False


def copydir(oldf,newf):
    '''
    - copy dir
    '''
    shutil.copy(oldf, newf)

def copyfile(oldf,newf):
    '''
    copy file
    '''
    for root, dirs, files in os.walk(oldf):
        filenametmp = newf + root
        if filenametmp.find('__pycache__') >= 0:
            continue
        mkdir(filenametmp)
        for f in files:
            shutil.copy(root + '/' + f, filenametmp)

        print('root',root) #当前目录路径  
        # print('dirs',dirs) #当前路径下所有子目录  
        print('files',files) #当前路径下所有非目录子文件 