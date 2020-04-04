import logging

import plotly.graph_objects as go
import plotly.express as px

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.ERROR)


# local imports
from wrangling import (
    preprocess_income_bin_data,
    subset_plot_data_for_scatter_plot,
    subset_year_age_sex_geo
)


def set_chart_title(plot_type, year, geo, age):
    subtitle = f"{year} total personal income in {geo}, {age}<br>"
    if plot_type=="hist":
        title = "<b>Income distrubution</b> <br>"
        
    elif plot_type=="cumulative":
        title = "<b>Cumulative income distrubution</b> <br>"
        
    title = title + subtitle
    return title

def format_bar_chart(plot_type, fig, year, age, geo):
    title = set_chart_title(plot_type, year, geo, age)
    fig.update_yaxes(range=[0, 1])
    fig.update_layout(
        title=title,
        barmode='overlay',
        template="simple_white",
        yaxis={"tickformat": ',.0%'}
        )
    fig.update_traces(opacity=0.7)
    return fig


def create_bar_chart(df, year, age, sex, geo)->go.Figure:
    x = ["<25k", "25-50k", "50k-75k","75k-100k",
         "...",
         "100-150k", "150-200k", "200-250k",
         "...",
         ">250k"]

    df_males = df[df["Sex"]=="Males"]
    df_females = df[df["Sex"]=="Females"]
    y_hist_m, y_cumulative_m = preprocess_income_bin_data(df_males)
    y_hist_f, y_cumulative_f = preprocess_income_bin_data(df_females)
    logger.debug(f"y_hist_m: {y_hist_m}")
    logger.debug(f"y_hist_f: {y_hist_f}")

    fig_hist = go.Figure([
        go.Bar(x=x, y=y_hist_f, name="Females", marker_color='#67001f'),
        go.Bar(x=x, y=y_hist_m, name="Males", marker_color='#053061'),
        ])

    fig_cumulative = go.Figure([
        go.Bar(x=x, y=y_cumulative_f, name="Females", marker_color='#67001f'),
        go.Bar(x=x, y=y_cumulative_m, name="Males", marker_color='#053061'),
        ])

    fig_hist = format_bar_chart("hist", fig_hist, year, age, geo)
    fig_cumulative = format_bar_chart("cumulative", fig_cumulative, year, age, geo)
    
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
    fig.update_xaxes(range=[1975, 2020],
        title="Year")
    fig.update_yaxes(range=[0, 90000],
        title="Median income")
    fig.update_layout(
        title=format_scatter_title(sex, age),
        template="simple_white",
        showlegend=True,
        legend_title='<b> Location and sex </b>',
        legend_orientation="h",
        legend_y=-0.3)
    
    return fig
    