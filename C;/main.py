from lexer import Lexer
from parser import Parser
from evaluator import Environment, Evaluator

def rodar_c_ponto_virgula(codigo):
    print("--- Iniciando Interpretador C; ---")
    try:
        lexer = Lexer(codigo)
        parser = Parser(lexer.tokens)
        ast = parser.parse()
        env = Environment()
        evaluator = Evaluator(env)
        evaluator.evaluate(ast)
    except Exception as e:
        print(f"\n[ERRO]: {e}")
    print("\n--- Execução Concluída ---")

if __name__ == "__main__":
    script_teste = """
        // Declaração de variáveis estilo C
        var nome = "C;";
        var idade = 25;

        function saudar(n) {
            print("Ola do " + n);
            return true;
        }

        if (idade >= 18) {
            var resultado = saudar(nome);
            print("Status de saudar: " + str(resultado));
        }

        var contador = 1;
        while (contador <= 3) {
            print("Iteracao: " + str(contador));
            contador = contador + 1;
        }

        var lista = {10, 20, 30};
        print("Item 2 da lista: " + str(lista[2]));
    """
    rodar_c_ponto_virgula(script_teste)