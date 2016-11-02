import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler.items import CrawlerItem
import psycopg2
from urllib.parse import urljoin


class CrawlerSpider(CrawlSpider):
    name = 'crawler'
    allowed_domains = ''
    allowed_mime_type = [b'application/zip', b'application/x-msdownload', b'application/pdf', b'image/jpeg',
                         b'image/jpg',
                         b'image/png', b'application/octet-stream']
    conn = psycopg2.connect(user="root", password="password",
                            dbname="db_name",
                            host='localhost')
    cur = conn.cursor()
    cur.execute("SELECT * FROM table_name")
    db_urls = cur.fetchall()

    def __init__(self, *args, **kwargs):
        super(CrawlerSpider, self).__init__(*args, **kwargs)
        list = []
        for row in self.db_urls:
            list.append('http://' + row[1].lstrip(' '))
        self.start_urls = list

    def parse(self, response):
        self.logger.info("I am in parse method : %s", response.url)
        hxs = Selector(response)
        Urls = ''
        for url in hxs.xpath('//a/@href').extract():
            if (url.startswith('http://') or url.startswith('https://')):
                yield Request(url, callback=self.parse_item)
            elif 'javascript' not in url:
                new_url = urljoin(response.url, url.strip())
                print("New url : ", new_url)
                yield Request(new_url, callback=self.parse_item)
        for url in hxs.xpath('//iframe/@src ').extract():
            Urls += str(url) + ", "
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        if response.headers['Content-Type'] in self.allowed_mime_type:
            self.logger.info('Hi, this is an item page! %s', response.request.headers['referer'])
            item = CrawlerItem()
            item['file_urls'] = response.url
            item['referer'] = str(response.request.headers['referer'].decode("utf-8"))
            yield item
        else:
            self.logger.info('Not found any zip, lets try next page : %s', response.url)
            yield Request(response.url, callback=self.parse, dont_filter=True)
