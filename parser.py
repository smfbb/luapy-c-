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
        raise SyntaxError(f"Erro Sintático: Esperava {expected_type.name}, encontrou {self.current().type.name}")

    def parse(self):
        statements = []
        while self.current().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return BlockNode(statements)

    def parse_statement(self):
        if self.current().type == TokenType.LOCAL:
            self.consume(TokenType.LOCAL)
            name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            value = self.parse_expression()
            return AssignNode(name, value, is_local=True)
            
        elif self.current().type == TokenType.IDENTIFIER:
            # Em vez de ler o nome manualmente, usamos o parse_primary
            # Ele já sabe ler o nome E verificar se tem [ ] depois!
            node = self.parse_primary()

            # Se depois de ler o "alvo" vier um '=', é atribuição
            if self.current().type == TokenType.ASSIGN:
                self.consume(TokenType.ASSIGN)
                value = self.parse_expression()
                
                if isinstance(node, IdentifierNode):
                    return AssignNode(node.name, value)
                elif isinstance(node, TableAccessNode):
                    return TableAssignNode(node.table, node.key, value)
            
            # Se não for '=', o parse_primary já resolveu se era print(x) ou lista[1]
            return node

        elif self.current().type == TokenType.IF:
            self.consume(TokenType.IF)
            condition = self.parse_expression()
            self.consume(TokenType.THEN)
                            
            then_body = []
            else_body = None
                            
            # Lê o que está no THEN até achar ELSE ou END
            while self.current().type not in (TokenType.END, TokenType.ELSE):
                then_body.append(self.parse_statement())
                            
            # Se parou porque achou um ELSE
            if self.current().type == TokenType.ELSE:
                self.consume(TokenType.ELSE)
                else_body = []
                while self.current().type != TokenType.END:
                    else_body.append(self.parse_statement())
                            
            self.consume(TokenType.END)
            return IfNode(condition, BlockNode(then_body), BlockNode(else_body) if else_body else None)
        
        elif self.current().type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            condition = self.parse_expression() # Lê a condição (ex: n1 < 10)
            self.consume(TokenType.DO)          # Espera a palavra 'do'
            
            body = []
            # Lê tudo até encontrar o 'end'
            while self.current().type != TokenType.END:
                body.append(self.parse_statement())
            
            self.consume(TokenType.END) # Fecha o loop
            return WhileNode(condition, BlockNode(body))
        
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
            
            body_stmts = []
            while self.current().type != TokenType.END:
                body_stmts.append(self.parse_statement())
            self.consume(TokenType.END)
            
            return FunctionDefNode(name, params, BlockNode(body_stmts))
        
        if self.current().type == TokenType.RETURN:
            self.consume(TokenType.RETURN)
            value = self.parse_expression()
            return ReturnNode(value)

        raise SyntaxError(f"Comando não reconhecido no token: {self.current()}")

        expr = self.parse_primary()
        if self.current().type == TokenType.ASSIGN:
            self.consume(TokenType.ASSIGN)
            val = self.parse_expression()
            if isinstance(expr, IdentifierNode): return AssignNode(expr.name, val)
            if isinstance(expr, TableAccessNode): return TableAssignNode(expr.table_expr, expr.key_expr, val)
        return expr

    def parse_expression(self):
        # Primeiro, resolvemos a parte lógica/comparação
        left = self.parse_arithmetic()
        logicos = (TokenType.AND, TokenType.OR, TokenType.LT, TokenType.GT, 
                   TokenType.EQ, TokenType.LE, TokenType.GE, TokenType.NE)
        
        while self.current().type in logicos:
            op = self.current().type
            self.consume(op)
            right = self.parse_arithmetic()
            left = BinaryOpNode(left, op, right)
        return left
    
    def parse_arithmetic(self):
        # Depois, resolvemos a parte matemática pura
        left = self.parse_primary()
        matematica = (TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV)
        
        while self.current().type in matematica:
            op = self.current().type
            self.consume(op)
            right = self.parse_primary()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_primary(self):
            token = self.current()
            node = None
            if token.type == TokenType.NUMBER:
                self.consume(TokenType.NUMBER); node = NumberNode(token.value)
            elif token.type == TokenType.TRUE:
                self.consume(TokenType.TRUE); node = NumberNode(True) # Usamos o True do Python
            elif token.type == TokenType.FALSE:
                self.consume(TokenType.FALSE); node = NumberNode(False) # Usamos o False do Python
            elif token.type == TokenType.STRING:
                self.consume(TokenType.STRING); node = StringNode(token.value)
            elif token.type == TokenType.IDENTIFIER:
                name = self.consume(TokenType.IDENTIFIER).value
                if self.current().type == TokenType.LPAREN: # Chamada
                    self.consume(TokenType.LPAREN)
                    args = []
                    if self.current().type != TokenType.RPAREN:
                        args.append(self.parse_expression())
                        while self.current().type == TokenType.COMMA:
                            self.consume(TokenType.COMMA); args.append(self.parse_expression())
                    self.consume(TokenType.RPAREN)
                    node = CallNode(name, args)
                else:
                    node = IdentifierNode(name)
            elif token.type == TokenType.LBRACE: # {1, 2}
                self.consume(TokenType.LBRACE)
                items = []
                while self.current().type != TokenType.RBRACE:
                    items.append(self.parse_expression())
                    if self.current().type == TokenType.COMMA: self.consume(TokenType.COMMA)
                self.consume(TokenType.RBRACE)
                node = TableNode(items)
            
            # Pós-processamento para acesso: lista[1]
            while self.current().type == TokenType.LBRACKET:
                self.consume(TokenType.LBRACKET)
                key = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                node = TableAccessNode(node, key)
                
            return node