# Hierarchical Bilingual Graph Visualization

This repository provides an interactive, hierarchical graph visualization using [Dash Cytoscape](https://dash.plotly.com/cytoscape). The graph represents a conceptual framework divided into multiple layers, each containing various concepts (nodes) and their relationships (edges). Users can toggle the visibility of different conceptual layers, switch on/off certain types of edges (pre-requirement and co-requirement), and view detailed information for each node.

## Key Features

- **Layered Visualization**  
  Nodes are arranged in concentric layers that represent different conceptual levels. The "Meta-level" concepts (e.g., *Research*, *Science*) are placed near the center, and "Base Layer" concepts (e.g., *Observation*, *Experience*) appear on the outer rings.

- **Customizable View**  
  The UI includes checklists that let users show or hide entire layers of the graph and toggle edge types (pre-requirement or co-requirement).

- **Color Coding**  
  Each layer is assigned a distinct color for its nodes, and edges are color-coded by type (e.g., pre-requirement edges in red, co-requirement edges in green).

- **Node Details**  
  Clicking on any node displays its definition, example, and bilingual label (English and Persian) in a details panel.

## Project Structure

project_root/
├── cyto/                # Directory for Cytoscape-related scripts or resources
├── graphviz/            # Directory for Graphviz-related scripts or resources
├── venv/                # Virtual environment for Python dependencies
├── cry_graph.py 

## Getting Started

Follow the steps below to set up and run the project locally:

### Prerequisites

- Python 3.8+
- `pip` for package management

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/hierarchical-graph-visualization.git
   cd hierarchical-graph-visualization
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python app.py
Open your browser and go to http://127.0.0.1:8050.

Usage
Toggling Layers
Use the layer checklist on the left to toggle the visibility of different conceptual layers.

Edge Controls
Toggle pre-requirement and co-requirement edges on or off using the edge type checklist.

Viewing Node Details
Click on any node to display its definition, example, and bilingual label in the details panel below the graph.

Layout
The graph uses a concentric layout with nodes arranged in layers:

Meta-level: Center
Base Layer: Outer ring
Example Graph

Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

vbnet
Copy code

### Instructions:

1. Save the above code in a `README.md` file in your project root.
2. Replace `https://github.com/your-username/hierarchical-graph-visualization.git` with your repository URL.
3. Add a screenshot of the graph to your project and update the `![Example Graph](path/to/screenshot.png)` line with the correct path. 

Let me know if you'd like to customize this further!
