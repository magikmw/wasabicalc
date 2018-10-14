import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import wasabicalc

app = dash.Dash()

app.css.append_css({
    "external_url": "https://cdn.rawgit.com/yegor256/tacit/gh-pages/tacit-css-1.3.3.min.css"
})

app.layout = html.Div(children=[
    html.Div(children='''
        Input parameters:
    '''),
    dcc.Input(id='full_interval',
              value=30, inputmode='numeric', type='number', step=5),
    dcc.Input(id='full_initial_size',
              value=500, inputmode='numeric', type='number', step=50),
    dcc.Input(id='partial_interval',
              value=1, inputmode='numeric', type='number'),
    dcc.Input(id='partial_size',
              value=0.1, inputmode='numeric', type='number'),
    dcc.Input(id='partial_size_var_min',
              value=-1, inputmode='numeric', type='number'),
    dcc.Input(id='partial_size_var_max',
              value=1, inputmode='numeric', type='number'),
    dcc.Input(id='retention',
              value=90, inputmode='numeric', type='number'),
    dcc.Input(id='time_range',
              value=12, inputmode='numeric', type='number', step=1),
    dcc.Input(id='price_mnimum',
              # hidden when this issue gets fixed:
              # https://github.com/plotly/dash-core-components/issues/169
              value=4.99, inputmode='numeric', type='hidden'),
    dcc.Input(id='minimum_storage_time',
              value=90, inputmode='numeric', type='hidden'),

    html.Div(id='output-graph')
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [
        Input(component_id='full_interval', component_property='value'),
        Input(component_id='full_initial_size', component_property='value'),
        Input(component_id='partial_interval', component_property='value'),
        Input(component_id='partial_size', component_property='value'),
        Input(component_id='partial_size_var_min', component_property='value'),
        Input(component_id='partial_size_var_max', component_property='value'),
        Input(component_id='retention', component_property='value'),
        Input(component_id='time_range', component_property='value'),
        Input(component_id='price_mnimum', component_property='value'),
        Input(component_id='minimum_storage_time', component_property='value')
    ]
)
def update_graph(
    input_full_interval,
    input_full_initial_size,
    input_partial_interval,
    input_partial_size,
    input_partial_size_var_min,
    input_partial_size_var_max,
    input_retention,
    input_time_range,
    input_price_minimum,
    input_minimum_storage_time
        ):
    wasabicalc_params = dict(
            full_interval=input_full_interval,
            full_initial_size=input_full_initial_size,
            partial_interval=input_partial_interval,
            partial_size=input_partial_size,
            partial_size_var=[input_partial_size_var_min,
                              input_partial_size_var_max],
            retention=input_retention,
            time_range=input_time_range*30,
            price_minimum=input_price_minimum,
            minimum_storage_time=input_minimum_storage_time
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
