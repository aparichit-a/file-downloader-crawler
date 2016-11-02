# file-downloader-crawler
Scarpy crawler for downloading specific format of files. First the url's that you want to crawl will be fetched from the DB(if you want specify custom then you can remove the DB part), then scrapy will hit every url and parse all the href links and hit those links again(right now recursive level is set 1, you can change it in settings) and check if the content type is exist in allowed mime types then pass the url info to pipeline and save it into db.

Python 3.x is required and rest of the requirements mentioned in requirements.txt
