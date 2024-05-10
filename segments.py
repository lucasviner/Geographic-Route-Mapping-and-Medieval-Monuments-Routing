from typing import TypeAlias
from dataclasses import dataclass
import requests, gpxpy
from staticmap import StaticMap, Line


@dataclass
class Point:
    lat: float
    lon: float

@dataclass
class Segment:
    start: Point
    end: Point

@dataclass
class Box:
    bottom_left: Point
    top_right: Point

Segments: TypeAlias = list[Segment]

def download_segments(box: Box, filename: str) -> None:
    """Download all segments in the box and save them to the file."""
    page = 0
    f = open(filename, 'w')
    while True:
        url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={box.bottom_left.lon,box.bottom_left.lat,box.top_right.lon,box.top_right.lat}&page={page}"
        response = requests.get(url)            
        gpx_content = response.content.decode("utf-8")
        gpx = gpxpy.parse(gpx_content)
        if len(gpx.tracks) == 0:
            break
        for track in gpx.tracks:
            for segment in track.segments:
                if all(point.time is not None for point in segment.points):
                    segment.points.sort(key=lambda p: p.time)  # type: ignore
                    p1, p2 = segment.points[0], segment.points[-1]
                    # Si volguèssim, també podriem accedir al temps de cada punt
                    f.write(f"{p1.latitude},{p1.longitude},{p2.latitude},{p2.longitude}\n")
        page += 1
    f.close()

def load_segments(filename: str) -> Segments:
    """ Load segments from the file. """
    segments: Segments = []
    file = open(filename, 'r')
    for line in file:
        start_lat, start_lon, end_lat, end_lon = map(float, line.strip().split(','))
        start_point = Point(start_lat, start_lon)
        end_point = Point(end_lat, end_lon)
        segment = Segment(start_point, end_point)
        segments.append(segment)
    return segments

def get_segments(box: Box, filename: str) -> Segments:
    """
    Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """
    try:
        segments = load_segments(filename)
    except FileNotFoundError:
        download_segments(box, filename)
        segments = load_segments(filename)
    return segments

def show_segments(segments: Segments, filename: str) -> None:
    """Show all segments in a PNG file using staticmaps."""
    static_map = StaticMap(800, 600)  # Tamaño del mapa

    # Agregar líneas para cada segmento
    for segment in segments:
        start_point = segment.start
        end_point = segment.end
        line = Line(((start_point.lon, start_point.lat), (end_point.lon, end_point.lat)), 'blue', 2)
        static_map.add_line(line)

    image = static_map.render()
    image.save(filename)



#COMPROVAR QUE FUNCIONEN

#print(load_segments("filename.txt"))
#show_segments(get_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "filename.txt"),"foto.png")
#download_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "filename.txt")