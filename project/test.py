import dash
import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nx
import argparse
import sys
parser = argparse.ArgumentParser(description='network_visualize')
parser.add_argument('--file',default='./proc_data/gmls/origin/1990_2.gml',help='the gml file',type=str)

args = parser.parse_args(args=sys.argv[1:])
app = dash.Dash(__name__)
G = nx.petersen_graph()
G = nx.read_gml(args.file)
elements=[]
for node in G.nodes:
    elements.append({'data': {'id': node, 'label': node,'age':G.nodes[node]['age']}})
    print(node)
for edge in G.edges:
    elements.append({'data': {'source': edge[0], 'target': edge[1]}})

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '800px'},
        elements=elements
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
