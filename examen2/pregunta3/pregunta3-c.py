import sys


class IteradorOrdenado:
    def __init__(self, lista):
        """
        Inicializa el iterador con una lista de enteros.

        Args:
            lista (list): Lista de enteros a ordenar
        """
        self.lista = lista.copy()  # Copia para no modificar la original
        self.heap = []  # Usaremos un min-heap implícito

        # Construir el heap inicial
        for elemento in self.lista:
            self._insertar_heap(elemento)

    def _insertar_heap(self, elemento):
        """
        Inserta un elemento en el heap manteniendo la propiedad de min-heap.
        """
        self.heap.append(elemento)
        indice = len(self.heap) - 1

        # Flotar el elemento hacia arriba
        while indice > 0:
            padre = (indice - 1) // 2
            if self.heap[indice] < self.heap[padre]:
                # Intercambiar con el padre
                self.heap[indice], self.heap[padre] = (
                    self.heap[padre],
                    self.heap[indice],
                )
                indice = padre
            else:
                break

    def _extraer_min(self):
        """
        Extrae y retorna el elemento mínimo del heap.

        Returns:
            int: El elemento mínimo del heap
        """
        if not self.heap:
            return None

        minimo = self.heap[0]
        ultimo = self.heap.pop()

        if self.heap:
            self.heap[0] = ultimo
            self._hundir(0)

        return minimo

    def _hundir(self, indice):
        """
        Hunde un elemento en el heap para mantener la propiedad de min-heap.
        """
        tamaño = len(self.heap)
        while True:
            izquierdo = 2 * indice + 1
            derecho = 2 * indice + 2
            menor = indice

            if izquierdo < tamaño and self.heap[izquierdo] < self.heap[menor]:
                menor = izquierdo

            if derecho < tamaño and self.heap[derecho] < self.heap[menor]:
                menor = derecho

            if menor == indice:
                break

            self.heap[indice], self.heap[menor] = self.heap[menor], self.heap[indice]
            indice = menor

    def __iter__(self):
        """Retorna el iterador mismo."""
        return self

    def __next__(self):
        """Retorna el siguiente elemento en orden ascendente."""
        if not self.heap:
            raise StopIteration

        return self._extraer_min()


# Ejemplo de uso
def ejemplo_iterador(lista=None):
    """Ejecuta el ejemplo del iterador.

    Si se proporciona `lista`, se usa esa lista como entrada. Si no, se usa
    la lista por defecto [1,3,3,2,1]. Los elementos se imprimen en orden
    ascendente usando `IteradorOrdenado`.
    """
    if lista is None:
        lista = [1, 3, 3, 2, 1]
    print("Lista original:", lista)
    print("Elementos en orden:", end=" ")

    for elemento in IteradorOrdenado(lista):
        print(elemento, end=" ")
    print()


def _parse_args(argv):
    # parsear argumentos como enteros; si falla, salir con error
    if not argv:
        return None
    lista = []
    for s in argv:
        try:
            lista.append(int(s))
        except ValueError:
            print(f"Error: '{s}' no es un entero válido.", file=sys.stderr)
            sys.exit(1)
    return lista


if __name__ == "__main__":
    argv = sys.argv[1:]
    lista = _parse_args(argv)
    ejemplo_iterador(lista)
