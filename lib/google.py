__all__ = []

import urllib.parse as urlparse
import requests
import threading
import re


class GoogleSearch:
    _session_var = threading.local()
    
    def _init_session():
        if not hasattr(GoogleSearch._session_var, "session"):
            GoogleSearch._session_var.session = requests.Session()

    def session_cleanup():
        if hasattr(GoogleSearch._session_var, "session"):
            delattr(GoogleSearch._session_var, "session")
        
    def _get_session():
        GoogleSearch._init_session()
        return GoogleSearch._session_var.session

    def __qencode__(q):
        return urlparse.quote_plus(q)
    
    def correct_page_size(page_size):
        default = 30
        if not page_size:
            return default
        
        try:
            page_size = int(page_size)
        except:
            return  default
        
        page_size /= 10
        # consider lower bound
        if page_size >= 10: 
            page_size = 100
        elif page_size >= 5:
            page_size = 50
        elif page_size > 0:
            page_size = page_size * 10
        else:
            page_size = default
        
        return int(page_size)

    def prepare_URL(query, site='', params='', page_num=1, page_size=30):
        if not query or query == '':
            raise Exception("Query cannot be empty")
        
        if not site:
            site = ''
        if not params:
            params = ''

        u = 'https://www.google.com/search?gbv=1&q='
        u += GoogleSearch.__qencode__(query)
        if params != '':
            u += '+' + GoogleSearch.__qencode__(params)
        if site != '':
            u += '+' + GoogleSearch.__qencode__(site)
        u += '&btnG=Google+Search'

        page_size = GoogleSearch.correct_page_size(page_size)

        fmt = '{}&start={}&num={}'
        page_num = int(page_num)

        if page_num <= 1:
            return fmt.format(u, '', page_size)
        else:
            return fmt.format(u, (page_num - 1) * page_size, page_size)

    def fetch(url, UA='f0x.py (Linux; python/requests)', proxy=None,
              time_out=None, sslcheck=True):
        hdrs = {
                'Host': 'www.google.com',
                'User-Agent': UA,
                'Accept': 'text/html,application/xhtml+xml,application/xml;' + 
                        ' q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0, no-cache',
                'Pragma': 'no-cache',
                'TE': 'Trailers'
                }

        return GoogleSearch._get_session().get(url, headers=hdrs,
                                               proxies=proxy, timeout=time_out,
                                               verify=sslcheck).text

    def has_next(text):
        o = re.search('aria-label="Next page"[^>]*>((Next &gt;)|' + 
                '(<span [^>]*>&gt;</span>))</a>', text, re.I)
        if o:
            return True
        else:
            return False

    def extract_urls(text):
        urls = []
        for pat in re.findall('\s+href="/url\?q=([^"&]*)[^"]*"[^>]*>', text,
                              re.M | re.I):
            if not re.search('^http(s)?://(www\.)?[^.]*\.google\.com', pat,
                             re.I):
                up = urlparse.unquote(pat)
                if not up.startswith('/search?q='):
                    urls += [up]
        return urls
