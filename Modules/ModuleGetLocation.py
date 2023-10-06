import requests
import pandas as pd


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


def add_location(dfRent):
    # 'S_Location' is the column containing location information
    dfRent_location = dfRent.groupby(['Location'])['Price'].sum()
    dfRent_location = dfRent_location.reset_index()
    dfRent_location['Coordinates'] = dfRent_location['Location'].apply(get_coordinates)
    dfRent_location[['Latitude', 'Longitude']] = pd.DataFrame(dfRent_location['Coordinates'].tolist(), index=dfRent_location.index)

    # Left Join from the main table to the Location dictionary
    dfRent = dfRent.merge(dfRent_location[['Location', 'Coordinates', 'Latitude', 'Longitude']], on='Location', how='left')

    # Add county column
    # Create a new column "County" by splitting the "location" column
    dfRent['County'] = dfRent['Location'].str.split(',', expand=True)[1]
    # If there is no comma, "County" will be the same as "location"
    dfRent['County'].fillna(dfRent['Location'], inplace=True)
    # Update the "location" column to contain the word before the comma
    dfRent['Location'] = dfRent['Location'].str.split(',').str[0]

    return (dfRent)
