import requests
import bs4
import re
import json
import random
import urllib
import socket
import datetime


def init():
    global ips
    global cfg
    ips = []
    with open('configures.json','r') as f:
        cfg = json.load(f)


def update_ips():
    print("Read Ip Table...")
    for page in range(1,11):
        url="http://www.xicidaili.com/nn/%d"%page
        print(page,"out of",10,'in',url)
        headers = cfg['xiciheader']
        r = requests.get(url,headers=headers)
        if r.text=="block":
            print("blocked")
            exit()
        soup =bs4.BeautifulSoup(r.text,'html.parser')  
        data=soup.table.find_all("td")  
        ip_compile=re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  
        port_compile=re.compile(r"<td>(\d+)</td>")  
        ip=re.findall(ip_compile,str(data))  
        port=re.findall(port_compile,str(data))  
        global ips
        ips.extend([":".join(i) for i in zip(ip,port)])

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

if __name__ == '__main__':
    html = getHtmlViaProxy('https://www.douban.com')
    print(html)
