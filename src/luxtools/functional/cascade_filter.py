from collections.abc import Callable, Iterable
from typing import TypeVar

from .basics import fnot, isempty
from .better_builtins import takefirst
from .compose import chain as fchain

T = TypeVar("T")


class NoItemsMatchedError(ValueError):
    pass


def cascade_filter(
    filter_predicates: Iterable[Callable[[T], bool]],
    items: Iterable[T],
    cascade_predicate: Callable[[Iterable[T]], bool] = isempty,
) -> Iterable[T]:
    """
    Apply a cascade of filters to an iterable of items.

    Each predicate in `filter_predicates` is applied to `items`, producing a list of
    matching items for that predicate. The first list that satisfies
    `cascade_predicate` (default: any items matched) is returned.

    Parameters
    ----------
    filter_predicates : Iterable[Callable[[T], bool]]
        An iterable of predicate functions. Each function takes an item of type T
        and returns True if the item should be kept.
    items : Iterable[T]
        The iterable of items to filter.
    cascade_predicate : Callable[[Iterable[T]], bool], optional
        A predicate applied to each filtered list. The first list that makes this
        predicate return True is returned. Defaults to lambda x: any(True for _ in x)
        (i.e., returns the first non-empty filtered list).

    Returns
    -------
    Iterable[T]
        The first filtered list that satisfies `cascade_predicate`.

    Raises
    ------
    NoItemsMatchedError
        If none of the filtered lists satisfy `cascade_predicate`.
    """
    filtered = map(lambda fc: filter(fc, items), filter_predicates)

    try:
        # get the first match
        return takefirst(fchain([fnot, cascade_predicate]), iter(filtered))
    except StopIteration:
        raise NoItemsMatchedError(
            f"No items satisfies the filters. Tried {len(list(filter_predicates))} filter(s)."
        )


def cascade_filter_safe(
    filter_predicates: Iterable[Callable[[T], bool]],
    items: Iterable[T],
    cascade_predicate: Callable[[Iterable[T]], bool] = isempty,
) -> Iterable[T]:
    """
    See `cascade_filter` for documentation
    """
    try:
        return cascade_filter(filter_predicates, items, cascade_predicate)
    except NoItemsMatchedError:
        return []


if __name__ == "__main__":
    items = range(10)

    filters = [
        lambda x: x > 20,  # will fail
        lambda x: x > 5,  # will work
        lambda x: x > 1,  # will work
    ]

    filters_bad = [
        lambda x: x > 20,  # will fail
        lambda x: x > 25,
        lambda x: x > 100,
    ]

    print(list(cascade_filter_safe(filters, items)))

    # print(first(items))
