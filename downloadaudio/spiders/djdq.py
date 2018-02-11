# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

from downloadautio.file_handle import FileEntry
from downloadautio.items import DownloadautioItem
from downloadautio import settings


class DjdqSpider(scrapy.Spider):
    name = 'dautio'

    allowed_domains = ['www.520tingshu.com']

    start_url = settings.MURL

    def __init__(self):
        self.server_url = 'http://www.520tingshu.com'
        self.fileEntry = FileEntry()

    def start_requests(self):
        self.start_url = self.fileEntry.readUrl()
        print("startUrl:" + self.start_url)
        yield scrapy.Request(url=self.start_url, callback=self.parse1)

    def parse1(self, response):
        sel = Selector(response)
        aTagList = sel.xpath('//li//a[re:test(@href, "/down/?.{3,20}$")]')
        autio_title = sel.xpath('//*[@id="baybox"]/div/div[1]/dl/dd[1]//h2/text()').extract()
        items = []
        for index in range(len(aTagList)):
            item = DownloadautioItem()
            cl = aTagList[index]
            title = cl.xpath('@title').extract()
            url = str(cl.xpath("@href").extract())
            strQuestionMarkIndex = url.index('?')
            strPeriodIndex = url.index('.')
            newUrl = url[strQuestionMarkIndex + 1:strPeriodIndex]
            list = newUrl.split('-')
            id = list[0]
            pid = list[1]
            vid = list[2]
            newUrl = '/xunleidown/?id=' + id + '&vid=' + vid + '&pid=' + pid

            tUrl = self.server_url + newUrl
            item['link_url'] = str(tUrl)
            item['file_name'] = title
            item['autio_title'] = autio_title

            items.append(item)
        for item in items:
            url = item['link_url']
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        item['link_url'] = response.url
        sel = Selector(response)
        downloadUrl = sel.xpath('//a/@thunderhref').extract()
        item['down_url'] = downloadUrl
        yield item
