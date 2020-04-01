import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# local imports
from load_data import income_distribution_dropdown_values


# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Page Menu", className="display-4")),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "rgba(0,0,0,.5)",
                    "border-color": "rgba(0,0,0,.1)",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("About", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Income distribution", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Median income statistics", href="/page-3", id="page-3-link"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)



layout1 = html.Div([
    html.H3("About"),
    html.P("This website summarizes Canadian personal income \
            statistics using data provided by Statistics Canada."),
    html.P("Unless it is defined otherwise, income refers to \
            'total personal income' which includes:"),
    dcc.Markdown("\
            - employment income (salaries, commission), \n \
            - self employment income, pension income \
                (OAS, CPP/QPP, registered pension plans, RRIFs), \n \
            - investment income, \n \
            - social benefit payments (EI, workers' compensation, \
                social assisstance), and \n \
            - other income.")
])

################
# Layout 2: income distribution
################
def get_dropdown_options(items):
    return [{'label': value, 'value': value} for value in items]


income_distribution_dropdown = html.Div([
    dcc.Dropdown(
        id='page2-year',
        placeholder="Select year",
        options=get_dropdown_options(income_distribution_dropdown_values["year_values"]),
        value=2017,
    ),
    dcc.Dropdown(
        id='page2-geo',
        placeholder="Select location",
        options=get_dropdown_options(income_distribution_dropdown_values["geo_values"]),
        value="Canada"
    ),
    dcc.Dropdown(
        id='page2-age',
        placeholder="Select age group",
        options=get_dropdown_options(income_distribution_dropdown_values["age_values"]),
        value='35 to 44 years',
    ),
    dcc.Dropdown(
        id='page2-sex',
        placeholder="Select sex",
        options=get_dropdown_options(income_distribution_dropdown_values["sex_values"]),
        value="Females"
        )
])

layout2 = html.Div([
    html.H3("Income distribution"),
    income_distribution_dropdown,
    dcc.Graph(id="income-distribution"),
    dcc.Graph(id="cumulative-distribution")
    
])


################
# Layout 3: median income
################
layout3 = html.Div([
    html.H3("Median income"),
    dcc.Graph(id="median-income")
    
])