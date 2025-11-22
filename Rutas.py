import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patches as mpatches
import pandas as pd


nodos = {
    'L': {'pos': (50, 400), 'nombre': 'Edificio L', 'info': 'Talleres y servicios', 'tipo': 'academico'},
    'H': {'pos': (150, 250), 'nombre': 'Edificio H', 'info': 'Investigación, talleres', 'tipo': 'academico'},
    'EXP': {'pos': (37, 229), 'nombre': 'Área Experimental', 'info': 'Laboratorios experimentales', 'tipo': 'laboratorio'},
    'DOMO': {'pos': (250, 500), 'nombre': 'Domo ITSX', 'info': 'Auditorio principal', 'tipo': 'especial'},
    'CAMPO': {'pos': (380, 600), 'nombre': 'Campo Deportivo', 'info': 'Canchas deportivas', 'tipo': 'deportivo'},
    'E': {'pos': (350, 180), 'nombre': 'Edificio E', 'info': 'Dirección, administración', 'tipo': 'administrativo'},
    'BIB': {'pos': (300, 250), 'nombre': 'Biblioteca', 'info': 'Biblioteca central', 'tipo': 'especial'},
    'D': {'pos': (550, 200), 'nombre': 'Edificio D', 'info': 'Aulas, laboratorios', 'tipo': 'academico'},
    'K': {'pos': (650, 140), 'nombre': 'Edificio K', 'info': 'Auditorio, aulas', 'tipo': 'academico'},
    'CAF': {'pos': (769, 220), 'nombre': 'Cafetería Voluntariado', 'info': 'Cafetería principal', 'tipo': 'servicio'},
    'SOLD': {'pos': (650, 280), 'nombre': 'Taller Soldadura', 'info': 'Talleres técnicos', 'tipo': 'laboratorio'},
    'F': {'pos': (660, 215), 'nombre': 'Taller Soldadura', 'info': 'Talleres técnicos', 'tipo': 'laboratorio'},
    'B': {'pos': (711, 408), 'nombre': 'Edificio B', 'info': 'Oficinas administrativas', 'tipo': 'administrativo'},
    'A': {'pos': (950, 270), 'nombre': 'Edificio A', 'info': 'Aulas principales', 'tipo': 'academico'},
    'C': {'pos': (770, 270), 'nombre': 'Edificio C', 'info': 'Aulas principales', 'tipo': 'academico'},
    'TENNIS': {'pos': (900, 190), 'nombre': 'Cancha de Tenis', 'info': 'Instalación deportiva', 'tipo': 'deportivo'},
    'G': {'pos': (1150, 170), 'nombre': 'Edificio G', 'info': 'Aulas múltiples', 'tipo': 'academico'},
    'G1': {'pos': (1200, 270), 'nombre': 'Edificio C', 'info': 'Aulas especializadas', 'tipo': 'academico'},
    'M': {'pos': (1251, 460), 'nombre': 'Edificio M', 'info': 'Laboratorios de cómputo', 'tipo': 'laboratorio'},
    'O': {'pos': (1350, 480), 'nombre': 'Edificio O', 'info': 'Aulas, cubículos', 'tipo': 'academico'},
    'N': {'pos': (1380, 600), 'nombre': 'Edificio N', 'info': 'Aulas', 'tipo': 'academico'},
    'J': {'pos': (1000, 500), 'nombre': 'Edificio J', 'info': 'Servicios escolares', 'tipo': 'administrativo'},
    'ESTD': {'pos': (1050, 400), 'nombre': 'Est. Directivos', 'info': 'Estacionamiento directivos', 'tipo': 'estacionamiento'},
    'ESTA': {'pos': (834, 450), 'nombre': 'Est. Admin/Docentes', 'info': 'Estacionamiento administrativos', 'tipo': 'estacionamiento'},
    'CAS1': {'pos': (1493, 359), 'nombre': 'Caseta de vigilancia 1', 'info': 'Entrada principal', 'tipo': 'seguridad'},
    'CAS2': {'pos': (901, 600), 'nombre': 'Caseta de vigilancia 2', 'info': 'Entrada estacionamiento', 'tipo': 'seguridad'},
    'CAS3': {'pos': (-76, 235), 'nombre': 'Caseta de vigilancia 3', 'info': 'Entrada Lomas verdes', 'tipo': 'seguridad'},
    'IE': {'pos': (1079, 333), 'nombre': 'Inicio de escaleras', 'info': 'inicio del techado', 'tipo': 'escaleras'},
    'IE1': {'pos': (1365,362), 'nombre': 'Inicio de escaleras', 'info': 'inicio del techado', 'tipo': 'escaleras'},
    'IE2': {'pos': (1245,367), 'nombre': 'Inicio de escaleras', 'info': 'inicio del techado', 'tipo': 'escaleras'}
}

