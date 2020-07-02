#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__NAME__    = "f0x.py"
__VERSION__ = "1.0"

import argparse
import re
import os
import time
from git import Repo
from lib.prettyPrint import Prettify as pp
from lib.config import ConfigManager as conf
from lib.utils import DirUtil as dutil
from lib.utils import FileUtil as futil
from lib.google import GoogleSearch as gs
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

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--site', help='Specify Target site', dest='site')

parser.add_argument('-q', '--query', help='Dork to use. If specified, \
        other files will not be read.', dest='query')
parser.add_argument('-i', '--inclusive', help='This works with `query` option \
        only, if used, will also read dorks from file. ', dest='inc', 
        action="store_true")
parser.add_argument('-A', '--args', help='Specify extra query to supply with \
        each dorks.', dest='ex_query')

parser.add_argument('-C', '--category', help='Use dorks from this category \
        only.', dest='category')
parser.add_argument('-S', '--severity', help='Specify minimum severity\
        (inclusive) dork file to read, range is [0, 10], defalut: 5.', 
        dest='severity', type=int, choices=range(1, 11))
parser.add_argument( '--only', help='Use along with severity, to \
        select only a particular value.', dest='s_only', action='store_true')
parser.add_argument( '--upper', help='Use along with severity, to mark \
        provided value as upper limit (exclusive).', dest='s_upper', 
        action='store_true')
parser.add_argument('-a', '--all', help='Use all the dork files to fetch \
        result (overrides --only, --upper flags).', dest='s_all', 
        action='store_true')
parser.add_argument('-Q', '--quality', help='Use only top severity(>=8) dork \
        files (overrides --only, --upper flags). ', dest='s_qual', 
        action='store_true')

parser.add_argument('-r', '--results', help='Total results to fetch in one \
        request, default is 30.', dest='page_size', type=int)
parser.add_argument('-t', '--total', help='Total results to fetch for each \
        dork, default is 150.', dest='dork_size', type=int)
parser.add_argument('-T', '--max', help='Maximum results to fetch for all the \
        dorks combined.', dest='max_results', type=int)

#parser.add_argument('-P', '--proxy', help='proxy', dest='')
#parser.add_argument('-f', '--proxy-file', help='list of proxies', dest='')
#parser.add_argument('-c', '--conn', help='connections per proxy', dest='')

parser.add_argument('-m', '--mintime', help='Specify minimum sec to wait \
        between requests, If not specified, default 5 sec range is assumed', 
        dest='min', type=int)
parser.add_argument('-M', '--maxtime', help='Specify maximum sec to wait \
        between requests, if not specified, default 5 sec range is assumed.', 
        dest='max', type=int)
parser.add_argument('-d', '--delay', help='Specify fix delay(in sec), if \
        specified, took priority over variable delay.', dest='delay', type=int)
parser.add_argument('-p', '--parallel', help='Specify total no of parallel \
        requests, default is 5.', dest='parallel', type=int)
parser.add_argument('-U', '--user-agent', help='Specify User Agent ', 
        dest='UA')

parser.add_argument('-o', '--output', help='Specify output directory', 
        dest='output')
parser.add_argument('-j', '--json', help='Save output in JSON format only', 
        dest='json', action="store_true")
parser.add_argument('-R', '--report', help='Create Report along with JSON \
        format ouput, default', dest='report', action="store_true")

parser.add_argument('--update', help='Update Dorks Repo, and exit', 
        dest='updaterepo', action="store_true")
parser.add_argument('-L', '--list', help='List Repo categories, total \
        dorks and exit', dest='listrepo', action="store_true")
parser.add_argument('-v', '--verbose', help='Be verbose.', dest='verbose', 
        action="store_true")

args = parser.parse_args()

banner()
print("\t{} v{}".format(pp.as_bold(pp.red(__NAME__)), pp.blue(__VERSION__)))

if not (args.site or \
        args.query or \
        args.category or \
        args.severity or \
        args.s_all or \
        args.s_qual  or \
        args.page_size or \
        args.dork_size or \
        args.max_results or \
        args.min or \
        args.max or \
        args.delay or \
        args.parallel or \
        args.UA or \
        args.output or \
        args.updaterepo or \
        args.listrepo):
            pp.p_error('No options are specified.')
            print (parser.format_help())
            quit()

