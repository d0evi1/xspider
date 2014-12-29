use douban_movie;

-- 名人
drop table if exists t_celebrities;

create table if not exists t_celebrities(
    id              bigint(11)  not null primary key   comment 'celebrity id',
    name            varchar(128) not null   comment '姓名',
    sex             varchar(16)     comment '性别',
    constellation   varchar(32)     comment '星座',
    birthday        varchar(32)     comment '出生日期',
    birthplace      varchar(128)    comment '出生地',
    profession      varchar(32)     comment '职业',
    en_names        varchar(256)    comment '更多外文名',        
    ch_names        varchar(256)    comment '更多中文名',
    family          varchar(256)    comment '家庭成员',
    imdb            varchar(64)     comment 'imdb编号',
    intro           text            comment '影人简介',
    awards          text            comment '获奖情况',
    fans            int(11)         comment '影迷数',
    update_time     int(11)         comment '最近一次更新时间'
);
