#!/usr/bin/env pyton3
# -*- coding: utf-8 -*-

import argparse

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

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--site', help='Specify target site.', dest='site')

parser.add_argument('-q', '--query', help='Dork to use. If specified, other files will not be read.', dest='query')
parser.add_argument('-i', '--inclusive', help='This works with `query` option only, if used, will also read dorks from file. ', dest='', action="store_true")

parser.add_argument('-C', '--catagory', help='Use dorks from this catagory only.', dest='catagory')
parser.add_argument('-S', '--severity', help='Specify minimum severity(inclusive) dork file to read.', dest='severity')
parser.add_argument('-a', '--all', help='Use all the dork files to fetch result.', dest='', action='store_true')
parser.add_argument('-Q', '--quality', help='Use only top severity dork files.', dest='', action='store_true')

parser.add_argument('-r', '--results', help='Total results to fetch in one request, default is 30.', dest='page_size')
parser.add_argument('-t', '--total', help='Total results to fetch for each dork, default is 150.', dest='dork_size')
parser.add_argument('-T', '--max', help='Maximum results to fetch for all the dorks combined.', dest='max_results')

#parser.add_argument('-P', '--proxy', help='proxy', dest='')
#parser.add_argument('-f', '--proxy-file', help='list of proxies', dest='')
#parser.add_argument('-c', '--conn', help='connections per proxy', dest='')

parser.add_argument('-m', '--mintime', help='Specify minimum sec to wait between requests, If not specified, default 5 sec range is assumed', dest='min')
parser.add_argument('-M', '--maxtime', help='Specify maximum sec to wait between requests, if not specified, default 5 sec range is assumed.', dest='max')
parser.add_argument('-d', '--delay', help='Specify fix delay(in sec), if specified, took priority over variable delay.', dest='delay')
parser.add_argument('-p', '--parallel', help='Specify total no of parallel requests, default is 5.', dest='parallel')
parser.add_argument('-U', '--user-agent', help='Specify User Agent ', dest='UA')

parser.add_argument('-o', '--output', help='Specify output directory', dest='output')
parser.add_argument('-j', '--json', help='Save output in JSON format only', dest='', action="store_true")
parser.add_argument('-R', '--report', help='Create Report along with JSON format ouput', dest='', action="store_true")

parser.add_argument('-v', '--verbose', help='Be verbose.', dest='', action="store_true")
parser.add_argument('-V', '--version', help='Print version and exit', dest='', action="store_true")


args = parser.parse_args()




if args.site:
    target=args.site;

