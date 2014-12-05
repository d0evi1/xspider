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
#    start_urls=["http://movie.douban.com/tag/%E7%94%B5%E5%BD%B1"]
#    rules=[
#        ## 抽取链接
#        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/%E7%94%B5%E5%BD%B1\?start=\d+.*')), ),
#        ## 解析item
#        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_movie"),      
#    ]

    start_urls=["http://movie.douban.com/tag/%E7%88%B1%E6%83%85"]
    rules=[
        ## 抽取链接
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/%E7%88%B1%E6%83%85\?start=\d+.*')), ),
        ## 解析item
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_movie"),      
    ]

    #-------------------------------------
    # 公共处理部分
    #-------------------------------------
    def process_common(self, response, sel, item):
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

 


    #-------------------------------------
    # 处理电视剧, xpath解析
    #-------------------------------------
    def process_drama(self, response, sel):
        item = MovieItem()
       
        ## 公共部分
        self.process_common(response, sel, item)

        ## 电视剧特殊部分.
        item['dtype']       = ['2']
        
        length = u"单集片长:"
        item['length']        = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]' % (length)).extract() 
 
        sets = u"集数:"
        item['sets']        = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]' % (sets)).extract() 
 
        log.msg("spider: %s" % item, level=log.INFO)
        return item

    #-------------------------------------
    # 处理电影
    #-------------------------------------
    def process_movie(self, response, sel):
        item = MovieItem()
      
        ## 公共部分
        self.process_common(response, sel, item)


        ## 电影物殊部分 
        item['dtype']       = ['1']
        item['length']      = sel.xpath('//span[@property="v:runtime"]/@content').extract()
        item['sets']        = [] 
        
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
            return self.process_drama(response, sel) 
        elif cmp(data_type[0], "电影".decode('utf-8')) == 0:
            return self.process_movie(response, sel)
        else:
            return None 
