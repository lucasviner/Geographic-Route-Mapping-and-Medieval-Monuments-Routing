# Pràctica GCED-AP2 2024 · Rutes i monuments

## Geographic Route Mapping and Medieval Monuments Routing

### Project Description

This project allows users to process geographic data, obtain hiking routes within a specified region, infer a map (graph) based on these routes, and find optimal paths to medieval monuments within the region. The results can be visualized in both 2D and 3D formats. Users can export the generated maps in .png and .kml formats and interactively find optimal routes to various points of interest.

### Table of Contents
1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installing](#installing)
4. [Running the Tests](#running-the-tests)
5. [Deployment](#deployment)
6. [Built With](#built-with)
7. [Authors](#authors)
8. [Example Workflow](#example-workflow)

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Que fa cada program

### Arquitectura del programa

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

### Deployment
1. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```

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

### Authors
Your Name - Initial work - YourGitHubProfile

### Example Workflow
#### Introduction

When you start the application, it will guide you through a series of steps to select a geographic region, process hiking routes, infer a map (graph), and find optimal paths to medieval monuments. The key steps and the expected workflow are detailed below.

#### Workflow Steps
1. Specify Geographic Region: Define the region of interest by providing the geographical coordinates (latitude and longitude) of the bounding rectangle.

2. Download Hiking Routes: The program fetches GPS routes from OpenStreetMap for the specified region.

3. Process and Cluster Data: The downloaded GPS data is processed, and points are clustered to identify significant waypoints, which become the nodes of the graph.

4. Graph Construction: Create an undirected graph where nodes represent clustered waypoints and edges represent paths between them.

5. Graph Simplification: Simplify the graph by merging nodes and edges based on specified criteria to reduce complexity without losing significant information.

6. Medieval Monuments Data: Fetch data about medieval monuments from Catalunya Medieval, including names and coordinates.

7. Find Optimal Routes: Using the graph, calculate the shortest paths from a given starting point to all specified monuments.

8. Visualization:

2D Visualization: Generate and save a PNG image of the map with routes using StaticMap.

3D Visualization: Generate and save a KML file for 3D visualization in Google Earth.

#### Example Output
2D Map Example: A PNG image showcasing the map and routes (insert example image if available).

3D Map Example: A KML file viewable in Google Earth displaying the routes in 3D (insert example image if available).

By following these steps, users can interactively explore hiking routes and find optimal paths to medieval monuments within their region of interest.
