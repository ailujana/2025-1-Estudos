from rich import print # type: ignore
from typing import cast
import re

# Exemplos positivos e negativos
exemplos_corretos = ["aAa", "bbBBB", "bb  AA  \t bbBbB \n AaaAa"]
exemplos_invalidos = ["ccc"]

Token = tuple[str, str]  # Cada token é representado como (texto, tipo)

# Regex com grupos nomeados:
# - AWORD: letras 'a' ou 'A'
# - BWORD: letras 'b' ou 'B'
# - WS: espaços em branco (não são armazenados)
LEXER = re.compile(r"(?P<AWORD>[aA]+)|(?P<BWORD>[bB]+)|(?P<WS>\s+)")


def lexer(src: str) -> list[Token]:
    result: list[Token] = []
    pos = 0

    while True:
        m = LEXER.match(src, pos)  # Procura casar a partir da posição atual
        if m is None:
            raise SyntaxError(src[pos:])  # Se nada casar, há caractere inválido

        initial, end = m.span()
        token = (src[initial:end], cast(str, m.lastgroup))  # Gera o token
        result.append(token)
        pos = end

        if pos == len(src):  # Quando atinge o final, retorna os tokens
            return result


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
            print("[green]OK!")  # Erro era esperado
        else:
            print("[red]aceitou e retornou", out)
