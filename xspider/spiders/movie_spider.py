#!/usr/bin/python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xspider.items import TopMovieItem

class MoiveSpider(CrawlSpider):
    name="xspider"
    allowed_domains=["movie.douban.com"]
    start_urls=["http://movie.douban.com/top250"]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_movie"),      
    ]

    def parse_movie(self,response):
        sel = Selector(response)
        item = TopMovieItem()

        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        item['category'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor'] = sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
        return item


