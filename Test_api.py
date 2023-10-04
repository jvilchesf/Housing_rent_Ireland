import requests
import pandas as pd
import re
import json

pd.set_option('display.max_columns', None)

url = "https://ws.cso.ie/public/api.jsonrpc"


# Define a function to clean characters
def clean_string(s):
	return str(s).replace('\r', '').replace('"', '')


# Define the JSON-RPC request payload

# Define the JSON-RPC request payload
payload = {
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
response = requests.post(url, json=payload)

# Check if the request was successful (status code 200)
if response.status_code == 200:
	data = response.json()
	data_result = data['result']
	lines = data_result.split('\r')
	#print(lines)
	data_result = [re.findall(r'"([^"]*)"', line) for line in lines[1:]]
	#df = pd.DataFrame(data_result, columns=['Year Label', 'Year', 'Bedrooms Label', 'Property Type Label', 'Value'])
	print(data_result)
else:
	print(f"Error connecting to API. Status code: {response.status_code}")
