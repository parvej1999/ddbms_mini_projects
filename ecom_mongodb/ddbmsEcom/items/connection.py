from pymongo import MongoClient

url = "mongodb://localhost:27017"
client = MongoClient(url)

db = client.items  
"""Or we can use client["items"] if database name is attribute 
    accessible db-items"""


