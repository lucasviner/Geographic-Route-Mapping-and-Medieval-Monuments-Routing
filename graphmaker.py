import networkx as nx
from sklearn.cluster import KMeans
from segments import Segment, Point
import numpy as np
from math import acos, degrees


def make_graph(segments: list[Segment], num_clusters: int) -> nx.Graph:
    """Create and simplify a graph from the segments"""
    points = convert_segments_to_numpy(segments)
    centroids, labels = perform_kmeans_clustering(points, num_clusters)
    graph = build_graph(centroids, labels)
    simplified_graph = simplify_graph(graph, 20)

    return simplified_graph


def convert_segments_to_numpy(segments: list[Segment]) -> np.ndarray:
    """Convert a list of segments to a numpy array of points"""
    points: list[Point] = []
    for segment in segments:
        points.append(segment.start)
        points.append(segment.end)
    points_array = np.array([[point.lat, point.lon] for point in points])

    return points_array


def perform_kmeans_clustering(points: np.ndarray, num_clusters: int) -> tuple[np.ndarray, np.ndarray]:
    """ Perform KMeans clustering on the points. """
    kmeans = KMeans(num_clusters)
    kmeans.fit(points)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    return centroids, labels


def build_graph(centroids: np.ndarray, labels: np.ndarray) -> nx.Graph:
    """Build a graph based on the centroids and their labels"""
    graph = nx.Graph()
    add_nodes_to_graph(graph, centroids)
    edges = create_edges(labels)
    graph.add_edges_from(edges)
    remove_nodes_with_no_edges(graph)
    
    return graph


def add_nodes_to_graph(graph: nx.Graph, centroids: np.ndarray) -> None:
    """Add nodes to the graph based on centroids."""
    for i, centroid in enumerate(centroids):
        graph.add_node(i, pos=centroid)


def create_edges(labels: np.ndarray) -> list[tuple[int, int]]:
    """Create edges based on the labels of the clusters"""
    max_cluster = max(labels) + 1
    adjacency_matrix = create_adjacency_matrix(labels, max_cluster)
    edges = extract_edges_from_matrix(adjacency_matrix, max_cluster)
    
    return edges


def remove_nodes_with_no_edges(graph: nx.Graph) -> None:
    """Remove nodes from the graph that have no edges."""
    nodes_to_remove = [node for node in graph.nodes() if graph.degree[node] == 0]
    graph.remove_nodes_from(nodes_to_remove)
    

def create_adjacency_matrix(labels: np.ndarray, max_cluster:int) -> list[list[int]]:
    """Create an adjacency matrix from the cluster labels."""
    adjacency_matrix: list[list[int]] = [[0 for _ in range(max_cluster)] for _ in range(max_cluster)]
    for i in range(0, len(labels), 2):
        if labels[i] != labels[i + 1]:
            cluster1, cluster2 = labels[i], labels[i + 1]
            adjacency_matrix[cluster1][cluster2] += 1
            
    return adjacency_matrix


def extract_edges_from_matrix(adjacency_matrix: list[list[int]], max_cluster: int) -> list[tuple[int,int]]:
    """ Extract edges from the adjacency matrix. """
    centroid_edges: list[tuple[int, int]] = []
    for cluster1 in range(max_cluster):
        for cluster2 in range(max_cluster):
            if adjacency_matrix[cluster1][cluster2] + adjacency_matrix[cluster2][cluster1] >= 2:
                centroid_edges.append((cluster1, cluster2))

    return centroid_edges


def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph by removing nodes with exactly two edges if the angle between the edges is near 180 degrees"""
    nodes_to_remove = find_nodes_to_remove(graph, epsilon)
    remove_nodes(graph, nodes_to_remove)

    return graph 

            
def find_nodes_to_remove(graph: nx.Graph, epsilon: float) -> list[tuple[int, int, int]]:
    """Returns the list of nodes which should be simplified"""
    nodes_to_remove: list[tuple[int, int, int]] = []
    for node in list(graph.nodes):
        neighbors = list(graph.neighbors(node))
        if len(neighbors) == 2:
            p1, p2, p3 = graph.nodes[neighbors[0]]['pos'], graph.nodes[node]['pos'], graph.nodes[neighbors[1]]['pos']
            angle = calculate_angle(p1, p2, p3)
            if abs(angle - 180) < epsilon:
                nodes_to_remove.append((node, neighbors[0], neighbors[1]))
                
    return nodes_to_remove


def remove_nodes(graph: nx.Graph, nodes_to_remove: list[tuple[int, int, int]]) -> None:
    """Remove nodes from the graph and connect their neighbors."""
    for node, neighbor1, neighbor2 in nodes_to_remove:
        if graph.has_node(node) and graph.has_node(neighbor1) and graph.has_node(neighbor2):
            # Add edge between the two neighbors if not already present
            if not graph.has_edge(neighbor1, neighbor2):
                graph.add_edge(neighbor1, neighbor2)
            # Remove the node and its edges
            graph.remove_node(node)


def calculate_angle(p1: list[float], p2: list[float], p3: list[float]) -> float:
    """Calculate the angle between three points p1, p2, and p3 with p2 being the vertex"""

    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = degrees(acos(cos_angle))

    return angle


# Example usage
'''
segments = load_segments('filename.txt')
G = create_graph(segments, 20)
plt.figure(figsize=(10, 8))
nx.draw(G, with_labels=True, node_color='blue', node_size=12)
plt.show()
'''