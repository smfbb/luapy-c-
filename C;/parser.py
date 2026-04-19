from tokens import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def consume(self, expected_type):
        if self.current().type == expected_type:
            token = self.current()
            self.pos += 1
            return token
        raise SyntaxError(f"Erro Sintático: Esperava {expected_type.name}, mas encontrou {self.current().type.name} na posição {self.pos}")

    def parse(self):
        statements = []
        while self.current().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return BlockNode(statements)

    def parse_statement(self):
        # var x = 10;
        if self.current().type == TokenType.VAR:
            self.consume(TokenType.VAR)
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            value = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            return AssignNode(name, value, is_local=True)
            
        # if (condicao) { corpo }
        elif self.current().type == TokenType.IF:
            self.consume(TokenType.IF)
            self.consume(TokenType.LPAREN)
            condition = self.parse_expression()
            self.consume(TokenType.RPAREN)
            
            self.consume(TokenType.LBRACE)
            then_body = []
            while self.current().type != TokenType.RBRACE:
                then_body.append(self.parse_statement())
            self.consume(TokenType.RBRACE)
            
            else_body = None
            if self.current().type == TokenType.ELSE:
                self.consume(TokenType.ELSE)
                self.consume(TokenType.LBRACE)
                else_body_stmts = []
                while self.current().type != TokenType.RBRACE:
                    else_body_stmts.append(self.parse_statement())
                self.consume(TokenType.RBRACE)
                else_body = BlockNode(else_body_stmts)
                
            return IfNode(condition, BlockNode(then_body), else_body)

        # while (condicao) { corpo }
        elif self.current().type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            self.consume(TokenType.LPAREN)
            condition = self.parse_expression()
            self.consume(TokenType.RPAREN)
            
            self.consume(TokenType.LBRACE)
            body_stmts = []
            while self.current().type != TokenType.RBRACE:
                body_stmts.append(self.parse_statement())
            self.consume(TokenType.RBRACE)
            return WhileNode(condition, BlockNode(body_stmts))

        # function nome(a, b) { corpo }
        elif self.current().type == TokenType.FUNCTION:
            self.consume(TokenType.FUNCTION)
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.LPAREN)
            params = []
            if self.current().type == TokenType.IDENTIFIER:
                params.append(self.consume(TokenType.IDENTIFIER).value)
                while self.current().type == TokenType.COMMA:
                    self.consume(TokenType.COMMA)
                    params.append(self.consume(TokenType.IDENTIFIER).value)
            self.consume(TokenType.RPAREN)
            
            self.consume(TokenType.LBRACE)
            body_stmts = []
            while self.current().type != TokenType.RBRACE:
                body_stmts.append(self.parse_statement())
            self.consume(TokenType.RBRACE)
            return FunctionDefNode(name, params, BlockNode(body_stmts))

        # return expressao;
        elif self.current().type == TokenType.RETURN:
            self.consume(TokenType.RETURN)
            value = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
            return ReturnNode(value)

        # Atribuição Global ou Chamada de Função isolada (print();)
        elif self.current().type == TokenType.IDENTIFIER:
            node = self.parse_primary()
            if self.current().type == TokenType.ASSIGN:
                self.consume(TokenType.ASSIGN)
                value = self.parse_expression()
                self.consume(TokenType.SEMICOLON)
                return AssignNode(node.name, value)
            
            self.consume(TokenType.SEMICOLON)
            return node
            
        raise SyntaxError(f"Instrução inválida: {self.current().type.name}")

    def parse_expression(self):
        # Mantendo a Matemática Linear do LuaPy (Esquerda para Direita)
        left = self.parse_primary()
        operadores = (TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV,
                      TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT, 
                      TokenType.LE, TokenType.GE, TokenType.AND, TokenType.OR)
        
        while self.current().type in operadores:
            op = self.current().type
            self.consume(op)
            right = self.parse_primary()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_primary(self):
        token = self.current()
        if token.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER); return NumberNode(token.value)
        elif token.type == TokenType.STRING:
            self.consume(TokenType.STRING); return StringNode(token.value)
        elif token.type == TokenType.TRUE:
            self.consume(TokenType.TRUE); return BooleanNode(True)
        elif token.type == TokenType.FALSE:
            self.consume(TokenType.FALSE); return BooleanNode(False)
        elif token.type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER).value
            # Chamada de função: nome(args)
            if self.current().type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                args = []
                if self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current().type == TokenType.COMMA:
                        self.consume(TokenType.COMMA)
                        args.append(self.parse_expression())
                self.consume(TokenType.RPAREN)
                node = CallNode(name, args)
            else:
                node = IdentifierNode(name)
            
            # Acesso a lista: lista[0]
            while self.current().type == TokenType.LBRACKET:
                self.consume(TokenType.LBRACKET)
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                node = TableAccessNode(node, index)
            return node
        elif token.type == TokenType.LBRACE: # Tabelas/Listas: {1, 2}
            self.consume(TokenType.LBRACE)
            items = []
            while self.current().type != TokenType.RBRACE:
                items.append(self.parse_expression())
                if self.current().type == TokenType.COMMA: self.consume(TokenType.COMMA)
            self.consume(TokenType.RBRACE)
            return TableNode(items)
        
        raise SyntaxError(f"Expressão inesperada: {token.type.name}")