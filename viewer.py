from graphmaker import make_graph, Graph
from segments import load_segments
from staticmap import StaticMap, CircleMarker, Line 
from fastkml import KML, Document, Placemark
from shapely.geometry import Point, LineString
import networkx as nx


def export_png(graph: Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""
    static_map = StaticMap(800, 600)
    add_edges_to_static_map(graph, static_map)
    add_nodes_to_static_map(graph, static_map)
    image = static_map.render()
    image.save(filename)


def add_edges_to_static_map(graph: Graph, static_map: StaticMap) -> None:
    """Add the edges of a graph to a StaticMap as Lines."""
    for edge in graph.edges():
        start_lat = graph.nodes[edge[0]]["pos"][0]
        start_lon = graph.nodes[edge[0]]["pos"][1]
        end_lat = graph.nodes[edge[1]]["pos"][0]
        end_lon = graph.nodes[edge[1]]["pos"][1]
        line = Line([(start_lat, start_lon), (end_lat, end_lon)], "black", 2)
        static_map.add_line(line)


def add_nodes_to_static_map(graph: Graph, static_map: StaticMap) -> None:
    """Add the nodes of a graph to a StaticMap as CircleMarkers."""
    for node in graph.nodes():
        pos = graph.nodes[node]["pos"]
        marker = CircleMarker(pos, "blue", 7)
        static_map.add_marker(marker)


def export_kml(graph: Graph, filename: str) -> None:
    """Export the graph to a KML file."""
    kml = KML()
    namespace = '{http://www.opengis.net/kml/2.2}'
    document = Document(namespace, 'docid', 'Graph', 'Graph KML')
    kml.append(document)
    add_nodes_to_kml(graph, document, namespace)
    add_edges_to_kml(graph, document, namespace)
    save_kml_to_file(filename, kml)


def add_nodes_to_kml(graph: Graph, document: Document, namespace: str) -> None:
    """Add the nodes of a graph to a KML as Placemarks."""
    for node in graph.nodes():
        lat = graph.nodes[node]['pos'][0]
        lon = graph.nodes[node]['pos'][1]
        point = Point(float(lat), float(lon))
        placemark = Placemark(namespace, str(node), str(node))
        placemark.geometry = point
        document.append(placemark)


def add_edges_to_kml(graph: Graph, document: Document, namespace: str) -> None:
    """Add the edges of a graph to a KML as Placemarks."""
    for edge in graph.edges():
        start_pos = graph.nodes[edge[0]]['pos']
        end_pos = graph.nodes[edge[1]]['pos']
        line = LineString([start_pos, end_pos])
        placemark = Placemark(namespace, f'edge_{edge[0]}_{edge[1]}', f'edge from {edge[0]} to {edge[1]}')
        placemark.geometry = line
        document.append(placemark)


def save_kml_to_file(filename: str, kml: KML) -> None:
    """Save the content of a KML object to a file."""
    with open(filename, 'w') as file:
        file.write(kml.to_string())




"""segments = load_segments('segments.dat')
graph = make_graph(segments, 100)
export_png(graph, 'graph.png')
export_kml(graph, 'graph.kml')
"""
