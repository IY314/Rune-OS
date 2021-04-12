"""
The Calculator (uses Sly Lex Yacc)
- has full order of operations
- supports +, -, *, /, and ^
- Special Commands:
    help - Shows this menu
    exit - Exits this app
"""
from sly import Lexer, Parser
import sys
sys.path.append("../")

INACCESSIBLE = True


def launch():
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        text = input("calc >")
        if text == "help":
            print(__doc__)
        elif text == "exit":
            from system import homepage
            return homepage.launch()
        else:
            result = parser.parse(lexer.tokenize(text))
            if result != None:
                print(result)


class CalcLexer(Lexer):
    tokens = { "NUMBER", "PLUS", "MINUS", "TIMES", "DIVIDE", "EXP" }

    literals = { "(", ")" }

    ignore = " \t"

    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    EXP = r"\^"

    @_(r"\d+(\.\d+)?")
    def NUMBER(self, t):
        int_value = int(t.value)
        if int_value != t.value:
            t.value = float(t.value)
        else:
            t.value = int_value
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print(f"Line {str(self.lineno)}: Invalid character {t.value[0]}")
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def error(self, token):
        print("Invalid syntax")

    @_("expr PLUS term")
    def expr(self, p):
        return p.expr + p.term

    @_("expr MINUS term")
    def expr(self, p):
        return p.expr - p.term

    @_("term")
    def expr(self, p):
        return p.term

    @_("term TIMES factor")
    def term(self, p):
        return p.term * p.factor

    @_("term DIVIDE factor")
    def term(self, p):
        if p.factor == 0:
            if p.term != 0:
                return "Infinity"
            else:
                return "Undefined"
        return p.term / p.factor

    @_("factor")
    def term(self, p):
        return p.factor

    @_("number EXP NUMBER")
    def factor(self, p):
        return p.number ** p.NUMBER

    @_("number")
    def factor(self, p):
        return p.number

    @_("NUMBER")
    def number(self, p):
        return p.NUMBER

    @_("\"(\" expr \")\"")
    def number(self, p):
        return p.expr
