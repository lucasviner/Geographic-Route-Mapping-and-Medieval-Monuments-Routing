from graphmaker import make_graph
from segments import load_segments
from staticmap import StaticMap, CircleMarker, Line 
import networkx as nx 
from fastkml import KML, Document, Placemark
from shapely.geometry import Point, LineString

def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""
    static_map = StaticMap(800, 600)
    #AIXO HAURIA DE ANAR EN UNA FUNCIÓ
    arestes_PNG(graph, static_map)
    nodes_PNG(graph, static_map)
    imatge = static_map.render()
    imatge.save(filename)

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
        vertex = CircleMarker(pos, "red", 6)
        static_map.add_marker(vertex)

def export_KML(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a KML file."""
    kml = KML()
    namespace = '{http://www.opengis.net/kml/2.2}'
    document = Document(namespace, 'docid', 'Graph', 'Graph KML')
    kml.append(document)
    nodes_KML(graph, document, namespace)
    arestes_KML(graph, document, namespace)
    obrir_fitxer(filename, kml)

def nodes_KML(graph: nx.Graph, document: Document, namespace: str)->None:
    """Add the nodes of a graph to a KML as Placemarks"""
    for node in graph.nodes():
            lat = graph.nodes[node]['pos'][0]
            lon = graph.nodes[node]['pos'][1]
            point = Point(float(lat),float(lon)) 
            placemark = Placemark(namespace, str(node), str(node))
            placemark.geometry = point
            document.append(placemark)

def arestes_KML(graph: nx.Graph, document: Document, namespace: str)->None:
    """Adds the edges of a graph to a KML as Placemarks"""
    for aresta in graph.edges():
        start_pos = graph.nodes[aresta[0]]['pos']
        end_pos = graph.nodes[aresta[1]]['pos']
        line = LineString([start_pos, end_pos])
        placemark = Placemark(namespace, f'edge_{aresta[0]}_{aresta[1]}', f'edge from {aresta[0]} to {aresta[1]}')
        placemark.geometry = line
        document.append(placemark)

def obrir_fitxer(filename: str, kml: KML)->None:
    """Saves the content of a KML object in a file"""
    with open(filename, 'w') as fitxer:
            fitxer.write(kml.to_string())

# COMPROVACIÓ
segments = load_segments('filename.txt')
graph = make_graph(segments, 100)
export_PNG(graph, 'graph.png')
export_KML(graph, 'graph.kml')