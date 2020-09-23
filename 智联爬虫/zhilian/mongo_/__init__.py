from pymongo import MongoClient

_client = MongoClient('121.36.74.141', 27017)
db = _client.mydb  # 打开或创建mydb库
