import math

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    HAY_GRAFICOS = True
except ImportError:
    HAY_GRAFICOS = False


def prim_mst_con_pasos(nodos, edges, start=0):
    """
    nodos: lista de secciones del súper (strings)
    edges: lista de aristas (u, v, w) con u,v índices y w "distancia" (pasoss/metros/min)
    start: índice de nodo inicial (ej. Entrada)
    """
    INF = math.inf
    n = len(nodos)

    # Matriz de adyacencia (como en tu ejemplo)
    adj = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < adj[u][v]:
            adj[u][v] = w
            adj[v][u] = w

    selected = [False] * n
    key = [INF] * n
    parent = [-1] * n
    key[start] = 0

    print("=== Prim (Árbol Parcial Mínimo) - Compras en el súper ===")
    print("Interpretación: conectar TODAS las secciones que visitarás con el menor costo total.")
    print("Peso = distancia/tiempo caminando entre secciones.\n")

    print("Secciones (nodos):")
    for i, nombre in enumerate(nodos):
        print(f"  {i}: {nombre}")
    print(f"\nIniciando desde: {start} ({nodos[start]})\n")

    for step in range(n):
        # 1) escoger nodo no seleccionado con menor key
        u = -1
        min_key = INF
        for v in range(n):
            if not selected[v] and key[v] < min_key:
                min_key = key[v]
                u = v

        if u == -1:
            print("El grafo NO es conexo, no se pueden conectar todas las secciones.")
            break

        selected[u] = True
        print(f"Paso {step + 1}:")
        print(f"  -> Agrego: {u} ({nodos[u]})  | costo incremental = {min_key}")

        # 2) mostrar aristas candidatas
        print("  Candidatos (desde lo ya conectado hacia lo que falta):")
        for a in range(n):
            if selected[a]:
                for b in range(n):
                    if (not selected[b]) and adj[a][b] != INF:
                        print(f"    {nodos[a]} --{adj[a][b]}--> {nodos[b]}")

        # 3) actualizar keys
        for v in range(n):
            if not selected[v] and adj[u][v] < key[v]:
                key[v] = adj[u][v]
                parent[v] = u

        # 4) árbol parcial acumulado
        total = 0
        print("  Árbol parcial actual (conexiones elegidas):")
        for v in range(n):
            if parent[v] != -1:
                total += adj[parent[v]][v]
                print(f"    {nodos[parent[v]]} --{adj[parent[v]][v]}--> {nodos[v]}")
        print(f"  Costo total acumulado: {total}\n")

    # resultado final
    total = 0
    print("=== Resultado final ===")
    print("Conexiones del Árbol Parcial Mínimo (MST):")
    for v in range(n):
        if parent[v] != -1:
            w = adj[parent[v]][v]
            print(f"  {nodos[parent[v]]} --{w}--> {nodos[v]}")
            total += w
    print("Costo total del árbol:", total)

    return parent


def dibujar(nodos, edges, parent, titulo="MST - Súper (Prim)"):
    if not HAY_GRAFICOS:
        print("\n[AVISO] Para ver gráfico instala: pip install networkx matplotlib")
        return

    G = nx.Graph()
    for i, nombre in enumerate(nodos):
        G.add_node(i, label=nombre)

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    mst_edges = [(parent[v], v) for v in range(len(nodos)) if parent[v] != -1]

    pos = nx.spring_layout(G, seed=42)
    labels_nodos = {i: nodos[i] for i in range(len(nodos))}
    labels_aristas = nx.get_edge_attributes(G, "weight")

    plt.figure()
    plt.title("Grafo original (distancias entre secciones)")
    nx.draw(G, pos, with_labels=True, labels=labels_nodos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_aristas)

    plt.figure()
    plt.title(titulo)
    nx.draw(G, pos, with_labels=True, labels=labels_nodos)
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_aristas)

    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Ejemplo de vida diaria: secciones típicas
    nodos = [
        "Entrada",
        "Frutas y Verduras",
        "Abarrotes",
        "Lácteos",
        "Carnes",
        "Panadería",
        "Caja"
    ]

    # Pesos (distancia/tiempo estimado caminando) entre secciones
    # (u, v, w) donde u y v son índices
    edges = [
        (0, 1, 3),   # Entrada - Frutas
        (0, 2, 4),   # Entrada - Abarrotes
        (1, 2, 2),   # Frutas - Abarrotes
        (1, 3, 5),   # Frutas - Lácteos
        (2, 3, 2),   # Abarrotes - Lácteos
        (2, 5, 3),   # Abarrotes - Panadería
        (3, 4, 3),   # Lácteos - Carnes
        (4, 6, 4),   # Carnes - Caja
        (5, 6, 2),   # Panadería - Caja
        (3, 6, 5),   # Lácteos - Caja (camino más largo)
    ]

    start = 0  # Entrada
    parent = prim_mst_con_pasos(nodos, edges, start=start)

    ver = input("\n¿Deseas ver el grafo y el MST gráficamente? (s/n): ").strip().lower()
    if ver == "s":
        dibujar(nodos, edges, parent, titulo="Árbol Parcial Mínimo - Súper (mínimo caminar total)")