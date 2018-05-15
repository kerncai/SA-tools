#!/usr/bin/env python 
# coding: utf-8

'''多线程 Socket TCP 端口扫描器  by: kerncai'''

import sys
import socket
import argparse
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

parser = argparse.ArgumentParser(description="progrom description")
parser.add_argument('--host',default='localhost',help="<host/ip>,default localhost")
parser.add_argument('--port',default=0,help="port range,like 1:20 or 20")
parser.add_argument('--timeout', default=0.5,help="<timeout>,default 0.5")
parser.add_argument('--limit', type=int,default=1,help='set process limit,default 1')
parser.add_argument('--portstatus',default='open',help='open port status description.default open')
parser.add_argument('--version', action='version', version='%(prog)s 1.0.1 by kerncai')
args = parser.parse_args()

host = args.host
port = args.port
timeout = args.timeout
limit = args.limit
status = args.portstatus
ports = []
show = []

try:
    remote_server_ip = socket.gethostbyname(host)
except Exception,e:
    print "please run the tcpgo --help"
    sys.exit(1)

socket.setdefaulttimeout(float(timeout))

def scan_port(port):
    try:
        s = socket.socket(2,1)
        res = s.connect_ex((remote_server_ip,port))
        if status == 'open':
            if res == 0:
                info = '%s port %s open' %(remote_server_ip,port)
                show.append(info)
            else:
                info = '%s port %s close' %(remote_server_ip,port)
                show.append(info)
        else:
            if res == 0:
                info = '%s port %s open' %(remote_server_ip,port)
                show.append(info)
        s.close()
    except Exception,e:
        pass

if port:
    if ':' in port:
        port_start = port.split(':')[0]
        port_end = port.split(':')[1]
    else:
        port_start = port
        port_end = port

    for i in range(int(port_start),int(port_end)+1):
        ports.append(i)
 
    pool = ThreadPool(processes = limit)
    results = pool.map(scan_port,ports)
    pool.close()
    pool.join()
else:
    print "please run the tcpgo --help"
    sys.exit(0)

for i in show:
    print i
