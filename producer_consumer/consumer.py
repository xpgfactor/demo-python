"""Consumer.

Consumes the data from the queue one by one
"""

import asyncio
from time import perf_counter


async def consume(data_queue: asyncio.Queue):
    """
    Consumes the data from the queue one by one
    :param data_queue: a queue with the data to be processed
    :return:
    """
    while True:
        # Get data from the queue
        data = await data_queue.get()

        item_id = data["id"]

        start = perf_counter()
        await asyncio.sleep(item_id % 5)
        end = perf_counter()
        print(f"Item #{item_id:<3} took {(end - start):.0f} seconds.")

        # Indicate that a formerly enqueued task is complete
        data_queue.task_done()
