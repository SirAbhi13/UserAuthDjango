import os

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

url = os.getenv("DB_STRING")

db_name = os.getenv("DB_NAME")
client = MongoClient(url)

db = client[db_name]
