from token import TokenType


class SyntaxError(Exception):
    pass


class SemanticError(Exception):
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.symtab = {}

    def eat(self, ttype):
        if self.lexer.peek().type == ttype:
            return self.lexer.next()
        raise SyntaxError(f"Expected {ttype} at position {self.lexer.peek().pos}")

    def parse(self):
        self.program()
        self.eat(TokenType.EOF)
        return self.symtab

    # <Program> ::= <StmtList>
    def program(self):
        self.stmt_list()

    # <StmtList> ::= <Stmt> | <Stmt> <StmtList>
    def stmt_list(self):
        self.stmt()

        if self.lexer.peek().type == TokenType.ID:
            self.stmt_list()

    def stmt(self):
        path = self.field_path()

        self.eat(TokenType.ASSIGN)
        value = self.expr()
        self.eat(TokenType.SEMICOLON)
        self.assign(path, value)

    def field_path(self):
        tok = self.eat(TokenType.ID)
        path = [tok.value]
        while self.lexer.peek().type == TokenType.DOT:
            self.eat(TokenType.DOT)
            path.append(self.eat(TokenType.ID).value)
        return path

    # <Expr> ::= <LeadMinusOpt> <Sum>
    def expr(self):
        sign = 1
        if self.lexer.peek().type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            sign = -1
        return sign * self.sum()

    # <Sum> ::= <Prod> <SumTail>
    def sum(self):
        value = self.prod()

        while self.lexer.peek().type in (TokenType.PLUS, TokenType.MINUS):
            if self.lexer.peek().type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                value += self.prod()
            else:
                self.eat(TokenType.MINUS)
                value -= self.prod()
        return value

    # <Prod> ::= <Primary> <ProdTail>
    def prod(self):
        value = self.primary()

        while self.lexer.peek().type in (TokenType.MUL, TokenType.DIV):
            if self.lexer.peek().type == TokenType.MUL:
                self.eat(TokenType.MUL)
                value *= self.primary()
            else:
                self.eat(TokenType.DIV)
                denom = self.primary()
                if denom == 0:
                    raise SemanticError("Division by zero")
                value /= denom
        return value

    # <Primary>
    def primary(self):
        tok = self.lexer.peek()

        if tok.type == TokenType.NUMBER:
            return self.eat(TokenType.NUMBER).value
        if tok.type == TokenType.ID:
            return self.resolve(self.field_path())
        if tok.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            val = self.expr()
            self.eat(TokenType.RPAREN)
            return val
        raise SyntaxError(f"Unexpected token {tok} at position {tok.pos}")

    def assign(self, path, value):
        cur = self.symtab

        for p in path[:-1]:
            cur = cur.setdefault(p, {})
        cur[path[-1]] = value

    def resolve(self, path):
        cur = self.symtab

        for p in path:
            if p not in cur:
                raise SemanticError(f"Uninitialized identifier {'.'.join(path)}")
            cur = cur[p]
        if isinstance(cur, dict):
            raise SemanticError(f"Identifier {'.'.join(path)} is not a value")
        return cur
