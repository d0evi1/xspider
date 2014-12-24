# -*- coding: utf-8 -*-

#----------------------------------------------- 
# 从豆瓣抓取电影
#
# author:   d0evi1
# date:     2014.11.6
#-----------------------------------------------

from scrapy.item import Item, Field 

#-----------------------------
# 短评 (1-n)
#-----------------------------
class CommentItem(Item):
    subject_id  = Field()   ## 豆瓣id
    comments    = Field()   ## 热门短评
    reviews     = Field()   ## 热门影评
    pass
