import re
from rich import print # type: ignore
from typing import cast

exemplos_corretos = ["aAa", "aa bbAB", "aabbbaaa"]
exemplos_incorretos = ["ccc", "a b c", "a c b"]

# Expressão regular que define os tipos de tokens aceitos:
# - WA: sequência de letras 'a' ou 'A' (um ou mais)
# - WB: sequência de letras 'b' ou 'B' (um ou mais)
# - WS: espaços em branco (ignorados)
# - ERROR: qualquer outro caractere não aceito
LEXER = re.compile(
    r"(?P<WA>[aA]+)"      # Grupo nomeado 'WA': um ou mais 'a' ou 'A'
    r"|(?P<WB>[bB]+)"     # Grupo nomeado 'WB': um ou mais 'b' ou 'B'
    r"|(?P<WS>\s+)"       # Grupo nomeado 'WS': espaços (whitespace)
    r"|(?P<ERROR>.)"      # Grupo nomeado 'ERROR': qualquer outro caractere (erro)
)

# Define o tipo Token como uma tupla com dois elementos: nome e valor do token
Token = tuple[str, str]


# Função que realiza a tokenização (análise léxica) de uma string de entrada
def tokenizer(src: str) -> list[Token]:
    result = []  # Lista para armazenar os tokens reconhecidos

    # Itera sobre todas as correspondências da expressão regular no texto
    for m in LEXER.finditer(src):
        kind = cast(str, m.lastgroup)  # Nome do grupo que foi correspondido (WA, WB, WS, ERROR)
        word = m.group(0)              # Texto correspondente

        if kind == "ERROR":
            raise SyntaxError(m)  # Lança erro se encontrou caractere inválido

        if kind == "WS":
            continue  # Ignora espaços

        # Adiciona token à lista
        result.append((kind, word))

    return result  # Retorna lista de tokens válidos


# Bloco principal de execução
if __name__ == "__main__":
    print("[blue bold]CORRETOS")  # Título azul para seções de entradas corretas

    # Testa cada string correta
    for src in exemplos_corretos:
        tokens = tokenizer(src)  # Tokeniza a entrada
        print(f"{src =}")        # Imprime a entrada original
        print(f"{tokens =}\n")   # Imprime os tokens gerados

    print("[red bold]INCORRETOS")  # Título vermelho para seções de entradas incorretas

    # Testa cada string incorreta
    for src in exemplos_incorretos:
        try:
            tokens = tokenizer(src)  # Tenta tokenizar a entrada
        except SyntaxError:
            print(f"{src =} OK!")  # Se lança erro, está tudo certo (esperado)
        else:
            # Se não lança erro, imprime os tokens (o que não era esperado)
            print(f"{src =}")
            print(f"{tokens =}\n")