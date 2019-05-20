import sys
from antlr4.error.ErrorListener import ErrorListener


class tmErrorListener(ErrorListener):
    def __init__(self):
        super(tmErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        sys.exit("Unrecognized symbol {} in source.TM file found at line {}, column {} ({}).".format(
            offendingSymbol.text, line, column, msg))
