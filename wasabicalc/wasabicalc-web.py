import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import wasabicalc

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Input parameters:
    '''),
    dcc.Input(id='full_interval', value=30, inputmode='numeric', type='number', step=1),
    dcc.Input(id='full_initial_size', value=500, inputmode='numeric', type='number', step=50),

    html.Div(id='output-graph')
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='full_interval', component_property='value'),
    Input(component_id='full_initial_size', component_property='value')]
)
def update_graph(input_full_interval, input_full_initial_size):
    wasabicalc_params = dict(
            full_interval=int(input_full_interval),
            full_initial_size=int(input_full_initial_size),
            partial_interval=1,
            partial_size=0.1,
            partial_size_var=(-1, 1),
            retention=90,
            time_ranges=[30, 60, 90, 180, 360, 720],
            price_minimum=4.99,
            minimum_storage_time=90
    )

    cost_raport = wasabicalc.wasabicalc(wasabicalc_params)

    cost_data = dict(
        x=[],
        y=[],
        type='line',
        name='Cost',
        xaxis='x1',
        yaxis='y1'
        )
    usage_data = dict(
        x=[],
        y=[],
        type='bar',
        name='Usage',
        xaxis='x1',
        yaxis='y2'
        )

    for month in cost_raport:
        cost_data['x'].append(month[0])
        cost_data['y'].append(month[2])

        usage_data['x'].append(month[0])
        usage_data['y'].append(month[1])

    return dcc.Graph(
        id='cost-graph',
        figure={
            'data': [
                cost_data,
                usage_data,
            ],
            'layout': {
                'yaxis': {
                    'overlaying': 'y2',
                    'title': 'Cost (USD)'
                },
                'yaxis2': {
                    'anchor': 'x',
                    'side': 'right',
                    'title': 'Usage (GB)'
                },
                'title': 'Monthly cost and usage'
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)
