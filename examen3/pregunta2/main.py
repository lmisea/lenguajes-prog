"""
Simulador de manejador de tipos (ATOMICO, STRUCT, UNION).

Comandos interactivos (separados por espacios):
 - ATOMICO <nombre> <representación> <alineación>
 - STRUCT <nombre> <tipo> [<tipo> ...]
 - UNION <nombre> <tipo> [<tipo> ...]
 - DESCRIBIR <nombre>
 - SALIR

Todas las salidas en español.
"""

from typing import Dict, List, Tuple, Optional


class TypeErrorDef(Exception):
    pass


class TypeManager:
    """Gestiona definiciones de tipos y cálculo de tamaño/alineación/padding."""

    def __init__(self):
        # name -> dict with kind and info
        self.types: Dict[str, Dict] = {}

    # ---- definiciones ----
    def define_atomic(self, name: str, size: int, align: int) -> None:
        if size <= 0 or align <= 0:
            raise TypeErrorDef("Tamaño o alineación inválidos")
        if name in self.types:
            raise TypeErrorDef("Tipo ya definido")
        self.types[name] = {"kind": "atomic", "size": int(size), "align": int(align)}

    def define_struct(self, name: str, field_types: List[str]) -> None:
        if name in self.types:
            raise TypeErrorDef("Tipo ya definido")
        for t in field_types:
            if t not in self.types:
                raise TypeErrorDef(f"Tipo desconocido: {t}")
        self.types[name] = {"kind": "struct", "fields": list(field_types)}

    def define_union(self, name: str, field_types: List[str]) -> None:
        if name in self.types:
            raise TypeErrorDef("Tipo ya definido")
        for t in field_types:
            if t not in self.types:
                raise TypeErrorDef(f"Tipo desconocido: {t}")
        self.types[name] = {"kind": "union", "fields": list(field_types)}

    # ---- consultas internas ----
    @staticmethod
    def _align_up(offset: int, align: int) -> int:
        return ((offset + align - 1) // align) * align

    def _atomic_props(self, name: str) -> Tuple[int, int]:
        t = self.types[name]
        assert t["kind"] == "atomic"
        return t["size"], t["align"]

    def _compute_struct(
        self, field_names: List[str], strategy: str
    ) -> Tuple[int, int, int]:
        # devuelve (total_size, alignment, wasted_bytes)
        # estrategia: 'unpacked' (sin empaquetar), 'packed', 'reordered'
        fields = []
        for fname in field_names:
            f = self.types[fname]
            if f["kind"] == "atomic":
                fields.append((f["size"], f["align"]))
            else:
                # permitir structs/unions anidados: calcular sus propiedades recursivamente con 'unpacked'
                sz, al, _ = self.describe_props(
                    fname
                )  # usa la versión por defecto (unpacked)
                fields.append((sz, al))

        if strategy == "packed":
            # alineación 1 y sin padding interno
            total_size = sum(s for s, a in fields)
            alignment = 1
            wasted = 0
            return total_size, alignment, wasted

        # para 'unpacked' y 'reordered'
        if strategy == "reordered":
            # ordenar por alineación descendente, romper empates por tamaño descendente
            fields = sorted(fields, key=lambda x: (-x[1], -x[0]))

        # calcular alignment struct = max de alineaciones
        struct_align = max((a for _, a in fields), default=1)
        offset = 0
        sum_field_sizes = 0
        for sz, al in fields:
            offset = self._align_up(offset, al)
            offset += sz
            sum_field_sizes += sz
        total_size = self._align_up(offset, struct_align)
        wasted = total_size - sum_field_sizes
        return total_size, struct_align, wasted

    def _compute_union(self, field_names: List[str]) -> Tuple[int, int, int]:
        # union: size = max(field_size) rounded up to max alignment
        sizes = []
        aligns = []
        for fname in field_names:
            f = self.types[fname]
            if f["kind"] == "atomic":
                sz, al = f["size"], f["align"]
            else:
                sz, al, _ = self.describe_props(fname)
            sizes.append(sz)
            aligns.append(al)
        if not sizes:
            return 0, 1, 0
        max_size = max(sizes)
        max_align = max(aligns)
        total_size = self._align_up(max_size, max_align)
        wasted = total_size - max_size
        return total_size, max_align, wasted

    # ---- interfaz pública ----
    def describe_props(self, name: str) -> Tuple[int, int, int]:
        """Devuelve (size, align, wasted) usando la estrategia 'unpacked' por defecto."""
        if name not in self.types:
            raise TypeErrorDef("Tipo no definido")
        t = self.types[name]
        if t["kind"] == "atomic":
            sz, al = t["size"], t["align"]
            return sz, al, 0
        if t["kind"] == "struct":
            return self._compute_struct(t["fields"], "unpacked")
        if t["kind"] == "union":
            return self._compute_union(t["fields"])
        raise TypeErrorDef("Tipo inválido")

    def describe_all_strategies(self, name: str) -> Dict[str, Tuple[int, int, int]]:
        """Devuelve un dict con claves: 'sin_empaquetar', 'empaquetado', 'reordenado' -> (size,align,wasted)."""
        if name not in self.types:
            raise TypeErrorDef("Tipo no definido")
        t = self.types[name]
        if t["kind"] == "atomic":
            sz, al = t["size"], t["align"]
            return {
                "sin_empaquetar": (sz, al, 0),
                "empaquetado": (sz, 1, 0),
                "reordenado": (sz, al, 0),
            }
        if t["kind"] == "struct":
            u = self._compute_struct(t["fields"], "unpacked")
            p = self._compute_struct(t["fields"], "packed")
            r = self._compute_struct(t["fields"], "reordered")
            return {"sin_empaquetar": u, "empaquetado": p, "reordenado": r}
        if t["kind"] == "union":
            u = self._compute_union(t["fields"])
            # empaquetado/reordenado no cambian para union
            return {"sin_empaquetar": u, "empaquetado": u, "reordenado": u}
        raise TypeErrorDef("Tipo inválido")

    # ---- utilidades REPL / parsing ----
    @staticmethod
    def parse_command(line: str) -> Tuple[str, List[str]]:
        parts = line.strip().split()
        if not parts:
            return "", []
        cmd = parts[0].upper()
        return cmd, parts[1:]


def repl():
    tm = TypeManager()
    prompt = "Acción (ATOMICO/STRUCT/UNION/DESCRIBIR/SALIR)> "
    while True:
        try:
            line = input(prompt)
        except EOFError:
            break
        cmd, args = TypeManager.parse_command(line)
        if cmd == "":
            continue
        try:
            if cmd == "SALIR":
                print("Saliendo...")
                break
            elif cmd == "ATOMICO":
                if len(args) != 3:
                    print("Uso: ATOMICO <nombre> <representación> <alineación>")
                    continue
                name, size_s, align_s = args
                tm.define_atomic(name, int(size_s), int(align_s))
                print(
                    f"Tipo atómico '{name}' definido (size={size_s}, align={align_s})"
                )
            elif cmd == "STRUCT":
                if len(args) < 2:
                    print("Uso: STRUCT <nombre> <tipo> [<tipo> ...]")
                    continue
                name, *fields = args
                tm.define_struct(name, fields)
                print(f"Struct '{name}' definido con campos: {fields}")
            elif cmd == "UNION":
                if len(args) < 2:
                    print("Uso: UNION <nombre> <tipo> [<tipo> ...]")
                    continue
                name, *fields = args
                tm.define_union(name, fields)
                print(f"Union '{name}' definido con campos: {fields}")
            elif cmd == "DESCRIBIR":
                if len(args) != 1:
                    print("Uso: DESCRIBIR <nombre>")
                    continue
                name = args[0]
                results = tm.describe_all_strategies(name)
                print(f"Descripción del tipo '{name}':")
                for k, (sz, al, wasted) in results.items():
                    etiqueta = {
                        "sin_empaquetar": "Sin empaquetar",
                        "empaquetado": "Empaquetado",
                        "reordenado": "Reordenando campos óptimamente",
                    }[k]
                    print(
                        f"  {etiqueta}: tamaño={sz} bytes, alineación={al}, desperdicio={wasted} bytes"
                    )
            else:
                print("Comando desconocido.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    repl()
