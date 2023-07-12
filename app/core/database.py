import urllib.parse
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_database_connection():
    username = "Cluster57997"
    password = "icecoldsnow"
    encoded_username = urllib.parse.quote_plus(username)
    encoded_password = urllib.parse.quote_plus(password)
    uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster57997.ywxeydt.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client
