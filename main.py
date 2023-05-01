import sys
from pycbc.coordinates import spherical_to_cartesian
from pycbc.waveform import get_td_waveform
from pycbc.detector import Detector
from dash import Dash, dcc, html, Input, Output
import dash_auth
from callbacks import *
import dash_bootstrap_components as dbc
import pandas
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(app, {sys.argv[1]: sys.argv[2]})
app.title = 'GW Visualization App'
app.layout = html.Div(
    style={'marginLeft': 20, 'marginRight': 20},
    children=[
        html.H1(children='GW Visualization App'),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='two columns',
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
                    className='two columns',
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
                    className='two columns',
                    children=[
                        dcc.Markdown("""
                            **Spin1 magnitude**
                        """),
                        dcc.Slider(
                            id='spin1m',
                            min=0, max=1, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Spin1 azimuthal angle**
                        """),
                        dcc.Slider(
                            id='spin1az',
                            min=0, max=6.28, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Spin1 polar angle**
                        """),
                        dcc.Slider(
                            id='spin1po',
                            min=0, max=3.14, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ]
                ),
                html.Div(
                    className='two columns',
                    children=[
                        dcc.Markdown("""
                            **Spin2 magnitude**
                        """),
                        dcc.Slider(
                            id='spin2m',
                            min=0, max=1, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Spin2 azimuthal angle**
                        """),
                        dcc.Slider(
                            id='spin2az',
                            min=0, max=6.28, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        ),
                        dcc.Markdown("""
                            **Spin2 polar angle**
                        """),
                        dcc.Slider(
                            id='spin2po',
                            min=0, max=3.14, step=0.01, value=0, marks=None,
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ]
                ),
                html.Div(
                    className='two columns',
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
        html.Br(),
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
    Input('spin1m', 'value'),
    Input('spin1az', 'value'),
    Input('spin1po', 'value'),
    Input('spin2m', 'value'),
    Input('spin2az', 'value'),
    Input('spin2po', 'value'),
    Input('dec', 'value'),
    Input('ra', 'value'),
    Input('pol', 'value'),
)
def update_figure(dets, mass1, mass2, spin1m, spin1az, spin1po, spin2m, spin2az, spin2po, dec, ra, pol):
    spin1x, spin1y, spin1z = spherical_to_cartesian(spin1m, spin1az, spin1po)
    spin2x, spin2y, spin2z = spherical_to_cartesian(spin2m, spin2az, spin2po)
    hp, hc = get_td_waveform(
        approximant='IMRPhenomXPHM',
        mass1=int(mass1),
        mass2=int(mass2),
        spin1x=spin1x,
        spin1y=spin1y,
        spin1z=spin1z,
        spin2x=spin2x,
        spin2y=spin2y,
        spin2z=spin2z,
        f_lower=10,
        delta_t=1/2048
    )
    det_color_dict = {'H1': '#4C78A8', 'L1': '#F58518', 'V1': '#E45756', 'K1': '#72B7B2'}
    wave_plots = []
    for det in dets:
        wave = Detector(det).project_wave(hp, hc, ra, dec, pol)
        wave_plots.append(
            go.Scatter(
                x=np.array(wave.sample_times),
                y=np.array(wave),
                name=det,
                marker=dict(color=det_color_dict[det])
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
