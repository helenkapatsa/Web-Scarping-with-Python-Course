from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())


# Retrieves a list of all internal links found on a page
def get_internal_links(bs_obj, include_url):
    include_url = urlparse(include_url).scheme+"://"+urlparse(include_url).netloc
    internal_links = []
    # Finds all links that begins with a "/"
    for link in bs_obj.findAll("a", href=re.compile(("^(/|.*"+include_url+")"))):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                if (link.attrs['href']).startswith("/"):
                    internal_links.append(include_url+link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])
    return internal_links


# Retrieves a list of all external links found on a page
def get_external_links(bs_obj, exclude_url):
    external_links = []
    # Finds all links that ...
    for link in bs_obj.findAll("a", href=re.compile("^(http|www)((?!"+exclude_url+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links


def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs_obj = BeautifulSoup(html, "lxml")
    external_links = get_external_links(bs_obj, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print("No external links, looking around the site for one")
        domain = urlparse(starting_page).scheme+"://"+urlparse(starting_page).netloc
        internal_links = get_internal_links(bs_obj, domain)
        return get_random_external_link(internal_links[random.randint(0, len(internal_links)-1)])
    else:
        return external_links[random.randint(0, len(external_links)-1)]


def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print("Random external link is: "+external_link)
    follow_external_only(external_link)


follow_external_only("http://python.org")