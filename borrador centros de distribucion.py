import heapq

# Definición del grafo basado en los datos de la imagen
# grafo = {
#     1: [(2, 10), (28, 8), (3, 12)],
#     2: [(1, 10), (3, 10)],
#     3: [(2, 10), (1, 12), (50, 10), (4,8),(5,4)],
#     4: [(3,8), (51,9)],
#     5: [(3,4), (51,3),(6,9)],
#     6: [(5,9),(7,8)],
#     7: [(6,8),(8,4)],
#     8: [(7,4), (51,10)],
#     28: [(1, 8), (50, 11)],
#     50: [(28, 11), (3, 10)],
#     51: [(4,9),(5,3),(8,10)]
#
#
# }

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

# Inicializar el grafo
grafo = {}

# Procesar los datos
for line in data.splitlines()[1:]:  # Saltar la cabecera
    origen, destino, costo = map(int, line.split(','))
    if origen not in grafo:
        grafo[origen] = []
    grafo[origen].append((destino, costo))

# Imprimir el grafo
print(grafo)

def dijkstra(grafo, inicio):
    # Inicializar las distancias con infinito
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]  # (distancia, nodo)

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

##centros = 50;

# Inicializar la sumatoria
# Inicializar la sumatoria
sumatoria = 0

# Definir el rango de nodos horizontales y verticales
nodos_horizontales = range(50, 58)  # Nodos 50 a 57
nodos_verticales = range(0, 50)     # Nodos 0 a 49

# Inicializar lista para totales de columnas
totales_columnas = {nodo: 0 for nodo in nodos_horizontales}

# Imprimir encabezados
print("     |", end=" ")  # Espacio para el encabezado de la columna
for nodo in nodos_horizontales:
    print(f"{nodo:>4}", end=" ")  # Imprimir encabezados de nodos horizontalmente
print()  # Nueva línea

# Imprimir separador
print("-----" + "-----" * len(nodos_horizontales))

# Iterar sobre los nodos verticales
for nodo_v in nodos_verticales:
    print(f"{nodo_v:>4} |", end=" ")  # Imprimir el nodo verticalmente
    for nodo_h in nodos_horizontales:
        distancias_desde_nodo_h = dijkstra(grafo, nodo_h)  # Obtener distancias desde el nodo horizontal
        distancia_a_nodo_v = distancias_desde_nodo_h.get(nodo_v, float('inf'))  # Obtener la distancia hacia el nodo vertical
        print(f"{distancia_a_nodo_v:>4}", end=" ")  # Imprimir distancia
        if distancia_a_nodo_v != float('inf'):  # Solo sumar si hay conexión
            totales_columnas[nodo_h] += distancia_a_nodo_v  # Sumar a la columna correspondiente
        sumatoria += distancia_a_nodo_v  # Sumar a la sumatoria total
    print()  # Nueva línea al final de cada fila

# Imprimir separador

 # Imprimir totales de cada columna
print()  # Nueva línea al final de los totales

# Imprimir la sumatoria total

print(f"Sumatoria de distancias: {sumatoria}")