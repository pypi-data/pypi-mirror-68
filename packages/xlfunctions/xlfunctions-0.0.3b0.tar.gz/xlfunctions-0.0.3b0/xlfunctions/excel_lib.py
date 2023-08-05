
from datetime import datetime
from collections.abc import Iterable
import itertools

from pandas import DataFrame

######################################################################################
# A dictionary that maps excel function names onto python equivalents. You should
# only add an entry to this map if the python name is different to the excel name
# (which it may need to be to  prevent conflicts with existing python functions
# with that name, e.g., max).

# So if excel defines a function foobar(), all you have to do is add a function
# called foobar to this module.  You only need to add it to the function map,
# if you want to use a different name in the python code.

# Note: some functions (if, pi, atan2, and, or, array, ...) are already taken care of
# in the FunctionNode code, so adding them here will have no effect.

SUPPORTED_FUNCTIONS = {
    "ABS":"xAbs.xabs",
    "AVERAGE":"Average.average",
    "CHOOSE":"Choose.choose",
    "_XLFN.CONCAT":"Concat.concat",
    "COUNT":"Count.count",
    "COUNTA":"Counta.counta",
    "DATE":"xDate.xdate",
    "IRR":"IRR.irr",
    "LN":"Ln.ln",
    "MAX":"xMax.xmax",
    "MID":"Mid.mid",
    "MIN":"xMin.xmin",
    "MOD":"Mod.mod",
    "NPV":"NPV.npv",
    "PMT":"PMT.pmt",
    "POWER":"Power.power",
    "RIGHT":"Right.right",
    "ROUND":"xRound.xround",
    "ROUNDDOWN":"xRound.rounddown",
    "ROUNDUP":"xRound.roundup",
    "SLN":"SLN.sln",
    "SQRT":"Sqrt.sqrt",
    "SUM":"xSum.xsum",
    "SUMPRODUCT":"Sumproduct.sumproduct",
    "TODAY":"Today.today",
    "VLOOKUP":"VLookup.vlookup", # need to support shared formulas and XLRange.ncols
    "XNPV":"XNPV.xnpv",
    "YEARFRAC":"Yearfrac.yearfrac",
}

IND_FUN = [
    "IF",
    "TAN",
    "ATAN2",
    "PI",
    "ARRAY",
    "ARRAYROW",
    "AND",
    "OR",
    "ALL",
    "VALUE",
    "LOG"
]


class BaseFunction():

    COMPATIBILITY = 'EXCEL'
    EXCEL_EPOCH = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
    CELL_CHARACTER_LIMIT = 32767

    ErrorCodes = (
        "#NULL!",
        "#DIV/0!",
        "#VALUE!",
        "#REF!",
        "#NAME?",
        "#NUM!",
        "#N/A"
    )


    @staticmethod
    def value(text):
        """"""

        # make the distinction for naca numbers
        if text.find('.') > 0:
            return float(text)

        elif text.endswith('%'):
            text = text.replace('%', '')
            return float(text) / 100

        else:
            return int(text)


    @staticmethod
    def extract_numeric_values(*args):
        """"""

        values = []

        for arg in args:
            if isinstance(arg, XLRange):
                for x in arg.values:
                    values

        return values


    @staticmethod
    def is_number(value): # http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python
        """Determines if a value is a number."""
        return isinstance(value, (int, float))


    @staticmethod
    def flatten(this_list, only_lists=False):
        if isinstance(this_list, DataFrame):
            this_list = this_list.values.tolist()

        return list(itertools.chain(*this_list))
    # def flatten(l, only_lists = False):
    #     instance = list if only_lists else collections.Iterable
    #
    #     for el in l:
    #         if isinstance(el, instance) and not isinstance(el, string_types):
    #             for sub in flatten(el, only_lists = only_lists):
    #                 yield sub
    #         else:
    #             yield el


    @staticmethod
    def find_corresponding_index(list, criteria):

        # parse criteria
        check = BaseFunction.criteria_parser(criteria)

        valid = []

        for index, item in enumerate(list):
            if check(item):
                valid.append(index)

        return valid


    @staticmethod
    def criteria_parser(criteria):

        if BaseFunction.is_number(criteria):
            def check(x):
                return x == criteria #and type(x) == type(criteria)

        elif type(criteria) == str:
            search = re.search('(\W*)(.*)', criteria.lower()).group
            operator = search(1)
            value = search(2)
            value = float(value) if BaseFunction.is_number(value) else str(value)

            if operator == '<':
                def check(x):
                    if not BaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x < value

            elif operator == '>':
                def check(x):
                    if not BaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x > value

            elif operator == '>=':
                def check(x):
                    if not BaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x >= value

            elif operator == '<=':
                def check(x):
                    if not BaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x <= value

            elif operator == '<>':
                def check(x):
                    if not BaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x != value

            else:
                def check(x):
                    return x == criteria

        else:
            raise Exception('Could\'t parse criteria %s' % criteria)

        return check


    @staticmethod
    def check_value(a):
        """"""

        if isinstance(a, ExcelError):
            return a

        elif isinstance(a, str) and a in ErrorCodes:
            return ExcelError(a)

        try:  # This is to avoid None or Exception returned by Range operations
            if float(a) or isinstance(a, (str)):
                return a

            else:
                return 0

        except:
            if a == 'True':
                return True

            elif a == 'False':
                return False

            else:
                return 0
