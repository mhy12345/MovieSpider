#-*- coding:utf-8 -*-
import urllib.request
import urllib
import time
import json
from database import db


tlist = ["剧情","喜剧","动作","爱情","科幻","动画","悬疑","惊悚","恐怖","纪录片","短片","情色","同性","音乐","歌舞","家庭","儿童","传记","历史","战争","犯罪","西部","奇幻","冒险","灾难","武侠","古装","运动","黑色电影"]

#https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=20&limit=20

def fetch_list():
    for it in range(1,len(tlist)+1):
        for ii in range(0,100,10):
            for il in range(0,10000,20):
                url = 'https://movie.douban.com/j/chart/top_list'
                params = {
                        'type':it,
                        'interval_id':'%d:%d'%(ii+10,ii),
                        'action':"",
                        'start':il,
                        'limit':20}
                urll = url + '?' + urllib.parse.urlencode(params)
                print(urll)
                response = urllib.request.urlopen(urll)
                data = response.read().decode('utf-8')
                data = json.loads(data)
                if len(data) == 0:
                    break
                for w in data:
                    print(w)
                    db.movie_list.insert(w)

print("Try to connect to database...")
title_list = db.movie_list.distinct('title')
id_list = db.movie_list.distinct('id')
print("Connection estabilished!")
print(len(title_list))
