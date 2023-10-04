from Modules import ModuleImportData
import pandas as pd

# Display all columns by executing print
pd.set_option('display.max_columns', None)

df_cens = ModuleImportData.ImportData_census()
print(df_cens.head())
print(df_cens.dtypes)
print(df_cens.values)

df_group = df_cens.groupby(['County', 'C02779V03348','Year'])['Male'].sum()

df_cens = df_cens.rename(columns={'C02779V03348': 'County_Index'})
# Delete rows:
# Population at Each Census
# STATISTIC
# TLIST(A1)
# UNI

df_cens = df_cens.drop(columns=['STATISTIC', 'Statistic', 'TLIST(A1)', 'UNI'])
print(df_cens)
