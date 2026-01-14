from collections.abc import Iterable
from typing import Iterator, TypeVar

from more_itertools import peekable

from .currying import overload

T = TypeVar("T")


def identity(x: T) -> T:
    return x


def fnot(x: bool):
    return not x


def first(items: Iterable[T]):
    return items.__iter__().__next__()


def first_safe(items: Iterable[T]):
    try:
        return items.__iter__().__next__()
    except StopIteration:
        return None


head = first


@overload()
def isempty(items: Iterator):
    it = peekable(items)
    try:
        it.peek()
        return False
    except StopIteration:
        return True


@overload()
def isempty(items: Iterable):
    it = peekable(items)
    try:
        it.peek()
        return False
    except StopIteration:
        return True
