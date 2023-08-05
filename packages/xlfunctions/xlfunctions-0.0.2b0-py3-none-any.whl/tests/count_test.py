
# Excel reference: https://support.office.com/en-us/article/COUNT-function-a59cd7fc-b623-4d93-87a4-d23bf411294c

import unittest

import pandas as pd

from xlfunctions import Count

"""
The COUNT function syntax has the following arguments:

value1    Required. The first item, cell reference, or range within which you want to count numbers.

value2, ...    Optional. Up to 255 additional items, cell references, or ranges within which you want to count numbers.

Note: The arguments can contain or refer to a variety of different types of data, but only numbers are counted.
"""

class TestCount(unittest.TestCase):

    def test_count(self):
        range_00 = pd.DataFrame([[1, 2],[3, 4]])
        choose_result_00 = Count.count(range_00)
        result_00 = 4
        self.assertEqual(result_00, choose_result_00)

        range_01 = pd.DataFrame([[2, 1],[3, "SPAM"]])
        choose_result_01 = Count.count(range_01)
        result_01 = 3
        self.assertEqual(result_01, choose_result_01)

        choose_result_02 = Count.count(range_00, range_01)
        result_02 = 7
        self.assertEqual(result_02, choose_result_02)

        choose_result_03 = Count.count(range_00, range_01, 1)
        result_03 = 8
        self.assertEqual(result_03, choose_result_03)

        choose_result_04 = Count.count(range_00, range_01, 1, "SPAM")
        result_04 = 8
        self.assertEqual(result_04, choose_result_04)
