import sys


def f(n):
    """
    Dado un número n, aplica la función f definida como:
    - Si n es par: n/2
    - Si n es impar: 3n + 1
    """
    if n % 2 == 0:
        return n // 2  # División entera
    else:
        return 3 * n + 1


def count(n):
    """
    Calcula la cantidad de aplicaciones consecutivas de f
    necesarias para que nos quedemos en 1.
    """
    aplicaciones = 0
    numero_actual = n

    # Aplicamos f hasta que lleguemos a 1
    while numero_actual != 1:
        numero_actual = f(numero_actual)
        aplicaciones += 1

    return aplicaciones


def main():
    """
    Si se pasa un entero n como argumento posicional, se imprime count(n).
    Si no se pasa ningún argumento, se ejecutan las pruebas que ya estaban.
    """
    argv = sys.argv  # Nos da el argumento de la línea de comandos
    if len(argv) > 1:
        # Solo aceptamos un entero si se proporciona argumento
        arg = argv[1]
        try:
            n = int(arg)
        except ValueError:
            print(f"Error: '{arg}' no es un entero válido.", file=sys.stderr)
            sys.exit(1)

        # Si se indicó un número, calcular y mostrar su resultado
        print(f"count({n}) = {count(n)}")
    else:
        # Si no se pasó argumento, ejecutamos las pruebas
        print("Pruebas de la función count(n):")
        numeros_prueba = [1, 2, 3, 6, 7, 42]
        for n in numeros_prueba:
            print(f"count({n}) = {count(n)}")


if __name__ == "__main__":
    main()
