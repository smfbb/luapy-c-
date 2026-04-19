import re
from tokens import TokenType

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)})"

class Lexer:
    # Regras do Lua 2.5 (simplificadas)
    RULES = [
        (r'--.*', None),                         # Comentários
        (r'\s+', None),                          # Espaços em branco
        (r'\b(local)\b', TokenType.LOCAL),
        (r'\b(while)\b', TokenType.WHILE),
        (r'\b(do)\b', TokenType.DO),
        (r'\b(if)\b', TokenType.IF),
        (r'\b(else)\b', TokenType.ELSE),
        (r'\b(then)\b', TokenType.THEN),
        (r'\b(end)\b', TokenType.END),
        (r'\b(while)\b', TokenType.WHILE),
        (r'\b(do)\b', TokenType.DO),
        (r'\band\b', TokenType.AND),
        (r'\bor\b', TokenType.OR),
        (r'\btrue\b', TokenType.TRUE),
        (r'\bfalse\b', TokenType.FALSE),
        (r'\b(function)\b', TokenType.FUNCTION),
        (r'\breturn\b', TokenType.RETURN),
        (r'\[', TokenType.LBRACKET),
        (r'\]', TokenType.RBRACKET),
        (r'\{', TokenType.LBRACE),
        (r'\}', TokenType.RBRACE),
        (r',', TokenType.COMMA),
        (r'==', TokenType.EQ),
        (r'<=', TokenType.LE),
        (r'!=', TokenType.NE),
        (r'>=', TokenType.GE),
        (r'=', TokenType.ASSIGN),
        (r'<', TokenType.LT),
        (r'>', TokenType.GT),
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MUL),
        (r'/', TokenType.DIV),
        (r'\(', TokenType.LPAREN),
        (r'\)', TokenType.RPAREN),
        (r'\d+(\.\d+)?', TokenType.NUMBER),      # Números
        (r'\"(.*?)\"', TokenType.STRING),        # Strings com aspas duplas
        (r'\'(.*?)\'', TokenType.STRING),        # Strings com aspas simples
        (r'[a-zA-Z_]\w*', TokenType.IDENTIFIER), # Variáveis
    ]

    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        position = 0
        while position < len(self.source_code):
            match = None
            for pattern, token_type in self.RULES:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, position)
                if match:
                    value = match.group(0)
                    if token_type == TokenType.NUMBER:
                        value = float(value) if '.' in value else int(value)
                    elif token_type == TokenType.STRING:
                        value = match.group(1) # Remove as aspas
                    
                    if token_type is not None: # Ignora comentários e espaços
                        self.tokens.append(Token(token_type, value))
                    
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Erro Léxico: Caractere inesperado '{self.source_code[position]}'")
        self.tokens.append(Token(TokenType.EOF, None))