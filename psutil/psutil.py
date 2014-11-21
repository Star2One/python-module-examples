#!/usr/bin/env python
# -*- coding: utf-8 -*-
# psutil.py
# Copyright (C)  chris.hill 2014 <sysse2009#gmail.com>
#
 
"""
    @author: chris.hill <sysse2009#gmail.com >
    @copyright: (C) 2014 chris.hill
    @license: GNU General Public License version 2.0 (GPLv2)
    @version: 0.1
"""

from datetime import datetime
import psutil
import socket
import time

def get_sys_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=0)
    time.sleep(1)
    cpu_percent = psutil.cpu_percent(interval=1)
    print "CPU核心数目:%s" %(psutil.NUM_CPUS)
    print "CPU使用率：%s" %(cpu_percent)

def get_sys_mem_info():
    mem = psutil.phymem_usage()
    print "内存总数: %s Mb" %(psutil.TOTAL_PHYMEM / 1024 / 1024)
    print "内存使用率: %.2f%%" %(mem.percent)

def get_sys_disks_info(path="/"):
    disks = psutil.disk_usage(path)
    print "根/分区总数: %s MB" %(disks.total/1024/1024)
    print "根/分区使用率: %.2f%%" %(disks.percent)


    


def main():
    get_sys_cpu_info()
    get_sys_mem_info()
    get_sys_disks_info()

if __name__ == "__main__":
    main()


