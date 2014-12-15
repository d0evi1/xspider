#!/bin/bash

#scrapy startproject xspider
#scrapy genspider movie  movie.com


#scrapy crawl xspider

date +"%Y%m%d %H:%m:%s"
date +%s

killall -9 python
#scrapy crawlall

#export SCRAPY_PROJECT=TopMovieSpider
#scrapy crawl TopMovieSpider 

### 1. movie.
#rm ./xspider/log/movie.log
#export SCRAPY_PROJECT=MovieSpider
#scrapy crawl MovieSpider 

###
rm ./xspider/log/celebrity.log
export SCRAPY_PROJECT=CelebritySpider
scrapy crawl CelebritySpider 



#killall -9 scrapy

#find . -name "*.pyc" -print -exec rm -rf {} \;
