import networkx as nx
from segments import Point, get_segments, Box
from graphmaker import Graph, make_graph
from monuments import Monuments, get_monuments
from typing import TypeAlias, Optional
from staticmap import StaticMap, CircleMarker, Line
from math import *
import simplekml
from geopy.distance import geodesic
from geopy.point import Point as pt



def find_routes(graph: Graph, start_point: Point, monuments: Monuments, filename: str) -> int:
    """Generate routes and save visualizations. Returns 1 if it has found monuments in the selected box, else -1."""
    start_node = find_closest_node(graph, start_point)
    shortest_paths = nx.single_source_dijkstra(graph, source=start_node, weight='weight')
    monuments_nodes = get_monuments_nodes(graph, monuments)
    
    if contains_node(monuments_nodes, shortest_paths):
        route_graph = build_route_graph(graph, monuments_nodes, shortest_paths)
        save_static_map(route_graph, start_node, monuments_nodes, f'{filename}.png')
        save_kml(route_graph, start_node, monuments_nodes,  f'{filename}.kml')
        return 1
    else:
        print('No monuments found in the selected box.')
        return -1


def find_closest_node(graph: Graph, point: Point) -> int:
    """Find the closest node in the graph to a given point."""
    closest_node = None
    min_distance = float('inf')
    for node, data in graph.nodes(data=True):
        lat, lon = data['pos'][1], data['pos'][0]
        distance = geodesic(pt(point.lat, point.lon), pt(lat, lon))
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    return closest_node


def get_monuments_nodes(G: Graph, monuments: Monuments) -> set[int]:
    """Get the set of nodes corresponding to the monuments."""
    return {find_closest_node(G, monument.location) for monument in monuments}


def map_monuments_to_nodes(graph: Graph, monuments: Monuments) -> dict[str, int]:
    """Map each monument to the closest node in the graph."""
    return {monument.name: find_closest_node(graph, monument.location) for monument in monuments}
      

def contains_node(monument_nodes: set, shortest_paths) -> bool:
    """Returns if it contains nodes"""
    return any(monument_node in path for path in shortest_paths[1].values() for monument_node in monument_nodes)


def get_node_position(G: Graph, node: int) -> Optional[tuple[float, float]]:
    """Get the position of a node in the graph."""
    return G.nodes[node]['pos'] if node in G.nodes else None


def build_route_graph(G: Graph, monument_nodes: set, shortest_paths) -> Graph:
    """Build a graph containing only the nodes and edges of the shortest paths to monuments."""
    route_graph = nx.Graph()
    for monument_node in list(monument_nodes):
            for path in list(shortest_paths[1].values()):
                if monument_node in path:
                    path = list(shortest_paths[1][monument_node])
                    add_nodes_and_edges(G, route_graph, path)
    return route_graph


def add_nodes_and_edges(G: Graph, route_graph: Graph, path)-> None:
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        lat1, lon1 = get_node_position(G,u)[0], get_node_position(G,u)[1]
        lat2, lon2 = get_node_position(G,v)[0], get_node_position(G,v)[1]
        weight = geodesic(pt(lat1, lon1), pt(lat2, lon2))
        route_graph.add_edge(u, v, weight=weight)
        route_graph.add_node(u, pos=(lat1,lon1))
        route_graph.add_node(v, pos=(lat2,lon2))
        
    return route_graph

def save_static_map(G: Graph, start_node: int, monument_nodes: set[int], filename: str) -> None:
    """Generate and save a static map image."""
    static_map = StaticMap(800, 800)
    add_nodes_to_static_map(G, static_map, start_node, monument_nodes)
    add_edges_to_static_map(G, static_map)    
    image = static_map.render()
    image.save(filename)


def add_nodes_to_static_map(graph: Graph, static_map: StaticMap, start_node: int, monument_nodes: set[int]) -> None:
    """Add the nodes of a graph to a StaticMap as CircleMarkers."""
    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color, size = ('green', 30) if node == start_node else ('red', 30) if node in monument_nodes else ('blue', 10)
        marker = CircleMarker((pos[0], pos[1]), color, size)
        static_map.add_marker(marker)


def add_edges_to_static_map(graph: Graph, static_map: StaticMap) -> None:
    """Add the edges of a graph to a StaticMap as Lines."""
    for u, v in graph.edges():
        pos_u, pos_v = graph.nodes[u]['pos'], graph.nodes[v]['pos']
        line = Line([(pos_u[0], pos_u[1]), (pos_v[0], pos_v[1])], 'black', 2)
        static_map.add_line(line)


def save_kml(graph: Graph, start_node: int, monument_nodes: set[int], filename: str) -> None:
    """Generate and save a KML file for visualization in Google Earth."""
    kml = simplekml.Kml()
    add_nodes_to_kml(graph, kml, start_node, monument_nodes)
    add_edges_to_kml(graph, kml)
    kml.save(filename)


def add_nodes_to_kml(graph: Graph, kml: simplekml.Kml, start_node: int, monument_nodes: set[int]) -> None:
    """Add the nodes of a graph to a KML as Placemarks."""
    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color = 'ff00ff00' if node == start_node else 'ff0000ff' if node in monument_nodes else 'ffff0000'
        point = kml.newpoint(name=str(node), coords=[(pos[0], pos[1])])
        point.style.iconstyle.color = color
        point.style.iconstyle.scale = 1


def add_edges_to_kml(graph: Graph, kml: simplekml.Kml) -> None:
    """Add the edges of a graph to a KML as LineStrings."""
    for u, v in graph.edges():
        pos_u, pos_v = graph.nodes[u]['pos'], graph.nodes[v]['pos']
        line = kml.newlinestring(name=f"{u}-{v}", coords=[(pos_u[0], pos_u[1]), (pos_v[0], pos_v[1])])
        line.style.linestyle.color = 'ff000000'  # Black
        line.style.linestyle.width = 2