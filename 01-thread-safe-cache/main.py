import threading
import time

INITIAL_TOTAL = 100000000

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class InMemoryCache(metaclass=SingletonMeta):

    def __init__(self, total: int = INITIAL_TOTAL) -> None:
        self.total = total

    def reset(self, total: int = INITIAL_TOTAL):
        self.total = total

    def update_total(self, value: int, with_lock=False) -> None:

        def _updated_unsafe():
            # this is not atomic since we carry out 3 operations:
            # 1. read self.total initial value
            # 2. calculate new value for self.total
            # 3. store new self.total
            # So if thread 1 finished step 1. and then there is a context switch
            # to thread 2 that carries out all steps 1-3, then when we switch back to 1, 
            # the operation carried by thread 2 would not be included in thread 1's value
            # thus causing a lost of information in shared memory - a race condition.`
            # Note: the time.sleep(0) are forcing the context switch

            # step 1 - read current total
            temp = self.total
            time.sleep(0)
            # step 2 - calculate new total
            temp = temp + value
            time.sleep(0)
            # step 3 - store new total
            self.total = temp
        
        if not with_lock:
            _updated_unsafe()
        else:
            with ThreadSafeLock():
                _updated_unsafe()


CACHE = InMemoryCache()


class ThreadSafeLock(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.lock = threading.Lock()


    def __enter__(self):
        self.lock.acquire()

    def  __exit__(self, *args, **kwargs):
        self.lock.release()


def runner(value: int, repeats: int, with_lock: bool):
    print(f"Thread {threading.get_ident()} will update total with value {value} {repeats} times.")
    for _ in range(repeats):

        InMemoryCache().update_total(value, with_lock=with_lock)


def multi_thread_runner(runs: int, with_lock: bool):
    
    CACHE.reset()
    
    # repeating sevaral times to force race condition
    for i in range(runs):
        print(f"Run #{i} - initial total {CACHE.total}")
        substracter_thread = threading.Thread(target=runner, args=(-5, 1000000), kwargs={"with_lock": with_lock})
        adder_thread = threading.Thread(target=runner, args=(5, 1000000), kwargs={"with_lock": with_lock})
        substracter_thread.start()
        adder_thread.start()
        substracter_thread.join()
        adder_thread.join()

        print(f"Run #{i} - final total {CACHE.total}")
        if CACHE.total != INITIAL_TOTAL:
            print(colored(255, 0, 0, "RACE CONDITION FOUND!"))
            break


def main():

    print("Running thread-unsafe")
    multi_thread_runner(runs=3, with_lock=False)

    print("Running thread-safe")
    multi_thread_runner(runs=3, with_lock=True)

if __name__ == "__main__":
    main()