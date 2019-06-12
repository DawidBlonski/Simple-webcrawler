import urllib.request
from urllib.parse import urlparse, urljoin
from requests.exceptions import InvalidSchema,MissingSchema,ConnectionError
import bs4 as bs
import sys
from pprint import pprint

class Page:
    def __init__(self, base_url, url):
        self.url = url
        self.base_url = base_url
        self.souped = None
        self.title = None
        self.links = None

    def soup(self):
        def clean(url):
            return url if urlparse(url).netloc else urljoin(self.base_url, url)

        sauce = urllib.request.urlopen(self.url).read()
        self.souped = bs.BeautifulSoup(sauce, "lxml")
        self.title = self.souped.title.string
        hrefs = set([clean(i.get("href")) for i in self.souped.findAll("a")])
        self.links = [link for link in hrefs if link.startswith(self.base_url)]
        return self

    @property
    def map_page(self):
        lookup = {self.url: {"title": self.title, "links": self.links}}
        return lookup


def site_map(base_url: str):
    if not isinstance(base_url,str):
        raise TypeError('Base URL must be a string')
    try:
        map_pages = {}
        links_to_map = [base_url]

        def check_and_add(url):
            if url not in map_pages:
                page = Page(base_url, url).soup()
                links_to_map.extend(page.links)
                map_pages.update(page.map_page)

        while links_to_map:
            check_and_add(links_to_map.pop())
        return map_pages

    except InvalidSchema as msg:
        print(msg, file=sys.stderr)
        print(msg.__doc__)
        exit()

    except ConnectionError as msg:
        print(msg, file=sys.stderr)
        print(msg.__doc__)
        exit()

    except MissingSchema as msg:
        print(msg, file=sys.stderr)
        print(msg.__doc__)
        exit()

    except ValueError as msg:
        print(msg,file = sys.stderr)
        print(msg.__doc__)
        exit()



if __name__ == "__main__":
    base_url = input('Enter a URL i.e "http://site.com"')
    pprint(base_url(input()))