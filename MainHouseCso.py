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

# Import data from https://data.cso.ie/
dfRent = ModuleImportData.ImportData_rent()
dfCensus = ModuleImportData.ImportData_census()

# CleanData
dfCensus = ModuleCleanData.CleanDataCens(dfCensus)
dfRent = ModuleCleanData.CleanDataRent(dfRent)

# Add Coordinates and County Column
dfRent = ModuleGetLocation.add_location(dfRent)

# LeftJoin rent + census
dfRent = pd.merge(dfRent, dfCensus, left_on=['State/Province', 'Year'], right_on=['County', 'Year'], how='left')


# Missing Value review
print(dfRent.isnull().sum())


# Export
dfRent.to_csv('output/data_cso_ie_rent_out.csv', index=False)
dfRent = ModuleExportData.ExportDataGoogle2()
