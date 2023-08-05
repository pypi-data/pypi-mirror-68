"""Contains classes and functions designed to improve the ease of processing iterable data.
"""

# Optional imports for numpy and pandas.
try:
    import numpy as np
except ImportError:
    np = None

try:
    import pandas as pd
except ImportError:
    pd = None


class Query():
    """Wraps around any object to allow for iterable manipulations and operations to be performed on it.
    """

    def __init__(self, obj):
        """Initialize a Query object.

        Args:
            obj (object): The object to perform a query on.
        """

        # Initialize with an object that we store.
        self.object = obj

    def evaluate(self):
        """Get the currently stored query object.

        Returns:
            object: The current query object.
        """

        # Simply return the stored object.
        return self.object

    @staticmethod
    def __default_iterator(obj, axis=None):
        """Obtain the default iterator for a specified object along an optional axis.

        Args:
            obj (object): The object to find the iterator of.
            axis (None or int, optional): The axis of a numpy.ndarray or pandas.DataFrame to iterate over.
                For instance, axis=0 iterates over rows and axis=1 iterates over columns. By default, iteration will be
                over rows. Should be left as None if not using a numpy.ndarray nor pandas.DataFrame. Defaults to None.

        Raises:
            ValueError: If axis was out of the range of the query object.
            ValueError: If axis was specified for query object not of type numpy.ndarray or pandas.DataFrame.
            TypeError: If query object is not iterable.

        Returns:
            iterator: An iterator over the given object.
        """

        # Define a generator to return a function applied to each item in an iterable.
        def enumeration_iterator(iterate, enum=False):
            """Generate the items of an iterator which may be enumerated.

            Args:
                iterate (iter): The iterator to pull items from.
                enum (bool, optional): Whether the iterator produces (index, value) pairs. Defaults to False.

            Yields:
                object: Each item of the given iterator.
            """

            # If enum is true, iterables are a tuple (index, value).
            if enum:
                for _, item in iterate:
                    yield item
            else:
                for item in iterate:
                    yield item

        # Handle numpy arrays.
        if np and isinstance(obj, np.ndarray):
            # Default axis is 0 (rows).
            if axis is None:
                axis = 0
            # Try applying function to specified axis of query object.
            return enumeration_iterator(np.rollaxis(obj, axis))

        # Handle pandas dataframes.
        if pd and isinstance(obj, pd.DataFrame):
            # Default axis is 0 (rows).
            if axis is None:
                axis = 0

            # Handle axis 0 (rows), axis 1 (columns), or erraneous axis respectively.
            if axis == 0:
                return enumeration_iterator(obj.iterrows(), enum=True)
            if axis == 1:
                return enumeration_iterator(obj.iteritems(), enum=True)
            raise ValueError("'axis' is not valid for `DataFrame` object; must be 0 or 1")

        # Handle generic iterable objects.
        if axis is None:
            # Try applying function to iterable version of query object.
            return enumeration_iterator(iter(obj))

        # Throw error if axis was set but we do not have an array or dataframe.
        raise ValueError("'axis' was specified but query object does not have axes")

    def select(self, func, axis=None):
        """
        Iterate over each item in the query object and apply the specified function to each item. If the query object
        is a ``numpy.ndarray`` or a ``pandas.DataFrame``, can iterate over a particular axis.

        Args:
            func (function): The function to apply to each item in the query object.
            axis (None or int, optional): The axis of a ``numpy.ndarray`` or ``pandas.DataFrame`` to iterate over. For
                instance, ``axis=0`` iterates over rows and ``axis=1`` iterates over columns. By default, iteration will
                be over rows. Should be left as ``None`` if not using a ``numpy.ndarray`` nor ``pandas.DataFrame``.
                Defaults to ``None``.

        Returns:
            Query:
            The query whose object is a generator over the items of the original query object with the function
            applied.
        """

        # Return a Query wrapping the iterator.
        iterator = Query.__default_iterator(self.object, axis)
        return Query((func(item) for item in iterator))

    def where(self, func, axis=None):
        """
        Iterate over each item in the query object and yield each one only if the specified function is satisfied. If
        the query object is a ``numpy.ndarray`` or a ``pandas.DataFrame``, can iterate over a particular axis.

        Args:
            func (function): The function to check if an item should be yielded.
            axis (None or int, optional): The axis of a ``numpy.ndarray`` or ``pandas.DataFrame`` to iterate over. For
                instance, ``axis=0`` iterates over rows and ``axis=1`` iterates over columns. By default, iteration will
                be over rows. Should be left as ``None`` if not using a ``numpy.ndarray`` nor ``pandas.DataFrame``.
                Defaults to ``None``.

        Returns:
            Query:
            The query whose object is a generator over the items of the original query object with the function
            applied.
        """

        # Return a Query wrapping the iterator.
        iterator = Query.__default_iterator(self.object, axis)
        return Query((item for item in iterator if func(item)))

    def cut(self, lengths, axis=None):
        """
        Split each set of items in the query object into parts of specified length. If the query object is a
        ``numpy.ndarray`` or a ``pandas.DataFrame``, can cut a particular axis.

        Args:
            lengths (iterable of int): An iterable of positive lengths for cuts. The i-th cut part will have length
                ``lengths[i]``.
            axis (None or int, optional): The axis of a ``numpy.ndarray`` or ``pandas.DataFrame`` to iterate over. For
                instance, ``axis=0`` iterates over rows and ``axis=1`` iterates over columns. By default, iteration will
                be over rows. Should be left as ``None`` if not using a ``numpy.ndarray`` nor ``pandas.DataFrame``.
                Defaults to ``None``.

        Raises:
            ValueError: If the sum of lengths is greater than the length of the query object.
            ValueError: If the sum of lengths is less than the length of the query object.
            ValueError: If any of the lengths is non-positive.

        Returns:
            Query: The query whose object is a generator over the cut parts of the original query object.
        """

        def take(iterate, length):
            # Try to get specified number of elements from iterator.
            try:
                for _ in range(length):
                    yield next(iterate)
            except StopIteration:
                # Error if reach end of iterator.
                raise ValueError("sum of cut lengths must equal length of query object but was greater")

        def parts(iterate):
            # Return parts.
            for length in lengths:
                # Error if length is negative.
                if length <= 0:
                    raise ValueError("each cut length must be positive")
                yield take(iterate, length)

            # Error if did not reach end of iterator.
            try:
                next(iterate)
                raise ValueError("sum of cut lengths must equal length of query object but was less")
            except StopIteration:
                pass

        # Get the default iterator.
        iterator = Query.__default_iterator(self.object, axis)

        # Reconstruct numpy array.
        if np and isinstance(self.object, np.ndarray):
            if axis is None:
                axis = 0
            return Query(map(lambda x: np.stack(tuple(x), axis=axis), parts(iterator)))

        # Reconstruct pandas dataframe.
        # If cutting columns, simply stitch the columns back together.
        # If cutting rows, stitch the row series together as columns and transpose back to rows.
        if pd and isinstance(self.object, pd.DataFrame):
            if axis is None:
                axis = 0
            if axis == 0:
                return Query(map(lambda x: pd.concat(tuple(x), axis=1).T, parts(iterator)))
            if axis == 1:
                return Query(map(lambda x: pd.concat(tuple(x), axis=1), parts(iterator)))

        # Reconstruct string.
        if isinstance(self.object, str):
            return Query(map(''.join, parts(iterator)))

        # Reconstruct generic iterable.
        return Query(map(type(self.object), parts(iterator)))
