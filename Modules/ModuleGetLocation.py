import requests
import pandas as pd


def cityCountMark(row):
    if ',' in row['Location']:
        return 'City'
    elif ' ' in row['Location']:
        return 'City'
    else:
        return 'County'


def updateLocation(row):
    if ',' in row['Location']:
        return row['Location']
    elif ' ' in row['Location']:
        return row['Location']
    else:
        return row['Location'].split(' ')[0] + ' County '

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
    # Add county column
    dfRent['State/Province'] = dfRent['Location']
    dfRent['cityCountMark'] = ''

    for index, row in dfRent.iterrows():
        County = row['State/Province']
        if ',' in County:
            dfRent.at[index, 'State/Province'] = County.split(',')[1].strip()
        else:
            dfRent.at[index, 'State/Province'] = County.split(' ')[0]


    dfRent['State/Province'] = dfRent['State/Province'] + ' County'
    dfRent['cityCountMark'] = dfRent.apply(cityCountMark, axis=1)
    dfRent['Location'] = dfRent.apply(updateLocation, axis = 1)
    dfRent['Country'] = 'Ireland'

    # 'Location' is the column containing location information
    dfRent_location = dfRent.groupby(['Location'])['Price'].sum()
    dfRent_location = dfRent_location.reset_index()
    dfRent_location['Coordinates'] = dfRent_location['Location'].apply(get_coordinates)
    dfRent_location[['Latitude', 'Longitude']] = pd.DataFrame(dfRent_location['Coordinates'].tolist(),
                                                              index=dfRent_location.index)

    # Left Join from the main table to the Location dictionary
    dfRent = dfRent.merge(dfRent_location[['Location', 'Coordinates', 'Latitude', 'Longitude']], on='Location',
                          how='left')

    return (dfRent)
