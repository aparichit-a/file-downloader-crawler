# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlerItem(scrapy.Item):
    files = scrapy.Field()
    path = scrapy.Field()
    file_urls = scrapy.Field()
    referer = scrapy.Field()
