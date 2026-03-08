import heapq
import matplotlib.pyplot as plt
import networkx as nx

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


# -----------------------------
# GRAFICAR EL GRAFO
# -----------------------------
def graficar_grafo(grafo, camino=None):
    G = nx.DiGraph()

    # Agregar nodos y aristas
    for origen in grafo:
        for destino, peso in grafo[origen].items():
            G.add_edge(origen, destino, weight=peso)

    # Posiciones fijas para que se vea ordenado
    pos = {
        "Casa": (0, 2),
        "Oxxo": (1, 3),
        "ParadaCamion": (2, 2),
        "Gimnasio": (1, 1),
        "Súper": (3, 1.2),
        "Banco": (4, 1.8),
        "Centro": (4, 3),
        "Escuela": (6, 2)
    }

    plt.figure(figsize=(12, 7))

    # Dibujar todos los nodos
    nx.draw_networkx_nodes(
        G, pos,
        node_color="lightblue",
        node_size=2200,
        edgecolors="black"
    )

    # Dibujar nombres de nodos
    nx.draw_networkx_labels(
        G, pos,
        font_size=10,
        font_weight="bold"
    )

    # Dibujar todas las aristas
    nx.draw_networkx_edges(
        G, pos,
        edge_color="gray",
        arrows=True,
        arrowsize=20,
        width=2,
        connectionstyle="arc3,rad=0.05"
    )

    # Etiquetas de pesos
    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=etiquetas,
        font_size=9
    )

    # Resaltar camino más corto
    if camino and len(camino) > 1:
        aristas_camino = list(zip(camino[:-1], camino[1:]))

        nx.draw_networkx_nodes(
            G, pos,
            nodelist=camino,
            node_color="lightgreen",
            node_size=2400,
            edgecolors="black"
        )

        nx.draw_networkx_edges(
            G, pos,
            edgelist=aristas_camino,
            edge_color="red",
            width=4,
            arrows=True,
            arrowsize=22,
            connectionstyle="arc3,rad=0.05"
        )

    plt.title("Mapa de rutas - Dijkstra aplicado a la vida diaria", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


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

            # Mostrar gráfica con la ruta óptima
            graficar_grafo(grafo_ciudad, camino)
        else:
            print(f"No hay ruta desde {inicio} hasta {fin}.")
            graficar_grafo(grafo_ciudad)