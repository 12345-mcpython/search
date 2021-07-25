import sys
import time

import requests
from bs4 import BeautifulSoup
from memcache import Client

from search.config.config import Config
from search.database.mysql import Simple
from search.utils.parse_url import get_url_scheme, url_join

mc = Client(["127.0.0.1:11211"], debug=True)
verbose = True


def disable_useless_url(url):
    if url.get("href"):
        if "javascript" not in url.get("href") and "#" not in url.get("href"):
            return True
        return False
    return False


def request(url):
    if verbose:
        print("Request url: ", url)
    memcached_title = get_memcached(url)
    if memcached_title:
        if verbose:
            print("Memcached has cache. cache: " + memcached_title, ", url: " + url)
        a = test_title(url, memcached_title)
        return a
    req = requests.get(url, headers=Config.HEADERS, timeout=15)
    req.encoding = req.apparent_encoding
    req.raise_for_status()
    return req


def request_clear(url):
    if verbose:
        print("Request url: ", url)
    req = requests.get(url, headers=Config.HEADERS, timeout=15)
    req.encoding = req.apparent_encoding
    req.raise_for_status()
    return req


def test_execute_file(url):
    if ".exe" in url or ".zip" in url or ".rar" in url or '.7z' in url or '.jpg' in url or '.png' in url or '.jar' in url or '.webm' in url or '.webp' in url:
        if verbose:
            print("Request ignore: is a execute file or image file!")
        return True
    return False


def save_memcached(url, title):
    mc.set(url, title)


def get_memcached(url):
    return mc.get(url)


def test_title(url, text):
    s = BeautifulSoup(text, "lxml")
    if s.title:
        if "mc" in s.title.string.lower() or "minecraft" in s.title.string.lower() or "我的世界" in s.title.string:
            if "登录" not in s.title.string and "提示信息" not in s.title.string and "注册" not in s.title.string:
                if verbose:
                    print("Check url successful: ", s.title.string.replace("\n", "").strip())
                save_memcached(url, s.title.string.strip().replace("\n", ""))
                return s.title.string
            # print("提示信息" not in s.title.string.lower())
            else:
                if verbose:
                    print("Request ignore: the page is login or register page: ",
                          s.title.string)
                save_memcached(url, s.title.string.strip().replace("\n", ""))
                return False
        else:
            if verbose:
                print("Result ignore: mc element not in s.title.string: ", s.title.string)
            save_memcached(url, s.title.string.strip().replace("\n", ""))
            return False
    else:
        if verbose:
            print("Result ignore: s.title.string is None")
        save_memcached(url, "null")
        return False


class MCCrawler:
    def __init__(self):
        self.start = time.time()
        self.db = Simple(Config.MYSQL['MYSQL_HOST'], Config.MYSQL["MYSQL_PORT"], Config.MYSQL['MYSQL_USER'],
                         Config.MYSQL['MYSQL_PASSWORD'], "so")
        self.verbose = True
        self.error_count = 0
        self.crawl_count = 0
        self.successful_count = 0
        self.duplicate_count = 0
        self.invalid_count = 0
        self.base_count = 0
        self.error_list = []

    def get_info(self):
        return self.db.query_data("baidu", "*")

    def crawl_url(self, url):
        try:
            print("Get Request: " + str(self.base_count))
            base_url = url[2]
            scheme = get_url_scheme(base_url)
            r = request_clear(base_url)
            soup = BeautifulSoup(r.text, "lxml")
            for i in soup.find_all("a"):
                self.crawl_count += 1
                ls = []
                if disable_useless_url(i):
                    result = url_join(scheme, i.get("href"))
                    if verbose:
                        print("Parsing {} url:".format(self.crawl_count), result)
                    if self.test_in_database(result):
                        continue
                    if test_execute_file(result):
                        self.invalid_count += 1
                        continue
                    req = request(result)
                    if not req:
                        self.invalid_count += 1
                        continue
                    title = test_title(result, req.text)
                    if not title:
                        self.invalid_count += 1
                        continue
                    ls.append(title.strip().replace("\n", ""))
                    if verbose:
                        print("Successful parse title:", title.replace("\n", "").strip())
                    ls.append(result)
                    res = self.db.insert_data("so_backup", ("title", "url"), tuple(ls))
                    if res == "-1":
                        print("Fail to insert data!")
                    self.successful_count += 1
        except Exception as e:
            import traceback
            print("Request error:", e)
            a = traceback.format_exc()
            self.error_list.append(a)
            self.error_count += 1
        except KeyboardInterrupt:
            use_time = time.time() - self.start
            print("\n" * 3)
            print('Stopped! ! !')
            print("Request count: {}".format(self.crawl_count))
            print("Request Error count: {}".format(self.error_count))
            print("Request Successful count: {}".format(self.successful_count))
            print("Request Invalid count: {}".format(self.invalid_count))
            print("Request Duplicate count: {}".format(self.duplicate_count))
            print('Request Error List is in error.txt')
            with open("error.txt", "w") as e:
                for i in self.error_list:
                    e.write(str(i) + "\n\n")
            print("Use time: " + str(round(use_time / 60, 2)) + "min", end="  ")
            print(str(round(use_time, 2)) + "s")
            sys.exit(0)

    def test_in_database(self, url):
        a = self.db.query_data("so_backup", "url")
        for i in a:
            url1 = i[0]
            if url1 == url:
                self.duplicate_count += 1
                if verbose:
                    print("Have duplicate url! Duplicate count: " + str(self.duplicate_count))
                return True
        return False

    def main(self):
        print("Start crawl.")
        a = self.get_info()
        for i in a:
            self.base_count += 1
            self.crawl_url(i)
        use_time = time.time() - self.start
        print("\n" * 3)
        print("Crawl successful! ")
        print("Request count: {}".format(self.crawl_count))
        print("Request Error count: {}".format(self.error_count))
        print("Request Successful count: {}".format(self.successful_count))
        print("Request Invalid count: {}".format(self.invalid_count))
        print("Request Duplicate count: {}".format(self.duplicate_count))
        if len(self.error_list) == 0:
            print('Request Error List is in error.txt')
            try:
                with open("error.txt", "w") as e:
                    for i in self.error_list:
                        e.write(str(i) + "\n\n")
            except Exception:
                print("Write Error!")
                import traceback
                traceback.print_exc()

        else:
            print("No error!")
        print("Use time: " + str(round(use_time / 60, 2)) + "min")


def main():
    crawler = MCCrawler()
    crawler.main()


if __name__ == "__main__":
    main()
