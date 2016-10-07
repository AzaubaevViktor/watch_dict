import unittest

from watching import WatchList


class TestList(unittest.TestCase):
    def setUp(self):
        self.simple_list = WatchList([1, 2, 3, 4, 5])

    def pre_callback(self):
        self.is_callback_called = False
        self.args = None

    def callback(self, *args):
        self.is_callback_called = True
        self.args = args

    def test_need(self):
        self.simple_list.set_callback(1, self.callback)

        self.pre_callback()
        old_value = self.simple_list[1]
        self.simple_list[1] = 12
        self.assertTrue(self.is_callback_called)
        self.assertTupleEqual(self.args, (1, old_value, 12))

    def test_other(self):
        self.simple_list.set_callback(2, self.callback)

        self.pre_callback()
        self.simple_list[3] = 12
        self.assertFalse(self.is_callback_called)

    def test_pop(self):
        self.simple_list.set_callback(2, self.callback)

        self.pre_callback()
        old_value = self.simple_list[2]
        self.simple_list.pop(2)
        self.assertTrue(self.is_callback_called)
        self.assertTupleEqual(self.args, (2, old_value, None))

    def test_pop_other(self):
        self.simple_list.set_callback(2, self.callback)

        self.pre_callback()
        self.simple_list.pop(3)
        self.assertFalse(self.is_callback_called)

if "__main__" == __name__:
    unittest.main()
