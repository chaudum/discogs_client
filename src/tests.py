# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"


import unittest, doctest
from zope.testing.doctestunit import DocFileSuite


class TestLayer(object):

    @classmethod
    def setUp(self):
        pass

    @classmethod
    def tearDown(self):
        pass

    @classmethod
    def testSetUp(self):
        pass

    @classmethod
    def testTearDown(self):
        pass

def test_suite():
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testfile('README.mkd', optionflags=doctest.ELLIPSIS)
    tests = (
        DocFileSuite('discogs.rst', optionflags=optionflags),
        # DocFileSuite('client.txt', optionflags=optionflags),
        )
    suite = unittest.TestSuite(tests)
    suite.layer = TestLayer
    return suite
