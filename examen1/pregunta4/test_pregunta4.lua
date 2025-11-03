-- Archivo de pruebas para el módulo vec3.lua
local Vec3 = require("./vec3")

local function almost_eq(a,b,eps)
    eps = eps or 1e-6
    return math.abs(a-b) <= eps
end

local function run()
    local passed, total = 0,0
    local function ok(name, f)
        total = total + 1
        local s, err = pcall(f)
        if s then passed = passed + 1; io.write("✓ "..name.."\n")
        else io.write("✗ "..name.." -> "..tostring(err).."\n") end
    end

    ok("constructor and tostring", function()
        local a = Vec3(1,2,3)
        assert(a.x==1 and a.y==2 and a.z==3)
        local s = tostring(a)
        assert(type(s)=="string")
    end)

    ok("add vec and scalar", function()
        local a = Vec3(1,1,1)
        local b = a + 3
        assert(b.x==4 and b.y==4 and b.z==4)
    end)

    ok("add vec+vec and sub", function()
        local a = Vec3(1,2,3)
        local b = Vec3(3,2,1)
        local c = a + b
        assert(c.x==4 and c.y==4 and c.z==4)
        local d = b - a
        assert(d.x==2 and d.y==0 and d.z==-2)
    end)

    ok("cross product and dot", function()
        local a = Vec3(1,0,0)
        local b = Vec3(0,1,0)
        local c = a * b -- cross -> should be (0,0,1)
        assert(c.x==0 and c.y==0 and c.z==1)
        local dp = a % b
        assert(dp == 0)
    end)

    ok("scalar multiply and combined expr", function()
        local a = Vec3(1,2,3)
        local b = a * 3
        assert(b.x==3 and b.y==6 and b.z==9)
        -- a * b + a  (cross product then +)
        local res = (Vec3(1,0,0) * Vec3(0,1,0)) + Vec3(1,1,1)
        assert(res.x==1 and res.y==1 and res.z==2)
    end)

    ok("norm (#) operator", function()
        local a = Vec3(3,4,0)
        local n = #a
        assert(almost_eq(n,5))
    end)

    io.write(string.format("\nTests passed: %d/%d\n", passed, total))

    -- comprobación de cobertura simple
    local ok, vec = pcall(require, "./vec3")
    if ok and vec and vec.coverage then
        local hit, tot, pct = vec.coverage()
        io.write(string.format("Coverage: %d/%d (%.1f%%)\n", hit, tot, pct))
        if pct < 80 then io.write("Coverage below 80%\n"); os.exit(2) end
    end

    if passed ~= total then os.exit(1) end
end

if ... == nil or ... == "run" then run() end
