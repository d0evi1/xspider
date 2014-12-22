use douban_movie;

-- -------------------------------------
-- 用户
-- -------------------------------------
drop table if exists t_users;
create table if not exists t_users(
    user_id     varchar(64)  not null primary key  comment 'user id',
    user_name   varchar(64) not null    comment '用户名',
    location    varchar(64)             comment '常居地',
    reg_time    date                    comment '加入时间',
    intro       varchar(512)            comment '个人签名',
    update_time int(11) unsigned not null   comment '最后更新时间'
) engine=MyISAM charset='utf8';

-- -------------------------------------
-- 看过列表
-- -------------------------------------
drop table if exists t_collect_list;
create table if not exists t_collect_list (
    user_id         varchar(64) not null     comment 'user id',
    subject_id      bigint(11) unsigned not null     comment '电影id',
    rank            int(64)    unsigned         comment '评分',
    day             date                        comment '评分日期',
    primary key(user_id, subject_id)
) engine=MyISAM charset='utf8';

-- ------------------------------------
-- 想看列表
-- ------------------------------------
drop table if exists t_wish_list;
create table if not exists t_wish_list (
    user_id         varchar(64) not null     comment 'user id',
    subject_id      bigint(11)  unsigned not null     comment '电影id',
    day             date                        comment '评分日期',
    primary key(user_id, subject_id)
) engine=MyISAM charset='utf8';

-- ------------------------------------
-- 在看列表
-- ------------------------------------
drop table if exists t_do_list;
create table if not exists t_do_list (
    user_id     varchar(64)     not null comment 'user id',
    subject_id  bigint(11)      not null comment '电影id',
    day         date                     comment '评分日期',
    primary key(user_id, subject_id)
) engine=MyISAM charset='utf8';

-- -------------------------------------
-- 关注列表.
-- -------------------------------------
drop table if exists t_follow_list;
create table if not exists t_follow_list (
    user_id     varchar(64)     not null comment 'user id',
    follow_id   varchar(64)     not null comment '关注者id',
    primary key(user_id, follow_id)    
) engine=MyISAM charset='utf8';
