
# Excel reference: https://support.office.com/en-us/article/COUNT-function-a59cd7fc-b623-4d93-87a4-d23bf411294c

import itertools

from pandas import DataFrame

from .excel_lib import BaseFunction
from .exceptions import ExcelError

class Count(BaseFunction):
    """"""

    @staticmethod
    def count(arg_1, *args):
        """The COUNT function counts the number of cells that contain numbers, and counts numbers within the list of arguments."""

        def get_count(arg):
            if isinstance(arg, DataFrame):
                # I don't like nesting list comprehensions. But here we are...
                return len([element for element in [item for item in itertools.chain( *arg.values.tolist() ) ] if Count.is_number(element) ])

            elif Count.is_number(arg):
                return 1

            else:
                return 0


        if arg_1 is None:
            return ExcelError('#VALUE', 'value1 is required')

        if len(list(args)) > 255:
            return ExcelError('#VALUE', "Can only have up to 255 supplimentary arguments, you provided {}".format(len(args)))

        total = 0
        total += get_count(arg_1)

        for arg in args:
            total += get_count(arg)

        return total
