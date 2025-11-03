# Pregunta 5 - Modelo T (programas, intérpretes y traductores)

Modelo que permite definir programas en lenguajes, intérpretes y traductores, y comprobar si un programa es ejecutable en `LOCAL`.

Archivos principales:
- Módulo: [`tmodel.lua`](tmodel.lua) (exporta `T`, constructor: [`T.new`](tmodel.lua))
- Cliente/demo: [`pregunta5.lua`](pregunta5.lua)
- Tests: [`test_pregunta5.lua`](test_pregunta5.lua)

Uso:
- Ejecutar en modo interactivo:
  ```
  lua pregunta5.lua
  ```
- Ejecutar demo:
  ```
  lua pregunta5.lua demo
  ```
- Ejecutar tests:
  ```
  lua test_pregunta5.lua
  ```
  o
  ```
  lua pregunta5.lua test
  ```
