import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


app = Dash(__name__)

colors = {
    'text': '#148974',
    'lines': '#147852'
}

data = (
    pd
    .read_csv('data/avocado.csv')
    .assign(Date=lambda data: pd.to_datetime(data['Date'],
                                             format='%Y-%m-%d'))
    .sort_values(['Date'])
)
regions = np.sort(data['region'].unique())
avocado_types = np.sort(data['type'].unique())

average_price_fig = px.line(data,
                            x='Date',
                            y='AveragePrice',
                            range_y=[0,3.0],
                            title='Average Price')
total_volume_fig = px.line(data,
                           x='Date',
                           y='Total Volume',
                           title='Total Sold')

def style_figure(fig):
    return (
        fig
        .update_layout(font_color=colors['text'])
        .update_traces(line_color=colors['lines'])
    )

def build_dashboard(data):
    layout = html.Div(
        children=[
            html.Div(
                id='header',
                children=[
                    html.H1(
                        children='Avocado Analytics',
                        style={'textAlign': 'center'}),
                    html.P(children='''
                            A simple viz dashboard powered by Dash, a love
                            child of Python and ReactJS.
                            ''')
                ]
            ),
            html.Div(
                id='filters',
                children=[
                    html.Div(
                        className='filter-section',
                        children=[
                            html.Div(children='Region',
                                     className='filter-title'),
                            dcc.Dropdown(
                                id='region-filter',
                                options=regions,
                                value='TotalUS',
                                searchable=False,
                                clearable=False,
                                className='dropdown'
                            ),
                        ]),
                    html.Div(
                        className='filter-section',
                        children=[
                            html.Div(children='Avocado Type',
                                     className='filter-title'),
                            dcc.Dropdown(
                                id='type-filter',
                                options=avocado_types,
                                value='organic',
                                searchable=False,
                                clearable=False,
                                className='dropdown'
                            ),
                        ])
                ]),
            html.Div(
                id='graphs',
                children=[
                    dcc.Graph(
                        id='average-price',
                        figure=style_figure(average_price_fig)),
                    dcc.Graph(
                        id='total-volume',
                        figure=style_figure(total_volume_fig))
                ])
        ])
    return layout


@app.callback(
    Output('average-price', 'figure'),
    Output('total-volume', 'figure'),
    Input('region-filter', 'value'),
    Input('type-filter', 'value')
)
def update_graphs(region_filter, type_filter):
    filtered_data = data.query(
        'region == @region_filter and type == @type_filter'
    )
    average_price_fig = px.line(filtered_data,
                                x='Date',
                                y='AveragePrice',
                                range_y=[0,3.0],
                                title='Average Price')
    total_volume_fig = px.line(filtered_data,
                               x='Date',
                               y='Total Volume',
                               title='Total Sold')
    return style_figure(average_price_fig), style_figure(total_volume_fig)


app.layout = build_dashboard(data)


if __name__ == '__main__':
    app.run_server('0.0.0.0', debug=True)
