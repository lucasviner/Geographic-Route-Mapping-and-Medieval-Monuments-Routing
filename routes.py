from typing import TypeAlias
from dataclasses import dataclass
import networkx as nx
from segments import Point, load_segments
from monuments import Monuments, load_monuments
from fastkml import *
from shapely.geometry import Point
from staticmap import *
from graphmaker import make_graph


@dataclass
class Routes:
    path: list[Point]

paths: TypeAlias = list[list[Point]]


def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> Routes:
    """ Find the shortest route between the starting point and all the endpoints. """
    routes = []
    for endpoint in endpoints:
        try:
            route = nx.shortest_path(graph, source=start, target=endpoint.location)
            routes.append(route)
        except nx.NetworkXNoPath:
            print(f"No path found from {start} to {endpoint.location}.")
    return Routes(path = routes)

def export_PNG(routes: Routes, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    static_map = StaticMap(800, 600)

    for path in routes.path:
        for i in range(len(path) - 1):
            start_point = path[i]
            end_point = path[i + 1]
            line = Line(((start_point.lon, start_point.lat), (end_point.lon, end_point.lat)), 'blue', 2)
            static_map.add_line(line)

    image = static_map.render()
    image.save(filename)

def export_KML(groutes: Routes, filename: str) -> None:
    """Export the graph to a KML file."""
    kml = KML()
    
    for path in routes.path:
        line = kml.newlinestring(name="Route", description="Shortest route", coords=[(point.lon, point.lat) for point in path])
        line.style.linestyle.width = 4
        line.style.linestyle.color = Color.blue
    
    kml.save(filename)

segments = load_segments('filename.txt')
G = make_graph(segments, 90)
routes = find_routes(G, Point(41.7215,1.8296944444444445), load_monuments('filenamee.txt'))
export_PNG(routes, 'graf.png')