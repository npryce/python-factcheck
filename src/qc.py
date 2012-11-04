
import random
import itertools



def _random_values(_generator_fn, *args, **kwargs):
    while True:
        yield _generator_fn(*args, **kwargs)


def always(v):
    """always returns 'v'"""
    return itertools.repeat(v)


def choices(seq):
    """random element from non-empty sequence 'seq'"""
    return _random_values(random.choice, seq)


def bits(lengths):
    """long ints with 'n' random bits"""
    return (random.getrandbits(length) for length in lengths)


def ints(min,max):
    """random integers between min and max, inclusive"""
    return _random_values(random.randint, min, max)


def from_range(start, stop=None, step=1):
    """random integers taken from range(start, stop[, step])"""
    return _random_values(random.randrange, start, stop, step)


def floats(a, b):
    """random floating-point numbers from uniform distribution within (a,b]."""
    return _random_values(random.uniform, a, b)


def sequences(lengths, elements):
    """random length sequences of random elements"""
    return (itertools.islice(elements, length) for length in lengths)


def lists(lengths, elements):
    """random length lists of random elements"""
    return map(list, sequences(lengths, elements))


def tuples(*elementses):
    """fixed-size tuples of random elements."""
    return zip(*elementses)


def dicts(d):
    """dicts with fixed keys and random values.
    
    Parameters:
       d : a dictionary mapping keys to generators
      
    Returns: a generator of dictionaries, mapping each key, k, of d to
       the next element of d[k].
    """
    keys, value_iters = zip(*d.items())
    return (dict(zip(keys,values)) for values in zip(*value_iters))


def unique(elements, key=(lambda x:x)):
    """Yield unique elements, preserving order.
    
    Warning: will be an infinite loop if there fewer unique elements than tests run.
    """
    seen = set()
    for element in elements:
        k = key(element)
        if k not in seen:
            seen.add(k)
            yield element


def forall(test_fn=None, tests=100):
    def bind_parameters(test_fn):
        arg_bindings = dicts(test_fn.__annotations__)
        def bound_test_fn():
            for args in itertools.islice(arg_bindings, tests):
                test_fn(**args)
        return bound_test_fn
    
    # Allow @forall or @forall(tests=100)
    return bind_parameters if test_fn is None else bind_parameters(test_fn)


