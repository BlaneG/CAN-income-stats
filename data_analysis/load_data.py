import requests, zipfile, io


def get_csv_zip_url(table_id):
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
    
    return response.json()['object']#['object']


def get_table(table_id):
    """
    Download and extract a csv file from a table_id from statistics Canada.
    """
    zip_file_url = get_csv_zip_url(table_id)
    print('downloading zipped csv file...')
    zip_csv_response = requests.get(zip_file_url)
    print('download complete')
    zip_csv = zipfile.ZipFile(io.BytesIO(zip_csv_response.content))
    print('extracting zipped csv file')
    zip_csv.extractall()
    print('extraction complete')