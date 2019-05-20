import sys
from app.TuringMachine import TuringMachine

def main(*args):
    filepath = ""
    word = ""
    tm = TuringMachine()

    if len(sys.argv) > 3:
        sys.exit(
            "Tmtrace only takes two arguments. (tmsourcefile, word)")
    elif len(sys.argv) == 3:
        filepath = sys.argv[1]
        tm.parsefile(filepath)
        word = sys.argv[2]     
        tm.runtrace(word)
    elif len(sys.argv) == 2:
        filepath = sys.argv[1]
        tm.parsefile(filepath)
        word = input("Please enter a word: ")
        tm.runtrace(word)
    else:
        filepath = input("Please enter a path to the source.TM file: ")
        tm.parsefile(filepath)
        word = input("Please enter a word: ")
        tm.runtrace(word)



if __name__ == '__main__':
    main(*sys.argv[1:])
