import networkx as nx #type: ignore 
from sklearn.cluster import KMeans #type: ignore 
from segments import * #type: ignore 
import numpy as np
import matplotlib.pyplot as plt
from math import acos, degrees


def make_graph(segments: list[Segment], clusters: int) -> nx.Graph:
    """Make a graph from the segments."""
    punts = segments_a_numpy(segments)
    
    kmeans = KMeans(clusters)
    kmeans.fit(punts) # type: ignore
    centroides = kmeans.cluster_centers_ # type: ignore retorna una tripleta amb el numero de centroid i la tupla altitud latitud
    etiquetas = kmeans.labels_ # type: ignore llista de enters que diu a quin centroid pertany cada punt
    graf = nx.Graph()
    for i, centroid in enumerate(centroides):
        graf.add_node(i, pos = centroid)
    aristas = arestes(etiquetas)
    graf.add_edges_from(aristas)
    
    nodes_to_remove = [node for node in graf.nodes() if graf.degree[node] == 0]
    graf.remove_nodes_from(nodes_to_remove)
    '''simplificat= simplify_graph(graf, 20)
    return simplificat'''
    return graf
    
def segments_a_numpy(segments: list[Segment]) -> np.array:
    """Changes a list of segments to a numpy array of segments"""
    points:list[Point] = []
    for segment in segments:
        points.append(segment.start)
        points.append(segment.end)
    points_array = np.array([[point.lat, point.lon] for point in points])
    return points_array

def arestes(etiquetas:list[int]) -> list[tuple[int,int]]: # llista de cluster de sortida i d'eentrada
    arestes_Centroides: list[tuple[int, int]] = []
    
    # Encuentra el número máximo de clusters
    max_cluster = max(etiquetas) + 1
    
    # Inicializa la matriz de adyacencia
    matriu: list[list[int]] = [[0 for _ in range(max_cluster)] for _ in range(max_cluster)]
    
    # Rellena la matriz de adyacencia con las conexiones entre clusters
    for i in range(0, len(etiquetas), 2):
        if etiquetas[i] != etiquetas[i + 1]:
            e1, e2 = etiquetas[i], etiquetas[i + 1]
            matriu[e1][e2] += 1
    
    # Añade aristas si hay 2 caminos o más entre clusters
    for e1 in range(max_cluster):
        for e2 in range(max_cluster):
            if matriu[e1][e2] + matriu [e2][e1] >= 2:
                arestes_Centroides.append((e1, e2))
    
    return arestes_Centroides

        
def calculate_angle(p1, p2, p3):
    """Calculate the angle between three points p1, p2, and p3 with p2 being the vertex."""
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = degrees(acos(cos_angle))
    
    return angle

def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph by removing nodes with exactly two edges if the angle between the edges is near 180 degrees."""
    nodes_to_remove = []
    
    for node in list(graph.nodes):
        neighbors = list(graph.neighbors(node))
        if len(neighbors) == 2:
            p1, p2, p3 = graph.nodes[neighbors[0]]['pos'], graph.nodes[node]['pos'], graph.nodes[neighbors[1]]['pos']
            angle = calculate_angle(p1, p2, p3)
            
            if abs(angle - 180) < epsilon:
                nodes_to_remove.append((node, neighbors[0], neighbors[1]))
    
    simplified_graph = graph.copy()
    
    for node, neighbor1, neighbor2 in nodes_to_remove:
        if simplified_graph.has_node(node) and simplified_graph.has_node(neighbor1) and simplified_graph.has_node(neighbor2):
            simplified_graph.add_edge(neighbor1, neighbor2)
            simplified_graph.remove_node(node)
    
    return simplified_graph


# COMPROVACIÓ 
"""
segments = [Segment(start=Point(lat=40.675465, lon=0.154932), end=Point(lat=40.675782, lon=0.154152)), Segment(start=Point(lat=40.67548, lon=0.154905), end=Point(lat=40.675793, lon=0.154127)), Segment(start=Point(lat=40.675491, lon=0.154884), end=Point(lat=40.67581, lon=0.154092)), Segment(start=Point(lat=40.675502, lon=0.154867), end=Point(lat=40.675821, lon=0.154065)), Segment(start=Point(lat=40.675513, lon=0.154855), end=Point(lat=40.67583, lon=0.154041)), Segment(start=Point(lat=40.675517, lon=0.154847), end=Point(lat=40.675839, lon=0.154016)), Segment(start=Point(lat=40.675524, lon=0.154836), end=Point(lat=40.675848, lon=0.153992)), Segment(start=Point(lat=40.675528, lon=0.15483), end=Point(lat=40.675863, lon=0.153962)), Segment(start=Point(lat=40.675532, lon=0.154833), end=Point(lat=40.675874, lon=0.153941)), Segment(start=Point(lat=40.675531, lon=0.154838), end=Point(lat=40.675882, lon=0.15391)), Segment(start=Point(lat=40.675529, lon=0.154839), end=Point(lat=40.675886, lon=0.153883)), Segment(start=Point(lat=40.67553, lon=0.154839), end=Point(lat=40.675893, lon=0.153857)), Segment(start=Point(lat=40.67553, lon=0.154839), end=Point(lat=40.675903, lon=0.153825)), Segment(start=Point(lat=40.675533, lon=0.154833), end=Point(lat=40.675912, lon=0.153806)), Segment(start=Point(lat=40.675533, lon=0.154835), end=Point(lat=40.67593, lon=0.153776)), Segment(start=Point(lat=40.675533, lon=0.154835), end=Point(lat=40.675946, lon=0.153757)), Segment(start=Point(lat=40.675534, lon=0.154833), end=Point(lat=40.675966, lon=0.153737)), Segment(start=Point(lat=40.675535, lon=0.154831), end=Point(lat=40.675985, lon=0.153719)), Segment(start=Point(lat=40.675542, lon=0.154823), end=Point(lat=40.676004, lon=0.15371)), Segment(start=Point(lat=40.675546, lon=0.154803), end=Point(lat=40.676028, lon=0.153704)), Segment(start=Point(lat=40.675553, lon=0.154785), end=Point(lat=40.676049, lon=0.153708)), Segment(start=Point(lat=40.675564, lon=0.154763), end=Point(lat=40.676065, lon=0.153716))]
G = make_graph(segments, 20)"""
"""
plt.figure(figsize=(10,8))
nx.draw(G, with_labels=True, node_color='blue', node_size=12)
plt.show()"""