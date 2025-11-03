"""
Pregunta 4

Implementaciones de la familia de funciones F_{alpha,beta} con:
  X=1, Y=7, Z=5
  alpha = ((X+Y) mod 5) + 3
  beta  = ((Y+Z) mod 5) + 3

Se implementan:
 (a) f_recursiva: traducción directa de la fórmula (recursión múltiple)
 (b) f_tail: versión recursiva de cola (tail-recursive style)
 (c) f_iterativa: versión iterativa equivalente

Se incluyen medidas de tiempo para comparar las tres implementaciones.
Todos los comentarios en español.
"""

from time import perf_counter


# Constantes dadas
X = 1
Y = 7
Z = 5


def compute_alpha_beta():
    """Calcula alpha y beta según la fórmula dada."""
    alpha = ((X + Y) % 5) + 3
    beta = ((Y + Z) % 5) + 3
    return alpha, beta


ALPHA, BETA = compute_alpha_beta()
# límite base: si 0 <= n < ALPHA * BETA entonces F(n) = n
BASE_LIMIT = ALPHA * BETA


def f_recursiva(n):
    """Implementación directa (traducción literal de la definición).

    F(n) = n                         si 0 <= n < ALPHA*BETA
         = sum_{i=1..ALPHA} F(n - BETA*i)  si n >= ALPHA*BETA

    Esta versión no usa memorización ni optimizaciones.
    """
    if 0 <= n < BASE_LIMIT:
        return n
    # n >= BASE_LIMIT
    s = 0
    for i in range(1, ALPHA + 1):
        s += f_recursiva(n - BETA * i)
    return s


def f_tail(n):
    """Versión recursiva de cola (tail-recursive style).

    Idea: mantenemos una lista de pendientes por procesar y un acumulador.
    En cada llamada tail(pendientes, acc) procesamos un elemento de pendientes.
    Si el elemento está en la base, lo acumulamos; si no, añadimos sus hijos
    (n - BETA*i) a la lista de pendientes. La llamada recursiva es en cola.

    Nota: Python no optimiza recursión de cola; esta versión es conceptualmente
    tail-recursive pero puede agotar la pila si hay demasiados pendientes.
    """

    def tail(pendientes, acc):
        if not pendientes:
            return acc
        m = pendientes.pop()
        if 0 <= m < BASE_LIMIT:
            return tail(pendientes, acc + m)
        # expandir m en sus ALPHA hijos
        for i in range(1, ALPHA + 1):
            pendientes.append(m - BETA * i)
        return tail(pendientes, acc)

    return tail([n], 0)


def f_iterativa(n):
    """Versión iterativa equivalente a la recursiva de cola.

    Corresponde directamente con la versión `f_tail`:
      - la pila/cola `pendientes` en la iterativa corresponde al argumento
        `pendientes` de la función recursiva de cola.
      - el acumulador `acc` corresponde al acumulador recursivo.
    """
    pendientes = [n]
    acc = 0
    while pendientes:
        m = pendientes.pop()
        if 0 <= m < BASE_LIMIT:
            acc += m
            continue
        for i in range(1, ALPHA + 1):
            pendientes.append(m - BETA * i)
    return acc


def tiempo_ejecucion(func, n, repeat=1):
    """Mide el tiempo de ejecución de func(n) (promedia sobre `repeat`)."""
    tiempos = []
    res = None
    for _ in range(repeat):
        t0 = perf_counter()
        res = func(n)
        t1 = perf_counter()
        tiempos.append(t1 - t0)
    return res, sum(tiempos) / len(tiempos)


def main_demo():
    """Demostración y comparación de tiempos.

    Se eligen algunos valores de `n` para comparar. Atención: la versión recursiva
    directa puede crecer exponencialmente y tardar mucho para `n` grandes.
    """
    print(f"Constantes: X={X}, Y={Y}, Z={Z}")
    print(f"alpha={ALPHA}, beta={BETA}, base_limit={BASE_LIMIT}")
    print()

    # valores de prueba (elegidos para que la versión recursiva directa sea manejable)
    pruebas = [10, 35, 50]

    for n in pruebas:
        print(f"n = {n}")
        # recursiva directa: intentar, pero proteger contra tiempos excesivos
        try:
            res_rec, t_rec = tiempo_ejecucion(f_recursiva, n, repeat=1)
        except RecursionError:
            res_rec, t_rec = None, float("inf")
        except Exception:
            res_rec, t_rec = None, float("inf")

        res_tail, t_tail = tiempo_ejecucion(f_tail, n, repeat=1)
        res_iter, t_iter = tiempo_ejecucion(f_iterativa, n, repeat=1)

        print(f"  recursiva directa:  resultado={res_rec}  tiempo={t_rec:.6f}s")
        print(f"  recursiva cola:     resultado={res_tail}  tiempo={t_tail:.6f}s")
        print(f"  iterativa:         resultado={res_iter}  tiempo={t_iter:.6f}s")
        print()