aristas = [
    ('E1', 'L', 'H', 94, 50, 'bueno'),
    ('E3', 'H', 'EXP', 20.47, 0, 'pavimentado'),
    ('E4', 'H', 'BIB', 68.33, 15, 'pavimentado'),
    ('E4B', 'H', 'BIB', 85, 50, 'regular'),
    ('E5', 'DOMO', 'CAMPO', 17.72, 0, 'tierra'),
    ('E6', 'DOMO', 'BIB', 2100, 15, 'regular'),
    ('E7', 'BIB', 'E', 42.86, 0, 'pavimentado'),
    ('E8', 'E', 'D', 45.73, 0, 'pavimentado'),
    ('E9', 'D', 'K', 120, 50, 'bueno'),
    ('E11', 'CAF', 'SOLD', 70, 15, 'bueno'),
    ('E12', 'C', 'SOLD', 103, 15, 'regular'),
    ('E13', 'SOLD', 'F', 120, 30, 'regular'),
    ('E14', 'F', 'D', 48.02, 5, 'pavimentado'),
    ('E15', 'N', 'A', 101.20, 10, 'regular'),
    ('E16', 'A', 'G1', 120.20, 45, 'regular'),
    ('E17', 'C', 'A', 66.30, 0, 'REGULAR'),
    ('E18', 'C', 'B', 26.24, 0, 'pavimentado'),
    ('E19', 'A', 'TENNIS', 100, 70, 'bueno'),
    ('E20', 'TENNIS', 'G', 250, 25, 'bueno'),
    ('E21', 'A', 'G', 54.46, 25, 'pavimentado'),
    ('E22', 'G', 'G1', 67.10, 60, 'excelente'),
    ('E23', 'G1', 'IE2', 29.47, 80, 'pavimentado'),
    ('E24', 'A', 'IE', 39, 25, 'bueno'),
    ('E40', 'IE', 'IE2', 25, 100, 'bueno'),
    ('E41', 'IE2', 'M', 35, 25, 'bueno'),
    ('E25', 'IE1', 'IE2', 15, 100, 'pavimentado'),
    ('E42', 'IE1', 'O', 45.52, 15, 'pavimentado'),
    ('E26', 'O', 'N', 86.85, 80, 'pavimentado'),
    ('E27', 'B', 'ESTA', 70, 0, 'bueno'),
    ('E28', 'ESTA', 'J', 10, 0, 'bueno'),
    ('E29', 'ESTA', 'ESTD', 0, 0, 'bueno'),
    ('E30', 'ESTD', 'J', 100, 0, 'bueno'),
    ('E31', 'J', 'N', 150, 5, 'bueno'),
    ('E32', 'A', 'B', 200, 15, 'regular'),
    ('E33', 'A', 'ESTA', 180, 0, 'bueno'),
    ('E34', 'CAS1', 'IE1', 35, 90, 'bueno'),
    ('E35', 'O', 'CAS1', 150, 70, 'bueno'),
    ('E36', 'CAS2', 'J', 100, 0, 'bueno'),
    ('E37', 'CAS2', 'N', 41, 15, 'bueno'),
    ('E38', 'CAS3', 'L', 120, 0, 'bueno'),
    ('E39', 'CAS3', 'EXP', 110, 0, 'bueno'),
]

