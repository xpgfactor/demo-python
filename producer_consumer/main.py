"""An entry point.

Defines a controller function
and runs it asynchronously.

The controller
1. initializes Producer and Consumers
2. waits for the results
3. performs finalizing

"""

import asyncio
from time import perf_counter
from typing import List

import consumer
import producer

NUM_TASKS = 100
DATA_QUEUE_MAX = 200


async def _controller(data: List[dict]) -> None:
    """
    The main controller
    1. initializes Producer and Consumers
    2. waits for the results
    3. performs finalizing
    :param data: the data to be processed (list of dictionaries with 'ID' of items)
    :return:
    """
    # Create a data queue
    data_queue = asyncio.Queue(maxsize=DATA_QUEUE_MAX)

    tasks = []

    # 'Producer done' event to check when the Producer is done
    producer_done_event = asyncio.Event()
    producer_done_event.clear()  # unset the event at the beginning
    # A new Task to put all the data into a Queue for processing
    tasks.append(asyncio.create_task(producer.produce(data, data_queue, producer_done_event)))

    # Create Tasks to consume (process) the data
    for _ in range(NUM_TASKS):
        tasks.append(asyncio.create_task(consumer.consume(data_queue)))

    # Waiting for a Producer to complete
    await producer_done_event.wait()  # blocks until the event flag is set to true
    # Waiting for all the tasks in the queue to complete
    await data_queue.join()

    # all processing is done
    # we can cancel all tasks
    for task in tasks:
        task.cancel()


def main() -> None:
    """
    Entry point.
    Pass the data to the main controller
    and runs it asynchronously.
    Performs a basic logging.
    :return:
    """
    print(f"Start processing data.")

    data = [{"id": i} for i in range(1_000)]

    start = perf_counter()
    asyncio.run(_controller(data))
    end = perf_counter()

    print("-" * 10)
    # sum of all I/O wait times simulated using asyncio.sleep
    total = sum(item["id"] % 5 for item in data)
    print(f"Total waiting time: {total:>6} seconds.")
    print(f"All items completed in: {(end - start):.0f} seconds.")


if __name__ == "__main__":
    main()
