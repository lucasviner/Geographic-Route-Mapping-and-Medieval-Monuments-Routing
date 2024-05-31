from graphmaker import Graph
from staticmap import StaticMap, CircleMarker, Line 
from fastkml import KML, Document, Placemark
from shapely.geometry import Point, LineString


def export_png(graph: Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""
    static_map = StaticMap(800, 600)
    add_edges_to_static_map(graph, static_map)
    add_nodes_to_static_map(graph, static_map)
    image = static_map.render()
    image.save(filename)


def add_edges_to_static_map(graph: Graph, static_map: StaticMap) -> None:
    """Add the edges of a graph to a StaticMap as Lines."""
    width = 2
    for edge in graph.edges():
        start_lat, start_lon = graph.nodes[edge[0]]["pos"]
        end_lat, end_lon = graph.nodes[edge[1]]["pos"]
        line = Line([(start_lat, start_lon), (end_lat, end_lon)], "black", width)
        static_map.add_line(line)


def add_nodes_to_static_map(graph: Graph, static_map: StaticMap) -> None:
    """Add the nodes of a graph to a StaticMap as CircleMarkers."""
    width = 7
    for node in graph.nodes():
        pos = graph.nodes[node]["pos"]
        marker = CircleMarker(pos, "blue", width)
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
        lat, lon = graph.nodes[node]['pos']
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
        