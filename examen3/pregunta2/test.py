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
    # sin empaquetar: a1 at 0, a4 at 4 -> offsets cause padding; check sizes sensible
    sin = res["sin_empaquetar"]
    empaq = res["empaquetado"]
    reord = res["reordenado"]
    assert sin[0] >= empaq[0]
    assert empaq[0] == 1 + 4 + 1  # packed suma simple
    # reordenado debe ser <= sin
    assert reord[0] <= sin[0]


def test_union_behavior():
    tm = TypeManager()
    tm.define_atomic("x1", 1, 1)
    tm.define_atomic("x8", 8, 8)
    tm.define_union("U", ["x1", "x8"])
    res = tm.describe_all_strategies("U")["sin_empaquetar"]
    # union size debe ajustarse a alineación máxima
    assert res[0] >= 8
    assert res[1] == 8
    assert res[2] == res[0] - 8


def test_nested_types_and_reorder_advantage():
    tm = TypeManager()
    tm.define_atomic("c", 1, 1)
    tm.define_atomic("i", 4, 4)
    tm.define_struct("inner", ["c", "i"])  # likely has padding
    tm.define_struct("outer", ["c", "inner", "i", "c"])
    res = tm.describe_all_strategies("outer")
    # asegurarse que reordenado no empeora y que empaquetado reduce size
    assert res["reordenado"][0] <= res["sin_empaquetar"][0]
    assert res["empaquetado"][0] <= res["reordenado"][0]


def test_errors_on_unknown_types_and_parse():
    tm = TypeManager()
    with pytest.raises(TypeErrorDef):
        tm.define_struct("bad", ["noexiste"])
    with pytest.raises(TypeErrorDef):
        tm.describe_props("noexiste")
    # parse command
    cmd, args = TypeManager.parse_command("ATOMICO char 1 1")
    assert cmd == "ATOMICO" and args[0] == "char"
