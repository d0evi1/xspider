-- 
create database if not exists douban_movie charset=utf8;

-- 
use douban_movie;

--
drop table if exists t_movie;
create table if not exists t_movie (
    name        varchar(64),
    year        varchar(32),
    score       int(11) unsigned,
    director    varchar(128),
    category    varchar(128),
    actor       varchar(128)
)engine=MyISAM charset=utf8;   

