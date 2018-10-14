#!/usr/bin/env python
# _*_coding:utf-8 _*_
import re
import sys
import os
from FuncLib import SubBlasting, NmapScan, DirScan
from common import get_out_file_name_txt
import multiprocessing
import time


def sub_dealip(target, args):
    iplist = []
    repeate = []
    file = get_out_file_name_txt(target, args)
    with open(file, 'r') as f1:
        with open('tmp/%s_domain.txt' % (target), 'w+') as f2:
            for string in f1:
                m1 = re.search(r'(.*\.com)|(.*\.cn)|(.*\.top)|(.*\.net)|(.*\.edu)|(.*\.org)', string)  # 可自行按格式添加后缀
                if m1 is not None:
                    s = m1.group()
                    f2.write(s + '\n')

                m2 = re.search(r'(\d+\.\d+\.\d+\.\d+)(,\s\d+\.\d+\.\d+\.\d+)*', string)
                if m2 is not None:
                    for ip in m2.group().split(', '):
                        iplist.append(ip)
        with open('tmp/%s_ip.txt' % (target), 'w+') as f3:
            for string in iplist:
                m = re.search(r'(\d+\.\d+\.\d+\.)', string)
                if m is not None:
                    if re.match(r'(192\.168\.\d+\.)|(172\.([1][6-9]|[2][0-9]|[3][0-1])\.\d+\.)|(10\.\d+\.\d+\.)',
                                m.group()):
                        continue
                    else:
                        newip = m.group() + '1/24'
                        if newip not in repeate:
                            f3.write(newip + '\n')
                            repeate.append(newip)


def deal_subdomain(filenames):
    output = 'Output/'
    if not os.path.exists(output):
        os.makedirs(output)

    with open('Output/deal_sudomain.txt', 'w+') as f1:
        with open('Output/deal_iplist.txt', 'w+') as f2:
            print filenames
            for filename in filenames:
                # 一个爆破文件
                iplist = []
                repeate = []
                with open(filename, 'r') as f3:
                    for string in f3:
                        # 文件内一行
                        string=string.strip()
                        m1 = re.search(r'(.*\.com)|(.*\.cn)|(.*\.top)|(.*\.net)|(.*\.edu)|(.*\.org)',string)  # 可自行按格式添加后缀
                        if m1 is not None:
                            s = m1.group()
                            f1.write(s + '\n')

                        m2 = re.search(r'(\d+\.\d+\.\d+\.\d+)(,\s\d+\.\d+\.\d+\.\d+)*', string)
                        if m2 is not None:
                            for ip in m2.group().split(', '):
                                iplist.append(ip)
                        for string in iplist:
                            m = re.search(r'(\d+\.\d+\.\d+\.)', string)
                            if m is not None:
                                if re.match(
                                        r'(192\.168\.\d+\.)|(172\.([1][6-9]|[2][0-9]|[3][0-1])\.\d+\.)|(10\.\d+\.\d+\.)',
                                        m.group()):
                                    continue
                                else:
                                    newip = m.group() + '1/24'
                                    if newip not in repeate:
                                        f2.write(newip + '\n')
                                        repeate.append(newip)


def Process_dir(args, domain):
    multiprocessing.freeze_support()
    all_process = []
    q = multiprocessing.Queue()
    for url in domain:
        q.put(url)
    time.sleep(0)
    try:
        for process_num in range(args.process - 2):
            p = multiprocessing.Process(target=Process_run, args=(q, args))
            all_process.append(p)
            p.start()
        while all_process:
            for p in all_process:
                if not p.is_alive():
                    all_process.remove(p)
                    p.terminate()
                    # print '[ERROR] Has some progress error,You can restart it to solve it!'
    except KeyboardInterrupt as e:
        for p in all_process:
            p.terminate()
        print '[ERROR] User aborted the Scan!'
        sys.exit(0)
    except Exception as e:
        print e


def Process_run(queue, args):
    while queue.qsize():
        url = queue.get()
        DirScan.dir_S(args, url)
        time.sleep(0)


def run(args):
    args.intranet = True
    SubBlasting.sb_main(args, args.Host_Url)

    sub_dealip(args.Host_Url, args)
    args.File_Ip_Domain = 'tmp/%s_ip.txt' % (args.Host_Url)
    NmapScan.Judge(args)

    print '[+] DirScan started...'
    domain = []
    with open('tmp/%s_domain.txt' % (args.Host_Url)) as f:
        for d_s in f:
            d_s = d_s.strip()
            domain.append(d_s)
    if not domain:
        print '[ERROR] The SubDomain is empty!'
        sys.exit(0)
    Process_dir(args, domain)
    print '[Done] The sub blasting,PortScan scan and DirScan all done.'
