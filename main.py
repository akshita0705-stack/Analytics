from fastapi import FastAPI
from pydantic import BaseModel
import redis
import sqlite3
from typing import Optional

app = FastAPI()

# ----------------------------
# 1. Connect to Redis Cloud
# ----------------------------
redis_url = "redis://default:i28JPAkrXJIhdnj8C3tVLNp8Y6LBwHq1@redis-18218.c305.ap-south-1-1.ec2.cloud.redislabs.com:18218"
r = redis.from_url(redis_url, decode_responses=True)

# ----------------------------
# 2. Home Endpoint
# ----------------------------
@app.get("/")
def home():
    return {"message": "Ingestion API is running!"}

# ----------------------------
# 3. Event Model (Schema)
# ----------------------------
class Event(BaseModel):
    event_name: str
    user_id: int
    metadata: Optional[dict] = None

# ----------------------------
# 4. Ingestion Endpoint
# ----------------------------
@app.post("/ingest")
def ingest_event(event: Event):
    event_data = event.dict()

    # Debug print for terminal
    print("Received event:", event_data)

    # push the data into Redis Queue
    r.lpush("events_queue", str(event_data))

    return {"status": "received", "data": event_data}


# ----------------------------
# 5. Reporting Endpoint: Get All Events
# ----------------------------
@app.get("/events")
def get_events():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, event_name, user_id, metadata, created_at FROM events")
    rows = cursor.fetchall()

    conn.close()

    # Convert DB rows → list of dicts
    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "event_name": row[1],
            "user_id": row[2],
            "metadata": row[3],
            "created_at": row[4]
        })

    return {"total": len(events), "events": events}
