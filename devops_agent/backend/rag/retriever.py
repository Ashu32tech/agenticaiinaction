
from backend.rag.quadrant_db import QuadrantDB

db = QuadrantDB()
db.build()

def retrieve_context(query):
    return db.search(query)
