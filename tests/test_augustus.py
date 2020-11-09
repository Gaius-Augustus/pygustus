import unittest

import augustus


class TestAugustus(unittest.TestCase):

    def setUp(self):
        print('-------------------------------')

    def tearDown(self) -> None:
        print('-------------------------------')

    def test_augustus_help(self):
        augustus.run('--help')

    def test_augustus_wrong_parameter(self):
        with self.assertRaises(ValueError) as cm:
            augustus.run('--unknown=nothing')
        ex = cm.exception
        self.assertEqual(ex.error_code, 3)
