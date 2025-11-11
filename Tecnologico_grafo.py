import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import pandas as pd

# ============================================
# DEFINICIÓN DE NODOS (Edificios del ITSX según mapa real)
# ============================================

nodos = {
    # Zona izquierda
    'L': {'pos': (50, 400), 'nombre': 'Edificio L', 'info': 'Talleres y servicios'},
    'H': {'pos': (150, 250), 'nombre': 'Edificio H', 'info': 'Investigación, talleres'},
    'EXP': {'pos': (100, 230), 'nombre': 'Área Experimental', 'info': 'Laboratorios experimentales'},
    
    # Zona centro-izquierda
    'DOMO': {'pos': (250, 500), 'nombre': 'Domo ITSX', 'info': 'Auditorio principal'},
    'CAMPO': {'pos': (380, 600), 'nombre': 'Campo Deportivo', 'info': 'Canchas deportivas'},
    'E': {'pos': (350, 180), 'nombre': 'Edificio E', 'info': 'Dirección, administración'},
    'BIB': {'pos': (300, 250), 'nombre': 'Biblioteca', 'info': 'Biblioteca central'},
    
    # Zona centro
    'D': {'pos': (550, 200), 'nombre': 'Edificio D', 'info': 'Aulas, laboratorios'},
    'K': {'pos': (650, 140), 'nombre': 'Edificio K', 'info': 'Auditorio, aulas'},
    'CAF': {'pos': (769, 220), 'nombre': 'Cafetería Voluntariado', 'info': 'Cafetería principal'},
    'SOLD': {'pos': (650, 280), 'nombre': 'Taller Soldadura', 'info': 'Talleres técnicos'},
    'F': {'pos': (660, 215), 'nombre': 'Taller Soldadura', 'info': 'Talleres técnicos'},
    
    # Zona centro-derecha
    'B': {'pos': (780, 420), 'nombre': 'Edificio B', 'info': 'Oficinas administrativas'},
    'A': {'pos': (950, 270), 'nombre': 'Edificio A', 'info': 'Aulas principales'},
    'C': {'pos': (770, 270), 'nombre': 'Edificio C', 'info': 'Aulas principales'},
    'TENNIS': {'pos': (900, 190), 'nombre': 'Cancha de Tenis', 'info': 'Instalación deportiva'},
    
    # Zona derecha
    'G': {'pos': (1150, 220), 'nombre': 'Edificio G', 'info': 'Aulas múltiples'},
    'G1': {'pos': (1200, 270), 'nombre': 'Edificio C', 'info': 'Aulas especializadas'},
    'M': {'pos': (1250, 370), 'nombre': 'Edificio M', 'info': 'Laboratorios de cómputo'},
    
    # Zona extremo derecha
    'O': {'pos': (1350, 480), 'nombre': 'Edificio O', 'info': 'Aulas, cubículos'},
    'N': {'pos': (1380, 600), 'nombre': 'Edificio N', 'info': 'Aulas'},
    
    # Zona sur
    'J': {'pos': (1000, 500), 'nombre': 'Edificio J', 'info': 'Servicios escolares'},
    'ESTD': {'pos': (1050, 400), 'nombre': 'Est. Directivos', 'info': 'Estacionamiento directivos'},
    'ESTA': {'pos': (834, 450), 'nombre': 'Est. Admin/Docentes', 'info': 'Estacionamiento administrativos'},
    'CAS1': {'pos': (1493, 359), 'nombre': 'Caseta de vigilancia 1', 'info': 'Entrada principal'},
    'CAS2': {'pos': (901, 600), 'nombre': 'Caseta de vigilancia 1', 'info': 'Entrada estacionamiento'},
    'CAS3': {'pos': (-76,235), 'nombre': 'Caseta de vigilancia 1', 'info': 'Entrada Lomas verdes'},
    
    
}

# ============================================
# DEFINICIÓN DE ARISTAS (Andadores según mapa real)
# ============================================

