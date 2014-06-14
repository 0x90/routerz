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


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Router vulnerability stat with help of searchsploit
# Tested on Kali Linux 1.06
#awk -F "\"*,\"*" '{printf "%-75s %s\n", $3, $2}' $csvpath | awk 'tolower($0) ~ /'$1'/ && /'$2'/ && /'$3'/' | sed s/platforms//

from subprocess import Popen, PIPE
from os import mkdir, path


###### CONFIG ##########
exploitdb = '/usr/share/exploitdb/'
csvpath= path.join(exploitdb, 'files.csv')
vendors = ['d-link', 'tp-link', 'zyxel','linksys', 'huawei', 'netgear']
#vendors = ['d-link', 'tp-link', 'zyxel', 'cisco', 'linksys', 'huawei', 'netgear']


def search_sploitz(vendor):
    out = Popen('searchsploit %s' % vendor, shell=True, stdout=PIPE).communicate()[0]
    if out is None:
        return None
    return out.split('\n')[2:-1]

def sploit_code(short_path):
    return open('/usr/share/exploitdb/platforms/%s' % short_path, 'rb').read()

def vendor_stat():
    stat = {}
    for vendor in vendors:
        exploits = filter(lambda x: x.find('/hardware/webapps') != -1 or
                          x.find('/hardware/remote') != -1 or
                          x.find('/cgi/webapps/') != -1,
                          search_sploitz(vendor))
                          if exploits is not None:
                              stat[vendor] = len(exploits)
    
    
    print('ExploitDB statistics')
    for w in sorted(stat, key=stat.get, reverse=True):
        print w, stat[w]

#return stat

def make_pack():
    for vendor in vendors:
        # if not path.exists(vendor):
        #     mkdir(vendor)
        
        # print('-'*80)
        # print(vendor)
        # print('-'*80)
        
        lines = filter(lambda x: x.find('/hardware/webapps') != -1 or
                       x.find('/hardware/remote') != -1 or
                       x.find('/cgi/webapps/') != -1,
                       search_sploitz(vendor))
                       
                       csrf = filter(lambda x: x.lower().find('csrf') != -1 or
                                     x.lower().find('xsrf') != -1 or
                                     x.lower().find('exec') != -1 or
                                     x.lower().find('forgery') != -1, lines )
                                     for line in csrf:
                                         print(line)

if __name__ == '__main__':
    make_pack()
#vendor_stat()
