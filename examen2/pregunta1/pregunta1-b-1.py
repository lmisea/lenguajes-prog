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

def dist(n):
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
    """Función principal para probar el programa"""
    # Probamos con el ejemplo dado: dist(42) debería ser 8
    numero = 42
    resultado = dist(numero)
    print(f"dist({numero}) = {resultado}")

    # Podemos probar con otros números
    numeros_prueba = [1, 2, 3, 6, 7, 42]
    for n in numeros_prueba:
        print(f"dist({n}) = {dist(n)}")

if __name__ == "__main__":
    main()
