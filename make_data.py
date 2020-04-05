# This file is for updating the preprocessed data used in the application.
import pandas as pd
from load_data import load_csv_table, download_raw_data
from wrangling import (
    subset_for_scatter_plot,
    subset_plot_data_for_income_bins
)


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


def download_and_preprocess_raw_data()->None:
    download_raw_data(11100239)
    download_raw_data(11100008)
    preprocess_11100239()
    preprocess_11100008()


if __name__ == "__main__":
    download_and_preprocess_raw_data()
