# Pràctica GCED-AP2 2024 · Rutes i monuments

FALTA: ROUTES I MONUMENTS QUE FAN BEN EXPLICAT, ARQUITECTURA DEL PROGRAMA, AFEGIR FOTOS A LA PART FINAL COM A EXEMPLES, EXPLICAR DECISIONS DE DISSENY QUE HAGUEM FET. 

## Geographic Route Mapping and Medieval Monuments Routing

### Project Description

This project allows users to process geographic data, obtain hiking routes within a specified region, infer a map (graph) based on these routes, and find optimal paths to medieval monuments. The results can be visualized in both 2D and 3D formats. Users can export the generated maps in .png and .kml formats and interactively find optimal routes to various points of interest.

### Table of Contents
1. [Getting Started](#getting-started)
2. [What each program does](#what-each-program-does)
3. [Program Architecture](#Program-Architecture)
4. [Prerequisites](#prerequisites)
5. [Installing](#installing)
6. [Running the Tests](#running-the-tests)
7. [Built With](#built-with)
8. [Example Workflow](#example-workflow)
9. [Authors](#authors)

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing. 

### What each program does

#### Main
The main program serves as the main entry point for the Medieval Routes Project. It guides the user through a series of steps to process geographic data, create a graph of hiking routes, and find optimal paths to medieval monuments. The results can be visualized and exported in both PNG and KML formats.
##### General Overview
- Introduction: The user is welcomed and given an overview of the project's capabilities.
- Input Region Coordinates: The user provides the geographical coordinates defining the region of interest.
- Download Segments: Hiking route segments for the specified region are downloaded and processed.
- Create Graph: A graph is created from the segments using clustering to identify key waypoints.
- Export Options: The user can choose to export the graph to PNG, KML, or both formats.
- Download Monuments Data: Data about medieval monuments in the region is fetched.
- Find Optimal Routes: The user can find and export the optimal routes from a specified starting point to the monuments.
  
#### Segments
This script is designed to handle segment processing and visualization for the Medieval Routes Project. It provides functionality to download segments within a specified bounding box from OpenStreetMap, validate and save these segments, load segments from a file, and visualize them using a static map.

##### General Overview
- Downloading Segments: Fetch and save segments within a bounding box from OpenStreetMap.
- Loading Segments: Load previously saved segments from a file.
- Validating Segments: Ensure segment data meets certain criteria (e.g., date and distance).
- Visualizing Segments: Create and save a static map image of the segments.

##### Key functions

1. Download Segments:  This function downloads all segments within the specified bounding box from OpenStreetMap and saves them to a file.
   
2. Validate Segments: Ensures segments meet specified criteria, such as the year of data(need to be newer than the limit year) and distance between points(need to be closer than 0.1km).
   
3. Load Segments: Reads segments from a file into a list of segment objects.

4. Get Segments: Depending on the existence of a file, either load segments from it or download them if the file does not exist.
   
5. View Segments: Creates a static map image of the segments and saves it as a PNG file.
   
#### Monuments
The Monuments module handles retrieving and managing monument data from the Catalunya Medieval website. It provides functionalities tailored for working with monument information:
1. Download Monuments: Retrieve monument data from the Catalunya Medieval website and save it to a file.

2. Load Monuments: Reads monument data from a file, enabling access to previously downloaded monuments. It offers the flexibility to filter monuments based on their geographic location within a specified bounding box.

3. Get Monuments: Similar to the Get Segments function, it either loads monuments from a file or downloads them if the file does not exist. It also allows the filtering of monuments based on a specified bounding box.
   
#### Graphmaker
The GraphMaker program is designed to create and simplify a graph based on geographical segments. It utilizes clustering techniques to organize points, builds a graph from these clusters, and then simplifies the graph by removing certain nodes to improve efficiency and readability.
##### General Overview
- Clustering Points: The program starts by converting geographical segments into a numpy array of points. These points are then clustered using the KMeans algorithm. Clustering helps in grouping nearby points together, reducing the complexity of the graph.

- Building the Graph: Once the points are clustered, the centroids of these clusters are used as nodes in the graph. The program then creates edges between these nodes based on the cluster labels, forming an initial graph.

- Simplifying the Graph: The program simplifies the graph by removing nodes with exactly two edges if the angle between the edges is nearly 180 degrees. This process helps in reducing unnecessary complexity in the graph while preserving the overall structure.

##### Key Functions
1. make_graph: This is the main function that coordinates the entire process. It converts segments into points, performs clustering, builds the initial graph, and then simplifies it.

2. simplify_graph: This function simplifies the graph by removing nodes with exactly two edges if the angle between the edges is near 180 degrees. This helps in reducing the complexity of the graph without losing significant information.
#### Viewer
The Viewer program provides functionalities to export a graph to PNG and KML formats. The PNG export uses the StaticMap library for rendering static map images, while the KML export uses the fastKML library to generate KML files suitable for viewing in applications like Google Earth.

##### General Overview
- Exporting to PNG:

  Purpose: This part of the module generates a static image of the graph, highlighting nodes and edges.
  
  Process: The graph's edges and nodes are added to a StaticMap object. The map is then rendered and saved as a PNG file.
  
- Exporting to KML:

  Purpose: This part of the module generates a KML file, which can be viewed in 3D mapping applications like Google Earth.
  
  Process: The graph's nodes and edges are converted to KML placemarks and lines. These are added to a KML document, which is then saved to a file.
  

##### Key Functions
1. export_png: This is the main function for exporting the graph to a PNG file. It creates a StaticMap object, adds the graph's edges and nodes, renders the map, and saves the image.
2. export_kml: This is the main function for exporting the graph to a KML file. It creates a KML document, adds the graph's nodes and edges as KML placemarks, and saves the document to a file.
#### Routes
The Routes module finds and generates optimal routes between specified locations or landmarks. It employs graph algorithms and spatial analysis techniques to compute shortest paths and visualize route information for navigation.

### Program Architecture

### Prerequisites

What things you need to install the software and how to install them:
- Python 3.x
- pip (Python package installer)

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the main program:
    ```bash
    python main.py
    ```

3. Follow the on-screen instructions to input the coordinates and generate maps.

### Running the Tests

#### Unit Tests:
```bash
python -m unittest discover tests
```
These tests simulate user interactions and verify that the system behaves as expected from start to finish.

### Built with
- Python - The programming language used
- NetworkX - Used for creating and manipulating complex networks/graphs
- Matplotlib - Used for generating 2D plots
- SimpleKML - Used for generating KML files
- StaticMap - Used for creating static map images
- BeautifulSoup - Used for parsing HTML data
- Requests - Used for making HTTP requests
- GPXPy - Used for parsing GPX files
- Scikit-learn - Used for clustering algorithms
- Haversine - Used for calculating distances between coordinates

### Example Workflow
#### Introduction

When you start the application, it will guide you through a series of steps to select a geographic region, process hiking routes, infer a map (graph), and find optimal paths to medieval monuments. The key steps and the expected workflow are detailed below.

#### Workflow Steps
1. Specify Geographic Region: Define the region of interest by providing the bounding rectangle's geographical coordinates (latitude and longitude).

2. Download Hiking Routes: The program fetches GPS routes from OpenStreetMap for the specified region.

3. Process and Cluster Data: The downloaded GPS data is processed, and points are clustered to identify significant waypoints, which become the graph nodes.

4. Graph Construction: Create an undirected graph where nodes represent clustered waypoints and edges represent paths between them.

5. Graph Simplification: Simplify the graph by merging nodes and edges based on specified criteria to reduce complexity without losing significant information.

6. Medieval Monuments Data: Fetch data about medieval monuments from Catalunya Medieval, including names and coordinates.

7. Find Optimal Routes: Calculate the shortest paths from a given starting point to all specified monuments using the graph.

8. Visualization:

2D Visualization: Generate and save a PNG image of the map with routes using StaticMap.

3D Visualization: Generate and save a KML file for 3D visualization in Google Earth.

#### Example Output
2D Map Example: A PNG image showcasing the map and routes (insert example image if available).

3D Map Example: A KML file viewable in Google Earth displaying the routes in 3D (insert example image if available).

By following these steps, users can interactively explore hiking routes and find optimal paths to medieval monuments within their region of interest.

### Authors
Lucas Federico Viner & Oriol Parent
