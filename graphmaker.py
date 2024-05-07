import networkx as nx
from sklearn.cluster import KMeans
import segments


def make_graph(segments: segments.Segment, clusters: int) -> nx.Graph:
    """Make a graph from the segments."""
    punts= segments_a_punts(segments)
    vertices = vertexs(punts, clusters)
    aristas = arestes(segments,vertices)
    graf = nx.Graph()
    graf.add_nodes_from(vertices)
    graf.add_edges_from(aristas)

    return graf
    
def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""



def segments_a_punts(segments:segments.Segment)-> list[segments.Point]:
    return [(segment.start , segment.end) for segment in segments]

def vertexs(punts: list[segments.Point]) -> list[segments.Point]:
    # Definimos el número de clusters que queremos
    n_clusters = 2 #Donat per l'usuari

    # Inicializamos el modelo de KMeans
    kmeans = KMeans(n_clusters = n_clusters)

    # Entrenamos el modelo con nuestros datos
    kmeans.fit(punts)

    # Obtenemos los centroides
    centroides = kmeans.cluster_centers_

    # Obtenemos las etiquetas de cluster para cada punto
    etiquetas = kmeans.labels_
    return centroides



def arestes(segments: segments.Segment, centroides: list[segments.Point], etiquetas)->list[segments.Segment]:
    arestes_Centroides: list[segments.Segment] = []
    for segment in segments:
        if #(centroide que pertany punt1) != (centroide que pertany a punt 2):
            arestes_Centroides.append(punt1,punt2)
    return arestes_Centroides
        

