import os
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Set up paths
OUTPUT_DIR = '../outputs'

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load top candidates
candidates = pd.read_csv(os.path.join(OUTPUT_DIR, 'top_candidates.csv'))

# Define app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Technosignature Candidate Dashboard", className="text-center my-4"),
            html.Hr()
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Top Candidates", className="text-center mb-3"),
            dash.dash_table.DataTable(
                id='candidates-table',
                columns=[
                    {"name": "Source ID", "id": "source_id"},
                    {"name": "Mission", "id": "mission"},
                    {"name": "Techno Score", "id": "techno_score", "type": "numeric", "format": {"specifier": ".3f"}},
                    {"name": "Anomaly Score", "id": "anomaly_score", "type": "numeric", "format": {"specifier": ".3f"}},
                    {"name": "Transit Power", "id": "transit_power", "type": "numeric", "format": {"specifier": ".3f"}},
                    {"name": "IR Excess", "id": "ir_excess", "type": "numeric", "format": {"specifier": ".3f"}},
                    {"name": "HI Hits", "id": "hi_hit_count", "type": "numeric"}
                ],
                data=candidates.to_dict('records'),
                sort_action="native",
                sort_mode="multi",
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Feature Distributions", className="text-center my-4"),
            dcc.Graph(id='feature-distributions')
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Score Correlations", className="text-center my-4"),
            dcc.Graph(id='score-correlations')
        ], width=12)
    ])
], fluid=True)

# Callback for feature distributions
@app.callback(
    Output('feature-distributions', 'figure'),
    Input('candidates-table', 'derived_virtual_data')
)
def update_feature_distributions(rows):
    if rows is None:
        df = candidates
    else:
        df = pd.DataFrame(rows)
    
    fig = go.Figure()
    
    features = ['transit_power', 'ir_excess', 'temperature', 'hi_hit_count']
    for feature in features:
        fig.add_trace(go.Histogram(
            x=df[feature],
            name=feature,
            opacity=0.75
        ))
    
    fig.update_layout(
        barmode='overlay',
        title='Distribution of Features',
        xaxis_title='Value',
        yaxis_title='Count',
        legend_title='Feature'
    )
    
    return fig

# Callback for score correlations
@app.callback(
    Output('score-correlations', 'figure'),
    Input('candidates-table', 'derived_virtual_data')
)
def update_score_correlations(rows):
    if rows is None:
        df = candidates
    else:
        df = pd.DataFrame(rows)
    
    fig = px.scatter_matrix(
        df,
        dimensions=['techno_score', 'anomaly_score', 'transit_power', 'ir_excess'],
        color='mission',
        title='Feature Correlations',
        labels={col: col.replace('_', ' ').title() for col in df.columns}
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050) 