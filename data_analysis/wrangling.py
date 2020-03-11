import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.ERROR)


###############################
# wrangling methods used in:
#  - income_distribution.ipynb
#  - median_income.ipynb
###############################
def subset_rows(df, column, value)->np.ndarray:
    """
    A method to s A method to subset rows of the https://doi.org/10.25318/1110000801-eng
    df : pd.DataFrame
    column : str
    value : str
    
    """
    mask = df[column] == value
    return mask.values


def subset_REF_DATE(df, year):
    return subset_rows(df, "REF_DATE", year)


def subset_GEO(df, geo):
    return subset_rows(df, "GEO", geo)


def subset_Sex(df, sex):
    return subset_rows(df, "Sex", sex)


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

def subset_plot_data_for_income_bins(df, year, age, sex, geo, income_to_plot, cols_to_keep):
    df = df.loc[:,cols_to_keep]
    df = subset_year_age_sex_geo(df, year, age, sex, geo)
    df = get_income_to_plot_for_hist(df, income_to_plot)
    return df

def subset_plot_data_for_scatter_plot(
    df, year, age, sex, geo,
    income_source, income_to_plot, cols_to_keep):
    df = df.loc[:,cols_to_keep]
    df = subset_year_age_sex_geo(df, year, age, sex, geo)
    df = df[df["Income source"].isin(income_source)]
    df = get_income_to_plot_for_scatter(df, income_to_plot)
    return df


##########################
# wrangling for small multiples plots
# code used in Plotting_mpl.ipynb and 
# plotting_plotly.ipynb
##########################

def _compute_population_income_bins(df):
    """A function to 
    
    Params
    ---------
    df : pd.DataFrame
        raw data input from stats Canada
    
    Returns
    --------
    df : pd.DataFrame
        updated dataframe with new column containing population by income bin
    """
    
    df["count"] = np.nan
    already_total = ["Total persons with income",
                     "Persons with income under $5,000",
                     "Persons with income of $250,000 and over"]
    
    not_evaluated = ["Median total income", "5-year percent change of median income"]
    
    # need to include >$250k here because we use shift() below
    mask1 = (~df["Persons with income"].isin(already_total[0:2])) & (~df["Persons with income"].isin(not_evaluated))
    df.loc[mask1, "count"] = df.loc[mask1, "VALUE"] - df.loc[mask1, "VALUE"].shift(-1)
    logger.debug("df.head(2): ")
    logger.debug("{}".format(df.head(2)))
    
    mask2 = (df["Persons with income"].isin(already_total))
    df.loc[mask2,"count"] = df.loc[mask2,"VALUE"]
    logger.debug("updated df.head(2):")
    logger.debug("{}".format(df.head(2)))
    df = df.reset_index(drop=True)
    logger.debug("reindexed df: ")
    logger.debug("{}".format(df.head(2)))
    
    return df

