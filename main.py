import sys
from lexer import Lexer, LexicalError
from parser import Parser, SyntaxError, SemanticError


if __name__ == '__main__':
    text = sys.stdin.read()
    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        symtab = parser.parse()
        print("Program parsed successfully.")
        print("Symbol table:")
        print(symtab)
    except (LexicalError, SyntaxError, SemanticError) as e:
        print(type(e).__name__ + ":", e)