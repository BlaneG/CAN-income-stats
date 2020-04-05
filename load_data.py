import requests, zipfile, io
import pandas as pd
import os
import numpy as np


def get_csv_zip_url(table_id)->str:
    """
    Returns the url for a table_id to extract raw data from Stats Canada.

    Parameters
    --------
    table_id : int
        Statistics Canada Table ID
    
    Returns
    --------
    str
        http address for downloading zipped csv file

    References
    --------
    Statistics Canada developer guide:
        https://www.statcan.gc.ca/eng/developers/wds/user-guide#a12-6
    """
    stats_can_url = 'https://www150.statcan.gc.ca/t1/wds/rest/'
    func = 'getFullTableDownloadCSV/'
    table_id = str(table_id) + '/'
    language = 'en'
    api_call = stats_can_url + func + table_id + language
    response = requests.get(api_call)
    
    return response.json()['object']


def download_raw_data(table_id):
    """
    Download and extract a csv file using a table_id from statistics Canada.
    """
    zip_file_url = get_csv_zip_url(table_id)
    print(f'downloading zipped csv file for {table_id}...')
    zip_csv_response = requests.get(zip_file_url)
    print('download complete')
    zip_csv = zipfile.ZipFile(io.BytesIO(zip_csv_response.content))
    print(f'extracting zipped csv file for {table_id}...')
    zip_csv.extractall("data/raw")
    print('extraction complete')


def load_csv_table(table_id):
    raw_data_path = "data/raw/"
    csv_path = raw_data_path + str(table_id) + ".csv"
    print(csv_path)
    print(os.getcwd())
    df = pd.read_csv(csv_path, low_memory=False)
    return df

income_distribution_dropdown_values = { \
    "age_values": ['All age groups', '0 to 24 years', '25 to 34 years',
        '35 to 44 years', '45 to 54 years', '55 to 64 years',
        '65 to 74 years', '75 years and over', '65 years and over'],
    "geo_values": ['Canada', 'Newfoundland and Labrador',
        "St. John's, Newfoundland and Labrador", 'Prince Edward Island',
        'Nova Scotia', 'Halifax, Nova Scotia', 'New Brunswick',
        'Saint John, New Brunswick', 'Quebec', 'Saguenay, Quebec',
        'Québec, Quebec', 'Sherbrooke, Quebec', 'Trois-Rivières, Quebec',
        'Montréal, Quebec', 'Ottawa-Gatineau, Quebec part', 'Ontario',
        'Ottawa-Gatineau, Ontario part', 'Oshawa, Ontario',
        'Toronto, Ontario', 'Hamilton, Ontario',
        'St. Catharines-Niagara, Ontario',
        'Kitchener-Cambridge-Waterloo, Ontario', 'London, Ontario',
        'Windsor, Ontario', 'Greater Sudbury, Ontario',
        'Thunder Bay, Ontario', 'Manitoba', 'Winnipeg, Manitoba',
        'Saskatchewan', 'Regina, Saskatchewan', 'Saskatoon, Saskatchewan',
        'Alberta', 'Calgary, Alberta', 'Edmonton, Alberta',
        'British Columbia', 'Vancouver, British Columbia',
        'Victoria, British Columbia', 'Yukon', 'Northwest Territories',
        'Nunavut', 'Kingston, Ontario',
        'Abbotsford-Mission, British Columbia', 'Moncton, New Brunswick',
        'Peterborough, Ontario', 'Brantford, Ontario', 'Guelph, Ontario',
        'Barrie, Ontario', 'Kelowna, British Columbia',
        'Bay Roberts, Newfoundland and Labrador',
        'Grand Falls-Windsor, Newfoundland and Labrador',
        'Corner Brook, Newfoundland and Labrador',
        'Non CMA-CA, Newfoundland and Labrador',
        'Charlottetown, Prince Edward Island',
        'Summerside, Prince Edward Island',
        'Non CMA-CA, Prince Edward Island', 'Kentville, Nova Scotia',
        'Truro, Nova Scotia', 'New Glasgow, Nova Scotia',
        'Cape Breton, Nova Scotia', 'Non CMA-CA, Nova Scotia',
        'Fredericton, New Brunswick', 'Bathurst, New Brunswick',
        'Miramichi, New Brunswick', 'Campbellton, New Brunswick part',
        'Edmundston, New Brunswick', 'Non CMA-CA, New Brunswick',
        'Campbellton, Quebec part', 'Matane, Quebec', 'Rimouski, Quebec',
        'Rivière-du-loup, Quebec', 'Baie-Comeau, Quebec', 'Alma, Quebec',
        'Dolbeau-Mistassini, Quebec', 'Sept-Îles, Quebec',
        'Saint-Georges, Quebec', 'Thetford Mines, Quebec',
        'Cowansville, Quebec', 'Victoriaville, Quebec',
        'Shawinigan, Quebec', 'La Tuque, Quebec', 'Drummondville, Quebec',
        'Granby, Quebec', 'Saint-Hyacinthe, Quebec', 'Sorel-Tracy, Quebec',
        'Joliette, Quebec', 'Saint-Jean-sur-Richelieu, Quebec',
        'Salaberry-de-Valleyfield, Quebec', 'Lachute, Quebec',
        "Val-d'Or, Quebec", 'Amos, Quebec', 'Rouyn-Noranda, Quebec',
        'Hawkesbury, Quebec part', 'Non CMA-CA, Quebec',
        'Cornwall, Ontario', 'Hawkesbury, Ontario part',
        'Brockville, Ontario', 'Pembroke, Ontario', 'Petawawa, Ontario',
        'Belleville, Ontario', 'Cobourg, Ontario', 'Port Hope, Ontario',
        'Kawartha Lakes, Ontario', 'Centre Wellington, Ontario',
        'Ingersoll, Ontario', 'Woodstock, Ontario', 'Tillsonburg, Ontario',
        'Norfolk, Ontario', 'Stratford, Ontario', 'Chatham-Kent, Ontario',
        'Leamington, Ontario', 'Sarnia, Ontario', 'Owen Sound, Ontario',
        'Collingwood , Ontario', 'Orillia, Ontario', 'Midland, Ontario',
        'North Bay, Ontario', 'Elliot Lake, Ontario',
        'Temiskaming Shores, Ontario', 'Timmins, Ontario',
        'Sault Ste. Marie, Ontario', 'Kenora, Ontario',
        'Non CMA-CA, Ontario', 'Portage la Prairie, Manitoba',
        'Brandon, Manitoba', 'Thompson, Manitoba', 'Non CMA-CA, Manitoba',
        'Yorkton, Saskatchewan', 'Moose Jaw, Saskatchewan',
        'Swift Current, Saskatchewan', 'North Battleford, Saskatchewan',
        'Prince Albert, Saskatchewan', 'Estevan, Saskatchewan',
        'Lloydminster, Saskatchewan part', 'Non CMA-CA, Saskatchewan',
        'Medicine Hat, Alberta', 'Brooks, Alberta', 'Lethbridge, Alberta',
        'Okotoks, Alberta', 'Canmore, Alberta', 'Red Deer, Alberta',
        'Camrose, Alberta', 'Lloydminster, Alberta part',
        'Cold Lake, Alberta', 'Grande Prairie, Alberta',
        'Wood Buffalo, Alberta', 'Wetaskiwin, Alberta',
        'Non CMA-CA, Alberta', 'Cranbrook, British Columbia',
        'Penticton, British Columbia', 'Vernon, British Columbia',
        'Salmon Arm, British Columbia', 'Kamloops, British Columbia',
        'Chilliwack, British Columbia', 'Squamish, British Columbia',
        'Duncan, British Columbia', 'Nanaimo, British Columbia',
        'Parksville, British Columbia', 'Port Alberni, British Columbia',
        'Courtenay, British Columbia', 'Campbell River, British Columbia',
        'Powell River, British Columbia',
        'Williams Lake, British Columbia', 'Quesnel, British Columbia',
        'Prince Rupert, British Columbia', 'Kitimat, British Columbia',
        'Terrace, British Columbia', 'Prince George, British Columbia',
        'Dawson Creek, British Columbia',
        'Fort St. John, British Columbia', 'Non CMA-CA, British Columbia',
        'Whitehorse, Yukon', 'Non CMA-CA, Yukon',
        'Yellowknife, Northwest Territories',
        'Non CMA-CA, Northwest Territories',
        'Campbellton, combined NewBrunswick/Quebec',
        'Hawkesbury, combined Ontario/Quebec',
        'Ottawa - Gatineau, combined Ontario/Quebec',
        'Lloydminster, combined Alberta/Saskatchewan',
        'Steinbach, Manitoba', 'High River, Alberta',
        'Strathmore, Alberta', 'Sylvan Lake, Alberta', 'Lacombe, Alberta',
        'Gander, Newfoundland and Labrador', 'Sainte-Marie, Quebec',
        'Arnprior, Ontario', 'Carleton Place, Ontario',
        'Wasaga Beach, Ontario', 'Winkler, Manitoba',
        'Weyburn, Saskatchewan', 'Nelson, British Columbia'],
    "sex_values": ['Both sexes', 'Males', 'Females'],
    "year_values": [2000, 2001, 2002, 2003, 2004, 2005, 2006,
        2007, 2008, 2009, 2010,
        2011, 2012, 2013, 2014, 2015, 2016, 2017]}


