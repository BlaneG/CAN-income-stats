import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# local imports
from load_data import (
    income_distribution_dropdown_values,
    median_income_dropdown_values
)


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
                    dbc.NavLink("Median income", href="/page-3", id="page-3-link"),
                    dbc.NavLink("References", href="/page-4", id="page-4-link"),
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
    html.P("This aim of this site is to help make some of the personal \
            income statistics from Statistics Canada more accessible to \
            Canadians."),
    html.H5("Income distribution"),
    dcc.Markdown("The *Income distribution* page is based on 'total income' from \
        income tax returns and includes [(ref)](https://www150.statcan.gc.ca/n1/en/catalogue/72-212-X):"),
    dcc.Markdown("\
            - employment income (salaries, commission), \n \
            - self employment income, \n \
            - pension income \
                (OAS, CPP/QPP, registered pension plans, RRIFs), \n \
            - investment income, \n \
            - social benefit payments (EI, workers' compensation, \
                social assistance), and \n \
            - other income."),
    dcc.Markdown("There is an important caveat about the definition of 'total income' \
        that is relevant when interpreting these statistics. Let's consider two \
        people with different income and pension benefits:"),
    dcc.Markdown("\
            - Person 1:  $70,000 total income, no pension, contributes $10,000 of their \
                income to RRSPs, \n \
            - Person 2:  $60,000 total income, receives a defined benefit \
                pension worth $10,000"),
    dcc.Markdown("At the end of the day these individuals have the same disposal \
        income, and presumably similar potential future income from their \
        pensions.  Based on StatCans 'total income' statistics, Person 1 has higher \
        'total income'.  The employment Person 1 uses \
        to make RRSP and RPP contributions counts as 'total income' \
        in the year it is earned, but also again when it \
        is withdrawn as pension income (plus any appreciation from capital gains, \
        dividends, and interest).  For Person 2, the defined benefit pension \
        is not counted as 'total income'.  Defined benefit pensions are \
        promises made by employers to pay employees in the future.  \
        Defined benefits pensions (and also employee contributions to \
        workplace pensions) show up on T4's as a 'pension adjustment'.  \
        "),
    html.H5("Median income"),
    dcc.Markdown("The *Median income* page is based on statistics from the \
        [Canadian Income Survey]\
        (https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&Id=1275662).\
        For the 2018 CIS, the sample size was around \
        56,000 households.")
])

################
# Layout 2: income distribution
################
def get_dropdown_options(items):
    return [{'label': value, 'value': value} for value in items]

layout2_dropdown_headers = dbc.Row([
    dbc.Col(html.Div("Select year")),
    dbc.Col(html.Div("Select location")),
    dbc.Col(html.Div("Select age group")),
])
layout2_dropdown = dbc.Row([
    dbc.Col(
        dcc.Dropdown(
            id='page2-year',
            placeholder="Select year",
            options=get_dropdown_options(
                income_distribution_dropdown_values["year_values"]),
            value=2017,
        ),
    ),
    dbc.Col(
        dcc.Dropdown(
            id='page2-geo',
            placeholder="Select location",
            options=get_dropdown_options(
                income_distribution_dropdown_values["geo_values"]),
            value="Canada"
        ),
    ),
    dbc.Col(
        dcc.Dropdown(
            id='page2-age',
            placeholder="Select age group",
            options=get_dropdown_options(
                income_distribution_dropdown_values["age_values"]),
            value='35 to 44 years',
        ),
    ),
])


layout2 = html.Div([
    html.H3("Income distribution"),
    layout2_dropdown_headers,
    layout2_dropdown,
    html.Div(
        dcc.Loading(dcc.Graph(id="income-distribution"), type='circle'),
        style={'width':'90%'}
        ),
    html.Div(
        dcc.Loading(dcc.Graph(id="cumulative-distribution"), type='circle'),
        style={'width':'90%'}
        )
])


################
# Layout 3: median income
################

page_3_dropdown_header = dbc.Row([
        dbc.Col(html.Div("Select age group")),
        dbc.Col(html.Div("Select sex")),
        dbc.Col()
        ])

page3_dropdown_header_2 = dbc.Row([
    dbc.Col(html.Div("Select region (hold ctrl for multiple selections)"))])

age_sex_dropdown = dbc.Row([
    dbc.Col(
        dcc.Dropdown(
                id='page3-age',
                placeholder="Select age group",
                options=get_dropdown_options(median_income_dropdown_values["Age group"]),
                value='35 to 44 years',
            )
    ),
    dbc.Col(
        dcc.Dropdown(
            id='page3-sex',
            placeholder="Select sex",
            options=get_dropdown_options(median_income_dropdown_values["Sex"]),
            value=["Males", "Females"],
            multi=True
            )
    ),
    dbc.Col()
])

region_dropdown = dbc.Row([
    dbc.Col(
        dcc.Dropdown(
                id='page3-geo',
                placeholder="Select location",
                options=get_dropdown_options(
                    median_income_dropdown_values["GEO"]),
                value=[
                    'Ottawa-Gatineau, Ontario/Quebec',
                    'Vancouver, British Columbia'],
                multi=True
            )
    )
])


layout3 = html.Div([
    html.H3("Median income"),
    page_3_dropdown_header,
    age_sex_dropdown,
    page3_dropdown_header_2,
    region_dropdown,
    html.Div(
        dcc.Loading(dcc.Graph(id="median-income"), type='circle'),
        style={'width':'100%'})
])


layout4 = html.Div([
    html.H3("References"),
    html.Div(dcc.Markdown("\
        - Statistics Canada \n\
            - [Tax filers and dependants with income by total income, sex and age](https://doi.org/10.25318/1110000801-eng),\n\
            - [Income of individuals by age group, sex and income source, Canada, provinces and selected census metropolitan areas](https://doi.org/10.25318/1110023901-eng)\n\
        - Source code for this webpage is hosted on [Github](https://github.com/BlaneG/CAN-income-stats)\n\
        "
    ))
])