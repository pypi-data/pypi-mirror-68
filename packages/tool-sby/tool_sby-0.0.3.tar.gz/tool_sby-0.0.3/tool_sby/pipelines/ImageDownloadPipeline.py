#!/usr/bin/python3
# -*- coding:utf-8 -*-

from tool_sby import ImgHandler


class ImageDownloadPipeline(object):

    def __init__(self, project, crawl_ip, fields):
        self.project = project
        self.crawl_ip = crawl_ip
        self.fields = fields

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            project=crawler.settings.get('PROJECT_NAME', 'test'),
            crawl_ip=crawler.settings.get('CRAWL_IP', ''),
            fields=crawler.settings.get('fields', [])
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if self.fields:
            for field in self.fields:
                item[field] = ImgHandler.download(self.project, item[field], self.crawl_ip)
        return item
