#!/usr/bin/env python
# _*_coding:utf-8 _*_
from ConsolePR import TempleteHtml_nmap
from ConsolePR import TempleteHtml_sub
from ConsolePR import TempleteHtml_dirscan
from string import Template
import requests
requests.adapters.DEFAULT_RETRIES = 3
#nmap
def deal(url,judge_port,html_port_str):
    status = 404
    if judge_port is True:
        url1='http://'+url
        status=requests.get(url1).status_code
    html_host = Template(TempleteHtml_nmap.html['host'])
    html_host_str=html_host.substitute(status=status,url=url,content2=html_port_str)
    return html_host_str

#sub
def Sub_html_print(url,ips):
	html_host_str=''
	status='Click'
	html_ip_str=''
	headers = {  
	'Accept': '*/*',
	'Referer': 'http://www.baidu.com',
	'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
	'Cache-Control': 'no-cache',
	}
	html_ip = Template(TempleteHtml_sub.html['ip'])
	html_host = Template(TempleteHtml_sub.html['host'])
	for ip in ips.split(', '):
	    html_ip_str+=html_ip.substitute(ip=ip.strip())
	url=url.strip()
	try:
	    url1='http://'+url
	    status=requests.head(url1,headers=headers).status_code
	except requests.exceptions.ConnectionError,requests.exceptions.Timeout:
	    pass
	finally:
	    html_host_str+=html_host.substitute(status=status,url=url,content2=html_ip_str)
	    return html_host_str

#dirscan
def Dirscan_html_print(url,html_Host_str,status):
    html_Host = Template(TempleteHtml_dirscan.html['host'])
    html_Host_str[0]+=html_Host.substitute(url=url,status=status)









