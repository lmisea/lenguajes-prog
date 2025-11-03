-- Modelo T: programas, intérpretes y traductores
local T = {}
T.__index = T

-- Instrumentación simple de cobertura
T.__covList = {"new","define_program","define_interpreter","define_translator","can_execute","resolve_execution_path"}
T.__covHits = {}
local function mark_cov(n) T.__covHits[n] = true end
function T.coverage()
    local tot = #T.__covList; local hit = 0
    for _,n in ipairs(T.__covList) do if T.__covHits[n] then hit = hit + 1 end end
    return hit, tot, (hit/tot)*100
end

function T.new()
    mark_cov("new")
    local self = setmetatable({}, T)
    -- estructuras de datos
    self.programs = {} -- name -> language
    self.interpreters = {} -- base_lang -> set of target langs
    self.translators = {} -- base -> map[from] = set(to)
    return self
end

local function ensure_set(tbl, key)
    if not tbl[key] then tbl[key] = {} end
    return tbl[key]
end

-- Definir PROGRAMA <nombre> <lenguaje>
function T:define_program(name, lang)
    mark_cov("define_program")
    if type(name) ~= "string" or name == "" then return false, "Nombre de programa inválido" end
    if type(lang) ~= "string" or lang == "" then return false, "Lenguaje inválido" end
    if self.programs[name] then return false, "Programa ya definido" end
    self.programs[name] = lang
    return true
end

-- Definir INTERPRETE <lenguaje_base> <lenguaje>
function T:define_interpreter(base, lang)
    mark_cov("define_interpreter")
    if type(base) ~= "string" or base == "" or type(lang) ~= "string" or lang == "" then
        return false, "Argumentos inválidos"
    end
    local s = ensure_set(self.interpreters, base)
    s[lang] = true
    return true
end

-- Definir TRADUCTOR <lenguaje_base> <lenguaje_origen> <lenguaje_destino>
function T:define_translator(base, from, to)
    mark_cov("define_translator")
    if type(base) ~= "string" or base == "" then return false, "Argumentos inválidos" end
    if type(from) ~= "string" or type(to) ~= "string" then return false, "Argumentos inválidos" end
    self.translators[base] = self.translators[base] or {}
    self.translators[base][from] = self.translators[base][from] or {}
    self.translators[base][from][to] = true
    return true
end

-- Ver si un programa es ejecutable en lenguaje LOCAL (relaciones transitivas usando intérpretes y traductores)
function T:can_execute(program_name)
    mark_cov("can_execute")
    local lang = self.programs[program_name]
    if not lang then return false, "Programa no definido" end
    -- si ya es LOCAL
    if lang == "LOCAL" then return true end
    -- intentar resolver camino hacia LOCAL
    local visited = {}
    local function dfs(current_lang)
        if current_lang == "LOCAL" then return true end
        if visited[current_lang] then return false end
        visited[current_lang] = true
        -- intérpretes: desde current_lang podemos ejecutar targets directly
        local ints = self.interpreters[current_lang]
        if ints then
            for t,_ in pairs(ints) do
                if t == "LOCAL" or dfs(t) then return true end
            end
        end
        -- traductores: need to consider base languages entries: for each base, translations available
        for base, map in pairs(self.translators) do
            -- only translators defined under this base apply if current_lang is "from" and base is reachable from current_lang
            local tos = map[current_lang]
            if tos then
                for to,_ in pairs(tos) do
                    if to == "LOCAL" or dfs(to) then return true end
                end
            end
        end
        return false
    end
    if dfs(lang) then return true end
    return false, "No se encontró camino de ejecución hacia LOCAL"
end

-- Función auxiliar para resolver pasos (para mostrar path) - BFS limitado
function T:resolve_execution_path(program_name)
    mark_cov("resolve_execution_path")
    local lang = self.programs[program_name]
    if not lang then return nil, "Programa no definido" end
    if lang == "LOCAL" then return {program_name.." (LOCAL)"} end
    -- BFS
    local queue = {}
    table.insert(queue, {lang, {lang}})
    local seen = {}
    seen[lang] = true
    while #queue > 0 do
        local item = table.remove(queue, 1)
        local cur = item[1]
        local path = item[2]
        if cur == "LOCAL" then
            return path
        end

        -- interpreters: desde cur podemos ir a cada target t
        local ints = self.interpreters[cur]
        if ints then
            for t,_ in pairs(ints) do
                if not seen[t] then
                    seen[t] = true
                    -- copiar path y añadir t
                    local p2 = {}
                    for i = 1, #path do p2[i] = path[i] end
                    table.insert(p2, t)
                    table.insert(queue, {t, p2})
                end
            end
        end

        -- translators: buscar traducciones desde cur
        for base, map in pairs(self.translators) do
            local tos = map[cur]
            if tos then
                for t,_ in pairs(tos) do
                    if not seen[t] then
                        seen[t] = true
                        local p2 = {}
                        for i = 1, #path do p2[i] = path[i] end
                        table.insert(p2, t)
                        table.insert(queue, {t, p2})
                    end
                end
            end
        end
    end
    return nil, "No hay camino hacia LOCAL"
end

return T
