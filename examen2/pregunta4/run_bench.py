from pregunta4 import run_bench

if __name__ == "__main__":
    ns = [10, 35, 50]
    run_bench(
        ns,
        timeout_rec=None,
        out_csv="pregunta4_bench.csv",
        out_png="pregunta4_bench.png",
    )
