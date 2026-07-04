import os

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if MONGODB_URI is None:
    raise ValueError("MONGODB_URI is not set.")

if DATABASE_NAME is None:
    raise ValueError("DATABASE_NAME is not set.")