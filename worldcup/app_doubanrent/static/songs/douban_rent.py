#!/usr/bin/python
#-*- coding:utf-8 -*-

from scrapy.spider import Spider 
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from douban_rent.items import DoubanRentItem


class doubanRentSpider(Spider):
    name = "douban_rent"
    start_urls = ["http://www.douban.com/group/shanghaizufang/"]
    rules = [
            Rule(SgmlLinkExtractor(allow=(r'http://www.douban.com/group/shanghaizufang/discussion\?start=\d+'))),
            Rule(SgmlLinkExtractor(allow=(r'http://www.douban.com/group/topic/\d+', callback="parse"))),
    ]

    def parse(self, response):
        sel  = Selector(response)
        item = DoubanRentItem() 

        item['title'] = sel.xpath('//title').extract()
        item['link']  = response.url
        item['desc']  = sel.xpath('//').extract()

