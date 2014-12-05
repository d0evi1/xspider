# -*- coding: utf-8 -*-

#----------------------------------------------- 
# 从豆瓣抓取电影
#
# author:   d0evi1
# date:     2014.11.6
#-----------------------------------------------

from scrapy.item import Item, Field 

#----------------------------
# top 250's movie.
#----------------------------
class TopMovieItem(Item):
    name        = Field()   ## 电影名
    year        = Field()   ## 上映时间
    score       = Field()   ## 评分
    director    = Field()   ## 导演
    category    = Field()   ## 分类
    actor       = Field()   ## 演员列表 
    pass
