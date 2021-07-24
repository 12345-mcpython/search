import os
import time
from importlib import import_module

from search.config.config import Config


def file_name(file_dir=os.path.join(Config.BASE_DIR, "crawler\\spider")):
    """
    Get spider class
    :param file_dir: Spider dir
    :return: Spider files
    """
    all_files = []
    for file in os.listdir(file_dir):
        if file.endswith("_crawl.py"):
            all_files.append(file.replace(".py", ""))
    return all_files


def spider_console():
    print("Spider Console Running...")
    start = time.time()
    all_files = file_name()
    for spider in all_files:
        spider_module = import_module("search.crawler.spider.{}".format(spider))
        spider_module.main()

    print(f"Time costs: {time.time() - start}")


if __name__ == "__main__":
    spider_console()
