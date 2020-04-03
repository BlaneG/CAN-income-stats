# run this file to 
import pandas as pd
from load_data import load_csv_table
from wrangling import (
    subset_for_scatter_plot,
    subset_plot_data_for_income_bins
)


def preprocess_raw_data():
    preprocess_11100239()
    preprocess_11100008()


def preprocess_11100239():
    """Reduces the raw data size so it can be stored in github."""
    df = load_csv_table(11100239)
    cols_to_keep = ['REF_DATE', 
                    'GEO', 
                    'Sex', 
                    'Age group', 
                    'Income source',
                    'Statistics',
                    'SCALAR_FACTOR', 
                    'VALUE', 
                    ]
    df = subset_for_scatter_plot(
        df,
        "Total income",
        'Median income (excluding zeros)',
        cols_to_keep)
    df.to_csv(r"data/processed/11100239.csv")


def preprocess_11100008():
    df = load_csv_table(11100008)
    df = subset_plot_data_for_income_bins(df)
    df.to_csv(r"data/processed/11100008.csv")


if __name__ == "__main__":
    preprocess_raw_data()