#------------------------------------------------------------------------------

class Fox:
    def __init__(self):
        self.verbose = None
        self.site = None
        self.ex_q = None
        self.raw_q = None
        self.inc = None
        self.cat = None
        self.sev = None
        self.sev_flag = None
        self.psize = None
        self.dsize = None
        self.max_res = None
        self.del_range = [None, None]
        self.par = None
        self.UA = None
        self.out_dir = None
        self.breport = None
        self.mr_achived = 0

    def set_site(self, site):
        self.site = site

    def get_site(self):
        return self.site

    def set_ex_query(self, q):
       self.ex_q = q

    def get_ex_query(self):
        return self.ex_q

    def set_raw_query(self, q):
        self.raw_q = q

    def get_raw_query(self):
        return self.raw_q

    def set_inc_q(self):
        self.inc = True
    
    def unset_inc_q(self):
        self.inc = False

    def get_inc_q(self):
        return self.inc

    def set_category(self, c):
        self.cat = c

    def get_category(self):
        return self.cat

    def set_severity(self, s):
        self.sev = s

    def get_severity(self):
        return self.sev

    def set_severity_flag(self, sf):
        self.sev_flag = sf

    def get_severity_flag(self):
        return self.sev_flag

    def set_page_size(self, ps):
        self.psize = ps

    def get_page_size(self):
        return self.psize

    def set_dork_size(self, ds):
        self.dsize = ds

    def get_dork_size(self):
        return self.dsize
    
    def set_max_results(self, mr):
        self.max_res = mr

    def get_max_results(self):
        return self.max_res

    def set_delay_range(self, s, e):
        self.del_range = [s, e]

    def get_delay_range(self):
        return self.del_range

    def get_delay_start(self):
        return self.get_delay_range()[0]

    def get_delay_end(self):
        return self.get_delay_range()[1]

    def set_max_parallel(self, p):
        self.par = p

    def get_max_parallel(self):
        return self.par

    def set_ua(self, ua):
        self.UA = ua

    def get_ua(self):
        return self.UA

    def has_ua(self):
        if self.UA and not (self.UA == ''):
            return True
        return False

    def set_out_dir(self, d):
        self.out_dir = d

    def get_out_dir(self):
        return self.out_dir

    def set_build_report(self):
        self.breport = True

    def unset_build_report(self):
        self.breport = False

    def get_build_report(self):
        return self.breport

    def set_verbose(self):
        self.verbose = True

    def is_verbose(self):
        return self.verbose

    def _load_conf(self):
        conf.load('f0x2.config')
    
    def get_conf(self):
        if conf.getConfig is None:
            self._load_conf()
        return conf.getConfig()

    def get_dork_path(self):
        dp = ''
        try:
            dp = self.get_conf().get('dork_path')
        except:
            pp.p_error("Dorks path not exists, Check config file.")
            return
        else:
            if dp == '':
                pp.p_error("Dorks path not defined, Check config file.")
                return

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

    def list_dorks_stats(self):
        dp = self.get_dork_path()
        if dp is None or dp == '':
            pp.p_error("Dorks path not defined, Check config file.")
            return

        dl = dutil.get_dir_list(dp, True)
        if len(dl) == 0:
            pp.p_log("No Dorks available, Update dork repo.")

        for i in dl: 
            dc = re.sub('^{}[/]?'.format(dp), '', i)
            dc = re.sub('/', '.', dc)
            td = len (dutil.get_files_list(i, True))
            pp.p_log("Category: {}".format(dc))
            pp.p_log("Total Dorks: {}\n".format(td), '**')

    def update_dorks_repo(self):
        pp.p_log("Building Dork Repo.")
        repo_url = self.get_conf().get('repo_url')
        pp.p_log("Fetching from '{}'".format(repo_url))
    
        tmpdir = dutil.create_temp_dir('f0x', 'repo_')
        Repo.clone_from(repo_url, tmpdir)
        pp.p_log("Done Fetching.")

        try:
            g = dutil.get_dir(tmpdir, '.git')
        except:
            pass
        else:
            dutil.rmdir(g)

        try:
            f = futil.get_file(tmpdir, 'README.md')
        except:
            pass
        else:
            os.remove(f)
        
        try:
            f = futil.get_file(tmpdir, 'LICENSE')
        except:
            pass
        else:
            os.remove(f)

        dutil.merge_dirs(tmpdir, self.get_dork_path)
        pp.p_log("Dork Repo updated.")

    def get_severity_list(self):
        sev = []
        s = self.get_severity()
        s_f = self.get_severity_flag()

        if s_f == 0:
            sev = list(range(s, 11))
        elif s_f  == 1:
            sev = [s]
        elif s_f  == 2:
            sev = list(range(1, s)) #if severity = 1, return empty set

        return sev

    def get_dorks(self, svr):
        dorks = []
        if self.get_raw_query():
            if svr == 10:
                dorks += [self.get_raw_query()]
            if not self.get_inc_q():
                return dorks
    
        dpath = self.get_dork_path()
        chome = ''

        if self.get_category() and self.get_category() != '':
            chome = re.sub('\.', '/', self.get_category())
   
        dpath = dutil.get_dir(dpath, chome)

        for i in dutil.get_files_list(dpath, True):
            with open (i, 'r') as dfile:
                d = ''
                j = ''
                for l in dfile:
                    if l.lstrip().lower().startswith('dork:'):
                        d = re.sub('^[dD][oO][rR][kK]:', '', l.lstrip())
                        d = d.strip()
                    elif l.lstrip().lower().startswith('severity:'):
                        j = re.sub('^severity:', '', l.lstrip().lower())
                        j = j.strip()
            
                if int(j) == svr:
                    dorks.append(d)

        return dorks
   
    def _get_count(self):
        self.mr_achived

    def _set_count(self, c):
        self.mr_achived = c

    def _update_results_count(self, c):
        self._set_count(self._get_count() + c)

    def _can_fetch_more(self):
        return (self.get_max_results() - self._get_count()) > 0

    def persist(self, r, d, s, o, fc):
        if fc == 1:
            fd = open(futil.join_names(o, 'dork.info'), 'w')
            fd.write("dork: {}\n".format(d))
            fd.write("severity: {}\n".format(s))
            fd.close()
        fd = open(futil.join_names(o, 'dork_page_' + str(fc)), 'w')
        fd.write(r)
        fd.close()

    def process_dork(self, d, s):
        if not self._can_fetch_more():
            return

        i = 0
        rFlag = True
        dd = dutil.create_random_dir(dutil.create_dir(self.get_out_dir(), \
                'dorks'), 'dork_')
        pp.p_log("Processing dork: {}".format(d))

        while rFlag and self._can_fetch_more() and \
                ((self.get_page_size() * i) <= self.get_dork_size()):
                    i += 1
                    url = gsrch.prepare_URL(d, self.get_site(), \
                            self.get_ex_query(), i, self.get_page_size())
                    t = rand.rand_between(self.get_delay_start(), \
                            self.get_delay_end())

                    pp.p_log("Sleeping for {} sec.".format(t))
                    time.sleep(t)
                    pp.p_log("Processing now.")
                    pp.p_log("#Page to fetch: {}".format(i))

                    if self.has_ua():
                        ua = self.get_ua()
                    else:
                        ua = UA.get_random_ua()
                    if self.is_verbose():
                        pp.p_debug("Using UA ==> {}".format(ua))

                    response = gsrch.fetch(url, ua)
                    pp.p_log("Got Response.")
        
                    self.persist(response, d, s, dd, i)
                    self._update_results_count(self.get_page_size())
                    rFlag = gsrch.has_next(response)
                    futil.dump_list(futil.join_names(dd, 'urls.txt'), \
                            gsrch.extract_urls(response))

    def dbBuilder(self):
        for s in self.get_severity_list():
            for d in self.get_dorks(s):
                self.process_dork(d, s)

