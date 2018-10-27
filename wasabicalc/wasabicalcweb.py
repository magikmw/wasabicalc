import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import wasabicalc

app = dash.Dash()

app.config.update({
    # as the proxy server will remove the prefix
    'routes_pathname_prefix': '/',

    # the front-end will prefix this string to the requests
    # that are made to the proxy server
    'requests_pathname_prefix': '/wasabicalc'
})

app.css.append_css({
    "external_url":
    "https://cdn.rawgit.com/yegor256/tacit/gh-pages/tacit-css-1.3.3.min.css"
})

app.title="wasabicalc by magikmw"

app.layout = html.Div(children=[

    html.H1('wasabicalc'),

    html.Div(className='textcontainer', children=[
        html.H2('''What is this?'''),
        dcc.Markdown(
'''
wasabicalc is a cost calculator for a backup scheme involving any incramental backup solution with an object storage service called [wasabi](https://wasabi.com/).

I've created wasabicalc due to wasabi's minimum 90-day storage charge. While overall wasabi's pricing is strightforward compared to other storage providers (no egress or API call charges), if your storage needs mean adding and removing files on a regular basis (as is common with incramenal backup software like [restic](https://restic.net/) or [duplicity](http://duplicity.nongnu.org/)) you probably want to adjust your backup and retention policies so you don't upload your backups into high costs over next three months.

You can read more about the minimum 90-day storage charge in wasabi's [pricing FAQ](https://wasabi.com/pricing/pricing-faqs/).

Adjust the sliders below according to your needs. Most should be self-explanatory. Partial backup size variation is used to simulate ups and downs in the backup source data size - if your data only grows push the minimal value to at least 0, for example.

wasabicalc:
  * was created with Python and [Dash by plot.ly](https://dash.plot.ly/),
  * is licensed under AGPL,
  * and you can find the source [on Github](https://github.com/magikmw/wasabicalc).

  [magikmw](https://michalwalczak.eu/)
'''),
    ]),

    html.Div(className='graph', id='output-graph'),

    html.Div(className='inputs', children=[

        html.H2('Input parameters:'),
        html.Div(className='label_with_inputs', children=[
            html.Label('Full backup interval [days]:'),
            dcc.Slider(id='full_interval',
                       value=30, min=1, max=90, step=None,
                       marks={i: '{0}'.format(i) for i in range(0, 91, 15)}
                       )]),

        html.Div(className='label_with_inputs', children=[
            html.Label('Full backup initial size [GB]: '),
            dcc.Slider(id='full_initial_size',
                       value=500, min=0, max=10000,
                       marks={i: '{0}'.format(i)
                              for i in range(0, 10001, 1000)}
                       )]),

        html.Div(className='label_with_inputs', children=[
            html.Label('Partial backup interval [days]: '),
            dcc.Slider(id='partial_interval',
                       value=1, min=1, max=30,
                       marks={i: '{0}'.format(i) for i in range(0, 31, 5)}
                       )]),

        html.Div(className='label_with_inputs', children=[
            html.Label('Partial backup size [GB]'),
            dcc.Slider(id='partial_size',
                       value=1, min=0, max=1000,
                       marks={i: '{0}'.format(i) for i in range(0, 1001, 100)}
                       )]),

        html.Div(className='label_with_inputs', children=[
            html.Label('Partial backup size variation [GB]: '),
            dcc.RangeSlider(id='partial_size_var',
                            value=[-1, 1], min=-100, max=100,
                            marks={i: '{0}'.format(i)
                                   for i in range(-100, 101, 10)}
                            )]),

        html.Div(className='label_with_inputs', children=[
            html.Label('Retention period [days]:'),
            dcc.Slider(id='retention',
                       value=90, min=30, max=360, step=None,
                       marks={i: '{0}'.format(i) for i in range(30, 361, 30)}
                       )]),

        html.Div(className='label_with_inputs', children=[
            html.Label('Time range [months]:'),
            # dcc.Input(id='time_range',
            #           value=12, inputmode='numeric', type='number', step=1,
            #           min=1)]),
            dcc.Slider(id='time_range',
                       value=12, min=1, max=36, step=None,
                       marks={i: '{0}'.format(i) for i in range(0, 37, 3)}
                       )]),

        dcc.Input(id='price_mnimum',
                  # hidden when this issue gets fixed:
                  # https://github.com/plotly/dash-core-components/issues/169
                  value=4.99, inputmode='numeric', type='hidden'),
        dcc.Input(id='minimum_storage_time',
                  value=90, inputmode='numeric', type='hidden')
    ])
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [
        Input(component_id='full_interval', component_property='value'),
        Input(component_id='full_initial_size', component_property='value'),
        Input(component_id='partial_interval', component_property='value'),
        Input(component_id='partial_size', component_property='value'),
        Input(component_id='partial_size_var', component_property='value'),
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
    input_partial_size_var,
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
            partial_size_var=input_partial_size_var,
            retention=input_retention,
            time_range=input_time_range*30+1,
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
