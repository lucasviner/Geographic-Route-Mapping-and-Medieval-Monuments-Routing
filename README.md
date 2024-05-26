# Project Title

Geographic Route Mapping and Medieval Monuments Routing

## One Paragraph of project description goes here

This project allows users to process geographic data, obtain hiking routes within a specified region, infer a map (graph) based on these routes, and find optimal paths to medieval monuments within the region. The results can be visualized in both 2D and 3D formats. Users can export the generated maps in .png and .kml formats and interactively find optimal routes to various points of interest.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.x
- pip (Python package installer)

### Installing

A step-by-step series of examples that tell you how to get a development environment running:


1. **Install the required Python packages:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Run the main program:**

   ```sh
   python main.py
   ```

   Follow the on-screen instructions to input the coordinates and generate maps.

### Running the tests

Explain how to run the automated tests for this system:

1. **Unit tests:**

   ```sh
   python -m unittest discover tests
   ```

   These tests check the core functionality of the project, including distance calculations and graph construction.

2. **End-to-end tests:**

   ```sh
   python -m unittest discover e2e_tests
   ```

   These tests simulate user interactions and verify that the system behaves as expected from start to finish.

### Deployment

Add additional notes about how to deploy this on a live system:

1. **Set up a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```sh
   python main.py
   ```

## Built With

- [Python](https://www.python.org/) - The programming language used
- [NetworkX](https://networkx.github.io/) - Used for creating and manipulating complex networks/graphs
- [Matplotlib](https://matplotlib.org/) - Used for generating 2D plots
- [SimpleKML](https://simplekml.readthedocs.io/en/latest/) - Used for generating KML files

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

## Authors

- **Your Name** - *Initial work* - [YourGitHubProfile](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/yourprojectname/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration from various online resources and communities
- etc

---

### Example Workflow

1. **Introduction:**

   When you start the application, it will guide you through a series of steps to process geographic data and find routes to medieval monuments. First, the application will download data on all medieval monuments in Catalonia, which may take a few moments.

2. **Input Coordinates:**

   You will be prompted to enter the coordinates of the region you want to process in a specific format. This information is used to form a bounding box and download the relevant segments.

3. **Generating Graphs:**

   After forming the bounding box, the system will download the segments and generate a graph based on the hiking routes within the specified region. This step might take a few minutes.

4. **Exporting Maps:**

   You will have options to export the generated graphs in .png and .kml formats, both, or neither.

5. **Finding Optimal Routes:**

   After exporting, the application will download data on medieval monuments. You will then be able to input starting points within the region to find and display optimal routes to various monuments. This process can be repeated as many times as needed.

By following these steps, you will be able to visualize and interact with the geographical routes and find the best paths to medieval monuments within the specified region.