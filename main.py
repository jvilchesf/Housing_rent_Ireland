import pandas as pd
from geopy.geocoders import Nominatim
import requests



pd.set_option('display.max_columns', None)

#Import Data
df = pd.read_csv('../Sources/Residential_Rental_Market_Prices_(RTB).csv')

#EDA Exploratory data analysis
#print(df.head())
#print(df.shape)
#print(df.dtypes)


#Change columns names
df= df.rename(columns = {'Values_' : 'Price'
                        })
#Missing Value review
#print(df.isnull().sum())

#Group by to delete columns
df_group = df.groupby(['Dublin_Postcodes','SubCat','S_Location','Location','RegionFilter'])['Price'].sum()
#df_group = df.groupby(['Status'])['Price'].sum()

#Drop Columns
df = df.drop(columns = ['Dublin_Postcodes','SubCat','ObjectId'])

#Add GeoCode Location
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


#'S_Location' is the column containing location information
df_location = df.groupby(['Location'])['Price'].sum()
df_location = df_location.reset_index()
df_location['Coordinates'] = df_location['Location'].apply(get_coordinates)
df_location[['Latitude', 'Longitude']] = pd.DataFrame(df_location['Coordinates'].tolist(), index=df_location.index)

#Left Join from the main table to the Location dictionary
df = df.merge(df_location[['Location', 'Coordinates', 'Latitude', 'Longitude']], on='Location', how='left')


df.to_csv('Rent_Prices_Ireland.csv', index=False)

