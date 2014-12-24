use douban_movie;

-- ----------------------------------
-- 创建最佳短评表
-- ----------------------------------
drop table if exists t_comments;
create table if not exists t_comments (
    subject_id  bigint(11) unsigned     comment '豆瓣id',
    user_id     varchar(64)             comment '用户id',
    user_rank   smallint(11) unsigned   comment '用户评分',
    votes       smallint(11) unsigned   comment '支持数',
    day         date                    comment '点评时间', 
    comment     text                comment '评论',
    primary key(subject_id, user_id) 
) engine=MyISAM charset='utf8';

-- ----------------------------------
-- 创建最佳影评表 (此处的review用的是简介)
-- ----------------------------------
drop table if exists t_reviews;
create table if not exists t_reviews (
    review_id   bigint(11)  unsigned not null   primary key comment '影评id',
    subject_id  bigint(11)  unsigned not null   comment '豆瓣id',
    user_id     varchar(64)  not null   comment '用户id',
    user_rank   int(11)     unsigned    comment '发表者评分',
    day         datetime                comment '点评时间',
    useful_cnt  int(11)     unsigned    comment '有用数',
    total_cnt   int(11)     unsigned    comment '总点赞数',
    reply_cnt   int(11)     unsigned    comment '回复数',
    review     text                    comment '影评'
) engine=MyISAM charset=utf8;
