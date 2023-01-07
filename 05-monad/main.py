"""Module contains PyMonads"""
from abc import ABC, abstractmethod
from typing import Callable, Any, Optional
from functools import partial
import logging

class AbstractMondad(ABC):

    @staticmethod
    @abstractmethod
    def wrap(*args, **kwargs) -> "AbstractMondad":
        """Abstract method to wrap input into monadic type."""

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs) -> "AbstractMondad":
        """Abstractmethod to run monadic_value with func."""

    @abstractmethod
    def get(self) -> Any:
        """Abstractmethod to get value from AbstractMonad."""

class MaybeMonad(AbstractMondad):

    def __init__(self, value: Optional[Any]) -> None:
        self.value = value

    @staticmethod
    def wrap(value: Optional[Any]) -> "MaybeMonad":
        """Wraps any value into MaybeMonad."""
        return MaybeMonad(value=value)

    @staticmethod
    def run(
        monad: "MaybeMonad", 
        func: Callable[[Any], Any],
    ) -> "MaybeMonad":
        
        if monad.value is None:
            return monad

        new_value = func(monad.value)
        
        return MaybeMonad(value=new_value)

    def get(self) -> Any:
        return self.value

        

class ErrorMonad(AbstractMondad):
    def __init__(self, res, error = None, logs = []) -> None:
        self.res = MaybeMonad.wrap(res)
        self.error = error
        self.logs = logs

    @staticmethod
    def wrap(res, error=None, logs=[]) -> "ErrorMonad":
        return ErrorMonad(
            res=res,
            error=error,
            logs=logs,
        )

    @staticmethod
    def run(
        monad: "ErrorMonad", 
        func: Callable[[Any], Any]
    ) -> "ErrorMonad":

        if monad.error is not None:
            return monad

        res, error = None, None
        logs = monad.logs

        try:
            res = func(monad.get())
            logs.append(f"Called {func}, args {monad.get()}, results {res}")
        except Exception as e:
            logs.append(f"Exception occured - reason {e}")
            error = e
        finally:
            return ErrorMonad(
                res=res,
                error=error,
                logs=logs
            )
        
    def get(self) -> Any:
        return self.res.get()

    def get_error(self) -> Exception:
        return self.error

    def get_logs(self) -> list[str]:
        return self.logs


def run_maybe_monad():
    logging.info("Running example with MaybeMonad")

    def adder(current_sum):
        logging.debug(f"Current sum {current_sum}")
        if current_sum % 2 == 0:
            return current_sum + 1
        else:
            return None

    maybe_monad = MaybeMonad(0)

    logging.debug("Running with MaybeMonad")
    for _ in range(5):
        maybe_monad = MaybeMonad.run(monad=maybe_monad, func=adder)
    

    logging.debug("Running without MaybeMonad")
    try:
        total = 0
        for _ in range(5):
            total = adder(total)
    except Exception:
        logging.debug("Running without MaybeMonad raises exception due to None value")


def run_error_monad():

    class SomeErrorException(Exception):
        pass

    logging.info("Running example with ErrorMonad")

    def run_with_error(current_sum):
        logging.debug(f"Current sum {current_sum}")
        if current_sum % 2 == 0:
            return current_sum + 1
        else:
            raise SomeErrorException("some exception")

    error_monad = ErrorMonad(0)

    logging.debug("Running with ErrorMonad")
    for _ in range(5):
        error_monad = ErrorMonad.run(monad=error_monad, func=run_with_error)
    
    logging.info("ErrorMonad - "
                 f"value:{error_monad.res.get()} "
                 f"error: {error_monad.error} "
                 f"logs: {error_monad.logs}")
    logging.debug("Running without ErrorMonad")
    try:
        total = 0
        for _ in range(5):
            total = run_with_error(total)
    except Exception:
        logging.debug("Running without ErrorMonad raises exception due to raised SomeErrorException exception")


def main():

    logging.basicConfig(level=logging.DEBUG)

    run_maybe_monad()

    run_error_monad()

if __name__ == "__main__":
    main()

