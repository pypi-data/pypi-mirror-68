# -*- coding: utf-8 -*-

"""
tests.test_spinners
~~~~~~~~~~~~~~~~~~~

Tests for spinners collection.
"""

from __future__ import absolute_import

import json
from collections import OrderedDict

import pytest

from yaspin.compat import iteritems
from yaspin.spinners import SPINNERS_DATA, Spinners


spinners_dict = OrderedDict(json.loads(SPINNERS_DATA))


test_cases = [
    (name, v["frames"], v["interval"]) for name, v in iteritems(spinners_dict)
]


def test_len():
    assert len(Spinners) == len(spinners_dict)


# Entry example:
# ('balloon', [' ', '.', 'o', 'O', '@', '*', ' '], 140)
@pytest.mark.parametrize("name, frames, interval", test_cases)
def test_spinners(name, frames, interval):
    assert getattr(Spinners, name).frames == frames
    assert getattr(Spinners, name).interval == interval
