import networkx as nx
from segments import Point
from monuments import Monument
from staticmap import StaticMap, CircleMarker, Line
import simplekml 
from viewer import graph
from monuments import load_monuments, Monuments
from segments import Box
from scipy.spatial.distance import euclidean
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

def euclidean(pos1, pos2):
    # Factor de conversión de grados de latitud/longitud a kilómetros
    conversion_factor = 111.319  # Aproximadamente, 1 grado de latitud/longitud ≈ 111.32 km
    # Calcular la diferencia de latitud y longitud en grados
    delta_lat = pos1[0] - pos2[0]
    delta_lon = pos1[1] - pos2[1]
    # Calcular la distancia euclidiana en kilómetros
    distance_km = sqrt((delta_lat * conversion_factor)**2 + (delta_lon * conversion_factor)**2)
    return distance_km



def find_routes(graph: nx.Graph, start: Point, endpoints: list[Monument]) -> nx.Graph:
    # Create a new graph for the shortest routes
    shortest_routes_graph = nx.Graph()

    # Associate start point and endpoints with the closest nodes in the original graph
    closest_nodes = {}
    remaining_nodes = set(graph.nodes)
    for location in [start] + [monument.location for monument in endpoints]:
        closest_node = min(remaining_nodes, key=lambda node: euclidean(graph.nodes[node]['pos'], (location.lat, location.lon)))
        closest_nodes[(location.lat, location.lon)] = closest_node
        remaining_nodes.remove(closest_node)

    # Add nodes to the new graph
    for node in closest_nodes.values():
        shortest_routes_graph.add_node(node, pos=(graph.nodes[node]['pos'][0], graph.nodes[node]['pos'][1]))

    # Find the shortest paths between the start node and each endpoint node
    for monument in endpoints:
        shortest_path = nx.shortest_path(graph, source=closest_nodes[(start.lat, start.lon)], target=closest_nodes[(monument.location.lat, monument.location.lon)], weight = 'weight')
        for i in range(len(shortest_path) - 1):
            shortest_routes_graph.add_edge(shortest_path[i], shortest_path[i + 1])
    
    return shortest_routes_graph


def dijkstra_distances(graph: nx.Graph, start: Point) -> nx.Graph:
    # Find the closest node to the start point
    start_node = min(graph.nodes, key=lambda node: euclidean(graph.nodes[node]['pos'], (start.lat, start.lon)))

    # Calculate the shortest path lengths and paths from the start node to all other nodes
    lengths, paths = nx.single_source_dijkstra(graph, source=start_node, weight='weight')

    # Create a new graph to store the distances and paths
    distances_graph = nx.Graph()

    # Add nodes to the new graph with their distances from the start node
    for node, dist in lengths.items():
        distances_graph.add_node(node, pos=(graph.nodes[node]['pos'][0], graph.nodes[node]['pos'][1]), distance=dist)
    
    # Add edges to the new graph based on the shortest paths
    for target_node, path in paths.items():
        if len(path) > 1:
            total_distance = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                # Calculate the distance between nodes and use it as weight
                weight = euclidean(graph.nodes[u]['pos'], graph.nodes[v]['pos'])
                total_distance += weight
                distances_graph.add_edge(u, v, weight=weight)
            distances_graph.nodes[target_node]['distance'] = total_distance
      
    return distances_graph

def visualize_graph(graph: nx.Graph, start: Point, filename:str):
    # Find the closest node to the start point
    start_node = min(graph.nodes, key=lambda node: euclidean(graph.nodes[node]['pos'], (start.lat, start.lon)))

    pos = nx.get_node_attributes(graph, 'pos')
    distances = nx.get_node_attributes(graph, 'distance')

    plt.figure(figsize=(12, 8))

    # Draw nodes
    node_colors = ['red' if node == start_node else 'black' for node in graph.nodes]
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos)

    # Draw node labels
    nx.draw_networkx_labels(graph, pos, labels={node: f"{node}" for node in graph.nodes}, font_color='white')

    # Draw distance labels
    distance_labels = {node: f"{dist:.2f}" for node, dist in distances.items()}
    nx.draw_networkx_labels(graph, pos, labels=distance_labels, font_color='blue', font_weight='bold', verticalalignment='bottom')

    plt.title("Graph Visualization with Dijkstra's Shortest Paths")
    #Guardar la visualización en un archivo PNG
    plt.savefig(filename)

def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""
    static_map = StaticMap(800, 600)
    arestes_PNG(graph, static_map)
    nodes_PNG(graph, static_map)
    image = static_map.render()
    image.save(filename)


def arestes_PNG(graph: nx.Graph, static_map: StaticMap)-> None:
    """Adds the edges of a graph to a StaticMap as Lines"""
    for edge in graph.edges():
        start_lat = graph.nodes[edge[0]]["pos"][0]
        start_lon = graph.nodes[edge[0]]["pos"][1]
        end_lat = graph.nodes[edge[1]]["pos"][0]
        end_lon = graph.nodes[edge[1]]["pos"][1]
        line = Line([(start_lat, start_lon), (end_lat,end_lon)], "blue", 2)
        static_map.add_line(line)


def nodes_PNG(graph: nx.Graph, static_map: StaticMap)->None:
    """Adds the nodes of a graph to a StaticMap as CircleMarkers"""
    for node in graph.nodes():
        pos = graph.nodes[node]["pos"]
        Marker = CircleMarker(pos, "red", 6)
        static_map.add_marker(Marker)

start_point = Point(lat=40.55, lon=0.6739316671)
grafo = find_routes(graph, start_point, load_monuments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)),'monuments.dat'))
grafo = dijkstra_distances(grafo,start_point)
export_PNG(grafo, 'graf2.png')
visualize_graph(grafo, start_point,'graf.png')
