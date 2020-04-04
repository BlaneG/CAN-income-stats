import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.ERROR)


################################
# wrangling methods used in:
#  - income_distribution.ipynb
################################

def get_persons_per_income_group(df):
    """Formats cumulative bins (e.g. <50k) to 25k incremental bins (e.g. >25-50k)."""
    df["VALUE"].values[1:-1] = df["VALUE"].values[1:-1] - df["VALUE"].values[2:]
    return df


def create_income_bins(y)->np.array:
    raw_income_bins = 13
    # sum 0:5, 5:7, and then take individual values
    logger.info("create_income_bins()")
    logger.debug(f"y: /n {y}")
    if len(y)==raw_income_bins:
        y = np.add.reduceat(y, [0,5,7,8,9,10,11,12])
        return y
    elif len(y)==0:
        return np.array([np.nan]*13)
    else: return y

def add_gaps(y):
    # some empty values for discontinuities
    y = np.insert(y, [4, 7], [np.nan])
    return y


def normalize_plot_data(y)->np.array:
    y = np.divide(y, np.sum(y))
    return y


def format_hist_data(df)->np.array:
    df = get_persons_per_income_group(df)
    y = df.VALUE.values
    y_hist = normalize_plot_data(y)
    return y_hist


def preprocess_income_bin_data(df)->tuple:
    """Process the data for plotting.

    Returns
    ---------
    tuple of np.arrays
    """
    y_hist = format_hist_data(df)
    y_hist = create_income_bins(y_hist)
    y_cumulative = np.cumsum(y_hist)
    y_hist = add_gaps(y_hist)
    y_cumulative = add_gaps(y_cumulative)
    return y_hist, y_cumulative


def subset_plot_data_for_income_bins(df)->pd.DataFrame:
    """Used in make_data.py to subset the raw data."""
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
    df = df.loc[:,cols_to_keep]
    df = get_income_to_plot_for_hist(df, income_to_plot)
    return df

###############################
# wrangling methods used in:
#  - median_income.ipynb
###############################
def subset_rows(df, column, value)->np.ndarray:
    """
    A method to s A method to subset rows of the https://doi.org/10.25318/1110000801-eng
    df : pd.DataFrame
    column : str
    value : str
    
    """
    mask = (df[column] == value)
    return mask.values


def subset_REF_DATE(df, year):
    return subset_rows(df, "REF_DATE", year)


def subset_GEO(df, geo):
    return subset_rows(df, "GEO", geo)


def subset_Sex(df, sex):
    # return subset_rows(df, "Sex", sex)
    logger.debug(f"sex: {sex}")
    return df["Sex"].isin(sex)


def subset_Age(df, age):
    return subset_rows(df, "Age group", age)


def subset_year_age_sex_geo(df, year=None, age=None, sex=None, geo=None):
    mask_year = subset_REF_DATE(df, year)
    mask_geo = subset_GEO(df, geo)
    mask_sex = subset_Sex(df, sex)
    mask_age = subset_Age(df, age)
    return df[(mask_year) & (mask_geo) & (mask_sex) & (mask_age)]


def get_income_to_plot_for_hist(df, income_to_plot):
    df = df[df["Persons with income"].isin(income_to_plot)]
    return df

def get_income_to_plot_for_scatter(df, income_to_plot):
    df = df[df["Statistics"].isin(income_to_plot)]
    return df


def subset_plot_data_for_scatter_plot(
    df, year, age, sex, geo,
    income_source, income_to_plot, cols_to_keep):
    df = df.loc[:,cols_to_keep]
    df = subset_year_age_sex_geo(df, year, age, sex, geo)
    df = df[df["Income source"].isin(income_source)]
    df = get_income_to_plot_for_scatter(df, income_to_plot)
    return df


def subset_for_scatter_plot(df, income_source, income_to_plot, cols_to_keep):
    df = df.loc[:,cols_to_keep]
    df = df[df["Income source"]==income_source]
    df = df[df["Statistics"]==income_to_plot]
    return df

