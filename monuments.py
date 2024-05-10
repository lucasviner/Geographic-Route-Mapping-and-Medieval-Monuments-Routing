from dataclasses import dataclass
from typing import TypeAlias
from bs4 import BeautifulSoup
import requests
from segments import Point


@dataclass
class Monument:
     name: str
     location: Point

Monuments: TypeAlias = list[Monument]

def download_monuments() -> Monuments:
    """ Download monuments from Catalunya Medieval. """
    monuments: Monuments = []
    url = "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/ermites/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    ermites = soup.find_all("li", class_="ermita")
    for ermita in ermites:
        link = ermita.find("a")
        monument_name = link.text.strip() 
        monument_url = link.get("href")
        monument_response = requests.get(monument_url)
        monument_soup = BeautifulSoup(monument_response.content, "html.parser")
        location_element = monument_soup.find(lambda tag: tag.name == "p" and "Localització:" in tag.text)
        if location_element:
            lat, lon = extreure_coordenades(location_element.text.strip()) #TENIM EL PROBLEMA QUE EL FORMAT NO SEMPRE ES EL MATEIX
            monuments.append(Monument(monument_name, Point(float(lat), float(lon))))
    return monuments


def extreure_coordenades(dades: str) -> tuple[str, str]:
    txt = dades.split()
    lat = txt[2] + txt[3] + txt[4]
    lon = txt[6] + txt[7] + txt[8]
    return lat, lon
    
def load_monuments(filename: str) -> Monuments:
    """ Load monuments from a file."""
    monuments: Monuments = []
    file = open(filename, 'r')
    for line in file:
        start_lat, start_lon, end_lat, end_lon = map(float, line.strip().split(','))
        start_point = Point(start_lat, start_lon)
        end_point = Point(end_lat, end_lon)
        segment = Segment(start_point, end_point)
        monuments.append(segment)
    return monuments

def get_monuments(filename: str) -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    try:
        # Try to load monuments from the file
        monuments = load_monuments(filename)
    except FileNotFoundError:
        # If file doesn't exist, download monuments
        monuments = download_monuments()
        # Save the downloaded monuments to the file
        save_monuments(monuments, filename)
    return monuments
    
'''
print(download_monuments())


