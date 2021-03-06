import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash()

df = pd.read_csv('https://raw.githubusercontent.com/cameron-marsden/pitchfork_analysis/master/p4k_summary_long_format.csv')

available_genres = df['Genre'].unique()

app.layout = html.Div([
    html.Div([
        html.H4('Select Genre:'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[{'label': i, 'value': i} for i in available_genres],
            value='Rock'
        )
    ], style={'width': '45%', 'padding-left': 200, 'padding-right': 200, 'font-family': 'Arial'}),

    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'width': '90%'})
])


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def create_x_time_series(selected_dropdown_value):
    dff = df[(df['Genre'] == selected_dropdown_value) & (df['Indicator Name'] == 'Sum of AOTY Points')]
    annotations = []
    # labeling left side of the plot
    annotations.append(dict(xref='paper', x=0, y=dff['Value'][dff.index[0]],
                        xanchor='right', yanchor='middle',
                        text='AOTY Points',
                        font=dict(family='Arial',
                                  size=16),
                        showarrow=False))

    # labeling right side of the plot
    annotations.append(dict(xref='paper', x=1, y=dff['Value'][dff.index[-1]],
                        xanchor='left', yanchor='middle',
                        text='{}'.format(dff['Value'][dff.index[-1]].astype(int)),
                        font=dict(family='Arial',
                                  size=16),
                        showarrow=False))

    return {
        'data': [{
            'x': dff['Year'],
            'y': dff['Value'],
            'mode': 'lines',
            'line': {
                'width': 3,
                'shape': 'spline',
                'smoothing': 0.3,
                'color': 'rgba(124, 124, 254, 1)'
            }
        }],
        'layout': {
            'height': 300,
            'margin': {'l': 200, 'b': 20, 'r': 50, 't': 20},
            'annotations': annotations,
            'yaxis': {'showgrid': False, 'showline': False, 'zeroline': False, 'showticklabels': False, 'fixedrange': True},
            'xaxis': {'showgrid': False, 'showline': True, 'zeroline': False, 'showticklabels': False, 'ticks': '', 'fixedrange': True}
        }
    }

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def create_y_time_series(selected_dropdown_value):
    dff = df[(df['Genre'] == selected_dropdown_value) & (df['Indicator Name'] == 'Proportion Genre Given BNM')]
    annotations = []
    # labeling left side of the plot
    annotations.append(dict(xref='paper', x=0, y=dff['Value'][dff.index[0]],
                            xanchor='right', yanchor='middle',
                            text='BNM Proportion',
                            font=dict(family='Arial',
                                      size=16),
                            showarrow=False))
    # labeling right side of the plot
    annotations.append(dict(xref='paper', x=1, y=dff['Value'][dff.index[-1]],
                        xanchor='left', yanchor='middle',
                        text='{}%'.format(round(100*dff['Value'][dff.index[-1]], 0).astype(int)),
                        font=dict(family='Arial',
                                  size=16),
                        showarrow=False))
    return {
        'data': [{
            'x': dff['Year'],
            'y': dff['Value'],
            'mode': 'lines',
            'line': {
                'width': 3,
                'shape': 'spline',
                'smoothing': 0.3,
                'color': 'rgba(124, 124, 124, 1)'
            }
        }],
        'layout': {
            'height': 300,
            'margin': {'l': 200, 'b': 50,'r': 50, 't': 0},
            'annotations': annotations,
            'yaxis': {'showgrid': False, 'showline': False, 'zeroline': False, 'showticklabels': False, 'fixedrange': True, 'hoverformat': ',.0%'},
            'xaxis': {'showgrid': False, 'showline': False, 'zeroline': False, 'fixedrange': True, 'ticks': 'outside', 'tickangle': -45, 'dtick': 1}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
