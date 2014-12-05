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
from xspider.spider2.MovieItem import MovieItem


#----------------------------------
# 只抓取电影数据.
#----------------------------------
class MoiveSpider(CrawlSpider):
    name="MovieSpider"
    allowed_domains=["douban.com"]
    start_urls=["http://movie.douban.com/tag/%E7%94%B5%E5%BD%B1"]
    rules=[
        ## 抽取链接
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/%E7%94%B5%E5%BD%B1\?start=\d+.*')), ),
        ## 解析item
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_movie"),      
    ]

    #-------------------------------------
    # 处理电影
    #-------------------------------------
    def process_movie(self, response, sel):
        item = MovieItem()
        
        item['subject_id']  = re.findall(r'\d+', response.url) 
        item['name']        = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['director']    = sel.xpath('//*[@id="info"]/span[1]/span/a/text()').extract()
        item['writer']      = sel.xpath('//*[@id="info"]/span[2]/span/a/text()').extract()
        item['actor']       = sel.xpath('//*[@id="info"]/span[3]/span/a/text()').extract()
        item['category']    = sel.xpath('//span[@property="v:genre"]/text()').extract()

        area = u"制片国家/地区:"
        item['area']        = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]' % (area)).extract() 
        lang = u"语言:"
        item['lang']        = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(lang)).extract() 
        item['play_time']   = sel.xpath('//span[@property="v:initialReleaseDate"]/text()').extract() 
        item['length']      = sel.xpath('//span[@property="v:runtime"]/@content').extract()

        alias_name = u"又名:"
        item['alias_name']  = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(alias_name)).extract() 
        
        item['imdb']        = sel.xpath('//*[@id="info"]/a[last()]/text()').extract() 
        item['score']       = sel.xpath('//strong[@property="v:average"]/text()').extract() 
        item['score_num']   = sel.xpath('//span[@property="v:votes"]/text()').extract() 
       
        ## view_num
        item['collect_num'] = sel.xpath('//*[@class="subject-others-interests-ft"]/a[1]/text()').extract()
        item['wish_num']    = sel.xpath('//*[@class="subject-others-interests-ft"]/a[2]/text()').extract()
        
        ## intro.
        item['synopsis']    = sel.xpath('//span[@property="v:summary"]/text()').extract() 

        log.msg("spider: %s" % item, level=log.INFO)
        return item

    #--------------------------------------
    # 解析html元素.
    #--------------------------------------
    def parse_movie(self,response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)

        ## 电视剧 or 电影
        data_type = sel.xpath('(//span[@class="rec"]/a/@data-type)[1]').extract()
        log.msg("%s" % data_type, level=log.INFO)
        if cmp(data_type[0], "电视剧".decode('utf-8')) == 0:
            log.msg(data_type[0], level=log.INFO)
            return None 
        elif cmp(data_type[0], "电影".decode('utf-8')) == 0:
            log.msg(data_type[0], level=log.INFO)
            return self.process_movie(response, sel)
        else:
            return None 
