# Pregunta 3 - IteradorOrdenado

Implementamos la clase `IteradorOrdenado` que permite iterar sobre una lista de
enteros devolviendo sus elementos en orden ascendente (usa un heap interno).

Uso desde la terminal:

- Para ejecutar el ejemplo por defecto (lista [1, 3, 3, 2, 1]):

```bash
python3 pregunta3-c.py
```

- Para pasar una lista desde la línea de comandos (cada argumento debe ser un entero):

```bash
python3 pregunta3-c.py <num1> <num2> <num3> ...
# imprimirá la lista original y luego los elementos en orden ascendente
```

Comportamiento:
- Si se pasan argumentos, el programa intentará parsearlos como enteros y usarlos como
  la lista a ordenar.
- Si no se pasan argumentos, se usa la lista de ejemplo por defecto.
- Si algún argumento no es un entero válido, el programa mostrará un mensaje de error
  por stderr y saldrá con código de salida 1.

Ejemplo de salida:

```
Lista original: [5, 1, 3, 2, 1]
Elementos en orden: 1 1 2 3 5
```
