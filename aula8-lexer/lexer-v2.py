from rich import print # type: ignore
from typing import Iterator, cast
import re

# Conjuntos de teste
exemplos_corretos = ["aAa", "bbBBB", "bb  AA  \t bbBbB \n AaaAa"]
exemplos_invalidos = ["ccc"]

Token = tuple[str, str]  # Cada token contém (texto, tipo)

# Dicionário que define os tipos de tokens permitidos
NON_TERMINALS = {
    "AWORD": r"[aA]+",   # Letras 'a' ou 'A'
    "BWORD": r"[bB]+",   # Letras 'b' ou 'B'
    "WS": r"\s+",        # Espaços
    "ERROR": r"."        # Qualquer outro caractere (deve ser o último)
}

# Constrói os grupos nomeados da regex
PATTERNS = (f"(?P<{name}>{pattern})" for name, pattern in NON_TERMINALS.items())
REGEX = "|".join(PATTERNS)
LEXER = re.compile(REGEX)


def lexer(src: str) -> list[Token]:
    return list(iter_tokens(src))


def iter_tokens(src: str) -> Iterator[Token]:
    for m in LEXER.finditer(src):
        if m.lastgroup == "WS":
            continue  # Espaços são ignorados

        if m.lastgroup == "ERROR":
            pos = m.pos
            chr = m.group()
            raise SyntaxError(f"caractere inválido em {pos}: {chr}")

        yield (m.group(0), cast(str, m.lastgroup))


if __name__ == "__main__":
    print("EXEMPLOS CORRETOS")
    for exemplo in exemplos_corretos:
        print(f"> {exemplo}")
        print(f"[green]- {lexer(exemplo)}\n")

    print("EXEMPLOS INCORRETOS")
    for exemplo in exemplos_invalidos:
        print(">", exemplo)
        try:
            out = lexer(exemplo)
        except SyntaxError:
            print("[green]OK!")  # Erro corretamente detectado
        else:
            print("[red]aceitou e retornou", out)
