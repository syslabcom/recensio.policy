import unittest2 as unittest
import doctest
from recensio.policy import citation

def test_suite():
    return doctest.DocTestSuite(citation)
