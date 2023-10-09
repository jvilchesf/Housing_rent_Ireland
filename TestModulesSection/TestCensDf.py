import pandas as pd
from geopy.geocoders import Nominatim
import requests

# ImportModules section
from Modules import ModuleImportData
from Modules import ModuleGetLocation
from Modules import ModuleCleanData
from Modules import ModuleExportData

# Display all columns by executing print
pd.set_option('display.max_columns', None)

dfRent = ModuleImportData.ImportData_rent()

# Change columns names
dfRent = dfRent.rename(columns={'Number of Bedrooms': 'Number_of_bedrooms',
                                'Property Type': 'Property_Type',
                                'VALUE': 'Price'
                                })

##Group by to delete columns
# df_group = dfCensus.groupby(['Dublin_Postcodes','SubCat','S_Location','Location','RegionFilter'])['Price'].sum()
df_group = dfRent.groupby(['Location', 'Year'])['Price'].sum()

##Drop Columns
dfRent = dfRent.drop(columns=['STATISTIC Label', 'UNIT'])

# Create condition to clean Nulls rows in dfRent
deleteConditionNoPrice = (
        (dfRent['Price'] == '') &
        (dfRent['Year'].notnull()) &
        (dfRent['Location'].notnull()) &
        (dfRent['Number_of_bedrooms'] == 'All bedrooms') &
        (dfRent['Property_Type'] == 'All property types')
)

# Create delete condition for propertyType and Bedrooms, to much nulls
deleteConditioTypeBed = (
        (dfRent['Number_of_bedrooms'] != 'All bedrooms') &
        (dfRent['Property_Type'] != 'All property types')
)

# Apply the condition to filter the DataFrame and keep the rows where the condition is False
dfRent = dfRent[~deleteConditionNoPrice]
dfRent = dfRent[~deleteConditioTypeBed]

# Parse Type
# dfRent['Price'] = dfRent['Price'].str[1:]
# dfRent['Price'] = dfRent['Price'].astype(float)

# Checking if a comma is present before splitting
# print(dfRent['Location'].str.split(',', expand=True))
# print(dfRent['Location'].str.split(' ', expand=True))

# dfRent['Location'] = dfRent['Location'].str.split(',', 1).str[1] if dfRent['Location'].str.contains(',') else dfRent['Location']#

# if dfRent['Location'].str.contains(',').any() == 'True':
#    dfRent['Split_Location'] = dfRent['Location'].str.split(',')[1]
# else:
#    dfRent['Split_Location'] = dfRent['Location'].str.split(' ')[0]
dfRent['County'] = dfRent['Location']

for index, row in dfRent.iterrows():
    County = row['County']
    if ',' in County:
        dfRent.at[index, 'County'] = County.split(',')[1].strip()
    else:
        dfRent.at[index, 'County'] = County.split(' ')[0]

print(dfRent.head())
# dfRent['Location'] = dfRent['Location'].apply(lambda x: 'Even' if x % 2 == 0 else 'Odd')

# dfRent['County'] = dfRent['Location'].str.split(',').str[1] if dfRent['Location'].str.contains(',') else \
# dfRent['Location'].str.split(' ')[0]
