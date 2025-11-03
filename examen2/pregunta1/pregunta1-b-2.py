import sys


def mergesort(lista):
    """
    Implementación de Mergesort.

    Args:
        lista (list): Lista de elementos comparables

    Returns:
        list: Lista ordenada
    """
    # Caso base: listas de 0 o 1 elemento ya están ordenadas
    if len(lista) <= 1:
        return lista

    # Dividir la lista en dos mitades
    medio = len(lista) // 2
    izquierda = lista[:medio]  # Primera mitad
    derecha = lista[medio:]  # Segunda mitad

    # Ordenar recursivamente cada mitad
    izquierda_ordenada = mergesort(izquierda)
    derecha_ordenada = mergesort(derecha)

    # Mezclar las dos mitades ordenadas
    return mezclar(izquierda_ordenada, derecha_ordenada)


def mezclar(izquierda, derecha):
    """
    Mezcla dos listas ordenadas en una sola lista ordenada.

    Args:
        izquierda (list): Lista ordenada
        derecha (list): Lista ordenada

    Returns:
        list: Lista resultante de mezclar ambas listas ordenadas
    """
    lista_mezclada = []
    i = j = 0  # Índices para recorrer izquierda y derecha

    # Comparar elementos de ambas listas y agregar el menor
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            lista_mezclada.append(izquierda[i])
            i += 1
        else:
            lista_mezclada.append(derecha[j])
            j += 1

    # Agregar los elementos restantes de izquierda (si los hay)
    while i < len(izquierda):
        lista_mezclada.append(izquierda[i])
        i += 1

    # Agregar los elementos restantes de derecha (si los hay)
    while j < len(derecha):
        lista_mezclada.append(derecha[j])
        j += 1

    return lista_mezclada


def main():
    """Función principal para probar Mergesort o ordenar una lista pasada por el usuario.

    Uso:
      - Si se pasan elementos en la línea de comandos: se ordenan esos elementos.
        Ejemplo: python3 pregunta1-b-2.py <num1> <num2> <num3> ...
      - Si no se pasan argumentos, se usa una lista de prueba.
    """
    argv = sys.argv[1:]  # Sacamos los argumentos

    def _parse_element_number(s):
        # Intentar parsear como int, luego float. Si falla, terminar con error.
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                # No es un número válido — salir con mensaje de error
                print(
                    f"Error: '{s}' no es un número válido. Sólo se aceptan enteros o floats.",
                    file=sys.stderr,
                )
                sys.exit(1)

    if argv:
        lista = [_parse_element_number(s) for s in argv]
        print(f"Original: {lista} -> Ordenada: {mergesort(lista)}")
    else:
        # Listas de prueba
        lista1 = [38, 27, 43, 3, 9, 82, 10]
        lista2 = [5, 2, 4, 7, 1, 3, 2, 6]
        lista3 = [1]
        lista4 = []

        print("Mergesort - Pruebas:")
        print(f"Original: {lista1} -> Ordenada: {mergesort(lista1)}")
        print(f"Original: {lista2} -> Ordenada: {mergesort(lista2)}")
        print(f"Original: {lista3} -> Ordenada: {mergesort(lista3)}")
        print(f"Original: {lista4} -> Ordenada: {mergesort(lista4)}")


if __name__ == "__main__":
    main()
