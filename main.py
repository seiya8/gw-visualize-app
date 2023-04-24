from pycbc.waveform import get_td_waveform
from pycbc.detector import Detector
from dash import Dash, dcc, html, Input, Output
from callbacks import *
import dash_bootstrap_components as dbc
import pandas
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={'marginLeft': 20, 'marginRight': 20},
    children=[
        html.H1(children='GW Visualization App'),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='three columns',
                    children=[
                        dcc.Markdown("""
                            **Detectors**
                        """),
                        dcc.Dropdown(
                            id = 'dets',
                            options = [
                                {'label': 'H1', 'value': 'H1'},
                                {'label': 'L1', 'value': 'L1'},
                                {'label': 'V1', 'value': 'V1'},
                                {'label': 'K1', 'value': 'K1'}
                            ],
                            multi = True,
                            value = ['H1', 'L1']
                        ),
                    ]
                ),
                html.Div(
                    className='three columns',
                    children=[
                        dcc.Markdown("""
                            **Mass 1**
                        """),
                        dcc.Slider(
                            id='mass1',
                            min=5, max=50, step=1, value=30, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Mass 2**
                        """),
                        dcc.Slider(
                            id='mass2',
                            min=5, max=50, step=1, value=30, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ]
                ),
                html.Div(
                    className='three columns',
                    children=[
                        dcc.Markdown("""
                            **Declination**
                        """),
                        dcc.Slider(
                            id='dec',
                            min=0, max=3.14, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Right Ascension**
                        """),
                        dcc.Slider(
                            id='ra',
                            min=0, max=6.28, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Polarization angle**
                        """),
                        dcc.Slider(
                            id='pol',
                            min=0, max=6.28, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ]
                )
            ]
        ),
        dcc.Graph(
            id='plot'
        )
    ]
)

@app.callback(
    Output('plot', 'figure'),
    Input('dets', 'value'),
    Input('mass1', 'value'),
    Input('mass2', 'value'),
    Input('dec', 'value'),
    Input('ra', 'value'),
    Input('pol', 'value'),
)
def update_figure(dets, mass1, mass2, dec, ra, pol):
    hp, hc = get_td_waveform(
        approximant='SEOBNRv4',
        mass1=int(mass1),
        mass2=int(mass2),
        f_lower=10,
        delta_t=1/2048
    )
    wave_dict = {det: Detector(det).project_wave(hp, hc, ra, dec, pol) for det in ('H1', 'L1', 'V1', 'K1')}

    wave_plots = []
    for det in dets:
        wave_plots.append(
            go.Scatter(
                x=np.array(wave_dict[det].sample_times),
                y=np.array(wave_dict[det]),
                name=det
            )
        )
    fig = go.Figure(wave_plots)
    fig.update_layout(
        xaxis_title='Time from merger (s)',
        yaxis_title='Strain'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
