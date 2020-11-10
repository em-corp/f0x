#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__NAME__ = "f0x.py"
__VERSION__ = "2.0"

import argparse
import re
import os
import time
import json
import threading
import asyncio
from proxybroker import Broker
from concurrent.futures import ThreadPoolExecutor
from git import Repo

from lib.prettyPrint import Prettify as pp
from lib.config import ConfigManager as conf
from lib.utils import DirUtil as dutil
from lib.utils import FileUtil as futil
from lib.google import GoogleSearch as gsrch
from lib.utils import Random as rand
from lib.useragents import UA


def banner():
    print(pp.green('  .o88o.   .o             o.'))
    print(pp.green('  888 `"  .8\'             `8.'))
    print(pp.green(' o888oo  .8\'  ' + pp.yellow('oooo    ooo') + '  `8.'))
    print(pp.green('  888    88    ' + pp.yellow('`88b..8P') + '     88'))
    print(pp.green('  888    88      ' + pp.yellow('Y888') + '       88'))
    print(pp.green('  888    `8.   ' + pp.yellow('.o8"\'88b') + '    .8\''))
    print(pp.green(' o888o    `8. ' + pp.yellow('o88\'   888o') + ' .8\''))
    print()


parser = argparse.ArgumentParser()

# input
parser.add_argument('-d', '--domain', help='Specify Target domain.', 
                    dest='domain')

parser.add_argument('-q', '--query', help='Specify query/dork manually, and' + 
                    ' don\'t use more dorks from dorks-db.', dest='query')

parser.add_argument('-n', '--no-stop', help='Works with `--query`, If ' + 
                    'specified dorks from dorks-db will also be used along ' + 
                    'with manually supplied dork.', dest='query_nostop',
                    action="store_true")

parser.add_argument('-Q', '--query-args', help='Specify extra query to ' + 
                    'supply with each dorks.', dest='ex_query')

# dork selection
parser.add_argument('-c', '--category', help='Comma (,) separated dorks ' + 
                    'categories to use.', dest='category')

parser.add_argument('-cA', '--any', help='Use all available categories.',
                    dest='cat_any', action="store_true")

parser.add_argument('-S', '--severity', help='Comma (,) separated severity ' + 
                    'range(from 1 to 10). eg. consider range expansion as : ' + 
                    '"-4" will become "1,2,3,4", or ' + 
                    '"2-5" will become "2,3,4,5", or ' + 
                    '"7-" will become "7,8,9,10", or ' + 
                    '"1-4,7" will become "1,2,3,4,7".', dest='severity')

parser.add_argument('-SQ', '--quality', help='Only use quality dorks ' + 
                    'i.e. with `severity >= 7`.', dest='sev_quality',
                    action="store_true")

parser.add_argument('-SA', '--all', help='Use all available severities.',
                    dest='sev_all', action="store_true")

# optimize fox
parser.add_argument('-t', '--threads', help='Max parallel threads ' + 
                    '(Default: 3).', type=int, dest='threads')

parser.add_argument('-p', '--proxy', help="Specify proxy to use.", dest='proxy')

parser.add_argument('-pF', '--proxy-file', help='Specify file to read proxies ' 
                    +'list (one per line).', dest='proxy_file')

parser.add_argument('-pO', '--open-proxies', help='Make use of open public ' + 
                    'proxies.', dest='proxy_open', action='store_true')

parser.add_argument('-pC', '--open-proxies-count', help='Try collecting ' + 
                    '`n` open proxies. (Default: 20)', dest='proxy_count', 
                    type=int)

parser.add_argument('-C', '--conn', help='Max connections per proxy ' + 
                    '(Default: 2).', dest='proxy_conn', type=int)

parser.add_argument('--no-ssl-check', help='Disable certificate check.',
                    dest='no_ssl_check', action='store_true')

parser.add_argument('--timeout', help='Set request timeout.', dest='time_out',
                    type=int)

