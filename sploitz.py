#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Router vuln stat by searchsploit

from subprocess import Popen, PIPE
from pprint import pprint

vendors = ['d-link', 'tp-link', 'zyxel', 'cisco', 'linksys', 'huawei']

def search_sploitz(vendor):
    lines = Popen('searchsploit %s' % vendor, shell=True).communicate()[0].split('\n')[2:-1]
    # for line in lines:
    #     fpart = line.split(' /')[0]
    #     spart = line.replace(fpart, '')
    return lines


def sploit_code(short_path):
    sploit_path = '/usr/share/exploitdb/platforms/%s' % short_path
    return open(sploit_path, 'rb').read()

#def sploit_stat()

if __name__ == '__main__':
    for vendor in vendors:
        print('Vendor: %s' % vendor)
        pprint(search_sploitz(vendor))
        raw_input()