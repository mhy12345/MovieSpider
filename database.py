from pymongo import MongoClient
MongoConnection = MongoClient('mhy12345.xyz', 27017)
db = MongoConnection.movie_db#连接mydb数据库，没有则自动创建
movie_list = db.movie_list#使用test_set集合，没有则自动创建
