"""Module contains an Event & Queues multi-threading example through Producer/Consumer."""
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import logging
import time
import random
from threading import Event


def producer(queue: Queue, event: Event):
    """Example of a producer - receives requests and publishes them to the queue."""
    while not event.is_set():
        message = random.randint(1, 101)

        logging.info(f"Publishing message: {message} - Queue size: {queue.qsize()}.")
        queue.put(message)
        logging.info(f"Published message {message} - Queue size: {queue.qsize()}.")

    logging.info("No more messages to produce.")


def consumer(queue: Queue, event: Event) -> None:
    """Example of a consumer - reads messages from the queue (published by producer). """
    while not (event.is_set() and queue.empty()):
        message = queue.get()
        logging.info(f"Consumed message:{message} - Queue size: {queue.qsize()}.")

    logging.info("No more messages to be consume.")


def main():
    logging.basicConfig(level=logging.DEBUG)

    pipeline = Queue(maxsize=3)
    event = Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        logging.info("Starting to send messages to producer.")

        executor.submit(producer, pipeline, event)  # listens on changes of state of event
        executor.submit(consumer, pipeline, event)  # listens on changes of state of event

        time.sleep(1)
        event.set()
        logging.info("Stopping to send messages to producer.")


    HELPER = """
    This is a basic in-memory thread-safe queue.\n
    queue.Queue in Python blocks on queue.Queue.get, 
    meaning it waits until a message has been added to the queue.\n
    In this example, the ThreadPoolExecutor starts both the producer and consumer. 
    
    Producer: Keeps producing messages to queue until threading.Event is set. 
    This event is affectively the end of the production of messages.\n

    Consumer: Keeps reading messages, blocking when the queue is empty.
    It stops reading messages when no more are produced (Event) and the queue is empty
    
    """
    logging.info("This is a basic in-memory thread-safe queue.")
if __name__ == "__main__":
    main()