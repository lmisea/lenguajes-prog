# Pregunta 3 - Gestor de memoria "Buddy"

Este módulo implementa un gestor de memoria tipo Buddy.

Archivos principales:
- Módulo: [`buddy.lua`](buddy.lua) (exporta `BuddyMemoryManager`, constructor: [`BuddyMemoryManager.new`](buddy.lua))
- Cliente CLI: [`pregunta3.lua`](pregunta3.lua)
- Tests: [`test_buddy.lua`](test_buddy.lua)

Uso:
- Ejecutar demo/cliente interactivo:
  ```
  lua pregunta3.lua <bloques_total>
  ```
  Ejemplo:
  ```
  lua pregunta3.lua 16
  ```
  `<bloques_total>` debe ser potencia de 2.
- Ejecutar tests:
  ```
  lua test_buddy.lua
  ```
  o
  ```
  lua pregunta3.lua test
  ```
