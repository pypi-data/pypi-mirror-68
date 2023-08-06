import os
import unittest

from z3c.recipe.compattest.testing import DocFileSuite


def test_suite():
    suite = unittest.TestSuite()
    here = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(here, 'setup.py')):
        prev, here = here, os.path.dirname(here)
        if here == prev:
            # Let's avoid infinite loops at root
            class SkippedDocTests(unittest.TestCase):  # pragma: no cover

                @unittest.skip('Could not find setup.py')
                def test_docs(self):
                    pass

            suite.addTest(
                unittest.makeSuite(SkippedDocTests))  # pragma: no cover
            return suite  # pragma: no cover

    readme = os.path.join(here, 'README.rst')

    suite.addTest(DocFileSuite(('runner.rst',)))
    suite.addTest(DocFileSuite((readme,), module_relative=False))
    return suite
