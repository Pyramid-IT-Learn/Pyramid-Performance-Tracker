# cmrit_leaderboard/database.py

import pandas as pd

from pymongo import MongoClient
from cmrit_leaderboard.config import MONGODB_URI, DB_NAME, USERS_COLLECTION

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.users_collection = self.db[USERS_COLLECTION]
        self.users_collection.create_index(
            [('hallTicketNo', 1)], unique=True
        )

    def upsert_user(self, hall_ticket_no, data):
        self.users_collection.update_one(
            {'hallTicketNo': hall_ticket_no},
            {'$set': data},
            upsert=True
        )

    def get_existing_users_for_platform(self, platform):
        # Find users with {paltform}Username field and {paltform}Status True
        return self.users_collection.find({f'{platform}Username': {'$exists': True, '$ne': None}, f'{platform}Status': True})

    def get_all_users(self):
        return self.users_collection.find({})
    
    def upload_to_db_with_df(self, users: pd.DataFrame) -> None:
        for index, row in users.iterrows():
            data = row.to_dict()
            data.pop('hallTicketNo', None)
            self.upsert_user(row['hallTicketNo'], data)

