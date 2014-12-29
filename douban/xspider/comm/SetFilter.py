# -*- coding: utf-8 -*-

import redis

#-----------------------------------
# 采用redis进行过滤已爬链接. 
#       "xspider.set.user_id"
#-----------------------------------
class SetFilter(object):
    def __init__(self, set_name):
        self.redis      = redis.Redis('127.0.0.1')
        self.set_name   = set_name 
    
    #----------------------------------------
    # add somd data need to filter. (like: subject_id, user_id etc.) 
    #----------------------------------------
    def add_filter(self, id):
        return self.redis.sadd(self.set_name, id)

    #----------------------------------------
    # is in filter. 
    #----------------------------------------
    def is_exists(self, id):
        return self.redis.sismember(self.set_name, id)
