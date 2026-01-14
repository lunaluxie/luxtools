from collections.abc import Callable, Iterable, Iterator
from itertools import tee
from typing import TypeVar

from .basics import first, fnot
from .compose import chain as fchain

T = TypeVar("T")


def recursive_tee(iterable, n=2):
    """
    A deep, recursive version of itertools.tee.

    It splits 'iterable' into 'n' independent iterators.
    Crucially, if it encounters an item that is itself an Iterator,
    it recursively 'tees' that item into 'n' independent copies
    before yielding it.
    """
    # 1. We must work with an iterator to use tee
    it = iter(iterable)

    # 2. Define a generator that processes items as they pass through.
    #    This is the "Lazy Mapper" that handles the splitting logic.
    def splitter():
        for item in it:
            if isinstance(item, Iterator):
                # RECURSION: The item is an iterator, so we must split it
                # into n copies (one for each branch we are creating)
                yield recursive_tee(item, n)
            else:
                # BASE CASE: The item is simple (int, string, etc).
                # Just return n references to the same object.
                yield (item,) * n

    # 3. Create a master stream that yields tuples of split items:
    #    e.g. ( (item1_copyA, item1_copyB), (item2_copyA, item2_copyB), ... )
    #    We tee this master stream so every output branch can access the tuples.
    streams_of_tuples = tee(splitter(), n)

    # 4. Unzip: Create n generators.
    #    The i-th generator picks the i-th element from the stream of tuples.
    return tuple((t[i] for t in stream) for i, stream in enumerate(streams_of_tuples))


def dropwhile_safe(predicate, iterable):
    """
    A safe, deep-aware implementation of dropwhile.
    """
    # We iterate over the main sequence
    outer_iter = iter(iterable)

    for item in outer_iter:
        # 1. RECURSIVE SPLIT:
        #    Use recursive_tee instead of standard tee.
        #    If 'item' is a nested iterator tree, both copies are fully independent.
        check_copy, keep_copy = recursive_tee(item, 2)

        # 2. CHECK:
        #    Predicate can consume 'check_copy' arbitrarily (even deeply).
        if predicate(check_copy):
            continue  # Drop and move to next

        # 3. YIELD & RESUME:
        #    Yield the pristine 'keep_copy' and the rest of the outer stream.
        yield keep_copy
        yield from outer_iter
        return


def takefirst(predicate: Callable[[T], bool], items: Iterable[T]):
    return first(iter(dropwhile_safe(fchain([fnot, predicate]), iter(items))))
