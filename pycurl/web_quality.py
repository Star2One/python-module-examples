#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *.py
# Copyright (C)  chris.hill 2014 <sysse2009#gmail.com>
#
 
"""
    @author: chris.hill <sysse2009#gmail.com >
    @copyright: (C) 2014 chris.hill
    @license: GNU General Public License version 2.0 (GPLv2)
    @version: 0.1
    @refer: http://book.51cto.com/art/201411/456735.htm
"""

import os
import sys
import time
import pycurl

NAME = sys.argv[0]

try:
    URL = sys.argv[1]
except Exception,e:
    print "Error" + str(e)
    print "Usage: %s URL" %(NAME)
    sys.exit()

site = pycurl.Curl()
site.setopt(pycurl.URL, URL)
site.setopt(pycurl.CONNECTTIMEOUT, 5)
site.setopt(pycurl.TIMEOUT, 5)
site.setopt(pycurl.NOPROGRESS, 1)
site.setopt(pycurl.FORBID_REUSE, 1)
site.setopt(pycurl.MAXREDIRS, 1)
site.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
site.setopt(pycurl.FOLLOWLOCATION, True)


sitefile = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")
site.setopt(pycurl.WRITEHEADER, sitefile)
site.setopt(pycurl.WRITEDATA, sitefile)

try:
    site.perform()
except Exception, e:
    print "Connection Error:" + str(e)
    sitefile.close()
    sys.exit()

NAMELOOKUP_TIME = site.getinfo(site.NAMELOOKUP_TIME)
CONNECT_TIME = site.getinfo(site.CONNECT_TIME)
PRETRANSFER_TIME = site.getinfo(site.PRETRANSFER_TIME)
STARTTRANSFER_TIME = site.getinfo(site.STARTTRANSFER_TIME)
REDIRECT_TIME = site.getinfo(site.REDIRECT_TIME)

TOTAL_TIME = site.getinfo(site.TOTAL_TIME)
HTTP_CODE = site.getinfo(site.HTTP_CODE)
SIZE_DOWNLOAD = site.getinfo(site.SIZE_DOWNLOAD)
HEADER_SIZE =  site.getinfo(site.HEADER_SIZE)
SPEED_DOWNLOAD = site.getinfo(site.SPEED_DOWNLOAD)


print "HTTP状态码：%s" %(HTTP_CODE)  
print "DNS解析时间：%.2f ms" %(NAMELOOKUP_TIME*1000)  
print "建立连接时间：%.2f ms" %(CONNECT_TIME*1000)  
print "准备传输时间：%.2f ms" %(PRETRANSFER_TIME*1000)  
print "传输开始时间：%.2f ms" %(STARTTRANSFER_TIME*1000)  
print "重定向消耗时间：%.2f ms" %(REDIRECT_TIME*1000)  
print "传输结束总时间：%.2f ms" %(TOTAL_TIME*1000)  
print "下载数据包大小：%d bytes/s" %(SIZE_DOWNLOAD)  
print "HTTP头部大小：%d byte" %(HEADER_SIZE)  
print "平均下载速度：%d bytes/s" %(SPEED_DOWNLOAD)  

sitefile.close()  
site.close() 


