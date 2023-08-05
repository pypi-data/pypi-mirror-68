
# Excel reference: https://support.office.com/en-us/article/CHOOSE-function-fc5c184f-cb62-4ec7-a46e-38653b98f5bc

from pandas import DataFrame

from .excel_lib import BaseFunction
from .exceptions import ExcelError

class Choose(BaseFunction):
    """"""

    @staticmethod
    def choose(index_num, *values):
        """"""

        if isinstance(index_num, str):
            index_num = int(index_num)

        if index_num <= 0 or index_num > 254:
            return ExcelError("#VALUE!", "{} must be between 1 and 254".format( str(index_num) ))

        elif index_num > len(values):
            return ExcelError("#VALUE!", "{} must not be larger than the number of values: {}".format( str(index_num), len(values)) )

        else:

            if isinstance(values[index_num - 1], DataFrame):
                return values[index_num - 1]

            else:
                return values[index_num - 1]
