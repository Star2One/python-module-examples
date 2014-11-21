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
"""

"""
    @ref:   https://code.google.com/p/corey-projects/source/browse/trunk/python2/linux_monitoring/linux_local_stats_rrd/linux_stats_rrd.py?r=166
"""

import time
import sys
import psutil  # http://code.google.com/p/psutil/
import rrdtool
import socket
import os


# Config Settings
NET_INTERFACE = 'eth0'
INTERVAL = 60  # 1 min


def rrd_update(stats, value, interval, ds_type):
    rrd_name = '%s.rrd' % stats
    interval = str(interval)
    interval_mins = float(interval) / 60
    heartbeat = str(int(interval) * 20)
    value = value
    if not os.path.exists(rrd_name):
        rrdb = rrdtool.create(rrd_name, '--step', '%s' % interval,
            'DS:ds:%s:%s:0:U' %(ds_type, heartbeat),
            'RRA:LAST:0.5:1:600',
            'RRA:AVERAGE:0.5:5:600',
            'RRA:MAX:0.5:5:600',
            'RRA:MIN:0.5:5:600')
        if rrdb:
            print rrdtool.error()
    else:
        up = rrdtool.updatev(rrd_name, 'N:%d' % value)
    print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()), stats, value




def net_stats(interface):
    for keys in psutil.network_io_counters(pernic=True):
        if keys == interface:
            tx_bits = psutil.network_io_counters(pernic=True)[keys][0]
            rx_bits = psutil.network_io_counters(pernic=True)[keys][1]
            return (rx_bits, tx_bits)


def rrd_graph(stats, color, title):
    rrd_name = '%s.rrd' % stats
    output_filename = '%s.png' % stats
    cur_date = time.strftime('%m/%d/%Y %H\:%M\:%S', time.localtime()) 
    graph_name = output_filename
    base = int(1024)
    print base
    rrdtool.graph(graph_name, 
        'COMMENT:\\s',
        'COMMENT:%s    ' % cur_date,
        'DEF:ds=%s:ds:AVERAGE' % rrd_name,
        'AREA:ds#%s:%s  ' % (color, stats),
        'VDEF:dslast=ds,LAST',
        'VDEF:dsavg=ds,AVERAGE',
        'VDEF:dsmin=ds,MINIMUM',
        'VDEF:dsmax=ds,MAXIMUM',
        'COMMENT:\\s',
        'COMMENT:\\s',
        'COMMENT:\\s',
        'COMMENT:\\s',
        'GPRINT:dslast:last %.1lf%S    ',
        'GPRINT:dsavg:avg %.1lf%S    ',
        'GPRINT:dsmin:min %.1lf%S    ',
        'GPRINT:dsmax:max %.1lf%S    ',
        'COMMENT:\\s',
        'COMMENT:\\s',
        '--title', '%s' % title,
        '--vertical-label', '%s' % stats,
        '--base', '%i' % base,
        '--slope-mode')

def rrd_ops(stats, value, interval, ds_type, color, title):
    rrd_update(stats, value, interval, ds_type)
    rrd_graph(stats,  color, title)

def main():
    time.sleep(1)
    cpu_percent = psutil.cpu_percent()
    mem_used = psutil.used_phymem()
    rx_bits, tx_bits = net_stats(NET_INTERFACE)

    localhost_name = socket.gethostname()

    rrd_ops('net_bps_in', rx_bits, INTERVAL, 'DERIVE', '6666FF', localhost_name)
    rrd_ops('net_bps_out', tx_bits, INTERVAL, 'DERIVE', '000099', localhost_name)
    rrd_ops('cpu_percent', cpu_percent, INTERVAL, 'GAUGE', 'FF0000', localhost_name)
    rrd_ops('mem_used', mem_used, INTERVAL, 'GAUGE', '00FF00', localhost_name)


if __name__ == '__main__':
    main()
