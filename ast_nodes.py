class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, value): self.value = value

class StringNode(ASTNode):
    def __init__(self, value): self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name): self.name = name

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class AssignNode(ASTNode):
    def __init__(self, name, value, is_local=False):
        self.name = name
        self.value = value
        self.is_local = is_local

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name     # Nome da função
        self.params = params # Lista de nomes de argumentos (ex: ["a", "b"])
        self.body = body     # O BlockNode com o código

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value # A expressão que será retornada

class TableNode(ASTNode):
    def __init__(self, fields): self.fields = fields

class TableAccessNode(ASTNode):
    def __init__(self, table_expr, key_expr):
        self.table_expr, self.key_expr = table_expr, key_expr
        
class TableAssignNode(ASTNode):
    def __init__(self, table_expr, key_expr, value_expr):
        self.table_expr, self.key_expr, self.value_expr = table_expr, key_expr, value_expr

class IfNode(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body # O novo "Plano B"

class CallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements