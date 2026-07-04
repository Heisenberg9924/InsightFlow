from app.database.connection import MongoConnection


db = MongoConnection.get_database()

documents = db["documents"]

knowledge_units = db["knowledge_units"]

conversations = db["conversations"]

messages = db["messages"]

users = db["users"]