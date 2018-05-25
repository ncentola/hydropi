from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from vapeplot import vapeplot
import plotly.plotly as py
import dash, datetime, db
import pandas as pd

colors = {
    'background': '#111111',
    'plot': vapeplot.palette('vaporwave'),
    'text': 'grey'
}


app = dash.Dash(__name__)
app.scripts.config.serve_locally=True

sensor_data = pd.read_sql('SELECT * FROM readings ORDER BY created_at DESC LIMIT 100', con=db.db_con)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        # html.H3('System Time', style={'color': colors['text']}),
        # html.Div([
        #     html.Div('pH', style={'fontSize':12, 'color':colors['plot'][0]}),
        #     html.Div('Water Temp', style={'fontSize':12, 'color':colors['plot'][1]}),
        #     html.Div('Air Temp', style={'fontSize':12, 'color':colors['plot'][2]}),
        #     html.Div('TDS', style={'fontSize':12, 'color':colors['plot'][3]})
        # ], style={'textAlign': 'left', 'columnCount': 4}),
        html.Div([
                html.Div([
                    html.Div('pH', style={'fontSize':12, 'color':colors['plot'][0]}),
                    html.Div(id='ph_display_metric', style={'fontSize':36})
                ]),
                html.Div([
                    html.Div('Water Temp', style={'fontSize':12, 'color':colors['plot'][1]}),
                    html.Div(id='water_temp_display_metric', style={'fontSize':36}),
                ]),
                html.Div([
                    html.Div('Air Temp', style={'fontSize':12, 'color':colors['plot'][2]}),
                    html.Div(id='air_temp_display_metric', style={'fontSize':36}),
                ]),
                html.Div([
                    html.Div('TDS', style={'fontSize':12, 'color':colors['plot'][3]}),
                    html.Div(id='ec_display_metric', style={'fontSize':36})
                ]),
                html.Div([
                    html.Div('Humidity', style={'fontSize':12, 'color':colors['plot'][4]}),
                    html.Div(id='humidity_display_metric', style={'fontSize':36})
                ])
        ], style={'textAlign': 'center', 'columnCount': 5}),
        html.Div(id='hidden_div', style={'display':'none'}),
        # dcc.Graph(id='temp_graphs'),
        dcc.Graph(id='ph_graph'),
        dcc.Graph(id='water_temp_graph'),
        dcc.Graph(id='air_temp_graph'),
        dcc.Graph(id='ec_graph'),
        dcc.Graph(id='humidity_graph'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=100
        )
    ]
)
@app.callback(Output('hidden_div', 'children'), [Input('interval-component', 'n_intervals')])
def get_data(n):
    global sensor_data
    sensor_data = pd.read_sql('SELECT * FROM readings ORDER BY created_at DESC LIMIT 100', con=db.db_con)

# numbers to be displayed up top
@app.callback(Output('ph_display_metric', 'children'), [Input('interval-component', 'n_intervals')])
def ph_display_metric(n):
    global sensor_data
    val = sensor_data.ph[0]
    return html.Span(val, style={'size':24, 'color': colors['plot'][0]})


@app.callback(Output('water_temp_display_metric', 'children'), [Input('interval-component', 'n_intervals')])
def water_temp_display_metric(n):
    global sensor_data
    val = sensor_data.water_temp[0]
    return html.Span(val, style={'size':24, 'color': colors['plot'][1]})


@app.callback(Output('air_temp_display_metric', 'children'), [Input('interval-component', 'n_intervals')])
def air_temp_display_metric(n):
    global sensor_data
    val = sensor_data.air_temp[0]
    return html.Span(val, style={'size':24, 'color': colors['plot'][2]})


@app.callback(Output('ec_display_metric', 'children'), [Input('interval-component', 'n_intervals')])
def ec_display_metric(n):
    global sensor_data
    val = sensor_data.ec[0]
    return html.Span(val, style={'size':24, 'color': colors['plot'][3]})


@app.callback(Output('humidity_display_metric', 'children'), [Input('interval-component', 'n_intervals')])
def humidity_display_metric(n):
    global sensor_data
    val = sensor_data.humidity[0]
    return html.Span(val, style={'size':24, 'color': colors['plot'][4]})


