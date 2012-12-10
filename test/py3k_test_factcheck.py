
import sys
import itertools
from factcheck import *

@forall
def test_can_specify_inputs_as_python_3_parameter_attributes(x:always("foo")):
    assert x == "foo"

@forall(samples=300)
def test_can_configure_test_samples_when_using_python_3_parameter_attributes(x:always("foo")):
    assert x == "foo"
