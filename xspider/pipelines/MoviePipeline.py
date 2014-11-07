# -*- coding: utf-8 -*-

#-----------------------------------------------
# Define your item pipelines here
#
#-----------------------------------------------

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors

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
    #
    #-----------------------------
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error)
        return item

    #------------------------------
    ### insert into db.
    #------------------------------
    def insert_data(self,tx,item):
        tx.execute("select * from t_top_movie where name= %s",(item['name'][0],))
        result=tx.fetchone()
        log.msg(result,level=log.DEBUG)
        print result
        if result:
            log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
        else:
            category=''
            lenCate = len(item['category'])
            for n in xrange(lenCate):
                category+=item['category'][n]
                if n<lenCate-1:
                    category+='/'
            
            
            actor=''
            lenActor = len(item['actor'])
            for n in xrange(lenActor):
                actor+=item['actor'][n]
                if n<lenActor-1:
                    actor+='/'

            tx.execute(\
                "insert into t_top_movie (name,\
                    year,\
                    score,\
                    director,\
                    category,\
                    actor) values (%s,%s,%s,%s,%s,%s)",\
                (item['name'][0],\
                item['year'][0],\
                item['score'][0],\
                item['director'][0],\
                category,\
                actor))

            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    ###
    def handle_error(self, e):
        log.err(e)
