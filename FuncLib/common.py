# coding:utf-8
# common functions
import sys
import os
from gevent.pool import Pool
import dns.resolver
from consle_width import getTerminalSize
console_width = getTerminalSize()[0] - 2



def is_intranet(ip):
    ret = ip.split('.')
    if len(ret) != 4:
        return True
    if ret[0] == '10':
        return True
    if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
        return True
    if ret[0] == '192' and ret[1] == '168':
        return True
    return False


def print_msg(msg=None, left_align=True, line_feed=False):
    if left_align:
        sys.stdout.write('\r' + msg + ' ' * (console_width - len(msg)))
    else: 
        sys.stdout.write('\r' + ' ' * (console_width - len(msg)) + msg)
    if line_feed:
        sys.stdout.write('\n')
    sys.stdout.flush()

def test_server(server, dns_servers):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.lifetime = resolver.timeout = 6.0
    try:
        resolver.nameservers = [server]
        answers = resolver.query('public-dns-a.baidu.com')
        if answers[0].address != '180.76.76.76':
            raise Exception('Incorrect DNS response')
        try:
            resolver.query(
                'test.bad.dns.myzxcg.com')  
            with open('bad_dns_servers.txt', 'a') as f:
                f.write(server + '\n')
            print_msg('[+] Bad DNS Server found %s' % server)
        except:
            dns_servers.append(server)
        print_msg('[+] Server %s < OK >   Found %s' % (server.ljust(16), len(dns_servers)))
    except:
        print_msg('[+] Server %s <Fail>   Found %s' % (server.ljust(16), len(dns_servers)))


def load_dns_servers():
    print_msg('[+] Validate DNS servers', line_feed=True)
    dns_servers = []
    pool = Pool(10)
    for server in open('Dict/dns_servers.txt').readlines():
        server = server.strip()
        if server:
            pool.apply_async(test_server, (server, dns_servers)) 
    pool.join()

    dns_count = len(dns_servers)
    print_msg('\n[+] %s available DNS Servers found in total' % dns_count, line_feed=True)
    if dns_count == 0:
        print_msg('[ERROR] No DNS Servers available!', line_feed=True)
        sys.exit(-1)
    return dns_servers


def load_next_sub(args):
    next_subs = []
    _file = 'Dict/next_sub_full.txt' if args.full_scan else 'Dict/next_sub.txt'
    with open(_file) as f:
        for line in f:
            sub = line.strip()
            if sub:
                next_subs.append(sub)
    return next_subs


def get_out_file_name_txt(target, args):
    output = 'Output/'
    if not os.path.exists(output):
        os.makedirs(output)
    if args.output is not None:
        outfile = output + args.output
    else:
        _name = os.path.basename(args.file).replace('subnames', '')
        if _name != '.txt':
            _name = '_' + _name
        outfile = output + target +'_sub'+ _name

    return outfile

def get_out_file_name_html(target, args):
    output = 'Output/'
    if not os.path.exists(output):
        os.makedirs(output)
    if args.output is not None:
        outfile = output + args.output
    else:
        outfile=output + target +'_sub'+'.html'
    return outfile

def user_abort(sig, frame):
    exit(-1)

