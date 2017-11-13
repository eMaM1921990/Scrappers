import requests
from requests.auth import HTTPProxyAuth

__author__ = 'eMaM'


def test():
    proxies = {'https': '181.214.198.60:3199'}


    auth = HTTPProxyAuth('emam151987-8vew1', 'T9gsZ0HOk4')


    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',

    }
    scraped_html_page = requests.get('https://sfbay.craigslist.org/fb/sfo/vac/6331031900',
                                     timeout=None, proxies=proxies,headers=header)
    print scraped_html_page.status_code
    print scraped_html_page.text


test()
