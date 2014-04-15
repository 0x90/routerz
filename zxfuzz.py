#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Dummy telnet fuzzer for ZyXELL Keenetic
#
# MacBookPro:~ 090h$ telnet 1.0.0.1
# Trying 1.0.0.1...
# Connected to 1.0.0.1.
# Escape character is '^]'.
#
# Password : """
# author: @090h

from telnetlib import *
from sys import exit
from argparse import ArgumentParser
from datetime import datetime
import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)

def errlog(msg):
    logging.critical(msg)
    exit()

def zyxell_fuzz_telnet(host, port=23, start=1, finish=0):
    msg = "Start telnet fuzzing %s:%i" % (host, port)
    logging.info(msg)
    tn = Telnet()
    buflen = start

    while buflen != finish:
        tn.open(host, port)
        #print 'connected'

        for x in xrange(0,3):
            buf = 'A'*buflen
            print "Trying length 0x%X" % len(buf)
            print tn.read_until('Password :')
            tn.write(buf+'\n')
            #print buf
            buflen += 1

def zyxell_fuzz2(host, port=23, length=0x42):
    #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    msg = "Start telnet fuzzing %s:%i" % (host, port)
    logging.info(msg)
    tn = Telnet()
    buflen = length - 1
    buf = chr(19)*buflen

    for x in xrange(20, 255):
        tn.open(host, port)
        print x
        new_buf = buf + chr(x)
        tn.write(new_buf+'\n')
        print tn.read_until('Password :')
        tn.close()

if __name__ == '__main__':
    parser = ArgumentParser(description='Dummy telnet fuzzer for ZyXELL Keenetic')
    parser.add_argument('host', required=True,  help='Telnet host to fuzz')
    parser.add_argument('-p', '--port', default=23, required=False, help='telnet port')
    parser.add_argument('-t', '--threads', action='store', type=int, default=5, help='thread count')
    parser.add_argument('-l', '--length', action='store', type=int, default=1, help='length start')
    parser.add_argument('--version', action='version', version='%(prog)s 0.01')
    args = parser.parse_args()
    start_time = datetime.now()
    logging.debug("Start time: " + start_time.strftime('%Y-%m-%d %H:%M:%S'))
    #zyxell_fuzz_telnet(args.host, args.port)
    zyxell_fuzz2(args.host)
    logging.debug("Finish time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))