COLORES_NODOS = {
    'academico': '#3498db',
    'administrativo': '#e74c3c',
    'laboratorio': '#9b59b6',
    'servicio': '#f39c12',
    'deportivo': '#27ae60',
    'especial': '#e67e22',
    'estacionamiento': '#95a5a6',
    'seguridad': '#34495e',
    'escaleras': "#c74387"
}

def obtener_color_techado(porcentaje):
    if porcentaje >= 75:
        return '#27ae60'
    elif porcentaje >= 50:
        return '#f39c12'
    elif porcentaje >= 25:
        return '#3498db'
    else:
        return '#95a5a6'

def visualizar_grafo_mejorado(guardar=False, nombre_archivo='grafo_itsx_mejorado.png'):
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(24, 14), facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    G = nx.MultiGraph()
    pos = {nodo: datos['pos'] for nodo, datos in nodos.items()}
    
    for nodo in nodos:
        G.add_node(nodo)
    
    for arista in aristas:
        id_arista, origen, destino, dist, porcentaje_techado, acceso = arista
        G.add_edge(origen, destino, key=id_arista, distancia=dist, 
                   porcentaje_techado=porcentaje_techado, accesibilidad=acceso)
    
    for arista in aristas:
        id_arista, origen, destino, dist, porcentaje_techado, acceso = arista
        color = obtener_color_techado(porcentaje_techado)
        
        if porcentaje_techado >= 75:
            ancho = 5
        elif porcentaje_techado >= 50:
            ancho = 4
        elif porcentaje_techado >= 25:
            ancho = 3
        else:
            ancho = 2.5
        
        num_edges = G.number_of_edges(origen, destino)
        if num_edges > 1:
            edges_list = list(G[origen][destino].keys())
            idx = edges_list.index(id_arista)
            rad = 0.2 * (idx - (num_edges - 1) / 2)
        else:
            rad = 0
        
        nx.draw_networkx_edges(G, pos, edgelist=[(origen, destino)],
                              edge_color='#bdc3c7', width=ancho + 1, alpha=0.3,
                              connectionstyle=f"arc3,rad={rad}", ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=[(origen, destino)],
                              edge_color=color, width=ancho, alpha=0.7,
                              connectionstyle=f"arc3,rad={rad}", ax=ax)
    
    colores_nodos = [COLORES_NODOS[nodos[nodo]['tipo']] for nodo in G.nodes()]
    tamaños_nodos = [1200 if nodos[nodo]['tipo'] in ['especial', 'administrativo'] else 900 for nodo in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color='#34495e',
                          node_size=[t + 100 for t in tamaños_nodos], alpha=0.15, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=colores_nodos, node_size=tamaños_nodos,
                          edgecolors='white', linewidths=3, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold',
                           font_color='white', font_family='sans-serif', ax=ax)
    
    for arista in aristas:
        id_arista, origen, destino, dist, porcentaje_techado, acceso = arista
        x = (pos[origen][0] + pos[destino][0]) / 2
        y = (pos[origen][1] + pos[destino][1]) / 2
        
        num_edges = G.number_of_edges(origen, destino)
        if num_edges > 1:
            edges_list = list(G[origen][destino].keys())
            idx = edges_list.index(id_arista)
            offset = 15 * (idx - (num_edges - 1) / 2)
            dx = pos[destino][0] - pos[origen][0]
            dy = pos[destino][1] - pos[origen][1]
            length = np.sqrt(dx**2 + dy**2)
            if length > 0:
                x += -dy / length * offset
                y += dx / length * offset
        
        label = f"{dist:.0f}m\n{porcentaje_techado}%"
        bbox_props = dict(boxstyle="round,pad=0.3", facecolor='white',
                         edgecolor='#bdc3c7', alpha=0.9, linewidth=1)
        ax.text(x, y, label, fontsize=7, fontweight='bold', color='#2c3e50',
               ha='center', va='center', bbox=bbox_props, zorder=5)
    ax.text(0.5, 0.96, 'Instituto Tecnológico Superior de Xalapa',
           transform=fig.transFigure, fontsize=14, color='#7f8c8d', ha='center', style='italic')
    handles_aristas = [
        mpatches.Patch(color='#27ae60', label='75-100% Techado'),
        mpatches.Patch(color='#f39c12', label='50-74% Techado'),
        mpatches.Patch(color='#3498db', label='25-49% Techado'),
        mpatches.Patch(color='#95a5a6', label='0-24% Techado')
    ]
    ax.legend(handles=handles_aristas, title='Porcentaje de Techado',
             loc='upper right', fontsize=10, title_fontsize=12,
             frameon=True, fancybox=True, shadow=True, framealpha=0.95)
        
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.margins(0.05)
    ax.grid(True, linestyle='--', alpha=0.2, color='#95a5a6')
    ax.set_axisbelow(True)
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()


