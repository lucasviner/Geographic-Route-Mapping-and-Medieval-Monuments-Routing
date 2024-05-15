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


def download_monuments(filename: str) -> Monuments:
    """Download monuments from Catalunya Medieval and it saves them to a file"""
    monuments: Monuments = []
    url = "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/ermites/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    ermites = soup.find_all("li", class_="ermita")
    f = open(filename, "w")
    for ermita in ermites:
        link = ermita.find("a")
        monument_name = link.text.strip()
        monument_url = link.get("href")
        monument_response = requests.get(monument_url)
        monument_soup = BeautifulSoup(monument_response.content, "html.parser")
        location_element = monument_soup.find(lambda tag: tag.name == "p" and "Localització:" in tag.text)
        if location_element:
            lat, lon = extreure_coordenades(location_element.text.strip())
            if lat != -1 and lon != -1:
                f.write(f"{monument_name},{float(lat)},{float(lon)}\n")
                monuments.append(Monument(monument_name, Point(float(lat), float(lon))))
    f.close()
    return monuments


def extreure_coordenades(dades: str) -> tuple[float, float]:
    """
    Retorna una tupla de dos strings que conté la longitud i la latitud d'un seguit de dades. Nomes la tindrem en compte si segueix el
    format general de la majoria de dades --> "Longitud: N <lat> <min> <seg> E <lon> <min> <seg>."
    En qualsevol cas alternatiu no es tindrà en compte el monument i la tupla serà de -1's.
    """
    lat, lon = -1.0, -1.0
    parts = dades.split()
    try:
        if (len(parts) <= 13 and parts[0] == "Localització:" and parts[1] == "N" and parts[5] == "E"):
            lat, lon = parse_coordinates(dades)
        return lat, lon
    except:
        return lat, lon


def parse_coordinates(coords_str: str) -> tuple[float, float]:
    """
    Parsea una cadena de coordenadas en formato DMS (grados, minutos, segundos) y devuelve un punto con coordenadas en grados decimales.
    """
    parts = coords_str.split()
    lat_deg = float(parts[2])
    lat_min = float(parts[3])
    lat_sec = float(parts[4])
    lon_deg = float(parts[6])
    lon_min = float(parts[7])
    lon_sec = float(parts[8])
    lat = dms_to_decimal(lat_deg, lat_min, lat_sec, parts[1])
    lon = dms_to_decimal(lon_deg, lon_min, lon_sec, parts[5])
    return lat, lon


def dms_to_decimal(degrees: float, minutes: float, seconds: float, direction: str) -> float:
    """
    Convierte coordenadas en grados, minutos y segundos a grados decimales.
    """
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees


def load_monuments(filename: str) -> Monuments:
    """Load monuments from a file."""
    monuments: Monuments = []
    file = open(filename, "r")
    for line in file:
        monument_name, lat, lon = line.strip().split(",")
        monuments.append(Monument(monument_name, Point(float(lat), float(lon))))  # type: ignore
    return monuments


def get_monuments(filename: str) -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    try:
        monuments = load_monuments(filename)
    except FileNotFoundError:
        monuments = download_monuments(filename)
        save_monuments(monuments, filename)
    return monuments


def save_monuments(monuments: Monuments, filename: str) -> None:
    """Saves the monument to a file."""
    f = open(filename, "w")
    for monument in monuments:
        name = monument.name
        lat = monument.location.lat
        lon = monument.location.lon
        f.write(f"{name},{float(lat)},{float(lon)}\n")
    f.close()


# COMPROVACIÓ

print(download_monuments("filenamee.txt"))
