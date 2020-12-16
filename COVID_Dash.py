# -*- coding: utf-8 -*-
"""
This program creates a dashboard that displays Covid infections, hospitalizations, and deaths by state
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



df = pd.read_csv('covid_long.csv')
tab_df = pd.read_csv('dec13_sum.csv')


states = df['STATE_NAME'].unique()

metrics = df['METRIC'].unique()

daily = df['DAY_TOTAL'].unique()

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

app.layout = html.Div([
    html.H1('COVID-19 State Metric Tracker', style={'textAlign': 'center'}),
     html.H6('Andrew vanderWilden -- MA 705 Final Project', style = {'textAlign': 'center'}),
     html.P('All data from The COVID Tracking Project through 12/13/2020\n',
             style = {'textAlign': 'center'}),
     html.P('Note that some states have not reported cumulative hospitalizations',
            style = {'textAlign': 'center', 'color': 'red', 'font-size': '12px'}),
     html.Br(),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='state',
                options=[{'label': i, 'value': i} for i in states],
                value='Alaska'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='metric',
                options=[{'label': i, 'value': i} for i in metrics],
                value='Infections'
            ),
            dcc.RadioItems(
                id='daily_ind',
                options=[{'label': i, 'value': i} for i in daily],
                value='Daily',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Br(),
    dcc.Graph(id='metric_plot'),
    html.Br(),
    html.P('Cumulative Metrics for all States as of 12/13/2020'),
    generate_table(tab_df, max_rows = 56)
    
])

@app.callback(
    Output('metric_plot', 'figure'),
    Input('state', 'value'),
    Input('metric', 'value'),
    Input('daily_ind', 'value'))

def update_graph(state_id, metric_id, daily_id):
    df2 = df[df['STATE_NAME'] == state_id]
    
    df3 = df2[df2['METRIC'] == metric_id]
    
    df4 = df3[df3['DAY_TOTAL'] == daily_id]
    
    if daily_id == 'Daily':
        fig = px.bar(df4, x = 'DATE', y = 'VALUE')
    else:
        fig = px.line(df4, x = 'DATE', y = 'VALUE')
        
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    
    fig.update_yaxes(title = metric_id)
    
    return fig
    


if __name__ == '__main__':
    app.run_server(debug=True)










