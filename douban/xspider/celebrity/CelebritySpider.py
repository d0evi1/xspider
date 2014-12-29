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
from xspider.celebrity.CelebrityItem import CelebrityItem


#----------------------------------
# 只抓取电影数据.
#----------------------------------
class CelebritySpider(CrawlSpider):
    name="CelebritySpider"
    allowed_domains=["douban.com"]

    start_urls=[
            "http://movie.douban.com/subject/1907966/"
            ]
    
    rules=[
        ## 抽取链接
        Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/subject/\d+/\?from=subject-page')), ),
 
        ## 解析item
        Rule(SgmlLinkExtractor(allow=(r'^http://movie.douban.com/celebrity/\d+')),callback="parse_celebrity"),
    ]

    #-------------------------------------
    # 公共处理部分
    #-------------------------------------
    def process_common(self, response, sel, item):
        item['id']      = re.findall(r'\d+', response.url)
        item['name']    = sel.xpath('//*[@id="content"]/h1/text()').extract()

        sex = u"性别"
        item['sex']        = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]' % (sex)).extract() 
        constellation = u"星座"
        item['constellation'] = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(constellation)).extract() 
       
        birthday = u"出生日期"
        item['birthday']   = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(birthday)).extract() 
       
        birthplace = u"出生地"
        item['birthplace']  = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(birthplace)).extract() 

        profession = u"职业"
        item['profession']  = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(profession)).extract()

        en_names = u"更多外文名"
        item['en_names']  = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(en_names)).extract() 

        ch_names = u"更多中文名"
        item['ch_names']  = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(ch_names)).extract() 

        family = u"家庭成员"
        item['family']  = sel.xpath('(//span[text()="%s"]/following-sibling::text())[1]'%(family)).extract() 

        imdb = u"imdb编号"
        item['imdb']  = sel.xpath('(//span[text()="%s"]/following-sibling::a/text())[1]'%(imdb)).extract() 
        
        ## intro.
        item['intro']    = sel.xpath('//*[@id="intro"]/div[@class="bd"]/span[2]/text()').extract() 
        if len(item['intro']) == 0:
            item['intro'] = sel.xpath('//*[@id="intro"]/div[@class="bd"]/span[1]/text()').extract()  

        item['awards']  = sel.xpath('//*[@class="award"]/li/text()').extract()
        item['fans']    = sel.xpath('//*[@id="fans"]/div[@class="hd"]/h2/text()').extract() 

    #-------------------------------------
    # 处理电影
    #-------------------------------------
    def process_celebrity(self, response, sel):
        item = CelebrityItem()
      
        ## 公共部分
        self.process_common(response, sel, item)

        log.msg("celebrity: %s" % item, level=log.INFO)
        return item

    #--------------------------------------
    # 解析html元素.
    #--------------------------------------
    def parse_celebrity(self,response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)
        
        return self.process_celebrity(response, sel)

        ## 电视剧 or 电影
        #data_type = sel.xpath('(//span[@class="rec"]/a/@data-type)[1]').extract()
        #log.msg("%s" % data_type, level=log.INFO)
        #if cmp(data_type[0], "电视剧".decode('utf-8')) == 0:
        #    return self.process_drama(response, sel) 
        #elif cmp(data_type[0], "电影".decode('utf-8')) == 0:
        #    return self.process_movie(response, sel)
        #else:
        #    return None 
