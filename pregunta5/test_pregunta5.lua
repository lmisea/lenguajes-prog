local Tmod = require("./tmodel")

local function run()
    local passed, total = 0, 0
    local function ok(name, fn)
        total = total + 1
        local s, err = pcall(fn)
        if s then passed = passed + 1; io.write("✓ "..name.."\n")
        else io.write("✗ "..name.." -> "..tostring(err).."\n") end
    end

    ok("create model", function()
        local m = Tmod.new()
        assert(m)
    end)

    ok("define program and interpreter (direct)", function()
        local m = Tmod.new()
        assert(m:define_program("P","L1"))
        assert(m:define_interpreter("L1","LOCAL"))
        local ok, msg = m:can_execute("P")
        assert(ok == true)
    end)

    ok("define translator chain", function()
        local m = Tmod.new()
        assert(m:define_program("Q","L2"))
        assert(m:define_translator("base","L2","L1"))
        assert(m:define_interpreter("L1","LOCAL"))
        local ok, msg = m:can_execute("Q")
        assert(ok == true)
        local path, err = m:resolve_execution_path("Q")
        assert(path and #path >= 2)
    end)

    ok("program in LOCAL", function()
        local m = Tmod.new()
        assert(m:define_program("R","LOCAL"))
        local ok = select(1, m:can_execute("R"))
        assert(ok == true)
    end)

    ok("no path returns false", function()
        local m = Tmod.new()
        assert(m:define_program("S","Lx"))
        local ok, msg = m:can_execute("S")
        assert(ok == false)
    end)

    ok("errors on duplicate or invalid defs", function()
        local m = Tmod.new()
        assert(m:define_program("A","L"))
        local ok, msg = m:define_program("A","L")
        assert(ok == false)
        local ok2, msg2 = m:define_interpreter("","L")
        assert(ok2 == false)
    end)

    io.write(string.format("\nTests passed: %d/%d\n", passed, total))
    local ok, tmod = pcall(require, "./tmodel")
    if ok and tmod and tmod.coverage then
        local hit, tot, pct = tmod.coverage()
        io.write(string.format("Coverage: %d/%d (%.1f%%)\n", hit, tot, pct))
        if pct < 80 then io.write("Coverage below 80%\n"); os.exit(2) end
    end

    if passed ~= total then os.exit(1) end
end

if ... == nil or ... == "run" then run() end
