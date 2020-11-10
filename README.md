# f0x

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

## usage
     $f0x.py [-h] [-d DOMAIN] [-q QUERY] [-n] [-Q EX_QUERY] [-c CATEGORY] [-cA] [-S SEVERITY] [-SQ] [-SA] [-t THREADS] [-p PROXY]
     [-pF PROXY_FILE] [-pO] [-pC PROXY_COUNT] [-C PROXY_CONN] [--no-ssl-check] [--timeout TIME_OUT] [-m DELAY_MIN]
     [-M DELAY_MAX] [-w DELAY] [-U UA] [--update] [-v] [-V] [-r PAGE_SIZE] [-R NO_OF_PAGES] [-T MAX_RESULTS] [-l] [-L]
     [-o OUT_DIR] [-oJ] [-oL] [-oR]


## example

     $ python3 f0x.py --update
     $ python3 f0x.py -L
     $ python3 f0x.py --any --quality -v -p "http://10.10.10.10:4444" --no-ssl-check -t 3