parser.add_argument('-m', '--min-delay', help='Specify minimum delay(sec) ' + 
                    'between requests. (Default: `max-delay` - 3)s.',
                    dest='delay_min', type=int)

parser.add_argument('-M', '--max-delay', help='Specify maximum delay(sec) ' + 
                    'between requests. (Default: `min-delay` + 3)s.',
                    dest='delay_max', type=int)

parser.add_argument('-w', '--wait', help='Specify fix delay(sec) between ' + 
                    'requests (Default: 1s).', dest='delay', type=int)

parser.add_argument('-U', '--user-agent', help='Specify User Agent.', dest='ua')

parser.add_argument('--update', help='Update dorks repo and exit.',
                    dest='repo_update', action="store_true")

parser.add_argument('-v', '--verbose', help='Be verbose.', dest='verbose',
        action="store_true")

parser.add_argument('-V', '--version', help='Display version info and exit.',
                    dest='version', action="store_true")

parser.add_argument('-r', '--results', help='Dork results to fetch in one ' + 
                    'page request (Default: 30).', dest='page_size', type=int)

parser.add_argument('-R', '--requests', help='Pages to request for each ' + 
                    'dork (Default: 5).', dest='no_of_pages', type=int)

parser.add_argument('-T', '--max-results', help='Maximum results to fetch ' + 
                    'for all the dorks combined.', dest='max_results', type=int)

# output filters
parser.add_argument('-l', '--list-dorks', help='List all dorks to be used ' + 
                    'and exit. Specify `category` or `severity` to narrow ' + 
                    'down the list. ', dest='list_dorks', action="store_true")

parser.add_argument('-L', '--categories', help='List available categories ' + 
                    'and exit.', dest='list_cat', action="store_true")

parser.add_argument('-o', '--outdir', help='Specify output directory.',
                    dest='out_dir')

parser.add_argument('-oJ', '--out-json', help='Save output in JSON format.',
                    dest='out_fmt_json', action="store_true")

parser.add_argument('-oL', '--out-list', help='Save output in simple list.',
                    dest='out_fmt_list', action="store_true")

parser.add_argument('-oR', '--out-report', help='Create html report with ' + 
                    'JSON format results.', dest='out_report',
                    action="store_true")

args = parser.parse_args()

if args.version:
    print("{} v{}".format(pp.as_bold(pp.red(__NAME__)), pp.blue(__VERSION__)))
    quit()
    
banner()


