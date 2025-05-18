from lark import Lark, Transformer, Tree # type: ignore

grammar = r"""
?start   : list

list     : "["  "]"
         | "[" items "]"

?items   : item
         | item "," items
         
?item    : NUMBER
         | list

DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
NUMBER   : DIGIT+

%ignore " " | "\n"
""" 
# Transformer que transforma a árvore sintática Lark em estruturas Python
class ListTransformer(Transformer):
    def list(self, children):
        # Retorna os filhos da lista diretamente (podem ser inteiros ou listas)
        return children

    def items(self, children):
        # Se a lista contiver múltiplos itens, junta a cabeça com a cauda
        head, tail = children
        
        if isinstance(children[1], list):
            return [head, *tail]  # Junta os itens da lista
        return children  # Caso não seja uma lista (fallback)

    def NUMBER(self, token):
        # Converte o número lido (como string) para inteiro
        return int(token)


transformer = ListTransformer()
parser = Lark(grammar)

def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)
        
# Bloco principal do script
if __name__ == "__main__":
    src = "[0,[42], 1,0]"  # Lista com inteiros e uma sublista

    print("src:", src)  # Exibe a string original de entrada
    tree = parser.parse(src)  # Faz parsing da string e gera a árvore sintática
    tree_ = transformer.transform(tree)  # Transforma a árvore em estrutura Python (listas aninhadas)

    print("-" * 10)
    pprint(tree_)  # Exibe o resultado final da transformação
