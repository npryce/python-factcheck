"""A simple but extensible implementation of QuickCheck 1 for Python 3.

Copyright (c) 2012 Nat Pryce.
"""

import sys
import random
from itertools import product, cycle, repeat, islice, chain
import inspect


if sys.version_info[0] > 2:
    imap = map
    izip = zip
else:
    from itertools import imap, izip


def _random_values(_generator_fn, *args, **kwargs):    
    while True:
        yield _generator_fn(*args, **kwargs)

def _defaulted(value, default_value):
    return value if value is not None else default_value

def _actual(xs):
    return [x for x in xs if x is not None]


def always(v):
    """always returns 'v'"""
    return repeat(v)


def choices(seq):
    """random element from non-empty sequence 'seq'"""
    return _random_values(random.choice, seq)


def bitseqs(lengths):
    """long ints with 'n' random bits"""
    return (random.getrandbits(length) for length in lengths)


default_min_int = -1000
"""Default min value for ints"""

default_max_int = +1000
"""Default max value for ints"""

def ints(min=None, max=None):
    """random integers between min and max, inclusive"""
    return chain(_actual([min,max]),
                 _random_values(random.randint, 
                                _defaulted(min, default_min_int), 
                                _defaulted(max, default_max_int)))


def from_range(start, stop=None, step=1):
    """random integers taken from range(start, stop[, step])"""
    return chain(_actual(set([start,stop-step])),
                 _random_values(random.randrange, start, stop, step))


default_min_float = -1000
"""Default min value for floats"""

default_max_float = 1000
"""Default max value for floats"""

def floats(lower=None, upper=None):
    """random floating-point numbers selected uniformly from [a,b) or [a,b] depending on rounding."""
    return chain(_actual([lower]),
                 _random_values(random.uniform,
                                _defaulted(lower, default_min_float),
                                _defaulted(upper, default_max_float)))

default_sequence_lengths = ints(min=0, max=32)
"""Default lengths for sequences and lists"""

default_sequence_elements = ints()
"""Default elements for sequences and lists"""

def sequences(lengths=None, elements=None):
    """random length sequences of random elements"""
    elements = _defaulted(elements, default_sequence_elements)
    lengths = _defaulted(lengths, default_sequence_lengths)
    
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
    if d:
        keys, value_iters = izip(*d.items())
        return (dict(izip(keys,values)) for values in izip(*value_iters))
    else:
        return always({})


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

def _always(*args, **kwargs):
    return True

def _params(param_bindings, f):
    argspec = inspect.getargspec(f)
    if argspec.keywords is not None:
        return param_bindings
    else:
        return dict((k,param_bindings[k]) for k in argspec.args)


def forall(_test_fn=None, samples=1000, where=_always, **parameter_generators):    
    where_argspec = inspect.getargspec(where)
    if where_argspec.keywords is None:
        where_bindings = lambda d: {k:d[k] for k in where_argspec.args}
    else:
        where_bindings = lambda d: d
    
    def bind_parameters(test_fn):
        parameter_generators.update(_annotations(test_fn))
        
        # Note: should be decorated by @functools.wraps(test_fn) but that confuses pytest
        def bound_test_fn(*args):
            param_names, param_value_iters = zip(*parameter_generators.items())
            
            # Shuffle the values so that fixed boundary values are not always applied together
            param_value_populations = [list(islice(cycle(i),0,samples)) for i in param_value_iters]
            for l in param_value_populations:
                random.shuffle(l)
            
            for param_values in zip(*param_value_populations):
                param_bindings = dict(zip(param_names, param_values))
                
                if where(**where_bindings(param_bindings)):
                    test_fn(*args, **param_bindings)
        
        return bound_test_fn
    
    # Allow @forall, @forall(samples=100) or @forall(param1=generator1, param2=generator2, ...)
    return bind_parameters if _test_fn is None else bind_parameters(_test_fn)