class F0x:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.severities = None
        self.categories = None
        self.domain = None
        self.query = None
        self.ex_args = None
        self.process_dorksdb_flag = True
        self.useragent = None
        self.threads = 3
        self.delay_min = 1
        self.delay_max = 1
        self.connection_per_proxy = 2
        self.proxies_list = None
        self._conn_per_proxy_count = None
        self._proxy_ptr = -1
        self.request_timeout = None
        self.ssl_check = True
        self.open_proxy_count = 20
        self.page_size = gsrch.correct_page_size(30)
        self.no_of_pages = 5
        self.max_results = None
        self.outdir = None
        self.outmode = None
        self.results_count = 0
        
        self._proxy_lock = threading.Lock()
        self._count_lock = threading.Lock()
        
        self._load_conf()

    def _load_conf(self):
        conf.load('./f0x.config')
        if self.is_verbose():
            pp.p_debug("Loaded Config file, keys: {}"
                       .format(self.get_conf().getKeys()))
    
    def get_conf(self):
        return conf.getConfig()

    def is_verbose(self):
        return self.verbose
    
    def set_categories(self, categories=None):
        self.categories = categories
  
    def get_categories(self):
        return self.categories
    
    def set_severities(self, severities=None):
        self.severities = severities
        
    def get_severities(self):
        return self.severities
    
    def set_domain(self, domain):
        self.domain = domain
    
    def get_domain(self):
        return self.domain
    
    def set_query(self, query):
        self.query = query
    
    def get_query(self):
        return self.query
        
    def set_ex_args(self, ex_args):
        self.ex_args = ex_args
    
    def get_ex_args(self):
        return self.ex_args
        
    def set_useragent(self, useragent):
        self.useragent = useragent
        
    def get_useragent(self):
        return self.useragent
    
    def set_process_dorksdb_flag(self, flag):
        self.process_dorksdb_flag = flag
        
    def get_process_dorksdb_flag(self):
        return self.process_dorksdb_flag
    
    def set_threads(self, threads):
        self.threads = threads
        
    def get_threads(self):
        return self.threads
    
    def set_delay_min(self, delay_min):
        self.delay_min = delay_min
        
    def get_delay_min(self):
        return self.delay_min
    
    def set_delay_max(self, delay_max):
        self.delay_max = delay_max
        
    def get_delay_max(self):
        return self.delay_max
    
    def set_connection_per_proxy(self, conn):
        self.connection_per_proxy = conn
    
    def get_connection_per_proxy(self):
        return self.connection_per_proxy
    
    def add_proxy(self, proxy):
        if not self.proxies_list:
            self.proxies_list = []
            self._conn_per_proxy_count = []
            
        self.proxies_list += [proxy]
        self._conn_per_proxy_count += [0]
    
    def get_proxy_list(self):
        return self.proxies_list
    
    def set_page_size(self, page_size):
        self.page_size = page_size
        
    def get_page_size(self):
        return self.page_size
    
    def set_no_of_pages(self, no_of_pages):
        self.no_of_pages = no_of_pages
        
    def get_no_of_pages(self):
        return self.no_of_pages
    
    def set_max_results(self, max_results):
        self.max_results = max_results
        
    def get_max_results(self):
        return self.max_results
    
    def set_outdir(self, outdir):
        self.outdir = outdir
    
    def get_outdir(self):
        return self.outdir
    
    def set_outmode(self, omode):
        self.outmode = omode
    
    def get_outmode(self):
        return self.outmode
    
    def set_results_count(self, count):
        self.results_count = count
    
    def get_results_count(self):
        return self.results_count
    
    def set_request_timeout(self, timeout):
        self.request_timeout = timeout
    
    def get_request_timeout(self):
        return self.request_timeout
    
    def set_ssl_check(self, ssl_check):
        self.ssl_check = ssl_check
        
    def do_ssl_check(self):
        return self.ssl_check

    def set_open_proxy_count(self, count):
        self.open_proxy_count = count
    
    def get_open_proxy_count(self):
        return self.open_proxy_count
        
    async def _record_proxy(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            proxy_url = '%s://%s:%d' % (proto, proxy.host, proxy.port)
            self.add_proxy(proxy_url)
            
            if fox.is_verbose():
                pp.p_log("Found proxy: {}".format(pp.light_green(proxy_url)))
    
    def collect_open_proxies(self):
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(broker.find(types=['HTTP', 'HTTPS'], 
                                           limit=self.get_open_proxy_count()), 
                                           self._record_proxy(proxies))
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)
    
    def update_dorks_repo(self):
        pp.p_log("Building Dork Repo.")
        repo_url = self.get_conf().get('repo_url')
        pp.p_log("Fetching from '{}'".format(repo_url))

        tmpdir = dutil.create_temp_dir('f0x', 'repo_')
        Repo.clone_from(repo_url, tmpdir)
        pp.p_log("Done Fetching.")

        rmdirs = ['.git']
        rmfiles = ['README.md', 'LICENSE']

        for i in rmdirs:
            try:
                g = dutil.get_dir(tmpdir, i)
            except:
                pass
            else:
                dutil.rmdir(g)
                
        for i in rmfiles:
            try:
                f = futil.get_file(tmpdir, i)
            except:
                pass
            else:
                os.remove(f)
        try:
            dutil.merge_dirs(tmpdir, self.get_dork_path())
        except Exception as e:
            pp.p_error(e)
            quit()

        pp.p_log("Dork Repo updated.")
    
    def get_dork_path(self):
        dp = ''
        flag = False

        try:
            dp = self.get_conf().get('dork_path')
        except:
            pp.p_error("Dorks path not exists.")
            flag = True
        else:
            if dp == '':
                pp.p_error("Dorks path not defined.")
                flag = True
        
        if flag:
            raise Exception("Error in Config file.")

        if dp.startswith('~'):
            dp = os.path.expanduser(dp)
        elif dp.startswith('/'):
            pass
        elif dp.startswith('./'):
            cwd = os.path.realpath('.')
            dp = dutil.join_names(cwd, dp[2:])
        else:
            cwd = os.path.realpath('.')
            dp = dutil.join_names(cwd, dp)

        return dp
        
    def list_repo_categories(self):
        dp = None
        try:
            dp = self.get_dork_path()
        except Exception as e:
            pp.p_error(e)
            quit()

        dl = dutil.get_dir_list(dp, True)
        if len(dl) == 0:
            pp.p_log("No Dorks available, Update dork repo.")
            return

        for i in dl:
            dc = re.sub('^{}[/]?'.format(dp), '', i)
            dc = re.sub('/', '.', dc)
            td = len(dutil.get_files_list(i, True))
            pp.p_log("Category: {}".format(dc))
            pp.p_log("Total Dorks: {}\n".format(td), '**')
    
    def list_dorks(self):
        cat = None
        sev = None
        
        if self.get_categories():
            cat = self.get_categories()
        else:
            cat = [""]
            
        if self.get_severities():
            sev = self.get_severities()
        else:
            sev = range(1, 11)
        
        for c in cat:
            for d in self.get_dorks(c, sev):
                pp.p_log(d)
    
    def get_dorks(self, category, sev_list):
        dorks = []
        dpath = None
        chome = ''
        
        if not sev_list or len(sev_list) == 0:
            return dorks
        
        try:
            dpath = self.get_dork_path()
        except Exception as e:
            pp.p_error(e)
            return []
        
        if category:
            chome = re.sub('\.', '/', category)

        dpath = dutil.get_dir(dpath, chome)

        for i in dutil.get_files_list(dpath, True):
            with open (i, 'r') as dfile:
                d = None
                j = None
                for l in dfile:
                    if l.lstrip().lower().startswith('googledork:'):
                        d = re.sub('^googledork:', '', l.lstrip().lower())
                        d = d.strip()
                    elif l.lstrip().lower().startswith('severity:'):
                        j = re.sub('^severity:', '', l.lstrip().lower())
                        j = j.strip()
                    elif (not d) and l.lstrip().lower().startswith('dork:'):
                        d = re.sub('^dork:', '', l.lstrip().lower())
                        d = d.strip()
                    
                if j and int(j) in sev_list and d:
                    dorks.append(d)

        return dorks
    
    def fetch_page_response(self, dork, pagenum, proxy):
        gurl = gsrch.prepare_URL(dork, self.get_domain(), self.get_query(),
                                 pagenum, self.get_page_size())
        
        ua = None
        if self.get_useragent():
            ua = self.get_useragent()
        else:
            ua = UA.get_random_ua()
        
        return gsrch.fetch(gurl, ua, proxy, self.get_request_timeout(), 
                           self.do_ssl_check())
        
    def save_links(self, links_list):  # FIXME: output
        for l in links_list:
            pp.p_log(l)
    
    def update_results_stats(self, c):
        with self._count_lock:
            self.set_results_count(self.get_results_count() + c)
    
    def can_fetch_more(self):
        if self.get_max_results():
            return self.get_results_count() < self.get_max_results()

        return True
    
    def get_proxy_object(self):
        proxy = {'proxy': None, 'loc': None}
        p = None
        l = None
        
        if self.get_proxy_list():
            pl = len(self.get_proxy_list())
            c = 0
            
            with self._proxy_lock:
                while True:
                    c += 1
                    self._proxy_ptr += 1
                    if self._proxy_ptr == pl:
                        self._proxy_ptr = 0
                    
                    if self._conn_per_proxy_count[self._proxy_ptr] < \
                    self.get_connection_per_proxy():
                        p = self.get_proxy_list()[self._proxy_ptr]
                        self._conn_per_proxy_count[self._proxy_ptr] += 1
                        l = self._proxy_ptr
                        break
                    
                    if c >= pl:
                        c = 0
                        time.sleep((self.get_delay_min() * 
                                    self.get_no_of_pages()) / 4)

        if p:
            proxy = {'proxy': {'http': p, 'https': p}, 'loc': l}
        return proxy
    
    def release_proxy(self, proxyobj):
        l = proxyobj['loc']
        try:
            if (l or int(l) == 0) and self._conn_per_proxy_count[l] != 0:
                self._conn_per_proxy_count[l] -= 1
        except:
            pass
    
    def process_dork(self, dork):
        if self.is_verbose():
            pp.p_debug("Processing dork: {}".format(dork))
        
        proxy = self.get_proxy_object()

        for p in range(1, self.get_no_of_pages() + 1):
            if not self.can_fetch_more():
                break
            
            time.sleep(rand.rand_between(self.get_delay_min(),
                                         self.get_delay_max()))
            response = None
            try:
                response = self.fetch_page_response(dork, p, proxy['proxy'])
            except Exception as e:
                self.release_proxy(proxy)
                gsrch.session_cleanup()
                pp.p_error(e)
                return

            if self.is_verbose():
                pp.p_debug("Fetched page : {}".format(p))
                
            links = gsrch.extract_urls(response)
            if self.is_verbose():
                pp.p_debug("Found {} url(s).".format(len(links)))
            
            self.save_links(links)
            
            self.update_results_stats(len(links))
            
            if not gsrch.has_next(response):
                break
            
        self.release_proxy(proxy)
        gsrch.session_cleanup()
    
    def execute(self):
        dorks = []
        if self.get_query():
            dorks += [self.get_query()]
        
        if self.get_process_dorksdb_flag():
            cat = []
            if self.get_categories():
                cat = self.get_categories()
            
            for c in cat:
                dorks += self.get_dorks(c, self.get_severities())
        
        if self.is_verbose():
            pp.p_debug("{} dorks to fetch.".format(len(dorks)))
        
        with ThreadPoolExecutor(max_workers=self.get_threads()) as exec:
            exec.map(self.process_dork, dorks)

                
