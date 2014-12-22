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
class UserItem(Item):
    user_id         = Field()   ## 名人id
    user_name       = Field()   ## 姓名 
    location        = Field()   ## 性别 
    reg_time        = Field()   ## 星座 
    intro           = Field()   ## 出生日期 
    pass

#-------------------------------
# collect list. (1-n)
# collects = (subject_id, rank)*n
# 需要自己去解析.
#-------------------------------
class CollectItem(Item):
    user_id     = Field()
    collects    = Field()
    pass

#-------------------------------
# wish lists. (1-n)
#-------------------------------
class WishItem(Item):
    user_id     = Field()
    wishes      = Field()
    pass

#--------------------------------
# 在看列表项.
#--------------------------------
class DoItem(Item):
    user_id     = Field()
    does        = Field()
    pass

#---------------------------------
# 关注列表
#---------------------------------
class FollowItem(Item):
    user_id     = Field()
    follow_id   = Field()
    pass
