# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DownloadautioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_name = scrapy.Field()
    link_url = scrapy.Field()
    down_url = scrapy.Field()
    file_path = scrapy.Field()
    autio_title = scrapy.Field()
