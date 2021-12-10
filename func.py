from typing import TypeVar, Callable, Iterable, Protocol, Any

T = TypeVar("T")
T1 = TypeVar("T1")


class Pipe(Protocol[T]):

    def __ror__(self, other: Any) -> T:
        ...


# general
not_None = lambda e: e is not None
is_None = lambda e: e is None

# helper index methods
fst: Callable[[Iterable[T]], T]
fst = lambda t: t[0]
snd: Callable[[Iterable[T]], T]
snd = lambda t: t[1]
lst: Callable[[Iterable[T]], T]
lst = lambda t: t[-1]

# str helpers
strip: Callable[[str], str]
strip = lambda s: s.strip()

# list helpers
flatten: Callable[[list[list[T]], ], list[T]]
flatten = lambda list_: [item for sublist in list_ for item in sublist]

# pipes
# >>> 10 | prange | pfilter(lambda a: a > 5) | pmap(lambda x: x*2) | plist | pout
pipe: Callable[[Callable[[Any], T]], Pipe[T]]
pipe = lambda f: type("pipe", (), {"__ror__": lambda _, other: f(other)})()

pfilter: Callable[[Callable[[T], bool]], Callable[[Iterable[T]], Iterable[T]]]
pfilter = lambda f: pipe(lambda l: filter(f, l))

pmap: Callable[[Callable[[Iterable[T]], Iterable[T1]]], Callable[[Iterable[T]], Iterable[T1]]]
pmap = lambda f: pipe(lambda l: map(f, l))

pout: Callable[[Any], None]
pout = pipe(print)

plist: Callable[[Iterable[T]], list[T]]
plist = pipe(list)

prange: Callable[[int], range]
prange = pipe(range)

pflatten: Callable[[Iterable[Iterable[T]]], Iterable[T]]
pflatten = pipe(flatten)


class infix:

    def __init__(self, func):
        self.func = func

    def __mod__(self, other):
        print(f'{other=}')
        return self.func(other)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


if __name__ == '__main__':
    print = infix(print)

    print % (infix(lambda x: x * 2) % 10)

    print % "test", "Test1"

    print("Test", end="/n...")
