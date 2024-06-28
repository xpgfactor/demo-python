"""Producer.

Puts all the data into a queue.
The queue has a limited size,
so the Producer waits if there is no space yet.
"""

import asyncio
from typing import List


async def produce(data: List[dict], data_queue: asyncio.Queue, producer_done_event: asyncio.Event):
    """
    Puts all the data into the given queue
    :param data: the data to be processed (list of dictionaries with 'ID' of items)
    :param data_queue: a queue with the data to be processed
    :param producer_done_event: event to be set when the Producer is done
    :return:
    """
    for item in data:
        await data_queue.put(item)

    # Mark the event as done
    producer_done_event.set()
