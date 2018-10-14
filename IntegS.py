#!/usr/bin/env python
# _*_coding:utf-8 _*_
'''
version 0.1.2 @myzxcg https://github.com/myzxcg
'''
from ConsolePR.Inputprocess import CmdParse
from ConsolePR.Picture_load import ProgressBar, picture
from FuncLib import SubBlasting, NmapScan, DirScan, allchose
import time
import os
import sys


def submodule(args):
    if args.Host_Url is not None and args.File_Ip_Domain is None:
        SubBlasting.sb_main(args, args.Host_Url)
    else:
        if os.path.getsize(args.File_Ip_Domain):
            with open(args.File_Ip_Domain, 'r') as f:
                for domain in f:
                    domain = domain.strip()
                    print '[Start] %s Subdomain blasting start....' % (domain)
                    SubBlasting.sb_main(args, domain)
        else:
            print '[ERROR] Domain file is empty!'
            sys.exit(0)


def dirscanmodule(args):
    output = 'Output/txt/'
    if not os.path.exists(output):
        os.makedirs(output)
    output = 'Output/html/'
    if not os.path.exists(output):
        os.makedirs(output)
    try:
        DirScan.dir_S(args, args.Host_Url)
    except KeyboardInterrupt:
        print '[ERROR] User aborted the scan!'


# 扫子域名和端口
def snmodule(args):
    
    args.intranet = True
    if args.output is not None:
        print '[Warning] This module does not support -o ,Will use The default directory is Output/.... '
        args.output = None
    SubBlasting.sb_main(args, args.Host_Url)

    allchose.sub_dealip(args.Host_Url, args)
    args.File_Ip_Domain = 'tmp/%s_ip.txt' % (args.Host_Url)
    NmapScan.Judge(args)
    print '[Done] The sub blasting and PortScan scan all done.'


# 扫子域名、端口、目录
def allmoudle(args):
    if args.output is not None:
        print '[Warning] This module does not support -o ,Will use The default directory is Output/.... '
        args.output = None
    allchose.run(args)


if __name__ == '__main__':
    bar = ProgressBar(total=10)
    for i in range(0,100,11):
        bar.move()
        bar.log(str(i)+'%')
        time.sleep(0.1)
    picture()
    print '[Attention] The Default output directory is Output/.... '
    print
    start = time.time()
    args = CmdParse()

    if args.sub is True:
        submodule(args)

    elif args.nmap is True:
        NmapScan.Judge(args)

    elif args.dirscan is True:
        dirscanmodule(args)

    elif args.sub_nmap is True:
        snmodule(args)

    elif args.all is True:
        allmoudle(args)
    #删除tmp目录
    # if os.path.exists('tmp/'):
    #     __import__('shutil').rmtree('tmp/')
    print '[All Done] All used %s s' % (time.time() - start)
