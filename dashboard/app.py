# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from os import name
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_html_components.Div import Div
from dash_html_components.Span import Span
from dash_html_components.Title import Title
import dash_table
from numpy.core.numeric import NaN
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from urllib.request import urlopen
import json
from datetime import date, datetime, timedelta
import math
import re

from plotly.subplots import make_subplots

external_stylesheets = [dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.15.3/css/all.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True, title="COVID-19 Statistics Brazil", update_title='Loading...')

wdir = os.getcwd()
wdir = re.sub(r'dashboard/', '', wdir)
wdir = re.sub(r'\\', '/', wdir)

subregions_metadata = pd.read_csv(f'{wdir}/data/filtered_data/SUBREGION_METADATA.csv')

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='cases', children=[
        dcc.Tab(label='Cases', value='cases'),
        dcc.Tab(label='Vaccinations', value='vaccinations'),
        # dcc.Tab(label='Predictions', value='predictions'),
        # dcc.Tab(label='Clustering', value='clustering'),
        # dcc.Tab(label='Hospitalisations', value='hospitalisations'),
        # dcc.Tab(label='Tests', value='tests'),
        # dcc.Tab(label='Mobility', value='mobility'),
        # dcc.Tab(label='About', value='about'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'cases':
        return html.Div([
            dcc.Dropdown(
                id='dropdown-region',
                options=[{'label': subregion, 'value': subregion} for subregion in subregions_metadata['SUBREGION']],
                value='Araraquara',
                clearable=False,
                style={
                    "width": "200px",
                    "margin": "auto",
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ], 
                id='general-info-div',
                style={
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ], id='active-div'),

            html.Div([

            ], id='cases-div'),

            html.Div([

            ], id='recovered-div'),

            html.Div([

            ], id='deaths-div'),
        ])
    elif tab == 'vaccinations':
        return html.Div([
            dcc.Dropdown(
                id='dropdown-region',
                options=[{'label': subregion, 'value': subregion} for subregion in subregions_metadata['SUBREGION']],
                value='Araraquara',
                clearable=False,
                style={
                    "width": "200px",
                    "margin": "auto",
                    "marginTop": "2rem"
                }
            ),

            html.Div([
            ], 
                id='vaccinations-info-div',
                style={
                    "marginTop": "2rem"
                }
            ),

            html.Div([

            ], id='first-dose-div'),

            html.Div([

            ], id='second-dose-div')
        ])
    # elif tab == 'predictions':
    #     return html.Div([
    #         dcc.Dropdown(
    #             id='predictions-province',
    #             options=[
    #                 {'label': 'Belgium', 'value': 'Belgium'},
    #                 {'label': 'Antwerpen', 'value': 'Antwerpen'},
    #                 {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
    #                 {'label': 'Brussel', 'value': 'Brussels'},
    #                 {'label': 'Henegouwen', 'value': 'Hainaut'},
    #                 {'label': 'Luik', 'value': 'Liège'},
    #                 {'label': 'Limburg', 'value': 'Limburg'},
    #                 {'label': 'Luxemburg', 'value': 'Luxembourg'},
    #                 {'label': 'Namen', 'value': 'Namur'},
    #                 {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
    #                 {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
    #                 {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
    #             ],
    #             value='Belgium',
    #             clearable=False,
    #             style={
    #                 "width": "200px",
    #                 "margin": "auto",
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div([

    #         ],
    #             id="predictions-info-div",
    #             style={
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div(
    #             id="predictions-div",
    #         ),
    #     ])
    # elif tab == 'clustering':
    #     df = pd.read_csv(f'{wdir}data/resulted_data/kmeans/CLUSTER_PROVINCES.csv')
    #     df = df.rename(columns={"PROVINCE": "Provincie", "INFECTION_RATE": "Infectie graad", "HOSPITALISATION_RATE": "Hospitalisatie graad", "TEST_POS_PERCENTAGE": "Percentage positieve testen", "CLUSTER": "Cluster"})
    #     df = df.astype({"Cluster": "int32"})

    #     df["Cluster"] += 1
    #     df = df.round(2)
    #     with open('geojson.json', encoding="utf-8") as file:
    #         be = json.load(file)

    #     be = rewind(be, rfc7946=False)

    #     cluster_be = px.choropleth(df, geojson=be, locations="Provincie", featureidkey="properties.NameDUT", projection="mercator", color="Cluster", hover_data=["Provincie", "Infectie graad", "Hospitalisatie graad", "Percentage positieve testen", "Cluster"], height=800, color_continuous_scale="ylorrd")

    #     cluster_be.update_geos(fitbounds="locations", visible=False)
    #     cluster_be.update_layout(dragmode=False, coloraxis_showscale=False)

    #     cluster_metadata = pd.read_csv(f'{wdir}data/resulted_data/kmeans/CLUSTER_METADATA.csv')
    #     cluster_metadata = round(cluster_metadata, 2)
    #     cluster_metadata = cluster_metadata.rename(columns={"CLUSTER": "Cluster", "INFECTION_RATE": "Infection rate", "HOSPITALISATION_RATE": "Hospitalisation rate", "TEST_POS_PERCENTAGE": "Percentage of positive tests"})

    #     return html.Div([

    #         dbc.Row([
    #             dbc.Col([
    #                 dcc.Graph(
    #                     figure=cluster_be,
    #                     config={'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'zoomInGeo', 'zoomOutGeo']}
    #                 ),
    #             ],
    #                 className="p-0"
    #             ),

    #             dbc.Col([
    #                 html.Div([
    #                     html.Div([
    #                         html.H3('Clustering results', className="h3"),
    #                         html.Article([
    #                             html.P('The map on the left shows Belgium and its provinces.', style={'margin': '5px', 'marginLeft': '0px'}),
    #                             html.P('The provinces are color-coded according to their cluster.', style={'margin': '5px', 'marginLeft': '0px'}),
    #                             html.P('Hover over a specific province to see its statistics.', style={'margin': '5px', 'marginLeft': '0px'}),
    #                             html.P('In the table below the values of the representatives of each cluster are presented.', style={'margin': '5px', 'marginBottom': '10px', 'marginLeft': '0px'}),
    #                         ])
    #                     ]),
    #                     dbc.Table.from_dataframe(cluster_metadata, striped=True, bordered=True, hover=True)
    #                 ]),
    #             ], 
    #                 className="d-flex align-items-center justify-content-center p-0"
    #             ),
    #         ],
    #             className="m-0"
    #         ),
    #     ],
    #         style={
    #             "marginTop": "2em"
    #         }
    #     )
    # elif tab == 'hospitalisations':
    #     return html.Div([
    #         dcc.Dropdown(
    #             id='predictions-province',
    #             options=[
    #                 {'label': 'Belgium', 'value': 'Belgium'},
    #                 {'label': 'Antwerpen', 'value': 'Antwerpen'},
    #                 {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
    #                 {'label': 'Brussel', 'value': 'Brussels'},
    #                 {'label': 'Henegouwen', 'value': 'Hainaut'},
    #                 {'label': 'Luik', 'value': 'Liège'},
    #                 {'label': 'Limburg', 'value': 'Limburg'},
    #                 {'label': 'Luxemburg', 'value': 'Luxembourg'},
    #                 {'label': 'Namen', 'value': 'Namur'},
    #                 {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
    #                 {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
    #                 {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
    #             ],
    #             value='Belgium',
    #             clearable=False,
    #             style={
    #                 "width": "200px",
    #                 "margin": "auto",
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div([

    #         ],
    #             id="hospitalisations-info-div",
    #             style={
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div(
    #             id="hospitalisations-div"
    #         ),
    #     ])
    # elif tab == 'tests':
    #     return html.Div([
    #         dcc.Dropdown(
    #             id='predictions-province',
    #             options=[
    #                 {'label': 'Belgium', 'value': 'Belgium'},
    #                 {'label': 'Antwerpen', 'value': 'Antwerpen'},
    #                 {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
    #                 {'label': 'Brussel', 'value': 'Brussels'},
    #                 {'label': 'Henegouwen', 'value': 'Hainaut'},
    #                 {'label': 'Luik', 'value': 'Liège'},
    #                 {'label': 'Limburg', 'value': 'Limburg'},
    #                 {'label': 'Luxemburg', 'value': 'Luxembourg'},
    #                 {'label': 'Namen', 'value': 'Namur'},
    #                 {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
    #                 {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
    #                 {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
    #             ],
    #             value='Belgium',
    #             clearable=False,
    #             style={
    #                 "width": "200px",
    #                 "margin": "auto",
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div([

    #         ],
    #             id="tests-info-div",
    #             style={
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div(
    #             id="tests-div"
    #         ),
    #     ])
    # elif tab == 'mobility':
    #     return html.Div([
    #         dbc.Row([
    #             dbc.Col(
    #                 dcc.Dropdown(
    #                     id='predictions-province',
    #                     options=[
    #                         {'label': 'Belgium', 'value': 'Belgium'},
    #                         {'label': 'Antwerpen', 'value': 'Antwerpen'},
    #                         {'label': 'Waals-Brabant', 'value': 'BrabantWallon'},
    #                         {'label': 'Brussel', 'value': 'Brussels'},
    #                         {'label': 'Henegouwen', 'value': 'Hainaut'},
    #                         {'label': 'Luik', 'value': 'Liège'},
    #                         {'label': 'Limburg', 'value': 'Limburg'},
    #                         {'label': 'Luxemburg', 'value': 'Luxembourg'},
    #                         {'label': 'Namen', 'value': 'Namur'},
    #                         {'label': 'Oost-Vlaanderen', 'value': 'OostVlaanderen'},
    #                         {'label': 'Vlaams-Brabant', 'value': 'VlaamsBrabant'},
    #                         {'label': 'West-Vlaanderen', 'value': 'WestVlaanderen'},
    #                     ],
    #                     value='Belgium',
    #                     clearable=False,
    #                     style={
    #                         "width": "200px",
    #                         "margin": "auto",
    #                     }
    #                 ), width=2,
    #             ),

    #             dbc.Col(
    #                 html.Div([
    #                     dbc.Button(
    #                         "More information about this page",
    #                         id="collapse-mobility-info",
    #                         color="primary",
    #                         n_clicks=0
    #                     ),

    #                     dbc.Collapse(
    #                         dbc.Card(
    #                             dbc.CardBody(
    #                                 [
    #                                     html.P(["The numbers on this page represent a percentage change for different sectors."], style={'margin': '5px', 'marginLeft': '0px', 'marginRight': '0px'}),
    #                                     html.P(["This percentage change shows the change of mobility for the sectors comparing it to the average before the pandemic."], style={'margin': '5px', 'marginLeft': '0px', 'marginRight': '0px'})
    #                                 ]
    #                             )
    #                         ),
    #                         id="mobility-info-collapse",
    #                         is_open=False,
    #                     )
    #                 ]), width=4,
    #             )
    #         ], style={"marginTop": "2rem", "marginLeft": "0", "marginRight": "0", "justifyContent": "center"}),

    #         html.Div([

    #         ],
    #             id="mobility-info-div",
    #             style={
    #                 "marginTop": "2rem"
    #             }
    #         ),

    #         html.Div(
    #             id="mobility-div"
    #         ),
    #     ])
    # elif tab == 'about':
    #     return html.Div([
    #         html.Div([
    #             html.Div([
    #                 html.H5([
    #                     "About"
    #                 ]),
    #                 html.P(["This dashboard is a result from a research done in collaboration with São Paulo State University (UNESP)"], style={'margin': '5px', 'marginLeft': '0px', 'marginRight': '0px'}),
    #                 html.P([
    #                     "Some information about the data can be found on this page, for a more detailed explication about our methodologies please refer to the paper of the research. Download the paper ",
    #                     html.A(["here"], href=f"./assets/AssessingCovid19CasesBelgium.pdf", download=True),
    #                     "."], style={'margin': '5px', 'marginLeft': '0px', 'marginRight': '0px'})
    #             ]),

    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Div([
    #                         dbc.Button([
    #                             "More information about the cases"
    #                         ],
    #                         id="collapse-cases-info",
    #                         color="primary",
    #                         n_clicks=0
    #                         ),
    #                         dbc.Collapse([
    #                             dbc.Card([
    #                                 dbc.CardBody([
    #                                     html.Article([
    #                                         html.H5([
    #                                             "Recovered cases"
    #                                         ]),
    #                                         html.P([
    #                                             "Since the Belgian government doesn't provide data about the recovered cases, the recovered cases found in this dashboard are estimated. The way we estimated these is the following: the recovered cases of today are the new cases of 14 days ago. Taken that infected people will only recover or die after exactly 14 days."
    #                                         ]),
    #                                         html.H5([
    #                                             "Deaths"
    #                                         ]),
    #                                         html.P([
    #                                             "The Belgian government doesn't provide information about the deaths for each province, because of that information about the deaths for each province aren't provided here either."
    #                                         ]),
    #                                         html.H5([
    #                                             "Active cases"
    #                                         ]),
    #                                         html.P([
    #                                             "The government doesn't provide data about active cases, so the cases found on this website are estimated aswell. The way of estimation is the following: the active infections on a specific day are equal to the amount of cumulative cases - the amount of cumulative recovered - the amount of cumulative deaths."
    #                                         ], style={"marginBottom": "0"})
    #                                     ])
    #                                 ])
    #                             ])
    #                         ],
    #                         id="cases-info-collapse",
    #                         is_open=False
    #                         )
    #                     ])
    #                 ]),
    #             ], style={"marginBottom": "2em"}),

    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Div([
    #                         dbc.Button([
    #                             "More information about the predictions"
    #                         ],
    #                         id="collapse-predictions-info",
    #                         color="primary",
    #                         n_clicks=0
    #                         ),
    #                         dbc.Collapse([
    #                             dbc.Card([
    #                                 dbc.CardBody([
    #                                     html.Article([
    #                                         html.H5([
    #                                             "Predictions"
    #                                         ]),
    #                                         html.P([
    #                                             "The predictions are made using a neural network together with a SIR model. The neural network takes 31 days to train itself and predicts the next 14 days."
    #                                         ]),
    #                                         html.H5([
    #                                             "Reproduction factor"
    #                                         ]),
    #                                         html.P([
    #                                             "The reproduction factor shows the average of how many extra infections an infected person will cause."
    #                                         ], style={"marginBottom": "0"})
    #                                     ])
    #                                 ])
    #                             ])
    #                         ],
    #                         id="predictions-info-collapse",
    #                         is_open=False
    #                         )
    #                     ])
    #                 ]),
    #             ], style={"marginBottom": "2em"}),

    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Div([
    #                         dbc.Button([
    #                             "More information about the clustering"
    #                         ],
    #                         id="collapse-clustering-info",
    #                         color="primary",
    #                         n_clicks=0
    #                         ),
    #                         dbc.Collapse([
    #                             dbc.Card([
    #                                 dbc.CardBody([
    #                                     html.Article([
    #                                         html.H5([
    #                                             "Clustering"
    #                                         ]),
    #                                         html.P([
    #                                             "The clustering algorithm used is the Kmeans algorithm."
    #                                         ], style={"marginBottom": "0"}),
    #                                     ])
    #                                 ])
    #                             ])
    #                         ],
    #                         id="clustering-info-collapse",
    #                         is_open=False
    #                         )
    #                     ])
    #                 ]),
    #             ], style={"marginBottom": "1em"}),

    #             html.Div([
    #                 html.H5([
    #                     "Sources"
    #                 ]),
    #                 html.P(["All the COVID related data, used in this dashboard can be found ", html.A(["here"], href="https://epistat.wiv-isp.be/covid/"), "."], style={'margin': '5px', 'marginLeft': '0px', 'marginRight': '0px'}),
    #                 html.P(["The mobility data can be found ", html.A(["here"], href="https://www.google.com/covid19/mobility/"), "."], style={'margin': '5px', 'marginLeft': '0px', 'marginRight': '0px'})
    #             ]),
    #         ],
    #             id="about-info-div",
    #             style={
    #                 "display": "flex",
    #                 "flex-direction": "column",
    #                 "margin": "auto",
    #                 "width": "80%"
    #             }
    #         ),
    #     ], style={"marginTop": "2rem",})


##########################
###                    ###
### CALLBACKS FOR TABS ###
###                    ###
##########################


@app.callback(
    Output('general-info-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_general_info(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')

    active_infections = df['ACTIVE_CASES'].iloc[-1]
    cumulative_cases = df['CUMULATIVE_CASES'].iloc[-1]
    cumulative_recovered = df['CUMULATIVE_RECOVERED'].iloc[-1]
    cumulative_deaths = df['CUMULATIVE_DEATHS'].iloc[-1]

    div = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Active cases'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-head-side-cough",
                            style={
                                "fontSize": "2rem",
                                "color": "CornflowerBlue"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(active_infections, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid CornflowerBlue",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total cases'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-viruses",
                            style={
                                "fontSize": "2rem",
                                "color": "orange"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(cumulative_cases, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid orange",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total recovered'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-virus-slash",
                            style={
                                "fontSize": "2rem",
                                "color": "green"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(cumulative_recovered, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid green",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Total deaths'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-cross",
                            style={
                                "fontSize": "2rem",
                                "color": "red"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(cumulative_deaths, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid red",
                }), 
                width=2
            ),
        ], className="justify-content-center m-0")
    ])

    return [div]

@app.callback(
    Output('vaccinations-info-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_general_info(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')

    new_first_doses = df['NEW_FIRST_DOSES'].iloc[-1]
    cumulative_first_doses = df['CUMULATIVE_FIRST_DOSES'].iloc[-1]
    new_second_doses = df['NEW_SECOND_DOSES'].iloc[-1]
    cumulative_second_doses = df['CUMULATIVE_SECOND_DOSES'].iloc[-1]

    div = html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['First doses'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-syringe",
                            style={
                                "fontSize": "2rem",
                                "color": "CornflowerBlue"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(cumulative_first_doses, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid CornflowerBlue",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['New first doses'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-syringe",
                            style={
                                "fontSize": "2rem",
                                "color": "orange"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(new_first_doses, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid orange",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['Second doses'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-syringe",
                            style={
                                "fontSize": "2rem",
                                "color": "green"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(cumulative_second_doses, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid green",
                }), 
                width=2
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.P(
                            ['New second doses'],
                            style={
                                "marginBottom": "0"
                            }
                        ),
                        html.I(
                            className="fas fa-syringe",
                            style={
                                "fontSize": "2rem",
                                "color": "red"
                            }
                        )
                    ], style={
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }),
                    dbc.CardBody([
                        html.H5(f'{region}', className='card-title'),
                        html.P(new_second_doses, className='card-text')
                    ])
                ], style={
                    "borderLeft": "5px solid red",
                }), 
                width=2
            ),
        ], className="justify-content-center m-0")
    ])

    return [div]

# @app.callback(
#     Output('predictions-info-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_predictions_info(province):
#     df = pd.read_csv(f'{wdir}data/resulted_data/neural_network/{province}/pred_all.csv')
#     df["Data"] = pd.to_datetime(df["Data"]).dt.date
#     days_trained = df[ df['Used in Train'] == True]
#     days_trained = len(days_trained)
#     days_predicted = df[ df['Used in Train'] == False]
#     days_predicted = len(days_predicted)
#     Rt = round(df[df['Data'] == date.today()]['Rt'], 2)

#     div = html.Div([
#         dbc.Row([
#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Days trained'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-dumbbell",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "CornflowerBlue"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(days_trained, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid CornflowerBlue",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Days predicted'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-chart-line",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "orange"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(days_predicted, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid orange",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Reproduction factor'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-people-arrows",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "crimson"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(Rt, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid crimson",
#                 }), 
#                 width=2
#             ),
#         ], className="justify-content-center m-0")
#     ])

#     return [div]

# @app.callback(
#     Output('hospitalisations-info-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_hospitalisations_info(province):
#     df = pd.read_csv(f'{wdir}data/filtered_data/HOSP.csv')
#     df = df[ df['REGION'] == province ]

#     total_in_icu = df['TOTAL_IN_ICU'].iloc[-1]
#     new_in = df['NEW_IN'].iloc[-1]
#     total_hospitalisations = df["NEW_IN"].sum()

#     div = html.Div([
#         dbc.Row([
#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Total in ICU'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-procedures",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "CornflowerBlue"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(total_in_icu, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid CornflowerBlue",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['New Hospitalisations'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-hospital-user",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "green"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(new_in, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid green",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Total Hospitalisations'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-hospital-user",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "darkseagreen"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(total_hospitalisations, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid darkseagreen",
#                 }), 
#                 width=2
#             ),
#         ], className="justify-content-center m-0")
#     ])

#     return [div]

# @app.callback(
#     Output('tests-info-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_tests_info(province):
#     df = pd.read_csv(f'{wdir}data/filtered_data/TESTS.csv')
#     df = df[ df['REGION'] == province ]

#     total_tests = df['TESTS_ALL'].sum()
#     total_positive_tests = df['TESTS_ALL_POS'].sum()
#     new_tests = df['TESTS_ALL'].iloc[-1]
#     new_positive = df['TESTS_ALL_POS'].iloc[-1]

#     div = html.Div([
#         dbc.Row([
#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['New tests'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-vials",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "CornflowerBlue"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(new_tests, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid CornflowerBlue",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Total tests'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-vials",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "DarkCyan"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(total_tests, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid DarkCyan",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['New positive tests'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-plus",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "green"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(new_positive, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid green",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Total positive tests'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-plus",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "darkseagreen"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(total_positive_tests, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid darkseagreen",
#                 }), 
#                 width=2
#             ),
#         ], className="justify-content-center m-0")
#     ])

#     return [div]

# @app.callback(
#     Output('mobility-info-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_tests_info(province):
#     df = pd.read_csv(f'{wdir}data/filtered_data/MOBILITY.csv')
    
#     if province == "Belgium":
#         df = df[ df["country_region"] == "Belgium"]
#         mask = pd.isnull(df["sub_region_2"])
#         df = df[mask]
#         mask = pd.isnull(df["sub_region_1"])
#         df = df[mask]
#     elif province == "Brussels":
#         df = df[ df["sub_region_1"] == "Brussels"]
#     else:
#         df = df[ df["sub_region_2"] == province]


#     retail_and_recreation = df["retail_and_recreation_percent_change_from_baseline"].iloc[-1]
#     grocery_and_pharmacy = df["grocery_and_pharmacy_percent_change_from_baseline"].iloc[-1]
#     parks = df["parks_percent_change_from_baseline"].iloc[-1]
#     transit = df["transit_stations_percent_change_from_baseline"].iloc[-1]
#     workplaces = df["workplaces_percent_change_from_baseline"].iloc[-1]
#     residential = df["residential_percent_change_from_baseline"].iloc[-1]

#     div = html.Div([
#         dbc.Row([
#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Retail and recreation'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-shopping-bag",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "CornflowerBlue"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(retail_and_recreation, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid CornflowerBlue",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Grocery and pharmacy'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-store",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "orange"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(grocery_and_pharmacy, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid orange",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Parks'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-umbrella-beach",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "green"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(parks, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid green",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Transit'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-train",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "red"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(transit, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid red",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Workplaces'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-briefcase",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "darkviolet"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(workplaces, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid darkviolet",
#                 }), 
#                 width=2
#             ),

#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader([
#                         html.P(
#                             ['Residential'],
#                             style={
#                                 "marginBottom": "0"
#                             }
#                         ),
#                         html.I(
#                             className="fas fa-home",
#                             style={
#                                 "fontSize": "2rem",
#                                 "color": "deeppink"
#                             }
#                         )
#                     ], style={
#                         "display": "flex",
#                         "flexDirection": "row",
#                         "justifyContent": "space-between",
#                         "alignItems": "center"
#                     }),
#                     dbc.CardBody([
#                         html.H5(f'{province}', className='card-title'),
#                         html.P(residential, className='card-text')
#                     ])
#                 ], style={
#                     "borderLeft": "5px solid deeppink",
#                 }), 
#                 width=2
#             ),
#         ], className="justify-content-center m-0")
#     ])

#     return [div]


###############################
###                         ###
### CALLBACKS FOR COLLAPSES ###
###                         ###
###############################


# @app.callback(
#     Output("mobility-info-collapse", "is_open"),
#     [Input("collapse-mobility-info", "n_clicks")],
#     [State("mobility-info-collapse", "is_open")]
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("cases-info-collapse", "is_open"),
#     [Input("collapse-cases-info", "n_clicks")],
#     [State("cases-info-collapse", "is_open")]
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("predictions-info-collapse", "is_open"),
#     [Input("collapse-predictions-info", "n_clicks")],
#     [State("predictions-info-collapse", "is_open")]
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("clustering-info-collapse", "is_open"),
#     [Input("collapse-clustering-info", "n_clicks")],
#     [State("clustering-info-collapse", "is_open")]
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


###############################
###                         ###
### CALLBACKS FOR CASES TAB ###
###                         ###
###############################


@app.callback(
    Output('active-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_active(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')

    fig = make_subplots(
        rows=1,
        cols=1,
        subplot_titles=(
            'Active infections',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['ACTIVE_CASES'],
            mode='lines',
            line=dict(color='CornflowerBlue'),
        ),
        row=1, col=1
    )

    fig.update_layout(hovermode="x unified")

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="Active infections", row=1, col=1)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('cases-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_cases(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'New infections',
            'Total infections'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_CASES'],
            mode='lines',
            line=dict(color='orange'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_CASES'],
            mode='lines',
            line=dict(color='orange'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="New infections", row=1, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Total infections", row=1, col=2)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('vaccinations-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_vaccinations(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Partly vaccinated',
            'Vaccinated'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['PARTLY_VACCINATED'],
            mode='lines',
            line=dict(color='darkviolet'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['VACCINATED'],
            mode='lines',
            line=dict(color='deeppink'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="1st dose vaccinated", row=1, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Vaccinated", row=1, col=2)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('recovered-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_recovered(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')
    
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'New recoveries',
            'Total recovered'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_RECOVERED'],
            mode='lines',
            line=dict(color='green'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_RECOVERED'],
            mode='lines',
            line=dict(color='green'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="New recoveries", row=1, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Total recoveries", row=1, col=2)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('deaths-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_deaths(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'New deaths',
            'Total deaths'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_DEATHS'],
            mode='lines',
            line=dict(color='red'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_DEATHS'],
            mode='lines',
            line=dict(color='red'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="New deaths", row=1, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Total deaths", row=1, col=2)

    return [dcc.Graph(figure=fig)]


######################################
###                                ###
### CALLBACKS FOR VACCINATIONS TAB ###
###                                ###
######################################


@app.callback(
    Output('first-dose-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_first_doses(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')
    df = df[ df["CUMULATIVE_FIRST_DOSES"] > 0 ]

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'New first doses',
            'Total first doses'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_FIRST_DOSES'],
            mode='lines',
            line=dict(color='orange'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_FIRST_DOSES'],
            mode='lines',
            line=dict(color='CornflowerBlue'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="New first doses", row=1, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Total first doses", row=1, col=2)

    return [dcc.Graph(figure=fig)]

@app.callback(
    Output('second-dose-div', 'children'),
    Input('dropdown-region', 'value')
)
def update_region_second_doses(region):
    df = pd.read_csv(f'{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv')
    df = df[ df["CUMULATIVE_SECOND_DOSES"] > 0 ]
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'New second doses',
            'Total second doses'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['NEW_SECOND_DOSES'],
            mode='lines',
            line=dict(color='red'),
            name=""
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['DATE'], 
            y=df['CUMULATIVE_SECOND_DOSES'],
            mode='lines',
            line=dict(color='green'),
            name=""
        ),
        row=1, col=2
    )

    fig.update_layout(hovermode="x unified", showlegend=False)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="New second doses", row=1, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Total second doses", row=1, col=2)

    return [dcc.Graph(figure=fig)]


#####################################
###                               ###
### CALLBACKS FOR PREDICTIONS TAB ###
###                               ###
#####################################


# @app.callback(
#     Output('predictions-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_predictions(province):
#     df = pd.read_csv(f'{wdir}data/resulted_data/neural_network/{province}/pred_all.csv')
#     df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%Y-%m-%d')
#     last_training_day = df[ df['Used in Train'] == True].iloc[-1]['Data']
#     last_training_day = datetime.strptime(last_training_day, '%Y-%m-%d')
#     last_training_day_epoch = last_training_day.timestamp()*1000
#     first_training_day = df[ df['Used in Train'] == True].iloc[0]['Data']
#     first_training_day = datetime.strptime(first_training_day, '%Y-%m-%d')

#     test_df = pd.read_csv(f'{wdir}data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv')
#     test_df = test_df[ test_df["REGION"] == province ]
#     test_df["DATE"] = pd.to_datetime(test_df["DATE"])
#     test_df = test_df[ test_df["DATE"] >= first_training_day]
#     test_df = test_df[ test_df["DATE"] <= last_training_day]

#     fig1 = make_subplots(
#         rows=1,
#         cols=2,
#         subplot_titles=(
#             'Active infections',
#             'Total recovered',
#         )
#     )

#     fig1.add_trace(
#         go.Scatter(
#             x=df['Data'], 
#             y=df['Infected'],
#             mode='lines',
#             line=dict(color='CornflowerBlue'),
#             name="Predicted"
#         ),
#         row=1, col=1
#     )

#     fig1.add_trace(
#         go.Scatter(
#             x=test_df["DATE"],
#             y=test_df["ACTIVE_CASES"],
#             mode='lines',
#             line=dict(color='black', dash='dot'),
#             name="Measured"
#         ),
#         row=1, col=1
#     )

#     fig1.add_trace(
#         go.Scatter(
#             x=df['Data'], 
#             y=df['Recovered'],
#             mode='lines',
#             line=dict(color='Green'),
#             name="Predicted"
#         ),
#         row=1, col=2
#     )

#     if province == "Belgium":
#         fig1.add_trace(
#             go.Scatter(
#                 x=test_df["DATE"],
#                 y=test_df["CUMULATIVE_RECOVERED"] + test_df["CUMULATIVE_DEATHS"],
#                 mode='lines',
#                 line=dict(color='black', dash='dot'),
#                 name="Measured"
#             ),
#             row=1, col=2
#         )
#     else:
#         fig1.add_trace(
#             go.Scatter(
#                 x=test_df["DATE"],
#                 y=test_df["CUMULATIVE_RECOVERED"],
#                 mode='lines',
#                 line=dict(color='black', dash='dot'),
#                 name="Measured"
#             ),
#             row=1, col=2
#         )

#     fig1.add_vline(x=last_training_day_epoch, line_dash="dash", annotation_text="End of training", annotation_position="bottom right", annotation_font_size=16)

#     fig2 = make_subplots(
#         rows=1,
#         cols=1,
#         subplot_titles=(
#             'Reproduction factor',
#         )
#     )

#     fig2.add_trace(
#         go.Scatter(
#             x=df['Data'], 
#             y=df['Rt'],
#             mode='lines',
#             line=dict(color='Crimson'),
#         ),
#         row=1, col=1
#     )

#     fig2.add_vline(x=last_training_day_epoch, line_dash="dash", annotation_text="End of training", annotation_position="bottom right", annotation_font_size=16)

#     fig1.update_layout(hovermode='x unified', showlegend=False)
#     fig2.update_layout(hovermode='x unified')

#     fig1.update_xaxes(title_text="Date", row=1, col=1)
#     fig1.update_yaxes(title_text="Active infections", row=1, col=1)
#     fig1.update_xaxes(title_text="Date", row=1, col=2)
#     fig1.update_yaxes(title_text="Total recovered", row=1, col=2)

#     fig2.update_xaxes(title_text="Date", row=1, col=1)
#     fig2.update_yaxes(title_text="Reproduction factor", row=1, col=1)

#     return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


##########################################
###                                    ###
### CALLBACKS FOR HOSPITALISATIONS TAB ###
###                                    ###
##########################################


# @app.callback(
#     Output('hospitalisations-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_hospitalisations(province):
#     df = pd.read_csv(f'{wdir}data/filtered_data/HOSP.csv')
#     df = df[ df["REGION"] == province ]

#     fig = make_subplots(
#         rows=1,
#         cols=2,
#         subplot_titles=(
#             'Total in ICU',
#             'New hospitalisations',
#         )
#     )

#     fig.add_trace(
#         go.Scatter(
#             x=df['DATE'], 
#             y=df['TOTAL_IN_ICU'],
#             mode='lines',
#             line=dict(color='CornflowerBlue'),
#             name=""
#         ),
#         row=1, col=1
#     )

#     fig.add_trace(
#         go.Scatter(
#             x=df['DATE'], 
#             y=df['NEW_IN'],
#             mode='lines',
#             line=dict(color='Green'),
#             name=""
#         ),
#         row=1, col=2
#     )

#     fig.update_xaxes(title_text="Date", row=1, col=1)
#     fig.update_yaxes(title_text="Total in ICU", row=1, col=1)
#     fig.update_xaxes(title_text="Date", row=1, col=2)
#     fig.update_yaxes(title_text="New Hospitalisations", row=1, col=2)

#     fig.update_layout(hovermode='x unified', showlegend=False)

#     return [dcc.Graph(figure=fig)]


###############################
###                         ###
### CALLBACKS FOR TESTS TAB ###
###                         ###
###############################


# @app.callback(
#     Output('tests-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_tests(province):
#     df = pd.read_csv(f'{wdir}data/filtered_data/TESTS.csv')
#     df = df[ df["REGION"] == province ]

#     fig = make_subplots(
#         rows=1,
#         cols=2,
#         subplot_titles=(
#             'New tests',
#             'New positive tests',
#         )
#     )

#     fig.add_trace(
#         go.Scatter(
#             x=df['DATE'], 
#             y=df['TESTS_ALL'],
#             mode='lines',
#             line=dict(color='CornflowerBlue'),
#             name=""
#         ),
#         row=1, col=1
#     )

#     fig.add_trace(
#         go.Scatter(
#             x=df['DATE'], 
#             y=df['TESTS_ALL_POS'],
#             mode='lines',
#             line=dict(color='Green'),
#             name=""
#         ),
#         row=1, col=2
#     )

#     fig.update_layout(hovermode='x unified', showlegend=False)

#     fig.update_xaxes(title_text="Date", row=1, col=1)
#     fig.update_yaxes(title_text="New tests", row=1, col=1)
#     fig.update_xaxes(title_text="Date", row=1, col=2)
#     fig.update_yaxes(title_text="New ositive tests", row=1, col=2)

#     return [dcc.Graph(figure=fig)]


##################################
###                            ###
### CALLBACKS FOR MOBILITY TAB ###
###                            ###
##################################


# @app.callback(
#     Output('mobility-div', 'children'),
#     Input('predictions-province', 'value')
# )
# def update_province_mobility(province):
#     df = pd.read_csv(f'{wdir}data/filtered_data/MOBILITY.csv')
    
#     if province == "Belgium":
#         df = df[ df["country_region"] == "Belgium"]
#         mask = pd.isnull(df["sub_region_2"])
#         df = df[mask]
#         mask = pd.isnull(df["sub_region_1"])
#         df = df[mask]
#     elif province == "Brussels":
#         df = df[ df["sub_region_1"] == "Brussels"]
#     else:
#         df = df[ df["sub_region_2"] == province]

#     fig1 = make_subplots(
#         rows=1,
#         cols=2,
#         subplot_titles=(
#             'Retail and recreation change',
#             'Grocery and pharmacy change',
#         )
#     )

#     fig2 = make_subplots(
#         rows=1,
#         cols=2,
#         subplot_titles=(
#             'Parks change',
#             'Transit change',
#         )
#     )

#     fig3 = make_subplots(
#         rows=1,
#         cols=2,
#         subplot_titles=(
#             'Workplaces change',
#             'Residential change',
#         )
#     )

#     fig1.add_trace(
#         go.Scatter(
#             x=df['date'], 
#             y=df['retail_and_recreation_percent_change_from_baseline'],
#             mode='lines',
#             line=dict(color='CornflowerBlue'),
#             name=""
#         ),
#         row=1, col=1
#     )

#     fig1.add_trace(
#         go.Scatter(
#             x=df['date'], 
#             y=df['grocery_and_pharmacy_percent_change_from_baseline'],
#             mode='lines',
#             line=dict(color='orange'),
#             name=""
#         ),
#         row=1, col=2
#     )

#     fig2.add_trace(
#         go.Scatter(
#             x=df['date'], 
#             y=df['parks_percent_change_from_baseline'],
#             mode='lines',
#             line=dict(color='Green'),
#             name=""
#         ),
#         row=1, col=1
#     )

#     fig2.add_trace(
#         go.Scatter(
#             x=df['date'], 
#             y=df['transit_stations_percent_change_from_baseline'],
#             mode='lines',
#             line=dict(color='red'),
#             name=""
#         ),
#         row=1, col=2
#     )

#     fig3.add_trace(
#         go.Scatter(
#             x=df['date'], 
#             y=df['workplaces_percent_change_from_baseline'],
#             mode='lines',
#             line=dict(color='darkviolet'),
#             name=""
#         ),
#         row=1, col=1
#     )

#     fig3.add_trace(
#         go.Scatter(
#             x=df['date'], 
#             y=df['residential_percent_change_from_baseline'],
#             mode='lines',
#             line=dict(color='deeppink'),
#             name=""
#         ),
#         row=1, col=2
#     )

#     fig1.update_layout(hovermode='x unified', showlegend=False)
#     fig2.update_layout(hovermode='x unified', showlegend=False)
#     fig3.update_layout(hovermode='x unified', showlegend=False)

#     fig1.update_xaxes(title_text="Date", row=1, col=1)
#     fig1.update_yaxes(title_text="Percentage change", row=1, col=1)
#     fig1.update_xaxes(title_text="Date", row=1, col=2)
#     fig1.update_yaxes(title_text="Percentage changes", row=1, col=2)

#     fig2.update_xaxes(title_text="Date", row=1, col=1)
#     fig2.update_yaxes(title_text="Percentage change", row=1, col=1)
#     fig2.update_xaxes(title_text="Date", row=1, col=2)
#     fig2.update_yaxes(title_text="Percentage changes", row=1, col=2)

#     fig3.update_xaxes(title_text="Date", row=1, col=1)
#     fig3.update_yaxes(title_text="Percentage change", row=1, col=1)
#     fig3.update_xaxes(title_text="Date", row=1, col=2)
#     fig3.update_yaxes(title_text="Percentage changes", row=1, col=2)

#     return [html.Div([dcc.Graph(figure=fig1), dcc.Graph(figure=fig2), dcc.Graph(figure=fig3)])]

if __name__ == '__main__':
    app.run_server(debug=True)