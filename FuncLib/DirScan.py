#!/usr/bin/env python
# _*_coding:utf-8 _*_
import gevent
from gevent import monkey

monkey.patch_all()
from gevent.queue import Queue
import requests
import os, sys
from ConsolePR import TempleteHtml_dirscan
from string import Template
from PrintHtml import Dirscan_html_print

class Dirscan:
    def __init__(self, args, url, f):
        self.args = args
        self.url = url if url.find('://') != -1 else 'http://%s' % url
        self.content404 = ''
        self.content_404()
        self.add_Dict()
        self.headers = {  
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }
        self.fileout = f

    def add_Dict(self):
        self.queue = Queue()
        with open(self.args.dict_dir) as f:
            for dict in f:
                if dict[0:1] != '#':
                    self.queue.put(dict.strip())
        if self.queue.qsize() > 0:
            print '[+] Total Dictionary:', self.queue.qsize()
        else:
            print '[Waring] Dict is empty!'
            sys.exit(0)

    def Start_scan(self, url,html_Host_str):
        html_content = 0
        try:
            html_content = requests.get(url, headers=self.headers, allow_redirects=False, timeout=30)
        except requests.exceptions.ConnectionError,requests.exceptions.Timeout:
            pass
        finally:
            if html_content != 0:
                if html_content.status_code == 200 and html_content.text != self.content404:
                    print '[%i]%s' % (html_content.status_code, html_content.url)

                    Dirscan_html_print(html_content.url,html_Host_str,html_content.status_code)

                    self.fileout.write('[%i]%s\n' % (html_content.status_code, html_content.url)) 

    def content_404(self):
        try:
            print self.url
            content404 = requests.get(self.url + '/designedbymyzxcg/haha.html')
            self.content404 = content404.text.replace('/designedbymyzxcg/haha.html', '')
        except requests.exceptions.ConnectionError as e:
            pass

    def run(self,html_Host_str):
        while not self.queue.empty():
            url = self.url + self.queue.get()
            self.Start_scan(url,html_Host_str)

    def getfile(self):
        return self.fileout

def dir_S(args, url):
    html_Host_str=['']
    html_general = Template(TempleteHtml_dirscan.html['general'])
    with open('Output/txt/%s_dirscan.txt' % (url), 'w+') as f:
        newdirscan = Dirscan(args, url, f)
        x = [gevent.spawn(newdirscan.run,html_Host_str) for i in range(200)]
        gevent.joinall(x)
    print "[Done] '%s' dirscan done" % (url)
    print 'The result is saved in Output/txt/%s_dirscan.txt' % (url)
    with open('Output/html/%s_dirscan.html' % (url), 'w+') as f:
        f.write(html_general.substitute(content1=html_Host_str[0]))
    print 'The result is saved in Output/html/%s_dirscan.html' % (url)

