import logging

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

# local imports
from app import app
from load_data import load_csv_table
from visualize import create_bar_chart


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(format=formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.callback(
    [Output('income-distribution', 'figure'),
    Output('cumulative-distribution', 'figure')],
    [Input('page2-year', 'value'),
    Input('page2-age', 'value'),
    Input('page2-sex', 'value'),
    Input('page2-geo', 'value')])
def update_income_distribution_plots(year, age, sex, geo):
    df = load_csv_table(11100008)
    logger.debug("year {}, age {}, sex {}, geo {}".format(year, age, sex, geo))
    hist, cumulative_plot = create_bar_chart(
        df, year,
        age, sex, geo)
    logger.debug("type(hist)")
    logger.debug(type(hist))
    return hist, cumulative_plot