fox = F0x(verbose=args.verbose)

if args.repo_update:
    fox.update_dorks_repo()
    quit()

if args.list_cat:
    fox.list_repo_categories()
    quit()

flag_dork_selector = False
    
if args.severity:
    flag_dork_selector = True
    s = []
    l = "1"
    m = "10"
    
    if re.search("[^0-9,-]", args.severity):
        pp.p_error("Severity value can only contains numbers or numeral " + 
                   "range, separated by comma (,).")
        quit()
    
    for i in args.severity.split(','):
        j = i
        if i.startswith('-'):
            j = l + i
        elif i.endswith('-'):
            j = i + m
            
        k = j.split('-')      
        for x in range(int(k[0]), int(k[-1]) + 1):
            s += [x]
            
    s = list(set(s))
    fox.set_severities(s)
    
if args.sev_all:
    flag_dork_selector = True
    
    s = []
    for x in range(1, 11):
        s += [x]
        
    fox.set_severities(s)

if args.severity and args.sev_all and fox.is_verbose():
    pp.p_debug("Provided severity range is overridden by `all` switch.") 

if args.sev_quality:
    flag_dork_selector = True
    
    s = []
    for x in range(7, 11):
        s += [x]
    fox.set_severities(s)

if (args.severity or args.sev_all) and args.sev_quality and fox.is_verbose():
    pp.p_debug("Provided severity (range | `all` switch) is overridden by " + 
               "`quality` switch.") 
    
