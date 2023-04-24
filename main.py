from pycbc.waveform import get_td_waveform
from dash import Dash, dcc, html, Input, Output
from callbacks import *
import dash_bootstrap_components as dbc
import pandas
import numpy as np
import plotly.express as px

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
                            id = 'det',
                            options = [
                                {'label': 'H1', 'value': 'H1'},
                                {'label': 'L1', 'value': 'L1'},
                                {'label': 'V1', 'value': 'V1'},
                                {'label': 'K1', 'value': 'K1'}
                            ],
                            multi = True
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
    Input('det', 'value'),
    Input('mass1', 'value'),
    Input('mass2', 'value')
)
def update_figure(det, mass1, mass2):
    hp, _ = get_td_waveform(
        approximant='SEOBNRv4',
        mass1=int(mass1),
        mass2=int(mass2),
        f_lower=15,
        delta_t=1/2048
    )
    fig = px.line(x=np.array(hp.sample_times), y=np.array(hp))
    fig.update_layout(
        title=f'{det}',
        xaxis_title='Time from merger (s)',
        yaxis_title='Strain'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
