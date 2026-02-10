import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "sovilo")

client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(
    MONGODB_URI
)

db = client[MONGODB_DB]


def get_collection(name: str):
    return db[name]
