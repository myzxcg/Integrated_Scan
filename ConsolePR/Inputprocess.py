#!/usr/bin/env python
# _*_coding:utf-8 _*_
import argparse
import sys
from FuncLib import allchose

usage = '''
IntegS.py [module] [sub parameter] target [nmap parameter]
Module Type: -sub        Blasting subdomains
             -nmap       Port scanning for ip
             -dirscan    Blast scan the web directory
             -subn       Blasting subdomains and Port scan
             -all        a complete moudle,contain subdomain,namp_scan and dirscan 
'''


def CmdParse():
    parser = argparse.ArgumentParser(prog='Integrated_Scan', usage=usage, description='Designed by myz',
                                     epilog='If you feel good, you can give me a Star at https://github.com/myzxcg/Integrated_Scan')
    parser.add_argument('-sub', dest='sub', action='store_true', help='Blasting subdomains')
    parser.add_argument('-nmap', dest='nmap', action='store_true', help='Port scanning for ip')
    parser.add_argument('-dirscan', dest='dirscan', action='store_true', help=' Blast scan the web directory')
    parser.add_argument('-subn', dest='sub_nmap', action='store_true', help='Blasting subdomains and Port scan')
    parser.add_argument('-all', dest='all', action='store_true',
                        help='a complete moudle,contain subdomain,namp_scan and dirscan')

    parser.add_argument('-re', dest='dealsub', default=None, type=str,
                        help='Process the subdomain name blast result file, separate the subdomain name from the IP, and regenerate the IP into a C segment')

    # 设定进程/线程
    parser.add_argument('-t', dest='threads', default=200, type=int, help="sub Blasting module's threads,default=200")
    parser.add_argument('-p', dest='process', default=6, type=int,
                        help="sub Blasting and PortScan module's Processes,default=6")

    parser.add_argument('-r', dest='File_Ip_Domain', default=None, type=str,
                        help="Specify the target domain file or Portscan ip file")
    parser.add_argument('-u', dest='Host_Url', default=None, type=str, help='Port scan ip/Ip segment or subdomain')
    parser.add_argument('-o', dest='output', default=None, type=str, help='Output filename')

    parser.add_argument('-f', dest='file', default='subnames.txt', help="subdomain's file,default is subnames.txt")
    parser.add_argument('-i', dest='intranet', default=False, action='store_true',
                        help='Ignore domains pointed to private IPs')
    parser.add_argument('--full', dest='full_scan', default=False, action='store_true',
                        help='sub Blasting complete dictionary')
    parser.add_argument('-d', dest='dict_dir', default='Dict/dict_dir.txt', type=str,
                        help='dirscan dict file,defalut Dict/dict_dir.txt')

    args = parser.parse_args()

    return Judge_Input(parser, args)


def Judge_Input(parser, args):
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.dealsub is not None:
        print '[Start] File deal start...'
        print '[Attention] The result will be saved in Output/deal_sudomain.txt & Output/deal_iplist.txt'
        print 'Running....',
        filenames = args.dealsub.split(',')
        allchose.deal_subdomain(filenames)
        print
        print '[ALL Done]'
        sys.exit(0)

    if args.sub is True or args.sub_nmap is True or args.all is True:
        if args.Host_Url is None and args.File_Ip_Domain is None:
            print '[ERROR] You must Specify a domain name or a domain file'
            sys.exit(0)
    elif args.nmap is True:
        if args.Host_Url is None and args.File_Ip_Domain is None:
            print '[ERROR] You must Specify a Hostname or a Host file'
            sys.exit(0)

    elif args.dirscan is True:
        if args.Host_Url is None:
            print "[ERROR] You Should use '-u' to specify a target!"
            sys.exit(0)
        if args.Host_Url.startswith('http://') or args.Host_Url.startswith('https://'):
        	print "[ERROR] You must delete 'http://' or 'https://' at '-u' and try again!"
        	sys.exit(0)
    else:
        print '[ERROR] No module name.'
        sys.exit(0)
    if args.Host_Url is not None:
        args.Host_Url = args.Host_Url.strip()
    return args
