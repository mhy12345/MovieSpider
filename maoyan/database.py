from pymongo import MongoClient
MongoConnection = MongoClient('mhy12345.xyz', 27017)
#MongoConnection = MongoClient('127.0.0.1', 27017)
db = MongoConnection.movie_db
db.test.save({'name':'test'})
