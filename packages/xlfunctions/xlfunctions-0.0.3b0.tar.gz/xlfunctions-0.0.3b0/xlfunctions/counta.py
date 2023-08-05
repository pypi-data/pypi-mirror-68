
# Excel reference: https://support.office.com/en-us/article/counta-function-7dc98875-d5c1-46f1-9a82-53f3219e2509

import itertools

from pandas import DataFrame

from .excel_lib import BaseFunction
from .exceptions import ExcelError

class Counta(BaseFunction):
    """"""

    @staticmethod
    def counta(arg_1, *args):
        """The COUNTA function counts the number of cells that are not empty in a range."""

        def get_counta(arg):
            if isinstance(arg, DataFrame):
                # I don't like nesting list comprehensions. But here we are...
                return len([element for element in [item for item in itertools.chain( *arg.values.tolist() ) ] if element not in ['', None]  ])

            elif arg not in ['', None]:
                return 1

            else:
                return 0


        if arg_1 is None:
            return ExcelError('#VALUE', 'value1 is required')

        if len(list(args)) > 255:
            return ExcelError('#VALUE', "Can only have up to 255 supplimentary arguments, you provided {}".format(len(args)))

        total = 0
        total += get_counta(arg_1)

        for arg in args:
            total += get_counta(arg)

        return total
