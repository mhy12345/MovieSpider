from bs4 import BeautifulSoup
import bs4
import re
from movie_list import id_list
import urllib
import threading
import time
import random
from proxy import ProxyPool
from database import db


Pool = ProxyPool()

def fetch_info(mid):
    url= 'https://movie.douban.com/subject/%s/'%mid
    print(url)
    html = Pool.getHtmlViaProxy(url)
    if html == "":
        return 
    soup = BeautifulSoup(html,'lxml')
    result = dict()
    result['id'] = mid
    res = soup.find(attrs={'id':'content'})
    if res != None and res.h1 != None:
        title_list = list(filter(lambda w:w!='\n',res.h1.contents))
    else:
        return 
    if len(title_list) == 1:
        result['title'] = title_list[0].string
        print("Warning : Title List with len 1!")
    elif len(title_list) == 2:
        result['title'] = title_list[0].string
        res = re.match(r'\((\d*)\)',title_list[1].string)
        if res!=None:
            result['year'] = res.group(1)
    else:
        print('Error : Title wrong!')
    info_box = soup.find(attrs={'id':'info'})
    texts = []
    for w in info_box.children:
        if type(w) == bs4.NavigableString:
            texts.append(str(w))
            continue
        texts.extend(w.strings)
    info_list = []
    for w in texts:
        if (w=='\n'):
            info_list.append("")
        else:
            info_list[-1] += w
    for w in info_list:
        if w == '':
            continue
        res = re.match(r'([^:]*): ([\s\S]*)',w)
        if res:
            result['_'+str(res.group(1))] = res.group(2).strip()
    res1 = soup.find(attrs={'class':'ll rating_num'})
    res2 = soup.find(attrs={'class':'rating_sum'})
    res3 = soup.find(attrs={'class':'tags'})
    if res1 != None:
        result['rating'] = res1.string
    if res2 != None:
        result['rating-sum'] = re.search(r"\d+","".join(soup.find(attrs={'class':'rating_sum'}).strings)).group(0)

    if res3 != None:
        result['tags'] = " / ".join(filter(lambda w:w!="",map(lambda w:w.strip(),soup.find(attrs={'class':'tags'}).div.strings)))
    return result


def run(taskList,start = 0):
    cnt = start
    taskList = taskList[start:]
    print("Length of the list is %d"%len(taskList))
    for w in taskList:
        print('>>> MAIN with movie ',w,cnt)
        cnt += 1
        res = db.movie_info.find_one({'id':w})
        if res:
            print("Already exist!")
            print(res)
            print("Skip!")
            continue
        else:
            print("Not found in database")
        data = fetch_info(w)
        if data:
            data['error'] = 'Success!'
            db.movie_info.insert(data)
            print("DB updated!")
            print(data)
        else:
            db.movie_info.insert({'id':w,'error':'Not found!'})
            print("NOT FOUND :",w)
        with open('log.txt','a') as f:
            f.write(str(cnt)+'$'+str(data)+'\n')
    

if __name__=='__main__':
    currentList = id_list
    random.shuffle(currentList)
    run(currentList)
    #run(id_list)
    print(db.movie_info.find({}))
