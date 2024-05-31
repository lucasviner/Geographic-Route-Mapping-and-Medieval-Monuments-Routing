from dataclasses import dataclass
from typing import TypeAlias
from bs4 import BeautifulSoup
from segments import Point, Box
from re import findall
import requests, os, time


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
    attempts = 0 
    delay, retries = 5, 10
    while attempts < retries:
        try:
            response = requests.get(url, timeout=20)
            return response.content
        except requests.RequestException as e: 
            attempts += 1
            print(f"Attempt {attempts} failed with error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise requests.RequestException(f"Failed to fetch page content from {url} after {retries} attempts.")


def extract_script_tag(content: bytes, keyword: str) -> str:
    """Extract the script tag containing the specified keyword."""
    soup = BeautifulSoup(content, "html.parser")
    script_tags = soup.find_all("script")
    
    for script_tag in script_tags:
        if keyword in script_tag.text:
            return script_tag.text
    return ""


def parse_monument_data(script_content: str) -> Monuments:
    """ Parse monument data from the script content. """
    title_pattern = r'"title":"(.*?)"'
    position_pattern = r'"position":{"lat":"(.*?)","long":"(.*?)"}'
    
    titles = findall(title_pattern, script_content)
    locations = findall(position_pattern, script_content)
    
    monuments: Monuments = []
    for i, location in enumerate(locations):
        title = decode_title(titles[i])
        lat, lon = map(float, location)
        monuments.append(Monument(title, Point(lat, lon)))
    
    return monuments


def decode_title(title: str) -> str:
    """Decode the title from unicode escape sequences."""
    return bytes(title, "utf-8").decode("unicode_escape")


def save_monuments_to_file(monuments: Monuments, filename: str) -> None:
    """Save a list of monuments to a file."""
    with open(filename, 'w') as f:
        for monument in monuments:
            f.write(f"{monument.name} - {monument.location.lat},{monument.location.lon}\n")


def load_monuments(box: Box, filename: str) -> Monuments:
    """Load monuments from a file and filter by location within the given box."""
    monuments: Monuments = []
    with open(filename, "r") as file:    
        for line in file:
            try:
                monument_name, lat, lon = get_data_from_file(line)                
                if monument_in_box(box, lat, lon): 
                    monuments.append(Monument(monument_name, Point(lat, lon)))
            except ValueError as e:
                print(f"Error processing line: {line.strip()} - {e}. This line will be ignored.")
    return monuments


def get_data_from_file(line: str) -> tuple[str, float, float]:
    """Extract the monument name and coordinates from a line in the file."""
    name_and_coords = line.strip().split(" - ")
    monument_name = name_and_coords[0]
    lat, lon = map(float, name_and_coords[1].split(","))
    return monument_name, lat, lon
                 

def monument_in_box(box: Box, lat: float, lon: float) -> bool:
    """Check if the monument is inside the specified box."""
    return box.bottom_left.lat <= lat <= box.top_right.lat and box.bottom_left.lon <= lon <= box.top_right.lon


def get_monuments(box: Box, filename: str) -> Monuments:
    """
    Get all monuments in the box. If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    if not os.path.exists(filename):
        download_monuments(filename)
    return load_monuments(box,filename)