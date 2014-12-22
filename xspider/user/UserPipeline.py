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

from scrapy.selector import Selector
from xspider.user.UserItem import UserItem
from xspider.user.UserItem import CollectItem
from xspider.user.UserItem import WishItem
from xspider.user.UserItem import DoItem

import re
import time

#-----------------------------------
#
#-----------------------------------
class UserPipeline(object):
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
        self.set_name = "xspider.set.user_id"
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
 
    #----------------------------
    #
    #----------------------------
    def get_second(self, item_list, is_none=False):
        ret = ''
        length = len(item_list)
        if length > 1:
            ret = item_list[1].strip()
        else:
            if is_none:
                ret = None 
        return ret

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
        if isinstance(item, UserItem):
            query = self.dbpool.runInteraction(self.insert_user, item)
            query.addErrback(self.handle_error)
        elif isinstance(item, CollectItem):
            query = self.dbpool.runInteraction(self.insert_collect, item)
            query.addErrback(self.handle_error)
        elif isinstance(item, WishItem):
            query = self.dbpool.runInteraction(self.insert_wish, item)
            query.addErrback(self.handle_error)
        elif isinstance(item, DoItem):
            query = self.dbpool.runInteraction(self.insert_do, item)
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
    # 获取注册时间
    #------------------------------
    def get_regtime(self, items):
        reg_item = self.get_second(items)
        reg_time = re.findall(r'\d+-\d+-\d+', reg_item)
        return reg_time 

    #------------------------------
    # 从html中获取subject_id.
    #------------------------------
    def get_subjectid(self, subjectids_html):
        if len(subjectids_html) == 0:
            return None

        sids = re.findall(r'http://movie.douban.com/subject/(\d+)', subjectids_html[0])
        if len(sids) == 0:
            return None

        return sids[0] 

    #------------------------------
    # 从html中获取rank
    #------------------------------
    def get_rank(self, ranks_html):
        if len(ranks_html) == 0:
            return None

        ranks = re.findall(r'rating(\d+)-t', ranks_html[0])
        if len(ranks) == 0:
            return None

        return ranks[0]
            
    #------------------------------
    ### insert into db.
    #------------------------------
    def insert_user(self, tx, item):
        id = item['user_id'][0]
        ret = self.is_filter(id) 
        if ret:
            log.msg("filter id: %s" % id, level=log.INFO)
        else:
            ## 特殊，多个
            user_id     = self.get_first(item['user_id'])
            user_name   = self.get_first(item['user_name'])
            location    = self.get_first(item['location'])
            reg_time    = self.get_regtime(item['reg_time'])
            intro       = self.get_items(item['intro'])

            tx.execute(\
                "insert ignore into t_users (user_id,\
                    user_name,   \
                    location,      \
                    reg_time,   \
                    intro) \
                    values (%s, %s, %s, %s, %s)",\
                (user_id,\
                user_name,     \
                location,      \
                reg_time,   \
                intro))

            log.msg("user item to db: %s" % item, level=log.INFO)

    #--------------------------------------
    # 插入collect (看过)
    #--------------------------------------
    def insert_collect(self, tx, item):
        id = item['user_id'][0]
        collects = item['collects']

        i = 0
        log.msg('num=%s, collect=%s' %(len(collects), collects), level=log.DEBUG)
        for collect in collects:
            csel = Selector(text=collect)
            subject_ids  = csel.xpath('//div[@class="info"]/ul/li[1]/a/@href').extract()
            ranks        = csel.xpath('//div[@class="info"]/ul/li[3]/span[contains(@class,"rating")]/@class').extract()
            days          = csel.xpath('//div[@class="info"]/ul/li[3]/span[@class="date"]/text()').extract()
            log.msg('%s, %s, %s' % (subject_ids, ranks, days), level=log.INFO)
            
            user_id     = id
            subject_id  = self.get_subjectid(subject_ids)
            rank        = self.get_rank(ranks)
            day         = self.get_first(days)
            
            tx.execute(\
                    "insert ignore into t_collect_list \
                    (user_id,       \
                        subject_id, \
                        rank,       \
                        day)       \
                     values (%s, %s, %s, %s)",\
                    (user_id,       \
                    subject_id,     \
                    rank,           \
                    day))

            log.msg("collect items to db: user_id=%s, subject_id=%s, rank=%s, day=%s" % (user_id, subject_id, rank, day), level=log.INFO)


    #--------------------------------------
    # 插入collect (看过)
    #--------------------------------------
    def insert_wish(self, tx, item):
        id = item['user_id'][0]
        wishes = item['wishes']

        i = 0
        log.msg('num=%s, wish=%s' %(len(wishes), wishes), level=log.INFO)
        for wish in wishes:
            csel = Selector(text=wish)
            subject_ids  = csel.xpath('//div[@class="info"]/ul/li[1]/a/@href').extract()
            days         = csel.xpath('//div[@class="info"]/ul/li[3]/span[@class="date"]/text()').extract()
            #log.msg('%s, %s' % (subject_ids, ranks), level=log.INFO)
            
            user_id     = id
            subject_id  = self.get_subjectid(subject_ids)
            day         = self.get_first(days)

            tx.execute(\
                    "insert ignore into t_wish_list \
                    (user_id,           \
                        subject_id,     \
                        day)            \
                     values (%s, %s, %s)",  \
                    (user_id,       \
                    subject_id,     \
                    day))

            log.msg("items to db: user_id=%s, subject_id=%s, day=%s" % (user_id, subject_id, day), level=log.INFO)

    #--------------------------------------
    # 插入collect (看过)
    #--------------------------------------
    def insert_do(self, tx, item):
        id = item['user_id'][0]
        does = item['does']

        i = 0
        log.msg('num=%s, do=%s' %(len(does), does), level=log.INFO)
        for do in does:
            csel = Selector(text=do)
            subject_ids  = csel.xpath('//div[@class="info"]/ul/li[1]/a/@href').extract()
            days         = csel.xpath('//div[@class="info"]/ul/li[3]/span[@class="date"]/text()').extract()
            #log.msg('%s, %s' % (subject_ids, ranks), level=log.INFO)
            
            user_id     = id
            subject_id  = self.get_subjectid(subject_ids)
            day         = self.get_first(days)

            tx.execute(\
                    "insert ignore into t_do_list \
                    (user_id,           \
                        subject_id,     \
                        day)            \
                     values (%s, %s, %s)",  \
                    (user_id,       \
                    subject_id,     \
                    day))

            log.msg("items to db: user_id=%s, subject_id=%s, day=%s" % (user_id, subject_id, day), level=log.INFO)

    ###
    def handle_error(self, e):
        log.err(e)
