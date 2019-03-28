from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Multiplexing")
bsObj = BeautifulSoup(html, "lxml")
nameList = bsObj.findAll("a", {"class": "mw-redirect"})
for name in nameList:
    print(name.get_text())
