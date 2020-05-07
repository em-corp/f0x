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

## usage
     f0x.py [-h] [-s SITE] [-q QUERY] [-i] [-A EX_QUERY] [-C CATEGORY] [-S {1,2,3,4,5,6,7,8,9,10}] 
     [--only] [--upper] [-a] [-Q] [-r PAGE_SIZE] [-t DORK_SIZE] [-T MAX_RESULTS] [-m MIN] [-M MAX] 
     [-d DELAY] [-p PARALLEL] [-U UA] [-o OUTPUT] [-j] [-R] [--update] [-L] [-v]


## example

     $ python3 f0x.py --update
     $ python3 f0x.py --L
     $ python3 f0x.py  -C 'Files_Containing_Juicy_Info'  -o /ghdb/juicyfiles  -T 60 -v
     $ python3 f0x.py  -S 9  -o /ghdb/juicyfiles  -T 60 -v


