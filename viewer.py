from graphmaker import *
from staticmap import StaticMap, CircleMaker, Line
import networkx as nx

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

