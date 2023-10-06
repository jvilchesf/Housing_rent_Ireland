from Modules import ModuleImportData
import pandas as pd

# Display all columns by executing print
pd.set_option('display.max_columns', None)

df_cens = ModuleImportData.ImportData_census()
print(df_cens.head())
#print(df_cens.dtypes)
#print(df_cens.values)

df_group = df_cens.groupby(['UNI'])['Male'].sum()
df_cens = df_cens.drop(columns=['STATISTIC', 'Statistic', 'TLIST(A1)', 'UNI'])

df_cens = df_cens.rename(columns={'C02779V03348': 'CensusCountyIndex',
                                  'Male': 'CensusMale',
                                  'Female': 'CensusFemale',
                                  'Both sexes': 'CensusBothSex',
                                  'County': 'CensusCounty',
                                  'CensusYear': 'Year'
                                  }
                         )
#print(df_cens.dtypes)


