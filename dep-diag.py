import pandas as pd
from jaal import Jaal
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import argparse

def create_app(df_grouped, df_nodes, from_col, to_col, weight_col):
    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id='network-graph'),
        html.Div(id='node-info')  # Added for node information display
    ])

    # Callback for Network Visualization
    @app.callback(
        Output('network-graph', 'figure'),
        Output('node-info', 'children'),
        [Input('network-graph', 'clickData')]
    )
    def update_graph(clickData):
        node_info = "Click a node to see its details"
        if clickData and 'points' in clickData:
            node_id = clickData['points'][0]['id']
            node_details = df_nodes[df_nodes['id'] == node_id].to_dict(orient='records')[0]
            node_info = f"Node ID: {node_details['id']}, Strength: {node_details['strength']}"

        # Visualize the network
        return Jaal(df_grouped).plot(
            vis_opts={
                'height': '1200px',
                'interaction': {'hover': True},
                'physics': {'enabled': False}  # Disable physics for static layout
            }
        ), node_info  # Return both the figure and node info

    return app

def main(file_path, from_col, to_col, weight_col):
    # Generic Data Loading and Preprocessing
    df = pd.read_csv(file_path)
    if "receivingIpAddress" in df.columns:
        df[to_col] = df[to_col] + " (" + df['receivingIpAddress'] + ")"

    df_grouped = df.groupby([from_col, to_col])[weight_col].sum().reset_index()
    df_grouped = df_grouped.rename(columns={from_col: 'from', weight_col: 'weight'})

    node_strengths = df_grouped.groupby('from')['weight'].sum().reset_index()
    node_strengths = node_strengths.rename(columns={'weight': 'strength'})
    df_nodes = pd.merge(df_grouped[['from']], node_strengths, on='from', how='left')
    df_nodes = df_nodes.rename(columns={'from': 'id'})

    app = create_app(df_grouped, df_nodes, from_col, to_col, weight_col)
    app.run_server(debug=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Network visualization from CSV")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    parser.add_argument("--from_col", type=str, default="initiatingDeviceName", help="Column name for the 'from' node")
    parser.add_argument("--to_col", type=str, default="receivingDeviceName", help="Column name for the 'to' node")
    parser.add_argument("--weight_col", type=str, default="connectionCount", help="Column name for the edge weight")
    args = parser.parse_args()

    main(args.file_path, args.from_col, args.to_col, args.weight_col)
