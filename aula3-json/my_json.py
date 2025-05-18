from typing import Any

# Função principal para interpretar uma string JSON
def read_json(src: str) -> Any:
    # Reverte a string em uma lista de caracteres para facilitar leitura com pop()
    chars = list(reversed(src))
    return read_value(chars)  # Inicia leitura do valor principal do JSON

# Função que decide qual tipo de valor JSON será lido
def read_value(chars: list[str]):
    ws(chars)  # Remove espaços em branco antes de processar o valor

    match chars[-1]:  # Analisa o próximo caractere
        case "t":
            # Literal "true"
            value = read_literal("true", chars, True)
        case "f":
            # Literal "false"
            value = read_literal("false", chars, False)
        case "n":
            # Literal "null"
            value = read_literal("null", chars, None)
        case "{":
            # Objeto JSON
            value = read_object(chars)
        case "[":
            # Array JSON
            value = read_array(chars)
        case '"':
            # String JSON
            value = read_string(chars)
        case '-':
            # Número negativo
            chars.pop()
            value = -read_number(chars)
        case c if c.isdigit():
            # Número positivo
            value = read_number(chars)
        case _:
            # Qualquer outro caractere causa erro de sintaxe
            raise SyntaxError 

    ws(chars)  # Remove espaços em branco após processar o valor
    return value


# Função auxiliar para ignorar espaços em branco
def ws(chars: list[str]):
    while chars and chars[-1] in " \n\t\r":
        chars.pop()


# Verifica e consome literais como "true", "false" e "null"
def read_literal(lit: str, chars: list[str], value):
    for c in lit:
        if c != chars.pop():
            raise SyntaxError  # Se algum caractere não bater, erro
    return value


# Lê números inteiros simples do JSON (sem ponto flutuante)
def read_number(chars: list[str]) -> int:
    if chars[-1] == "0":
        chars.pop()
        return 0  # Trata 0 como caso especial

    ns = []
    while chars and chars[-1] in "0123456789":
        n = chars.pop()
        ns.append(n)
    return int("".join(ns))  # Junta os dígitos e converte para int


# Lê strings JSON entre aspas duplas
def read_string(chars: list[str]) -> str:
    if chars.pop() != '"':
        raise SyntaxError  # Erro se não começar com aspas

    parts = []
    while (c := chars.pop()) != '"':
        parts.append(c)  # Coleta cada caractere da string

    return "".join(parts)  # Retorna a string formada


# Lê arrays JSON (listas Python)
def read_array(chars: list[str]) -> list:
    if chars.pop() != "[":
        raise SyntaxError  # Erro se não começar com [

    ws(chars)  # Ignora espaços

    # Caso de array vazio
    if chars[-1] == "]":
        chars.pop()
        return []

    values = []
    while True:
        value = read_value(chars)  # Lê um valor dentro do array
        values.append(value)
        
        c = chars.pop()
        if c == ",":
            continue  # Lê próximo valor
        elif c == "]":
            break  # Fim do array
        else:
            raise SyntaxError  # Qualquer outra coisa é erro
    
    return values


# OBS: Essa função está declarada mas não utilizada neste exemplo
# Lê objetos JSON (dicionários), ainda a ser implementada se necessário
def read_object(chars: list[str]):
    raise NotImplementedError("Objetos JSON não implementados")

# Bloco principal de testes
if __name__ == "__main__":
    import json 
    import time

    # Testes simples de leitura de tipos diferentes
    print(read_json("null"))                         # Saída: None
    print(read_json("42") + 1)                       # Saída: 43
    print(read_json('"Fabio"'))                      # Saída: Fabio
    print(read_json('[1, "Fabio", [1, 2, [[]]], "compiladores"]'))  # Saída: [1, 'Fabio', [1, 2, [[]]], 'compiladores']

    # Texto de entrada a ser testado com benchmarks
    src = '[1, "Fabio", [1, 2, [[]]], "compiladores"]'
    
    # Benchmark usando o parser nativo do Python
    t0 = time.time()
    for _ in range(1000):
        json.loads(src)
    print("json.loads:", time.time() - t0)

    # Benchmark usando o parser customizado
    t0 = time.time()
    for _ in range(1000):
        read_json(src)
    print("read_json:", time.time() - t0)