def encontrar_ruta_max_techado(origen, destino):

    if origen not in nodos or destino not in nodos:
        print(f"Error: Nodos '{origen}' o '{destino}' no existen")
        return None
    
    G = nx.Graph()
    aristas_dict = {}
    
    for arista in aristas:
        id_arista, o, d, dist, techado, acceso = arista
        key = (o, d) if o < d else (d, o)
        if key not in aristas_dict or techado > aristas_dict[key]['techado']:
            aristas_dict[key] = {'dist': dist, 'techado': techado, 'id': id_arista}
    
    for (o, d), data in aristas_dict.items():
        G.add_edge(o, d, **data)
    
    if not nx.has_path(G, origen, destino):
        print(f"No existe camino entre {origen} y {destino}")
        return None
    
    camino_corto = nx.shortest_path(G, origen, destino, weight='dist')
    dist_min = sum(aristas_dict[(camino_corto[i], camino_corto[i+1]) if camino_corto[i] < camino_corto[i+1] 
                                 else (camino_corto[i+1], camino_corto[i])]['dist'] 
                   for i in range(len(camino_corto) - 1))
    
    try:
        todas_rutas = list(nx.all_simple_paths(G, origen, destino, cutoff=8))
        if len(todas_rutas) > 50:
            todas_rutas = todas_rutas[:50]
    except:
        todas_rutas = [camino_corto]
    
    mejor_ruta = None
    mejor_score = -999999
    mejor_distancia = 0
    mejor_techado = 0

    for ruta in todas_rutas:
        dist_total = 0
        techado_ponderado = 0
        
        for i in range(len(ruta) - 1):
            o, d = ruta[i], ruta[i+1]
            key = (o, d) if o < d else (d, o)
            data = aristas_dict[key]
            dist_total += data['dist']
            techado_ponderado += data['techado'] * data['dist']
        
        promedio_techado = techado_ponderado / dist_total if dist_total > 0 else 0
        
        exceso_distancia = max(0, dist_total - dist_min)
        penalizacion_dist = (exceso_distancia / dist_min) * 100 if dist_min > 0 else 0
        
        score = (promedio_techado * 0.7) - (penalizacion_dist * 0.3)
        
        if score > mejor_score:
            mejor_score = score
            mejor_ruta = ruta
            mejor_distancia = dist_total
            mejor_techado = promedio_techado
    
    detalles = []
    for i in range(len(mejor_ruta) - 1):
        o, d = mejor_ruta[i], mejor_ruta[i+1]
        key = (o, d) if o < d else (d, o)
        data = aristas_dict[key]
        detalles.append({
            'desde': mejor_ruta[i],
            'hasta': mejor_ruta[i+1],
            'distancia': data['dist'],
            'techado': data['techado']
        })
    
    return {
        'camino': mejor_ruta,
        'detalles': detalles,
        'distancia_total': mejor_distancia,
        'techado_promedio': mejor_techado,
        'score': mejor_score,
        'distancia_minima': dist_min
    }

