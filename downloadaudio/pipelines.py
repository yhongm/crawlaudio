# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from downloadautio import settings
import requests
import os

from downloadautio.file_handle import FileEntry


class DownloadautioPipeline(object):
    def __init__(self):
        self.fileEntry = FileEntry()

    def process_item(self, item, spider):
        downUrl = item['down_url'][0]
        fileName = item['file_name'][0]
        autio_title = item['autio_title'][0]
        print("item fileName:" + fileName + ",downUrl:" + str(downUrl))
        localPath = self.fileEntry.readPath()
        dir_path = '%s/%s' % (localPath, autio_title)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        houzui = downUrl[downUrl.index('.', len(downUrl) - 5, len(downUrl)): len(downUrl)]
        autio_file_path = fileName + houzui
        print("autio_path:" + autio_file_path)
        autio_file = '%s/%s ' % (dir_path, autio_file_path)

        print("autio_file:" + autio_file)
        print("download_url:" + downUrl)
        if not os.path.exists(autio_file):
            with open(autio_file, 'wb') as handle:
                response = requests.get(url=downUrl)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

        return item
