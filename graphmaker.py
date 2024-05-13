import networkx as nx
from sklearn.cluster import KMeans
from segments import *
import numpy as np
import matplotlib.pyplot as plt


def make_graph(segments: list[Segment], clusters: int) -> nx.Graph:
    """Make a graph from the segments."""
    punts = segments_a_numpy(segments)
    kmeans = KMeans(n_clusters = clusters)
    kmeans.fit(punts)
    centroides = kmeans.cluster_centers_ # retorna una tripleta amb el numero de centroid i la tupla altitud latitud
    etiquetas = kmeans.labels_ # llista de enters que diu a quin centroid pertany cada punt
    graf = nx.Graph()
    for i, centroid in enumerate(centroides):
        graf.add_node(i,pos = centroid)
    aristas = arestes(etiquetas)
    graf.add_edges_from(aristas)

    return graf
    
'''def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""'''
    
def segments_a_numpy(segments: list[Segment]) -> np.array:
    points = []
    for segment in segments:
        points.append(segment.start)
        points.append(segment.end)
    points_array = np.array([[point.lat, point.lon] for point in points])
    return points_array

def arestes(etiquetas:list[int]) -> list[tuple[int,int]]: # llista de cluster de sortida i d'eentrada
    arestes_Centroides: list[tuple[int,int]] = []
    for i in range(0,len(etiquetas),2):
        if etiquetas[i] != etiquetas[i+1]:
            arestes_Centroides.append([etiquetas[i],etiquetas[i+1]])
    return arestes_Centroides
        
nx.draw(make_graph(), with_labels=True)
plt.show()