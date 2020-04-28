import doctest

import unittest2 as unittest
from recensio import policy


def test_suite():
    return doctest.DocTestSuite(policy)
