import networkx as nx
from sklearn.cluster import KMeans
from segments import *
import numpy as np


def make_graph(segments: list[Segment], clusters: int) -> nx.Graph:
    """Make a graph from the segments."""
    punts = segments_a_punts(segments)
    kmeans = KMeans(n_clusters = clusters)
    kmeans.fit(np.array(punts))
    centroides = kmeans.cluster_centers_ # retorna una tripleta amb el numero de centroid i la tupla altitud latitud
    etiquetas = kmeans.labels_ # llista de enters que diu a quin centroid pertany cada punt
    graf = nx.Graph()
    for i, centroid in list(enumerate(centroides)):
        graf.add_node(i,pos = (centroid[0],centroid[1]))
    aristas = arestes(etiquetas)
    graf.add_edges_from(aristas)

    return graf
    
'''def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""'''
    
def segments_a_punts(segments: list[Segment]) -> np.array:
    return np.array([[segment.start, segment.end] for segment in segments])

def arestes(etiquetas:list[int]) -> list[tuple[int,int]]: # llista de cluster de sortida i d'eentrada
    arestes_Centroides: list[tuple[int,int]] = []
    for i in range(0,len(etiquetas),2):
        if etiquetas[i] != etiquetas[i+1]:
            arestes_Centroides.append((etiquetas[i],etiquetas[i+1]))
    return arestes_Centroides
        
print(make_graph(load_segments("filename.txt"), 10))