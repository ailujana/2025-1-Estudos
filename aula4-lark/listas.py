# Use python3 -m pip install lark-parser
# para instalar o Lark

# O arquivo descreve uma linguagem que aceita listas (potencialmente aninhadas)
# de elementos x. Aqui ilustramos um uso muito simples da biblioteca Lark.
# Veja mais em https://github.com/lark-parser/lark

import lark  # type: ignore # Importa a biblioteca Lark, usada para criar parsers com gramática formal

# Definição da gramática como uma string multilinha (em formato EBNF)
grammar = r"""
start : list  # A regra inicial da gramática é uma lista

# Uma lista pode ser:
# - uma lista vazia: []
# - ou uma lista com elementos (com ou sem vírgula final): [elementos,]
list : "["  "]"
     | "[" elementos virgula "]"

# A produção 'elementos' define:
# - um único dado
# - ou um dado seguido por vírgula e mais elementos (forma recursiva)
elementos : dado
          | dado "," elementos

# Um 'dado' pode ser:
# - o literal "x"
# - ou uma nova lista (permitindo aninhamento de listas)
dado : "x"
     | list

# A vírgula final após os elementos é opcional:
# - pode ser uma vírgula real
# - ou pode ser ausente (epsilon)
virgula : "," 
        | epsilon

# A produção epsilon representa o símbolo vazio (nada)
epsilon :
"""

# Cria um parser Lark com base na gramática definida
parser = lark.Lark(grammar)

# Faz o parsing da string de entrada '[x,[x,]]'
# Essa string representa uma lista com dois elementos:
# - um 'x'
# - uma lista aninhada contendo um 'x' (seguido por vírgula final opcional)
tree = parser.parse("[x,[x,]]")

# Exibe a árvore sintática de forma indentada e legível
print(tree.pretty())
