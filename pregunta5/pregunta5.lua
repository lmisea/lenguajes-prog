local Tmod = require("./tmodel")

local function usage()
    io.write("Uso: lua pregunta5.lua test\n")
    io.write("  O: lua pregunta5.lua demo\n")
end

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

if #arg == 0 then usage(); os.exit(1) end
if arg[1] == "test" then run_tests(); os.exit(0) end
if arg[1] == "demo" then demo(); os.exit(0) end
