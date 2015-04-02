#!/usr/bin/env python
# -*- coding: utf-8 -*-


create table train_behavior_type as
select dt,user_id,item_id,behavior_type,count(behavior_type) as cnt
from recommend_train_user_rs
group by user_id,item_id,behavior_type,dt;



create table demo_buy as
select a.user_id,a.item_id,a.dt,a._c3,a._c4,a._c5,a._c6
from
(select user_id,item_id,dt,
	sum(case behavior_type when 1 then cnt else 0 end),
	sum(case behavior_type when 2 then cnt else 0 end),
	sum(case behavior_type when 3 then cnt else 0 end),
	sum(case behavior_type when 4 then cnt else 0 end)
from train_behavior_type
group by user_id,item_id,dt)a
where a._c6>0;

create table tianchi_mobile_recommendation_predict as
select demo_buy.user_id,demo_buy.item_id
from demo_buy inner join recommend_train_item
on demo_buy.item_id=recommend_train_item.item_id
