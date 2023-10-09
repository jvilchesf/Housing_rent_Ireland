import requests
import re
import pandas as pd


# Import Data

def ImportData_rent():
    url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22RIA02%22%7D,%22version%22:%222.0%22%7D%7D"
    # Define the JSON-RPC request payload
    payload_rent = {
        "jsonrpc": "2.0",
        "method": "PxStat.Data.Cube_API.ReadDataset",
        "params": {
            "class": "query",
            "id": [],
            "dimension": {},
            "extension": {
                "language": {
                    "code": "en"
                },
                "format": {
                    "type": "CSV",
                    "version": "1.0"
                },
                "matrix": "RIA02"
            },
            "version": "2.0"
        }
    }

    # Make the POST request
    response_rent = requests.post(url, json=payload_rent)

    # Check if the request was successful (status code 200)
    if response_rent.status_code == 200:
        data = response_rent.json()
        data_result = data['result']
        lines = data_result.split('\r')
        data_result = [re.findall(r'"([^"]*)"', line) for line in lines[1:]]
        df = pd.DataFrame(data_result,
                          columns=['STATISTIC Label', 'Year', 'Number of Bedrooms', 'Property Type', 'Location', 'UNIT',
                                   'VALUE'])
    else:
        print(f"Error connecting to API. Status code: {response_rent.status_code}")

    return df


def ImportData_census():
    payload_census = {
        "jsonrpc": "2.0",
        "method": "PxStat.Data.Cube_API.ReadDataset",
        "params": {
            "class": "query",
            "id": [],
            "dimension": {},
            "extension": {
                "pivot": "C02199V02655",
                "codes": 1,
                "language": {
                    "code": "en"
                },
                "format": {
                    "type": "CSV",
                    "version": "1.0"
                },
                "matrix": "F1001"
            },
            "version": "2.0"
        }
    }
    url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22RIA02%22%7D,%22version%22:%222.0%22%7D%7D"
    # Make the POST request
    response_census = requests.post(url, json=payload_census)

    if response_census.status_code == 200:
        data_census = response_census.json()
        data_result_census = data_census['result']
        lines_census = data_result_census.split('\r')
        data_result_census = [re.findall(r'"([^"]*)"', line) for line in lines_census[1:]]
        df_census = pd.DataFrame(data_result_census,
                                 columns=['STATISTIC', 'Statistic', 'TLIST(A1)', 'CensusYear', 'C02779V03348', 'County',
                                          'UNI', 'Both sexes', 'Male', 'Female'])
    else:
        print(f"Error connecting to API. Status code: {response_census.status_code}")

    return df_census
