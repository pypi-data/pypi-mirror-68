# built-in
import typing
from inspect import signature

# external
import hypothesis
import hypothesis.strategies
import typeguard

# app
from ._decorators import Pre, Raises
from ._types import ArgsKwargsType


class TestCase(typing.NamedTuple):
    args: typing.Tuple[typing.Any, ...]
    kwargs: typing.Dict[str, typing.Any]
    func: typing.Callable
    exceptions: typing.Tuple[typing.Type[Exception], ...]

    def __call__(self) -> typing.Any:
        """Calls the given test case returning the called functions result on success or
        Raising an exception on error
        """
        try:
            result = self.func(*self.args, **self.kwargs)
        except self.exceptions:
            return typing.NoReturn  # type: ignore
        self._check_result(result)
        return result

    def _check_result(self, result: typing.Any) -> None:
        hints = typing.get_type_hints(self.func)
        if 'return' not in hints:
            return
        typeguard.check_type(
            argname='return',
            value=result,
            expected_type=hints['return'],
        )


def get_excs(func: typing.Callable) -> typing.Iterator[typing.Type[Exception]]:
    while True:
        if getattr(func, '__closure__', None):
            for cell in func.__closure__:       # type: ignore
                obj = cell.cell_contents
                if isinstance(obj, Raises):
                    yield from obj.exceptions
                elif isinstance(obj, Pre):
                    if isinstance(obj.exception, Exception):
                        yield type(obj.exception)
                    else:
                        yield obj.exception

        if not hasattr(func, '__wrapped__'):    # type: ignore
            return
        func = func.__wrapped__                 # type: ignore


def get_examples(func: typing.Callable, kwargs: typing.Dict[str, typing.Any],
                 count: int) -> typing.List[ArgsKwargsType]:
    kwargs = kwargs.copy()
    for name, value in kwargs.items():
        if isinstance(value, hypothesis.strategies.SearchStrategy):
            continue
        kwargs[name] = hypothesis.strategies.just(value)

    def pass_along_variables(*args, **kwargs) -> ArgsKwargsType:
        return args, kwargs

    pass_along_variables.__signature__ = signature(func)    # type: ignore
    pass_along_variables.__annotations__ = getattr(func, '__annotations__', {})
    strategy = hypothesis.strategies.builds(pass_along_variables, **kwargs)
    examples = []

    @hypothesis.given(strategy)
    @hypothesis.settings(
        database=None,
        max_examples=count,
        deadline=None,
        verbosity=hypothesis.Verbosity.quiet,
        phases=(hypothesis.Phase.generate,),
        suppress_health_check=hypothesis.HealthCheck.all(),
    )
    def example_generator(ex: ArgsKwargsType) -> None:
        examples.append(ex)

    example_generator()  # pylint: disable=no-value-for-parameter
    return examples


def cases(func: typing.Callable, *, count: int = 50,
          kwargs: typing.Dict[str, typing.Any] = None,
          ) -> typing.Iterator[TestCase]:
    if not kwargs:
        kwargs = {}
    params_generator = get_examples(
        func=func,
        count=count,
        kwargs=kwargs,
    )
    for args, kwargs in params_generator:
        yield TestCase(
            args=args,
            kwargs=kwargs,
            func=func,
            exceptions=tuple(get_excs(func)),
        )
