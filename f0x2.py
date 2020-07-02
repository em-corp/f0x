#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__NAME__    = "f0x.py"
__VERSION__ = "1.0"

import argparse
import re
import os
from git import Repo
from lib.prettyPrint import Prettify as pp
from lib.config import ConfigManager as conf
from lib.utils import DirUtil as dutil
from lib.utils import FileUtil as futil

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
    def _load_conf():
        conf.load('f0x2.config')
    
    def get_conf():
        if conf.getConfig is None:
            Fox._load_conf()
        return conf.getConfig()

    def get_dork_path():
        dp = ''
        try:
            dp = Fox.get_conf().get('dork_path')
        except:
            pp.p_error("Dorks path not exists, Check config file.")
            return
        else:
            if dp = '':
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

    def list_dorks_stats():
        dp = Fox.get_dork_path()
        if dp is None or dp = '':
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

    def update_dorks_repo():
        pp.p_log("Building Dork Repo.")
        repo_url = Fox.get_conf().get('repo_url')
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

        dutil.merge_dirs(tmpdir, Fox.get_dork_path)
        pp.p_log("Dork Repo updated.")



#------------------------------------------------------------------------------
verbose = args.verbose

if args.listrepo:
    Fox.list_dorks_stats()
    quit()

if args.updaterepo:
    Fox.update_dorks_repo()
    quit()
