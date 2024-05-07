import networkx as nx
from sklearn.cluster import KMeans


def make_graph(segments: Segments, clusters: int) -> nx.Graph:
    """Make a graph from the segments."""
    vertices = vertexs()
    arestes = 

    
def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""
  
def vertexs(dades: list[tuple(int, int)]) -> list[list[int, int]]:
    # Definimos el número de clusters que queremos
    n_clusters = 2 #Donat per l'usuari

    # Inicializamos el modelo de KMeans
    kmeans = KMeans(n_clusters = n_clusters)

    # Entrenamos el modelo con nuestros datos
    kmeans.fit(dades)

    # Obtenemos los centroides
    centroides: list[list[int, int]] = kmeans.cluster_centers_

    # Obtenemos las etiquetas de cluster para cada punto
    etiquetas = kmeans.labels_
    return centroides