def visualizar_ruta_en_grafo(resultado, guardar=False):
    origen = resultado['camino'][0]
    destino = resultado['camino'][-1]
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(24, 14), facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    G = nx.MultiGraph()
    pos = {nodo: datos['pos'] for nodo, datos in nodos.items()}
    
    for nodo in nodos:
        G.add_node(nodo)
    
    for arista in aristas:
        id_arista, o, d, dist, porcentaje_techado, acceso = arista
        G.add_edge(o, d, key=id_arista, distancia=dist, 
                   porcentaje_techado=porcentaje_techado, accesibilidad=acceso)
    
    aristas_ruta = set()
    for i in range(len(resultado['camino']) - 1):
        n1, n2 = resultado['camino'][i], resultado['camino'][i+1]
        aristas_ruta.add((n1, n2))
        aristas_ruta.add((n2, n1))

    for arista in aristas:
        id_arista, o, d, dist, porcentaje_techado, acceso = arista
        es_ruta = (o, d) in aristas_ruta or (d, o) in aristas_ruta
        
        if not es_ruta:
            color = obtener_color_techado(porcentaje_techado)
            
            if porcentaje_techado >= 75:
                ancho = 5
            elif porcentaje_techado >= 50:
                ancho = 4
            elif porcentaje_techado >= 25:
                ancho = 3
            else:
                ancho = 2.5
            
            num_edges = G.number_of_edges(o, d)
            if num_edges > 1:
                edges_list = list(G[o][d].keys())
                idx = edges_list.index(id_arista)
                rad = 0.2 * (idx - (num_edges - 1) / 2)
            else:
                rad = 0
            
            nx.draw_networkx_edges(G, pos, edgelist=[(o, d)],
                                  edge_color='#bdc3c7', width=ancho + 1, alpha=0.2,
                                  connectionstyle=f"arc3,rad={rad}", ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=[(o, d)],
                                  edge_color=color, width=ancho, alpha=0.3,
                                  connectionstyle=f"arc3,rad={rad}", ax=ax)
    
    for i in range(len(resultado['camino']) - 1):
        o, d = resultado['camino'][i], resultado['camino'][i+1]

        nx.draw_networkx_edges(G, pos, edgelist=[(o, d)],
                              edge_color='#2980b9', width=9, alpha=0.4, ax=ax)
        

        nx.draw_networkx_edges(G, pos, edgelist=[(o, d)],
                              edge_color='#3498db', width=7, alpha=0.95, ax=ax)
    
    colores_nodos = []
    tamaños_nodos = []
    for nodo in G.nodes():
        if nodo == origen or nodo == destino:
            colores_nodos.append('#e74c3c')  
            tamaños_nodos.append(1500)
        elif nodo in resultado['camino']:
            colores_nodos.append('#3498db')  
            tamaños_nodos.append(1300)
        else:
            colores_nodos.append(COLORES_NODOS[nodos[nodo]['tipo']])
            tamaños_nodos.append(1200 if nodos[nodo]['tipo'] in ['especial', 'administrativo'] else 900)
    
    nx.draw_networkx_nodes(G, pos, node_color='#34495e',
                          node_size=[t + 100 for t in tamaños_nodos], alpha=0.15, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=colores_nodos, node_size=tamaños_nodos,
                          edgecolors='white', linewidths=3, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold',
                           font_color='white', font_family='sans-serif', ax=ax)
    
    for arista in aristas:
        id_arista, o, d, dist, porcentaje_techado, acceso = arista
        
        es_ruta = (o, d) in aristas_ruta or (d, o) in aristas_ruta
        
        if es_ruta:
            x = (pos[o][0] + pos[d][0]) / 2
            y = (pos[o][1] + pos[d][1]) / 2
            
            num_edges = G.number_of_edges(o, d)
            if num_edges > 1:
                edges_list = list(G[o][d].keys())
                idx = edges_list.index(id_arista)
                offset = 15 * (idx - (num_edges - 1) / 2)
                dx = pos[d][0] - pos[o][0]
                dy = pos[d][1] - pos[o][1]
                length = np.sqrt(dx**2 + dy**2)
                if length > 0:
                    x += -dy / length * offset
                    y += dx / length * offset
            
            label = f"{dist:.0f}m\n{porcentaje_techado}%"
            bbox_props = dict(boxstyle="round,pad=0.3", facecolor='#3498db',
                             edgecolor='#2980b9', alpha=0.9, linewidth=2)
            ax.text(x, y, label, fontsize=8, fontweight='bold', color='white',
                   ha='center', va='center', bbox=bbox_props, zorder=10)
    
    handles = [
        mpatches.Patch(color='#3498db', label='Ruta Óptima Seleccionada'),
        mpatches.Patch(color='#e74c3c', label='Origen / Destino'),
        mpatches.Patch(color='#95a5a6', label='Otras rutas disponibles')
    ]
    ax.legend(handles=handles, title='Elementos del Mapa',
             loc='upper right', fontsize=11, title_fontsize=13,
             frameon=True, fancybox=True, shadow=True, framealpha=0.95)
    
    info_text = f"Camino: {' → '.join(resultado['camino'])}"
    ax.text(0.5, 0.02, info_text, transform=fig.transFigure, fontsize=11,
           color='#2c3e50', ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                    edgecolor='#3498db', alpha=0.9, linewidth=2))
    
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.margins(0.05)
    ax.grid(True, linestyle='--', alpha=0.2, color='#95a5a6')
    ax.set_axisbelow(True)
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    plt.show()

