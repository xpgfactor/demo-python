"""Master

Pushes messages into a Redis Queue
"""

import os
from datetime import datetime, timezone
from json import dumps
from time import sleep

import redis


def get_connection():
    """
    returns a connection to Redis
    """
    db = redis.Redis(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        db=os.environ.get("REDIS_DB"),
        password=os.environ.get("REDIS_PASSWORD"),
        decode_responses=True,
    )
    return db


def push_item(db, message):
    """
    send a message to the queue
    """
    db.lpush(os.environ.get("QUEUE_PRIMARY"), message)


def main(num_messages: int, delay: float = 1):
    """
    pushes messages into a Redis Queue
    """
    # get Redis connection
    db = get_connection()

    for i in range(1, num_messages + 1):
        # Create message data
        message = {
            "id": i,
            "scheduled_at": datetime.now(timezone.utc).isoformat(),
            "data": {
                "number": i,
            },
        }

        # the data is stored as JSON
        message_json = dumps(message)

        # Push message to a Redis queue
        print(f"Sending message #{i}")
        push_item(db, message_json)

        # wait a bit, so see the process
        sleep(delay)


if __name__ == "__main__":
    main(1_000, 1)
