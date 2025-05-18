from lark import Lark, Transformer, Tree # type: ignore

grammar = r"""
?start   : list 

list     : "["  "]"
         | "[" items "]"

items    : item            -> single
         | item "," items
         
?item    : math
         | list
         
?math    : atom OP math  
         | atom
         
?atom    : NUMBER
         | list

OP       : "+" | "*" | "-" | "/" | "**"

DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
NUMBER   : DIGIT+

%ignore " " | "\n"
""" 

# Transformer que transforma a árvore sintática em estruturas Python reais
class ListTransformer(Transformer):
    def list(self, children):
        # Retorna o conteúdo da lista, que está dentro dos colchetes
        return children[0]

    def math(self, children):
        # Avalia a expressão matemática com eval (ex: 1 + 2, 3 * 4, etc.)
        x, op, y  = children
        return eval(f"{x} {op} {y}")

    def single(self, children):
        # Para o caso de lista com apenas um item
        return children

    def items(self, children):
        # Junta o primeiro item (head) com o restante (tail)
        head, tail = children
        if isinstance(children[1], list):
            return [head, *tail]
        return children  # Fallback se não for uma lista (por segurança)

    def NUMBER(self, token):
        # Converte o número tokenizado para inteiro
        return int(token)


transformer = ListTransformer()
parser = Lark(grammar)

def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)
        
# Bloco principal de execução do script
if __name__ == "__main__":
    src = "[[1] + [2, 3]]"  # Exemplo de entrada: soma entre 1 e 2 (3 ignorado no exemplo)

    print("src:", src)  # Imprime a entrada original
    tree = parser.parse(src)  # Gera árvore sintática com base na entrada
    tree_ = transformer.transform(tree)  # Transforma a árvore em estrutura Python

    print("-" * 10)
    pprint(tree_)  # Exibe o resultado final (deve ser 3)
