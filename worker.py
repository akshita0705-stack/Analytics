import time
import redis
import ast
import sqlite3

redis_url = "redis://default:i28JPAkrXJIhdnj8C3tVLNp8Y6LBwHq1@redis-18218.c305.ap-south-1-1.ec2.cloud.redislabs.com:18218"
r = redis.from_url(redis_url, decode_responses=True)

conn = sqlite3.connect("events.db")
cursor = conn.cursor()

print("Worker started and listening for events...")

while True:
    event_data = r.rpop("events_queue")

    if event_data:
        event_dict = ast.literal_eval(event_data)

        print("Processing event:", event_dict)

        # Insert data into database
        
        cursor.execute(
            "INSERT INTO events (event_name, user_id, metadata) VALUES (?, ?, ?)",
            (
                event_dict["event_name"],
                event_dict["user_id"],
                str(event_dict["metadata"])
            )
        )

        conn.commit()

    else:
        time.sleep(1)

