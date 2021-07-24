import scrapy


# import pymysql
# from search.config.config import Config
#
# def get_url():


class SoCrawlSpider(scrapy.Spider):
    name = 'so_crawl'
    start_urls = ['http://a.com/']

    def parse(self, response):
        pass
