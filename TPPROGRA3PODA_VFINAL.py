import heapq

# Inicializar el grafo
grafo = {}
data = """origen,destino,costo
1,2,10
2,1,10
2,3,10
3,2,10
1,28,8
28,1,8
28,50,11
50,28,11
1,3,12
3,1,12
3,50,10
50,3,10
3,4,8
4,3,8
51,4,9
4,51,9
3,5,4
5,3,4
5,51,3
51,5,3
6,5,9
5,6,9
6,7,8
7,6,8
7,8,4
8,7,4
8,51,10
51,8,10
8,10,12
10,8,12
9,10,9
10,9,9
10,11,6
11,10,6
11,12,5
12,11,5
12,13,6
13,12,6
11,14,8
14,11,8
14,15,8
15,14,8
15,16,9
16,15,9
15,20,6
20,15,6
13,20,4
20,13,4
20,18,2
18,20,2
17,18,6
18,17,6
18,19,7
19,18,7
19,23,6
23,19,6
18,55,9
55,18,9
20,55,7
55,20,7
20,21,6
21,20,6
21,56,9
56,21,9
22,56,7
56,22,7
22,23,5
23,22,5
23,55,4
55,23,4
23,24,4
24,23,4
24,25,5
25,24,5
24,26,6
26,24,6
24,27,7
27,24,7
27,57,7
57,27,7
26,57,6
57,26,6
29,31,5
31,29,5
31,32,7
32,31,7
31,53,4
53,31,4
50,30,5
30,50,5
30,53,7
53,30,7
32,33,8
33,32,8
33,52,4
52,33,4
31,52,8
52,31,8
52,34,8
34,52,8
34,35,6
35,34,6
35,36,7
36,35,7
34,39,4
39,34,4
39,38,3
38,39,3
38,37,9
37,38,9
39,40,8
40,39,8
40,41,7
41,40,7
52,41,6
41,52,6
41,53,9
53,41,9
41,13,7
13,41,7
39,43,5
43,39,5
39,54,4
54,39,4
40,54,5
54,40,5
41,49,6
49,41,6
43,42,5
42,43,5
43,54,4
54,43,4
43,44,9
44,43,9
44,45,7
45,44,7
45,54,6
54,45,6
45,46,9
46,45,9
45,47,7
47,45,7
47,48,8
48,47,8
48,49,9
49,48,9
49,56,3
56,49,3
48,0,6
0,48,6
0,56,6
56,0,6
0,57,4
57,0,4
29,50,3
50,29,3"""

# Procesar los datos para construir el grafo
for line in data.splitlines()[1:]:  # Saltar la cabecera
    origen, destino, costo = map(int, line.split(','))
    if origen not in grafo:
        grafo[origen] = []
    grafo[origen].append((destino, costo))

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        if distancia_actual > distancias[nodo_actual]:
            continue
        for vecino, peso in grafo[nodo_actual]:
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola_prioridad, (distancia, vecino))
    return distancias

# Configuración inicial
nodos_horizontales = list(range(50, 58))
nodos_verticales = list(range(0, 50))
matriz_distancias = [[float('inf')] * len(nodos_horizontales) for _ in range(len(nodos_verticales))]
for j, nodo_h in enumerate(nodos_horizontales):
    distancias_desde_nodo_h = dijkstra(grafo, nodo_h)
    for i, nodo_v in enumerate(nodos_verticales):
        matriz_distancias[i][j] = distancias_desde_nodo_h.get(nodo_v, float('inf'))

volumen_por_cliente = {i: 10 for i in range(50)}
costos_centros = [2300, 1900, 1500, 2000, 2700, 2500, 3000, 500]
costos_transporte = [3, 3, 3, 2, 2, 2, 1, 1]

# Variables globales para el backtracking
mejor_suma_total = float('inf')
mejor_combinacion = []

# Evaluación de la combinación de centros
def evaluar_combinacion(combinacion):
    global mejor_suma_total, mejor_combinacion
    suma_total = sum(costos_centros[i] for i, activo in enumerate(combinacion) if activo)
    for i, nodo_v in enumerate(nodos_verticales):
        dist_minima = float('inf')
        for j, activo in enumerate(combinacion):
            if activo:
                costo_total = (matriz_distancias[i][j] + costos_transporte[j]) * volumen_por_cliente[nodo_v]
                dist_minima = min(dist_minima, costo_total)
        suma_total += dist_minima
    if suma_total < mejor_suma_total:
        mejor_suma_total = suma_total
        mejor_combinacion = combinacion[:]

# Backtracking con poda
def backtracking(idx, combinacion):
    if idx == len(nodos_horizontales):
        if any(combinacion):  # Al menos un centro activo
            evaluar_combinacion(combinacion)
        return

    # Sin activar este centro
    combinacion.append(False)
    backtracking(idx + 1, combinacion)
    combinacion.pop()

    # Activando este centro, con poda eficiente
    combinacion.append(True)
    suma_activos = sum(costos_centros[i] for i, activo in enumerate(combinacion) if activo)
    if suma_activos < mejor_suma_total:
        backtracking(idx + 1, combinacion)
    combinacion.pop()

# Ejecutar backtracking
backtracking(0, [])
print("Mejor combinación de centros activos:", mejor_combinacion)
print("Suma total mínima de distancias:", mejor_suma_total)

# Asignación de clientes a centros
for i, nodo_v in enumerate(nodos_verticales):
    minimo = float('inf')
    for j, centro_activo in enumerate(mejor_combinacion):
        if centro_activo:
            cap = costos_transporte[j]
            distancia = matriz_distancias[i][j] + cap
            if distancia < minimo:
                minimo = distancia
                centro_minimo = j
    print(f"El cliente {i} debe enviar la materia prima al centro {centro_minimo + 50}.")
