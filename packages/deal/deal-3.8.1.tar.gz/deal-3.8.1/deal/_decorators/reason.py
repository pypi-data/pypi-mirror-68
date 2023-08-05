# built-in
from typing import Callable, TypeVar

# app
from .._exceptions import ReasonContractError
from .._types import ExceptionType
from .base import Base


_CallableType = TypeVar('_CallableType', bound=Callable)


class Reason(Base[_CallableType]):
    exception: ExceptionType = ReasonContractError

    def __init__(self, event: Exception, validator: Callable, *,
                 message: str = None, exception: ExceptionType = None, debug: bool = False):
        """
        Step 1. Set allowed exceptions list.
        """
        self.event = event
        super().__init__(
            validator=validator,
            message=message,
            exception=exception,
            debug=debug,
        )

    def patched_function(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        try:
            return self.function(*args, **kwargs)
        except self.event as origin:
            try:
                self.validate(*args, **kwargs)
            except self.exception:
                raise self.exception from origin
            raise

    async def async_patched_function(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        try:
            return await self.function(*args, **kwargs)
        except self.event as origin:
            try:
                self.validate(*args, **kwargs)
            except self.exception:
                raise self.exception from origin
            raise

    def patched_generator(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        try:
            yield from self.function(*args, **kwargs)
        except self.event as origin:
            try:
                self.validate(*args, **kwargs)
            except self.exception:
                raise self.exception from origin
            raise
