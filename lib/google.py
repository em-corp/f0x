__all__ = []

import urllib.parse as urlparse
import requests
import re

class GoogleSearch:

    def __qencode__(q):
        return urlparse.quote_plus(q)

    def prepare_URL(query, site = '', params = '', page_num = 1, \
            page_size = 30):
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

        page_size = int(page_size) / 10
        # consider lower bound
        if page_size >= 10: 
            page_size = 100
        elif page_size >= 5:
            page_size = 50
        elif page_size > 0:
            page_size = page_size * 10
        else:
            page_size = 30

        fmt = '{}&start={}&num={}'
        page_size = int(page_size)
        page_num = int(page_num)

        if page_num <= 1:
            return fmt.format(u, '', page_size)
        else:
            return fmt.format(u, (page_num - 1) * page_size, page_size)

    def fetch(url, UA = 'f0x.py/1.0 (Linux; python/requests)'):
        hdrs = {
                'Host': 'www.google.com',
                'User-Agent': UA,
                'Accept': 'text/html,application/xhtml+xml,application/xml;\
                        q=0.9,*/*;q=0.8',
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
        return requests.get(url, headers=hdrs).text

    def has_next(text):
        o = re.search('aria-label="Next page"[^>]*>((Next &gt;)|\
                (<span [^>]*>&gt;</span>))</a>', text, re.I)
        if o:
            return True
        else:
            return False

    def extract_urls(text):
        urls = []
        for pat in re.findall('\s+href="/url\?q=([^"&]*)[^"]*"[^>]*>', text, \
                re.M|re.I):
            if not re.search('^http(s)?://(www\.)?[^.]*\.google\.com', pat, \
                    re.I):
                up = urlparse.unquote(pat)
                if not up.startswith('/search?q='):
                    urls += [up]
        return urls


