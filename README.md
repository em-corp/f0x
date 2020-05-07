# f0k

     .o88o.   .o             o.   
     888 `"  .8'             `8.  
    o888oo  .8'  oooo    ooo  `8. 
     888    88    `88b..8P'    88 
     888    88      Y888'      88 
     888    `8.   .o8"'88b    .8' 
    o888o    `8. o88'   888o .8'  
    

* Crawl URL from GHDB.
* Let user defined and saved dorks as per severity/category so dorks can be quickly executed to gather intel
* Generate Report and JSON file of extracted urls
* Require python3

** usage: f0x.py [-h] [-s SITE] [-q QUERY] [-i] [-A EX_QUERY] [-C CATEGORY]
              [-S {1,2,3,4,5,6,7,8,9,10}] [--only] [--upper] [-a] [-Q]
              [-r PAGE_SIZE] [-t DORK_SIZE] [-T MAX_RESULTS] [-m MIN] [-M MAX]
              [-d DELAY] [-p PARALLEL] [-U UA] [-o OUTPUT] [-j] [-R]
              [--update] [-L] [-v]

** optional arguments:
  -h, --help            show this help message and exit
  -s SITE, --site SITE  Specify target site.
  -q QUERY, --query QUERY
                        Dork to use. If specified, other files will not be
                        read.
  -i, --inclusive       This works with `query` option only, if used, will
                        also read dorks from file.
  -A EX_QUERY, --args EX_QUERY
                        Specify extra query to supply with each dorks.
  -C CATEGORY, --category CATEGORY
                        Use dorks from this category only.
  -S {1,2,3,4,5,6,7,8,9,10}, --severity {1,2,3,4,5,6,7,8,9,10}
                        Specify minimum severity(inclusive) dork file to read,
                        range is [0, 10], defalut: 5.
  --only                Use along with severity, to select only a particular
                        value.
  --upper               Use along with severity, to mark provided value as
                        upper limit (exclusive).
  -a, --all             Use all the dork files to fetch result (overrides
                        --only, --upper flags).
  -Q, --quality         Use only top severity(>=8) dork files (overrides
                        --only, --upper flags).
  -r PAGE_SIZE, --results PAGE_SIZE
                        Total results to fetch in one request, default is 30.
  -t DORK_SIZE, --total DORK_SIZE
                        Total results to fetch for each dork, default is 150.
  -T MAX_RESULTS, --max MAX_RESULTS
                        Maximum results to fetch for all the dorks combined.
  -m MIN, --mintime MIN
                        Specify minimum sec to wait between requests, If not
                        specified, default 5 sec range is assumed
  -M MAX, --maxtime MAX
                        Specify maximum sec to wait between requests, if not
                        specified, default 5 sec range is assumed.
  -d DELAY, --delay DELAY
                        Specify fix delay(in sec), if specified, took priority
                        over variable delay.
  -p PARALLEL, --parallel PARALLEL
                        Specify total no of parallel requests, default is 5.
  -U UA, --user-agent UA
                        Specify User Agent
  -o OUTPUT, --output OUTPUT
                        Specify output directory
  -j, --json            Save output in JSON format only
  -R, --report          Create Report along with JSON format ouput, default
  --update              Update Dorks Repo, and exit
  -L, --list            List Repo categories, total dorks and exit
  -v, --verbose         Be verbose.


** example

$ python3 f0x.py --update
$ python3 f0x.py --L
$ python3 f0x.py  -C 'Files_Containing_Juicy_Info'  -o /ghdb/juicyfiles  -T 60 -v
$ python3 f0x.py  -S 9  -o /ghdb/juicyfiles  -T 60 -v


