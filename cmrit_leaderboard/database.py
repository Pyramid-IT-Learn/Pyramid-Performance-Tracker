# cmrit_leaderboard/database.py

from pymongo import MongoClient
from cmrit_leaderboard.config import MONGODB_URI, DB_NAME, USERS_COLLECTION

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.users_collection = self.db[USERS_COLLECTION]

    def upsert_user(self, hall_ticket_no, data):
        self.users_collection.update_one(
            {'hallTicketNo': hall_ticket_no},
            {'$set': data},
            upsert=True
        )

    def get_users_with_usernames(self, platform):
        return self.users_collection.find({
            f'{platform}Username': {'$exists': True, '$ne': None}
        })
    
    def get_all_users(self):
        return self.users_collection.find({})
