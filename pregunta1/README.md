# Pregunta 1 - Carpeta "pregunta1"

Esta es la sección (b) de la pregunta 1, que contiene dos programas en Lua:

1)  **`pregunta1-b-1.lua`**
   - Función: rotar(w, k) -> rota la cadena `w` k veces.
   - Uso desde la terminal:
     `lua pregunta1-b-1.lua <cadena_w> <k>`

     Ejemplo: `lua pregunta1-b-1.lua hola 2`

   - Modo test (ejecuta ejemplos):
     `lua pregunta1-b-1.lua test`

2)  **`pregunta1-b-2.lua`**
   - Función: calcular A × A^T para una matriz cuadrada NxN.
   - Modo de uso:
     `lua pregunta1-b-2.lua <N> <lista_de_NxN_enteros>`

     Ejemplo: para N=2 y matriz [[1,2],[2,1]]:
       `lua pregunta1-b-2.lua 2 1 2 2 1`

   - Si no se proporcionan suficientes valores en la línea de comandos, el programa solicitará las filas por stdin.
   - Modo test (ejecuta ejemplo 3x3):
     `lua pregunta1-b-2.lua test`
