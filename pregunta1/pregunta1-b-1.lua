function rotar(w, k)
    -- Caso base: si k = 0 o la cadena es vacía
    if k == 0 or #w == 0 then
        return w
    end

    -- Caso recursivo: si k > 0 ∧ w = ax ∧ a es un caracter
    if k > 0 then
        local a = string.sub(w, 1, 1) -- a es el primer caracter
        local x = string.sub(w, 2)    -- x es el resto de la cadena

        -- rotar(x ++ [a], k - 1)
        return rotar(x .. a, k - 1)
    end

    return w -- si k < 0 devolvemos la cadena sin cambios
end

local function usage()
    print("Uso: lua pregunta1-b-1.lua <cadena_w> <k>")
    print("  O: lua pregunta1-b-1.lua test  -> ejecuta pruebas internas")
end

local function run_tests()
    print("rotar('hola', 0) = " .. rotar("hola", 0))
    print("rotar('hola', 1) = " .. rotar("hola", 1))
    print("rotar('hola', 2) = " .. rotar("hola", 2))
    print("rotar('hola', 3) = " .. rotar("hola", 3))
    print("rotar('hola', 4) = " .. rotar("hola", 4))
    print("rotar('hola', 5) = " .. rotar("hola", 5))
end

if #arg == 0 then
    usage()
    os.exit(1)
end

if arg[1] == "test" then
    run_tests()
    os.exit(0)
end

local w = arg[1]
local k = tonumber(arg[2]) or 0
print(rotar(w, k))
