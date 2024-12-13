import json
import dash
from dash import dcc, html
import dash_cytoscape as cyto

# Load the JSON data
data_file = 'Research_Method_Project_Graph.json'
with open(data_file, 'r', encoding='utf-8') as f:
    graph_data = json.load(f)

# Convert nodes and edges into Cytoscape format
elements = []

# Add edges with validation
def format_edge(edge):
    if edge['from'] in [node['id'] for node in graph_data['nodes']] and edge['to'] in [node['id'] for node in graph_data['nodes']]:
        return {
            'data': {
                'source': edge['from'],
                'target': edge['to'],
                'type': edge['type']
            }
        }
    else:
        print(f"Skipping edge with invalid reference: {edge}")
        return None

edges = [format_edge(edge) for edge in graph_data['edges']]
elements.extend([edge for edge in edges if edge is not None])

# Add edges with validation
def format_edge(edge):
    if edge['from'] in [node['id'] for node in graph_data['nodes']] and edge['to'] in [node['id'] for node in graph_data['nodes']]:
        return {
            'data': {
                'source': edge['from'],
                'target': edge['to'],
                'type': edge['type']
            }
        }
    else:
        print(f"Skipping edge with invalid reference: {edge}")
        return None

edges = [format_edge(edge) for edge in graph_data['edges']]
elements.extend([edge for edge in edges if edge is not None])

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Bilingual Graph"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={
            'name': 'cose',  # Use the cose layout for directed graphs
            'animate': True
        },
        style={'width': '100%', 'height': '800px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'width': '40px',
                    'height': '40px',
                    'background-color': '#0074D9',
                    'color': '#ffffff',
                    'text-valign': 'center',
                    'text-halign': 'center'
                }
            },
            {
                'selector': '[type="pre-requirement"]',
                'style': {
                    'line-color': '#FF4136',
                    'target-arrow-color': '#FF4136',
                    'target-arrow-shape': 'triangle',
                    'arrow-scale': 1.5
                }
            },
            {
                'selector': '[type="co-requirement"]',
                'style': {
                    'line-color': '#2ECC40',
                    'target-arrow-color': '#2ECC40',
                    'target-arrow-shape': 'circle',
                    'arrow-scale': 1.2
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 2
                }
            }
        ]
    ),
    html.Div(id='node-info', style={'marginTop': '20px'})
])

# Add callback to display node information
@app.callback(
    dash.Output('node-info', 'children'),
    [dash.Input('cytoscape', 'tapNodeData')]
)
def display_node_info(data):
    if data is None:
        return "Click on a node to see details."
    return html.Div([
        html.H4(f"Details for: {data['label']}"),
        html.P(f"Definition: {data['definition']}"),
        html.P(f"Example: {data['example']}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
