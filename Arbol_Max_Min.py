try:
    import networkx as nx
    import matplotlib.pyplot as plt
    HAY_GRAFICOS = True
except ImportError:
    HAY_GRAFICOS = False


# -----------------------------
# UNION-FIND (Disjoint Set)
# -----------------------------
class UnionFind:
    def __init__(self, elementos):
        self.parent = {x: x for x in elementos}
        self.rank = {x: 0 for x in elementos}

    def find(self, x):
        # Compresión de caminos
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # Unión por rango
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def print_componentes(uf, nodos):
    comp = {}
    for n in nodos:
        r = uf.find(n)
        comp.setdefault(r, []).append(n)

    for i, (raiz, lista) in enumerate(comp.items(), start=1):
        print(f"  Componente {i} (raíz {raiz}): {lista}")


# -----------------------------
# KRUSKAL (MIN / MAX)
# -----------------------------
def kruskal(aristas, tipo="min", mostrar_pasos=True):
    """
    aristas: lista de tuplas (u, v, peso)
    tipo: "min" => árbol de mínimo coste (MST)
          "max" => árbol de máximo coste (MaxST)
    """

    # Detectar nodos
    nodos = set()
    for u, v, w in aristas:
        nodos.add(u)
        nodos.add(v)

    # Orden de selección de aristas
    if tipo == "min":
        aristas_ordenadas = sorted(aristas, key=lambda x: x[2])              # ascendente
        titulo = "ÁRBOL DE MÍNIMO COSTE (Kruskal)"
    else:
        aristas_ordenadas = sorted(aristas, key=lambda x: x[2], reverse=True) # descendente
        titulo = "ÁRBOL DE MÁXIMO COSTE (Kruskal)"

    if mostrar_pasos:
        print("\n====================================")
        print(" ", titulo)
        print("====================================\n")
        print("Nodos:", nodos)
        print("\nAristas ordenadas (u, v, peso):")
        for e in aristas_ordenadas:
            print("  ", e)

    uf = UnionFind(nodos)
    arbol = []
    total = 0

    if mostrar_pasos:
        print("\nComponentes iniciales:")
        print_componentes(uf, nodos)

    for (u, v, w) in aristas_ordenadas:
        if mostrar_pasos:
            print("\n---------------------------------")
            print(f"Probando: ({u}, {v}, {w})")
            print(f"  Raíz {u}: {uf.find(u)}")
            print(f"  Raíz {v}: {uf.find(v)}")

        # Si no forman ciclo, se acepta
        if uf.union(u, v):
            arbol.append((u, v, w))
            total += w
            if mostrar_pasos:
                print("ACEPTADA (no forma ciclo)")
        else:
            if mostrar_pasos:
                print("RECHAZADA (forma ciclo)")

        if mostrar_pasos:
            print("  Componentes ahora:")
            print_componentes(uf, nodos)

        # Si ya conectaste todo (n-1 aristas), puedes parar
        if len(arbol) == len(nodos) - 1:
            break

    if mostrar_pasos:
        print("\n====================================")
        print(" ARISTAS DEL ÁRBOL RESULTANTE")
        print("====================================")
        for (u, v, w) in arbol:
            print(f"  ({u} - {v}) peso={w}")
        print("\nTotal:", total)

    return arbol, total


def dibujar(aristas, arbol, titulo):
    if not HAY_GRAFICOS:
        print("\n[AVISO] Instala networkx y matplotlib si quieres el dibujo:")
        print("        pip install networkx matplotlib")
        return

    G = nx.Graph()
    for (u, v, w) in aristas:
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    pesos = nx.get_edge_attributes(G, "weight")

    plt.figure()
    plt.title(titulo)

    nx.draw_networkx_nodes(G, pos, node_size=750)
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=8)

    # resaltar árbol
    if arbol:
        edges_tree = [(u, v) for (u, v, _) in arbol]
        nx.draw_networkx_edges(G, pos, edgelist=edges_tree, width=3)

    plt.axis("off")
    plt.tight_layout()
    plt.show()


# -----------------------------
# EJEMPLO VIDA DIARIA
# -----------------------------
def ejemplo_wifi_costos():
    """
    Caso: quieres cablear/conectar todos los cuartos con el menor costo (MIN).
    Nodos = habitaciones/zonas
    Peso = costo estimado (o metros de cable).
    """
    return [
        ("Router", "Sala", 6),
        ("Router", "Cuarto1", 10),
        ("Router", "Cuarto2", 12),
        ("Router", "Cocina", 7),

        ("Sala", "Cocina", 3),
        ("Sala", "Cuarto1", 8),
        ("Cocina", "Cuarto2", 5),
        ("Cuarto1", "Cuarto2", 4),

        ("Sala", "Patio", 9),
        ("Cocina", "Patio", 6),
        ("Cuarto2", "Patio", 11),
    ]


def ejemplo_wifi_calidad():
    """
    Caso: quieres una red 'más robusta' usando enlaces con mejor calidad (MAX).
    Peso = calidad/estabilidad del enlace.
    """
    return [
        ("Router", "Sala", 8),
        ("Router", "Cuarto1", 6),
        ("Router", "Cuarto2", 5),
        ("Router", "Cocina", 7),

        ("Sala", "Cocina", 9),
        ("Sala", "Cuarto1", 7),
        ("Cocina", "Cuarto2", 8),
        ("Cuarto1", "Cuarto2", 9),

        ("Sala", "Patio", 4),
        ("Cocina", "Patio", 6),
        ("Cuarto2", "Patio", 5),
    ]


def main():
    print("==============================================")
    print(" Árbol MIN/MAX (Kruskal) - Vida diaria (Wi-Fi/Cableado)")
    print("==============================================\n")

    print("Elige el escenario:")
    print("  1) MINIMIZAR costo/metros de cable (MST)")
    print("  2) MAXIMIZAR calidad de enlaces (MaxST)")
    print("  3) Ambos")
    op = input("Opción (1/2/3): ").strip()

    if op == "1":
        aristas = ejemplo_wifi_costos()
        arbol, total = kruskal(aristas, tipo="min", mostrar_pasos=True)
        dibujar(aristas, arbol, f"Conexión más barata (total={total})")

    elif op == "2":
        aristas = ejemplo_wifi_calidad()
        arbol, total = kruskal(aristas, tipo="max", mostrar_pasos=True)
        dibujar(aristas, arbol, f"Conexión más robusta (score={total})")

    else:
        aristas = ejemplo_wifi_costos()
        arbol_min, total_min = kruskal(aristas, tipo="min", mostrar_pasos=True)
        dibujar(aristas, arbol_min, f"MIN costo (total={total_min})")

        aristas2 = ejemplo_wifi_calidad()
        arbol_max, total_max = kruskal(aristas2, tipo="max", mostrar_pasos=True)
        dibujar(aristas2, arbol_max, f"MAX calidad (score={total_max})")


if __name__ == "__main__":
    main()