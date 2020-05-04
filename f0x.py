#!/usr/bin/env pyton3
# -*- coding: utf-8 -*-

def banner():
    print ('''
     .o88o.   .o             o.   
     888 `"  .8'             `8.  
    o888oo  .8'  oooo    ooo  `8. 
     888    88    `88b..8P'    88 
     888    88      Y888'      88 
     888    `8.   .o8"'88b    .8' 
    o888o    `8. o88'   888o .8'  
    
    ''');
banner()

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--site', help='Specify target site.', dest='site')

parser.add_argument('-q', '--query', help='Dork to use. If specified, other files will not be read.', dest='query')
parser.add_argument('-i', '--inclusive', help='This works with `query` option only, if used, will also read dorks from file. ', dest='inc', action="store_true")

parser.add_argument('-C', '--category', help='Use dorks from this category only.', dest='category')
parser.add_argument('-S', '--severity', help='Specify minimum severity(inclusive) dork file to read, range is [0, 10], defalut: 5.', dest='severity', type=int, choices=range(11))
parser.add_argument('-a', '--all', help='Use all the dork files to fetch result.', dest='s_all', action='store_true')
parser.add_argument('-Q', '--quality', help='Use only top severity(>=8) dork files. ', dest='s_qual', action='store_true')

parser.add_argument('-r', '--results', help='Total results to fetch in one request, default is 30.', dest='page_size', type=int)
parser.add_argument('-t', '--total', help='Total results to fetch for each dork, default is 150.', dest='dork_size', type=int)
parser.add_argument('-T', '--max', help='Maximum results to fetch for all the dorks combined.', dest='max_results', type=int)

#parser.add_argument('-P', '--proxy', help='proxy', dest='')
#parser.add_argument('-f', '--proxy-file', help='list of proxies', dest='')
#parser.add_argument('-c', '--conn', help='connections per proxy', dest='')

parser.add_argument('-m', '--mintime', help='Specify minimum sec to wait between requests, If not specified, default 5 sec range is assumed', dest='min', type=int)
parser.add_argument('-M', '--maxtime', help='Specify maximum sec to wait between requests, if not specified, default 5 sec range is assumed.', dest='max', type=int)
parser.add_argument('-d', '--delay', help='Specify fix delay(in sec), if specified, took priority over variable delay.', dest='delay', type=int)
parser.add_argument('-p', '--parallel', help='Specify total no of parallel requests, default is 5.', dest='parallel', type=int)
parser.add_argument('-U', '--user-agent', help='Specify User Agent ', dest='UA')

parser.add_argument('-o', '--output', help='Specify output directory', dest='output')
parser.add_argument('-j', '--json', help='Save output in JSON format only', dest='json', action="store_true")
parser.add_argument('-R', '--report', help='Create Report along with JSON format ouput, default', dest='report', action="store_true")

parser.add_argument('-v', '--verbose', help='Be verbose.', dest='verbose', action="store_true")

args = parser.parse_args()

import re
import os
import errno
import sys


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
        args.output):
            print "[ERROR]: no options are specified"
            print parser.format_help()
            quit()

verbose = args.verbose

#read config file
def get_value(key):
    with open(sys.path[0] + '/f0x.config', 'r') as config:
        for line in config:
            if line.startswith(key):
                return line.split('=')[1].strip('\n')

site=''
# if site provided
if args.site:
    site = args.site.strip()
    site = re.sub(r'^http(s)?://(www\.)?', '', site)
    site = re.sub('/.*(/)?', '', site)

if verbose and args.site:
    print "Target recieved ==> {}".format(site)

r_query=''
# if raw query provided
if args.query:
    r_query = args.query.strip()

if verbose and args.query:
    print "Query provided ==> {}".format(r_query)

inclusive = args.inc

if inclusive and not args.query:
    print "[ERROR]: Query not found, but inclusive switch is on"
    quit()

if verbose and inclusive:
    print "Including dorks results along with query results"

category = ''
if args.category:
    category = args.category.strip()

if verbose and category:
    print "category recieved ==> {}".format(category)

severity = 5
if args.severity:
    severity = args.severity

if verbose and args.severity:
    print "Using severity ==> {}".format(severity)

if args.s_all:
    severity = 0

if verbose and args.s_all:
    if args.severity:
        print "Severity is overridden by `--all` switch"
    print "Using severity ==> {}".format(severity)
    
if args.s_qual:
    severity = 8


if verbose and args.s_qual:
    if args.severity or args.s_all:
        print "Severity is overridden by `--quality` switch"
    print "Using severity ==> {}".format(severity)

page_size = 30
if args.page_size:
    page_size = args.page_size / 10

    if  page_size >= 10:
        page_size = 100
    elif page_size >=5:
        page_size = 50
    elif page_size > 0 :
        page_size = page_size * 10
    else:
        page_size = 30

if verbose:
    print "page size ==> {}".format(page_size)

dork_size = 150
if args.dork_size and args.dork_size >= page_size:
    dork_size = args.dork_size

if verbose:
    print "max results per dork ==> {}".format(dork_size)

max_results = -1
if args.max_results:
    if args.max_results >= dork_size:
        max_results = args.max_results
    else:
        max_results = dork_size * 100
else:
    max_results = dork_size * 100

if verbose:
    print "total results limit to ==> {}".format(max_results)

delay = 2
var_delay = 5 
# total delay will be calculated as delay + (var_delay * random_no(0, 1))

if args.delay and args.delay >= 0:
    delay = args.delay
    var_delay = 0
else:
    if args.min and args.max:
        if args.min > 0 and args.max >= args.min:
            delay = args.min
            var_delay = args.max - args.min
        elif args.min > 0:
            delay = args.min
    elif args.min:
        if args.min > 0:
            delay = args.min
    elif args.max:
        if args.max >= var_delay  :
            delay = args.max - var_delay
        elif args.max >= 0:
            delay = 0
            var_delay = args.max

if verbose: 
    print "delay between each request ==> min {}, max {} sec".format(delay, delay + var_delay)

parallel_req = 5
if args.parallel and args.parallel > 0:
    parallel_req = args.parallel

if verbose:
    print "parallel requests set to ==> {}".format(parallel_req)


useragents = []
if args.UA:
    useragents = args.UA.strip().split(',')
else:
    with open(get_value('useragents'), 'r') as uas:
        useragents = [ua.strip('\n') for ua in uas]

if verbose:
    print "Using User-Agents ==> {}".format(useragents)

out_dir = ''

if args.output:
    out_dir = args.output
    
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
else:
    print "[ERROR]: Output directory is not specified"
    quit()

out_flag = 2 
# 2 > to save report along with json 
# 1 > to save json only
if args.json and not args.report:
    out_flag = 1

if verbose: 
    print "Using output directory ==> {}".format(out_dir)
    if out_flag == 1:
        print "Output will be saved in JSON format"
    else:
        print "Reporting is enabled, along with JSON format"
