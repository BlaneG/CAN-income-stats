import plotly.graph_objects as go

# local imports
from wrangling import (
    subset_plot_data_for_income_bins,
    preprocess_income_bin_data
)


def set_chart_title(plot_type, year, geo, sex, age):
    subtitle1 = f"{year} total income in {geo} <br>"
    subtitle2 = f"{sex}, {age}"
    if plot_type=="hist":
        title = "<b>Income distrubution:</b> <br>"
        
    elif plot_type=="cumulative":
        title = "<b>Cumulative income distrubution:</b> <br>"
        
    title = title + subtitle1 + subtitle2
    return title

def format_bar_chart(plot_type, fig, year, age, sex, geo):
    title = set_chart_title(plot_type, year, geo, sex, age)
    fig.update_yaxes(range=[0, 1])
    fig.update_layout(
        title=title,
        yaxis={"tickformat": ',.0%'}
        )
    return fig

def create_bar_chart(df, year, age, sex, geo):
    x = ["<25k", "25-50k", "50k-75k","75k-100k",
         "...",
         "100-150k", "150-200k", "200-250k",
         "...",
         ">250k"]
    
    cols_to_keep = ['REF_DATE', 
                    'GEO', 
                    'Sex', 
                    'Age group', 
                    'Persons with income',
                    'SCALAR_FACTOR', 
                    'VALUE', 
                    ]

    income_to_plot = ["Persons with income under $5,000",
                                "Persons with income of $5,000 and over",
                                "Persons with income of $10,000 and over",
                                "Persons with income of $15,000 and over",
                                "Persons with income of $20,000 and over",
                                "Persons with income of $25,000 and over",
                                "Persons with income of $35,000 and over",
                                "Persons with income of $50,000 and over",
                                "Persons with income of $75,000 and over",
                                "Persons with income of $100,000 and over",
                                "Persons with income of $150,000 and over",
                                "Persons with income of $200,000 and over",
                                "Persons with income of $250,000 and over"]

    df = subset_plot_data_for_income_bins(df, year, age, sex, geo, income_to_plot, cols_to_keep)
    y_hist, y_cumulative = preprocess_income_bin_data(df)
    fig_hist = go.Figure([go.Bar(x=x, y=y_hist)])
    fig_cumulative = go.Figure([go.Bar(x=x, y=y_cumulative)])
    fig_hist = format_bar_chart("hist", fig_hist, year, age, sex, geo)
    fig_cumulative = format_bar_chart("cumulative", fig_cumulative, year, age, sex, geo)
    
    return fig_hist, fig_cumulative
