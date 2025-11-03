# Pregunta 2 — Evaluador de expresiones (PRE/POST)

Programa en Python que evalúa expresiones aritméticas escritas en notación prefija (PRE) o
postfija (POST) y también muestra la representación en notación infija con la menor cantidad
posible de paréntesis necesaria para mantener la semántica (precedencia y asociatividad
estándar, operadores + - * / con división entera).

Archivos principales:
- `pregunta2.py` — implementación del parser, evaluador y REPL.
- `test_pregunta2.py` — pruebas unitarias usando `pytest`.

Uso rápido (REPL):

1. Ejecutar el programa:

```bash
python3 pregunta2.py
```

2. En el prompt, escribir comandos:

- Evaluar una expresión en prefijo:

  EVAL PRE + * + 3 4 5 7

  (imprime `42`)

- Evaluar una expresión en postfijo:

  EVAL POST 8 3 - 8 4 4 + * +

  (imprime `69`)

- Mostrar en notación infija con mínimos paréntesis:

  MOSTRAR PRE + * + 3 4 5 7

  (imprime `(3 + 4) * 5 + 7`)

- Salir del REPL:

  SALIR

Pruebas unitarias:

Las pruebas están en `test_pregunta2.py` pero para ejecutarlas se necesita instalar dependencias externas:

```bash
# instalar dependencias (usuario/local)
python3 -m pip install --user -r requirements.txt
```

Una vez instaladas las dependencias, puedes ejecutar las pruebas bajo coverage con:

```bash
# ejecutar pytest con coverage y mostrar reporte
coverage run -m pytest -q
coverage report -m
```

También puedes ejecutar pytest directamente:

```bash
pytest -q
```

Pero esto no medirá la cobertura, para eso si es necesario usar coverage como se mostró antes.

**Nota:** Es recomendable estar en la carpeta `pregunta2` al ejecutar las pruebas para usar los comandos tal como se indican en este README.

Las pruebas incluidas cubren evaluación PRE/POST, la conversión a infija y casos de asociatividad
que requieren o no paréntesis.