aristas = [
    # ID, from, to, distancia, techado, accesibilidad
    
    # Zona izquierda
    ('E1', 'L', 'H', 94, 'parcial', 'bueno'),           # Original. (L-H no es arista oficial)
    ('E2', 'L', 'EXP', 120, 'sin techo', 'regular'),    # Original. (L-EXP no es arista oficial)
    # E3 (H, EXP) -> Arista 1 (H, AE)
    ('E3', 'H', 'EXP', 20.47, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 143, 146]
    # E4 (H, BIB) -> Arista 3 (H, I)
    ('E4', 'H', 'BIB', 68.33, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 150, 152]
    
    # Conexiones DOMO y Campo
    # E5 (DOMO, CAMPO) -> Arista 6 (Domo, CD)
    ('E5', 'DOMO', 'CAMPO', 17.72, 'sin techo', 'tierra'), # ACTUALIZADA [cite: 157, 158]
    ('E6', 'DOMO', 'BIB', 2100, 'sin techo', 'regular'),  # Original. (DOMO-BIB no es arista oficial)
    
    # Zona centro
    # E7 (BIB, E) -> Arista 4 (I, E)
    ('E7', 'BIB', 'E', 42.86, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 153, 154]
    # E8 (E, D) -> Arista 10 (E, D)
    ('E8', 'E', 'D', 45.73, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 165, 166]
    ('E9', 'D', 'K', 120, 'parcial', 'bueno'),          # Original. (D-K no es arista oficial)
    ('E11', 'CAF', 'SOLD', 70, 'sin techo', 'bueno'),    # Original.
    ('E12', 'C', 'SOLD', 103, 'sin techo', 'regular'),   # Original.
    ('E13', 'SOLD', 'F', 120, 'sin techo', 'regular'),   # Original.
    # E14 (F, D) -> Arista 12 (D, F)
    ('E14', 'F', 'D', 48.02, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 169, 170]
    ('E15', 'N', 'A', 101.20, 'sin techo', 'regular'),      # Original.
    ('E16', 'A', 'G1', 120.20, 'sin techo', 'regular'),     # Original. (G1 no es nodo oficial)
    # Conexión centro con A
    # E17 (C, A) -> Arista 15 (C, A)
    ('E17', 'C', 'A', 66.30, 'sin techo', 'REGULAR'), # ACTUALIZADA [cite: 177, 178]
    # E18 (C, B) -> Arista 14 (C, B)
    ('E18', 'C', 'B', 26.24, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 175, 176]
    
    # Zona A y áreas deportivas
    ('E19', 'A', 'TENNIS', 100, 'sin techo', 'bueno'),   # Original.
    ('E20', 'TENNIS', 'G', 250, 'parcial', 'bueno'),     # Original.
    # E21 (A, G) -> Arista 18 (A, G)
    ('E21', 'A', 'G', 54.46, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 183, 184]
    
    # Zona derecha (G, C, M)
    ('E22', 'G', 'G1', 67.10, 'completo', 'excelente'),     # Original. (G1 no es nodo oficial)
    # E23 (G1, M) -> Arista 20 (G, M) se usa G-M
    ('E23', 'G1', 'M', 29.47, 'parcial', 'pavimentado'),  # ACTUALIZADA (Distancia G-M) [cite: 187, 188]
    ('E24', 'M', 'A', 110, 'parcial', 'bueno'),          # Original.
    # E25 (M, O) -> Arista 21 (M, O)
    ('E25', 'M', 'O', 45.52, 'sin techo', 'pavimentado'), # ACTUALIZADA [cite: 189, 190]
    # E26 (O, N) -> Arista 23 (O, N)
    ('E26', 'O', 'N', 86.85, 'parcial', 'pavimentado'), # ACTUALIZADA [cite: 193, 194]
    
    # Conexiones B, J, Estacionamientos
    ('E27', 'B', 'ESTA', 70, 'sin techo', 'bueno'),      # Original.
    ('E28', 'ESTA', 'J', 80, 'sin techo', 'bueno'),      # Original.
    ('E29', 'ESTA', 'ESTD', 90, 'sin techo', 'bueno'),   # Original.
    ('E30', 'ESTD', 'J', 100, 'sin techo', 'bueno'),     # Original.
    ('E31', 'J', 'N', 150, 'sin techo', 'bueno'),        # Original.
    
    # Conexiones adicionales
    ('E32', 'A', 'B', 200, 'sin techo', 'regular'),      # Original.
    ('E33', 'A', 'ESTA', 180, 'sin techo', 'bueno'),     # Original.
    ('E34', 'CAS1', 'M', 140, 'completo', 'bueno'), 
    ('E35', 'O', 'CAS1', 150, 'parcial', 'bueno'), 
    ('E36', 'CAS2', 'J', 100, 'sin techo', 'bueno'), 
    ('E37', 'CAS2', 'N', 41, 'sin techo', 'bueno'), 
    ('E38', 'CAS3', 'L', 120, 'sin techo', 'bueno'), 
    ('E39', 'CAS3', 'EXP', 110, 'sin techo', 'bueno'), 
]

