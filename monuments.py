from dataclasses import dataclass
from typing import TypeAlias
from bs4 import BeautifulSoup
import requests, os
from segments import Point, Box
from re import findall


@dataclass
class Monument:
    name: str
    location: Point


Monuments: TypeAlias = list[Monument]


def download_monuments(filename: str) -> None:
    """ Download monuments from Catalunya Medieval and it saves them to a file. """
    url = "https://www.catalunyamedieval.es/comarques/"
    content = fetch_page_content(url)
    script_content = extract_script_tag(content, "var aCasaForta")    
    if script_content:
        save_monuments_to_file(parse_monument_data(script_content), filename)


def fetch_page_content(url: str) -> bytes:
    """ Fetch the content of a web page. """
    response = requests.get(url, timeout=20)
    return response.content


def extract_script_tag(content: bytes, keyword: str) -> str:
    """Extract the script tag containing the specified keyword."""
    soup = BeautifulSoup(content, "html.parser")
    script_tags = soup.find_all("script")
    
    for script_tag in script_tags:
        if keyword in script_tag.text:
            return script_tag.text
    return ""


def parse_monument_data(script_content: str) -> list[Monument]:
    """ Parse monument data from the script content. """
    title_pattern = r'"title":"(.*?)"'
    position_pattern = r'"position":{"lat":"(.*?)","long":"(.*?)"}'
    
    titles = findall(title_pattern, script_content)
    locations = findall(position_pattern, script_content)
    
    monuments = []
    for i, location in enumerate(locations):
        title = bytes(titles[i], "utf-8").decode("unicode_escape")
        lat, lon = map(float, location)
        monuments.append(Monument(title, Point(lat, lon)))
    
    return monuments


def save_monuments_to_file(monuments: list[Monument], filename: str) -> None:
    """Save a list of monuments to a file."""
    with open(filename, 'w') as f:
        for monument in monuments:
            f.write(f"{monument.name} - {monument.location.lat},{monument.location.lon}\n")


def load_monuments(box: Box, filename: str) -> Monuments:
    """Load monuments from a file."""
    monuments: Monuments = []
    with open(filename, "r") as file:    
        for line in file:
            try:
                monument_name, lat, lon = get_data_from_file(line)                
                if monument_in_box(box, lat, lon): 
                    monuments.append(Monument(monument_name, Point(lat, lon)))
            except Exception as e:
                print(f"Error processing line: {line.strip()} - {e}. This line will be ignored.")
    return monuments


def get_data_from_file(line: str) -> tuple[str, float, float]:
    """ Gets the monument name and the coordenates from the file """
    name_and_coords = line.strip().split(" - ")
    monument_name = name_and_coords[0]
    lat, lon = name_and_coords[1].split(",")
    return monument_name, float(lat), float(lon)
                 

def monument_in_box(box: Box, lat: float, lon: float) -> bool:
    """ Returns if the monument is inside the interested box. """
    return box.bottom_left.lat <= lat <= box.top_right.lat and box.bottom_left.lon <= lon <= box.top_right.lon

def get_monuments(box: Box, filename: str) -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    if not os.path.exists(filename):
        download_monuments(filename)
    return load_monuments(box,filename)
    


# COMPROVACIÓ

#download_monuments("monuments.dat")
#print(get_monuments(Box(Point(40.5363713, 0.5739316671), Point(40.79886535, 0.9021482)), "monuments.dat"))