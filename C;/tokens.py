from enum import Enum, auto

class TokenType(Enum):
    # Palavras-chave estilo C
    VAR = auto()        # var (antigo local)
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FUNCTION = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()

    # Símbolos Estruturais
    ASSIGN = auto()      # =
    SEMICOLON = auto()   # ;
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,

    # Operadores de Comparação e Lógica
    EQ = auto()          # ==
    NE = auto()          # !=
    LT = auto()          # <
    GT = auto()          # >
    LE = auto()          # <=
    GE = auto()          # >=
    AND = auto()         # and
    OR = auto()          # or

    # Operadores Matemáticos
    PLUS = auto()        # +
    MINUS = auto()       # -
    MUL = auto()         # *
    DIV = auto()         # /

    # Tipos de Dados
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    EOF = auto()         # End Of File