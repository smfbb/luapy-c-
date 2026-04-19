from enum import Enum, auto

class TokenType(Enum):
    # Palavras-chave
    LOCAL = auto()
    IF = auto()
    ELSE = auto()
    THEN = auto()
    END = auto()
    FUNCTION = auto()
    RETURN = auto()
    WHILE = auto()
    DO = auto()
    AND = auto()
    OR = auto()
    TRUE = auto()
    FALSE = auto()

    # Símbolos e Operadores
    ASSIGN = auto()      # =
    EQ = auto()          # ==
    LE = auto()          # <=
    NE = auto()          # !=
    LT = auto()          # <
    GT = auto()          # >
    GE = auto()          # >=
    PLUS = auto()        # +
    MINUS = auto()       # -
    MUL = auto()         # *
    DIV = auto()         # /
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    DOT = auto()


    # Tipos de Dados
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    EOF = auto()         # Fim do arquivo