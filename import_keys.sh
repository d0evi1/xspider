#!/bin/bash

#--------------------------------------
# map db'subject_id to redis.
#  
#--------------------------------------



function main()
{
    rm ./output.txt
    echo "select subject_id from t_movies" | mysql -uroot douban_movie -N > ./ids.txt
    while read line
    do
        echo "sadd xspider.set.MovieSpider $line " | redis-cli >> output.txt
    done < ./ids.txt 
}

main
