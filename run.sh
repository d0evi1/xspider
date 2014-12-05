#!/bin/bash

#scrapy startproject xspider
#scrapy genspider movie  movie.com


#scrapy crawl xspider

killall -9 python
rm ./xspider/log/spider1.log
rm ./xspider/log/spider2.log
#scrapy crawlall

#export SCRAPY_PROJECT=TopMovieSpider
#scrapy crawl TopMovieSpider 

export SCRAPY_PROJECT=MovieSpider
scrapy crawl MovieSpider 



#killall -9 scrapy

#find . -name "*.pyc" -print -exec rm -rf {} \;
