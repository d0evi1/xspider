#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
import re

from scrapy import signals,log
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import Request

#--------------------------------
# 主要功能：
# 1. 去重链接.
#--------------------------------
class MovieMiddleware(object):
    redis = None
    lock = True
    info = {}

    ### 
    def __init__(self):
        dispatcher.connect(self.open, signals.engine_started)
        dispatcher.connect(self.close, signals.engine_stopped)
    
    ### 
    def process_spider_output(self, response, result, spider):
        if self.lock is True:
            self.info = spider
            self.lock = False

        for x in result:
            if isinstance(x, Request):
                log.msg("type=%s, url=%s" %( type(x.url), x.url), level=log.INFO)
                url = re.findall(r"movie.douban.com/subject/\d+", x.url)
                
                if len(url) == 0:
                    yield x
                    continue
                
                [subject_id, ] = re.findall(r"\d+", url[0])
                set_name = "xspider.set.%s" % spider.name

                if self.redis.sismember(set_name, subject_id) is True:
                    log.msg(format="Filtered offsite request to page: %(request)s",
                                level=log.INFO, spider=spider, request=x)
                else:
                    yield x
            else:
                yield x

    ### init redis.
    def open(self):
        self.redis = redis.Redis('127.0.0.1')

    ### close redis. 
    def close(self):
        #self.redis.zrem(self.info.name, *self.info.start_urls)
        pass
