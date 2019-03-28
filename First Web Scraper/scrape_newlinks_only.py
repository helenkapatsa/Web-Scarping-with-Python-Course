from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()


def get_links(page_url):
    global pages
    html = urlopen("http://en.wikipedia.org/"+page_url)
    bsObj = BeautifulSoup(html, "lxml")
    try:
        print("H1: ", bsObj.h1.get_text())
        print("1st paragraph:\n", bsObj.find(id = "mw-content-text").findAll("p")[0])
        print("Edit link: ", bsObj.find(id = "ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This paragraph is missing something! No worries though!")

    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if "href" in link.attrs:
            if link.attrs['href'] not in pages:
                new_page = link.attrs['href']
                print('--------------------\n'+new_page)
                pages.add(new_page)
                get_links(new_page)


get_links("")