# Pràctica GCED-AP2 2024 · Rutes i monuments

FALTA: ARQUITECTURA DEL PROGRAMA, EXPLICAR DECISIONS DE DISSENY QUE HAGUEM FET. 

## Geographic Route Mapping and Medieval Monuments Routing

### Project Description

This project allows users to process geographic data, obtain hiking routes within a specified region, infer a map (graph) based on these routes, and find optimal paths to medieval monuments. The results can be visualized in both 2D and 3D formats. Users can export the generated maps in .png and .kml formats and interactively find optimal routes to various monuments of interest.

### Table of Contents
1. [What each program does](#what-each-program-does)
2. [Program Architecture](#Program-Architecture)
3. [Getting Started](#getting-started)
4. [Prerequisites](#prerequisites)
5. [Installing](#installing)
7. [Built With](#built-with)
8. [Example Workflow](#example-workflow)
6. [Step-by-Step User Guide](#Step-by-Step_User-Guide)  
9. [Authors](#authors)


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

1. Download Segments
  - This function downloads all segments within the specified bounding box from OpenStreetMap and saves them to a file.

2. Validate Segments
  - Ensures segments meet specified criteria, such as the year of data(need to be newer than the limit year) and distance between points(need to be closer than 0.1km).

3. Load Segments
  - Reads segments from a file into a list of segment objects.
    
4. Get Segments
  -  Depending on the existence of a file, either load segments from it or download them if the file does not exist.
    
5. View Segments
  - Creates a static map image of the segments and saves it as a PNG file.
    
#### Monuments
This script is designed to handle monument processing for the Medieval Routes Project. It provides functionality to download monument data from a website, parse and save this data, load monuments from a file, and filter monuments based on a specified bounding box.

##### General Overview
- Downloading Monuments: Fetch and save monument data from the Catalunya Medieval website.
- Parsing Data: Extract and parse monument information from the downloaded content.
- Loading Monuments: Load monument data from a file and filter by location within a specified bounding box.
- Data Handling: Decode monument titles and manage data extraction.

##### Key Functions
1. Download Monuments
   
  - This function downloads monument data from the Catalunya Medieval website and saves it to a specified file.
  - It fetches the page content, extracts the relevant script tag, parses the monument data, and saves it to a file.

2. Fetch Page Content
   
  - Fetches the content of a web page, with retry logic in case of request failures.
    
3. Extract Script Tag

  - Extracts the script tag containing a specified keyword from the fetched web page content.

4. Save Monuments to File

  - Saves a list of monuments to a specified file, writing their names and coordinates.

5. Load Monuments

  - Loads monument data from a file and filters monuments based on their location within a specified bounding box.
  - Reads the file line by line, extracts monument data, and checks if each monument is within the given bounding box.

6. Get Monuments:
   
  - Retrieves all monuments within a specified bounding box.
  - If the specified file exists, it loads monuments from the file.
  - If the file does not exist, it downloads the monument data and saves it to the file before loading the monuments.

#### Graphmaker
The GraphMaker program is designed to create and simplify a graph based on geographical segments. It utilizes clustering techniques to organize points, builds a graph from these clusters, and then simplifies the graph by removing certain nodes to improve efficiency and readability.

##### General Overview
- Clustering Points: The program starts by converting geographical segments into a numpy array of points. These points are then clustered using the KMeans algorithm. Clustering helps in grouping nearby points together, reducing the complexity of the graph.

- Building the Graph: Once the points are clustered, the centroids of these clusters are used as nodes in the graph. The program then creates edges between these nodes based on the cluster labels, forming an initial graph.

- Simplifying the Graph: The program simplifies the graph by removing nodes with exactly two edges if the angle between the edges is nearly 180 degrees. This process helps in reducing unnecessary complexity in the graph while preserving the overall structure.

##### Key Functions
1. make_graph
  - Main function that coordinates the entire process.
  - Converts segments into points
  - Performs clustering
  - Builds the initial graph
  - Simplifies the graph.

2. simplify_graph
  - Simplifies the graph by removing nodes with exactly two edges if the angle between the edges is near 180 degrees.
  - Helps in reducing the complexity of the graph without losing significant information.

#### Viewer
This script is designed to handle the visualization of graphs for the Medieval Routes Project. It provides functionality to export graph data as static map images (PNG) and KML files for visualization in Google Earth.

##### General Overview

- Exporting to PNG: Create and save a static map image of the graph.
- Exporting to KML: Create and save a KML file of the graph for visualization in Google Earth.
- Adding Nodes and Edges: Add graph nodes and edges to both static maps and KML files.
  

##### Key Functions
1. Export PNG:

  - This function exports the graph to a PNG file using the staticmap library.
  - It adds nodes and edges to the static map and saves the rendered image to a specified file.

2. Add Edges to Static Map:

  - Adds the edges of the graph to a static map as lines.
  - Each edge is represented by a black line with a specified width.

3. Add Nodes to Static Map:

  - Adds the nodes of the graph to a static map as circle markers.
  - Each node is represented by a blue circle with a specified width.

4. Export KML:

  - This function exports the graph to a KML file using the fastkml library.
  - It adds nodes and edges to a KML document and saves it to a specified file.

5. Add Nodes to KML:

  - Adds the nodes of the graph to a KML document as placemarks.
  - Each node is represented by a placemark with its geographic coordinates.
 
 6. Add Edges to KML:

  - Adds the edges of the graph to a KML document as placemarks.
  - Each edge is represented by a line string connecting the start and end positions.

7. Save KML to File:

  - Saves the content of a KML object to a specified file.
  - Writes the KML data to a file in string format.

#### Routes
This script is designed to generate routes for the Medieval Routes Project, connecting a starting point with nearby monuments within a specified area. It provides functionality to find the closest node to a starting point, compute the shortest paths in a graph, identify nodes corresponding to monuments, and visualize the routes using static maps and KML files.

##### General Overview
- Finding Routes: Identify the shortest paths from a starting point to multiple monuments and save the visualizations.
- Computing Distances: Calculate Haversine distances between geographic points.
- Node Management: Map geographic points to graph nodes and handle node positions.
- Graph Construction: Build a route graph containing paths to monuments.
- Visualization: Create and save both static map images and KML files of the routes.

##### Key Functions

1. Find Routes:

  - This function generates routes from a starting point to nearby monuments.
  - It finds the closest node to the starting point, computes the shortest paths, and identifies if any monuments are within these paths.
  - If monuments are found, it builds a route graph and saves the visualizations as both a static map image and a KML file.

2. Find Closest Node:

  - Finds the closest graph node to a given geographic point using Haversine distance.

3. Haversine Distance:

  - Calculates the Haversine distance between two geographic points, which is essential for determining the closest nodes and edge weights in the graph.

4. Get Monuments Nodes:

  - Maps each monument's location to the closest graph node, returning a set of these nodes.

5. Build Route Graph:

  - Constructs a subgraph containing only the nodes and edges from the shortest paths that lead to the monuments.

6. Save Static Map:

  - Generates and saves a static map image of the route graph, highlighting the start node, monument nodes, and the routes.

7. Save KML:

  - Generates and saves a KML file for visualization in Google Earth, including the nodes and edges of the route graph.

### Program Architecture

The architecture of our program follows this relationship between its modules:

![ARQUITECTURA](https://github.com/lucasviner/practica2-AP2/assets/167958211/f0fbbfaf-cfe1-4190-a212-e60af8f9ec10)


It should be noted that having a dependency on a program has been interpreted as requiring data from it, not merely needing a type initialized in another module.

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing. 

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
2D Map Example: A PNG image showcasing the map and routes 

- Example of the graph with the segments
  
![EXAMPLE_GRAPH](https://github.com/lucasviner/practica2-AP2/assets/101245656/f4a98ff0-e84b-4691-b1ed-98ca6d85973c)

- Example of the graph with the optimal routes from an initial point to all the nearby monuments
  
![EXAMPLE_ROUTES](https://github.com/lucasviner/practica2-AP2/assets/101245656/97665dae-d7e5-48bb-8fe8-712d2ebb8b0e)

3D Map Example: A KML file viewable in Google Earth displaying the routes in 3D 

- Example of the graph with the segments
  
![image](https://github.com/lucasviner/practica2-AP2/assets/101245656/c5d291d7-b4a1-473c-ac5a-28b53578ec87)

- Example of the graph with some routes(indicated in black) to get to the nearby monuments(red points) strarting from an initial point(green point)

![image](https://github.com/lucasviner/practica2-AP2/assets/101245656/5593d30d-24c4-496c-b5c2-93f99423cb59)



By following these steps, users can interactively explore hiking routes and find optimal paths to medieval monuments within their region of interest.

### Step-by-Step User Guide


#### Running the Script
To run the main script main.py, open a terminal in the project directory and execute:

``` bash
python main.py
```
#### Step-by-Step Guide
- Introduction:
  
At the start of the script, you will see a welcome message that describes the project's objectives.

- Entering Coordinates:
  
You will be prompted to enter the coordinates of the region you want to process.

Latitude of the bottom left corner: Enter the latitude of the bottom left point of the box.

Longitude of the bottom left corner: Enter the longitude of the bottom left point of the box.

Latitude of the top right corner: Enter the latitude of the top right point of the box.

Longitude of the top right corner: Enter the longitude of the top right point of the box.

Example:

``` bash
Enter the latitude of the bottom left corner: 40.5363713
Enter the longitude of the bottom left corner: 0.5739316671
Enter the latitude of the top right corner: 40.79886535
Enter the longitude of the top right corner: 0.9021482
```

- Downloading Segments:
The script will download the segments within the specified box. This may take a few minutes.

- Creating the Graph:
You will be prompted to enter the number of clusters to create the graph. Enter an integer.

- Exporting the Graph:
You will be asked how you would like to export the graph:

1: Export to a .png file.

2: Export to a .kml file.

3: Export to both .png and .kml files.

4: Do not export.

- Downloading Monuments:
The script will download the medieval monument data from Medieval Catalunya. Please wait while the download completes.

- Calculating Optimal Routes:

You will be prompted to enter an initial point to find optimal routes to nearby monuments.

Latitude: Enter the latitude of the initial point.
Longitude: Enter the longitude of the initial point.

Example:

``` bash
Latitude: 40.65
Longitude: 0.75
```

- Continuation Options:

Enter exit to exit.

Enter restart to define a new box.

Enter any other character to continue.

#### Complete Execution Example

Here is an example of what a complete session might look like:

``` python
Welcome to the Medieval Routes Project!
In this project, you will be able to:
1. Obtain hiker routes in a geographic region.
2. Infer a map (a graph) from the routes.
3. Obtain coordinates of medieval monuments.
4. Find optimal routes to medieval monuments in the inferred graph.
5. Visualize the resulting maps in 2D and 3D.

Let's get started!
Please enter the coordinates of the region you would like to process:
Enter the latitude of the bottom left corner: 40.5363713
Enter the longitude of the bottom left corner: 0.5739316671
Enter the latitude of the top right corner: 40.79886535
Enter the longitude of the top right corner: 0.9021482
Downloading segments for the specified region. This may take a few minutes...
Creating the graph from the segments...
Please, indicate the number of clusters:
5
Choose an option for exporting the graph routes:
1) --> Export to .png file
2) --> Export to .kml file
3) --> Export to both .png and .kml files
4) --> Do not export
2
Indicate the name of the file where you would like to save the graph.kml. If the name of the file is the same as any other existing file, we will only consider the file already created.
my_graph
Graph routes exported to my_graph.kml
Now, we will download the monuments data from Medieval Catalunya.
Indicate the name of the file where you would like to save the monuments. If the name of the file is the same as any other existing file, we will only consider the file already created.
monuments_data
Please wait...
Download complete! You can now find optimal routes to nearby monuments within the region.
Enter an initial point to find optimal routes to all nearby monuments within the region:
Latitude: 40.65
Longitude: 0.75
Indicate the name of the file where you would like to save the routes. If the name of the file is the same as any other existing file, we will only consider the file already created.
optimal_routes
Calculating optimal routes from (40.65, 0.75) to nearby monuments...
Done! To watch the results, look at the optimal_routes documents (.png and .kml)
Introduce 'exit' if you would like to exit.
Introduce 'restart' if you would like to define a new box.
If you want to continue, introduce any character: 
```

#### Contact

If you have any questions or need assistance, feel free to contact the Medieval Routes Project support team.

### Authors
Lucas Federico Viner & Oriol Parent
