-- 
create database if not exists douban_movie charset=utf8;

-- 
use douban_movie;

-- 创建电影表
drop table if exists t_movies;
create table if not exists t_movies (
    subject_id  bigint(11) unsigned primary key comment '豆瓣id',
    dtype       smallint(11) unsigned not null comment '类型：电视剧 or 电影',
    name        varchar(256) comment '片名',
    director    varchar(512) comment '导演',
    writer      varchar(512) comment '编剧',
    actor       varchar(512) comment '主演',
    category    varchar(512) comment '类型',
    area        varchar(512) comment '制片地区',
    lang        varchar(128) comment '语言',
    play_time   varchar(128) comment '首映日期',
    length      varchar(128) comment '片长',
    alias_name  varchar(512) comment '别名',
    imdb        varchar(256) comment 'imdb url',
    score       double       comment '评分',
    score_num   int(11) unsigned    comment '评论人数',
    collect_num int(11) unsigned    comment '已看人数',
    wish_num    int(11) unsigned    comment '想看人数',
    synopsis    text                comment '剧情介绍',
    update_time int(11) unsigned    comment '更新时间'
)engine=MyISAM charset=utf8;

-- 创建评论表
