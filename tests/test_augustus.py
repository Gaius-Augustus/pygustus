#!/usr/bin/env python3

import unittest
import os
import augustus


class TestAugustus(unittest.TestCase):

    def test_augustus_help(self):
        augustus.run('--help')

    def test_augustus_simple(self):
        augustus.run('data/example.fa', species='human',
                     UTR='on', softmasking=False)

    def test_augustus_wrong_parameter(self):
        with self.assertRaises(ValueError) as cm:
            augustus.run('data/example.fa', species='human',
                         UTR='on', smasking=False)
        ex = cm.exception
        self.assertEqual(ex.error_code, 3)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAugustus('test_augustus_help'))
    suite.addTest(TestAugustus('test_augustus_simple'))
    suite.addTest(TestAugustus('test_augustus_wrong_parameter'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())

    if result.wasSuccessful():
        os._exit(0)
    else:
        os._exit(1)