# ============================================
# CREAR MATRIZ DE INCIDENCIA
# ============================================

def crear_matriz_incidencia():
    """Crea la matriz de incidencia (nodos x aristas)"""
    nodos_lista = list(nodos.keys())
    n_nodos = len(nodos_lista)
    n_aristas = len(aristas)
    
    # Matriz de ceros
    matriz = np.zeros((n_nodos, n_aristas), dtype=int)
    
    # Llenar la matriz
    for j, arista in enumerate(aristas):
        id_arista, origen, destino, dist, techado, acceso = arista
        i_origen = nodos_lista.index(origen)
        i_destino = nodos_lista.index(destino)
        
        matriz[i_origen][j] = 1
        matriz[i_destino][j] = 1
    
    return matriz, nodos_lista

# ============================================
# VISUALIZAR GRAFO CON MATPLOTLIB
# ============================================

def visualizar_grafo(guardar=False, nombre_archivo='grafo_itsx.png'):
    """Visualiza el grafo del campus ITSX"""
    
    fig, ax = plt.subplots(figsize=(20, 12))
    
    G = nx.Graph()

    pos = {nodo: datos['pos'] for nodo, datos in nodos.items()}
    
    for nodo in nodos:
        G.add_node(nodo)
    
    colores_aristas = []
    anchos_aristas = []
    for arista in aristas:
        id_arista, origen, destino, dist, techado, acceso = arista
        G.add_edge(origen, destino, distancia=dist, techado=techado, accesibilidad=acceso)
        
        if techado == 'completo':
            colores_aristas.append('#2E7D32')
            anchos_aristas.append(4)
        elif techado == 'parcial':
            colores_aristas.append('#FF9800')
            anchos_aristas.append(3)
        else:
            colores_aristas.append('#1976D2')
            anchos_aristas.append(2)
    
    nx.draw_networkx_edges(G, pos,
                          edge_color=colores_aristas,
                          width=anchos_aristas,
                          alpha=0.6,
                          ax=ax)

    nx.draw_networkx_nodes(G, pos,
                          node_color='#42A5F5',
                          node_size=800,
                          edgecolors='black',
                          linewidths=2,
                          ax=ax)
    
    nx.draw_networkx_labels(G, pos,
                           font_size=10,
                           font_weight='bold',
                           font_color='white',
                           ax=ax)

    edge_labels = {(a[1], a[2]): f"{a[3]}m" for a in aristas}
    nx.draw_networkx_edge_labels(G, pos, 
                                 edge_labels=edge_labels,
                                 font_size=8,
                                 font_weight='bold',
                                 ax=ax)
    
    plt.title('Grafo del Campus ITSX',
             fontsize=18, fontweight='bold', pad=20)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#2E7D32', lw=4, label='Techo Completo'),
        Line2D([0], [0], color='#FF9800', lw=3, label='Techo Parcial'),
        Line2D([0], [0], color='#1976D2', lw=2, label='Sin Techo')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
    
    ax.invert_yaxis()
    ax.axis('off')
    plt.tight_layout()
    
    if guardar:
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
        print(f"✓ Grafo guardado como '{nombre_archivo}'")
    
    plt.show()




# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main():
    
    print("\n" + "="*70)
    print("MODELADO DEL CAMPUS ITSX")
    print("Instituto Tecnológico Superior de Xalapa")
    print("="*70)
    

    # Visualizar grafo
    visualizar_grafo()
    
    print("\n" + "="*70)
    print(" PROCESO COMPLETADO EXITOSAMENTE")
    print("="*70)
    print("\n")

# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    main()
