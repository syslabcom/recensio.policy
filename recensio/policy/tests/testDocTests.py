from recensio import policy

import doctest
import unittest2 as unittest


def test_suite():
    return doctest.DocTestSuite(policy)
