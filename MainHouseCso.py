import pandas as pd
from geopy.geocoders import Nominatim
import requests

# ImportModules section
from Modules import ModuleImportData
from Modules import ModuleGetLocation
from Modules import ModuleCleanData

# Display all columns by executing print
pd.set_option('display.max_columns', None)

# Import data from https://data.cso.ie/
dfRent = ModuleImportData.ImportData_rent()
dfCensus = ModuleImportData.ImportData_census()

# CleanData
dfCensus = ModuleCleanData.CleanDataCens(dfCensus)
dfRent = ModuleCleanData.CleanDataRent(dfRent)

# Add Coordinates and County Column
df = ModuleGetLocation.add_location(dfRent)

# Missing Value review
print(df.isnull().sum())

df.to_csv('../output/data_cso_ie_rent_out.csv', index=False)
