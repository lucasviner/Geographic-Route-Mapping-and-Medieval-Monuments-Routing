from dataclasses import dataclass
from typing import *
from bs4 import BeautifulSoup
import requests
from segments import Point


@dataclass
class Monument:
     name: str
     location: Point

Monuments: TypeAlias = list[Monument]

def download_monuments(filename: str) -> Monuments:
    """ Download monuments from Catalunya Medieval and it saves them to a file """
    monuments: Monuments = []
    url = "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/ermites/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    ermites = soup.find_all("li", class_="ermita")
    f = open(filename, 'w')
    for ermita in ermites:
        link = ermita.find("a")
        monument_name = link.text.strip() 
        monument_url = link.get("href")
        monument_response = requests.get(monument_url)
        monument_soup = BeautifulSoup(monument_response.content, "html.parser")
        location_element = monument_soup.find(lambda tag: tag.name == "p" and "Localització:" in tag.text)
        if location_element:
            lat, lon = extreure_coordenades(location_element.text.strip()) #type: ignore
            if lat != None and lon != None:
                f.write(f"{monument_name},{float(lat)},{float(lon)}\n")
                monuments.append(Monument(monument_name, Point(float(lat), float(lon)))) #type: ignore
    f.close()
    return monuments


def extreure_coordenades(dades: str) -> Optional[tuple[str, str]]:
    """ 
    Retorna una tupla de dos strings que conté la longitud i la latitud d'un seguit de dades. Nomes la tindrem en compte si segueix el 
    format general de la majoria de dades --> "Longitud: N <lat> <min> <seg> E <lon> <min> <seg>."
    En qualsevol cas alternatiu no es tindrà en compte el monument i la tupla serà de None's. 
    """

    lat, lon = None, None
    parts = dades.split()
    try:
        if len(parts) <= 13 and parts[0] == "Localització:" and parts[1] == "N" and parts[5] == "E":
            lat = parts[2]
            lon = parts[6]
    except: 
        return lat, lon
    return lat, lon


def load_monuments(filename: str) -> Monuments:
    """ Load monuments from a file."""
    monuments: Monuments = []
    file = open(filename, 'r')
    for line in file:
        monument_name, lat, lon = line.strip().split(',')
        monuments.append(Monument(monument_name, Point(float(lat), float(lon)))) #type: ignore
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
        monuments = download_monuments(filename) #type: ignore
        save_monuments(monuments, filename)
    return monuments

def save_monuments(monuments: Monuments, filename: str) -> None:
    """ Saves the monument to a file. """
    f = open(filename, 'w')
    for monument in monuments:
        name = monument.name
        lat = monument.location.lat #type: ignore
        lon = monument.location.lon #type: ignore
        f.write(f"{name},{float(lat)},{float(lon)}\n")
    f.close()
    

#COMPROVACIÓ

print(get_monuments('filename.txt'))