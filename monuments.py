from dataclasses import dataclass
from typing import TypeAlias
from bs4 import BeautifulSoup
import requests
from segments import Point
import re


@dataclass
class Monument:
    name: str
    location: Point


Monuments: TypeAlias = list[Monument]


def download_monuments(filename: str) -> None:
    """Download monuments from Catalunya Medieval and it saves them to a file"""
    sexy = open(filename, "w")
    url = "https://www.catalunyamedieval.es/comarques/"
    response = requests.get(url, timeout=20)
    soup = BeautifulSoup(response.content, "html.parser")
    script_tags = soup.find_all("script")

    script_target = None
    for script_tag in script_tags:
        if "var aCasaForta" in script_tag.text:
            script_target = script_tag
            break

    if script_target:
        script_content = script_target.text
        title_pattern = r'"title":"(.*?)"'
        position_pattern = r'"position":{"lat":"(.*?)","long":"(.*?)"}'
                    
        titles = re.findall(title_pattern, script_content)            
        locations = re.findall(position_pattern, script_content)

        i = 0
        for location in locations:
            title = bytes(titles[i], "utf-8").decode("unicode_escape")
            sexy.write(f"{title},{float(location[0])},{float(location[1])}\n")
            i += 1
    
    sexy.close()

'''def load_monuments(filename: str) -> Monuments:
    """Load monuments from a file."""
    monuments: Monuments = []
    file = open(filename, "r")
    for line in file:
        monument_name, lat, lon = line.strip().split(",")
        monuments.append(Monument(monument_name, Point(float(lat), float(lon))))  # type: ignore
    return monuments
'''
def load_monuments(filename: str) -> list[Monument]:
    """Load monuments from a file."""
    monuments = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    print(f"Skipping malformed line: {line}")
                    continue
                monument_name, lat, lon = parts
                monuments.append(Monument(name=monument_name, location=Point(float(lat), float(lon))))
            except ValueError as e:
                print(f"Error processing line '{line}': {e}")
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
    return monuments


# COMPROVACIÓ

#download_monuments("filenamee.txt")