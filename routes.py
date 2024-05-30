import networkx as nx
from segments import Point, get_segments, Box
from graphmaker import Graph, make_graph
from monuments import Monuments, load_monuments
from typing import TypeAlias, Optional
from staticmap import StaticMap, CircleMarker, Line
from math import *
import simplekml


Routes: TypeAlias = dict[str, list[int]]


def find_routes(graph: Graph, start_point: Point, monuments: Monuments, filename: str) -> None:
    """Generate routes and save visualizations."""
    start_node = find_closest_node(graph, start_point)
    shortest_paths = nx.single_source_dijkstra(graph, source=start_node, weight='weight')
    monuments_nodes = get_monuments_nodes(graph, monuments)
    
    if contains_node(monuments_nodes, shortest_paths):
        route_graph = build_route_graph(graph, monuments_nodes, shortest_paths)
        save_static_map(route_graph, start_node, monuments_nodes, f'{filename}.png')
        save_kml(route_graph, start_node, monuments_nodes,  f'{filename}.kml')
    else:
        print('No monuments found in the selected box.')


def find_closest_node(graph: Graph, point: Point) -> int:
    """Find the closest node in the graph to a given point."""
    closest_node = None
    min_distance = float('inf')
    for node, data in graph.nodes(data=True):
        lat, lon = data['pos'][1], data['pos'][0]
        distance = haversine_distance(point, Point(lat, lon))
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    return closest_node


def haversine_distance(point1: Point, point2: Point) -> float:
    """Calculate the Haversine distance between two points."""
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1 = convert_to_radians(point1.lat, point1.lon)
    lat2, lon2 = convert_to_radians(point2.lat, point2.lon)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c # Distance in kilometers
    
    return distance


def convert_to_radians(lat: float, lon: float) -> tuple[float, float]:
    """Convert latitude and longitude from degrees to radians."""
    return radians(lat), radians(lon)


def get_monuments_nodes(G: Graph, monuments: Monuments) -> set[int]:
    """Get the set of nodes corresponding to the monuments."""
    monument_node_map = map_monuments_to_nodes(G, monuments)
    monument_nodes = set(monument_node_map.values())
    return monument_nodes


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
                    for i in range(len(path) - 1):
                        u, v = path[i], path[i + 1]
                        if get_node_position(u) != None and get_node_position(v) != None:
                            lat1, lon1 = get_node_position(G,u)[0], get_node_position(G,u)[1]
                            lat2, lon2 = get_node_position(G,v)[0], get_node_position(G,v)[1]
                            weight = haversine_distance(Point(lat1, lon1), Point(lat2, lon2))
                            route_graph.add_edge(u, v, weight=weight)
                            route_graph.add_node(u, pos=(lat1,lon1))
                            route_graph.add_node(v,pos=(lat2,lon2))
                        else: 
                            pass
    return route_graph


def save_static_map(G: Graph, start_node: int, monument_nodes: set[int], filename: str) -> None:
    """Generate and save a static map image."""
    map_imatge = StaticMap(800, 800)
    
    for node, data in G.nodes(data=True):
        pos = data['pos']
        color, size = ('green', 30) if node == start_node else ('red', 30) if node in monument_nodes else ('blue', 10)
        marker = CircleMarker((pos[0], pos[1]), color, size)
        map_imatge.add_marker(marker)

    
    for u, v in G.edges():
        pos_u, pos_v = G.nodes[u]['pos'], G.nodes[v]['pos']
        line = Line([(pos_u[0], pos_u[1]), (pos_v[0], pos_v[1])], 'black', 2)
        map_imatge.add_line(line)
    
    image = map_imatge.render()
    image.save(filename)


def save_kml(graph: Graph, start_node: int, monument_nodes: set[int], filename: str) -> None:
    """Generate and save a KML file for visualization in Google Earth."""
    kml = simplekml.Kml()
    
    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color = 'ff00ff00' if node == start_node else 'ff0000ff' if node in monument_nodes else 'ffff0000'
        point = kml.newpoint(name=str(node), coords=[(pos[0], pos[1])])
        point.style.iconstyle.color = color
        point.style.iconstyle.scale = 1

    for u, v in graph.edges():
        pos_u, pos_v = graph.nodes[u]['pos'], graph.nodes[v]['pos']
        line = kml.newlinestring(name=f"{u}-{v}", coords=[(pos_u[0], pos_u[1]), (pos_v[0], pos_v[1])])
        line.style.linestyle.color = 'ff000000'  # Black
        line.style.linestyle.width = 2
    
    kml.save(filename)

'''monuments = load_monuments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "monuments.dat")
segments = get_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "segments.dat")
G = make_graph(segments, 100)
start_point = Point(lat=40.55, lon=0.6739316671)

find_routes(G, start_point, monuments, 'routes')'''