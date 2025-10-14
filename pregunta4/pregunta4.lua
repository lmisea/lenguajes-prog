
-- Cliente para el módulo vec3
local vec3 = require("./vec3")

local function usage()
	io.write("Uso: lua pregunta4.lua test\n")
	io.write("  O: lua pregunta4.lua demo   -> ejecuta una demo de operaciones\n")
end

local function run_tests()
	local cmd = 'lua test_pregunta4.lua'
	local res = os.execute(cmd)
	if not res then io.write("Error al ejecutar tests\n"); os.exit(1) end
end

local function demo()
	local Vec3 = require("./vec3")
	local a = Vec3(1,2,3)
	local b = Vec3(3,1,0)
	local c = Vec3(0,1,2)
	io.write("a = "..tostring(a) .."\n")
	io.write("b = "..tostring(b) .."\n")
	io.write("c = "..tostring(c) .."\n")
	io.write("b + 3 = "..tostring(b + 3) .."\n")
	io.write("a * b + c = "..tostring((a * b) + c) .."\n")
	io.write("(b + b) * (c - a) = "..tostring((b + b) * (c - a)) .."\n")
	io.write("a % (c * b) = "..tostring(a % (c * b)) .."\n")
	io.write("#b = "..tostring(#b) .."\n")
end

if #arg == 0 then usage(); os.exit(1) end
if arg[1] == "test" then run_tests(); os.exit(0) end
if arg[1] == "demo" then demo(); os.exit(0) end
