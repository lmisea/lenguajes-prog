-- Módulo Vec3: vectores tridimensionales y operadores
local Vec3 = {}
Vec3.__index = Vec3

-- Instrumentación simple de cobertura por funciones
Vec3.__covList = {"new","add","sub","mul_vec","mul_scalar","dot","norm","tostring"}
Vec3.__covHits = {}
local function mark_cov(name) Vec3.__covHits[name] = true end
function Vec3.coverage()
    local total = #Vec3.__covList
    local hit = 0
    for _, n in ipairs(Vec3.__covList) do if Vec3.__covHits[n] then hit = hit + 1 end end
    return hit, total, (hit/total)*100
end

-- Constructor
function Vec3.new(x,y,z)
    mark_cov("new")
    local v = {x = x or 0, y = y or 0, z = z or 0}
    setmetatable(v, Vec3)
    return v
end

-- Permitir llamado como Vec3(x,y,z)
setmetatable(Vec3, {__call = function(_,x,y,z) return Vec3.new(x,y,z) end})

local function isvec(v) return type(v) == "table" and getmetatable(v) == Vec3 end

-- suma: vector + vector ó vector + scalar (por la derecha)
function Vec3.__add(a,b)
    mark_cov("add")
    if isvec(b) then
        return Vec3.new(a.x + b.x, a.y + b.y, a.z + b.z)
    elseif type(b) == "number" then
        return Vec3.new(a.x + b, a.y + b, a.z + b)
    else
        error("Operando inválido para +")
    end
end

-- resta: vector - vector ó vector - scalar (por la derecha)
function Vec3.__sub(a,b)
    mark_cov("sub")
    if isvec(b) then
        return Vec3.new(a.x - b.x, a.y - b.y, a.z - b.z)
    elseif type(b) == "number" then
        return Vec3.new(a.x - b, a.y - b, a.z - b)
    else
        error("Operando inválido para -")
    end
end

-- multiplicación: si b es vector -> producto cruz; si b es número -> escala (por la derecha)
function Vec3.__mul(a,b)
    if isvec(b) then
        mark_cov("mul_vec")
        -- cross product
        return Vec3.new(
            a.y*b.z - a.z*b.y,
            a.z*b.x - a.x*b.z,
            a.x*b.y - a.y*b.x
        )
    elseif type(b) == "number" then
        mark_cov("mul_scalar")
        return Vec3.new(a.x * b, a.y * b, a.z * b)
    else
        error("Operando inválido para *")
    end
end

-- módulo % como producto punto (dot)
function Vec3.__mod(a,b)
    mark_cov("dot")
    if not isvec(b) then error("El operador % requiere otro vector") end
    return a.x*b.x + a.y*b.y + a.z*b.z
end

-- norma: usaremos el operador # (length) como norma euclidiana
-- Nota: el enunciado pedía '&' pero Lua no tiene operador unario '&'. Usamos '#' en su lugar.
function Vec3.__len(a)
    mark_cov("norm")
    return math.sqrt(a.x*a.x + a.y*a.y + a.z*a.z)
end

function Vec3.__tostring(a)
    mark_cov("tostring")
    return string.format("(%.3f, %.3f, %.3f)", a.x, a.y, a.z)
end

-- Exportar
return Vec3
