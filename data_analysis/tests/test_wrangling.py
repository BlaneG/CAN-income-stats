import pandas as pd
import numpy as np
import pytest

from ..wrangling import (
    subset_plot_data_for_income_bins,
    subset_plot_data_for_scatter_plot
)
def test_subset_plot_data_for_income_bins():

    expected_result = {'Age group': {598748: '35 to 44 years',
                                    598749: '35 to 44 years',
                                    598750: '35 to 44 years',
                                    598751: '35 to 44 years',
                                    598752: '35 to 44 years',
                                    598753: '35 to 44 years',
                                    598754: '35 to 44 years',
                                    598755: '35 to 44 years',
                                    598756: '35 to 44 years',
                                    598757: '35 to 44 years',
                                    598758: '35 to 44 years',
                                    598759: '35 to 44 years',
                                    598760: '35 to 44 years'},
                        'GEO': {598748: 'Canada',
                                598749: 'Canada',
                                598750: 'Canada',
                                598751: 'Canada',
                                598752: 'Canada',
                                598753: 'Canada',
                                598754: 'Canada',
                                598755: 'Canada',
                                598756: 'Canada',
                                598757: 'Canada',
                                598758: 'Canada',
                                598759: 'Canada',
                                598760: 'Canada'},
                        'Persons with income': {598748: 'Persons with income under $5,000',
                                                598749: 'Persons with income of $5,000 and over',
                                                598750: 'Persons with income of $10,000 and over',
                                                598751: 'Persons with income of $15,000 and over',
                                                598752: 'Persons with income of $20,000 and over',
                                                598753: 'Persons with income of $25,000 and over',
                                                598754: 'Persons with income of $35,000 and over',
                                                598755: 'Persons with income of $50,000 and over',
                                                598756: 'Persons with income of $75,000 and over',
                                                598757: 'Persons with income of $100,000 and over',
                                                598758: 'Persons with income of $150,000 and over',
                                                598759: 'Persons with income of $200,000 and over',
                                                598760: 'Persons with income of $250,000 and over'},
                        'REF_DATE': {598748: 2017,
                                    598749: 2017,
                                    598750: 2017,
                                    598751: 2017,
                                    598752: 2017,
                                    598753: 2017,
                                    598754: 2017,
                                    598755: 2017,
                                    598756: 2017,
                                    598757: 2017,
                                    598758: 2017,
                                    598759: 2017,
                                    598760: 2017},
                        'SCALAR_FACTOR': {598748: 'units ',
                                        598749: 'units ',
                                        598750: 'units ',
                                        598751: 'units ',
                                        598752: 'units ',
                                        598753: 'units ',
                                        598754: 'units ',
                                        598755: 'units ',
                                        598756: 'units ',
                                        598757: 'units ',
                                        598758: 'units ',
                                        598759: 'units ',
                                        598760: 'units '},
                        'Sex': {598748: 'Females',
                                598749: 'Females',
                                598750: 'Females',
                                598751: 'Females',
                                598752: 'Females',
                                598753: 'Females',
                                598754: 'Females',
                                598755: 'Females',
                                598756: 'Females',
                                598757: 'Females',
                                598758: 'Females',
                                598759: 'Females',
                                598760: 'Females'},
                        'VALUE': {598748: 116190.0,
                                598749: 2214880.0,
                                598750: 2098920.0,
                                598751: 1966980.0,
                                598752: 1836860.0,
                                598753: 1699380.0,
                                598754: 1406370.0,
                                598755: 958310.0,
                                598756: 470300.0,
                                598757: 193910.0,
                                598758: 48780.0,
                                598759: 20580.0,
                                598760: 10390.0}}
    # params
    path = r"../../data/raw/11100008.csv"
    df = pd.read_csv(path, low_memory=False)
    age = "35 to 44 years"
    year = 2017
    geo = "Canada"
    sex = "Females"

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

    df = subset_plot_data_for_income_bins(
        df, year, age, sex, geo,
        income_to_plot, cols_to_keep)
    assert expected_result == df.to_dict()


def test_subset_plot_data_for_scatter_plot():

    expected_value = {'Age group': {1550629: '25 to 34 years'},
                        'GEO': {1550629: 'Canada'},
                        'Income source': {1550629: 'Total income'},
                        'REF_DATE': {1550629: 2017},
                        'SCALAR_FACTOR': {1550629: 'units'},
                        'Sex': {1550629: 'Females'},
                        'Statistics': {1550629: 'Median income (excluding zeros)'},
                        'VALUE': {1550629: 34800.0}}

    # load the data
    path = r"../../data/raw/11100239.csv"
    df = pd.read_csv(path, low_memory=False)

    # parameters
    year = 2017
    Age = '25 to 34 years'
    sex = "Females"
    geo = "Canada"
    cols_to_keep = ['REF_DATE', 
                'GEO', 
                'Sex', 
                'Age group', 
                'Income source',
                'Statistics',
                'SCALAR_FACTOR', 
                'VALUE', 
                 ]
    
    df = subset_plot_data_for_scatter_plot(
        df, year, Age, sex, geo,
        ["Total income"], ['Median income (excluding zeros)'],
        cols_to_keep)

    assert expected_value == df.to_dict()