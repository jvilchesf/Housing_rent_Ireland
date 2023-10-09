import pandas as pd

# Display all columns by executing print
pd.set_option('display.max_columns', None)


def CleanDataRent(dfRent):
    # EDA Exploratory data analysis
    # print(dfRent.head())
    # print(dfRent.shape)
    # print(dfRent.dtypes)

    # Change columns names
    dfRent = dfRent.rename(columns={'Number of Bedrooms': 'Number_of_bedrooms',
                                    'Property Type': 'Property_Type',
                                    'VALUE': 'Price'
                                    })

    # Group by to delete columns
    # df_group = dfCensus.groupby(['Dublin_Postcodes','SubCat','S_Location','Location','RegionFilter'])['Price'].sum()

    # Drop Columns
    dfRent = dfRent.drop(columns=['STATISTIC Label', 'UNIT'])

    # Create condition to clean Nulls rows in dfRent


    indexDropRentBed = dfRent[
        (dfRent['Number_of_bedrooms'] != 'All bedrooms')|
        (dfRent['Property_Type'] != 'All property types')
        ].index

    indexDropRentPrice = dfRent[
        (dfRent['Price'] == '') &
        (dfRent['Year'].notnull()) &
        (dfRent['Location'].notnull()) &
        (dfRent['Number_of_bedrooms'] == 'All bedrooms') &
        (dfRent['Property_Type'] == 'All property types')
    ].index

    dfRent = dfRent.drop(indexDropRentBed)
    dfRent = dfRent.drop(indexDropRentPrice)

    # indexDropRent = dfRent[(dfRent['Property_Type'] != 'All property types')].index
    # dfRent = dfRent.drop(indexDropRent)

    df_group = dfRent.groupby(['Number_of_bedrooms', 'Property_Type'])['Price'].sum()

    # Parse Type
    # dfRent['Price'] = dfRent['Price'].fillna(0).astype('float')


    return dfRent


def CleanDataCens(dfCensus):
    # print(dfCensus.head())
    # print(dfCensus.dtypes)
    # print(dfCensus.values)

    df_group = dfCensus.groupby(['UNI'])['Male'].sum()
    dfCensus = dfCensus.drop(columns=['STATISTIC', 'Statistic', 'TLIST(A1)', 'UNI'])

    dfCensus = dfCensus.rename(columns={'C02779V03348': 'CensusCountyIndex',
                                        'Male': 'CensusMale',
                                        'Female': 'CensusFemale',
                                        'Both sexes': 'CensusBothSex',
                                        'CensusYear': 'Year'
                                        }
                               )

    # Parse type to INT64
    dfCensus['CensusBothSex'] = dfCensus['CensusBothSex'].fillna(0).astype('int64')
    dfCensus['CensusMale'] = dfCensus['CensusMale'].fillna(0).astype('int64')
    dfCensus['CensusFemale'] = dfCensus['CensusFemale'].fillna(0).astype('int64')

    censusGroup = dfCensus.groupby(['Year','County'])['CensusBothSex'].sum()

    return dfCensus
