import os
import sys
from antlr4 import *
from app.parser.tmLexer import tmLexer
from app.parser.tmListener import tmListener
from app.parser.tmParser import tmParser
from app.listener.tmErrorListener import tmErrorListener
from app.listener.tmParseListener import tmParseListener


class TuringMachine():
    def __init__(self):
        self.states = []
        self.start = []
        self.accept = []
        self.reject = []
        self.alpha = []
        self.talpha = ['_']
        self.trans = []

    def parsefile(self, filepath):
        if not os.path.isfile(filepath):
            sys.exit('Invalid file path or filename. Check case or spelling.')
        if not filepath.lower().endswith('.tm'):
            sys.exit('Input file must have .tm extension.')
        filepath = os.path.abspath(filepath)
        input = FileStream(filepath)
        lexer = tmLexer(input)
        stream = CommonTokenStream(lexer)
        parser = tmParser(stream)
        parser._listeners = [tmErrorListener()]
        builder = tmParseListener(self)
        tree = parser.init()
        walker = ParseTreeWalker()
        walker.walk(builder, tree)
        self.ensurevalidtm()

    def ensurevalidtm(self):
        self.checkdup(self.start, "start")
        self.checkdup(self.accept, "accept")
        self.checkdup(self.reject, "reject")
        self.checkdup(self.alpha, "alphabet")
        self.checkdup(self.talpha, "tape alphabet")
        self.checkdup(self.trans, "transition function")
        self.checkaccrej()
        self.checkalph()
        self.checktalph()
        self.checktransacceprej()
        self.checktransmembership()
        self.checktransfunction()

    # Trace Functions
    def dotrans(self, headpos, tape, state):
        ahead = tape[headpos:]
        ahead = ahead[1:]
        behind = tape[:headpos]
        nextheadpos = headpos
        newtape = tape
        nextstate = state

        for transfunc in self.trans:
            if (state == transfunc[1] and tape[headpos] == transfunc[2]):
                if len(transfunc) > 3:
                    nextstate = transfunc[3]
                if len(transfunc) > 4:
                    newtape = behind + transfunc[4] + ahead
                    if headpos == len(tape) - 1 and not nextstate in self.accept:
                        newtape = newtape + '_'
                if transfunc[0] == 'R':
                    if headpos == len(newtape) - 1 and not nextstate in self.accept:
                        newtape = newtape + '_'
                    nextheadpos += 1
                else:
                    if not nextheadpos == 0:
                        nextheadpos -= 1
                return(nextheadpos, newtape, nextstate)
            else:
                continue

        return(headpos, tape, state)

    def trace(self, headpos, tape, state):
        try:
            strtape = tape[:-1]
            string = strtape[:headpos] + \
                '[' + str(state) + ']' + strtape[headpos:]
            if state in self.accept:
                print("Accept: " + string)
                return
            elif state in self.reject:
                print("Reject: " + string)
                return
            else:
                tmp = self.dotrans(headpos, tape, state)
                x, y, z = tmp
                if x == headpos and y == tape and z == state:
                    print("Reject (loop or no transition): " + string)
                    return
                else:
                    print(string)
                    self.trace(x, y, z)
        except:
            sys.exit("\nMaximum recursion depth exceeded at configuration:")

    def runtrace(self, word):
        self.checkword(word)
        word = word + '_'
        start = self.start[0]
        self.trace(0, word, start)

    # Error Functions
    def checkdup(self, list, listname):
        tmp = []
        for i in list:
            if i in tmp:
                sys.exit(
                    "Duplicate item found in {} list. (Item: {})".format(listname, i))
            tmp.append(i)

    def checkaccrej(self):
        for state in self.accept:
            if state in self.reject:
                sys.exit(
                    "Accept list intersecting reject list (Offending state: {})".format(state))

    def checkalph(self):
        if '_' in self.alpha:
            sys.exit("Special '_' symbol found in input alphabet.")

    def checkword(self, word):
        for c in word:
            if c not in self.alpha:
                sys.exit(
                    "Symbol in input word not in input Alphabet. (Offending symbol: {})".format(c))

    def checktalph(self):
        for item in self.alpha:
            if not item in self.talpha:
                sys.exit(
                    "Tape alphabet missing symbol in input alphabet. (Missing symbol: {})".format(item))

    def checktransacceprej(self):
        for transfunc in self.trans:
            if transfunc[1] in self.accept:
                sys.exit(
                    "Transition on accept state found. (Transition function: {}".format(transfunc))
            if transfunc[1] in self.reject:
                sys.exit(
                    "Transition on reject state found. (Transition function: {}".format(transfunc))

    def checktransmembership(self):
        for transfunc in self.trans:
            if not transfunc[1] in self.states:
                sys.exit("Transition function contains state not in the list of states. (Transition function: {}, State: '{}')".format(
                    transfunc, transfunc[1]))
            if not transfunc[2] in self.talpha:
                sys.exit("Transition function contains symbol not in the list of tape alphabet symbols. (Transition function: {}, Symbol: '{}')".format(
                    transfunc, transfunc[3]))
            if len(transfunc) > 3:
                if not transfunc[1] in self.states:
                    sys.exit("Transition function contains state not in the list of states. (Transition function: {}, State: '{}')".format(
                        transfunc, transfunc[3]))
            if len(transfunc) > 4:
                if not transfunc[1] in self.states:
                    sys.exit("Transition function contains symbol not in the list of input alphabet symbols. (Transition function: {}, Symbol: '{}')".format(
                        transfunc, transfunc[4]))

    def checktransfunction(self):
        outertemp = []
        for transfunc in self.trans:
            tmp = [transfunc[1], transfunc[2]]
            if tmp in outertemp:
                sys.exit("Transition function has two outputs. (State: '{}' Reading:'{}')".format(
                    tmp[0], tmp[1]))
