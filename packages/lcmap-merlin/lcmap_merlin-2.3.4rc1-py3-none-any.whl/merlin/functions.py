"""functions.py is a module of generalized, reusable functions"""

from collections import Counter
from cytoolz import drop
from cytoolz import first
from cytoolz import get_in
from cytoolz import merge
from cytoolz import partial
from cytoolz import reduce
from cytoolz import second
from datetime import datetime
from functools import singledispatch
import functools
import hashlib
import itertools
import json
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)


def extract(sequence, elements):
    """Given a sequence (possibly with nested sequences), extract
    the element identifed by the elements sequence.

    Args:
        sequence: A sequence of elements which may be other sequences
        elements: Sequence of nested element indicies (in sequence parameter)
            to extract

    Returns:
        The target element

    Example:
        >>> inputs = [1, (2, 3, (4, 5)), 6]
        >>> extract(inputs, [0])
        >>> 1
        >>> extract(inputs, [1])
        >>> (2, 3, (4, 5))
        >>> extract(inputs, [1, 0])
        >>> 2
        >>> extract(inputs, [1, 1])
        >>> 3
        >>> extract(inputs, [1, 2])
        >>> (4, 5)
        >>> extract(inputs, [1, 2, 0])
        >>> 4
    ...
    """

    e = tuple(elements)
    if len(e) == 0 or not getattr(sequence, '__iter__', False):
        return sequence
    else:
        seq = sequence[first(e)]
        return extract(seq, drop(1, e))


def flatten(iterable):
    """Reduce dimensionality of iterable containing iterables

    Args:
        iterable: A multi-dimensional iterable

    Returns:
        A one dimensional iterable
    """

    return itertools.chain.from_iterable(iterable)


def intersection(items):
    """Returns the intersecting set contained in items

    Args:
        items: Two dimensional sequence of items

    Returns:
        Intersecting set of items

    Example:
        >>> items = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        >>> intersection(items)
        {3}
    """

    return set.intersection(*(map(lambda x: set(x), items)))


def sha256(string):
    """Computes and returns a sha256 digest of the supplied string

    Args:
        string (str): string to digest

    Returns:
        digest value
    """

    return hashlib.sha256(string.encode('UTF-8')).hexdigest()


def md5(string):
    """Computes and returns an md5 digest of the supplied string

    Args:
        string: string to digest

    Returns:
        digest value
    """

    return hashlib.md5(string.encode('UTF-8')).hexdigest()


def sort(iterable, key=None):
    """Sorts an iterable"""

    return sorted(iterable, key=key, reverse=False)


def rsort(iterable, key=None):
    """Reverse sorts an iterable"""

    return sorted(iterable, key=key, reverse=True)


@singledispatch
def serialize(arg):
    """Converts datastructure to json, computes digest

    Args:
        dictionary: A python dict

    Returns:
        tuple: (digest,json)
    """

    s = json.dumps(arg, sort_keys=True, separators=(',', ':'),
                   ensure_ascii=True)
    return md5(s), s


@serialize.register(set)
def _(arg):
    """Converts set to list then serializes the resulting value"""

    return serialize(sorted(list(arg)))


def deserialize(string):
    """Reconstitues datastructure from a string.

    Args:
        string: A serialized data structure

    Returns:
        Data structure represented by string parameter
    """

    return json.loads(string)


def flip_keys(dods):
    """Accepts a dictionary of dictionaries and flips the outer and inner keys.
    All inner dictionaries must have a consistent set of keys or key Exception
    is raised.

    Args:
        dods: dict of dicts

    Returns:
        dict of dicts with inner and outer keys flipped

    Example:
        >>> dods = {"reds":   {(0, 0): [110, 110, 234, 664],
                               (0, 1): [23, 887, 110, 111]},
                    "greens": {(0, 0): [120, 112, 224, 624],
                               (0, 1): [33, 387, 310, 511]},
                    "blues":  {(0, 0): [128, 412, 244, 654],
                               (0, 1): [73, 987, 119, 191]},
        >>> flip_keys(dods)
        {(0, 0): {"reds":   [110, 110, 234, 664],
                  "greens": [120, 112, 224, 624],
                  "blues":  [128, 412, 244, 654], ... },
         (0, 1), {"reds":   [23, 887, 110, 111],
                  "greens": [33, 387, 310, 511],
                  "blues":  [73, 987, 119, 191], ... }}

    """

    def flip(innerkeys, outerkeys, inputs):
        for ik in innerkeys:
            yield({ik: {ok: inputs[ok][ik] for ok in outerkeys}})

    outerkeys = set(dods.keys())
    innerkeys = set(reduce(lambda accum, v: accum + v,
                           [list(dods[ok].keys()) for ok in outerkeys]))
    return merge(flip(innerkeys, outerkeys, dods))


def cqlstr(string):
    """Makes a string safe to use in Cassandra CQL commands

    Args:
        string: The string to use in CQL

    Returns:
        str: A safe string replacement
    """

    return re.sub('[-:.]', '_', string)


def represent(item):
    """Represents callables and values consistently

    Args:
        item: The item to represent

    Returns:
        Item representation
    """

    return repr(item.__name__) if callable(item) else repr(item)


