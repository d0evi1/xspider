#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapy import log
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xspider.spider1.TopMovieItem import TopMovieItem

class TopMoiveSpider(CrawlSpider):
    name="TopMovieSpider"
    allowed_domains=["movie.douban.com"]
    start_urls=["http://movie.douban.com/top250"]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_movie"),      
    ]

    def parse_movie(self,response):
        sel = Selector(response)
        item = TopMovieItem()
        log.msg(response.url, level=log.INFO)

        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year'] = sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        item['category'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor'] = sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()

        log.msg("%s" % item, level=log.INFO)
        return item