@app.callback(Output('live-update-text', 'children'), [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    thing = pd.read_sql('SELECT * FROM readings ORDER BY created_at DESC LIMIT 1', con=db.db_con)
    text = 'System Time - {time}'.format(time=thing.created_at.max())

    return html.Span(text, style={'color': colors['text']})


@app.callback(Output('ph_graph', 'figure'), [Input('interval-component', 'n_intervals')])
def ph_graph(n):
    global sensor_data

    ph_trace = go.Scatter(
        x = sensor_data.created_at,
        y = sensor_data.ph,
        name = 'pH',
        mode='lines',
        yaxis='y1',
        line = dict(width=4, color=colors['plot'][0])
    )

    layout = go.Layout(
        height='240',
        font = dict(
          color = colors['text'],
          size = 12
        ),
        plot_bgcolor= colors['background'],
        paper_bgcolor= colors['background'],
        title='pH',
        yaxis=dict(
            side='right',
            dtick=.1
        )
    )

    graph_data = [ph_trace]

    return go.Figure(data=graph_data, layout=layout)


@app.callback(Output('water_temp_graph', 'figure'), [Input('interval-component', 'n_intervals')])
def water_temp_graph(n):
    global sensor_data

    water_temp_trace = go.Scatter(
        x = sensor_data.created_at,
        y = sensor_data.water_temp,
        name = 'Water Temp',
        mode='lines',
        line = dict(width=4, color=colors['plot'][1])
    )


    layout = go.Layout(
        height='240',
        font = dict(
          color = colors['text'],
          size = 12
        ),
        plot_bgcolor= colors['background'],
        paper_bgcolor= colors['background'],
        title='Water Temp (°F)',
        yaxis=dict(
            side='right',
            dtick=1
        )
    )

    graph_data = [water_temp_trace]

    return go.Figure(data=graph_data, layout=layout)

@app.callback(Output('air_temp_graph', 'figure'), [Input('interval-component', 'n_intervals')])
def air_temp_graph(n):
    global sensor_data

    air_temp_trace = go.Scatter(
        x = sensor_data.created_at,
        y = sensor_data.air_temp,
        name = 'Air Temp',
        mode='lines',
        line = dict(width=4, color=colors['plot'][2])
    )

    layout = go.Layout(
        height='240',
        font = dict(
          color = colors['text'],
          size = 12
        ),
        plot_bgcolor= colors['background'],
        paper_bgcolor= colors['background'],
        title='Air Temp (°F)',
        yaxis=dict(
            side='right',
            dtick=1
        )
    )

    graph_data = [air_temp_trace]

    return go.Figure(data=graph_data, layout=layout)


@app.callback(Output('ec_graph', 'figure'), [Input('interval-component', 'n_intervals')])
def ec_graph(n):
    global sensor_data

    ec_trace = go.Scatter(
        x = sensor_data.created_at,
        y = sensor_data.ec,
        name = 'TDS',
        mode='lines',
        line = dict(width=4, color=colors['plot'][3])
    )

    layout = go.Layout(
        height='240',
        font = dict(
          color = colors['text'],
          size = 12
        ),
        plot_bgcolor= colors['background'],
        paper_bgcolor= colors['background'],
        title='TDS (ppm)',
        yaxis=dict(
            side='right',
            dtick=5
        )
    )

    graph_data = [ec_trace]

    return go.Figure(data=graph_data, layout=layout)


@app.callback(Output('humidity_graph', 'figure'), [Input('interval-component', 'n_intervals')])
def humidity_graph(n):
    global sensor_data

    humidity_trace = go.Scatter(
        x = sensor_data.created_at,
        y = sensor_data.humidity,
        name = 'Humidity',
        mode='lines',
        line = dict(width=4, color=colors['plot'][4])
    )

    layout = go.Layout(
        height='240',
        font = dict(
          color = colors['text'],
          size = 12
        ),
        plot_bgcolor= colors['background'],
        paper_bgcolor= colors['background'],
        title='Humidity',
        yaxis=dict(
            side='right',
            dtick=.05
        )
    )

    graph_data = [humidity_trace]

    return go.Figure(data=graph_data, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
