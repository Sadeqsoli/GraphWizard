import json
import math
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_cytoscape as cyto

app = dash.Dash(__name__)
server = app.server

# Define layers and their nodes
layer_map = {
    "Meta-level": ["Research", "Science"],
    "Macro Structure": ["Paradigm", "Framework", "Architecture", "Architectural Pattern", "Approach", "Quantitative and Qualitative Methods", "System"],
    "Theory Formation": ["Hypothesis", "Test", "Induction", "Deduction", "Inference", "Principle", "Law", "Theory", "Theorem"],
    "Initial Processing": ["Data Analysis", "Concept", "Problem", "Pattern"],
    "Base Layer": ["Observation", "Experience", "Intuition", "Data Collection"]
}

layer_values = {
    "Meta-level": 5,
    "Macro Structure": 4,
    "Theory Formation": 3,
    "Initial Processing": 2,
    "Base Layer": 1
}

layer_colors = {
    "Base Layer": "#1f77b4",
    "Initial Processing": "#ff7f0e",
    "Theory Formation": "#2ca02c",
    "Macro Structure": "#d62728",
    "Meta-level": "#9467bd"
}

data_file = 'Research_Method_Project_Graph.json'
with open(data_file, 'r', encoding='utf-8') as f:
    graph_data = json.load(f)

# Normalize node IDs
for node in graph_data['nodes']:
    node['id'] = node['id'].strip()

valid_node_ids = {node['id'] for node in graph_data['nodes']}

def get_node_layer(node_id):
    for layer, nodes in layer_map.items():
        if node_id in nodes:
            return layer
    return None

elements = []

# Add nodes with layer attribute and layerValue
def format_node(node):
    layer = get_node_layer(node['id'])
    return {
        'data': {
            'id': node['id'],
            'label': node['label'],  # English label
            'bilingual_label': node['bilingual_label'],  # English/Persian label
            'definition': node['definition'],
            'example': node['example'],
            'layer': layer,
            'layerValue': layer_values[layer] if layer else 0
        }
    }

elements.extend([format_node(node) for node in graph_data['nodes']])

def format_edge(edge):
    edges = []
    for source in edge['from']:
        s = source.strip()
        t = edge['to'].strip()
        if s in valid_node_ids and t in valid_node_ids:
            edges.append({
                'data': {
                    'source': s,
                    'target': t,
                    'type': edge['type']
                }
            })
    return edges

for edge in graph_data['edges']:
    elements.extend(format_edge(edge))

# Precompute positions for a preset layout
max_layer_value = max(layer_values.values())  # 5 in our case
radius_step = 200
center_x, center_y = 500, 400

# Group nodes by layerValue
nodes_by_layer_value = {}
for el in elements:
    if 'data' in el and 'layerValue' in el['data']:
        lv = el['data']['layerValue']
        nodes_by_layer_value.setdefault(lv, []).append(el)

for lv, node_list in nodes_by_layer_value.items():
    count = len(node_list)
    if count == 0:
        continue
    radius = (max_layer_value - lv) * radius_step
    # If radius is 0 and multiple nodes exist, spread them on a small circle
    if radius == 0 and count > 1:
        radius = 50

    for i, node in enumerate(node_list):
        angle = 2 * math.pi * i / count
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        node['position'] = {'x': x, 'y': y}

base_stylesheet = [
    {
        'selector': 'edge',
        'style': {
            'width': 2,
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#999',
            'line-color': '#999'
        }
    }
]

edge_color_map = {
    'pre-requirement': '#FF4136',   # Red
    'co-requirement': '#2ECC40'     # Green
}

# The language selected will determine which label attribute we use
def generate_stylesheet(selected_layers, selected_edge_types, selected_language):
    stylesheet = base_stylesheet[:]

    # Determine which label attribute to show
    label_field = 'label' if selected_language == 'en' else 'bilingual_label'

    # Define node style with larger font and size
    stylesheet.insert(0, {
        'selector': 'node',
        'style': {
            'label': f'data({label_field})',
            'text-wrap': 'wrap',
            'text-max-width': '120px',
            'font-size': '20px',
            'text-valign': 'center',
            'text-halign': 'center',
            'width': '100px',
            'height': '100px',
            'color': '#ffffff',
            'border-color': '#333',
            'border-width': 1
        }
    })

    # Hide all nodes
    stylesheet.append({'selector': 'node', 'style': {'display': 'none'}})

    # Show nodes in selected layers with their colors
    for layer in selected_layers:
        color = layer_colors.get(layer, '#0074D9')
        stylesheet.append({
            'selector': f'[layer = "{layer}"]',
            'style': {
                'display': 'element',
                'background-color': color
            }
        })

    # Hide all edges
    stylesheet.append({'selector': 'edge', 'style': {'display': 'none'}})

    # Show selected edge types
    for etype in selected_edge_types:
        stylesheet.append({
            'selector': f'[type = "{etype}"]',
            'style': {
                'display': 'element',
                'line-color': edge_color_map.get(etype, '#ccc'),
                'target-arrow-color': edge_color_map.get(etype, '#ccc')
            }
        })

    return stylesheet

all_layers = list(layer_map.keys())
edge_types = ['pre-requirement', 'co-requirement']

app.layout = html.Div([
    html.H1("Preset Layout with Concentric Positioning and Language Toggle"),
    html.Div(style={'display': 'flex'}, children=[
        html.Div(className='controls', style={'width': '20%', 'padding': '10px'}, children=[
            html.H3("Layers"),
            dcc.Checklist(
                id='layers-checklist',
                options=[{'label': layer, 'value': layer} for layer in all_layers],
                value=all_layers,
                labelStyle={'display': 'block'}
            ),
            html.H3("Edge Types"),
            dcc.Checklist(
                id='edge-types-checklist',
                options=[
                    {'label': 'Pre-Requirement', 'value': 'pre-requirement'},
                    {'label': 'Co-Requirement', 'value': 'co-requirement'}
                ],
                value=edge_types,
                labelStyle={'display': 'block'}
            ),
            html.H3("Language"),
            dcc.RadioItems(
                id='language-radio',
                options=[
                    {'label': 'English', 'value': 'en'},
                    {'label': 'Farsi', 'value': 'fa'}
                ],
                value='en',  # Default to bilingual
                labelStyle={'display': 'block'}
            )
        ]),
        html.Div(style={'width': '80%'}, children=[
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                layout={'name': 'preset'},
                style={'width': '100%', 'height': '800px'},
                # Initial stylesheet
                stylesheet=generate_stylesheet(all_layers, edge_types, 'fa')
            ),
            html.Div(id='node-info', style={'marginTop': '20px', 'whiteSpace': 'pre-line'})
        ])
    ])
])

@app.callback(
    Output('cytoscape', 'stylesheet'),
    Input('layers-checklist', 'value'),
    Input('edge-types-checklist', 'value'),
    Input('language-radio', 'value')
)
def update_stylesheet(selected_layers, selected_edge_types, selected_language):
    return generate_stylesheet(selected_layers, selected_edge_types, selected_language)

@app.callback(
    Output('node-info', 'children'),
    Input('cytoscape', 'tapNodeData')
)
def display_node_info(data):
    if data is None:
        return "Click on a node to see details."
    return html.Div([
        html.H4(f"Details for: {data['bilingual_label']}"),
        html.P(f"Definition: {data['definition']}"),
        html.P(f"Example: {data['example']}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
