import unittest


class Assert(unittest.TestCase):
    """A dummy class for exposing unittests assertion methods"""

    longMessage = True  # Include the message & variable values

    def runTest(self):
        pass  # we define runTest to allow the class to be instantiated.

    def equal(self, a, b, msg=None):
        self.assertEqual(a, b, msg)

    def not_equal(self, a, b, msg=None):
        self.assertNotEqual(a, b, msg)

    def is_(self, a, b, msg=None):
        self.assertIs(a, b, msg)

    def is_not(self, a, b, msg=None):
        self.assertIsNot(a, b, msg)

    def in_(self, a, b, msg=None):
        self.assertIn(a, b, msg)

    def not_in(self, a, b, msg=None):
        self.assertNotIn(a, b, msg)

    def less(self, a, b, msg=None):
        self.assertLess(a, b, msg)

    def less_equal(self, a, b, msg=None):
        self.assertLessEqual(a, b, msg)

    def greater(self, a, b, msg=None):
        self.assertGreater(a, b, msg)

    def greater_equal(self, a, b, msg=None):
        self.assertGreaterEqual(a, b, msg)

    def true(self, a, b, msg=None):
        self.assertTrue(a, b, msg)

    def false(self, a, b, msg=None):
        self.assertFalse(a, b, msg)


_assert = Assert()
assert_equal = _assert.equal
assert_not_equal = _assert.not_equal
assert_is = _assert.is_
assert_is_not = _assert.is_not
assert_in = _assert.in_
assert_not_in = _assert.not_in
assert_less = _assert.less
assert_less_equal = _assert.less_equal
assert_greater = _assert.greater
assert_greater_equal = _assert.greater_equal
assert_true = _assert.true
assert_false = _assert.false