median_income_dropdown_values = {
    'REF_DATE': np.array([
        1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986,
        1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997,
        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
        2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
               dtype=int),
    'GEO': np.array([
        'Canada', 'Atlantic provinces', 'Newfoundland and Labrador',
        'Prince Edward Island', 'Nova Scotia', 'New Brunswick', 'Quebec',
        'Ontario', 'Prairie provinces', 'Manitoba', 'Saskatchewan',
        'Alberta', 'British Columbia', 'Québec, Quebec',
        'Montréal, Quebec', 'Ottawa-Gatineau, Ontario/Quebec',
        'Toronto, Ontario', 'Winnipeg, Manitoba', 'Calgary, Alberta',
        'Edmonton, Alberta', 'Vancouver, British Columbia'], dtype=object),
    'Sex': np.array(['Both sexes', 'Males', 'Females'], dtype=object),
    'Age group': np.array([
        '16 years and over', '16 to 24 years', '25 to 54 years',
        '25 to 34 years', '35 to 44 years', '45 to 54 years',
        '55 to 64 years', '65 years and over'], dtype=object),
    'Income source': np.array([
        'Total income', 'Market income', 'Employment income',
        'Wages, salaries and commissions', 'Self-employment income',
        'Investment income', 'Retirement income', 'Other income',
        'Government transfers',
        "Old Age Security (OAS) and Guaranteed Income Supplement (GIS), Spouse's Allowance (SPA)",
        'Canada Pension Plan (CPP) and Quebec Pension Plan (QPP) benefits',
        'Child benefits', 'Employment Insurance (EI) benefits',
        'Social assistance', 'Other government transfers'], dtype=object),
    'Statistics': np.array([
        'Average income (excluding zeros)',
        'Median income (excluding zeros)'], dtype=object)}