import re
from tokens import TokenType

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)})"

class Lexer:
    # Regras do C; (Inspirado em C com a base do LuaPy)
    RULES = [
        (r'//.*', None),                         # Comentários de linha única
        (r'\s+', None),                          # Espaços e quebras de linha
        (r'\bvar\b', TokenType.VAR),
        (r'\bif\b', TokenType.IF),
        (r'\belse\b', TokenType.ELSE),
        (r'\bwhile\b', TokenType.WHILE),
        (r'\bfunction\b', TokenType.FUNCTION),
        (r'\breturn\b', TokenType.RETURN),
        (r'\band\b', TokenType.AND),
        (r'\bor\b', TokenType.OR),
        (r'\btrue\b', TokenType.TRUE),
        (r'\bfalse\b', TokenType.FALSE),
        
        # Símbolos de dois caracteres (precisam vir antes dos de um)
        (r'==', TokenType.EQ),
        (r'!=', TokenType.NE),
        (r'<=', TokenType.LE),
        (r'>=', TokenType.GE),
        
        # Símbolos de um caractere
        (r'=', TokenType.ASSIGN),
        (r';', TokenType.SEMICOLON),
        (r'\{', TokenType.LBRACE),
        (r'\}', TokenType.RBRACE),
        (r'\(', TokenType.LPAREN),
        (r'\)', TokenType.RPAREN),
        (r'\[', TokenType.LBRACKET),
        (r'\]', TokenType.RBRACKET),
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MUL),
        (r'/', TokenType.DIV),
        (r',', TokenType.COMMA),

        # Literais
        (r'\d+(\.\d+)?', TokenType.NUMBER),
        (r'\"(.*?)\"', TokenType.STRING),
        (r'\'(.*?)\'', TokenType.STRING),
        (r'[a-zA-Z_]\w*', TokenType.IDENTIFIER),
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
                        value = match.group(1)
                    
                    if token_type is not None:
                        self.tokens.append(Token(token_type, value))
                    
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Erro Léxico: Caractere '{self.source_code[position]}' inválido.")
        self.tokens.append(Token(TokenType.EOF, None))