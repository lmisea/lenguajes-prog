from collections import deque


class Node:
    pass


class IntNode(Node):
    def __init__(self, value: int):
        self.value = value


class OpNode(Node):
    def __init__(self, op: str, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right


OPS = {"+", "-", "*", "/"}


def parse_prefix(tokens):
    d = deque(tokens)

    def parse():
        if not d:
            raise ValueError("Expresión incompleta (prefijo)")
        tok = d.popleft()
        if tok in OPS:
            left = parse()
            right = parse()
            return OpNode(tok, left, right)
        else:
            try:
                return IntNode(int(tok))
            except ValueError:
                raise ValueError(f"Token no válido: {tok}")

    node = parse()
    if d:
        raise ValueError("Tokens sobrantes después de parsear (prefijo)")
    return node


def parse_postfix(tokens):
    stack = []
    for tok in tokens:
        if tok in OPS:
            if len(stack) < 2:
                raise ValueError("Expresión incompleta (postfijo)")
            right = stack.pop()
            left = stack.pop()
            stack.append(OpNode(tok, left, right))
        else:
            try:
                stack.append(IntNode(int(tok)))
            except ValueError:
                raise ValueError(f"Token no válido: {tok}")
    if len(stack) != 1:
        raise ValueError("Expresión inválida (postfijo)")
    return stack[0]


def eval_node(node: Node) -> int:
    if isinstance(node, IntNode):
        return node.value
    assert isinstance(node, OpNode)
    left_val = eval_node(node.left)
    right_val = eval_node(node.right)
    if node.op == "+":
        return left_val + right_val
    if node.op == "-":
        return left_val - right_val
    if node.op == "*":
        return left_val * right_val
    if node.op == "/":
        # división entera
        return left_val // right_val
    raise ValueError(f"Operador desconocido: {node.op}")


def precedence(op: str) -> int:
    if op in ("+", "-"):
        return 1
    if op in ("*", "/"):
        return 2
    return 0


def to_infix(node: Node) -> str:
    if isinstance(node, IntNode):
        return str(node.value)
    assert isinstance(node, OpNode)
    left = node.left
    right = node.right
    left_s = to_infix(left)
    right_s = to_infix(right)
    # decidir si se necesitan paréntesis
    if isinstance(left, OpNode):
        if precedence(left.op) < precedence(node.op):
            left_s = f"({left_s})"
        # hijo izquierdo con igual precedencia: left-assoc => no paréntesis
    if isinstance(right, OpNode):
        if precedence(right.op) < precedence(node.op):
            right_s = f"({right_s})"
        elif precedence(right.op) == precedence(node.op):
            # iguales y operadores asociativos a la izquierda -> paréntesis en el hijo derecho
            right_s = f"({right_s})"
    return f"{left_s} {node.op} {right_s}"


def eval_expr(order: str, tokens):
    order = order.upper()
    if order == "PRE":
        node = parse_prefix(tokens)
    elif order == "POST":
        node = parse_postfix(tokens)
    else:
        raise ValueError("Orden desconocido: debe ser PRE o POST")
    return eval_node(node)


def mostrar_infix(order: str, tokens):
    order = order.upper()
    if order == "PRE":
        node = parse_prefix(tokens)
    elif order == "POST":
        node = parse_postfix(tokens)
    else:
        raise ValueError("Orden desconocido: debe ser PRE o POST")
    return to_infix(node)


def repl():
    prompt = "Introduzca una acción <EVAL | MOSTRAR | SALIR> \n"
    while True:
        try:
            line = input(prompt)
        except EOFError:
            break
        if not line:
            continue
        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0].upper()
        if cmd == "SALIR":
            break
        if len(parts) < 2:
            print(
                "Comando inválido. Introduzca EVAL <PRE|POST> <expr>, MOSTRAR <PRE|POST> <expr> o SALIR"
            )
            continue
        action = cmd
        order = parts[1].upper()
        expr_tokens = parts[2:]
        if not expr_tokens:
            print("Falta la expresión.")
            continue
        try:
            if action == "EVAL":
                res = eval_expr(order, expr_tokens)
                print(res)
            elif action == "MOSTRAR":
                s = mostrar_infix(order, expr_tokens)
                print(s)
            else:
                print("Comando desconocido.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    repl()
