import networkx as nx
from sklearn.cluster import KMeans
from segments import Segment, Point, load_segments
import numpy as np
import matplotlib.pyplot as plt
from math import acos, degrees

def create_graph(segments: list[Segment], num_clusters: int) -> nx.Graph:
    """Create and simplify a graph from the segments"""
    points = convert_segments_to_numpy(segments)
    kmeans = KMeans(num_clusters)
    kmeans.fit(points)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
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


def build_graph(centroids: np.ndarray, labels: np.ndarray) -> nx.Graph:
    """Build a graph based on the centroids and their labels"""
    graph = nx.Graph()
    for i, centroid in enumerate(centroids):
        graph.add_node(i, pos=centroid)
    
    edges = create_edges(labels)
    graph.add_edges_from(edges)
    
    # Remove nodes with no edges
    nodes_to_remove = [node for node in graph.nodes() if graph.degree[node] == 0]
    graph.remove_nodes_from(nodes_to_remove)

    return graph


def create_edges(labels: np.ndarray) -> list[tuple[int, int]]:
    """
    Create edges based on the labels of the clusters"""
    centroid_edges: list[tuple[int, int]] = []
    max_cluster = max(labels) + 1
    adjacency_matrix: list[list[int]] = [[0 for _ in range(max_cluster)] for _ in range(max_cluster)]

    # Fill the adjacency matrix with the connections between clusters
    for i in range(0, len(labels), 2):
        if labels[i] != labels[i + 1]:
            cluster1, cluster2 = labels[i], labels[i + 1]
            adjacency_matrix[cluster1][cluster2] += 1

    # Add edges if there are 2 or more paths between clusters
    for cluster1 in range(max_cluster):
        for cluster2 in range(max_cluster):
            if adjacency_matrix[cluster1][cluster2] + adjacency_matrix[cluster2][cluster1] >= 2:
                centroid_edges.append((cluster1, cluster2))

    return centroid_edges


def simplify_graph(graph: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph by removing nodes with exactly two edges 
    if the angle between the edges is near 180 degrees"""
    nodes_to_remove = find_nodes_to_remove(graph, epsilon)
    simplified_graph = graph.copy()

    for node, neighbor1, neighbor2 in nodes_to_remove:
        if simplified_graph.has_node(node) and simplified_graph.has_node(neighbor1) and simplified_graph.has_node(neighbor2):
            simplified_graph.add_edge(neighbor1, neighbor2)
            simplified_graph.remove_node(node)

    return simplified_graph


def find_nodes_to_remove(graph: nx.Graph, epsilon: float) -> list[tuple[int, int, int]]:
    """Returns the list of nodes which should be simplified"""
    nodes = []
    for node in list(graph.nodes):
        neighbors = list(graph.neighbors(node))
        if len(neighbors) == 2:
            p1, p2, p3 = graph.nodes[neighbors[0]]['pos'], graph.nodes[node]['pos'], graph.nodes[neighbors[1]]['pos']
            angle = calculate_angle(p1, p2, p3)
            if abs(angle - 180) < epsilon:
                nodes.append((node, neighbors[0], neighbors[1]))
    return nodes


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