def _create_50k_histogram_bins(df):
    """
    This is a function to create income bins of equal size (in dollar value).
    Used by format_data_for_histogram()
    
    Params
    ----------
    df : pd.DataFrame
        takes an input dataframe that has been pre-processed by _compute_population_income_bins
    
    Returns
    ---------
    pd.DataFrame
        a df with equal sized income bins
    """
    columns_to_keep = {"Year": "REF_DATE", "Location": "GEO", "Sex":"Sex", "Age": "Age group"}
    #initialize df
    new_df = pd.DataFrame(columns = ["Income", "Location", "Age", "Sex", "Year"])
    # here we create a new label for income bins (Income) and 
    # specify the ordering of the Income bins for pandas


    income_labels = {"Persons with income under $5,000": 1, 
                            "Persons with income of $5,000 and over":2, 
                            "Persons with income of $10,000 and over":3, 
                            "Persons with income of $15,000 and over":4, 
                            "Persons with income of $20,000 and over":5, 
                            "Persons with income of $25,000 and over":6, 
                            "Persons with income of $35,000 and over":7, 
                            "Persons with income of $50,000 and over":8, 
                            "Persons with income of $75,000 and over":9, 
                            "Persons with income of $100,000 and over":10, 
                            "Persons with income of $150,000 and over":11, 
                            "Persons with income of $200,000 and over":12, 
                            "Persons with income of $250,000 and over":13,
                    }

    histogram_bin_labels = {"0-<25k":[1,2,3,4,5],
                            "$25-<50k":[6,7],
                            "$50-<75k":[8],
                            "$75-<100k":[9],
                            "$100-<125k":[10],
                            "$125-<150k":[10],
                            "$150-<175k":[11],
                            "$175-<200k":[11],
                            "$200-225k":[12],
                            "225-250k":[12],
                            ">250k":[13],
                           }
    
    if df.empty:
        return new_df
    
    else:
        for i, income_bin in enumerate(histogram_bin_labels.keys()):
            row_values = histogram_bin_labels[income_bin]
            for column in columns_to_keep.keys():
                new_df.loc[i,column] = df.loc[0,columns_to_keep[column]]

            if all([value<10 for value in row_values]):
                # rows to sum
                logger.debug("income_bin: ")
                logger.debug(income_bin)
                logger.debug('new_df.loc[i,"Income"]: ')
                logger.debug(new_df.loc[i,"Income"])
                logger.debug("new_df.head(2)")
                logger.debug(new_df.head(2))
                

                new_df.loc[i,"Income"] = income_bin
                new_df.loc[i,"count"] = df.loc[row_values,"count"].sum()
            elif all([value==13 for value in row_values]):
                # we can use this value directly
                assert len(row_values)==1, "row_values should have len==1"
                new_df.loc[i,"Income"] = income_bin
                new_df.loc[i,"count"] = df.loc[row_values,"count"].sum()
            else:
                # a simple interpolation to break apart larger bins
                new_df.loc[i,"Income"] = income_bin
                new_df.loc[i,"count"] = df.loc[row_values,"count"].values/2.

        new_df = new_df.sort_values(by="Income")
        new_df["percentage"] = new_df.loc[:,"count"].values / np.sum(new_df.loc[:,"count"].values)
        new_df["cumulative_percent"] = new_df.loc[:,"percentage"].cumsum()

    return new_df




def format_data_for_histogram(df, dates, locations, sex, age, cols_to_keep):
    """
    dates: list of int, year of data
    locations: list of str, locations to be evaluated
    sex: list of str, m or f
    age:  list of str, age groups to be evaluated
    """
    
    df = df.loc[:,cols_to_keep]
    histogram_df = pd.DataFrame()
    
    # loop through all the unique label combinations
    for d in dates:
        for l in locations:
            for s in sex:
                for a in age:
                    labels = {"Location": l,"Year": d, "Sex": s, "Age": a}
                    # if True:
                    mask = (df.REF_DATE==d) & (df.GEO==l) & (df.Sex==s) & (df["Age group"]==a)
                    
                    temp_df = df.loc[mask,:]
                    temp_df = _compute_population_income_bins(temp_df)
                    hist_df_update = _create_50k_histogram_bins(temp_df)

                    if histogram_df.empty:
                        histogram_df = hist_df_update
                    else:
                        histogram_df = pd.concat([histogram_df, hist_df_update], ignore_index=True)

    return histogram_df

if __name__=='__main__':
    # parameters
    path = r"../data/raw/11100008.csv"
    df = pd.read_csv(path, low_memory=False)
    locations = ["Canada",
                'Halifax, Nova Scotia',
                "St. John's, Newfoundland and Labrador",
                'Saint John, New Brunswick',
                'Montréal, Quebec',
                'Ottawa-Gatineau, Ontario part',
                'Toronto, Ontario',
                'Regina, Saskatchewan',
                'Winnipeg, Manitoba',
                'Calgary, Alberta',
                'Vancouver, British Columbia',
                'Victoria, British Columbia',
                'Moncton, New Brunswick',
                'Charlottetown, Prince Edward Island',
                ]
    sex = ["Males",
        "Females"]

    dates = [2016]
    age = df["Age group"].unique()
    cols_to_keep = ['REF_DATE', 
                    'GEO', 
                    'Sex', 
                    'Age group', 
                    'Persons with income',
                    'SCALAR_FACTOR', 
                    'VALUE', 
                    ]

    processed_data = format_data_for_histogram(df, dates, locations, sex, age, cols_to_keep)
    path = r"../data/processed/11100008.csv"
    processed_data.to_csv(path)