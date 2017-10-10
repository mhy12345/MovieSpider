import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
from database import db

def fetch_basic_info(mid):
    result = {'id':mid}
    url = 'http://piaofang.maoyan.com/movie/%d'%mid
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html,'lxml')
    #print(soup.title)
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
    db.maoyan_info.save(result)


def fetch_cel_info(mid):
    url = 'http://piaofang.maoyan.com/movie/%d/celebritylist'%mid
    result = {'id':mid}
    html = urllib.request.urlopen(url).read().decode('utf-8')
    with open('cel.html','w') as f:
        f.write(html)
    soup = BeautifulSoup(html,'lxml')
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
        print(result)
        db.maoyan_cel_info.save(result)

def fetch_com_info(mid):
    url = 'http://piaofang.maoyan.com/movie/%d/companylist'%mid
    result = {'id':mid}
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html,'lxml')
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
        print(result)
        db.maoyan_com_info.save(result)

def clean():
    db.maoyan_com_info.remove({})
    db.maoyan_cel_info.remove({})
    db.maoyan_info.remove({})


if __name__ == "__main__":
    mid = 0
    clean()
    while True:
        mid += 1
        fetch_basic_info(mid)
        fetch_cel_info(mid)
        fetch_com_info(mid)
        print(mid)
