from typing import TypeAlias
from dataclasses import dataclass
from sklearn.cluster import KMeans
from fastkml import KML, Document, Placemark
from shapely.geometry import Point, LineString
from staticmap import StaticMap, Line
import networkx as nx
import numpy as np
import haversine as hs
from segments import Point, load_segments
from monuments import Monuments, load_monuments
from graphmaker import make_graph



@dataclass
class Routes:
    path: list[Point]

paths: TypeAlias = list[list[Point]]


def find_routes(graph: nx.Graph, start: Point, endpoints: Monuments) -> list[Routes]:
    """ Find the shortest route between the starting point and all the endpoints. """
    routes = []
    start_node = find_closest_node(graph, start)

    for endpoint in endpoints:
        try:
            end_node = find_closest_node(graph, endpoint.location)
            route = nx.shortest_path(graph, source = start_node, target=end_node, weight='weight')
            route_points = [Point(lat=graph.nodes[node]['pos'][0], lon=graph.nodes[node]['pos'][1]) for node in route] 
            routes.append(Routes(path=route_points))
        except nx.NetworkXNoPath:
            print(f"No path found from {start} to {endpoint.location}.")

    return routes


def find_closest_node(graph: nx.Graph, point: Point) -> int:
    """Find the closest graph node to a given Point."""
    closest_node = min(
    graph.nodes, key=lambda node: hs.haversine((graph.nodes[node]['pos'][0], graph.nodes[node]['pos'][1]),(point.lat, point.lon)))
    return closest_node


def assign_monuments_to_clusters(monuments: Monuments, centroids: np.ndarray) -> dict:
    """ Assign each monument to the nearest cluster based on the centroids. """
    kmeans = KMeans(n_clusters=len(centroids))
    kmeans.cluster_centers_ = centroids
    monument_clusters = {}
    for monument in monuments:
        cluster_index = kmeans.predict([[monument.location.lat, monument.location.lon]])[0]
        monument_clusters[monument] = cluster_index
    return monument_clusters


def export_PNG(routes: list[Routes], filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    static_map = StaticMap(800, 600)
    has_lines = False

    for route in routes:
        for i in range(len(route.path) - 1):
            start_point = route.path[i]
            end_point = route.path[i + 1]
            line = Line(((start_point.lon, start_point.lat), (end_point.lon, end_point.lat)), 'blue', 2)
            static_map.add_line(line)
            has_lines = True
    
    if has_lines:
        image = static_map.render()
        image.save(filename)
    else:
        print("No routes to render in the map")


def export_KML(routes: list[Routes], filename: str) -> None:
    """Export the graph to a KML file."""
    kml = KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    doc = Document(ns, 'docid', 'Routes', 'Routes KML')
    kml.append(doc)

    for route in routes:
        if len(route.path) < 2:
            print(f"Skipping route with insufficient points: {route.path}")
            continue
        coords = [(point.lon, point.lat) for point in route.path]
        linestring = LineString(coords)
        placemark = Placemark(ns, 'route', 'Route', 'Shortest route', linestring)
        doc.append(placemark)
    
    with open(filename, 'w') as file:
        file.write(kml.to_string(prettyprint=True))

segments = load_segments('filename.txt')
G = make_graph(segments, 90)
start_point = Point(lat=40.416775, lon=-3.703790)
routes = find_routes(G, start_point, load_monuments('filenamee.txt'))
export_KML(routes, 'graf.KML')