def _run_with_timeout(func, n, timeout):
    """Ejecuta func(n) en proceso aparte y devuelve (result, time) o (None, inf) si timeout.

    Implementación basada en multiprocessing.Process y Pipe para evitar problemas de
    pickle de funciones locales.
    """
    from multiprocessing import Process, Pipe
    from time import perf_counter

    def _worker(name, x, conn):
        """Worker que ejecuta la función por nombre y envía (result, time) por conn."""
        t0 = perf_counter()
        try:
            fn = globals()[name]
            r = fn(x)
            t1 = perf_counter()
            conn.send((r, t1 - t0))
        except Exception:
            conn.send((None, float("inf")))
        finally:
            conn.close()

    parent_conn, child_conn = Pipe()
    p = Process(target=_worker, args=(func.__name__, n, child_conn))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return None, float("inf")
    if parent_conn.poll():
        return parent_conn.recv()
    return None, float("inf")


def run_bench(
    ns, timeout_rec=1.0, out_csv="pregunta4_bench.csv", out_png="pregunta4_bench.png"
):
    """Ejecuta benchmarks para los valores en `ns`. Guarda CSV y un gráfico PNG.

    timeout_rec: tiempo máximo (s) para intentar la versión recursiva directa por entrada.
    """
    import csv

    rows = []
    for n in ns:
        print(f"Benchmark n={n}")
        if timeout_rec is None:
            # ejecutar recursiva directa sin timeout (usar solo para ns pequeños)
            try:
                rec_res, rec_t = tiempo_ejecucion(f_recursiva, n, repeat=1)
            except Exception:
                rec_res, rec_t = None, float("inf")
        else:
            rec_res, rec_t = _run_with_timeout(f_recursiva, n, timeout_rec)
        tail_res, tail_t = tiempo_ejecucion(f_tail, n, repeat=1)
        iter_res, iter_t = tiempo_ejecucion(f_iterativa, n, repeat=1)
        print(f"  rec: {rec_res} t={rec_t:.6f}s")
        print(f"  tail:{tail_res} t={tail_t:.6f}s")
        print(f"  iter:{iter_res} t={iter_t:.6f}s")
        rows.append((n, rec_res, rec_t, tail_res, tail_t, iter_res, iter_t))

    # Guardar CSV
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "n",
                "rec_res",
                "rec_time",
                "tail_res",
                "tail_time",
                "iter_res",
                "iter_time",
            ]
        )
        for r in rows:
            w.writerow(r)

    # Generar gráfico (tiempos)
    try:
        import matplotlib.pyplot as plt

        ns_plot = [r[0] for r in rows]
        rec_times = [r[2] for r in rows]
        tail_times = [r[4] for r in rows]
        iter_times = [r[6] for r in rows]

        plt.figure(figsize=(8, 5))
        plt.plot(ns_plot, rec_times, "-o", label="recursiva directa")
        plt.plot(ns_plot, tail_times, "-s", label="recursiva cola")
        plt.plot(ns_plot, iter_times, "-^", label="iterativa")
        plt.yscale("log")
        plt.xlabel("n")
        plt.ylabel("Tiempo (s) [escala log]")
        plt.title("Benchmark F_{alpha,beta}: tiempos de ejecución")
        plt.legend()
        plt.grid(True, which="both", ls="--", lw=0.5)
        plt.tight_layout()
        plt.savefig(out_png)
        print(f"Gráfico guardado en {out_png}")
    except Exception as e:
        print(f"No se pudo generar gráfico: {e}")

    return rows


if __name__ == "__main__":
    # Ejecutar demo/mediciones
    main_demo()
