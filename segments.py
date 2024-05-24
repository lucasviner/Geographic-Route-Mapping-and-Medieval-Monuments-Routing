from typing import TypeAlias
from dataclasses import dataclass
from staticmap import StaticMap, Line
from datetime import datetime
import requests, gpxpy, haversine, os, gpxpy.gpx


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
    bbox = f"{box.bottom_left.lon},{box.bottom_left.lat},{box.top_right.lon},{box.top_right.lat}"
    with open(filename, "w") as f:
        while True:
            url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={bbox}&page={page}"
            gpx_content = fetch_gpx_content(url)
            gpx = gpxpy.parse(gpx_content)

            # Break the loop if there are no more tracks to process                            
            if len(gpx.tracks) == 0:
                break

            for track in gpx.tracks:
                for segment in track.segments:
                    if all(point.time is not None for point in segment.points):
                        segment.points.sort(key=lambda p: p.time)  # type: ignore
                        for i in range(len(segment.points) - 1):
                            p1, p2 = segment.points[i], segment.points[i + 1]
                            if is_valid_data(p1, p2):
                                f.write(f"{p1.latitude},{p1.longitude},{p2.latitude},{p2.longitude}\n")
            page += 1


def fetch_gpx_content(url: str) -> str:        
    """Fetch GPX content from the given URL."""   
    response = requests.get(url)
    return response.content.decode("utf-8")


def is_valid_data(p1: gpxpy.gpx.GPXTrackPoint, p2: gpxpy.gpx.GPXTrackPoint) -> bool:
    """Check if the data between two points is valid according to the specified criteria."""
    limit_year = 2015
    t_point1 = datetime.strptime(str(p1.time), "%Y-%m-%d %H:%M:%S%z")
    t_point2 = datetime.strptime(str(p2.time), "%Y-%m-%d %H:%M:%S%z")

    if t_point1.year < limit_year or t_point2.year < limit_year:
        return False

    distance = haversine.haversine((p1.latitude, p1.longitude), (p2.latitude, p2.longitude))
    return distance <= 0.1


def load_segments(filename: str) -> Segments:
    """Load segments from the file."""
    segments: Segments = []
    with open(filename, "r") as file:
        for line in file:
            try:
                segment = get_data_from_file(line)
                segments.append(segment)
            except ValueError as e:
                print(f"Error processing line: {line.strip()} - {e}. This line will be ignored.")
    return segments


def get_data_from_file(line:str) -> Segment:
    """ Convert a line of text into a Segment object. """
    bottom_left_lon, bottom_left_lat, top_right_lon, top_right_lat = map(float, line.strip().split(","))
    start_point = Point(bottom_left_lat, bottom_left_lon)
    end_point = Point(top_right_lat, top_right_lon)
    return Segment(start_point, end_point)


def get_segments(box: Box, filename: str) -> Segments:
    """
    Get all segments in the box. If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """
    if not os.path.exists(filename):
        download_segments(box, filename)
    return load_segments(filename)


def show_segments(segments: Segments, filename: str) -> None:
    """Show all segments in a PNG file using staticmaps."""
    static_map = StaticMap(800, 600)

    for segment in segments:
        start_point, end_point = segment.start, segment.end
        line = Line(((start_point.lon, start_point.lat), (end_point.lon, end_point.lat)),"blue", 2)
        static_map.add_line(line)

    image = static_map.render()
    image.save(filename)


# COMPROVAR QUE FUNCIONEN

# print(load_segments("filename.txt"))
# print(get_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "segments.dat"))
# show_segments(get_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "segments.dat"),"foto.png")
#download_segments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "segments.dat")
#download_segments(Box(Point(40.5363713, 0.8139316671), Point(40.79886535, 0.90211422)), "segments.dat")