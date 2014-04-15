#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Router vulnerability stat with help of searchsploit
# Tested on Kali Linux 1.06
# Author: @090h

from subprocess import Popen, PIPE

vendors = ['d-link', 'tp-link', 'zyxel', 'cisco', 'linksys', 'huawei', 'netgear']
stat = {}

def search_sploitz(vendor):
    out = Popen('searchsploit %s' % vendor, shell=True, stdout=PIPE).communicate()[0]
    if out is None:
        return None
    return out.split('\n')[2:-1]

def sploit_code(short_path):
    return open('/usr/share/exploitdb/platforms/%s' % short_path, 'rb').read()

# Get exploit DB stat
for vendor in vendors:
    lines = search_sploitz(vendor)
    if lines is not None:
        stat[vendor] = len(lines)


print('ExploitDB statistics')
for w in sorted(stat, key=stat.get, reverse=True):
    print w, stat[w]

