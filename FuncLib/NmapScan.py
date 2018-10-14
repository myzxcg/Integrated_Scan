#!/usr/bin/env python
# _*_coding:utf-8 _*_
import nmap
import sys
import os
import gevent
import re
from gevent import monkey
import Config
monkey.patch_all()
from gevent.queue import Queue
from FuncLib.PrintHtml import deal
from string import Template
from ConsolePR.TempleteHtml_nmap import html
import sys

class nmap_scan:
    def __init__(self, args,iplist):
        self.length = 9
        self.args = args
        self.argm = Config.nmap_arguments
        self.iplist = iplist
        self.q = Queue()
        for ip in self.iplist:
            self.q.put(ip)

    def nscan(self, hostname,html_str,*args):
        html_port_str=''
        html_port = Template(html['port'])
        judge_port=False    #用于判断这个ip是否存在80端口
        n_s = nmap.PortScanner()
        n_s.scan(hostname, arguments=self.argm)
        if n_s.all_hosts() == '':
            print '[*] This group has not alive host'
        for ip in n_s.all_hosts():
            print '[*] %s is alive' % (ip)
            print 'Port \tState \tService'
            if not n_s[ip].all_protocols():
                print
            if len(args) != 0:
                args[0].write('[*] %s is alive' % (ip) + '\n')
                if n_s[ip].all_protocols():
                    args[0].write('Port \tState \tService' + '\n')
            for proto in n_s[ip].all_protocols():
                for port in sorted(n_s[ip][proto].keys()):
                    result = str(port) + '/' + proto + '\t' + n_s[ip][proto][port]['state'] + '\t' + \
                             n_s[ip][proto][port]['name']

                    if port ==80:
                        judge_port=True
                    html_port_str+=html_port.substitute(url=hostname, port=port, service=n_s[ip][proto][port]['name']).strip()+'</br>'

                    print  result
                    if len(args) != 0:
                        args[0].write(result + '\n')
                        args[0].flush()
                print
                if len(args) != 0:
                    args[0].write('------------------------------------\n')

            html_str[0] += deal(hostname,judge_port,html_port_str)


    def run_scan(self, f,html_str):
        while not self.q.empty():
            hostname = self.q.get()
            self.nscan(hostname, html_str,f)

def run_process(args,iplist):
    html_general = Template(html['general'])
    html_str=['']

    output = 'Output/txt/'
    if not os.path.exists(output):
        os.makedirs(output)
    output = 'Output/html/'
    if not os.path.exists(output):
        os.makedirs(output)


    _str = args.File_Ip_Domain.split('.')[0].split('\\')[-1]
    if '/' in _str:
        _str = _str.split('/')[1]
    outfile = 'Output/txt/%s_ip.txt' % (_str)
    if args.output is not None:
        outfile = output + args.output
    newnmap = nmap_scan(args,iplist)
    with open(outfile, 'w+') as f:
        x = [gevent.spawn(newnmap.run_scan, f,html_str) for _ in range(args.process + 1)]
        gevent.joinall(x)

    print '[Done] Port scan done ,The result is saved in %s.' % (outfile)

    #写到html中
    outfile = 'Output/html/%s_ip.html' % (_str)
    if args.output is not None:
        outfile = output + args.output.split('.')[0]+'.html'
    with open(outfile,'w+') as f:
        f.write(html_general.substitute(content1=html_str[0]))

    print '[Done] Port scan done ,The result is saved in %s.' % (outfile)


def run_one(args):
    html_str = ['']
    html_general = Template(html['general'])
    iplist = []

    output = 'Output/txt/'
    if not os.path.exists(output):
        os.makedirs(output)
    output = 'Output/html/'
    if not os.path.exists(output):
        os.makedirs(output)

    if '/' in args.Host_Url:
        with open('Output/txt/ip_result.txt', 'w+') as f:
            reip = re.search(r'(\d+\.\d+\.\d+\.)', args.Host_Url)
            if reip is not None:
                for i in range(256):
                    iplist.append(reip.group() + str(i))
                newnmap = nmap_scan(args,iplist)
                x = [gevent.spawn(newnmap.run_scan, f,html_str) for _ in range(args.process + 1)]
                gevent.joinall(x)
            else:
                print '[ERROR] Please check your host.'
    else:
        newnmap = nmap_scan(args, args.Host_Url)
        newnmap.nscan(args.Host_Url,html_str)

    #写到html中
    with open('Output/html/ip_result.html','w+') as f:
        f.write(html_general.substitute(content1=html_str[0]))


def Process_scan(args):
    iplist = []
    print '[+] Init %s scan process.' % args.process
    with open(args.File_Ip_Domain, 'r') as f:
        for ip in f:
            ip = ip.strip()
            if '/' in ip:
                reip = re.search(r'(\d+\.\d+\.\d+\.)', ip)
                if reip is not None:
                    for i in range(256):
                        iplist.append(reip.group() + str(i))
            else:
                iplist.append(ip)
    if not iplist:
        print '[ERROR] The ip list is empty!'
        sys.exit(0)
    run_process(args,iplist)


def Judge(args):
    print '[+] The Port Scan Started.....'
    try:
        if args.File_Ip_Domain is None and args.Host_Url is not None:
            run_one(args)
            print '[Done] Port scan done ,The result is saved in Output/txt/ip_result.txt.'
            print '[Done] Port scan done ,The result is saved in Output/html/ip_result.html.'

        elif args.File_Ip_Domain is not None:
            Process_scan(args)
        else:
            print '[ERROR] You Must order an ip , -u ip | -r ip.txt'
            sys.exit(0)

    except KeyboardInterrupt:
        print '[ERROR] User aborted the Scan!'
        sys.exit(0)

