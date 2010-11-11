import unittest2 as unittest
import doctest
from recensio import policy

def test_suite():
    return doctest.DocTestSuite(policy)
