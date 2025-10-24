import time
import random
import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

#La Clase de union es unir nodos evitando crear ciclos
class Union:
    def __init__(self, n):
        self.parent = list(range(n)) #Crea una lista de valores
        self.rank = [0] * n # Crea inicialmente una lista en 0

    def find(self, x): #Devuelve la raíz de un elemento
        if self.parent[x] != x: #Comprueba si x es raíz
            self.parent[x] = self.find(self.parent[x]) # Se usa la recursión para encontrar la raíz de un elemento
        return self.parent[x] #Devuelve la ráíz

    def union(self, x, y): # Obtiene las raices y une los elementos
        px, py = self.find(x), self.find(y) # Obtiene las raices
        if px == py: # Comprueba si los elementos son igual. Si es asi retorna false
            return False
        if self.rank[px] < self.rank[py]: # Si los elementos del grupo px es más chico que py se hace un intercambio
            px, py = py, px
        self.parent[py] = px # Se crea la unión entre los grupos
        if self.rank[px] == self.rank[py]: # si los 2 grupos tenían la misma altura, se aumenta la altura
            self.rank[px] += 1
        return True # Se indica que se realizo la unión


class Grafo:
    def __init__(self, vertices):
        self.V = vertices #Guarda los vertices que tiene el grafo
        self.aristas = [] #Guarda las conexiones en forma de lista
        self.adj = defaultdict(list) # Guarda los vecinos de cada nodo

    def agregar_arista(self, u, v, peso): # Agrega una arista entre los elementos y con un peso
        self.aristas.append((peso, u, v))
        self.adj[u].append((v, peso))
        self.adj[v].append((u, peso))

    def kruskal(self):
        inicio = time.time()
        self.aristas.sort() # Ordena las aristas de menor a mayor
        uf = Union(self.V) # Utilizamos la clase union para poder evitar los ciclos
        aem = []
        peso_total = 0
        pasos = []
        for peso, u, v in self.aristas:
            if uf.union(u, v): #Une los nodos
                aem.append((u, v, peso)) #Añade a la arista en la lista de AEM
                peso_total += peso #Se suma el peso
                pasos.append((u, v, peso, 'ACEPTADA'))
            else:
                pasos.append((u, v, peso, 'DESCARTADA'))
            if len(aem) == self.V - 1: # Cuando el grafo obtiene V-1 se rompe el ciclo
                break
        tiempo = time.time() - inicio
        return aem, peso_total, tiempo, pasos #Devuelve las aristas, el peso, el tiempo y los pasos

    def prim(self, inicio=0):
        tiempo_inicio = time.time()
        visitado = [False] * self.V # Crea una lista de los nodos que ya fueron visitados
        heap = [(0, inicio, -1)]
        aem = []
        peso_total = 0
        pasos = []
        while heap and len(aem) < self.V - 1: # Sigue el ciclo hasta que se complete el AEM
            peso, u, padre = heapq.heappop(heap) # Se obtienen la arista de menor peso
            if visitado[u]: # Si ya se visito el nodo se salta la arista
                continue
            visitado[u] = True # Marca como visitado
            if padre != -1:
                aem.append((padre, u, peso))
                peso_total += peso
                pasos.append((padre, u, peso, 'ACEPTADA'))
            for v, w in self.adj[u]: # Recorre todos los nodos vecinos
                if not visitado[v]:
                    heapq.heappush(heap, (w, v, u)) # Si un vecino no fue visitado, lo añade a la lista heap
                    pasos.append((u, v, w, 'CONSIDERADA'))
        tiempo = time.time() - tiempo_inicio
        return aem, peso_total, tiempo, pasos #Devuelve las aristas, el peso, el tiempo y los pasos


def generar_grafo_aleatorio(n, densidad=0.3): # Se crea un grafo aleatorio
    g = Grafo(n) #Se crea un grafo vacio de n nodos
    for i in range(1, n): # Se verifica que los nodos estén conectados almenos una vez
        padre = random.randint(0, i - 1)
        peso = random.randint(1, 100) # Asigna un peso aleatorio 1 al 100
        g.agregar_arista(padre, i, peso) # Manda a llamar agregar_arista para añadir la conexión al grafo
    aristas_adicionales = int(densidad * n * (n - 1) / 2) # Se calcula cuantas aristas se pueden agregar
    for _ in range(aristas_adicionales): # Se genera un bucle para agregra las aristas de forma azar
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            peso = random.randint(1, 100)
            g.agregar_arista(u, v, peso)
    return g #Devuelve el grafo generado


