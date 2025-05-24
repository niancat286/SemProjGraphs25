# Graph Visualizer
A Python-based tool for visualizing graphs, built as semestral project.

## Installation

### Prerequisites
- Python 3.8 or higher
- `git` for cloning the repository
- `pip3` for installing dependencies

### Install From Source
```bash
git clone https://github.com/niancat286/SemProjGraphs25.git Graph_Visualizer
cd Graph_Visualizer
```

### Dependencies


The following libraries are required:
- Numpy
- Tkinter
- sv-ttk

Install all dependencies using ```pip3 install -r requirements.txt```
Or install them yourself. 

## Usage

 To start the program, run ```python3 main.py```. This will launch the Graph Visualizer GUI, where you can import graph data and visualize it.

### GUI Features and Usage Instructions

Once the GUI is launched, you can interact with the graph visualization using the following features:

- **Edge Labels**:

  - Use the checkbox in the bottom right corner to hide or show edge labels.

- **Navigation**:

  - Drag the visualization with your mouse to move the view.
  - Use the four arrow buttons on the GUI.

- **Zooming**:

  - Scroll the mouse wheel to zoom in or out.
  - Alternatively, adjust the zoom level using the slider on the GUI.

- **Rotation**:

  - To rotate the graph around its centroid, drag the mouse while holding the Ctrl key.
  - Rotation can also be controlled via the sliders on the right side of the interface.
  - Click the 'Recalculate Centroid' button to update the centroid based on the current vertices' positions.
  - For rotation around a specific vertex, select the vertex and use the rotation sliders.

- **Vertex Manipulation**:

  - Individual vertices can be dragged to new positions using the mouse.
  - While holding a vertex with the mouse, scroll the wheel to move this vertex farther/closer to the camera.
  - To precisely adjust a vertex's coordinates, use the interface accessed via the 'Move Vertex' button.
