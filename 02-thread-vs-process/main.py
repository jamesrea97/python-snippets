"""Module contains an example of the distinction between thread/multiprocessing in Python."""
import multiprocessing
import threading
from enum import Enum
import logging
from time import sleep

PROCESS_NOT_SHARED_MEMORY = [0]
THREAD_SHARED_MEMORY = [0]

thread_lock = threading.Lock()
process_lock = multiprocessing.Lock()


class ConcurrencyType(Enum):
    PROCESS = "PROCES"
    THREAD = "THREAD"


def increase(concurrency_type: ConcurrencyType) -> None:
    """Increases corresponding shared memory"""
    sleep(1)
    if concurrency_type == ConcurrencyType.PROCESS:
        with process_lock:
            PROCESS_NOT_SHARED_MEMORY[0] += 1
            logging.info(
                f"Current status of Process (not) shared memory: {PROCESS_NOT_SHARED_MEMORY}")
    elif concurrency_type == ConcurrencyType.THREAD:
        with thread_lock:
            THREAD_SHARED_MEMORY[0] += 1
            logging.info(f"Current status of Thread shared memory: {THREAD_SHARED_MEMORY}")


def processes():
    """Relies on processes to change PROCESS_SHARED_MEMORY"""

    processess_list = []

    for i in range(2):
        logging.debug(f"Creating process {i}.")
        processess_list.append(multiprocessing.Process(target=increase,
                                                       args=((ConcurrencyType.PROCESS,))))

    for process in processess_list:
        process.start()

    for process in processess_list:
        process.join()


def threads():
    """Relies on threads to change THREAD_SHARED_MEMORY"""

    threads_list = []
    for i in range(2):
        logging.debug(f"Creating thread {i}.")
        threads_list.append(threading.Thread(target=increase, args=((ConcurrencyType.THREAD,))))

    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()


def main():
    """Main driver for this example."""

    logging.basicConfig(level=logging.DEBUG)

    logging.info("Running with multiprocessing.")
    processes()
    logging.info("Finished running with multiprocessing.\n")

    sleep(2)

    logging.info("Running with multithreading.")
    threads()
    logging.info("Finished running with multithreading.\n")

    print("Notice in multiprocessing, memory (array) is not shared betwee processes.\n"
          "Notice in multithreading, memory (array is shared between threads.\n"
          "Note that this is the case even when a lock is applied (i.e. no race condition)."
          "This shows the key difference between multiprocessing and multithreading.")


if __name__ == "__main__":
    main()