#------------------------------------------------------------------------------
fox = Fox()

if args.verbose:
    fox.set_verbose()

if args.listrepo:
    fox.list_dorks_stats()
    quit()

if args.updaterepo:
    fox.update_dorks_repo()
    quit()

if args.site:
    site = ''
    site = args.site.strip()
    site = re.sub(r'^http(s)?://(www\.)?', '', site)
    site = re.sub('/.*(/)?', '', site)

    fox.set_site(site)

    if fox.is_verbose():
        pp.p_debug("Using target ==> {}".format(fox.get_site()))

if args.ex_query:
    fox.set_ex_query(args.ex_query.strip())

    if fox.is_verbose():
        pp.p_debug("Using extra query parameters ==> {}".format(fox.\
                get_ex_query()))

if args.query:
    fox.set_raw_query(args.query.strip())

    if fox.is_verbose():
        pp.p_debug("Using query ==> {}".format(fox.get_raw_query()))

if args.inc:
    if not args.query:
        pp.p_error("Query not found, but inclusive switch is on")
        quit()

    fox.set_inc_q()
    if fox.is_verbose():
        pp.p_debug("Including dorks results along with query results")

if args.category:
    fox.set_category(args.category.strip())

    if fox.is_verbose():
        pp.p_debug("Using category ==> {}".format(fox.get_category()))

