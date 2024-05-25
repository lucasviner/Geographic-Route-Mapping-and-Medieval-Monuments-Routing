from yogi import read
from graphmaker import make_graph
from viewer import export_png, export_kml
from segments import Box, Point, get_segments
from monuments import download_monuments, load_monuments
import networkx as nx


def main():
    print("Welcome to the Medieval Routes Project!")
    print("In this project, you will be able to:")
    print("1. Obtain hiker routes in a geographic region.")
    print("2. Infer a map (a graph) from the routes.")
    print("3. Obtain coordinates of medieval monuments.")
    print("4. Find optimal routes to medieval monuments in the inferred graph.")
    print("5. Visualize the resulting maps in 2D and 3D.")
    print("\nLet's get started!")
    
    print("Please enter the coordinates of the region you would like to process:")
    box = get_user_input_box()
    
    print("Downloading segments for the specified region. This may take a few minutes...")
    segments = get_segments_in_box(box)
    
    print("Creating the graph from the segments...")
    graph = create_graph(segments)
    
    export_option = get_export_option()
    export_graph(graph, export_option)
    
    print("Now, we will download the monuments data from Medieval Catalunya. Please wait...")
    download_monuments('monuments.dat')
    print("Download complete! You can now find optimal routes to nearby monuments within the region.")
    
    while True:
        find_optimal_routes()


def get_user_input_box() -> Box:
    """Prompt the user to input the coordinates of the region."""
    bottom_left_lat = float(input("Enter the latitude of the bottom left corner: "))
    bottom_left_lon = float(input("Enter the longitude of the bottom left corner: "))
    top_right_lat = float(input("Enter the latitude of the top right corner: "))
    top_right_lon = float(input("Enter the longitude of the top right corner: "))
    return Box(Point(bottom_left_lat, bottom_left_lon), Point(top_right_lat, top_right_lon))


def get_segments_in_box(box: Box) -> list:
    """Get the segments within the specified box."""
    return get_segments(box, "segments.dat")


def create_graph(segments: list) -> nx.Graph:
    """Create a graph from the given segments."""
    return make_graph(segments, num_clusters=100)


def get_export_option() -> int:
    """Prompt the user to choose an export option."""
    print("Choose an option for exporting the graph routes:")
    print("1) --> Export to .png file")
    print("2) --> Export to .kml file")
    print("3) --> Export to both .png and .kml files")
    print("4) --> Do not export")
    return read(int)


def export_graph(graph: nx.Graph, export_option: int) -> None:
    """Export the graph routes based on the chosen export option."""
    if export_option == 1:
        export_png(graph, "graph.png")
        print("Graph routes exported to graph.png")
    elif export_option == 2:
        export_kml(graph, "graph.kml")
        print("Graph routes exported to graph.kml")
    elif export_option == 3:
        export_png(graph, "graph.png")
        export_kml(graph, "graph.kml")
        print("Graph routes exported to graph.png and graph.kml")
    else:
        print("No export selected.")


def find_optimal_routes() -> None:
    """Prompt the user to input an initial point and find optimal routes to nearby monuments within the region."""
    print("Enter an initial point to find optimal routes to all nearby monuments within the region:")
    lat = float(input("Latitude: "))
    lon = float(input("Longitude: "))
    point = Point(lat, lon)
    box = get_user_input_box()
    monuments = load_monuments(box, 'monuments.dat')
    # Here you would calculate the routes and display the maps
    print(f"Calculating optimal routes from ({lat}, {lon}) to nearby monuments...")
    # routes(point)


if __name__ == "__main__":
    main()
