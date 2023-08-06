import doctest
import unittest

import zc.set


def setUpSetsOne(test):
    test.globs['factory'] = set


def setUpSetsTwo(test):
    test.globs['factory'] = zc.set.Set


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite('README.txt', setUp=setUpSetsOne,
                             optionflags=doctest.ELLIPSIS),
        doctest.DocFileSuite('README.txt', setUp=setUpSetsTwo,
                             optionflags=doctest.ELLIPSIS),
    ])
