local Tmod = require("./tmodel")

local function run_tests()
    local cmd = 'lua test_pregunta5.lua'
    local res = os.execute(cmd)
    if not res then io.write("Error al ejecutar tests\n"); os.exit(1) end
end

local function demo()
    local m = Tmod.new()
    m:define_program("prog", "LangA")
    m:define_interpreter("LangA","LOCAL")
    io.write("Programa 'prog' definido en LangA y se añadió intérprete a LOCAL\n")
    local ok = select(1, m:can_execute("prog"))
    io.write("¿Executable en LOCAL? "..tostring(ok).."\n")
end

local function interactive()
    local m = Tmod.new()
    io.write("Modelo T interactivo. Comandos: \n")
    io.write("  DEFINIR PROGRAMA <nombre> <lenguaje>\n")
    io.write("  DEFINIR INTERPRETE <lenguaje_base> <lenguaje>\n")
    io.write("  DEFINIR TRADUCTOR <lenguaje_base> <origen> <destino>\n")
    io.write("  EJECUTABLE <nombre>\n")
    io.write("  SALIR\n")

    while true do
        io.write("> ")
        io.flush()
        local line = io.read()
        if not line then break end
        local parts = {}
        for p in line:gmatch("%S+") do table.insert(parts, p) end
        if #parts == 0 then -- ignore
        elseif parts[1]:upper() == "SALIR" then
            io.write("Saliendo...\n")
            break
        elseif parts[1]:upper() == "DEFINIR" and parts[2] then
            local kind = parts[2]:upper()
            if kind == "PROGRAMA" and #parts == 4 then
                local name = parts[3]; local lang = parts[4]
                local ok, msg = m:define_program(name, lang)
                if ok then io.write("✓ Programa definido\n") else io.write("✗ Error: "..tostring(msg).."\n") end
            elseif kind == "INTERPRETE" and #parts == 4 then
                local base = parts[3]; local lang = parts[4]
                local ok, msg = m:define_interpreter(base, lang)
                if ok then io.write("✓ Intérprete definido\n") else io.write("✗ Error: "..tostring(msg).."\n") end
            elseif kind == "TRADUCTOR" and #parts == 5 then
                local base = parts[3]; local from = parts[4]; local to = parts[5]
                local ok, msg = m:define_translator(base, from, to)
                if ok then io.write("✓ Traductor definido\n") else io.write("✗ Error: "..tostring(msg).."\n") end
            else
                io.write("Error: formato DEFINIR incorrecto. Ejemplos:\n")
                io.write("  DEFINIR PROGRAMA <nombre> <lenguaje>\n")
                io.write("  DEFINIR INTERPRETE <lenguaje_base> <lenguaje>\n")
                io.write("  DEFINIR TRADUCTOR <lenguaje_base> <origen> <destino>\n")
            end
        elseif parts[1]:upper() == "EJECUTABLE" and #parts == 2 then
            local name = parts[2]
            local ok, msg = m:can_execute(name)
            if ok then
                io.write("✓ El programa es ejecutable en LOCAL\n")
                local path, err = m:resolve_execution_path(name)
                if path then
                    io.write("Camino: ")
                    for i, v in ipairs(path) do io.write(v .. (i<#path and " -> " or "\n")) end
                end
            else
                io.write("✗ No ejecutable: "..tostring(msg).."\n")
            end
        else
            io.write("Comando no reconocido. Use DEFINIR, EJECUTABLE o SALIR.\n")
        end
    end
end

-- Entry point
if #arg == 0 then
    -- por defecto, iniciar modo interactivo
    interactive(); os.exit(0)
end
if arg[1] == "test" then run_tests(); os.exit(0) end
if arg[1] == "demo" then demo(); os.exit(0) end
