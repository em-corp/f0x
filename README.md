# f0x

     .o88o.   .o             o.   
     888 `"  .8'             `8.  
    o888oo  .8'  oooo    ooo  `8. 
     888    88    `88b..8P'    88 
     888    88      Y888'      88 
     888    `8.   .o8"'88b    .8' 
    o888o    `8. o88'   888o .8'  
    

* Build on python3
* Fetch exposed URLs using google dorks.
* Support HTML Report to feed results to crawler.
* Support JSON & XML output of extracted urls to feed results to external apis.
* Support grep-able output generation.
* Suport proxies.
* Multithread & optimised for better performance.
* Easy dorks updation.
* Uses huge dork collection.
* Dorks db is updating frequently.
* Easily integrable with other tools.
* Can be easily optimized to generate low noise and fetch quality results.
* Can be used for checking leaked info for tagreted domain.
* Integrate in ecosystem to search for urls for targeted domain and check for any blacklisted/unwanted exposed info.
* Out of the box search queries can be easily extendable to check extra information.

## usage
     $f0x.py [-h] [-d DOMAIN] [-q QUERY] [-n] [-Q EX_QUERY] [-c CATEGORY] [-cA] [-S SEVERITY] [-SQ] [-SA] [-t THREADS] [-p PROXY]
     [-pF PROXY_FILE] [-pO] [-pC PROXY_COUNT] [-C PROXY_CONN] [--no-ssl-check] [--timeout TIME_OUT] [-m DELAY_MIN]
     [-M DELAY_MAX] [-w DELAY] [-U UA] [--update] [-v] [-V] [-r PAGE_SIZE] [-R NO_OF_PAGES] [-T MAX_RESULTS] [-l] [-L]
     [-o OUT_DIR] [-oJ] [-oX] [-oR] [--silent]


## example

     $ python3 f0x.py --update
     $ python3 f0x.py -L
     $ python3 f0x.py --any --quality -v -p "http://10.10.10.10:4444" --no-ssl-check -t 3


