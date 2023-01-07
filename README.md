# Python Snippets

This repository includes several fun experimental Python snippets.

Here is a full list:

- `01-thread-safe-cache` - Compares a thread-safe and thread-unsafe implementation of an in-memory cache.
- `02-thread-vs-process` - Compares multithreading and multiprocessing shared memory.
- `03-daemon-no-daemon` - Compares daemon tasks and non-daemon tasks.
- `04-in-memory-event-thread-queue` - A producer-consumer pattern queue with an event to stop both producer and consumer.
## Development

`Python>=3.10`


```sh
# Installing development dependencies
python -m venv venv 
. venv/bin/activate
pip install -r dev_requirements.txt
```

