from lexer import Lexer
from parser import Parser
from evaluator import Environment, Evaluator

def rodar_lua(codigo_fonte):
    print(f"--- Executando Código ---\n{codigo_fonte}\n-------------------------")
    
    # 1. Lexer (Gera tokens)
    lexer = Lexer(codigo_fonte)
    
    # 2. Parser (Gera a Árvore AST)
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    
    # 3. Evaluator (Executa a Árvore)
    env = Environment()
    evaluator = Evaluator(env)
    evaluator.evaluate(ast)

if __name__ == "__main__":
    # Testando um script Lua 2.5 puro
    codigo_teste = """
        function calcular_area(lado)
            local area = lado * lado
            return area
        end

        function verificar_maioridade(idade)
            if idade >= 18 then
                return "Maior de idade"
            end
            return "Menor de idade"
        end

        local minha_area = calcular_area(5)
        print("A area do quadrado eh: " + str(minha_area))

        local status = verificar_maioridade(20)
        print("Status do usuario: " + status)
    """
    
    rodar_lua(codigo_teste)