def mostrar_ruta_interactiva():
    while True:
        print("\n Edificios disponibles:")
        print("-" * 70)
        edificios = sorted(nodos.items())
        for i in range(0, len(edificios), 3):
            linea = ""
            for j in range(3):
                if i + j < len(edificios):
                    cod, info = edificios[i + j]
                    linea += f"  {cod:6s} - {info['nombre']:25s}"
            print(linea)
        
        print("\n" + "="*70)
        print("Ingrese el nodo de ORIGEN (o 'salir' para terminar): ", end="")
        origen = input().strip().upper()
        
        if origen.lower() == 'salir':
            print("\n Adiós\n")
            break
        
        if origen not in nodos:
            print(f"Error: '{origen}' no existe")
            continue
        
        print("Ingrese el nodo de DESTINO: ", end="")
        destino = input().strip().upper()
        
        if destino not in nodos:
            print(f" Error: '{destino}' no existe")
            continue
        
        if origen == destino:
            print("Error: Origen y destino deben ser diferentes")
            continue
        
        resultado = encontrar_ruta_max_techado(origen, destino)
        
        if resultado:
            print(f"Camino: {' → '.join(resultado['camino'])}")
            print(f"Techado promedio: {resultado['techado_promedio']:.1f}%")
            print(f"Score de ruta: {resultado['score']:.1f}")
            print(f" Número de segmentos: {len(resultado['detalles'])}")
            print("\nDetalles por segmento:")
            print("-" * 70)
            for i, det in enumerate(resultado['detalles'], 1):
                print(f"  {i}. {det['desde']:6s} → {det['hasta']:6s} | "
                      f"{det['distancia']:6.1f}m | Techado: {det['techado']:5.1f}%")
            print("="*70)
            
            print("\n¿Desea visualizar la ruta en el grafo? (s/n): ", end="")
            visualizar = input().strip().lower()
            if visualizar == 's':
                visualizar_ruta_en_grafo(resultado)

def main():
    print("\nOpciones:")
    print("  1. Ver grafo completo del campus")
    print("  2. Calcular ruta óptima (máximo techado + distancia corta)")
    opcion = input("\nSeleccione una opción (1-2): ").strip()
    
    if opcion == '1':
        visualizar_grafo_mejorado(guardar=False)
    elif opcion == '2':
        mostrar_ruta_interactiva()
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()
