# -*- coding: utf-8 -*-

#-----------------------------------------------
# Define your item pipelines here
#
#-----------------------------------------------

import redis

from scrapy import log
from scrapy.http import Request

from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors

import re
import time

#-----------------------------------
#
#-----------------------------------
class CelebrityPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'douban_movie',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
        
        self.redis = redis.Redis('127.0.0.1')
        self.set_name = "xspider.set.celebrity_id"
        log.msg("init celebrity pipeline!", level=log.INFO)
    
    #-----------------------------
    # 将一个list列表做拼接.
    #-----------------------------
    def get_items(self, item_list):
        ret = ''
        length = len(item_list)
        for n in xrange(length):
            ret += item_list[n].strip()
            if n < length-1:
                ret += '/'

        return ret.strip()

    #-----------------------------
    # 获取list的第一个元素, 如果不存在，返回空.
    #-----------------------------
    def get_first(self, item_list, is_none=False):
        ret = ''
        length = len(item_list)
        if length > 0:
            ret = item_list[0].strip()
        else:
            if is_none:
                ret = None 
        return ret
   
    #-----------------------------
    # 获取简介.
    #-----------------------------
    def get_intro(self, item_list):
        length = len(item_list)
        if length >= 2:
            ret = item_list[1].strip()
        elif length == 1:
            ret = item_list[0].strip()
        else:
            ret = None

        return ret

    #----------------------------
    # 获取 awards.
    #-----------------------------
    def get_awards(self, item_list):
        ret = ''
        length = len(item_list)
        for n in xrange(length):
            ret += item_list[n]
            if n < length-1:
                ret += ' '

        return ret.strip()

    def get_fans(self, item_list):
        fans_info = self.get_first(item_list, True)
        if fans_info is None:
            return None

        fans = re.findall(r'\d+', fans_info)
        if len(fans) == 0:
            return None
        return int(fans[0]) 

    #-----------------------------
    #
    #-----------------------------
    def filter_head(self, item_list, is_single=True):
        if is_single:
            item_str = self.get_first(item_list)
        else:
            item_str = self.get_items(item_list)
        return item_str.lstrip(":").lstrip()

    #-----------------------------
    #
    #-----------------------------
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error)
        return item

    #------------------------------
    # 
    #------------------------------
    def add_filter(self, id):
        return self.redis.sadd(self.set_name, id)

    #------------------------------
    #
    #------------------------------
    def is_filter(self, id):
        return self.redis.sismember(self.set_name, id)

    #------------------------------
    ### insert into db.
    #------------------------------
    def insert_data(self, tx, item):
        ret = self.is_filter(item['id'][0]) 
        if ret == False:
            ## 特殊，多个
            id          = self.get_first(item['id'])
            name        = self.get_first(item['name'])
            sex         = self.filter_head(item['sex'])
            
            constellation   = self.filter_head(item['constellation'])
            birthday        = self.filter_head(item['birthday'])
            birthplace      = self.filter_head(item['birthplace'])
            profession      = self.filter_head(item['profession'])
            en_names        = self.filter_head(item['en_names'], False)
            ch_names        = self.filter_head(item['ch_names'], False)
            family          = self.filter_head(item['family'])
            imdb        = self.get_first(item['imdb'])
            intro       = self.get_items(item['intro']) 
            awards      = self.get_awards(item['awards'])
            fans        = self.get_fans(item['fans'])

            update_time  = int(time.time())

            tx.execute(\
                "insert ignore into t_celebrities (id,\
                    name,       \
                    sex,      \
                    constellation,   \
                    birthday,     \
                    birthplace,      \
                    profession,   \
                    en_names,       \
                    ch_names,       \
                    family,  \
                    imdb,     \
                    intro,       \
                    awards, \
                    fans, \
                    update_time) \
                    values (%s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, \
                            %s, %s, %s, %s, %s)",\
                (id,\
                name,     \
                sex,      \
                constellation,   \
                birthday,   \
                birthplace, \
                profession, \
                en_names,   \
                ch_names,   \
                family,     \
                imdb,       \
                intro,      \
                awards,  \
                fans, \
                update_time))

            log.msg("celebirty item to db: %s" % item, level=log.INFO)
            self.add_filter(id)

    ###
    def handle_error(self, e):
        log.err(e)
