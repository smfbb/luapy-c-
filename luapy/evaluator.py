from tokens import TokenType
from ast_nodes import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self):
        self.variables = {
            "true": True,
            "false": False
        }
        # Funções nativas que vêm embutidas no nosso Lua
        self.builtins = {
            "print": print,
            "int": lambda x: int(x),
            "str": lambda x: str(x),
            "float": lambda x: float(x),
            "type": lambda x: type(x).__name__ # Útil para depurar!
        }

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if name in self.builtins:
            return self.builtins[name]
        return None # No Lua, variável não definida é nil (None)

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
            
        elif isinstance(node, IfNode):
            condition = self.evaluate(node.condition)
            if condition:
                self.evaluate(node.then_body)
            elif node.else_body: # Se a condição foi falsa E tem um else...
                self.evaluate(node.else_body)
        
        elif isinstance(node, WhileNode):
            # Enquanto a condição avaliada for verdadeira (em Lua, diferente de None/False)
            while self.evaluate(node.condition):
                self.evaluate(node.body)

        elif isinstance(node, ReturnNode):
            value = self.evaluate(node.value)
            raise ReturnException(value) # Lança o valor para cima
        
        elif isinstance(node, FunctionDefNode):
            def lua_func(*args):
                local_env = Environment()
                local_env.variables = self.env.variables.copy()
                for name, val in zip(node.params, args):
                    local_env.set(name, val)
                
                new_evaluator = Evaluator(local_env)
                try:
                    new_evaluator.evaluate(node.body)
                except ReturnException as e:
                    return e.value # Captura o valor e retorna para o Python
                return None
            
            self.env.set(node.name, lua_func)
        
        elif isinstance(node, TableNode):
            return {i+1: self.evaluate(val) for i, val in enumerate(node.fields)}
            
        elif isinstance(node, TableAccessNode):
            table = self.evaluate(node.table_expr)
            key = self.evaluate(node.key_expr)
            return table.get(key)

        elif isinstance(node, TableAssignNode):
            table = self.evaluate(node.table_expr)
            key = self.evaluate(node.key_expr)
            table[key] = self.evaluate(node.value_expr)     
        elif isinstance(node, CallNode):
            func = self.env.get(node.name)
            if callable(func):
                args = [self.evaluate(arg) for arg in node.args]
                return func(*args)
            else:
                raise RuntimeError(f"Tentativa de chamar um valor não-função: {node.name}")

        elif isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            # Lógica simples de fallbacks matemáticos
            if node.op == TokenType.PLUS: return left + right
            if node.op == TokenType.MINUS: return left - right
            if node.op == TokenType.MUL: return left * right
            if node.op == TokenType.DIV: return left / right
            if node.op == TokenType.LT: return left < right
            if node.op == TokenType.GT: return left > right
            if node.op == TokenType.EQ: return left == right
            if node.op == TokenType.LE: return left <= right
            if node.op == TokenType.GE: return left >= right
            if node.op == TokenType.NE: return left != right
            if node.op == TokenType.AND: return left and right
            if node.op == TokenType.OR: return left or right

        elif isinstance(node, NumberNode) or isinstance(node, StringNode):
            return node.value
            
        elif isinstance(node, IdentifierNode):
            return self.env.get(node.name)