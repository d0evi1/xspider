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
class CelebrityMiddleware(object):
    redis = None
    lock = True
    info = {}
    count = 0

    ### 
    def __init__(self):
        dispatcher.connect(self.open, signals.engine_started)
        dispatcher.connect(self.close, signals.engine_stopped)

    #---------------------------
    ### redis filter 
    #---------------------------
    def is_exist_url(self, url, spider_name):
        [id, ] = re.findall(r"\d+", url)
        set_name = "xspider.set.%s" % spider_name
        return self.redis.sismember(set_name, id)

    #----------------------------------------------
    # 当spider处理完response，返回result, 调用该函数
    #----------------------------------------------
    def process_spider_output(self, response, result, spider):
        if self.lock is True:
            self.info = spider
            self.lock = False

        self.count += 1
        log.msg("----------%d---------------" % self.count, level=log.INFO)
        for x in result:
            if isinstance(x, Request):
                url = re.findall(r"movie.douban.com/celebrity/\d+", x.url)
                ### none-celebrity url.
                if len(url) == 0:
                    log.msg(format="[process]filter return: return this page: %(request)s",
                         level=log.INFO, spider=spider, request=x) 
                    yield x
                    continue 
                
                ### celebrity url.
                if self.is_exist_url(url[0], spider.name) is True:
                    log.msg(format="[process]redis filter: Filter this page: %(request)s",
                         level=log.INFO, spider=spider, request=x) 
                else:
                    yield x
            else:
                yield x

    ### init redis.
    def open(self):
        log.msg("SpiderMiddleware is open().", level=log.INFO)
        self.redis = redis.Redis('127.0.0.1')


    ### close redis. 
    def close(self):
        log.msg("SpiderMiddleware is close()", level=log.INFO)
        #self.redis.zrem(self.info.name, *self.info.start_urls)
        pass
