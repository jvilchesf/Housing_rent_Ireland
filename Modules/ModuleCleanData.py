import pandas as pd

# Display all columns by executing print
pd.set_option('display.max_columns', None)


def CleanDataRent(dfRent):
    # EDA Exploratory data analysis
    print(dfRent.head())
    print(dfRent.shape)
    print(dfRent.dtypes)

    # Change columns names
    df = dfRent.rename(columns={'Number of Bedrooms': 'Number_of_bedrooms',
                                'Property Type': 'Property_Type',
                                'VALUE': 'Price'
                                })

    ##Group by to delete columns
    # df_group = df.groupby(['Dublin_Postcodes','SubCat','S_Location','Location','RegionFilter'])['Price'].sum()
    df_group = df.groupby(['UNIT'])['Price'].sum()

    ##Drop Columns
    df = df.drop(columns=['STATISTIC Label', 'UNIT'])

    return (dfRent)


def CleanDataCens(dfCensus):
    print(dfCensus.head())
    print(dfCensus.dtypes)
    print(dfCensus.values)

    df_group = dfCensus.groupby(['County', 'C02779V03348'])['Male'].sum()

    dfCensus = dfCensus.rename(columns={'C02779V03348': 'County_Index'})
    # Delete rows:
    # Population at Each Census
    # STATISTIC
    # TLIST(A1)
    # UNI

    dfCensus = dfCensus.drop(columns=['STATISTIC', 'Statistic', 'TLIST(A1)', 'UNI'])
    print(dfCensus)
    return dfCensus
