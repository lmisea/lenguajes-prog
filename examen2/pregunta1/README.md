# Pregunta 1 - Función count(n) y Mergesort

Archivos principales:

1. `pregunta1-b-1.py`
   - Función: `count(n)` -> cuenta las aplicaciones de f hasta llegar a 1.
   - Uso desde la terminal:
     - Para calcular un valor concreto:
       ```
       python3 pregunta1-b-1.py <n>
       # salida: count(n) = <resultado>
       ```
     - Si no se pasa ningún argumento, se muestran algunas pruebas por defecto con distintos n:
       ```
       python3 pregunta1-b-1.py
       ```

2. `pregunta1-b-2.py`
   - Implementación de Mergesort.
   - Uso desde la terminal:
     - Para ordenar una lista de números (enteros o floats):
       ```
       python3 pregunta1-b-2.py <num1> <num2> <num3> ...
       # salida: Original: <lista original> -> Ordenada: <lista ordenada>
       ```
     - Si no se pasan argumentos, se muestra una lista de prueba por defecto:
       ```
       python3 pregunta1-b-2.py
       ```

Nota:
- `pregunta1-b-2.py` acepta sólo argumentos numéricos. Cada argumento se intenta parsear primero como `int` y si falla como `float`.
