from pymongo import MongoClient
def get_database():
    """Simple function to connect to MongoDB"""
    client = MongoClient("mongodb://localhost:27017/")
    return client['study_buddy']