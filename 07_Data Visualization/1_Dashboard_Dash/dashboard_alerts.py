# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 09:45:06 2022

@author: cflorelu
"""

# Import required libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.title = "Oil & Gas Wells"
server = app.server

#Load data
df_day = pd.read_csv("data/df_day.csv")

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview")

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Clinical Analytics"),
            html.H3("Welcome to the Clinical Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
            ),
        ],
    )

clinic_list = ["1"]
admit_list = ["1"]
all_departments = ["1"]

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Clinic"),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in clinic_list],
                value=clinic_list[0],
            ),
            html.Br(),
            html.P("Select Check-In Time"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=dt(2014, 1, 1),
                end_date=dt(2014, 1, 15),
                min_date_allowed=dt(2014, 1, 1),
                max_date_allowed=dt(2014, 12, 31),
                initial_visible_month=dt(2014, 1, 1),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Admit Source"),
            dcc.Dropdown(
                id="admit-select",
                options=[{"label": i, "value": i} for i in admit_list],
                value=admit_list[:],
                multi=True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )

def generate_table_row(id, style, col1, col2, col3):
    """ Generate table rows.
    :param id: The ID of table row.
    :param style: Css style of this row.
    :param col1 (dict): Defining id and children for the first column.
    :param col2 (dict): Defining id and children for the second column.
    :param col3 (dict): Defining id and children for the third column.
    """

    return html.Div(
        id=id,
        className="row table-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                style={"display": "table", "height": "100%"},
                className="two columns row-department",
                children=col1["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"textAlign": "center", "height": "100%"},
                className="five columns",
                children=col2["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"textAlign": "center", "height": "100%"},
                className="five columns",
                children=col3["children"],
            ),
        ],
    )

def generate_table_row_helper(department):
    """Helper function.
    :param: department (string): Name of department.
    :return: Table row.
    """
    return generate_table_row(
        department,
        {},
        {"id": department + "_department", "children": html.B(department)},
        {
            "id": department + "wait_time",
            "children": dcc.Graph(
                id=department + "_wait_time_graph",
                style={"height": "100%", "width": "100%"},
                className="wait_time_graph",
                config={
                    "staticPlot": False,
                    "editable": False,
                    "displayModeBar": False,
                },
                figure={
                    "layout": dict(
                        margin=dict(l=0, r=0, b=0, t=0, pad=0),
                        xaxis=dict(
                            showgrid=False,
                            showline=False,
                            showticklabels=False,
                            zeroline=False,
                        ),
                        yaxis=dict(
                            showgrid=False,
                            showline=False,
                            showticklabels=False,
                            zeroline=False,
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                    )
                },
            ),
        },
        {
            "id": department + "_patient_score",
            "children": dcc.Graph(
                id=department + "_score_graph",
                style={"height": "100%", "width": "100%"},
                className="patient_score_graph",
                config={
                    "staticPlot": False,
                    "editable": False,
                    "displayModeBar": False,
                },
                figure={
                    "layout": dict(
                        margin=dict(l=0, r=0, b=0, t=0, pad=0),
                        xaxis=dict(
                            showgrid=False,
                            showline=False,
                            showticklabels=False,
                            zeroline=False,
                        ),
                        yaxis=dict(
                            showgrid=False,
                            showline=False,
                            showticklabels=False,
                            zeroline=False,
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                    )
                },
            ),
        },
    )

def initialize_table():
    """
    :return: empty table children. This is intialized for registering all figure ID at page load.
    """

    # header_row
    header = [
        generate_table_row(
            "header",
            {"height": "50px"},
            {"id": "header_department", "children": html.B("Department")},
            {"id": "header_wait_time_min", "children": html.B("Wait Time Minutes")},
            {"id": "header_care_score", "children": html.B("Care Score")},
        )
    ]

    # department_row
    rows = [generate_table_row_helper(department) for department in all_departments]
    header.extend(rows)
    empty_table = header

    return empty_table

# Create app layout
app.layout = html.Div(
    
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],),
        # Left column
        
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Patient Volume"),
                        html.Hr(),
                        dcc.Graph(id="patient_volume_hm"),
                    ],
                ),
                # Patient Wait time by Department
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("Patient Wait Time and Satisfactory Scores"),
                        html.Hr(),
                        html.Div(id="wait_time_table", children=initialize_table()),
                    ],
                ),
            ],
        ),
    ],
)

app.run_server(debug=True, use_reloader=False)
