-- Funcion para calcular la transpuesta de una matriz
function transpuesta(A)
    local N = #A
    local AT = {}

    for i = 1, N do
        AT[i] = {}
        for j = 1, N do
            AT[i][j] = A[j][i]  -- ATi,j = Aj,i
        end
    end

    return AT
end

-- Funcion para multiplicar dos matrices
function multiplicarMatrices(A, B)
    local N = #A
    local C = {}  -- Matriz resultado

    for i = 1, N do
        C[i] = {}
        for j = 1, N do
            local suma = 0
            for k = 1, N do
                -- (A × B)i,j = sum_{k=1}^N Ai,k × Bk,j
                suma = suma + A[i][k] * B[k][j]
            end
            C[i][j] = suma
        end
    end

    return C
end

-- Funcion principal: calcular A × AT
function productoPorTranspuesta(A)
    local AT = transpuesta(A)
    return multiplicarMatrices(A, AT)
end

-- Funcion auxiliar para imprimir una matriz
function imprimirMatriz(matriz, nombre)
    print(nombre .. ":")
    for i = 1, #matriz do
        local fila = ""
        for j = 1, #matriz do
            fila = fila .. string.format("%6d", matriz[i][j])
        end
        print(fila)
    end
    print()
end

-- Ejemplo de uso
local function usage()
    print("Uso: lua pregunta1-b-2.lua <N> <lista_de_NxN_enteros>")
    print("  Ejemplo: lua pregunta1-b-2.lua 2 1 2 2 1")
    print("  O: lua pregunta1-b-2.lua test   -> ejecuta ejemplo interno")
end

local function run_test()
    local A = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    }
    print("Matriz original A:")
    imprimirMatriz(A, "A")
    local AT = transpuesta(A)
    imprimirMatriz(AT, "AT (Transpuesta de A)")
    local A_por_AT = productoPorTranspuesta(A)
    imprimirMatriz(A_por_AT, "A × AT")
end

if #arg == 0 then usage(); os.exit(1) end
if arg[1] == "test" then run_test(); os.exit(0) end

local N = tonumber(arg[1])
if not N or N <= 0 then print("N inválido"); usage(); os.exit(1) end

-- Leer N*N valores de los argumentos siguientes; si faltan, pedir por stdin
local vals = {}
for i = 2, #arg do table.insert(vals, tonumber(arg[i])) end
local need = N * N
local idx = 1
while #vals < need do
    io.write(string.format("Falta %d valores, ingrese la fila %d (separados por espacios): ", need - #vals, math.floor(#vals / N) + 1))
    io.flush()
    local line = io.read()
    if not line then break end
    for num in line:gmatch("%-?%d+") do table.insert(vals, tonumber(num)) end
end

if #vals < need then print("No se recibieron suficientes valores"); os.exit(1) end

local A = {}
for i = 1, N do
    A[i] = {}
    for j = 1, N do
        A[i][j] = vals[idx]; idx = idx + 1
    end
end

print("Matriz original A:")
imprimirMatriz(A, "A")
local AT = transpuesta(A)
imprimirMatriz(AT, "AT (Transpuesta de A)")
local A_por_AT = productoPorTranspuesta(A)
imprimirMatriz(A_por_AT, "A × AT")
