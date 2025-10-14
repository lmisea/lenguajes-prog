-- Archivo de pruebas para el módulo buddy.lua
local Buddy = require("./buddy")

local function run()
    local passed = 0
    local total = 0

    local function ok(name, fn)
        total = total + 1
        local status, err = pcall(fn)
        if status then passed = passed + 1; io.write("✓ "..name.."\n")
        else io.write("✗ "..name.." -> "..tostring(err).."\n") end
    end

    ok("create manager", function()
        local m, err = Buddy.new(16)
        assert(m ~= nil, err)
    end)

    ok("reserve and free", function()
        local m = Buddy.new(16)
        assert(m, "No se pudo crear el manager")
        local ok, msg = m:reserve(4, "p1")
        assert(ok == true, msg)
        local ok2, msg2 = m:free("p1")
        assert(ok2 == true, msg2)
    end)

    ok("duplicate name", function()
        local m = Buddy.new(16)
        assert(m, "No se pudo crear el manager")
        local ok1, msg1 = m:reserve(2, "p")
        assert(ok1 == true, msg1)
        local ok2, msg2 = m:reserve(1, "p")
        assert(ok2 == false)
    end)

    ok("exceed memory", function()
        local m = Buddy.new(8)
        assert(m, "No se pudo crear el manager")
        local ok, msg = m:reserve(16, "x")
        assert(ok == false)
    end)

    ok("coverage helpers", function()
        local m = Buddy.new(16)
        assert(m, "No se pudo crear el manager")
        -- Ejercitar display
        m:display()
        -- Ejercitar allocate_block_at: extraer y volver a insertar el bloque superior
        local idx = m.max_index
        assert(type(idx) == "number")
        local b = m:allocate_block_at(idx)
        assert(b and b.size == 16)
        table.insert(m.free_lists[idx], b)
    end)

    io.write(string.format("\nTests passed: %d/%d\n", passed, total))
    -- comprobación de cobertura
    local ok, buddy = pcall(require, "./buddy")
    if ok and buddy and buddy.coverage then
        local hit, tot, pct = buddy.coverage()
        io.write(string.format("Coverage: %d/%d (%.1f%%)\n", hit, tot, pct))
        if pct < 80 then io.write("Coverage below 80%\n"); os.exit(2) end
    end

    if passed ~= total then os.exit(1) end
end

if ... == nil or ... == "run" then run() end
