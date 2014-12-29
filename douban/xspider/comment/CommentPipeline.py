# -*- coding: utf-8 -*-

#-----------------------------------------------
# Define your item pipelines here
#
#-----------------------------------------------

from scrapy import log
from scrapy.http import Request
from scrapy import Selector

from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors

import re
import time

from xspider.comment.CommentItem import CommentItem
from xspider.comm.SetFilter import SetFilter 

#-----------------------------------
# 电影pipeline.
#-----------------------------------
class CommentPipeline(object):
    
    #------------------------------
    # mysql/redis.
    #------------------------------
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'douban_movie',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )

        ### redis filter.
        self.filter = SetFilter('xspider.set.subject_id')  
    
    #-----------------------------
    # 将一个list列表做拼接.
    #-----------------------------
    def get_items(self, item_list):
        ret = ''
        length = len(item_list)
        for n in xrange(length):
            ret += item_list[n]
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
    # 处理主过程.
    #-----------------------------
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error)
        return item

    #------------------------------
    ### insert into db.
    #------------------------------
    def insert_data(self, tx, item):
        self.insert_comments(tx, item)
        self.insert_reviews(tx, item)

    
    #---------------------------------
    # comment (user_id, user_rank, support, day, comments) 
    #---------------------------------
    def insert_comments(self, tx, item):
        subject_id  = item['subject_id'][0]
        comments    = item['comments']

        for comment in comments:
            csel = Selector(text=comment)
            user_id     = csel.xpath("//span[@class='comment-info']/a[1]/@href").re(r"^http://movie.douban.com/people/(.*?)/$") 
            user_id     = self.get_first(user_id)
            
            user_rank   = csel.xpath("//span[@class='comment-info']/span[contains(@class,'rating')]/@class").re('allstar(\d+)0')
            user_rank   = self.get_first(user_rank, True)

            votes       = csel.xpath("//span[@class='comment-vote']/span[@class='votes pr5']/text()").extract()
            votes       = self.get_first(votes, True)
            
            day         = csel.xpath("//span[@class='comment-info']/span[@class='']/text()").extract()
            day         = self.get_first(day)

            cmt         = csel.xpath("//div[@class='comment']/p/text()").extract()
            cmt         = self.get_items(cmt)

            log.msg("user_id=%s, user_rank=%s, votes=%s, day=%s, cmt=%s" %(user_id, user_rank, votes, day, cmt), level=log.INFO)
            tx.execute(\
                "insert into t_comments (subject_id,\
                    user_id,        \
                    user_rank,      \
                    votes,          \
                    day,            \
                    comment)        \
                    values (%s, %s, %s, %s, %s, %s)",\
                (subject_id,    \
                user_id,        \
                user_rank,      \
                votes,          \
                day,            \
                cmt))


    #---------------------------------
    # reviews (review_id, subject_id, user_id, user_rank, day, useful_cnt, total_cnt, reply_cnt, review)
    #---------------------------------
    def insert_reviews(self, tx, item):
        subject_id  = item['subject_id'][0]
        reviews    = item['reviews']
        
        log.msg("insert_reviews: %s" % len(reviews), level=log.INFO)
        for review in reviews:
            log.msg("review: %s" % review, level=log.INFO)
             
            csel = Selector(text=review)
            user_id     = csel.xpath("//div/h3/a[1]/@href").re(r"^http://movie.douban.com/people/(.*?)/$") 
            user_id     = self.get_first(user_id)

            review_id   = csel.xpath("//div/h3/a[2]/@href").re(r"^http://movie.douban.com/review/(\d+)/$") 
            review_id   = self.get_first(review_id)
            
            user_rank   = csel.xpath("//div[@class='review-hd-info']/span[contains(@class, 'allstar')]/@class").re("allstar(\d+)0")
            user_rank   = self.get_first(user_rank, True)

            day         = csel.xpath("//div[@class='review-hd-info']/a[1]/following-sibling::text()").extract() 
            day         = self.get_first(day, True)

            useful      = csel.xpath("//div[@class='review-short-ft']/span[contains(@id,'useful')]/text()").extract()
            useful      = self.get_first(useful, True)
            if useful is not None:
                useful  = useful.split('/')
                useful_cnt  = useful[0]
                total_cnt   = useful[1]
            else:
                useful_cnt  = None
                total_cnt   = None

            reply       = csel.xpath("//div[@class='review-short-ft']/a[1]/text()").re('(\d+)')
            reply_cnt   = self.get_first(reply, True) 

            review      = csel.xpath("//div[@class='review-short']/span[1]/text()").extract()
            review      = self.get_items(review)

            log.msg("subject_id=%s, user_id=%s, review_id=%s, user_rank=%s, day=%s, useful_cnt=%s, total_cnt=%s, reply=%s, review=%s" %(subject_id, user_id, review_id, user_rank, day, useful_cnt, total_cnt, reply_cnt, review), level=log.INFO)
            tx.execute(\
                "insert into t_reviews (subject_id,\
                    user_id,        \
                    review_id,      \
                    user_rank,      \
                    day,            \
                    useful_cnt,     \
                    total_cnt,      \
                    reply_cnt,      \
                    review)        \
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",\
                (subject_id,    \
                user_id,        \
                review_id,      \
                user_rank,      \
                day,            \
                useful_cnt,     \
                total_cnt,      \
                reply_cnt,      \
                review))
         
    ###
    def handle_error(self, e):
        log.err(e)
