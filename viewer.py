from graphmaker import * #type : ignore
from segments import *
from staticmap import StaticMap, CircleMarker, Line #type : ignore
import networkx as nx #type : ignore
from fastkml import *
from shapely.geometry import Point, LineString

def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""
    static_map = StaticMap(800, 600)
    
    for aresta in graph.edges():
        pos_ini_ent = graph.nodes[aresta[0]]["pos"][0]
        pos_ini_sort = graph.nodes[aresta[0]]["pos"][1]
        pos_fin_ent = graph.nodes[aresta[1]]["pos"][0]
        pos_fin_sort = graph.nodes[aresta[1]]["pos"][1]
        linia = Line([(pos_ini_ent, pos_ini_sort), (pos_fin_ent,pos_fin_sort)], "blue", 2)
        static_map.add_line(linia)

    for node in graph.nodes():
        pos = graph.nodes[node]["pos"]
        vertex = CircleMarker(pos,"red",6)
        static_map.add_marker(vertex)
    imatge = static_map.render()
    imatge.save(filename)

def export_KML(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a KML file."""
    k = KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    doc = Document(ns, 'docid', 'Graph', 'Graph KML')
    k.append(doc)

    for node in graph.nodes():
        pos_1 = graph.nodes[node]['pos'][0]
        pos_2 = graph.nodes[node]['pos'][1]
        #print(pos_1,pos_2)
        punt = Point(float(pos_1),float(pos_2)) 
        marca = Placemark(ns, str(node), str(node))
        marca.geometry = punt
        doc.append(marca)

    for aresta in graph.edges():
        start_pos = graph.nodes[aresta[0]]['pos']
        end_pos = graph.nodes[aresta[1]]['pos']
        linia = LineString([start_pos, end_pos])
        marca = Placemark(ns, f'edge_{aresta[0]}_{aresta[1]}', f'edge from {aresta[0]} to {aresta[1]}')
        marca.geometry = linia
        doc.append(marca)

        with open(filename, 'w') as fitxer:
            fitxer.write(k.to_string())

segments = load_segments('filename.txt')
graph = make_graph(segments, 100)
export_PNG(graph, 'graph.png')
export_KML(graph, 'graph.kml')