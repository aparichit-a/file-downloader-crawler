# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import scrapy
import psycopg2
import datetime
import hashlib
import os

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

FILES_STORE = 'location_to_save_downloaded_files'


class CrawlerPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(user="root", password="password",
                                     dbname="db_name",
                                     host='localhost')

    def process_item(self, item, spider):
        item['path'] = self.write_to_file(item['file_urls'])
        cur = self.conn.cursor()
        cur.execute('''
                insert into table_name ( file_url, referer,path,created_date)
                values (%s, %s,%s, %s);
                ''', [
            item['file_urls'],
            item['referer'],
            item['path'],
            datetime.datetime.now()])
        self.conn.commit()
        return item

    def write_to_file(self, url):
        response = urllib2.urlopen(url)
        directory = FILES_STORE + str(hashlib.md5(url.encode('utf-8')).hexdigest()) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = url.split('/')[-1]
        with open(directory + str(file_name), "wb") as handle:
            handle.write(response.read())
        return directory + str(file_name)
