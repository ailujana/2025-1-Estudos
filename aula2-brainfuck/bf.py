#!/usr/bin/python3
import sys
import click  # type: ignore # Biblioteca usada para ler entrada do usuário via teclado

# Classe que representa a máquina virtual do interpretador Brainfuck
class BF:
    def __init__(self):
        self.memory = [0] * 10_000  # Fita de memória com 10.000 posições, todas iniciadas com 0
        self.index = 0              # Ponteiro de memória (inicialmente na posição 0)

    # Método que executa o código Brainfuck
    def run(self, src: str):
        chars = iter(src)  # Cria um iterador sobre os caracteres do código
        for c in chars:
            match c:
                case ">":
                    # Move o ponteiro uma posição para a direita
                    self.index += 1

                case "<":
                    # Move o ponteiro uma posição para a esquerda
                    if self.index == 0:
                        raise IndexError  # Evita acessar posição negativa da memória
                    self.index -= 1

                case "+":
                    # Incrementa o valor da célula atual, com overflow para 0 após 255
                    self.memory[self.index] = (self.memory[self.index] + 1) % 256

                case "-":
                    # Decrementa o valor da célula atual, com underflow para 255 após 0
                    self.memory[self.index] = (self.memory[self.index] - 1) % 256

                case ".":
                    # Imprime o caractere ASCII correspondente ao valor atual da célula
                    print(chr(self.memory[self.index]), end="")

                case ",":
                    # Lê um caractere do teclado e armazena o código ASCII na célula atual
                    self.memory[self.index] = ord(click.getchar(echo=True)) % 256

                case "[":
                    # Início de um loop: enquanto o valor da célula atual for diferente de zero,
                    # o código entre [ e ] será executado
                    cmd = []
                    open_paren = 1  # Contador de colchetes para lidar com loops aninhados

                    # Lê os caracteres dentro do bloco de loop
                    for c in chars:
                        if c == "]":
                            open_paren -= 1
                        if c == "[":
                            open_paren += 1
                        if open_paren == 0:
                            break
                        cmd.append(c)
                    else:
                        # Se não encontrar um colchete de fechamento, lança erro de sintaxe
                        raise SyntaxError

                    body = "".join(cmd)  # Junta o corpo do loop como string

                    # Executa o corpo do loop enquanto o valor da célula atual for diferente de zero
                    while self.memory[self.index] != 0:
                        self.run(body)

                case "]":
                    # Colchete de fechamento isolado não é permitido
                    raise SyntaxError


# Função principal que carrega o arquivo e executa o interpretador
def main():
    vm = BF()  # Cria instância da máquina virtual
    filename = sys.argv[-1]  # Pega o nome do arquivo passado por argumento

    with open(filename, "r") as fd:
        source = fd.read()  # Lê o conteúdo do arquivo

    vm.run(source)  # Executa o código Brainfuck


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
