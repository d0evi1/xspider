#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------------------
# 用于抓取页面.
# @author   d0evi1 
# @date     2014.11.8
#---------------------------------------

import re
from scrapy import log
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xspider.comment.CommentItem import CommentItem

#----------------------------------
# 只抓取电影数据.
#----------------------------------
class CommentSpider(CrawlSpider):
    name="CommentSpider"
    allowed_domains=["douban.com"]

    start_urls=["http://movie.douban.com/subject/21359619/"]
    rules=[
        ## 抽取链接
        #Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/2014\?start=\d+.*')), ),
        
        ## 解析item
        Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/subject/\d+/$')),callback="parse_comments", follow=True),     
        Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/subject/\d+/\?from=subject-page$')),callback="parse_comments", follow=True),     


    ]

    #-------------------------------------
    # 处理comments.
    #-------------------------------------
    def parse_comments(self, response):
        item = CommentItem()
        
        sel = Selector(response)

        item['subject_id']     = re.findall(r'^http://movie.douban.com/subject/(\d+)/', response.url) 
        item['comments']    = sel.xpath('//div[@class="comment"]').extract() 
        item['reviews']     = sel.xpath('//div[@class="review"]').extract() 
        
        log.msg("parse_comments: %s" % item, level=log.INFO)
        return item
