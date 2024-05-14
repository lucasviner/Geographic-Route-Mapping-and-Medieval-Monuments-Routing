from graphmaker import *
from segments import *
from staticmap import StaticMap, CircleMaker, Line
import networkx as nx
from fastkml import kml, geometry

def export_PNG(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmap."""
    static_map = StaticMap(800.600)
    for aresta in graph.edges():
        pos_ini = graph.nodes[aresta[0]]["pos"]
        pos_fin = graph.nodes[aresta[1]]["pos"]
        linia = Line([pos_ini,pos_fin],"blue",2)
        static_map.add_line(linia)
        #Pensar com posar-ho en una funció

    for node in graph.nodes():
        pos = graph.nodes[node]["pos"]
        vertex =  CircleMaker(pos,"red",6)
        static_map.add_maker(vertex)
    imatge = static_map.render()
    imatge.save(filename)

def export_KML(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a KML file."""
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    doc = kml.Document(ns, 'docid', 'Graph', 'Graph KML')
    k.append(doc)

    for node in graph.nodes():
        pos = graph.nodes[node]['pos']
        punt = geometry.Point(pos)
        marca = kml.Placemark(ns, str(node), str(node))
        marca.geometry = punt
        doc.append(marca)


    for aresta in graph.edges():
        start_pos = graph.nodes[aresta[0]]['pos']
        end_pos = graph.nodes[aresta[1]]['pos']
        linia = geometry.LineString([start_pos, end_pos])
        marca = kml.Placemark(ns, f'edge_{edge[0]}_{edge[1]}', f'Edge from {edge[0]} to {edge[1]}')
        marca.geometry = linia
        doc.append(marca)

        with open(filename, 'w') as fitxer:
            fitxer.write(k.to_string())

segments = load_segments('filename.txt')
graph = make_graph(segments, 5)
export_PNG(graph, 'graph.png')
export_KML(graph, 'graph.kml')