if args.category:
    flag_dork_selector = True
    fox.set_categories(args.category.split(','))

if args.cat_any:
    flag_dork_selector = True
    fox.set_categories(["."])

if args.category and args.cat_any and fox.is_verbose():
    pp.p_debug("Provided categories value is overridden by `any` switch.")

if args.list_dorks:
    fox.list_dorks()
    quit()
    
if args.query:
    flag_dork_selector = True
    fox.set_query(args.query.strip())
    fox.set_process_dorksdb_flag(args.query_nostop)

if not flag_dork_selector:
    pp.p_error('Please provide atleast one dork selector from ' + 
               '`category`, `severity` or `query`.')
    quit()

if args.domain:
    domain = args.domain.strip()
    domain = re.sub(r'^http(s)?://(www\.)?', '', domain)
    domain = re.sub('/.*(/)?', '', domain)

    fox.set_domain(domain)

if args.ex_query:
    fox.set_ex_args(args.ex_query.strip())

if args.ua:
    fox.set_useragent(args.ua.strip())

if args.threads:
    if args.threads > 0:
        fox.set_threads(args.threads)
    else:
        pp.p_error("Please provide some +ve value for threads.")
        quit()

if args.delay:
    if args.delay > 0:
        fox.set_delay_min(args.delay)
        fox.set_delay_max(args.delay)
    else:
        pp.p_error("Please provide some +ve value for delay.")
        quit()

