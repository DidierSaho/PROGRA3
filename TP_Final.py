import heapq

# Procesar los datos para construir el grafo
def cargar_grafo(grafo):
    rutas=open("rutas.txt","r")
    data=rutas.read()
    for line in data.splitlines()[1:]:  # Saltar la cabecera
        origen, destino, costo = map(int, line.split(','))
        if origen not in grafo:
            grafo[origen] = []
        grafo[origen].append((destino, costo))
    rutas.close()
    return
        

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
def configuracion_inicial(grafo, nodos_h, nodos_v, matriz_d):
    for j, nodo_h in enumerate(nodos_h):
        distancias_desde_nodo_h = dijkstra(grafo, nodo_h)
        for i, nodo_v in enumerate(nodos_v):
            matriz_d[i][j] = distancias_desde_nodo_h.get(nodo_v, float('inf'))
    return


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
    return

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
    return

# Asignación de clientes a centros
def clientes_centros(nodos_v, mejor_c, costos_t, matriz_d):
    for i, nodo_v in enumerate(nodos_v):
        minimo = float('inf')
        for j, centro_activo in enumerate(mejor_c):
            if centro_activo:
                cap = costos_t[j]
                distancia = matriz_d[i][j] + cap
                if distancia < minimo:
                    minimo = distancia
                    centro_minimo = j
        print(f"El cliente {i} debe enviar la materia prima al centro {centro_minimo + 50}.")
    return



grafo = {}

nodos_horizontales = list(range(50, 58))
nodos_verticales = list(range(0, 50))
matriz_distancias = [[float('inf')] * len(nodos_horizontales) for _ in range(len(nodos_verticales))]

volumen_por_cliente = {i: 10 for i in range(50)}
costos_centros = [2300, 1900, 1500, 2000, 2700, 2500, 3000, 500]
costos_transporte = [3, 3, 3, 2, 2, 2, 1, 1]

# Variables globales para el backtracking
mejor_suma_total = float('inf')
mejor_combinacion = []



cargar_grafo(grafo)

configuracion_inicial(grafo, nodos_horizontales, nodos_verticales, matriz_distancias)

backtracking(0, [])
print("Mejor combinación de centros activos:", mejor_combinacion)
print("Suma total mínima de distancias:", mejor_suma_total)

clientes_centros(nodos_verticales, mejor_combinacion, costos_transporte, matriz_distancias)
