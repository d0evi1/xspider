#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------------------
# 用于抓取名人页面.
# @author   d0evi1 
# @date     2014.12.15
#---------------------------------------

import re
from scrapy import log
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

### items.
from xspider.user.UserItem import UserItem
from xspider.user.UserItem import CollectItem
from xspider.user.UserItem import WishItem
from xspider.user.UserItem import DoItem
from xspider.user.UserItem import FollowItem

#----------------------------------
# 只抓取电影数据.
#----------------------------------
class UserSpider(CrawlSpider):
    name="UserSpider"
    allowed_domains=["douban.com"]

    start_urls=[
            "http://www.douban.com/people/caishiyao/"
            ]
    
    rules=[
        ## 抽取链接
#        Rule(SgmlLinkExtractor(allow=(r'', ),

        ## 解析item
        Rule(SgmlLinkExtractor(allow=(r'^http://www.douban.com/people/[a-zA-Z0-9_]{3,32}/$')),callback="parse_user", follow=True),
#        Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/people/[a-zA-Z0-9_]{3,32}/collect')),callback="parse_collect", follow=True),
#        Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/people/[a-zA-Z0-9_]{3,32}/wish')),callback="parse_wish", follow=True),
#         Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/people/[a-zA-Z0-9_]{3,32}/do')),callback="parse_do", follow=True),
    ]

    #--------------------------------------
    # 解析用户.
    #--------------------------------------
    def parse_user(self,response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)
        
        item = UserItem()
        item['user_id']     = re.findall(r'^http://www.douban.com/people/(.*?)/', response.url)
        item['user_name']   = sel.xpath('//*[@id="db-usr-profile"]/div[@class="info"]/h1/text()').extract()
        item['location']    = sel.xpath('//*[@class="user-info"]/a[1]/text()').extract()
        item['reg_time']    = sel.xpath('//*[@class="user-info"]/div[1]/text()').extract()
        item['intro']       = sel.xpath('//*[@id="intro_display"]/text()').extract() 

        item['follows']  = sel.xpath('//div[@id="friend"]/dl[@class="obu"]').extract()

        log.msg("parser_user: %s" % item, level=log.INFO)
        
        return item

    #--------------------------------------
    # 看过电影列表. (1-n)
    #--------------------------------------
    def parse_collect(self, response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)
        
        item = CollectItem()
        item['user_id']   = re.findall(r'^http://movie.douban.com/people/(.*?)/', response.url)
        item['collects']  = sel.xpath('//div[@class="item"]').extract()
        log.msg("parser_collect: %s" % item, level=log.INFO)
        
        return item

    #--------------------------------------
    # 想看电影列表. (1-n)
    #--------------------------------------
    def parse_wish(self, response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)
        
        item = WishItem()
        item['user_id'] = re.findall(r'^http://movie.douban.com/people/(.*?)/', response.url)
        item['wishes']  = sel.xpath('//div[@class="item"]').extract()
        log.msg("parser_wish: %s" % item, level=log.INFO)
        
        return item

    #--------------------------------------
    # 想看电影列表. (1-n)
    #--------------------------------------
    def parse_do(self, response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)
        
        item = DoItem()
        item['user_id'] = re.findall(r'^http://movie.douban.com/people/(.*?)/', response.url)
        item['does']  = sel.xpath('//div[@class="item"]').extract()
        log.msg("parser_do: %s" % item, level=log.INFO)
        
        return item



