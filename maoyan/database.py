from pymongo import MongoClient
MongoConnection = MongoClient('mhy12345.xyz', 27017)
db = MongoConnection.movie_db
