import pandas as pd
from geopy.geocoders import Nominatim
import requests

import ImportDataModule

pd.set_option('display.max_columns', None)

df= ImportDataModule.ImportData_rent()
df_Census= ImportDataModule.ImportData_census()

# EDA Exploratory data analysis
print(df.head())
print(df.shape)
print(df.dtypes)

# Change columns names

df = df.rename(columns={'Number of Bedrooms': 'Number_of_bedrooms',
                        'Property Type': 'Property_Type',
                        'VALUE': 'Price'
                        })

##Group by to delete columns
# df_group = df.groupby(['Dublin_Postcodes','SubCat','S_Location','Location','RegionFilter'])['Price'].sum()
df_group = df.groupby(['UNIT'])['Price'].sum()
print(df_group)

##Drop Columns
df = df.drop(columns=['STATISTIC Label', 'UNIT'])


# Add GeoCode Location
def get_coordinates(location):
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={location}")
        location_data = response.json()

        if location_data:
            return (location_data[0]['lat'], location_data[0]['lon'])
        else:
            return (None, None)  # Handle case where location is not found
    except Exception as e:
        print(f"Error occurred: {e}")
        return (None, None)  # Handle other potential errors


# 'S_Location' is the column containing location information
df_location = df.groupby(['Location'])['Price'].sum()
df_location = df_location.reset_index()
df_location['Coordinates'] = df_location['Location'].apply(get_coordinates)
df_location[['Latitude', 'Longitude']] = pd.DataFrame(df_location['Coordinates'].tolist(), index=df_location.index)

# Left Join from the main table to the Location dictionary
df = df.merge(df_location[['Location', 'Coordinates', 'Latitude', 'Longitude']], on='Location', how='left')

# Add county column
# Create a new column "County" by splitting the "location" column
df['County'] = df['Location'].str.split(',', expand=True)[1]
# If there is no comma, "County" will be the same as "location"
df['County'].fillna(df['Location'], inplace=True)
# Update the "location" column to contain the word before the comma
df['Location'] = df['Location'].str.split(',').str[0]

##Missing Value review
print(df.isnull().sum())

df.to_csv('../output/data_cso_ie_rent_out.csv', index=False)
