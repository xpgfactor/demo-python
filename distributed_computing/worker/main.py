"""Worker

Processes messages coming from the Redis Queue
"""

import os
import random
from json import loads

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


def redis_queue_push(db, message):
    """
    send a message to the queue
    """
    db.lpush(os.environ.get("QUEUE_PRIMARY"), message)


def get_next_item(db):
    """
    'blmove' is used to implement a 'reliable queue' pattern
    to ensure the safety of messages if a worker crashes.
    The message is retrieved from a primary queue and is stored in a temporary one
    for the processing time.
    """
    message_json = db.blmove(
        os.environ.get("QUEUE_PRIMARY"),
        os.environ.get("QUEUE_PROCESSING"),
        src="RIGHT",
        dest="LEFT",
        timeout=5,
    )
    return message_json


def process_message(db, message_json: str):
    """
    the actual computation process should be here
    """
    message = loads(message_json)
    print(f"Item #{message['id']} is being processed:")

    # "False" simulates the case when the processing fails
    is_success = random.choices((True, False), weights=(6, 1), k=1)[0]
    if is_success:
        print(f"\tsuccessfully")
    else:
        print(f"\tfailed - requeueing...")
        redis_queue_push(db, message_json)


def finalize_item(db, message_json: str):
    """
    finally remove the message
    if the processing is completed
    """
    # "False" simulates the case when the Worker crashes and the message remains in a temporary queue
    is_success = random.choices((True, False), weights=(100, 1), k=1)[0]
    if is_success:
        db.lrem(os.environ.get("QUEUE_PROCESSING"), 1, message_json)


def main():
    """
    Consumes items from the Redis queue
    """
    # get Redis connection
    db = get_connection()

    while True:
        message_json = get_next_item(db)  # this blocks until an item is received
        if message_json:
            process_message(db, message_json)
            finalize_item(db, message_json)


if __name__ == "__main__":
    main()
