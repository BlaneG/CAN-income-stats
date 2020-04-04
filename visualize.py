import plotly.graph_objects as go
import plotly.express as px


# local imports
from wrangling import (
    preprocess_income_bin_data,
    subset_plot_data_for_scatter_plot,
    subset_year_age_sex_geo
)


def set_chart_title(plot_type, year, geo, sex, age):
    subtitle = f"{year} total personal income in {geo} for {sex}, {age}<br>"
    if plot_type=="hist":
        title = "<b>Income distrubution</b> <br>"
        
    elif plot_type=="cumulative":
        title = "<b>Cumulative income distrubution</b> <br>"
        
    title = title + subtitle
    return title

def format_bar_chart(plot_type, fig, year, age, sex, geo):
    title = set_chart_title(plot_type, year, geo, sex, age)
    fig.update_yaxes(range=[0, 1])
    fig.update_layout(
        title=title,
        yaxis={"tickformat": ',.0%'}
        )
    return fig

def create_bar_chart(df, year, age, sex, geo)->go.Figure:
    x = ["<25k", "25-50k", "50k-75k","75k-100k",
         "...",
         "100-150k", "150-200k", "200-250k",
         "...",
         ">250k"]

    y_hist, y_cumulative = preprocess_income_bin_data(df)
    fig_hist = go.Figure([go.Bar(x=x, y=y_hist)])
    fig_cumulative = go.Figure([go.Bar(x=x, y=y_cumulative)])
    fig_hist = format_bar_chart("hist", fig_hist, year, age, sex, geo)
    fig_cumulative = format_bar_chart("cumulative", fig_cumulative, year, age, sex, geo)
    
    return fig_hist, fig_cumulative


def format_scatter_title(sex, age):
    title = "<b>Median income</b> <br>"
    subtitle = f"Total median income (2018 dollars) for {', '.join(sex)} aged {age}"
    return title + subtitle

def create_scatter_plot(df, sex, age, geo)->go.Figure:
    """
    Parameters
    ----------
    df : pd.DataFrame
    sex : tuple
    age : str
    locations : tuple

    """
    # year = 2017
    # df = subset_plot_data_for_scatter_plot(df, year, age, sex, geo,
    # income_source, income_to_plot, cols_to_keep)

    df = df[df["Age group"]==age]
    df = df[df.GEO.isin(geo)]
    df = df[df.Sex.isin(sex)]
    fig = px.line(df, x="REF_DATE", y="VALUE", color="GEO", line_dash="Sex")
    fig.update_xaxes(range=[1975, 2020])
    fig.update_yaxes(range=[0, 90000])
    fig.update_layout(title=format_scatter_title(sex, age))
    fig.update_layout(showlegend=True)
    fig.update_layout(legend_title='Location and sex')
    
    return fig
    