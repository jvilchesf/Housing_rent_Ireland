import requests
import pandas as pd

url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22CSV%22,%22version%22:%221.0%22%7D,%22matrix%22:%22RIA02%22%7D,%22version%22:%222.0%22%7D%7D"

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

	# Assuming data['result'] contains the relevant information
	df = pd.json_normalize(data['result'])
	print(df)
else:
    print(f"Error connecting to API. Status code: {response.status_code}")