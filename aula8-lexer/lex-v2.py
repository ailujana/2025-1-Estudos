import re
from rich import print # type: ignore
from typing import Iterator, cast
from dataclasses import dataclass

exemplos_corretos = ["aAa 42 3.14", "aa bbAB #foo\naaa", "aabbbaaa"]
exemplos_incorretos = ["ccc", "a b c", "a c b"]

# Dicionário que define os padrões de tokens reconhecidos pela linguagem
PATTERNS = {
    "COMMENT": r"#[^\n]*",  # Comentários iniciados com # até o fim da linha
    "FLOAT": r"-?0|[1-9][0-9]*\.[0-9]+",  # Números de ponto flutuante
    "INT": r"-?0|[1-9][0-9]*",  # Números inteiros
    "WA": r"[aA]+",  # Letras 'a' ou 'A' repetidas
    "WB": r"[bB]+",  # Letras 'b' ou 'B' repetidas
    "WS": r"\s+",  # Espaços, tabs ou quebras de linha (ignorar)
    
    # Esse padrão captura qualquer coisa que não foi reconhecida.
    # Deve ficar no final para atuar como fallback.
    "ERROR": r".",
}

GROUPS = (f"(?P<{name}>{regex})" for name, regex in PATTERNS.items())
REGEX = "|".join(GROUPS)
LEXER = re.compile(REGEX)


# Classe Token que representa cada token identificado pelo lexer
@dataclass
class Token:
    kind: str  # Tipo do token (ex: WA, INT, FLOAT)
    word: str  # Valor correspondente do texto original


# Função que recebe uma string de entrada e gera um iterador de tokens válidos
def tokenizer(src: str) -> Iterator[Token]:
    IGNORE = ("WS", "COMMENT")  # Tipos de tokens que devem ser ignorados
    
    for m in LEXER.finditer(src):  # Itera sobre os matches da expressão regular
        kind = cast(str, m.lastgroup)  # Nome do grupo casado
        word = m.group(0)  # Texto correspondente

        if kind == "ERROR":
            raise SyntaxError(m)  # Qualquer caractere não reconhecido gera erro

        if kind in IGNORE:
            continue  # Pula comentários e espaços

        yield Token(kind, word)  # Gera token válido

    

# Bloco principal: executa testes quando o script é executado diretamente
if __name__ == "__main__":
    print("[blue bold]CORRETOS")
    for src in exemplos_corretos:
        print(f"{src =}")
        for token in tokenizer(src):  # Gera e imprime os tokens
            print(f" - {token}")

    print("\n[red bold]INCORRETOS")
    for src in exemplos_incorretos:
        try:
            tokens = list(tokenizer(src))  # Tenta gerar todos os tokens
        except SyntaxError:
            print(f"{src =} OK!")  # Erro era esperado: comportamento correto
        else:
            # Se não der erro, mostra os tokens (o que não deveria acontecer)
            print(f"{src =}")
            print(f"{tokens =}\n")
