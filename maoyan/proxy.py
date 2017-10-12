import requests
import bs4
import re
import json
import random
import urllib
import socket
import datetime
import time


def init():
    global ips
    global cfg
    ips = []
    with open('configures.json','r') as f:
        cfg = json.load(f)

default_proxy = '111.155.124.84:8123'

def update_ips():
    print("Read Ip Table...")
    for page in range(1,11):
        url="http://www.xicidaili.com/nn/%d"%page
        print(page,"out of",10,'in',url)
        def undirect(url):
            html = getHtmlViaProxy(url,default_proxy)
            if re.search('国内高匿代理',html):
                return html
            while True:
                print("请输入一个HTTP代理：")
                proxyIp = input()
                html = getHtmlViaProxy(url,proxyIp)
                if re.search('国内高匿代理',html):
                    return html
                print("Retrie...")
        def direct(url):
            headers = cfg['xiciheader']
            r = requests.get(url,headers=headers)
            if r.text=="block":
                print("blocked")
                return undirect(url)
            return r.text

        html = direct(url)
        soup =bs4.BeautifulSoup(html,'html.parser')  
        data=soup.table.find_all("td")  
        ip_compile=re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  
        port_compile=re.compile(r"<td>(\d+)</td>")  
        ip=re.findall(ip_compile,str(data))  
        port=re.findall(port_compile,str(data))  
        global ips
        ips.extend([":".join(i) for i in zip(ip,port)])
        time.sleep(1)
    with open('data/xici_ip.txt','w') as f:
        f.write(get_ips_as_string())

def load_ips():
    global ips
    with open('data/xici_ip.txt','r') as f:
        ips = f.read().split('\n')
def get_ips_as_string():
    global ips
    return "\n".join(ips)

def getHtmlViaProxy(url,rawProxyIp=None):
    global ips
    print("代理池大小：",len(ips))
    if rawProxyIp:
        proxyIp = rawProxyIp
    else:
        proxyIp = random.choice(ips)
    print('>>> proxy_update : [%d]Using Proxy Ip : '%len(ips),proxyIp , 'URL = ',url)
    proxies = {
            'http':proxyIp
            }
    'User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Referer":"",
            "User-Agent":cfg['agents'][0],
            }
    html = ""
    res = requests.get(url,headers=headers,proxies=proxies)
    if (int(res.status_code) == 200):
        print(datetime.datetime.now().strftime('%H:%M:%S')+':当前状态是'+str(res.status_code))
    else:
        print(datetime.datetime.now().strftime('%H:%M:%S')+'访问错误')
        ips.remove(proxyIp)
    html = res.text
    return html


init()
update_ips()
#load_ips()

if __name__ == '__main__':
    html = getHtmlViaProxy('https://www.douban.com')
    print(html)
