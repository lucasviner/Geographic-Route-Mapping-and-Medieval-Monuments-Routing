import networkx as nx
from segments import Point, Box, get_segments
from monuments import Monuments, load_monuments, Monument
from typing import TypeAlias
from staticmap import StaticMap, CircleMarker, Line
import numpy as np
from graphmaker import create_graph
from math import *
import simplekml

monuments = load_monuments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "monuments.dat")
segments = get_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "segments.dat")
G = create_graph(segments, 100)
start_point = Point(lat=40.55, lon=0.6739316671)

Routes: TypeAlias = dict[str, list[int]]

def haversine_distance(point1: Point, point2: Point) -> float:

    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(point1.lat)
    lon1 = radians(point1.lon)
    lat2 = radians(point2.lat)
    lon2 = radians(point2.lon)

    # Calculate the change in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate the distance using the Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

def find_closest_node(G: nx.Graph, point: Point) -> int:
    closest_node = None
    min_distance = float('inf')
    for node, data in G.nodes(data=True):
        dist = haversine_distance(point, Point(data['pos'][1], data['pos'][0]))
        if dist < min_distance:
            min_distance = dist
            closest_node = node
    return closest_node

def monuments_nodes(graph: nx.Graph, monuments: Monuments) -> dict[str, int]:
    return {monument.name: find_closest_node(graph, monument.location) for monument in monuments}

def create_monuments_set(G: nx.Graph, monuments: Monuments)->set[int]:
    monument_node_map = monuments_nodes(G, monuments)
    monument_nodes = set(monument_node_map.values())
    return monument_nodes

def create_routes_graph(G: nx.Graph, start_point: Point, monuments: Monuments):
    start_node = find_closest_node(G, start_point)
    shortest_paths = nx.single_source_dijkstra(G, source=start_node, weight='weight')
    monuments_set = create_monuments_set(G, monuments)
    if check_node(monuments_set, shortest_paths):
        graph = add_edges_and_nodes(G, monuments_set, shortest_paths)
    create_static_map(graph, start_node, monuments_set, 'routes.png')
    create_kml(graph, start_node, monuments_set, 'routes.kml' )
def check_node(monument_nodes: set, shortest_paths)->bool:
    monument_node_found = False
    for monument_node in list(monument_nodes):
        for path in list(shortest_paths[1].values()):
            if monument_node in path:
                monument_node_found = True
                break

    return monument_node_found

def get_node_position(G: nx.Graph, node: int):
    """Obtiene la posición de un nodo en el grafo"""
    return G.nodes[node]['pos'] if node in G.nodes else None

def add_edges_and_nodes(G: nx.Graph, monument_nodes: set, shortest_paths)->nx.Graph:
    graph_routes = nx.Graph()
    for monument_node in list(monument_nodes):
            for path in list(shortest_paths[1].values()):
                if monument_node in path:
                    path = list(shortest_paths[1][monument_node])
                    for i in range(len(path) - 1):
                        u, v = path[i], path[i + 1]
                        lat1, lon1 = get_node_position(G,u)[0], get_node_position(G,u)[1]
                        lat2, lon2 = get_node_position(G,v)[0], get_node_position(G,v)[1]
                        weight = haversine_distance(Point(lat1, lon1),Point(lat2, lon2))
                        graph_routes.add_edge(u, v, weight=weight)
                        graph_routes.add_node(u, pos=(lat1,lon1))
                        graph_routes.add_node(v,pos=(lat2,lon2))
    return graph_routes

def create_static_map(G: nx.Graph, start_node: int, monument_nodes: set[int], filename: str):
    m = StaticMap(800, 800)
    
    for node, data in G.nodes(data=True):
        pos = data['pos']
        if node == start_node:
            color = 'green'
            marker = CircleMarker((pos[0], pos[1]), color, 30)
            m.add_marker(marker)
        elif node in monument_nodes:
            color = 'red'
            marker = CircleMarker((pos[0], pos[1]), color, 30)
            m.add_marker(marker)
        else:
            color = 'blue'
            marker = CircleMarker((pos[0], pos[1]), color, 10)
            m.add_marker(marker)
        
    
    for u, v in G.edges():
        pos_u = G.nodes[u]['pos']
        pos_v = G.nodes[v]['pos']
        line = Line([(pos_u[0], pos_u[1]), (pos_v[0], pos_v[1])], 'black', 2)
        m.add_line(line)
    
    image = m.render()
    image.save(filename)

def create_kml(graph: nx.Graph, start_node: int, monument_nodes: set[int], filename: str):
    kml = simplekml.Kml()
    
    # Añadir nodos al KML
    for node, data in graph.nodes(data=True):
        pos = data['pos']
        if node == start_node:
            color = 'ff00ff00'  # Verde
        elif node in monument_nodes:
            color = 'ff0000ff'  # Rojo
        else:
            color = 'ffff0000'  # Azul
        
        pnt = kml.newpoint(name=str(node), coords=[(pos[0], pos[1])])  # KML usa (lon, lat)
        pnt.style.iconstyle.color = color
        pnt.style.iconstyle.scale = 1

    # Añadir aristas al KML
    for u, v in graph.edges():
        pos_u = graph.nodes[u]['pos']
        pos_v = graph.nodes[v]['pos']
        line = kml.newlinestring(name=f"{u}-{v}", coords=[(pos_u[0], pos_u[1]), (pos_v[0], pos_v[1])])
        line.style.linestyle.color = 'ff000000'  # Negro
        line.style.linestyle.width = 2
    
    kml.save(filename)
create_routes_graph(G, start_point, monuments)