def isnumeric(value):
    """Does a string value represent a number (positive or negative?)

    Args:
        value (str): A string

    Returns:
        bool: True or False
    """

    try:
        float(value)
        return True
    except:
        return False


def timed(f):
    """Timing wrapper for functions.  Prints start and stop time to INFO
    along with function name, arguments and keyword arguments.

    Args:
        f (function): Function to be timed

    Returns:
        function: Wrapped function
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        msg = '{}(args={}, kwargs={}):'.format(f.__name__,  args, kwargs)
        logger.info('{} start:{}'.format(msg, datetime.now().isoformat()))
        r = f(*args, **kwargs)
        logger.info('{} stop:{}'.format(msg, datetime.now().isoformat()))
        return r
    return wrapper


def seqeq(a, b):
    """Determine if two unordered sequences are equal.

    Args:
        a: sequence a
        b: sequence b

    Returns:
        bool: True or False
    """

    #runs in linear (On) time.
    return Counter(a) == Counter(b)


def issubset(a, b):
    """Determines if a exists in b

    Args:
        a: sequence a
        b: sequence b

    Returns:
        bool: True or False
    """

    return set(a).issubset(set(b))


def difference(a, b):
    """Subtracts items in b from items in a.

    Args:
        a: sequence a
        b: sequence b

    Returns:
        set: items that exist in a but not b
    """

    return set(a) - set(b)


def chexists(dictionary, keys, check_fn):
    """applies check_fn against dictionary minus keys then ensures the items
    returned from check_fn exist in dictionary[keys]

    Args:
        dictionary (dict): {key: [v1, v3, v2]}
        keys (sequence): A sequence of keys in dictionary
        check_fn (function): Function that accepts dict and returns
                             sequence of items or Exception

    Returns:
        A sequence of items that are returned from check_fn and exist in
        dictionary[keys] or Exception
    """

    def exists_in(superset, subset):
        if issubset(subset, second(superset)):
            return True
        else:
            msg =  '{} is missing data.'.format(first(superset))
            msg2 = '{} is not a subset of {}'.format(subset, second(superset))
            raise Exception('\n\n'.join([msg, msg2]))

    popped  = {k: dictionary[k] for k in keys}
    checked = check_fn({k: dictionary[k] for k in difference(dictionary, keys)})
    all(map(partial(exists_in, subset=checked), popped.items()))
    return checked


def insert_into_every(dods, key, value):
    """Insert key:values into every subdictionary of dods.

    Args:
        dods: dictionary of dictionaries
        key: key to hold values in subdictionaires
        value: value to associate with key

    Returns:
        dict: dictionary of dictionaries with key:values inserted into each
    """

    def update(d, v):
        d.update({key: v})
        return d

    return {k: update(v, value) for k, v in dods.items()}


@singledispatch
def denumpify(arg):
    """Converts numpy datatypes to python datatypes

    bool_ and bool8 are converted to Python bool
    float64, float32 and float16's are converted to Python float()
    intc, intp, int8, int16, int32, int64, uint8, uint16, uint32 and uint64 are converted to Python int()
    complex_, complex64 and complex128 are converted to Python complex()
    None is returned as None
    numpy ndarrays are returned as list()    

    Python lists, maps, sets and tuples are returned with all values converted
    to Python types (recursively).

    If there is no implemented converter, returns arg.

    Args:
        arg: A (possibly numpy) data structure

    Returns:
        A Python data structure
    """
    
    return arg


@denumpify.register(np.bool_)
@denumpify.register(np.bool8)
def _(arg):
    """Converts numpy bools to python bools"""
    return bool(arg)


@denumpify.register(np.float64)
@denumpify.register(np.float32)
@denumpify.register(np.float16)
def _(arg):
    """Converts numpy floats to python floats"""
    return float(arg)


@denumpify.register(np.intc)
@denumpify.register(np.intp)
@denumpify.register(np.int8)
@denumpify.register(np.int16)
@denumpify.register(np.int32)
@denumpify.register(np.int64)
@denumpify.register(np.uint8)
@denumpify.register(np.uint16)
@denumpify.register(np.uint32)
@denumpify.register(np.uint64)
def _(arg):
    """Converts numpy ints to python ints"""
    return int(arg)


@denumpify.register(np.complex_)
@denumpify.register(np.complex64)
@denumpify.register(np.complex128)
def _(arg):
    """Converts numpy complex numbers to python complex"""
    return complex(arg)


@denumpify.register(np.ndarray)
def _(arg):
    """Converts ndarray to listset to list"""
    return arg.tolist()


@denumpify.register(list)
def _(arg):
    """Converts list values to Python types"""
    return [denumpify(l) for l in arg]


@denumpify.register(set)
def _(arg):
    """Converts set values to Python types"""
    return set(denumpify(list(arg)))


@denumpify.register(tuple)
def _(arg):
    """Converts tuple values to Python types"""
    return tuple(denumpify(list(arg)))

        
@denumpify.register(dict)
def _(arg):
    """Converts dict values to Python types"""
    return {k: denumpify(v) for k, v in arg.items()}