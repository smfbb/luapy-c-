from tokens import TokenType
from ast_nodes import *

class ReturnException(Exception):
    def __init__(self, value): self.value = value

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
        self.builtins = {
            "print": print,
            "str": str,
            "int": int,
            "float": float
        }

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables: return self.variables[name]
        if name in self.builtins: return self.builtins[name]
        if self.parent: return self.parent.get(name)
        return None

class Evaluator:
    def __init__(self, env):
        self.env = env

    def evaluate(self, node):
        if isinstance(node, BlockNode):
            for statement in node.statements:
                self.evaluate(statement)

        elif isinstance(node, AssignNode):
            value = self.evaluate(node.value)
            self.env.set(node.name, value)

        elif isinstance(node, NumberNode) or isinstance(node, StringNode) or isinstance(node, BooleanNode):
            return node.value

        elif isinstance(node, IdentifierNode):
            return self.env.get(node.name)

        elif isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == TokenType.PLUS: return left + right
            if node.op == TokenType.MINUS: return left - right
            if node.op == TokenType.MUL: return left * right
            if node.op == TokenType.DIV: return left / right
            if node.op == TokenType.EQ: return left == right
            if node.op == TokenType.NE: return left != right
            if node.op == TokenType.GT: return left > right
            if node.op == TokenType.LT: return left < right
            if node.op == TokenType.AND: return left and right
            if node.op == TokenType.OR: return left or right

        elif isinstance(node, IfNode):
            if self.evaluate(node.condition):
                self.evaluate(node.then_body)
            elif node.else_body:
                self.evaluate(node.else_body)

        elif isinstance(node, WhileNode):
            while self.evaluate(node.condition):
                self.evaluate(node.body)

        elif isinstance(node, FunctionDefNode):
            def func_wrapper(*args):
                new_env = Environment(self.env)
                for param, arg in zip(node.params, args):
                    new_env.set(param, arg)
                evaluator = Evaluator(new_env)
                try:
                    evaluator.evaluate(node.body)
                except ReturnException as e:
                    return e.value
                return None
            self.env.set(node.name, func_wrapper)

        elif isinstance(node, ReturnNode):
            raise ReturnException(self.evaluate(node.value))

        elif isinstance(node, CallNode):
            func = self.env.get(node.name)
            args = [self.evaluate(arg) for arg in node.args]
            return func(*args)

        elif isinstance(node, TableNode):
            return [self.evaluate(item) for item in node.fields]

        elif isinstance(node, TableAccessNode):
            table = self.evaluate(node.table_expr)
            index = self.evaluate(node.key_expr)
            # Ajuste para índice 1-based (como no Lua original)
            return table[int(index) - 1]