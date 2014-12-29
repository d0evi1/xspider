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
rm ./xspider/log/movie.log
export SCRAPY_PROJECT=MovieSpider
scrapy crawl MovieSpider -s JOBDIR=dqs/moviespider 

###
#rm ./xspider/log/celebrity.log
#export SCRAPY_PROJECT=CelebritySpider
#scrapy crawl CelebritySpider -s JOBDIR=dqs/celebrityspider 

###
#rm ./xspider/log/user.log
#export SCRAPY_PROJECT=UserSpider
#scrapy crawl UserSpider -s JOBDIR=dqs/userspider 

##rm ./xspider/log/comment.log
##export SCRAPY_PROJECT=CommentSpider
##scrapy crawl CommentSpider -s JOBDIR=dqs/commentspider 




#killall -9 scrapy

#find . -name "*.pyc" -print -exec rm -rf {} \;
