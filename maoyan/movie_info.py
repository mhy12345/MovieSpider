#coding:utf-8
import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
from database import db
import time
import random
import proxy


def fetch_basic_info(mid):
    result = {'id':mid}
    url = 'https://piaofang.maoyan.com/movie/%d'%mid
    html = proxy.getHtmlViaProxy(url)
    with open('caches/%d_bas.html'%mid,'w') as f:
        f.write(html)
    soup = BeautifulSoup(html,'lxml')
    if re.search(r'抱歉，您的访问被我们识别为机器行为',html):
        return "Banned"
    if soup.title == None:
        return "Not found"
    result['title'] = soup.title.string
    res = soup.find(attrs={'class':'rating-num'})
    if res:
        result['rating-num'] = res.string
    res = soup.find(attrs={'class':'value'})
    if res:
        result['rating-total'] = "".join(res.strings).strip()
    res = soup.find(attrs={'class':'emspan'})
    if res:
        res = res.find('em')
    if res:
        result['emspan'] = "".join(res.strings)
    res = soup.findAll(class_='info-sb-item')
    if res:
        for w in res:
            res2 = w.find(class_='info-sb-percent')
            t1 = re.match(r'(\S*)\((\d*.\d*%)\)',res2.string)
            res3 = w.find(class_='info-sb-num')
            result['boxOffice_'+t1.group(1)+'_ratio'] = t1.group(2)
            result['boxOffice_'+t1.group(1)+'_num'] = "".join(map(lambda w:w.strip(),res3.strings))
    res = db.maoyan_info.find_one({'id':result['id']})
    if not res:
        db.maoyan_info.save(result)
    else:
        print("Already Exist!")
        exit()
    return "Success"


def fetch_cel_info(mid):
    url = 'https://piaofang.maoyan.com/movie/%d/celebritylist'%mid
    result = {'id':mid}
    #html = urllib.request.urlopen(url).read().decode('utf-8')
    html = proxy.getHtmlViaProxy(url)
    with open('caches/%d_cel.html'%mid,'w') as f:
        f.write(html)
    soup = BeautifulSoup(html,'lxml')
    if re.search(r'抱歉，您的访问被我们识别为机器行为',html):
        return "Banned"
    if soup.title == None:
        return "Not found"
    result['title'] = soup.title.string
    panels = soup.findAll(class_='panel-main')
    for panel in panels:
        ptitle = panel.find(class_='title-name').string
        result['field'] = ptitle
        clist = []
        elist = []
        items = panel.findAll(class_='p-item-name')
        if items:
            for item in items:
                clist.append(item.string)
        items = panel.findAll(class_='p-item-e-name')
        if items:
            for item in items:
                elist.append(item.string)
        result['elist'] = elist
        result['clist'] = clist
        if not db.maoyan_cel_info.find_one({'id':result['id'],'field':ptitle}):
            db.maoyan_cel_info.save(result)
        else:
            print("Already Exist!")
    return "Success"

def fetch_com_info(mid):
    url = 'https://piaofang.maoyan.com/movie/%d/companylist'%mid
    result = {'id':mid}
    html = proxy.getHtmlViaProxy(url)
    with open('caches/%d_com.html'%mid,'w') as f:
        f.write(html)
    soup = BeautifulSoup(html,'lxml')
    if re.search(r'抱歉，您的访问被我们识别为机器行为',html):
        return "Banned"
    if soup.title == None:
        return "Not found"
    result['title'] = soup.title.string
    panels = soup.findAll(class_='panel-main')
    for panel in panels:
        ptitle = panel.find(class_='title-name').string
        result['field'] = ptitle
        clist = []
        items = panel.findAll(class_='p-item-name')
        if items:
            for item in items:
                clist.append(item.string)
        result['list'] = clist
        #print(result)
        if not db.maoyan_com_info.find_one({'id':result['id'],'field':ptitle}):
            db.maoyan_com_info.save(result)
        else:
            print("Already Exist!")
    return "Success"

def clean(mid = None):
    if mid == None:
        db.maoyan_com_info.remove({})
        db.maoyan_cel_info.remove({})
        db.maoyan_info.remove({})
        db.maoyan_status.remove({})
    else:
        db.maoyan_com_info.remove({'id':mid})
        db.maoyan_cel_info.remove({'id':mid})
        db.maoyan_info.remove({'id':mid})
        db.maoyan_status.remove({'id':mid})



if __name__ == "__main__":
    mid = 1000
    while True:
        def run(func,mid):
            cnt = 0
            while True:
                cnt += 1
                res = func(mid)
                print(func.__name__,"(%d)"%mid,"...",res)
                if res == "Success":
                    break
                if res == "Banned":
                    time.sleep(random.randint(1,5))
                if res == 'Not found' and cnt>=3:
                    break
        if db.maoyan_status.find_one({'id':mid}):
            print(mid,"Already Exist!")
            mid += 1
            continue
        clean(mid)
        run(fetch_basic_info,mid)
        run(fetch_cel_info,mid)
        run(fetch_com_info,mid)
        db.maoyan_status.save({'id':mid})
        print(mid)
        mid += 1
        time.sleep(1)
