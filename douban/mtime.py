#-*- coding:utf-8 -*-
import urllib.request
import urllib
import time
import json
#from pymongo import MongoClient
#from movie_list import title_list

if __name__ == '__main__':
    url = 'http://search.mtime.com/search/'
    name = '古墓丽影'
    query = {'q':name,'t':0}
    #s = ".".join(title_list)
    #print(s[s.find(name):])
