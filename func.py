from typing import TypeVar, Callable, Iterable, Protocol, Any, NewType, Union, Generic

T = TypeVar("T")
T1 = TypeVar("T1")
Number = NewType("Number", Union[int, float])
Matrix = NewType("Matrix", list[list[Number]])
foo = ...
bar = ...


class Pipe(Protocol[T]):

    def __ror__(self, other: Any) -> T:
        ...


class Infix(Protocol[T]):

    def __mod__(self, other: Any) -> T:
        ...

    def __call__(self, *args, **kwargs) -> T:
        ...


# general
not_None = lambda e: e is not None
is_None = lambda e: e is None
inc = lambda i: i + 1
decr = lambda i: i - 1
eq_n = lambda i: lambda e: e == i
gt_n = lambda i: lambda e: e > i
lt_n = lambda i: lambda e: e < i

# make a lambda expression recursive
rec = lambda f, *a: f(f, *a)

# foldr :)
foldr: Callable[[Callable[[T, T1], T1], T1, Iterable[T]], T1]
foldr = lambda f, d, l: rec(lambda self, l_: d if not l_ else f(l_[0], self(self, l_[1:])), l)

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

# retuns the position of the first element to match the condition
index: Callable[[Iterable[T], Callable[[T], bool]], int]
index = lambda l, cond: rec(lambda self, i: -1 if i == len(l) else (i if cond(l[i]) else self(self, i + 1)), 0)

# pipes
# >>> 10 | prange | pfilter(lambda a: a > 5) | pmap(lambda x: x*2) | plist | pout
pipe: Callable[[Callable[[Any], T]], Pipe[T]]
pipe = lambda f: type("pipe", (), {"__ror__": lambda _, other: f(other), "__call__": lambda _, *a, **kw: f(*a, **kw)})()

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

# infix notation
infix: Callable[[Callable[[Any], T]], Pipe[T]]
infix = lambda f: type("infix", (),
                       {"__mod__": lambda _, other: f(other), "__call__": lambda _, *a, **kw: f(*a, **kw)})()

# matrix helpers
position = lambda m, x, y: m[y][x]

# returns the coordinates of all neighbors (diagonal included
neighbors = lambda m, x, y: filter(not_None,
                                   ((x_, y_) if 0 <= x_ < len(m[0]) and 0 <= y_ < len(m) and (x_, y_) != (
                                       x, y) else None
                                    for x_ in (x - 1, x, x + 1)
                                    for y_ in (y - 1, y, y + 1)))

# same as index but for two dimensions, returns the x and y position
indexm: Callable[[Matrix, Callable[[Number], bool]], tuple[int, int]]
indexm = lambda m, cond: rec(lambda self, y: (-1, -1) if y == len(m[0]) \
    else (x, y) if (x := index(m[y], cond)) != -1 else self(self, y + 1), 0)


def print_matrix(matrix: list[list[Any]]) -> None:
    max_len = max(len(str(elem)) for row in matrix for elem in row)
    for row in matrix:
        print(" ".join(str(elem).rjust(max_len) for elem in row))


class Monad:
    def __init__(self, expr):
        self.expr = expr

    @classmethod
    def unit(cls, expr):
        return Monad(expr)

    def __irshift__(self, other):
        print(other)


class Maybe(Generic[T]):
    def __init__(self, val):
        self.val = val

    def __and__(self, other):
        return None if self.val is None else other


Just = lambda maybe: maybe.val

div = lambda x, y: None if y == 0 else x / y

if __name__ == '__main__':
    do = lambda *args: lst(args)
    res = do(
        x := 1,
        y := 2 + x,
        _ := 3 + y
    )
    print(res)  # -> 6

    res = (Maybe(x := 10) &
           Maybe(y := x * 2) &
           Maybe(z := y - 20) &
           Maybe(err := div(1, 0)) &
           Maybe(z + 42))

    print(res)
