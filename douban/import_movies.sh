#!/bin/bash

#--------------------------------------
# map db'subject_id to redis.
#  
#--------------------------------------



function add_all()
{
    rm ./output.txt
    echo "select subject_id from t_movies" | mysql -uroot douban_movie -N |
        while read line
        do
            echo "sadd xspider.set.MovieSpider $line " | redis-cli >> output.txt
        done 
}

function add_update()
{
    input=$1
    rm ./output.txt
    echo "select subject_id from t_movies where update_time > $input" | mysql -uroot douban_movie -N |
        while read line
        do
            echo "sadd xspider.set.MovieSpider $line " | redis-cli >> output.txt
        done 
}

case $1 in
all)
    echo "add_all"
    add_all
    ;;

update)
    echo "add_update"
    add_update $2
    ;;

*)
    echo "usage: $0 {all | update}"
esac

exit 0
