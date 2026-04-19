class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, value): self.value = value

class StringNode(ASTNode):
    def __init__(self, value): self.value = value

class BooleanNode(ASTNode):
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

class BlockNode(ASTNode):
    def __init__(self, statements): self.statements = statements

class IfNode(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value): self.value = value

class CallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class TableNode(ASTNode):
    def __init__(self, fields): self.fields = fields

class TableAccessNode(ASTNode):
    def __init__(self, table_expr, key_expr):
        self.table_expr = table_expr
        self.key_expr = key_expr