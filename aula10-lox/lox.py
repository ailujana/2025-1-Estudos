from typing import Callable, Union
from dataclasses import dataclass
from pathlib import Path
import operator
from lark import Lark, Transformer, v_args # type: ignore

# Caminho até o arquivo grammar.lark que define a gramática Lark
DIR = Path(__file__).parent
GRAMMAR_PATH = DIR / "grammar.lark"
grammar = GRAMMAR_PATH.read_text()


# Função para gerar dinamicamente métodos de operações binárias
def op_handler(op):
    def method(self, left, right):
        return BinOp(left, right, op)
    return method


@v_args(inline=True)
class LoxTransformer(Transformer):
    # Transforma operadores binários aritméticos
    mul = op_handler(operator.mul)
    div = op_handler(operator.truediv)
    sub = op_handler(operator.sub)
    add = op_handler(operator.add)

    # Operadores de comparação
    gt = op_handler(operator.gt)
    lt = op_handler(operator.lt)
    ge = op_handler(operator.ge)
    le = op_handler(operator.le)
    eq = op_handler(operator.eq)
    ne = op_handler(operator.ne)

    def VAR(self, token):
        return Var(str(token))  # Transforma variável em objeto

    def NUMBER(self, token):
        return Literal(float(token))  # Transforma número em objeto literal


# Parser e transformer instanciados
transformer = LoxTransformer()
parser = Lark(grammar)

# Definições de tipos para facilitar a leitura e o uso posterior
Expr = Union["BinOp", "Literal", "Var"]
Stmt = Union["If", "For", "While"]
Value = bool | str | float | None
Ctx = dict[str, Value]  # Contexto: dicionário que guarda valores das variáveis



@dataclass
class BinOp:
    """
    Uma operação infixa com dois operandos. x + y, 2 * x, etc.
    """

    left: Expr
    right: Expr
    op: Callable[[Value, Value], Value]
    
    def eval(self, ctx: Ctx):
        left_value = self.left.eval(ctx)
        right_value = self.right.eval(ctx)
        return self.op(left_value, right_value)


@dataclass
class Literal:
    """
    Representa valores literais no código, ex.: strings, booleanos,
    números, etc.
    """

    value: Value
    
    def eval(self, ctx: Ctx):
        return self.value


@dataclass
class Var:
    """
    Uma variável no código
    """

    name: str
    
    def eval(self, ctx: Ctx):
        try:
            return ctx[self.name]
        except KeyError:
            raise NameError(f"variável {self.name} não existe!")


@dataclass
class If: ...


@dataclass
class For: ...


@dataclass
class While:
    cond: Expr
    body: list[Stmt]


def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)


if __name__ == "__main__":
    src = "2 * x + y > 40"  # Exemplo de expressão

    print("src:", src)
    lark_tree = parser.parse(src)  # Gera árvore Lark
    lox_tree = transformer.transform(lark_tree)  # Transforma em objetos Python
    print("-" * 10)

    # Avalia a expressão com variáveis dadas
    result = lox_tree.eval({"x": 20, "y": 2, "z": 3})
    pprint(result)  # Esperado: True
