from lark import Lark, Transformer, Tree  # type: ignore
# Importa a biblioteca Lark:
# - Lark: para criar o parser com base em uma gramática
# - Transformer: para transformar a árvore sintática em estruturas Python
# - Tree: representa a árvore de sintaxe gerada (não usada diretamente aqui)

# Define a gramática EBNF (Extended Backus–Naur Form)
grammar = r"""
?start   : list  # Regra inicial da gramática: um programa começa com uma 'list'

# A produção 'list' define uma lista:
# - Pode ser vazia: []
# - Ou conter uma sequência de itens: [ items ]
list     : "["  "]"
         | "[" items "]"

# A produção 'items' define:
# - Um único item (regra 'single')
# - Ou um item seguido de vírgula e mais itens (forma recursiva)
items    : item            -> single
         | item "," items

# Um 'item' pode ser:
# - Uma expressão matemática (math)
# - Ou uma lista (permite listas aninhadas)
?item    : math
         | list

# Uma expressão matemática pode ser:
# - Um átomo seguido de um operador e outra expressão (recursão à direita)
# - Ou apenas um átomo
?math    : atom OP math  
         | atom

# Um átomo pode ser:
# - Um número (literal)
# - Ou uma lista (novamente, permitindo recursividade)
?atom    : NUMBER
         | list

# Os operadores suportados são: +, -, *, /, **
OP       : "+" | "*" | "-" | "/" | "**"

# Definição de número como sequência de dígitos
DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
NUMBER   : DIGIT+

# Espaços e quebras de linha são ignorados na análise léxica
%ignore " " | "\n"
""" 

# Define um Transformer que percorre e transforma a árvore gerada pelo parser
class ListTransformer(Transformer):
    def list(self, children):
        # A regra 'list' retorna os filhos diretamente
        # Se for lista com elementos, retorna o conteúdo da lista
        return children[0]

    def math(self, children):
        # A regra 'math' avalia expressões matemáticas simples usando eval
        # Ex: [[1] + [2]] vira 1 + 2 = 3
        x, op, y = children
        return eval(f"{x} {op} {y}")

    def single(self, children):
        # Para listas com um único item, retorna o item diretamente
        return children

    def items(self, children):
        # Trata a construção recursiva de listas com múltiplos itens
        head, tail = children
        if isinstance(children[1], list):
            return [head, *tail]  # Junta cabeça e cauda se a cauda for lista
        return children  # Caso contrário, retorna os itens como estão

    def NUMBER(self, token):
        # Converte tokens do tipo NUMBER (string) para inteiro
        return int(token)

# Instancia o transformer e o parser com a gramática fornecida
transformer = ListTransformer()
parser = Lark(grammar)

# Função auxiliar que imprime a árvore sintática formatada ou o resultado final
def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())  # Imprime árvore sintática com indentação
    else:
        print(obj)  # Imprime resultado final da transformação

# Bloco principal do programa
if __name__ == "__main__":
    src = "[[1] + [2, 3]]"  # Entrada de exemplo: lista com uma operação de soma

    print("src:", src)  # Mostra o texto de entrada
    tree = parser.parse(src)  # Analisa sintaticamente a entrada e gera árvore
    tree_ = transformer.transform(tree)  # Transforma árvore em estrutura Python

    print("-" * 10)
    pprint(tree_)  # Imprime o resultado da transformação (ex: 3)
