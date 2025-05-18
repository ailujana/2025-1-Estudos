from lark import Lark, Transformer, Tree, v_args # type: ignore
from rich import print  # type: ignore # comente isso se quebrar, ou pip install rich

grammar = r"""
?start   : prog  # Ponto de entrada da gramática

# Um programa pode ser:
# - Apenas uma comparação
# - Ou um corpo com declarações seguido de comparação
?prog    : cmp
         | body ";" cmp

# Corpo (body) pode ser:
# - Uma única declaração
# - Ou várias declarações separadas por ';'
?body    : decl
         | body ";" decl

# Declaração de variável: x = expressão
decl     : DEF "=" cmp

# Comparações entre expressões
?cmp     : expr ">" expr   -> gt
         | expr "<" expr   -> lt
         | expr ">=" expr  -> ge
         | expr "<=" expr  -> le
         | expr "=" expr   -> eq
         | expr "=/=" expr -> ne
         | expr            # fallback sem comparação

# Expressões com soma e subtração
?expr    : expr "+" term   -> add
         | expr "-" term   -> sub
         | term

# Termos com multiplicação e divisão (suporta × e ÷ também)
?term    : term ("*"|"×") pow   -> mul
         | term ("/"|"÷") pow   -> div 
         | pow

# Potenciação com ^ ou emoji 🫠
?pow     : atom ("^" | "🫠") pow
         | atom

# Átomos são números, variáveis ou expressões entre parênteses
?atom    : NUMBER 
         | VAR
         | "(" cmp ")"

# Tokens para variáveis e números
VAR      : "x" | "y" | "z"
DEF      : "x" | "y" | "z"
NUMBER   : DIGIT+
DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

# Ignora espaços e quebras de linha
%ignore " " | "\n"
"""


# Transformer responsável por interpretar e avaliar a árvore sintática
@v_args(inline=True)  # Faz com que os métodos recebam argumentos diretamente
class CalcTransformer(Transformer):  
    # Importa operadores matemáticos e lógicos
    from operator import pow, add, sub, mul, truediv as div
    from operator import eq, ne, lt, le, gt, ge

    def __init__(self, visit_tokens = True):
        super().__init__(visit_tokens)
        self.env = {}  # Ambiente de variáveis (como uma memória simples)
    
    def decl(self, name, value):
        # Define uma variável no ambiente
        self.env[name] = value

    def body(self, decl1, decl2):
        # Este método existe por estrutura, mas o corpo não precisa retornar nada
        ...

    def prog(self, body, cmp):
        # Em um programa com declarações e uma expressão final, retorna o valor da comparação
        return cmp

    def NUMBER(self, token):
        # Converte tokens de número para inteiro
        return int(token)

    def DEF(self, token):
        # Retorna o nome da variável (para uso em declarações)
        return str(token)

    def VAR(self, token):
        # Acessa o valor de uma variável previamente declarada
        name = str(token)
        return self.env[name]

    
transformer = CalcTransformer()
parser = Lark(grammar)

def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)

if __name__ == "__main__":
    src = "x = 2; y = x + 1; x * y"  # Código de exemplo: define x e y, depois calcula x * y

    print("src:", src)  # Mostra o código fonte de entrada
    tree = parser.parse(src)  # Gera árvore sintática a partir do código
    tree_ = transformer.transform(tree)  # Avalia e transforma a árvore sintática

    print("-" * 10)
    pprint(tree_)  # Exibe o resultado da expressão final (6 neste caso)
