# -*- coding: utf-8 -*-

#-----------------------------------------------
# Define your item pipelines here
#
#-----------------------------------------------

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
class MoviePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'douban_movie',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
    
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
    #
    #-----------------------------
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error)
        return item

    #------------------------------
    ### insert into db.
    #------------------------------
    def insert_data(self, tx, item):
        tx.execute("select * from t_movies where subject_id = %s",(item['subject_id'][0],))
        result = tx.fetchone()

        if result:
            log.msg("Item already stored in db:%s" % item,level=log.INFO)
        else:
            ## 特殊，多个
            subject_id  = self.get_first(item['subject_id'])
            name        = self.get_first(item['name'])

            director    = self.get_items(item['director'])
            writer      = self.get_items(item['writer'])
            actor       = self.get_items(item['actor'])
            category    = self.get_items(item['category'])
            area        = self.get_items(item['area'])
            lang        = self.get_items(item['lang'])

            play_time   = self.get_first(item['play_time'])

            length      = self.get_first(item['length'])
            alias_name  = self.get_items(item['alias_name'])
            
            imdb        = self.get_first(item['imdb'])
            score       = self.get_first(item['score'], True)
            score_num   = self.get_first(item['score_num'], True)

            collects    = re.findall('\d+', self.get_first(item['collect_num']))
            collect_num = self.get_first(collects, True)

            wishes      = re.findall('\d+', self.get_first(item['wish_num'])) 
            wish_num    = self.get_first(wishes, True)

            synopsis    = self.get_first(item['synopsis'])
            update_time  = int(time.time())

            tx.execute(\
                "insert into t_movies (subject_id,\
                    name,\
                    director,\
                    writer,\
                    actor,\
                    category,\
                    area,\
                    lang,\
                    play_time,\
                    length,\
                    alias_name,\
                    imdb,\
                    score,\
                    score_num,\
                    collect_num,\
                    wish_num,\
                    synopsis,\
                    update_time) \
                    values (%s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, \
                            %s, %s)",\
                (subject_id,\
                name,       \
                director,   \
                writer,     \
                actor,      \
                category,   \
                area,       \
                lang,       \
                play_time,  \
                length,     \
                alias_name, \
                imdb,       \
                score,      \
                score_num,  \
                collect_num,   \
                wish_num,   \
                synopsis,   \
                update_time))

            log.msg("item stored in db: %s" % item, level=log.INFO)

    ###
    def handle_error(self, e):
        log.err(e)