if args.delay_min:
    if args.delay_min > 0:
        fox.set_delay_min(args.delay_min)
        fox.set_delay_max(args.delay_min + 3)
    else:
        pp.p_error("Please provide some +ve value for delay_min.")
        quit()

if args.delay_max:
    if args.delay_max > 0:
        fox.set_delay_max(args.delay_max)
        if args.delay_max - 3 > 0:
            fox.set_delay_min(args.delay_max - 3)
        else:
            fox.set_delay_min(0)
    else:
        pp.p_error("Please provide some +ve value for delay_max.")
        quit()
        
if args.delay_min and args.delay_max:
    fox.set_delay_min(args.delay_min)
    fox.set_delay_max(args.delay_max)

if args.page_size:
    if args.page_size <= 0:
        pp.p_error("Please provide some +ve value for `dork results`.")
        quit()
    fox.set_page_size(gsrch.correct_page_size(args.page_size))

if args.no_of_pages:
    if args.no_of_pages <= 0:
        pp.p_error("Please provide some +ve value for `pages to request`.")
        quit()
    fox.set_no_of_pages(int(args.no_of_pages))

if args.max_results:
    if args.max_results <= 0:
        pp.p_error("Please provide some +ve value for `max results`.")
        quit()
    fox.set_max_results(args.max_results)

# TODO: FIXME:
# output dir and report logic/code left

if args.no_ssl_check:
    fox.set_ssl_check(False)

if args.time_out:
    if args.time_out <= 0:
        pp.p_error("Please provide some +ve value for `request timeout`.")
        quit()
    fox.set_request_timeout(args.time_out)

if args.proxy_conn:
    if args.proxy_conn > 0:
        fox.set_connection_per_proxy(args.proxy_conn)
    else:
        pp.p_error("Please provide some +ve value for connection per proxy.")

if args.proxy_open and (args.proxy or args.proxy_file):
    pp.p_error("Please use only one option from `open proxies` or " + 
               "(proxy and proxy_file).")
    quit()
    
if args.proxy and args.proxy_file:
    pp.p_error("Please use only one option from proxy or proxy_file.")
    quit()

if args.proxy:
    fox.add_proxy(args.proxy.strip())

if args.proxy_file:
    for i in futil.get_file_aslist(args.proxy_file):
        fox.add_proxy(i)

if args.proxy_count:
    if args.proxy_count <= 0:
        pp.p_error("Please provide some +ve value for `open proxy count`.")
        quit()

    fox.set_open_proxy_count(args.proxy_count)
    
    if fox.is_verbose() and not args.proxy_open:
        pp.p_info('Ignoring `open proxy count` as provided without ' + 
                  'enabling `open proxies` switch.')
        
if args.proxy_open:
    fox.collect_open_proxies()

fox.execute()
        