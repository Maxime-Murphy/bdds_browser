import streamlit as st
import uisdata.bdds as ud
import datetime
import pandas as pd

# %% Get archive list
#Cached because it call the online CSV each time

@st.cache
def get_archives_list():
    """
    Get the archive name dictionary and inverse to label:acronym 

    Returns
    -------
    Dict
        A Dict of all archive label:acronym for instantiating the BDDS class.

    """
    dict_name_label = ud.bdds("SDG").dictNameLabel
    dict_label_name = {}
    for acr, label in dict.items(dict_name_label):
        dict_label_name[label]=acr
        
    return dict_label_name    
    

#Function for instantiating an archive 
    # !!! WARNING do not cache, will CRASH : instantiation cannot be cached
def inst_archive(arch_name):
    """
    Instantiate the bdds class with the user selected archive

    Parameters
    ----------
    arch_name : String
        The name of the archive.

    Returns
    -------
    archive : BDDS Object
        The bdds class instantiated with an archive name.

    """
    archive = ud.bdds(arch_name)
    return archive
        

#Getting the data of the instantiated class
@st.cache
def getData(archive):
    #Add DocStrings
    dict_tables = archive.dataTables()     # create table dictionary
    
    return dict_tables

#Some core data wrangling (core dataset and variables for populating the different widget)
    #underscore on "_my_archive" parameter added to specify unhashable object
@st.experimental_memo
def varCreation(_my_archive, dict_tables):
# def varCreation(sel_geotype, my_archive, dict_tables):
# if sel_geotype == "Country":
    df_c = _my_archive.allLabelMerge(dict_tables, dict_tables["DATA_NATIONAL"])         # extracting the national data from the dict
    df_c = df_c[["INDICATOR_ID", "COUNTRY_NAME_EN","YEAR", "VALUE", "MAGNITUDE", "QUALIFIER", "INDICATOR_LABEL_EN", "COUNTRY_ID"]]

    #Dictionaries id:label (country and indicators)
        #!!! Invert dict to be id:label (label are sometimes missing)    
    dict_country_c = dict(zip(df_c.COUNTRY_NAME_EN.astype(str), df_c.COUNTRY_ID.astype(str)))     # getting all countries
    dict_indic_c = dict(zip(df_c.INDICATOR_LABEL_EN.astype(str), df_c.INDICATOR_ID.astype(str)))
    
    # Unique values
    # lst_count_lab = pd.unique(df["COUNTRY_NAME_EN"])          # getting all years
    # lst_indic_lab = pd.unique(df["INDICATOR_LABEL_EN"])          # getting all years
    lst_count_lab_c = sorted([label for label in dict_country_c])
    lst_indic_lab_c = sorted([label for label in dict_indic_c])

    geo_c = pd.unique(df_c["COUNTRY_ID"])      # getting all countries
    year_c = pd.unique(df_c["YEAR"])          # getting all years
    indic_c = pd.unique(df_c["INDICATOR_ID"])     # getting all indics

    try:                                        # try because some archive have no meta
        meta_c = dict_tables["METADATA"]          # getting metadata file
    except KeyError:
        meta_c = None
    
# elif sel_geotype == "Region":
    try:                                            #try because some archive have no regionals data
        df_r = _my_archive.allLabelMerge(dict_tables, dict_tables["DATA_REGIONAL"], geoType="Region")         # extracting the national data from the dict
        df_r = df_r[["INDICATOR_ID", "REGION_ID", "YEAR", "VALUE", "MAGNITUDE", "QUALIFIER", "INDICATOR_LABEL_EN"]]

    #Dictionaries id:label (indicators)
        #!!! Invert dict to be id:label (label are sometimes missing)    
        dict_indic_r = dict(zip(df_r.INDICATOR_LABEL_EN.astype(str), df_r.INDICATOR_ID.astype(str))) 
        dict_country_r = None
        
        lst_indic_lab_r = sorted([label for label in dict_indic_r])
        lst_count_lab_r = None

        # Keep geo because region is alaready named without acronym
        geo_r = pd.unique(df_r["REGION_ID"])      # getting all regions
        year_r = pd.unique(df_r["YEAR"])          # getting all years
        indic_r = pd.unique(df_r["INDICATOR_ID"]) # getting all indics

        meta_r = None                                 # no metadata for regional data
    except KeyError:
        df_r = None
        dict_country_r = None
        dict_indic_r = None
        lst_count_lab_r = None
        lst_indic_lab_r = None
        geo_r = None
        year_r = None
        indic_r = None
        meta_r = None

            
    return (df_c, dict_country_c, dict_indic_c, lst_count_lab_c, lst_indic_lab_c, 
            geo_c, year_c, indic_c, meta_c, df_r, dict_country_r, dict_indic_r, 
            lst_count_lab_r, lst_indic_lab_r, geo_r, year_r, indic_r, meta_r)


# df, dict_country, dict_indic, lst_count_lab, lst_indic_lab, geo, year, indic, meta
# df_c, dict_country_c, dict_indic_c, lst_count_lab_c, lst_indic_lab_c, geo_c, year_c, indic_c, meta_c
# df_r, dict_country_r, dict_indic_r, lst_count_lab_r, lst_indic_lab_r, geo_r, year_r, indic_r, meta_r


# function for converting dataFrame to csv
def df_to_csv(df):
    return df.to_csv().encode('utf-8')

# For adding date and creating a unique file name when downloading
def fileDate():
    rawDate = str(datetime.datetime.today())
    trimedDate=rawDate[:19]                 #Get date up to the seconds
    cleanedDate=trimedDate.replace('-', '').replace(' ', "-").replace(":","")
    return cleanedDate















