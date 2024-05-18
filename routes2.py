from typing import TypeAlias
from dataclasses import dataclass
import networkx as nx
from segments import Point, load_segments
from monuments import Monument, load_monuments
from staticmap import StaticMap, Line
import simplekml
from graphmaker import *
@dataclass
class Routes:
    path: list[Point]

paths: TypeAlias = list[list[Point]]

def find_closest_node(graph: nx.Graph, point: Point) -> int:
    """Find the closest node in the graph to the given point."""
    closest_node = None
    min_distance = float('inf')
    
    for node, data in graph.nodes(data=True):
        node_pos = data['pos']
        distance = ((node_pos[0] - point.lat) ** 2 + (node_pos[1] - point.lon) ** 2) ** 0.5  # Euclidean distance
        if distance < min_distance:
            min_distance = distance
            closest_node = node
    
    return closest_node
def find_routes(graph: nx.Graph, start: Point, endpoints: list[Monument]) -> Routes:
    """Find the shortest route between the starting point and all the endpoints."""
    routes = []
    start_node = find_closest_node(graph, start)

    for endpoint in endpoints:
        try:
            end_node = find_closest_node(graph, endpoint.location)
            route_node_ids = nx.shortest_path(graph, source=start_node, target=end_node)
            route_points = [Point(*graph.nodes[node]['pos']) for node in route_node_ids]
            routes.append(route_points)
        except nx.NetworkXNoPath:
            print(f"No path found from {start} to {endpoint.location}.")
        except nx.NodeNotFound as e:
            print(f"Node not found error: {e}")
    
    return Routes(path=routes)

def export_PNG(routes: Routes, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    static_map = StaticMap(800, 600)

    if not routes.path:
        print("No routes to export to PNG.")
        return
    
    for path in routes.path:
        for i in range(len(path) - 1):
            start_point = path[i]
            end_point = path[i + 1]
            line = Line([(start_point.lon, start_point.lat), (end_point.lon, end_point.lat)], 'blue', 2)
            static_map.add_line(line)

    image = static_map.render()
    image.save(filename)

def export_KML(routes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    kml = simplekml.Kml()
    if not routes.path:
        print("No routes to export to KML.")
        return
    
    for path in routes.path:
        coords = [(point.lon, point.lat) for point in path]
        line = kml.newlinestring(name="Route", coords=coords)
        line.style.linestyle.color = simplekml.Color.blue
        line.style.linestyle.width = 4

    kml.save(filename)

# Verificación de segmentos
segments = load_segments('filename.txt')
#print("Loaded segments:", segments)

# Crear el grafo
G = make_graph(segments, 90)
#print("Graph nodes:", G.nodes)

# Definir el punto de inicio y cargar monumentos
start = Point(41.7215, 1.8296944444444445)
monuments = load_monuments('filenamee.txt')
#print("Loaded monuments:", monuments)

# Encontrar rutas
routes = find_routes(G, start, monuments)

# Exportar las rutas a PNG y KML
export_PNG(routes, 'graf.png')
export_KML(routes, 'graf.kml')

print("Routes:", routes)
