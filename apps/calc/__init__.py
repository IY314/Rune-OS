"""
The Calculator (uses Sly Lex Yacc)
- has full order of operations
- supports +, -, *, and /
"""
from sly import Lexer, Parser
import sys
sys.path.append("../")


def launch():
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        text = input("calc >")
        if text == "help":
            print(__doc__)
        elif text == "exit":
            from apps import homepage
            return homepage.launch()
        else:
            result = parser.parse(lexer.tokenize(text))
            print(result)


class CalcLexer(Lexer):
    tokens = { NUMBER, PLUS, MINUS, TIMES, DIVIDE }

    literals = { "(", ")" }

    ignore = " \t"

    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"

    @_(r"\d+(\.)?\d*")
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")
    
    def error(self, t):
        print(f"Line {str(self.lineno)}: Bad character {t.value[0]}")
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

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
        return p.term / p.factor
    
    @_("factor")
    def term(self, p):
        return p.factor
    
    @_("NUMBER")
    def factor(self, p):
        return p.NUMBER
    
    @_("\"(\" expr \")\"")
    def factor(self, p):
        return p.expr
    
    


if __name__ == "__main__":
    launch()