fox.set_severity(5)
fox.set_severity_flag(0)

if args.severity:
    fox.set_severity(args.severity)

# 0 for >= severity
# 1 for = severity
# 2 for < severity
if args.s_only:
    fox.set_severity_flag(1)
if args.s_upper:
    fox.set_severity_flag(2)

if args.s_all:
    fox.set_severity(0)
    fox.set_severity_flag(0)

if fox.is_verbose() and args.s_all:
    if args.severity:
        pp.p_debug("Severity is overridden by `--all` switch")
    
if args.s_qual:
    fox.set_severity(8)
    fox.set_severity_flag(0)

if fox.is_verbose() and args.s_qual:
    if args.severity or args.s_all:
        pp.p_debug("Severity is overridden by `--quality` switch")

if fox.is_verbose():
    s_m = ''
    if fox.get_severity_flag() == 0:
        s_m = 'min'
    elif fox.get_severity_flag() == 1:
        s_m = 'only'
    elif fox.get_severity_flag() == 2:
        s_m = 'max'
    pp.p_debug("Using severity ==> {}".format(fox.get_severity()))
    pp.p_debug("Using Severity as ==> {}".format(s_m))

fox.set_page_size(30)
if args.page_size:
    fox.set_page_size(args.page_size)

if fox.is_verbose():
    pp.p_debug("Using page size ==> {}".format(fox.get_page_size()))

fox.set_dork_size(150)
if args.dork_size:
    fox.set_dork_size(args.dork_size)

if fox.is_verbose():
    pp.p_debug("Max results per dork ==> {}".format(fox.get_dork_size()))

# defaults to 100 dorks 
fox.set_max_results(fox.get_dork_size() * 100)
if args.max_results and args.max_results >= 0:
    fox.set_max_results(args.max_results)

if fox.is_verbose():
    pp.p_debug("Total results limit to ==> {}".format(fox.get_max_results()))

s_delay = 2
e_delay = 7
if args.delay and args.delay >= 0:
    s_delay = e_delay = args.delay
else:
    if args.min and args.max:
        s_delay = args.min
        e_delay = args.max
    elif args.min:
        s_delay = args.min
        e_delay = s_delay + 5
    elif args.max:
        e_delay = args.max
        s_delay = 0
        if e_delay - 5 > 0:
            s_delay = e_delay - 5

fox.set_delay_range(s_delay, e_delay)
if fox.is_verbose(): 
    pp.p_debug("Using delay range ==> [{}, {}] sec".format\
            (fox.get_delay_start(), fox.get_delay_end()))

fox.set_max_parallel(5)
if args.parallel and args.parallel > 0:
    fox.set_max_parallel(args.parallel)

if fox.is_verbose():
    pp.p_debug("Using parallel requests ==> {}".format(\
            fox.get_max_parallel()))

if args.UA:
    fox.set_ua(args.UA.strip())

if fox.is_verbose() and fox.has_ua():
    pp.p_debug("Using User-Agent ==> {}".format(fox.get_ua()))

if args.output:
    fox.set_out_dir(dutil.create_dir(args.output.strip()))
else:
    pp.p_error("Output directory is not specified")
    quit()

fox.set_build_report()
if args.json and not args.report:
    fox.unset_build_report()

if fox.is_verbose(): 
    pp.p_debug("Using output directory ==> {}".format(fox.get_out_dir()))
    if fox.get_build_report():
        pp.p_debug("Output will be saved in JSON format")
    else:
        pp.p_debug("Reporting is enabled, along with JSON format")

pp.p_log("Building db.")
fox.dbBuilder()
pp.p_log("Finished building db")
