# -*- coding: utf-8 -*-

#----------------------------------------------- 
# 从豆瓣抓取电影
#
# author:   d0evi1
# date:     2014.11.6
#-----------------------------------------------

from scrapy.item import Item, Field 

#-----------------------------
# every movie.
#-----------------------------
class MovieItem(Item):
    subject_id  = Field()   ## 豆瓣id
    name        = Field()   ## 电影名
    director    = Field()   ## 导演
    writer      = Field()   ## 编剧
    actor       = Field()   ## 主演
    category    = Field()   ## 类别
    area        = Field()   ## 地区
    lang        = Field()   ## 语言
    play_time   = Field()   ## 上映时间, 上映地
    length      = Field()   ## 片长
    alias_name  = Field()   ## 别名
    imdb        = Field()   ## imdb链接
    score       = Field()   ## 评分
    score_num   = Field()   ## 评分人数
    collect_num = Field()   ## 已看人数
    wish_num    = Field()   ## 想看人数
    synopsis    = Field()   ## 简介

    pass