def visualizar_algoritmo(grafo, pasos, titulo_algoritmo):
    import matplotlib.pyplot as plt
    import networkx as nx 
    
    G = nx.Graph()
    for peso, u, v in grafo.aristas:
        G.add_edge(u, v, weight=peso)
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'weight')
    aristas_aceptadas = []

    print(f"\nVisualizando {titulo_algoritmo} paso a paso...\n")

    fig, ax = plt.subplots(figsize=(9, 7))
    plt.ion()
    for i, (u, v, peso, estado) in enumerate(pasos, 1):
        if estado == 'IGNORADA':
            continue
        ax.clear()
        ax.set_title(f"{titulo_algoritmo} - Paso {i}\nArista ({u}, {v}) Peso: {peso} [{estado}]",
                      fontsize=14, fontweight='bold')
        nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1, alpha=0.5, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=aristas_aceptadas, edge_color='green', width=2, ax=ax)
        color = 'red' if estado == 'ACEPTADA' else 'orange'
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, width=3, ax=ax)
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=600, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10, ax=ax)
        if estado == 'ACEPTADA':
            aristas_aceptadas.append((u, v))
        print(f" Paso {i:02d}: ({u}, {v}) -> {estado} (Peso: {peso})")
        plt.axis('off')
        plt.draw()
        plt.pause(0.01) 
        input("Presiona ENTER para continuar con el siguiente paso...")
    ax.clear()
    ax.set_title(f"RESULTADO FINAL: {titulo_algoritmo}\n(Peso Total: {sum(G.get_edge_data(u, v)['weight'] for u, v in aristas_aceptadas)})",
                  fontsize=14, fontweight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1, alpha=0.3, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=aristas_aceptadas, edge_color='green', width=3, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=600, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10, ax=ax)
    plt.axis('off')
    plt.draw()
    plt.ioff()
    print(f"\n Visualización del algoritmo {titulo_algoritmo} completada.")
    print("La ventana del AEM final permanecerá abierta para su análisis.")
    plt.show()


def pruebas_rendimiento(): 
    tamanios = [100, 500, 1000, 2000, 5000, 7000, 8000, 10000]
    resultados = {'Kruskal': [], 'Prim': []}
    print("=" * 70)
    print("PRUEBAS DE RENDIMIENTO - ÁRBOLES DE EXPANSIÓN MÍNIMA")
    print("=" * 70)
    for n in tamanios:
        print(f"\n>>> Probando con N = {n} vértices...")
        g = generar_grafo_aleatorio(n)
        aem_k, peso_k, tiempo_k, _ = g.kruskal()
        resultados['Kruskal'].append((n, tiempo_k))
        print(f" Kruskal: {tiempo_k:.6f} segundos | Peso total: {peso_k}")
        aem_p, peso_p, tiempo_p, _ = g.prim()
        resultados['Prim'].append((n, tiempo_p))
        print(f" Prim: {tiempo_p:.6f} segundos | Peso total: {peso_p}")
    return resultados

def ingresar_grafo_manual():
    print("\n=== INGRESO MANUAL DE GRAFO ===")
    n = int(input("Ingrese el número de vértices: "))
    g = Grafo(n)
    m = int(input("Ingrese el número de aristas: "))

    print("\nIngrese las aristas en el formato: u v peso")
    print("(Los nodos van de 0 a", n-1, ")")

    for i in range(m):
        while True:
            try:
                u, v, peso = map(int, input(f"Arista {i+1}: ").split())
                if u < 0 or v < 0 or u >= n or v >= n or u == v:
                    print("Nodos inválidos. Intente de nuevo.")
                    continue
                g.agregar_arista(u, v, peso)
                break
            except ValueError:
                print("Entrada inválida. Debe ingresar tres números separados por espacios.")
    print("\n Grafo ingresado correctamente.")
    return g

def menu():
    while True:
        print("\n" + "=" * 70)
        print("  PRÁCTICA EQUIPO 3: Árboles de Expansión Mínima (AEM")
        print("=" * 70)
        print("1. Visualizar paso a paso - Algoritmo de Kruskal")
        print("2. Visualizar paso a paso - Algoritmo de Prim")
        print("3. Ejecutar pruebas de rendimiento")
        print("4. Ingresar grafo manual y visualizar")
        print("5. Salir")
        print("=" * 70)
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            g = generar_grafo_aleatorio(8, 0.3)
            _, _, _, pasos = g.kruskal()
            visualizar_algoritmo(g, pasos, "KRUSKAL")
        elif opcion == '2':
            g = generar_grafo_aleatorio(8, 0.3)
            _, _, _, pasos = g.prim()
            visualizar_algoritmo(g, pasos, "PRIM")
        elif opcion == '3':
            pruebas_rendimiento()
        elif opcion == '4':
            g = ingresar_grafo_manual()
            print("\nSeleccione el algoritmo a aplicar:")
            print("  1. Kruskal")
            print("  2. Prim")
            alg = input("Opción: ")
            if alg == '1':
                _, _, _, pasos = g.kruskal()
                visualizar_algoritmo(g, pasos, "KRUSKAL (Grafo Manual)")
            elif alg == '2':
                inicio = int(input(f"Ingrese el vértice inicial (0 a {g.V - 1}): "))
                _, _, _, pasos = g.prim(inicio)
                visualizar_algoritmo(g, pasos, "PRIM (Grafo Manual)")
            else:
                print("Opción inválida.")
        elif opcion == '5':
            print("\nSaliendo del programa")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
