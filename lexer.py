import re
from token import Token, TokenType


class LexicalError(Exception):
    pass


class Lexer:
    token_spec = [
        ('NUMBER', r'\d+(\.\d+)?([eE][+-]?\d+)?'),
        ('ID', r'[A-Za-z][A-Za-z0-9]*'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MUL', r'\*'),
        ('DIV', r'/'),
        ('ASSIGN', r'='),
        ('DOT', r'\.'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('SEMICOLON', r';'),
        ('SKIP', r'[ \t\n]+'),
        ('MISMATCH', r'.'),
    ]

    def __init__(self, text):
        self.text = text
        self.regex = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in self.token_spec))
        self.tokens = []
        self._tokenize()
        self.tokens.append(Token(TokenType.EOF, pos=len(text)))
        self.index = 0

    def _tokenize(self):
        for m in self.regex.finditer(self.text):
            kind = m.lastgroup
            value = m.group()
            pos = m.start()
            if kind == 'NUMBER':
                self.tokens.append(Token(TokenType.NUMBER, float(value), pos))
            elif kind == 'ID':
                self.tokens.append(Token(TokenType.ID, value, pos))
            elif kind == 'PLUS':
                self.tokens.append(Token(TokenType.PLUS, value, pos))
            elif kind == 'MINUS':
                self.tokens.append(Token(TokenType.MINUS, value, pos))
            elif kind == 'MUL':
                self.tokens.append(Token(TokenType.MUL, value, pos))
            elif kind == 'DIV':
                self.tokens.append(Token(TokenType.DIV, value, pos))
            elif kind == 'ASSIGN':
                self.tokens.append(Token(TokenType.ASSIGN, value, pos))
            elif kind == 'DOT':
                self.tokens.append(Token(TokenType.DOT, value, pos))
            elif kind == 'LPAREN':
                self.tokens.append(Token(TokenType.LPAREN, value, pos))
            elif kind == 'RPAREN':
                self.tokens.append(Token(TokenType.RPAREN, value, pos))
            elif kind == 'SEMICOLON':
                self.tokens.append(Token(TokenType.SEMICOLON, value, pos))
            elif kind == 'SKIP':
                continue
            else:
                raise LexicalError(f"Unexpected symbol '{value}' at position {pos}")

    def peek(self):
        return self.tokens[self.index]

    def next(self):
        tok = self.tokens[self.index]
        self.index += 1
        return tok
