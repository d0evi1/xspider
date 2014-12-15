# -*- coding: utf-8 -*-

#----------------------------------------------- 
# 从豆瓣抓取名人
#
# author:   d0evi1
# date:     2014.12.15
#-----------------------------------------------

from scrapy.item import Item, Field 

#-----------------------------
# every movie.
#-----------------------------
class CelebrityItem(Item):
    id              = Field()   ## 名人id
    name            = Field()   ## 姓名 
    sex             = Field()   ## 性别 
    constellation   = Field()   ## 星座 
    birthday        = Field()   ## 出生日期 
    birthplace      = Field()   ## 出生地 
    profession      = Field()   ## 职业 
    en_names        = Field()   ## 更多外文名 
    ch_names        = Field()   ## 更多中文名
    family          = Field()   ## 家庭成员 
    imdb            = Field()   ## imdb编号 
    intro           = Field()   ## 个人简介 
    awards          = Field()   ## 获奖情况 
    fans            = Field()   ## 豆瓣影迷数 

    pass
