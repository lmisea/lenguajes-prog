import pytest
from examen3.pregunta2.main import TypeManager, TypeErrorDef


def test_define_and_atomic_properties():
    tm = TypeManager()
    tm.define_atomic("char", 1, 1)
    tm.define_atomic("short", 2, 2)
    assert tm.describe_props("char") == (1, 1, 0)
    assert tm.describe_props("short") == (2, 2, 0)
    with pytest.raises(TypeErrorDef):
        tm.define_atomic("char", 1, 1)  # duplicado


def test_struct_unpacked_and_packed():
    tm = TypeManager()
    tm.define_atomic("a1", 1, 1)
    tm.define_atomic("a4", 4, 4)
    tm.define_struct("S", ["a1", "a4", "a1"])
    res = tm.describe_all_strategies("S")
    sin = res["sin_empaquetar"]
    empaq = res["empaquetado"]
    reord = res["reordenado"]
    assert sin[0] >= empaq[0]
    assert empaq[0] == 1 + 4 + 1  # packed suma simple
    assert reord[0] <= sin[0]


def test_union_behavior():
    tm = TypeManager()
    tm.define_atomic("x1", 1, 1)
    tm.define_atomic("x8", 8, 8)
    tm.define_union("U", ["x1", "x8"])
    res = tm.describe_all_strategies("U")["sin_empaquetar"]
    assert res[0] >= 8
    assert res[1] == 8
    assert res[2] == res[0] - 8


def test_nested_types_and_reorder_advantage():
    tm = TypeManager()
    tm.define_atomic("c", 1, 1)
    tm.define_atomic("i", 4, 4)
    tm.define_struct("inner", ["c", "i"])  # likely tiene padding
    tm.define_struct("outer", ["c", "inner", "i", "c"])
    res = tm.describe_all_strategies("outer")
    assert res["reordenado"][0] <= res["sin_empaquetar"][0]
    assert res["empaquetado"][0] <= res["reordenado"][0]


def test_errors_on_unknown_types_and_parse():
    tm = TypeManager()
    with pytest.raises(TypeErrorDef):
        tm.define_struct("bad", ["noexiste"])
    with pytest.raises(TypeErrorDef):
        tm.describe_props("noexiste")
    cmd, args = TypeManager.parse_command("ATOMICO char 1 1")
    assert cmd == "ATOMICO" and args[0] == "char"


def test_repl_simulation(monkeypatch, capsys):
    # Simular una sesión REPL con varias acciones válidas e inválidas
    inputs = iter(
        [
            "ATOMICO a 1 1",
            "ATOMICO b 4 4",
            "STRUCT S a b a",
            "UNION U a b",
            "DESCRIBIR S",
            "DESCRIBIR U",
            "ATOMICO bad 0 1",  # tamaño inválido
            "FOO BAR",  # comando desconocido
            "SALIR",
        ]
    )

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)
    # importar repl y ejecutarlo
    from examen3.pregunta2.main import repl

    repl()
    out = capsys.readouterr().out
    assert "Tipo atómico 'a' definido" in out
    assert "Struct 'S' definido" in out
    assert "Union 'U' definido" in out
    assert "Descripción del tipo 'S'" in out
    assert "Comando desconocido" in out


def test_repl_missing_args(monkeypatch, capsys):
    # Probar mensajes de uso cuando faltan argumentos
    inputs = iter(
        [
            "ATOMICO onlytwo 1",  # falta align
            "STRUCT onlyname",
            "UNION onlyname",
            "DESCRIBIR",
            "SALIR",
        ]
    )

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)
    from examen3.pregunta2.main import repl

    repl()
    out = capsys.readouterr().out
    assert "Uso: ATOMICO <nombre> <representación> <alineación>" in out
    assert "Uso: STRUCT <nombre> <tipo> [<tipo> ...]" in out
    assert "Uso: UNION <nombre> <tipo> [<tipo> ...]" in out
    assert "Uso: DESCRIBIR <nombre>" in out


def test_atomic_invalid_values():
    tm = TypeManager()
    # tamaño o alineación no positivos deben lanzar TypeErrorDef
    with pytest.raises(TypeErrorDef):
        tm.define_atomic("bad1", 0, 1)
    with pytest.raises(TypeErrorDef):
        tm.define_atomic("bad2", 1, 0)


def test_empty_struct_and_union():
    tm = TypeManager()
    # definir tipos atómicos mínimos para usar en pruebas mixtas
    tm.define_atomic("a1", 1, 1)
    # struct vacío permitido (sin campos)
    tm.define_struct("EmptyS", [])
    sz, al, wasted = tm.describe_props("EmptyS")
    assert sz == 0 and al == 1 and wasted == 0
    # union vacío permitido
    tm.define_union("EmptyU", [])
    sz2, al2, wasted2 = tm.describe_props("EmptyU")
    assert sz2 == 0 and al2 == 1 and wasted2 == 0
