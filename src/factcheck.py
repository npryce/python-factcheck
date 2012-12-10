"""A simple but extensible implementation of QuickCheck 1 for Python 3.

Copyright (c) 2012 Nat Pryce.
"""

import sys
import random
from itertools import product, cycle, repeat, islice

if sys.version_info[0] > 2:
    imap = map
    izip = zip
else:
    from itertools import imap, izip


def _random_values(_generator_fn, *args, **kwargs):
    while True:
        yield _generator_fn(*args, **kwargs)


def always(v):
    """always returns 'v'"""
    return repeat(v)


def choices(seq):
    """random element from non-empty sequence 'seq'"""
    return _random_values(random.choice, seq)


def bits(lengths):
    """long ints with 'n' random bits"""
    return (random.getrandbits(length) for length in lengths)


default_min_int = -1000
"""Default min value for ints"""

default_max_int = +1000
"""Default max value for ints"""

def ints(min=None, max=None):
    """random integers between min and max, inclusive"""
    return _random_values(random.randint, 
                          min if min is not None else default_min_int, 
                          max if max is not None else default_max_int)


def from_range(start, stop=None, step=1):
    """random integers taken from range(start, stop[, step])"""
    return _random_values(random.randrange, start, stop, step)


default_min_float = sys.float_info.min
"""Default min value for floats"""

default_max_float = sys.float_info.max
"""Default max value for floats"""

def floats(a=None, b=None):
    """random floating-point numbers selected uniformly from [a,b) or [a,b] depending on rounding."""
    return _random_values(random.uniform,
                          a if a is not None else default_min_float,
                          b if b is not None else default_max_float)

default_sequence_lengths = ints(min=0, max=32)
"""Default lengths for sequences and lists"""

default_sequence_elements = ints()
"""Default elements for sequences and lists"""

def sequences(lengths=None, elements=None):
    """random length sequences of random elements"""
    elements = elements if elements is not None else default_sequence_elements
    lengths = lengths if lengths is not None else default_sequence_lengths
    
    return (islice(elements, length) for length in lengths)


def lists(lengths=None, elements=None):
    """random length lists of random elements"""
    return imap(list, sequences(lengths, elements))


def tuples(*elementses):
    """fixed-size tuples of random elements."""
    return izip(*elementses)


def dicts(d):
    """dicts with fixed keys and random values.
    
    Parameters:
       d : a dictionary mapping keys to generators
      
    Returns: a generator of dictionaries, mapping each key, k, of d to
       the next element of d[k].
    """
    keys, value_iters = izip(*d.items())
    return (dict(izip(keys,values)) for values in izip(*value_iters))


def mapping(f, *args_gens, **kwargs_gens):
    return (f(*args,**kwargs) for (args, kwargs) in izip(tuples(*args_gens), dicts(kwargs_gens)))


def unique(elements, key=(lambda x:x)):
    """Yield unique elements, preserving order."""
    seen = set()
    for element in elements:
        k = key(element)
        if k not in seen:
            seen.add(k)
            yield element


def _annotations(f):
    return f.__annotations__ if hasattr(f, "__annotations__") else {}



def forall(_test_fn=None, samples=100, **parameter_generators):    
    def bind_parameters(test_fn):
        parameter_generators.update(_annotations(test_fn))
        
        # Note: should be decorated by @functools.wraps(test_fn) but that confuses pytest
        def bound_test_fn(*args):
            param_names, param_value_iters = zip(*parameter_generators.items())
            param_value_samples = product(*[islice(cycle(i), samples) for i in param_value_iters])
            
            for param_values in param_value_samples:
                test_fn(*args, **dict(zip(param_names, param_values)))
        
        return bound_test_fn
    
    # Allow @forall, @forall(samples=100) or @forall(param1=generator1, param2=generator2, ...)
    return bind_parameters if _test_fn is None else bind_parameters(_test_fn)

