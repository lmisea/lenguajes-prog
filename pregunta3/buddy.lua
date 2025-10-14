
-- Módulo: gestor de memoria Buddy
local BuddyMemoryManager = {}
BuddyMemoryManager.__index = BuddyMemoryManager

-- Instrumentación simple de cobertura (auto-contenida)
BuddyMemoryManager.__covList = {"new", "find_index_for_size", "allocate_block_at", "reserve", "find_buddy_start", "free", "display"}
BuddyMemoryManager.__covHits = {}

local function mark_cov(name)
    BuddyMemoryManager.__covHits[name] = true
end

function BuddyMemoryManager.coverage()
    local total = #BuddyMemoryManager.__covList
    local hit = 0
    for _, n in ipairs(BuddyMemoryManager.__covList) do
        if BuddyMemoryManager.__covHits[n] then hit = hit + 1 end
    end
    return hit, total, (hit / total) * 100
end

-- Comprueba si un número es potencia de dos
local function is_power_of_two(n)
    return n > 0 and (n & (n - 1)) == 0
end

function BuddyMemoryManager.new(total_blocks)
    mark_cov("new")
    if type(total_blocks) ~= "number" or total_blocks <= 0 or not is_power_of_two(total_blocks) then
        return nil, "La cantidad de bloques debe ser una potencia de 2 positiva"
    end

    local self = setmetatable({}, BuddyMemoryManager)
    self.total_blocks = total_blocks
    self.max_index = math.floor(math.log(total_blocks, 2))
    self.blocks = {} -- map block index -> allocation name (for display)
    self.allocations = {} -- name -> {start, size, requested}
    self.free_lists = {}
    for i = 0, self.max_index do self.free_lists[i] = {} end

    -- inicialmente toda la memoria está libre
    table.insert(self.free_lists[self.max_index], {start = 0, size = total_blocks})

    return self
end

function BuddyMemoryManager:find_index_for_size(size)
    mark_cov("find_index_for_size")
    if size <= 0 then return nil, "El tamaño debe ser positivo" end
    local s = 1
    local idx = 0
    while s < size do s = s * 2; idx = idx + 1 end
    return idx
end

function BuddyMemoryManager:allocate_block_at(index)
    mark_cov("allocate_block_at")
    -- tomar un bloque de free_lists[index]; devolverlo o nil
    if #self.free_lists[index] == 0 then return nil end
    return table.remove(self.free_lists[index], 1)
end

function BuddyMemoryManager:reserve(size, name)
    mark_cov("reserve")
    if type(name) ~= "string" or name == "" then return false, "El nombre debe ser una cadena no vacía" end
    if self.allocations[name] then return false, "Ya existe una reserva con ese nombre" end
    if type(size) ~= "number" or size <= 0 then return false, "El tamaño debe ser positivo" end
    if size > self.total_blocks then return false, "El tamaño solicitado excede la memoria total" end

    local target_index = self:find_index_for_size(size)
    if not target_index then return false, "Tamaño inválido" end

    -- buscar un bloque libre en target_index o por encima
    local i = target_index
    while i <= self.max_index and #self.free_lists[i] == 0 do i = i + 1 end
    if i > self.max_index then return false, "No hay memoria suficiente" end

    -- tomar bloque del nivel i y partirlo hasta target_index
    local block = table.remove(self.free_lists[i], 1)
    while i > target_index do
        i = i - 1
        local half = block.size / 2
        local left = {start = block.start, size = half}
        local right = {start = block.start + half, size = half}
        -- mantener left para seguir dividiendo/allocando, poner right en la lista libre
        table.insert(self.free_lists[i], right)
        block = left
    end

    -- asignar bloque
    self.allocations[name] = {start = block.start, size = block.size, requested = size}
    for idx = block.start, block.start + block.size - 1 do self.blocks[idx] = name end

    return true, "Reserva exitosa"
end

function BuddyMemoryManager:find_buddy_start(start, size)
    mark_cov("find_buddy_start")
    return start ~ size
end

function BuddyMemoryManager:free(name)
    mark_cov("free")
    if not self.allocations[name] then return false, "No existe una reserva con ese nombre" end
    local alloc = self.allocations[name]
    -- limpiar bloques
    for i = alloc.start, alloc.start + alloc.size - 1 do self.blocks[i] = nil end

    -- intentar fusionar hacia arriba
    local block = {start = alloc.start, size = alloc.size}
    local index = math.floor(math.log(block.size, 2))

    while index < self.max_index do
        local buddy_start = self:find_buddy_start(block.start, block.size)
        local buddy_index = nil
        for k, b in ipairs(self.free_lists[index]) do
            if b.start == buddy_start and b.size == block.size then
                buddy_index = k
                break
            end
        end

        if buddy_index then
            -- eliminar el buddy
            table.remove(self.free_lists[index], buddy_index)
            -- fusionar
            block.start = math.min(block.start, buddy_start)
            block.size = block.size * 2
            index = index + 1
        else
            break
        end
    end

    -- insertar el bloque (posiblemente fusionado) en la lista libre
    table.insert(self.free_lists[index], block)

    -- eliminar asignación
    self.allocations[name] = nil
    return true, "Liberación exitosa"
end

function BuddyMemoryManager:display()
    mark_cov("display")
    io.write("\n=== ESTADO DE LA MEMORIA ===\n")
    io.write("Bloques totales: " .. self.total_blocks .. "\n")
    local line = "Memoria: ["
    for i = 0, self.total_blocks - 1 do
        if self.blocks[i] then
            line = line .. self.blocks[i]:sub(1,1)
        else
            line = line .. "."
        end
    end
    line = line .. "]\n"
    io.write(line)

    io.write("\nAsignaciones:\n")
    if next(self.allocations) == nil then
        io.write("  No hay asignaciones\n")
    else
        for name, a in pairs(self.allocations) do
            io.write(string.format("  %s: bloques %d-%d (tamaño: %d, solicitado: %d)\n",
                name, a.start, a.start + a.size - 1, a.size, a.requested))
        end
    end

    io.write("\nBloques libres por tamaño:\n")
    local has_free = false
    for i = 0, self.max_index do
        if #self.free_lists[i] > 0 then
            has_free = true
            local size = 2 ^ i
            local s = ""
            for _, b in ipairs(self.free_lists[i]) do
                s = s .. string.format(" [%d-%d]", b.start, b.start + size - 1)
            end
            io.write(string.format("  Tamaño %d: %s\n", size, s))
        end
    end
    if not has_free then io.write("  No hay bloques libres\n") end
    io.write("============================\n\n")
end

return BuddyMemoryManager
