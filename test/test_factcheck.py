
import itertools
from factcheck import *

# Pretty rudimentary tests.  In particular, they test nothing about distributions.

@forall
def test_always_always_returns_same_value(x:always("foo")):
    assert x == "foo"


@forall(x=always("foo"))
def test_can_specify_inputs_in_decorator(x):
    assert x == "foo"

@forall
def test_can_specify_fixed_sequence_ofinputs(x:[1,2], y:[20,30]):
    assert x in (1,2) and y in (20,30)

@forall
def test_can_specify_fixed_sequence_of_inputs_which_is_then_repeated(x:[1,2], samples=300):
    assert x == 1 or x == 2

class TestCanApplyForallDecoratorToTestMethods:
    @forall
    def test_example_method(self, x:ints()):
        # Doesn't crash qc when run as a test
        pass

@forall
def test_choice_selects_random_elements_from_a_sequence(v:choices([3, 6, 2, 1, 11])):
    assert v in [3, 6, 2, 1, 11]

@forall
def test_ints_generates_ints_between_min_and_max_inclusive(n:ints(-3,4)):
    assert -3 <= n <= 4

@forall
def test_ints_generates_ints_between_default_min_and_max_inclusive(n:ints()):
    assert default_min_int <= n <= default_max_int

@forall
def test_from_range_generates_ints_between_start_inclusive_stop_exclusive_by_step(n:from_range(start=2, stop=22, step=4)):
    assert 2 <= n < 22
    assert n%4 == 2

@forall
def test_lists_generates_random_length_lists_with_random_elements(l:lists(lengths=ints(min=2,max=4), elements=ints(min=10,max=20))):
    assert 2 <= len(l) <= 4
    assert all(10 <= e <= 20 for e in l)

@forall
def test_lists_with_no_parameters_generates_lists_of_default_lengths_with_integer_elements(l:lists()):
    assert 0 <= len(l) <= 32
    assert all(type(i) == int for i in l)

@forall
def test_tuples_generates_random_fixed_size_tuples(t:tuples(ints(2,4), ints(3,9))):
    assert 2 <= t[0] <= 4
    assert 3 <= t[1] <= 9

@forall
def test_dicts_generates_dicts_with_fixed_keys_and_random_values(d:dicts({'a':ints(3,7), 'b':ints(0,6)})):
    assert 3 <= d['a'] <= 7
    assert 0 <= d['b'] <= 6

@forall
def test_bits_generates_integers_with_random_bits_of_random_size(i:bits(lengths=ints(min=3,max=4))):
    assert 0 <= i < 16

@forall
def test_floats_generates_floating_point_numbers_within_range(f:floats(1.0, 3.0)):
    assert 1.0 <= f < 3.0

@forall
def test_floats_generates_floating_point_numbers_within_default_range(f:floats()):
    assert default_min_float <= f < default_max_float

def _f(a, b, c, d):
    return (a+b-c)+d

@forall
def test_mapping_generates_result_of_mapping_callable_over_argument_generators(n: mapping(_f, always(1), b=always(2), d=always(3), c=always(4))):
    assert n == 2

def test_unique_returns_unique_elements_in_order():
    assert list(unique([1,2,3,2,1])) == [1,2,3]
    assert list(unique([])) == []

def test_unique_identifier_can_be_defined_by_key_function():
    assert list(unique([-1,-2,-3,1,2,3,4], key=abs)) == [-1, -2, -3, 4]

