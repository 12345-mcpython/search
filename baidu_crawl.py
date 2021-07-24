import requests
from bs4 import BeautifulSoup

from search.config.config import Config
from search.database.mysql import Simple

db = Simple(Config.MYSQL['MYSQL_HOST'], Config.MYSQL["MYSQL_PORT"], Config.MYSQL['MYSQL_USER'],
            Config.MYSQL['MYSQL_PASSWORD'], "so")

l = []
b = []
h1 = []
for k in range(10):
    r = requests.get("http://www.baidu.com/s?wd={}&pn={}".format("我的世界", k * 10), headers=Config.HEADERS)
    print(k, r)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    print(r.text)
    a = soup.find_all(class_="result")
    for i in a:
        b.append(i.find("a"))

    for j in b:
        s = ""
        # print(j.attrs['href'])
        a = requests.get(j.attrs['href'], headers=Config.HEADERS, proxy={"http": "122.136.212.132", "https": "122.136.212.132"})
        a.encoding = "utf-8"
        l.append(a.url)
        soup1 = BeautifulSoup(a.text, "lxml")
        cc = soup1.find("meta")
        if cc.get("charset"): a.encoding = cc.get("charset")
        print(soup1.title.string)
        if soup1.title:
            h1.append(soup1.title.string)
        else:
            h1.append(a.url)
for i in zip(h1, l):
    res = db.insert_data("baidu", ("title", "url"), tuple(i))
    if res == "-1":
        print("Fail to insert data")
    elif res >= 0:
        print("Successful insert data")
