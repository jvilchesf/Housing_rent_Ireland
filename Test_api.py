import requests
import pandas as pd
pd.set_option('display.max_columns', None)


url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:true,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22F1001%22%7D,%22version%22:%222.0%22%7D%7D"

# Define a function to clean characters
def clean_string(s):
    return str(s).replace('\r', '').replace('"','')

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
	result_str = data['result']
	# Split the string into lines
	lines = result_str.split('\n')
	# Extract column names from the first line
	columns = lines[0].split(',')
	# Create a list of lists for the data
	data = [line.split(',') for line in lines[1:]]
	# Create a DataFrame
	df = pd.DataFrame(data, columns=['Index',"STATISTIC Label", "Year", "Number of Bedrooms", "Property Type", "Location", "UNIT", "VALUE"])
else:
    print(f"Error connecting to API. Status code: {response.status_code}")

# Apply the clean_string function to all elements in the DataFrame
df = df.map(clean_string)

print(df)
