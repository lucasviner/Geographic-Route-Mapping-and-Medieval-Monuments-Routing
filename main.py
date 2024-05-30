from yogi import read
from graphmaker import make_graph, Graph
from viewer import export_png, export_kml
from segments import Box, Point, Segments, get_segments
from monuments import get_monuments, load_monuments, Monuments
from routes import find_routes
import traceback


def main() -> None:
    introduction()
    
    print("Please enter the coordinates of the region you would like to process:")
    box = get_user_input_box()
    
    segments = get_segments_in_box(box)
    print("Downloading segments for the specified region. This may take a few minutes...")
    
    print("Creating the graph from the segments...")
    graph = create_graph(segments)
    
    export_option = get_export_option()
    export_graph(graph, export_option)
    
    print("Now, we will download the monuments data from Medieval Catalunya.")
    filename_monuments = get_filename('monuments')
    print("Please wait...")
    get_monuments(box, f'{filename_monuments}.dat')
    print("Download complete! You can now find optimal routes to nearby monuments within the region.")
    monuments_of_the_box = load_monuments(box, f'{filename_monuments}.dat')
    
    while True:
        find_optimal_routes(monuments_of_the_box, graph)
        decision = input("Introduce 'exit' if you would like to exit.\nIntroduce 'restart' if you would like to define a new box.\nIf not, introduce any character: \n")
        if decision == "exit": break
        if decision == "restart": 
            main() 
            return


def introduction() -> None:
    print("Welcome to the Medieval Routes Project!")
    print("In this project, you will be able to:")
    print("1. Obtain hiker routes in a geographic region.")
    print("2. Infer a map (a graph) from the routes.")
    print("3. Obtain coordinates of medieval monuments.")
    print("4. Find optimal routes to medieval monuments in the inferred graph.")
    print("5. Visualize the resulting maps in 2D and 3D.")
    print("\nLet's get started!")


def get_user_input_box() -> Box:
    """Prompt the user to input the coordinates of the region."""
    while True:
        try:
            bottom_left_lat = float(input("Enter the latitude of the bottom left corner: "))
            bottom_left_lon = float(input("Enter the longitude of the bottom left corner: "))
            top_right_lat = float(input("Enter the latitude of the top right corner: "))
            top_right_lon = float(input("Enter the longitude of the top right corner: "))
            return Box(Point(bottom_left_lat, bottom_left_lon), Point(top_right_lat, top_right_lon))
        except ValueError:
            print("Invalid input. Please enter numeric values for coordinates.")


def get_filename(information: str) -> str:
    """Asks the user for the name of the file where the information will be saved. """
    return input(f"Indicate the name of the file where you would like to save the {information}. Take into account that if the name of the file is the same as any other existing file, we will only take into account the file arleady created.\n")


def get_segments_in_box(box: Box) -> Segments:
    """Get the segments within the specified box."""
    filename_segments = get_filename('segments')
    return get_segments(box, f'{filename_segments}.dat')


def create_graph(segments: Segments) -> Graph:
    """Create a graph from the given segments."""
    return make_graph(segments, num_clusters=100)


def get_export_option() -> int:
    """Prompt the user to choose an export option."""
    while True:
        try:
            print("Choose an option for exporting the graph routes:")
            print("1) --> Export to .png file")
            print("2) --> Export to .kml file")
            print("3) --> Export to both .png and .kml files")
            print("4) --> Do not export")
            return read(int)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")


def export_graph(graph: Graph, export_option: int) -> None:
    """Export the graph routes based on the chosen export option."""
    if export_option == 4:
        print("No export selected.")
        return
    else:
        if export_option == 1:
            filename_png = get_filename('graph.png')
            export_png(graph, f"{filename_png}.png")
            print("Graph routes exported to graph.png")
        elif export_option == 2:
            filename_kml = get_filename('graph.kml')
            export_kml(graph, f"{filename_kml}.kml")
            print("Graph routes exported to graph.kml")
        else:
            filename_png = get_filename('graph.png')
            filename_kml = get_filename('graph.kml')
            export_png(graph, f"{filename_png}.png")
            export_kml(graph, f"{filename_kml}.kml")
            print(f"Graph routes exported to {filename_png}.png and {filename_kml}.kml")

def find_optimal_routes(monuments: Monuments, graph: Graph) -> None:
    """Prompt the user to input an initial point and find optimal routes to nearby monuments within the region."""
    while True:    
        try:
            print("Enter an initial point to find optimal routes to all nearby monuments within the region:")
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
            point = Point(lat, lon)
            filename_routes = get_filename('routes')
            print(f"Calculating optimal routes from ({lat}, {lon}) to nearby monuments...")
            find_routes(graph, point, monuments, filename_routes)
            print(f"Done! To watch the results, look the {filename_routes} documents (.png and .kml)")
            return
        except ValueError:
            print("Invalid input. Please enter numeric values for latitude and longitude.")    


if __name__ == "__main__":
    main()