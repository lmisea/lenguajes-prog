import pytest

from pregunta2 import eval_expr, mostrar_infix, parse_prefix, parse_postfix


def test_eval_examples_prefix():
    toks = ["+", "*", "+", "3", "4", "5", "7"]
    assert eval_expr("PRE", toks) == 42


def test_eval_examples_postfix():
    toks = ["8", "3", "-", "8", "4", "4", "+", "*", "+"]
    assert eval_expr("POST", toks) == 69


def test_mostrar_prefix():
    toks = ["+", "*", "+", "3", "4", "5", "7"]
    assert mostrar_infix("PRE", toks) == "(3 + 4) * 5 + 7"


def test_mostrar_postfix():
    toks = ["8", "3", "-", "8", "4", "4", "+", "*", "+"]
    assert mostrar_infix("POST", toks) == "8 - 3 + 8 * (4 + 4)"


def test_parentheses_and_assoc():
    # 8 - (3 - 4)
    toks = ["-", "8", "-", "3", "4"]
    assert eval_expr("PRE", toks) == 9
    assert mostrar_infix("PRE", toks) == "8 - (3 - 4)"

    # (8 - 3) - 4 -> no necesita paréntesis
    toks2 = ["-", "-", "8", "3", "4"]
    assert eval_expr("PRE", toks2) == 1
    assert mostrar_infix("PRE", toks2) == "8 - 3 - 4"


def test_invalid_tokens_raise():
    with pytest.raises(ValueError):
        parse_prefix(["+", "a", "1"])
    with pytest.raises(ValueError):
        parse_postfix(["1", "b", "+"])


def test_parse_errors_and_invalid_order():
    # prefijo incompleto
    with pytest.raises(ValueError):
        parse_prefix(["+"])
    # tokens sobrantes después de prefijo
    with pytest.raises(ValueError):
        parse_prefix(["+", "1", "2", "3"])
    # postfijo incompleto
    with pytest.raises(ValueError):
        parse_postfix(["+"])
    # comando inválido
    with pytest.raises(ValueError):
        eval_expr("MID", ["1", "2", "+"])
    with pytest.raises(ValueError):
        mostrar_infix("MID", ["1", "2", "+"])


def test_division_and_negatives():
    # división entera con positivos
    assert eval_expr("PRE", ["/", "7", "3"]) == 7 // 3
    # división entera con negativos (truncamiento piso de Python)
    assert eval_expr("PRE", ["/", "-7", "3"]) == -7 // 3


def test_parentheses_variety():
    # hijo izquierdo con menor precedencia -> necesita paréntesis
    assert mostrar_infix("PRE", ["*", "+", "1", "2", "3"]) == "(1 + 2) * 3"
    # hijo derecho con igual precedencia -> paréntesis en el hijo derecho
    assert mostrar_infix("PRE", ["-", "1", "-", "2", "3"]) == "1 - (2 - 3)"


def test_repl_flow(monkeypatch, capsys):
    # Simula entradas del usuario para recorrer rutas del REPL
    inputs = iter(
        [
            "",  # empty -> ignored
            "UNKNOWN",  # comando desconocido -> mensaje de error
            "EVAL PRE + * + 3 4 5 7",  # debe imprimir 42
            "MOSTRAR PRE + * + 3 4 5 7",  # debe imprimir (3 + 4) * 5 + 7
            "SALIR",
        ]
    )

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)
    # corremos repl
    from pregunta2 import repl

    repl()
    captured = capsys.readouterr()
    assert "42" in captured.out
    assert "(3 + 4) * 5 + 7" in captured.out
