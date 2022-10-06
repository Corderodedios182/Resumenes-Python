# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 11:30:32 2022
@author: corde
"""

# import dash-core, dash-html, dash io, bootstrap
import os
import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Rick and Morty", href=f"{app_name}/rick_and_morty")),
            dbc.NavItem(dbc.NavLink("Ciudad de México", href=f"{app_name}/cdmx")),
            dbc.NavItem(dbc.NavLink("Otro Proyecto", href=f"{app_name}/otro_proyecto"))],
        brand="Home",
        brand_href=f"{app_name}",
        sticky="top",
        color="light",
        dark=False,
        expand="lg",
    )
    return navbar

# set app variable with dash, set external style to bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard Machine Learning"
# set app server to variable for deployment
srv = app.server

# set app callback exceptions to true
app.config.suppress_callback_exceptions = True

app_name = os.getenv("DASH_APP_PATH", "/dash_machine_learning_sandbox")

# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div(
            [
                html.H2(children="Machine learning sandbox"),
                html.H3(children="Diferentes proyectos de ciencia de datos"),
            ]
        )
    ),
    className="banner",
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container([header, content])

# Main index function that will call and return all layout variables
def index():
    layout = html.Div([nav, container])
    return layout


# Set layout to index function
app.layout = index()

# Main
if __name__ == "__main__":
    app.run_server(debug=True, 
                   use_reloader=False)