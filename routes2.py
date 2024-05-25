import networkx as nx
from segments import Point
from monuments import Monument
from staticmap import StaticMap, CircleMarker, Line
import simplekml 
from viewer import graph
from monuments import load_monuments
from segments import Box
from scipy.spatial.distance import euclidean


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
        shortest_path = nx.shortest_path(graph, source=closest_nodes[(start.lat, start.lon)], target=closest_nodes[(monument.location.lat, monument.location.lon)])
        for i in range(len(shortest_path) - 1):
            shortest_routes_graph.add_edge(shortest_path[i], shortest_path[i + 1])
    print(closest_nodes)
    return shortest_routes_graph


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
export_PNG(grafo, 'graf.png')

