import heapq

# -----------------------------
# DIJKSTRA (vida diaria)
# -----------------------------
def dijkstra(grafo, inicio, fin=None, mostrar_pasos=True):
    dist = {n: float("inf") for n in grafo}
    dist[inicio] = 0

    prev = {n: None for n in grafo}

    heap = [(0, inicio)]
    visitados = set()
    paso = 0

    while heap:
        d_actual, u = heapq.heappop(heap)

        if u in visitados:
            continue
        visitados.add(u)

        if mostrar_pasos:
            print(f"\n--- Paso {paso} ---")
            print(f"Confirmo: {u} con costo {d_actual}")
            print("Distancias:")
            for k in dist:
                print(f"  {k}: {dist[k]}")
            paso += 1

        if fin is not None and u == fin:
            break

        for v, w in grafo[u].items():
            if v in visitados:
                continue

            nd = d_actual + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

                if mostrar_pasos:
                    print(f"  Mejoro {v}: {nd} (viene de {u}, tramo = {w})")

    return dist, prev


def reconstruir_camino(prev, inicio, fin):
    camino = []
    x = fin
    while x is not None:
        camino.append(x)
        x = prev[x]
    camino.reverse()
    return camino if camino and camino[0] == inicio else []


if __name__ == "__main__":
    # Pesos = minutos estimados (vida diaria)
    # Ejemplo: quieres ir de CASA a ESCUELA minimizando tiempo.
    grafo_ciudad = {
        "Casa": {
            "ParadaCamion": 6,
            "Oxxo": 4,
            "Gimnasio": 12
        },
        "Oxxo": {
            "ParadaCamion": 3,
            "Súper": 8
        },
        "ParadaCamion": {
            "Centro": 18,
            "Escuela": 25
        },
        "Gimnasio": {
            "Súper": 10,
            "Centro": 14
        },
        "Súper": {
            "Banco": 7,
            "Escuela": 20
        },
        "Banco": {
            "Escuela": 9,
            "Centro": 6
        },
        "Centro": {
            "Escuela": 11
        },
        "Escuela": {}
    }

    print("Lugares disponibles:")
    for lugar in grafo_ciudad.keys():
        print(" -", lugar)

    inicio = input("\n¿Desde dónde sales?: ").strip()
    fin = input("¿A dónde quieres llegar?: ").strip()

    if inicio not in grafo_ciudad or fin not in grafo_ciudad:
        print("\nError: ese lugar no existe en el mapa.")
    else:
        dist, prev = dijkstra(grafo_ciudad, inicio, fin, mostrar_pasos=True)
        camino = reconstruir_camino(prev, inicio, fin)

        print("\n==============================")
        print("RESULTADO (vida diaria)")
        print("==============================")

        if camino:
            print("Ruta más rápida:")
            print("  " + " -> ".join(camino))
            print(f"Tiempo total: {dist[fin]} minutos")
        else:
            print(f"No hay ruta desde {inicio} hasta {fin}.")