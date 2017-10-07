#coding:UTF-8 
import urllib
import urllib.request
import time
import threading
import random
import re
import socket

defaulttimeout = 10
socket.setdefaulttimeout(defaulttimeout)
ips = []
lastTime = None

class ProxyPool:
    def __init__(self):
        self.ips = []
        self.count = dict()
        self.resume();
        self.updatePool()
        print("Proxy Pool init!")

    def resume(self):
        with open('ips.txt','r') as f:
            txt = f.read()
        self.ips.extend(list(map(lambda w : w.strip(),txt.strip().split("\n"))))
        for w in self.ips:
            self.count[w] = 0

    def store(self):
        with open('ips.txt','w') as f:
            f.write("\n".join(self.ips))

    def updatePool(self):
        if len(self.ips)<20:
            socket.setdefaulttimeout(30)
            print("Refill Pool!")
            #url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=49b322eca329472c8f2becbf60001f11&orderno=MF20171060571UXYXmM&returnType=1&count=20'
            url = 'http://http-webapi.zhimaruanjian.com/getip?num=50&type=1&pro=&city=0&yys=0&port=11&pack=3386&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1'
            while True:
                try:
                    txt = urllib.request.urlopen(url).read().decode('utf-8')
                except urllib.error.URLError:
                    print('Little Sleep')
                    time.sleep(15)
                    continue
                break
            print(txt)
            self.ips.extend(list(map(lambda w : w.strip(),txt.strip().split("\n"))))
            self.store()
            with open('ips_all.txt','a') as f:
                f.write('\n' + '\n'.join(list(map(lambda w : w.strip(),txt.strip().split("\n")))))
            for w in self.ips:
                self.count[w] = 0
            socket.setdefaulttimeout(defaulttimeout)

    def getProxyIp(self):
        self.updatePool()
        return random.choice(self.ips)

            
    def getHtmlViaProxy(self,url):
        totalTries = 5
        while totalTries:
            totalTries -= 1
            proxyIp = self.getProxyIp()
            print('>>> [%d]Using Proxy Ip : '%len(self.ips),proxyIp)
            #这是代理IP
            proxy = {'http':proxyIp}
            #创建ProxyHandler
            proxy_support = urllib.request.ProxyHandler(proxy)
            #创建Opener
            opener = urllib.request.build_opener(proxy_support)
            #添加User Angent
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
            #安装Opener
            urllib.request.install_opener(opener)
            html = ""
            #使用自己安装好的Opener
            #读取相应信息并解码
            def errorDealer():
                self.count[proxyIp] += 1
                if self.count[proxyIp] >=5:
                    print("Bad Ip",proxyIp)
                    self.ips.remove(proxyIp)
                    self.store()
                html = ""
            def normalDealer():
                self.count[proxyIp] = 0
            try:
                response = urllib.request.urlopen(url)
                html = response.read().decode("utf-8")
                normalDealer()
            except urllib.error.URLError:
                errorDealer()
            except ConnectionResetError:
                errorDealer()
            except socket.timeout:
                errorDealer()
            #打印信息
            if html != "":
                return html
            else:
                print("Unsecessfull connection")
        return ""

if __name__ == '__main__':
    P = ProxyPool()
    for i in range(0,100000):
        url = 'http://www.whatismyip.com.tw/'
        html = P.getHtmlViaProxy(url)
        print(html)
        time.sleep(.1)
        print("OK")
