
import sys
import itertools
from factcheck import *

# Pretty rudimentary tests.  In particular, they test nothing about distributions.

@forall(x=always("foo"))
def test_always_always_returns_same_value(x):
    assert x == "foo"

@forall(x=[1,2], y=[20,30])
def test_can_specify_fixed_sequence_of_inputs(x, y):
    assert x in (1,2) and y in (20,30)

@forall(x=[1,2], samples=300)
def test_can_specify_fixed_sequence_of_inputs_which_is_then_repeated(x):
    assert x == 1 or x == 2

class TestCanApplyForallDecoratorToTestMethods:
    @forall(x=ints())
    def test_example_method(self, x):
        type(x) == int

@forall(v=choices([3, 6, 2, 1, 11]))
def test_choice_selects_random_elements_from_a_sequence(v):
    assert v in [3, 6, 2, 1, 11]

@forall(n=ints(-3,4))
def test_ints_generates_ints_between_min_and_max_inclusive(n):
    assert -3 <= n <= 4

@forall(n=ints())
def test_ints_generates_ints_between_default_min_and_max_inclusive(n):
    assert default_min_int <= n <= default_max_int

@forall(n=from_range(start=2, stop=22, step=4))
def test_from_range_generates_ints_between_start_inclusive_stop_exclusive_by_step(n):
    assert 2 <= n < 22
    assert n%4 == 2

@forall(l=lists(lengths=ints(min=2,max=4), elements=ints(min=10,max=20)))
def test_lists_generates_random_length_lists_with_random_elements(l):
    assert 2 <= len(l) <= 4
    assert all(10 <= e <= 20 for e in l)

@forall(l=lists())
def test_lists_with_no_parameters_generates_lists_of_default_lengths_with_integer_elements(l):
    assert 0 <= len(l) <= 32
    assert all(type(i) == int for i in l)

@forall(t=tuples(ints(2,4), ints(3,9)))
def test_tuples_generates_random_fixed_size_tuples(t):
    assert 2 <= t[0] <= 4
    assert 3 <= t[1] <= 9

@forall(d=dicts({'a':ints(3,7), 'b':ints(0,6)}))
def test_dicts_generates_dicts_with_fixed_keys_and_random_values(d):
    assert 3 <= d['a'] <= 7
    assert 0 <= d['b'] <= 6

@forall(d=dicts({}))
def test_dicts_can_generate_empty_dictionaries(d):
    assert len(d) == 0

@forall(i=bitseqs(lengths=ints(min=3,max=4)))
def test_bitseqs_generates_integers_with_random_bits_of_random_size(i):
    assert 0 <= i < 16

@forall(f=floats(1.0, 3.0))
def test_floats_generates_floating_point_numbers_within_range(f):
    assert 1.0 <= f < 3.0

@forall(f=floats())
def test_floats_generates_floating_point_numbers_within_default_range(f):
    assert default_min_float <= f <= default_max_float

def _f(a, b, c, d):
    return (a+b-c)+d

@forall(n=mapping(_f, always(1), b=always(2), d=always(3), c=always(4)))
def test_mapping_generates_result_of_mapping_callable_over_argument_generators(n):
    assert n == 2

@forall(n=mapping(_f, always(1), always(2), always(4), always(3)))
def test_mapping_works_if_no_keyword_arguments(n):
    assert n == 2

def test_unique_returns_unique_elements_in_order():
    assert list(unique([1,2,3,2,1])) == [1,2,3]
    assert list(unique([])) == []

def test_unique_identifier_can_be_defined_by_key_function():
    assert list(unique([-1,-2,-3,1,2,3,4], key=abs)) == [-1, -2, -3, 4]


@forall(x=range(4), y=range(4), where=lambda x, y: x != y)
def test_can_filter_inputs(x, y):
    assert x != y

@forall(x=range(4), y=range(4), z=range(4), where=lambda x, y: x != y)
def test_do_not_need_to_refer_to_all_parameters_in_filter(x, y, z):
    assert x != y
