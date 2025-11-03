-- Este archivo es un cliente CLI para el módulo buddy.lua
local buddy = require("./buddy")

local function usage()
    io.write("Uso: lua pregunta3.lua <bloques_total>\n")
    io.write("  O: lua pregunta3.lua test   -> Ejecutar pruebas unitarias\n")
end

local function run_tests_cli()
    -- Ejecutar el script de pruebas en un proceso separado para que su salida
    -- se muestre en la terminal (igual que `lua test_buddy.lua`).
    local cmd = 'lua test_buddy.lua'
    local res = os.execute(cmd)
    if not res then
        io.write("Error al ejecutar pruebas (os.execute retornó falso)\n")
        os.exit(1)
    end
end

local function interactive(total_blocks)
    local manager, err = buddy.new(total_blocks)
    if not manager then io.write("Error al crear el manager: " .. tostring(err) .. "\n"); os.exit(1) end

    io.write(string.format("Buddy System iniciado con %d bloques de memoria\n", total_blocks))
    io.write("Comandos disponibles: RESERVAR <tamaño> <nombre>, LIBERAR <nombre>, MOSTRAR, SALIR\n")

    while true do
        io.write("> ")
        io.flush()
        local input = io.read()
        if not input then break end
        local parts = {}
        for part in input:gmatch("%S+") do table.insert(parts, part) end

        if #parts == 0 then
        elseif parts[1]:upper() == "SALIR" then
            io.write("Saliendo del programa...\n")
            break
        elseif parts[1]:upper() == "MOSTRAR" then
            manager:display()
        elseif parts[1]:upper() == "RESERVAR" and #parts == 3 then
            local size = tonumber(parts[2])
            local name = parts[3]
            if not size or size <= 0 then io.write("Error: El tamaño debe ser un número positivo\n")
            else
                local ok, msg = manager:reserve(size, name)
                if ok then io.write("✓ " .. msg .. "\n") else io.write("✗ Error: " .. msg .. "\n") end
            end
        elseif parts[1]:upper() == "LIBERAR" and #parts == 2 then
            local name = parts[2]
            local ok, msg = manager:free(name)
            if ok then io.write("✓ " .. msg .. "\n") else io.write("✗ Error: " .. msg .. "\n") end
        else
            io.write("Error: Comando no reconocido o formato incorrecto\n")
            io.write("Formato correcto:\n  RESERVAR <cantidad> <nombre>\n  LIBERAR <nombre>\n  MOSTRAR\n  SALIR\n")
        end
    end
end

-- Entry point
if #arg == 0 then usage(); os.exit(1) end
if arg[1] == "test" then run_tests_cli(); os.exit(0) end

local total_blocks = tonumber(arg[1])
if not total_blocks then usage(); os.exit(1) end
if total_blocks <= 0 or (total_blocks & (total_blocks - 1)) ~= 0 then io.write("Error: El número de bloques debe ser una potencia de 2\n"); os.exit(1) end

interactive(total_blocks)
